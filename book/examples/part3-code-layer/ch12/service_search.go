/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     code-layer-reference-impl
// source_path:     reference-impl/code-kg/service.go
// commit_sha:      7afa52003fd6  (dirty — uncommitted changes)
// captured_at:     2026-04-18T01:15:58Z
// content_sha256:  930a1780a8fd8a076f571b3a7d77e7d9178f9e9c121f3d5da0764062942eb0d8
// regenerate with: make book-refresh-excerpts
 */

package ckg

import (
	"crypto/sha256"
	"database/sql"
	"fmt"
	"os"
	"strings"
	"time"

	sqlite_vec "github.com/asg017/sqlite-vec-go-bindings/cgo"
	"github.com/google/uuid"
	codeenricher "example.com/reference-impl/code-kg/enricher"
	"example.com/reference-impl/code-kg/generator"
	codeparser "example.com/reference-impl/code-kg/parser"
	"example.com/reference-impl/code-kg/retriever"
	"example.com/reference-impl/code-kg/store/pgvector"
	"example.com/reference-impl/code-kg/syncer"
	"example.com/reference-impl/code-kg-repo/internal/llm"
	ilog "example.com/reference-impl/code-kg-repo/internal/log"
	"example.com/reference-impl/code-kg-repo/internal/rag"
	"gorm.io/gorm"
)

func init() {
	sqlite_vec.Auto()
}

type Service struct {
	db          *gorm.DB
	sqlDB       *sql.DB
	config      Config
	parser      *codeparser.Service
	enricher    *codeenricher.Service
	vectorStore pgvector.Store
	graphStore  GraphStore
	syncTracker *syncer.Tracker[*SyncStatus]
}

func NewService(db *gorm.DB) *Service {
	if err := AutoMigrate(db); err != nil {
		ilog.GetLogger().Errorf("Failed to auto-migrate codekg tables: %v", err)
	}

	sqlDB, err := db.DB()
	if err != nil {
		ilog.GetLogger().Errorf("Failed to get sql.DB for sqlite-vec: %v", err)
	}

	config := LoadConfigFromEnv()
	var embedder *rag.EmbeddingService
	apiKey := config.Embedding.APIKey
	if apiKey != "" {
		embedder = rag.NewEmbeddingService(rag.EmbeddingConfig{
			APIKey:  apiKey,
			BaseURL: config.Embedding.BaseURL,
			Model:   config.Embedding.Model,
		})
	}

	var vectorStore pgvector.Store
	if sqlDB != nil {
		vectorStore = pgvector.NewSQLiteVecStore(sqlDB)
	}

	return &Service{
		db:          db,
		sqlDB:       sqlDB,
		config:      config,
		parser:      codeparser.New(),
		enricher:    codeenricher.New(embedder),
		vectorStore: vectorStore,
		graphStore:  newGraphStoreFromConfig(config.Graph),
		syncTracker: syncer.NewTracker[*SyncStatus](),
	}
}

func (s *Service) RegisterRepo(repo *Repository) error {
	if repo.ID == "" {
		repo.ID = uuid.New().String()[:8]
	}
	if repo.Branch == "" {
		repo.Branch = "main"
	}
	if repo.SourceType == "" {
		repo.SourceType = "local_path"
	}
	return s.db.Create(repo).Error
}

func (s *Service) ListRepos() ([]Repository, error) {
	var repos []Repository
	err := s.db.Order("created_at desc").Find(&repos).Error
	return repos, err
}

func (s *Service) GetRepo(id string) (*Repository, error) {
	var repo Repository
	err := s.db.First(&repo, "id = ?", id).Error
	return &repo, err
}

func (s *Service) DeleteRepo(id string) error {
	s.deleteVecEntries(id)
	s.db.Unscoped().Where("repo_id = ?", id).Delete(&KnowledgeDoc{})
	s.db.Unscoped().Where("repo_id = ?", id).Delete(&Entity{})
	return s.db.Unscoped().Delete(&Repository{}, "id = ?", id).Error
}

func (s *Service) GetSyncStatus(repoID string) *SyncStatus {
	if status, ok := s.syncTracker.Get(repoID); ok {
		return status
	}
	var job SyncJob
	if err := s.db.Where("repo_id = ?", repoID).Order("created_at desc").First(&job).Error; err == nil {
		status := syncJobToStatus(job)
		s.syncTracker.Set(repoID, status)
		return status
	}
	return &SyncStatus{Status: "idle"}
}

func (s *Service) TriggerSync(repoID string) (string, error) {
	repo, err := s.GetRepo(repoID)
	if err != nil {
		return "", fmt.Errorf("repository not found: %w", err)
	}

	repoPath := repo.LocalPath
	if repoPath == "" {
		repoPath = repo.URL
	}
	if repoPath == "" {
		return "", fmt.Errorf("no local_path or url configured for repo %s", repo.Name)
	}

	jobID := uuid.New().String()[:8]
	startedAt := time.Now()
	status := &SyncStatus{
		JobID:         jobID,
		Status:        "running",
		Phase:         string(SyncPhaseQueued),
		TriggerSource: s.config.Sync.DefaultTriggerSource,
		StartedAt:     &startedAt,
	}
	s.syncTracker.Set(repoID, status)
	if err := s.persistSyncStatus(repoID, status); err != nil {
		return "", err
	}

	s.db.Model(repo).Update("status", "syncing")

	if syncer.IsGitRepo(repoPath) && repo.LastSuccessfulCommit != "" {
		diff, err := syncer.ComputeGitDiff(repoPath, repo.LastSuccessfulCommit)
		if err == nil && !diff.IsFullSync && diff.Changes != nil {
			go s.runIncrementalSync(repo, repoPath, status, diff)
			return jobID, nil
		}
	}

	go s.runSync(repo, repoPath, status)

	return jobID, nil
}

func (s *Service) runSync(repo *Repository, repoPath string, status *SyncStatus) {
	defer func() {
		if r := recover(); r != nil {
			status.Status = "failed"
			status.Phase = string(SyncPhaseFailed)
			status.Error = fmt.Sprintf("panic: %v", r)
			finishedAt := time.Now()
			status.FinishedAt = &finishedAt
			_ = s.persistSyncStatus(repo.ID, status)
		}
	}()

	status.Phase = string(SyncPhaseScanning)
	_ = s.persistSyncStatus(repo.ID, status)
	codeFiles, err := s.collectCodeFiles(repoPath)
	if err != nil {
		status.Status = "failed"
		status.Phase = string(SyncPhaseFailed)
		status.Error = fmt.Sprintf("failed to scan directory: %v", err)
		finishedAt := time.Now()
		status.FinishedAt = &finishedAt
		_ = s.persistSyncStatus(repo.ID, status)
		s.db.Model(repo).Updates(map[string]interface{}{"status": "failed"})
		return
	}

	status.TotalFiles = len(codeFiles)
	if len(codeFiles) == 0 {
		status.Status = "completed"
		status.Phase = string(SyncPhaseCompleted)
		now := time.Now()
		status.FinishedAt = &now
		_ = s.persistSyncStatus(repo.ID, status)
		s.db.Model(repo).Updates(map[string]interface{}{"status": "idle", "last_sync": &now})
		return
	}

	s.db.Unscoped().Where("repo_id = ?", repo.ID).Delete(&Entity{})
	s.deleteVecEntries(repo.ID)

	var allEntities []Entity
	var parsedFiles []parsedFile
	status.Phase = string(SyncPhaseParsing)
	_ = s.persistSyncStatus(repo.ID, status)
	for _, filePath := range codeFiles {
		parsed := s.parseFileForSync(repo.ID, repoPath, filePath)
		if parsed.Metadata != nil {
			parsedFiles = append(parsedFiles, parsed)
		}
		allEntities = append(allEntities, parsed.Entities...)
		status.ProcessedFiles++
		status.EntitiesCreated += len(parsed.Entities)
		_ = s.persistSyncStatus(repo.ID, status)
	}

	batchSize := 100
	for i := 0; i < len(allEntities); i += batchSize {
		end := i + batchSize
		if end > len(allEntities) {
			end = len(allEntities)
		}
		if err := s.db.CreateInBatches(allEntities[i:end], batchSize).Error; err != nil {
			ilog.GetLogger().Errorf("Failed to save entities batch: %v", err)
		}
	}

	if s.enricher.Available() && len(allEntities) > 0 {
		status.Phase = string(SyncPhaseEmbedding)
		_ = s.persistSyncStatus(repo.ID, status)
		s.generateAndStoreEmbeddings(allEntities)
	}

	if s.graphStore != nil {
		status.Phase = string(SyncPhaseGraph)
		_ = s.persistSyncStatus(repo.ID, status)
		graphEntities, graphRelations := buildGraphData(repo.ID, parsedFiles)
		if err := s.graphStore.UpsertRepositoryGraph(repo.ID, repo.Name, graphEntities, graphRelations); err != nil {
			status.Status = "failed"
			status.Phase = string(SyncPhaseFailed)
			status.Error = fmt.Sprintf("failed to sync graph to memgraph: %v", err)
			finishedAt := time.Now()
			status.FinishedAt = &finishedAt
			_ = s.persistSyncStatus(repo.ID, status)
			s.db.Model(repo).Updates(map[string]interface{}{"status": "failed"})
			return
		}
	}

	status.Phase = string(SyncPhaseDocs)
	_ = s.persistSyncStatus(repo.ID, status)
	s.generateKnowledgeDocs(repo, repoPath, allEntities, codeFiles)

	now := time.Now()
	updates := map[string]interface{}{
		"status":                 "idle",
		"last_sync":              &now,
		"last_successful_sync":   &now,
		"last_successful_job_id": status.JobID,
	}
	if syncer.IsGitRepo(repoPath) {
		if headCommit, err := syncer.HeadCommit(repoPath); err == nil {
			updates["last_commit"] = headCommit
			updates["last_successful_commit"] = headCommit
		}
	}
	s.db.Model(repo).Updates(updates)
	status.Status = "completed"
	status.Phase = string(SyncPhaseCompleted)
	status.FinishedAt = &now
	_ = s.persistSyncStatus(repo.ID, status)
}

func (s *Service) runIncrementalSync(repo *Repository, repoPath string, status *SyncStatus, diff *syncer.DiffResult) {
	defer func() {
		if r := recover(); r != nil {
			status.Status = "failed"
			status.Phase = string(SyncPhaseFailed)
			status.Error = fmt.Sprintf("panic: %v", r)
			finishedAt := time.Now()
			status.FinishedAt = &finishedAt
			_ = s.persistSyncStatus(repo.ID, status)
		}
	}()

	supported := syncer.FilterSupportedChanges(diff.Changes, repoPath)
	if len(supported) == 0 {
		now := time.Now()
		status.Status = "completed"
		status.Phase = string(SyncPhaseCompleted)
		status.FinishedAt = &now
		_ = s.persistSyncStatus(repo.ID, status)
		s.db.Model(repo).Updates(map[string]interface{}{
			"status":                 "idle",
			"last_sync":              &now,
			"last_commit":            diff.ToCommit,
			"last_successful_commit": diff.ToCommit,
			"last_successful_sync":   &now,
			"last_successful_job_id": status.JobID,
		})
		return
	}

	status.TotalFiles = len(supported)
	status.Phase = string(SyncPhaseParsing)
	_ = s.persistSyncStatus(repo.ID, status)

	var newEntities []Entity
	var parsedFiles []parsedFile

	for _, change := range supported {
		fullPath := repoPath + "/" + change.Path

		switch change.Status {
		case syncer.StatusDeleted:
			relPath := codeparser.RelativePath(repoPath, fullPath)
			s.db.Unscoped().Where("repo_id = ? AND file_path = ?", repo.ID, relPath).Delete(&Entity{})
			var deletedEntities []Entity
			s.db.Where("repo_id = ? AND file_path = ?", repo.ID, relPath).Find(&deletedEntities)
			status.EntitiesDeleted += len(deletedEntities)

		case syncer.StatusAdded, syncer.StatusModified:
			relPath := codeparser.RelativePath(repoPath, fullPath)
			s.db.Unscoped().Where("repo_id = ? AND file_path = ?", repo.ID, relPath).Delete(&Entity{})

			parsed := s.parseFileForSync(repo.ID, repoPath, fullPath)
			if parsed.Metadata != nil {
				parsedFiles = append(parsedFiles, parsed)
			}
			newEntities = append(newEntities, parsed.Entities...)
			status.EntitiesCreated += len(parsed.Entities)
		}

		status.ProcessedFiles++
		_ = s.persistSyncStatus(repo.ID, status)
	}

	if len(newEntities) > 0 {
		batchSize := 100
		for i := 0; i < len(newEntities); i += batchSize {
			end := i + batchSize
			if end > len(newEntities) {
				end = len(newEntities)
			}
			if err := s.db.CreateInBatches(newEntities[i:end], batchSize).Error; err != nil {
				ilog.GetLogger().Errorf("Failed to save entities batch: %v", err)
			}
		}
	}

	if s.enricher.Available() && len(newEntities) > 0 {
		status.Phase = string(SyncPhaseEmbedding)
		_ = s.persistSyncStatus(repo.ID, status)
		s.generateAndStoreEmbeddings(newEntities)
	}

	if s.graphStore != nil && len(parsedFiles) > 0 {
		status.Phase = string(SyncPhaseGraph)
		_ = s.persistSyncStatus(repo.ID, status)
		graphEntities, graphRelations := buildGraphData(repo.ID, parsedFiles)
		if err := s.graphStore.UpsertRepositoryGraph(repo.ID, repo.Name, graphEntities, graphRelations); err != nil {
			ilog.GetLogger().Warnf("Incremental graph update failed: %v", err)
		}
	}

	status.Phase = string(SyncPhaseDocs)
	_ = s.persistSyncStatus(repo.ID, status)

	var allEntities []Entity
	s.db.Where("repo_id = ?", repo.ID).Find(&allEntities)
	allCodeFiles, _ := s.collectCodeFiles(repoPath)
	s.generateKnowledgeDocs(repo, repoPath, allEntities, allCodeFiles)

	now := time.Now()
	s.db.Model(repo).Updates(map[string]interface{}{
		"status":                 "idle",
		"last_sync":              &now,
		"last_commit":            diff.ToCommit,
		"last_successful_commit": diff.ToCommit,
		"last_successful_sync":   &now,
		"last_successful_job_id": status.JobID,
	})
	status.Status = "completed"
	status.Phase = string(SyncPhaseCompleted)
	status.FinishedAt = &now
	_ = s.persistSyncStatus(repo.ID, status)
}

func (s *Service) collectCodeFiles(rootPath string) ([]string, error) {
	return s.parser.CollectSupportedFiles(rootPath)
}

func (s *Service) parseFile(repoID, repoRoot, filePath string) []Entity {
	return s.parseFileForSync(repoID, repoRoot, filePath).Entities
}

func (s *Service) parseFileForSync(repoID, repoRoot, filePath string) parsedFile {
	metadata, err := s.parser.ParseFile(filePath)
	if err != nil {
		ilog.GetLogger().Warnf("Failed to parse %s: %v", filePath, err)
		return parsedFile{}
	}

	relPath := codeparser.RelativePath(repoRoot, filePath)

	var entities []Entity

	for _, fn := range metadata.Functions {
		entities = append(entities, Entity{
			ID:         entityID(repoID, relPath, "function", fn.Name, fn.StartLine),
			RepoID:     repoID,
			EntityType: "function",
			Name:       fn.Name,
			FilePath:   relPath,
			StartLine:  fn.StartLine,
			EndLine:    fn.EndLine,
			Signature:  extractSignature(fn.Content),
			DocString:  fn.Comment,
			Body:       truncate(fn.Content, 4000),
			Language:   string(metadata.Language),
		})
	}

	for _, cls := range metadata.Classes {
		entities = append(entities, Entity{
			ID:         entityID(repoID, relPath, "class", cls.Name, cls.StartLine),
			RepoID:     repoID,
			EntityType: "class",
			Name:       cls.Name,
			FilePath:   relPath,
			StartLine:  cls.StartLine,
			EndLine:    cls.EndLine,
			Signature:  extractSignature(cls.Content),
			DocString:  cls.Comment,
			Body:       truncate(cls.Content, 4000),
			Language:   string(metadata.Language),
		})
	}

	return parsedFile{
		RepoID:   repoID,
		FullPath: filePath,
		RelPath:  relPath,
		Metadata: metadata,
		Entities: entities,
	}
}

func (s *Service) generateAndStoreEmbeddings(entities []Entity) {
	if s.vectorStore == nil || !s.enricher.Available() {
		ilog.GetLogger().Warn("vector store or embedding service unavailable, skipping embedding storage")
		return
	}

	const batchSize = 50
	for i := 0; i < len(entities); i += batchSize {
		end := i + batchSize
		if end > len(entities) {
			end = len(entities)
		}

		var texts []string
		for _, e := range entities[i:end] {
			texts = append(texts, codeenricher.BuildEntityInput(e.Language, e.EntityType, e.Name, e.Signature, e.DocString))
		}

		embeddings, err := s.enricher.GenerateEmbeddings(texts)
		if err != nil {
			ilog.GetLogger().Warnf("Failed to generate embeddings for batch %d: %v", i/batchSize, err)
			continue
		}

		for j, emb := range embeddings {
			eid := entities[i+j].ID
			if err := s.vectorStore.Upsert(eid, emb); err != nil {
				ilog.GetLogger().Warnf("Failed to store embedding for %s: %v", eid, err)
			}
		}
	}
}

func (s *Service) Search(req SearchRequest) (*SearchResult, error) {
	if req.TopK <= 0 {
		req.TopK = s.config.Retrieval.DefaultTopK
	}

	var entities []Entity

	if s.enricher.Available() && s.vectorStore != nil {
		ranked, err := s.searchByVec(req)
		if err != nil {
			ilog.GetLogger().Warnf("Vec search failed, falling back to keyword: %v", err)
			entities = s.keywordFallback(req)
		} else {
			entities = ranked
		}
	} else {
		entities = s.keywordFallback(req)
	}

	answer, err := s.generateAnswer(req.Query, entities)
	if err != nil {
		ilog.GetLogger().Warnf("Failed to generate answer: %v", err)
		answer = "Failed to generate answer. See matched code entities below."
	}

	return &SearchResult{
		Entities: entities,
		Answer:   answer,
	}, nil
}

// searchByVec uses sqlite-vec KNN to find the closest entity embeddings.
func (s *Service) searchByVec(req SearchRequest) ([]Entity, error) {
	queryEmb, err := s.enricher.GenerateEmbedding(req.Query)
	if err != nil {
		return nil, fmt.Errorf("embed query: %w", err)
	}

	matches, err := s.vectorStore.Search(queryEmb, req.TopK)
	if err != nil {
		return nil, fmt.Errorf("vec knn query: %w", err)
	}

	var ids []string
	for _, match := range matches {
		ids = append(ids, match.EntityID)
	}
	if len(ids) == 0 {
		return nil, nil
	}

	var entities []Entity
	q := s.db.Where("id IN ?", ids)
	if req.RepoID != "" {
		q = q.Where("repo_id = ?", req.RepoID)
	}
	if req.EntityType != "" {
		q = q.Where("entity_type = ?", req.EntityType)
	}
	q.Select("id, repo_id, entity_type, name, file_path, start_line, end_line, signature, doc_string, body, summary, language, created_at").
		Find(&entities)

	idOrder := make(map[string]int, len(ids))
	for i, id := range ids {
		idOrder[id] = i
	}
	sortedEntities := make([]Entity, len(entities))
	copy(sortedEntities, entities)
	for i := 0; i < len(sortedEntities); i++ {
		for j := i + 1; j < len(sortedEntities); j++ {
			if idOrder[sortedEntities[j].ID] < idOrder[sortedEntities[i].ID] {
				sortedEntities[i], sortedEntities[j] = sortedEntities[j], sortedEntities[i]
			}
		}
	}
	return sortedEntities, nil
}

func (s *Service) keywordFallback(req SearchRequest) []Entity {
	var entities []Entity
	query := s.db.Where("1=1")
	if req.RepoID != "" {
		query = query.Where("repo_id = ?", req.RepoID)
	}
	if req.EntityType != "" {
		query = query.Where("entity_type = ?", req.EntityType)
	}
	query.Find(&entities)
	return s.rankByKeyword(req.Query, entities, req.TopK)
}

func (s *Service) rankByKeyword(query string, entities []Entity, topK int) []Entity {
	var docs []retriever.Document
	entityByID := make(map[string]Entity, len(entities))
	for i, e := range entities {
		docID := e.ID
		if docID == "" {
			docID = fmt.Sprintf("__rank_%d", i)
		}
		entityByID[docID] = e
		docs = append(docs, retriever.Document{ID: docID, Name: e.Name, Body: e.Body})
	}

	results := retriever.RankByKeyword(query, docs, topK)

	var out []Entity
	for _, result := range results {
		out = append(out, entityByID[result.ID])
	}
	return out
}

func (s *Service) generateAnswer(query string, entities []Entity) (string, error) {
	settings := llm.LLMSettings{
		BaseUrl:     s.config.Generation.BaseURL,
		ApiKey:      s.config.Generation.APIKey,
		Model:       s.config.Generation.Model,
		Temperature: s.config.Generation.Temperature,
	}
	if settings.ApiKey == "" {
		return "LLM API key not configured. Cannot generate answer.", nil
	}

	var snippets []generator.Snippet
	for _, e := range entities {
		snippets = append(snippets, generator.Snippet{
			EntityType: e.EntityType,
			Name:       e.Name,
			FilePath:   e.FilePath,
			StartLine:  e.StartLine,
			EndLine:    e.EndLine,
			Body:       truncate(e.Body, 1500),
		})
	}
	systemPrompt, userPrompt := generator.BuildAnswerPrompt(query, snippets)

	return llm.AskLLM(systemPrompt, userPrompt, settings)
}

func (s *Service) GetEntities(repoID, entityType string, page, perPage int) ([]Entity, int64, error) {
	if page <= 0 {
		page = 1
	}
	if perPage <= 0 {
		perPage = 20
	}

	query := s.db.Model(&Entity{})
	if repoID != "" {
		query = query.Where("repo_id = ?", repoID)
	}
	if entityType != "" {
		query = query.Where("entity_type = ?", entityType)
	}

	var total int64
	query.Count(&total)

	var entities []Entity
	err := query.Select("id, repo_id, entity_type, name, file_path, start_line, end_line, signature, doc_string, summary, language, created_at").
		Offset((page - 1) * perPage).Limit(perPage).
		Order("name asc").Find(&entities).Error
	return entities, total, err
}

// --- PKB-style knowledge doc generation ---

func (s *Service) generateKnowledgeDocs(repo *Repository, repoPath string, entities []Entity, codeFiles []string) {
	s.db.Unscoped().Where("repo_id = ?", repo.ID).Delete(&KnowledgeDoc{})

	repoMap := s.buildRepoMap(repo, repoPath, entities, codeFiles)
	s.db.Create(&repoMap)

	overview := s.buildProjectOverview(repo, repoPath, entities, codeFiles)
	s.db.Create(&overview)
}

func (s *Service) buildRepoMap(repo *Repository, repoPath string, entities []Entity, codeFiles []string) KnowledgeDoc {
	var mapped []generator.RepoMapEntity
	for _, e := range entities {
		mapped = append(mapped, generator.RepoMapEntity{
			Name:       e.Name,
			EntityType: e.EntityType,
			Language:   e.Language,
			FilePath:   e.FilePath,
			StartLine:  e.StartLine,
		})
	}

	content := generator.BuildRepoMapContent(repo.Name, repoPath, codeFiles, mapped)

	return KnowledgeDoc{
		ID:      entityID(repo.ID, "repo-map", "doc", "repo-map", 0),
		RepoID:  repo.ID,
		DocType: "repo-map",
		Title:   "Repository Map",
		Content: content,
	}
}

func (s *Service) buildProjectOverview(repo *Repository, repoPath string, entities []Entity, codeFiles []string) KnowledgeDoc {
	settings := llm.LLMSettings{
		BaseUrl:     s.config.Generation.BaseURL,
		ApiKey:      s.config.Generation.APIKey,
		Model:       s.config.Generation.Model,
		Temperature: s.config.Generation.Temperature,
	}

	if settings.ApiKey == "" {
		return KnowledgeDoc{
			ID:      entityID(repo.ID, "overview", "doc", "overview", 0),
			RepoID:  repo.ID,
			DocType: "overview",
			Title:   "Project Overview",
			Content: fmt.Sprintf("# Project Overview: %s\n\nLLM API key not configured. Run with LLM_API_KEY to generate an AI-powered overview.\n\n**Files**: %d | **Entities**: %d",
				repo.Name, len(codeFiles), len(entities)),
		}
	}

	var mapped []generator.OverviewEntity
	for _, e := range entities {
		mapped = append(mapped, generator.OverviewEntity{
			Name:       e.Name,
			EntityType: e.EntityType,
			FilePath:   e.FilePath,
			StartLine:  e.StartLine,
			Signature:  e.Signature,
		})
	}

	systemPrompt, userPrompt := generator.BuildOverviewPrompt(repo.Name, repoPath, codeFiles, mapped, 80)

	answer, err := llm.AskLLM(systemPrompt, userPrompt, settings)
	if err != nil {
		answer = fmt.Sprintf("# Project Overview: %s\n\nFailed to generate overview: %v", repo.Name, err)
	}

	return KnowledgeDoc{
		ID:      entityID(repo.ID, "overview", "doc", "overview", 0),
		RepoID:  repo.ID,
		DocType: "overview",
		Title:   "Project Overview",
		Content: answer,
	}
}

func (s *Service) GetKnowledgeDocs(repoID string) ([]KnowledgeDoc, error) {
	var docs []KnowledgeDoc
	err := s.db.Where("repo_id = ?", repoID).Order("doc_type asc").Find(&docs).Error
	return docs, err
}

func syncJobToStatus(job SyncJob) *SyncStatus {
	return &SyncStatus{
		JobID:           job.ID,
		Status:          job.Status,
		Phase:           job.Phase,
		TriggerSource:   job.TriggerSource,
		TotalFiles:      job.TotalFiles,
		ProcessedFiles:  job.ProcessedFiles,
		EntitiesCreated: job.EntitiesCreated,
		EntitiesUpdated: job.EntitiesUpdated,
		EntitiesDeleted: job.EntitiesDeleted,
		Error:           job.Error,
		StartedAt:       job.StartedAt,
		FinishedAt:      job.FinishedAt,
	}
}

func (s *Service) persistSyncStatus(repoID string, status *SyncStatus) error {
	if status == nil {
		return nil
	}
	job := SyncJob{
		ID:              status.JobID,
		RepoID:          repoID,
		TriggerSource:   status.TriggerSource,
		Status:          status.Status,
		Phase:           status.Phase,
		TotalFiles:      status.TotalFiles,
		ProcessedFiles:  status.ProcessedFiles,
		EntitiesCreated: status.EntitiesCreated,
		EntitiesUpdated: status.EntitiesUpdated,
		EntitiesDeleted: status.EntitiesDeleted,
		Error:           status.Error,
		StartedAt:       status.StartedAt,
		FinishedAt:      status.FinishedAt,
	}
	return s.db.Save(&job).Error
}

// deleteVecEntries removes sqlite-vec rows for all entities belonging to a repo.
func (s *Service) deleteVecEntries(repoID string) {
	if s.vectorStore == nil {
		return
	}

	var ids []string
	if err := s.db.Model(&Entity{}).Where("repo_id = ?", repoID).Pluck("id", &ids).Error; err != nil {
		ilog.GetLogger().Warnf("Failed to load vec entry ids for repo %s: %v", repoID, err)
		return
	}

	for _, id := range ids {
		if err := s.vectorStore.Delete(id); err != nil {
			ilog.GetLogger().Warnf("Failed to delete vec entry %s for repo %s: %v", id, repoID, err)
		}
	}
}

// --- helpers ---

func entityID(repoID, filePath, entityType, name string, startLine int) string {
	h := sha256.Sum256([]byte(fmt.Sprintf("%s:%s:%s:%s:%d", repoID, filePath, entityType, name, startLine)))
	return fmt.Sprintf("%x", h[:8])
}

func extractSignature(content string) string {
	lines := strings.SplitN(content, "\n", 3)
	if len(lines) > 0 {
		return strings.TrimSpace(lines[0])
	}
	return ""
}

func truncate(s string, maxLen int) string {
	if len(s) <= maxLen {
		return s
	}
	return s[:maxLen] + "..."
}

func getEnvOrDefault(key, defaultVal string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return defaultVal
}
