/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     prose-layer-reference-impl
// source_path:     reference-impl/prose-wiki/pipeline.go
// commit_sha:      working-tree  (dirty — uncommitted changes)
// captured_at:     2026-04-17T21:13:41Z
// content_sha256:  541d1e9912a19a9ede2d00929e91f130635b6a950d73f64ac5c4dbee8e5f13cf
// regenerate with: make book-refresh-excerpts
 */

package wiki

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"

	"example.com/reference-impl/prose-wiki/llm"
)

type Pipeline struct {
	contentDir  string
	metadataDir string
	rawDir      string
	classifier  llm.Classifier
	repo        *FileRepository
	service     *WikiService
	index       *IndexEngine
	schema      *SchemaManager
	governance  *GovernanceManager
	git         *GitService
	config      *WikiConfig
	configPath  string
}

type IngestResult struct {
	Created int `json:"pages_created"`
	Skipped int `json:"pages_skipped"`
	Errors  int `json:"errors"`
}

type importOptions struct {
	archiveDir       string
	categoryOverride string
	useCategoryPath  bool
	disambiguateSlug bool
}

func (p *Pipeline) SetClassifier(c llm.Classifier) {
	p.classifier = c
}

func (p *Pipeline) getClassifier() llm.Classifier {
	if p.classifier != nil {
		return p.classifier
	}
	return &llm.HeuristicClassifier{}
}

func (p *Pipeline) getRewriter() llm.Rewriter {
	if rw, ok := p.classifier.(llm.Rewriter); ok {
		return rw
	}
	return llm.NewRewriter()
}

type PipelineStatus struct {
	Kind         string    `json:"kind"`
	WikiRoot     string    `json:"wiki_root"`
	ContentDir   string    `json:"content_dir"`
	PageCount    int       `json:"page_count"`
	SourceCount  int       `json:"source_count"`
	LastInit     time.Time `json:"last_init"`
	LastUpdate   time.Time `json:"last_update"`
	LastVerify   time.Time `json:"last_verify"`
	LastBuild    time.Time `json:"last_build"`
	WikiBaseURL  string    `json:"wiki_base_url"`
	GitAvailable bool      `json:"git_available"`
	LastCommit   string    `json:"last_commit"`
}

type VerifyReport struct {
	Staleness   []VerifyIssue `json:"staleness"`
	BrokenRefs  []VerifyIssue `json:"broken_refs"`
	Orphaned    []VerifyIssue `json:"orphaned"`
	Quality     []VerifyIssue `json:"quality"`
	Coverage    []VerifyIssue `json:"coverage"`
	Consistency []VerifyIssue `json:"consistency"`
	Trust       []VerifyIssue `json:"trust"`
	Summary     VerifySummary `json:"summary"`
}

type VerifyIssue struct {
	Type    string `json:"type"`
	File    string `json:"file"`
	Message string `json:"message"`
	AutoFix bool   `json:"auto_fix"`
}

type VerifySummary struct {
	TotalIssues int `json:"total_issues"`
	AutoFixable int `json:"auto_fixable"`
	Categories  int `json:"categories"`
}

func NewPipeline(contentDir, metadataDir, rawDir string, service *WikiService, index *IndexEngine) *Pipeline {
	wikiRoot := filepath.Dir(contentDir)
	return &Pipeline{
		contentDir:  contentDir,
		metadataDir: metadataDir,
		rawDir:      rawDir,
		repo:        NewFileRepository(contentDir),
		service:     service,
		index:       index,
		schema:      NewSchemaManager(metadataDir),
		governance:  NewGovernanceManager(metadataDir),
		git:         NewGitService(wikiRoot),
		configPath:  filepath.Join(metadataDir, "wiki.yaml"),
	}
}

func (p *Pipeline) Init(kind, projectRepo string) error {
	templateDir := TemplateDir()
	wikiRoot := filepath.Dir(p.contentDir)

	if info, err := os.Stat(templateDir); err == nil && info.IsDir() {
		log.Printf("Copying wiki template from %s to %s", templateDir, wikiRoot)
		if err := CopyDir(templateDir, wikiRoot); err != nil {
			return fmt.Errorf("failed to copy template: %w", err)
		}
	}

	if password, err := EnsureUsersYAML(p.metadataDir); err != nil {
		return fmt.Errorf("failed to initialize users: %w", err)
	} else if password != "" {
		fmt.Println("========================================")
		fmt.Println("  Default admin account created")
		fmt.Printf("  Username: admin\n")
		fmt.Printf("  Password: %s\n", password)
		fmt.Println("  Please change the password after login.")
		fmt.Println("========================================")
	}

	dirs := []string{
		p.contentDir,
		p.metadataDir,
		p.rawDir,
		filepath.Join(p.contentDir, "_assets"),
		filepath.Join(p.metadataDir, "skills"),
	}

	if kind == "pkb" {
		pkbDirs := []string{"adr", "tutorials", "how-to", "reference", "explanation"}
		for _, d := range pkbDirs {
			dirs = append(dirs, filepath.Join(p.contentDir, d))
		}
	}

	for _, d := range dirs {
		os.MkdirAll(d, 0755)
	}

	p.schema.EnsureSchema()

	indexPath := filepath.Join(p.metadataDir, "index.md")
	if _, err := os.Stat(indexPath); os.IsNotExist(err) {
		os.WriteFile(indexPath, []byte("# Wiki Index\n\n*Auto-generated — do not edit manually.*\n"), 0644)
	}

	logPath := filepath.Join(p.metadataDir, "log.md")
	if _, err := os.Stat(logPath); os.IsNotExist(err) {
		os.WriteFile(logPath, []byte("# Operation Log\n\n"), 0644)
	}

	cfg := &WikiConfig{
		Kind:        kind,
		ContentDir:  p.contentDir,
		MetadataDir: p.metadataDir,
		RawDir:      p.rawDir,
		ProjectRepo: projectRepo,
		Schema:      filepath.Join(p.metadataDir, "SCHEMA.md"),
		WikiBaseURL: "http://localhost:8080",
		Created:     time.Now().UTC(),
	}
	p.config = cfg
	SaveConfig(p.configPath, cfg)

	GenerateSkill(p.metadataDir)

	p.governance.AppendLog(fmt.Sprintf("Initialized wiki (kind=%s)", kind))

	if p.git.IsAvailable() {
		p.git.AutoCommit(wikiRoot, "init: wiki scaffold")
	}

	return nil
}

// supportedExtensions defines file types that ingestFile can process.
var supportedExtensions = map[string]bool{
	".md": true, ".txt": true, ".html": true, ".rst": true,
}

var (
	fencedCodeBlockRegex = regexp.MustCompile("(?s)```.*?```")
	inlineCodeRegex      = regexp.MustCompile("`[^`]*`")
	htmlSupRegex         = regexp.MustCompile(`(?is)<sup>.*?</sup>`)
	numericLinkRegex     = regexp.MustCompile(`^\d+$`)
)

// ingestFile is the shared core for all content entry modes.
// archiveDir is empty for direct imports (file stays in place);
// for batch ingest it is "raw/.processed/" and the original is moved there.
func (p *Pipeline) ingestFile(filePath string, archiveDir string) error {
	return p.ingestFileWithOptions(filePath, importOptions{archiveDir: archiveDir})
}

func (p *Pipeline) ingestFileWithOptions(filePath string, opts importOptions) error {
	ext := strings.ToLower(filepath.Ext(filePath))
	if !supportedExtensions[ext] {
		return fmt.Errorf("unsupported file type: %s", ext)
	}

	data, err := os.ReadFile(filePath)
	if err != nil {
		return fmt.Errorf("failed to read file: %w", err)
	}
	content := string(data)

	cls := p.getClassifier()
	if hc, ok := cls.(*llm.HeuristicClassifier); ok {
		hc.Filename = filepath.Base(filePath)
	}
	categories := p.existingCategories()
	classification, cerr := cls.Classify(content, categories)
	if cerr != nil {
		hc := &llm.HeuristicClassifier{Filename: filepath.Base(filePath)}
		classification, _ = hc.Classify(content, categories)
	}
	classification.Validate()

	if existing := p.findFileBySourcePath(filePath); existing != "" {
		return fmt.Errorf("skip: page from source %q already exists", filePath)
	}

	categoryDir := opts.categoryOverride
	if !opts.useCategoryPath {
		categoryDir = SanitizeCategory(classification.Category)
	}

	baseName := strings.TrimSuffix(filepath.Base(filePath), ext)
	slug := GenerateSlug(baseName + ".md")
	if opts.disambiguateSlug {
		slug = p.resolveImportSlug(baseName, categoryDir)
	} else if existing := p.service.findFileBySlug(slug); existing != "" {
		return fmt.Errorf("skip: page with slug %q already exists", slug)
	}

	var body string
	var existingFM *Frontmatter

	switch ext {
	case ".md":
		existingFM, body, _ = ParseFrontmatter(content)
		if existingFM == nil {
			body = content
		}
	case ".txt":
		body = content
	case ".html", ".rst":
		body = fmt.Sprintf("```%s\n%s\n```\n", strings.TrimPrefix(ext, "."), content)
	}

	assetsDir := filepath.Join(p.contentDir, "_assets")
	if ext == ".md" || ext == ".txt" {
		rewritten, n := downloadExternalImages(body, assetsDir)
		if n > 0 {
			body = rewritten
			log.Printf("ingestFile: downloaded %d external image(s) for %s", n, filepath.Base(filePath))
		}
	}

	fm := &Frontmatter{
		Title:              classification.Title,
		Slug:               slug,
		Tags:               classification.Tags,
		Summary:            classification.Summary,
		Created:            time.Now().UTC(),
		CreatedBy:          "human",
		Updated:            time.Now().UTC(),
		Status:             PageStatusPublished,
		DocType:            DocType(classification.DocType),
		VerificationStatus: VerificationUnreviewed,
		Source:             &Source{Type: SourceTypeDoc, Path: filePath},
	}

	if existingFM != nil {
		if existingFM.Title != "" {
			fm.Title = existingFM.Title
		}
		if existingFM.Summary != "" {
			fm.Summary = existingFM.Summary
		}
		if len(existingFM.Tags) > 0 {
			fm.Tags = existingFM.Tags
		}
		if existingFM.DocType != "" {
			fm.DocType = existingFM.DocType
		}
	}

	destDir := filepath.Join(p.contentDir, categoryDir)
	os.MkdirAll(destDir, 0755)
	destPath := filepath.Join(destDir, slug+".md")

	pageContent, err := SerializeFrontmatter(fm, body)
	if err != nil {
		return fmt.Errorf("failed to serialize page: %w", err)
	}
	if err := os.WriteFile(destPath, []byte(pageContent), 0644); err != nil {
		return fmt.Errorf("failed to write page: %w", err)
	}

	page, err := p.repo.ReadPage(destPath)
	if err == nil && page != nil {
		p.index.AddPage(page)
	}

	if opts.archiveDir != "" {
		os.MkdirAll(opts.archiveDir, 0755)
		archivePath := filepath.Join(opts.archiveDir, filepath.Base(filePath))
		if err := os.Rename(filePath, archivePath); err != nil {
			return fmt.Errorf("failed to archive file: %w", err)
		}
	}

	return nil
}

func (p *Pipeline) findFileBySourcePath(sourcePath string) string {
	p.index.mu.RLock()
	defer p.index.mu.RUnlock()
	for _, page := range p.index.pages {
		if page.Frontmatter.Source != nil && page.Frontmatter.Source.Path == sourcePath {
			return page.FilePath
		}
	}
	return ""
}

func (p *Pipeline) resolveImportSlug(baseName, categoryDir string) string {
	baseSlug := GenerateSlug(baseName + ".md")
	if existing := p.service.findFileBySlug(baseSlug); existing == "" {
		return baseSlug
	}

	segments := []string{}
	if categoryDir != "" {
		segments = strings.Split(categoryDir, "/")
	}

	for i := len(segments) - 1; i >= 0; i-- {
		prefix := strings.Join(segments[i:], "-")
		candidate := SanitizeName(prefix + "-" + baseSlug)
		if candidate != "" && candidate != "untitled" && p.service.findFileBySlug(candidate) == "" {
			return candidate
		}
	}

	prefix := baseSlug
	if categoryDir != "" {
		prefix = SanitizeName(strings.ReplaceAll(categoryDir, "/", "-") + "-" + baseSlug)
	}
	for i := 2; ; i++ {
		candidate := SanitizeName(fmt.Sprintf("%s-%d", prefix, i))
		if p.service.findFileBySlug(candidate) == "" {
			return candidate
		}
	}
}

func sourceCategoryFromImportRoot(rootDir, filePath string) string {
	rel, err := filepath.Rel(rootDir, filePath)
	if err != nil {
		return ""
	}
	dir := filepath.Dir(rel)
	if dir == "." || dir == "" {
		return ""
	}
	return SanitizeCategory(filepath.ToSlash(dir))
}

func sanitizeBodyForVerify(body string) string {
	body = fencedCodeBlockRegex.ReplaceAllString(body, "")
	body = inlineCodeRegex.ReplaceAllString(body, "")
	body = htmlSupRegex.ReplaceAllString(body, "")
	return body
}

// existingCategories returns the unique set of category paths from already-indexed pages.
func (p *Pipeline) existingCategories() []string {
	p.index.mu.RLock()
	defer p.index.mu.RUnlock()
	seen := make(map[string]bool)
	for _, pg := range p.index.pages {
		if pg.Category.Path != "" {
			seen[pg.Category.Path] = true
		}
	}
	cats := make([]string, 0, len(seen))
	for c := range seen {
		cats = append(cats, c)
	}
	return cats
}

// ImportFile directly classifies a single file and creates a wiki page.
// The original file stays in place (no archival).
func (p *Pipeline) ImportFile(filePath string) error {
	if err := p.ingestFile(filePath, ""); err != nil {
		if strings.HasPrefix(err.Error(), "skip:") {
			p.governance.AppendLog(fmt.Sprintf("ImportFile skipped: %s", filepath.Base(filePath)))
			return err
		}
		return err
	}
	p.governance.AppendLog(fmt.Sprintf("ImportFile: created page from %s", filepath.Base(filePath)))
	p.rebuildIndexMd()
	if p.git.IsAvailable() {
		p.git.AutoCommit(p.contentDir, fmt.Sprintf("import: %s", filepath.Base(filePath)))
	}
	return nil
}

// ImportDir recursively imports all supported files from a directory.
func (p *Pipeline) ImportDir(dirPath string) (*IngestResult, error) {
	result := &IngestResult{}

	err := filepath.Walk(dirPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return nil
		}
		if info.IsDir() {
			if info.Name() == ".processed" || info.Name() == ".git" {
				return filepath.SkipDir
			}
			return nil
		}
		ext := strings.ToLower(filepath.Ext(path))
		if !supportedExtensions[ext] {
			return nil
		}

		opts := importOptions{
			categoryOverride: sourceCategoryFromImportRoot(dirPath, path),
			useCategoryPath:  true,
			disambiguateSlug: true,
		}
		if ierr := p.ingestFileWithOptions(path, opts); ierr != nil {
			if strings.HasPrefix(ierr.Error(), "skip:") {
				result.Skipped++
			} else {
				result.Errors++
				log.Printf("ImportDir: error processing %s: %v", path, ierr)
			}
		} else {
			result.Created++
		}
		return nil
	})
	if err != nil {
		return result, err
	}

	if result.Created > 0 {
		p.governance.AppendLog(fmt.Sprintf("ImportDir: created %d pages from %s (skipped %d, errors %d)",
			result.Created, dirPath, result.Skipped, result.Errors))
		p.rebuildIndexMd()
		if p.git.IsAvailable() {
			p.git.AutoCommit(p.contentDir, fmt.Sprintf("import-dir: %d pages from %s", result.Created, filepath.Base(dirPath)))
		}
	}
	return result, nil
}

// Ingest batch-processes all supported files in the raw/ inbox.
// Processed files are archived to raw/.processed/.
func (p *Pipeline) Ingest() (*IngestResult, error) {
	result := &IngestResult{}
	archiveDir := filepath.Join(p.rawDir, ".processed")

	files, err := os.ReadDir(p.rawDir)
	if err != nil {
		if os.IsNotExist(err) {
			return result, nil
		}
		return result, err
	}

	for _, f := range files {
		if f.IsDir() {
			continue
		}
		ext := strings.ToLower(filepath.Ext(f.Name()))
		if !supportedExtensions[ext] {
			continue
		}

		srcPath := filepath.Join(p.rawDir, f.Name())
		if ierr := p.ingestFile(srcPath, archiveDir); ierr != nil {
			if strings.HasPrefix(ierr.Error(), "skip:") {
				result.Skipped++
			} else {
				result.Errors++
				log.Printf("Ingest: error processing %s: %v", f.Name(), ierr)
			}
		} else {
			result.Created++
		}
	}

	if result.Created > 0 {
		p.governance.AppendLog(fmt.Sprintf("Ingest: created %d pages from raw/ (skipped %d, errors %d)",
			result.Created, result.Skipped, result.Errors))
		p.rebuildIndexMd()
		if p.git.IsAvailable() {
			p.git.AutoCommit(p.contentDir, fmt.Sprintf("ingest: %d pages from raw/", result.Created))
		}
	}
	return result, nil
}

// Import copies a file or URL content into the raw/ folder (legacy behavior).
func (p *Pipeline) Import(sourceType, path string) error {
	sourcesDir := p.rawDir
	os.MkdirAll(sourcesDir, 0755)

	var destName string
	var content []byte

	switch sourceType {
	case "file":
		data, err := os.ReadFile(path)
		if err != nil {
			return fmt.Errorf("failed to read source file: %w", err)
		}
		content = data
		destName = filepath.Base(path)

	case "url":
		resp, err := http.Get(path)
		if err != nil {
			return fmt.Errorf("failed to fetch URL: %w", err)
		}
		defer resp.Body.Close()
		data, err := io.ReadAll(resp.Body)
		if err != nil {
			return fmt.Errorf("failed to read URL content: %w", err)
		}
		content = data
		slug := GenerateSlug(path)
		destName = slug + ".md"

	case "git":
		return fmt.Errorf("git import not yet implemented — use file import after cloning")
	default:
		return fmt.Errorf("unknown source type: %s", sourceType)
	}

	destPath := filepath.Join(sourcesDir, destName)
	if err := os.WriteFile(destPath, content, 0644); err != nil {
		return fmt.Errorf("failed to write source: %w", err)
	}

	p.governance.AppendLog(fmt.Sprintf("Imported source: %s (%s)", destName, sourceType))
	return nil
}

// Update is DEPRECATED: use Ingest() instead.
// Retained for backward compatibility; processes raw/ without LLM classification.
func (p *Pipeline) Update() error {
	log.Println("DEPRECATED: Pipeline.Update() is deprecated. Use Pipeline.Ingest() instead.")

	sourcesDir := p.rawDir
	files, err := os.ReadDir(sourcesDir)
	if err != nil {
		if os.IsNotExist(err) {
			return nil
		}
		return err
	}

	created := 0
	for _, f := range files {
		if f.IsDir() || !strings.HasSuffix(f.Name(), ".md") {
			continue
		}

		srcPath := filepath.Join(sourcesDir, f.Name())
		data, err := os.ReadFile(srcPath)
		if err != nil {
			continue
		}

		slug := GenerateSlug(f.Name())
		if existing := p.service.findFileBySlug(slug); existing != "" {
			continue
		}

		title := strings.TrimSuffix(f.Name(), ".md")
		title = strings.ReplaceAll(title, "-", " ")
		title = strings.Title(title) //nolint:staticcheck

		fm := &Frontmatter{
			Title:              title,
			Slug:               slug,
			Created:            time.Now().UTC(),
			CreatedBy:          "ai",
			Updated:            time.Now().UTC(),
			UpdatedBy:          "ai",
			Status:             PageStatusPublished,
			DocType:            DocTypeReference,
			VerificationStatus: VerificationUnreviewed,
			Source:             &Source{Type: SourceTypeDoc, Path: srcPath},
		}

		body := string(data)
		existing, _, _ := ParseFrontmatter(body)
		if existing != nil {
			body = body[strings.Index(body, "---\n")+4:]
			if idx := strings.Index(body, "---\n"); idx >= 0 {
				body = body[idx+4:]
			}
		}

		pageContent, _ := SerializeFrontmatter(fm, body)
		destPath := filepath.Join(p.contentDir, slug+".md")
		os.WriteFile(destPath, []byte(pageContent), 0644)

		page, _ := p.repo.ReadPage(destPath)
		if page != nil {
			p.index.AddPage(page)
			created++
		}
	}

	if created > 0 {
		p.governance.AppendLog(fmt.Sprintf("Update: created %d pages from sources", created))
		p.rebuildIndexMd()
		if p.git.IsAvailable() {
			p.git.AutoCommit(p.contentDir, fmt.Sprintf("update: created %d pages from sources", created))
		}
	}

	return nil
}

func (p *Pipeline) Verify(autoFix bool) (*VerifyReport, error) {
	report := &VerifyReport{}

	files, err := p.repo.ListFiles(p.contentDir)
	if err != nil {
		return nil, err
	}

	var pages []*Page
	for _, f := range files {
		pg, err := p.repo.ReadPage(f)
		if err != nil {
			continue
		}
		pages = append(pages, pg)
	}

	slugSet := make(map[string]bool)
	for _, pg := range pages {
		slugSet[pg.Frontmatter.Slug] = true
	}

	for _, pg := range pages {
		// Staleness: no update in 90 days
		if time.Since(pg.Frontmatter.Updated) > 90*24*time.Hour {
			report.Staleness = append(report.Staleness, VerifyIssue{
				Type: "staleness", File: pg.FilePath,
				Message: fmt.Sprintf("Page not updated since %s", pg.Frontmatter.Updated.Format("2006-01-02")),
			})
		}

		// Broken refs
		sanitizedBody := sanitizeBodyForVerify(pg.Body)
		matches := wikiLinkRegex.FindAllStringSubmatch(sanitizedBody, -1)
		for _, m := range matches {
			linkName := strings.TrimSpace(m[1])
			if numericLinkRegex.MatchString(linkName) {
				continue
			}
			linkSlug := GenerateSlug(linkName + ".md")
			if !slugSet[linkSlug] {
				report.BrokenRefs = append(report.BrokenRefs, VerifyIssue{
					Type: "broken_ref", File: pg.FilePath,
					Message: fmt.Sprintf("Broken wiki-link: [[%s]]", linkName),
				})
			}
		}

		// Quality: missing summary
		if pg.Frontmatter.Summary == "" {
			issue := VerifyIssue{
				Type: "quality", File: pg.FilePath,
				Message: "Missing summary in frontmatter", AutoFix: false,
			}
			report.Quality = append(report.Quality, issue)
		}

		// Quality: missing doc_type
		if pg.Frontmatter.DocType == "" {
			issue := VerifyIssue{
				Type: "quality", File: pg.FilePath,
				Message: "Missing doc_type", AutoFix: autoFix,
			}
			report.Quality = append(report.Quality, issue)
			if autoFix {
				pg.Frontmatter.DocType = DocTypeReference
				p.repo.WritePage(pg)
			}
		}

		// Consistency: slug mismatch
		expectedSlug := GenerateSlug(filepath.Base(pg.FilePath))
		if pg.Frontmatter.Slug != expectedSlug {
			report.Consistency = append(report.Consistency, VerifyIssue{
				Type: "consistency", File: pg.FilePath,
				Message: fmt.Sprintf("Slug %q doesn't match filename (expected %q)", pg.Frontmatter.Slug, expectedSlug),
			})
		}

		// Trust: AI-authored but not unreviewed
		if pg.Frontmatter.CreatedBy == "ai" && pg.Frontmatter.VerificationStatus != VerificationUnreviewed {
			report.Trust = append(report.Trust, VerifyIssue{
				Type: "trust", File: pg.FilePath,
				Message: "AI-authored page should be unreviewed",
			})
		}
	}

	// Orphaned: pages not in index.md
	indexContent, _ := os.ReadFile(filepath.Join(p.metadataDir, "index.md"))
	indexStr := string(indexContent)
	for _, pg := range pages {
		if !strings.Contains(indexStr, pg.Frontmatter.Slug) {
			issue := VerifyIssue{
				Type: "orphaned", File: pg.FilePath,
				Message: "Page not listed in index.md", AutoFix: autoFix,
			}
			report.Orphaned = append(report.Orphaned, issue)
		}
	}
	if autoFix && len(report.Orphaned) > 0 {
		p.rebuildIndexMd()
	}

	// Coverage: check all Diataxis types have at least one page
	for _, dt := range []DocType{DocTypeTutorial, DocTypeHowTo, DocTypeReference, DocTypeExplanation} {
		found := false
		for _, pg := range pages {
			if pg.Frontmatter.DocType == dt {
				found = true
				break
			}
		}
		if !found {
			report.Coverage = append(report.Coverage, VerifyIssue{
				Type:    "coverage",
				Message: fmt.Sprintf("No pages with doc_type=%s", dt),
			})
		}
	}

	total := len(report.Staleness) + len(report.BrokenRefs) + len(report.Orphaned) +
		len(report.Quality) + len(report.Coverage) + len(report.Consistency) + len(report.Trust)
	autoFixable := 0
	for _, issues := range [][]VerifyIssue{report.Staleness, report.BrokenRefs, report.Orphaned,
		report.Quality, report.Coverage, report.Consistency, report.Trust} {
		for _, i := range issues {
			if i.AutoFix {
				autoFixable++
			}
		}
	}

	categories := 0
	if len(report.Staleness) > 0 {
		categories++
	}
	if len(report.BrokenRefs) > 0 {
		categories++
	}
	if len(report.Orphaned) > 0 {
		categories++
	}
	if len(report.Quality) > 0 {
		categories++
	}
	if len(report.Coverage) > 0 {
		categories++
	}
	if len(report.Consistency) > 0 {
		categories++
	}
	if len(report.Trust) > 0 {
		categories++
	}

	report.Summary = VerifySummary{
		TotalIssues: total,
		AutoFixable: autoFixable,
		Categories:  categories,
	}

	p.governance.AppendLog(fmt.Sprintf("Verify: %d issues in %d categories", total, categories))
	return report, nil
}

func (p *Pipeline) Build() error {
	if err := p.service.LoadAndIndex(); err != nil {
		return err
	}

	p.rebuildIndexMd()
	p.governance.AppendLog("Build: indexes rebuilt")
	return nil
}

func (p *Pipeline) Status() (*PipelineStatus, error) {
	sourceCount := 0
	sourcesDir := p.rawDir
	if files, err := os.ReadDir(sourcesDir); err == nil {
		for _, f := range files {
			if strings.HasSuffix(f.Name(), ".md") {
				sourceCount++
			}
		}
	}

	wikiRoot := filepath.Dir(p.contentDir)
	status := &PipelineStatus{
		WikiRoot:     wikiRoot,
		ContentDir:   p.contentDir,
		PageCount:    p.index.PageCount(),
		SourceCount:  sourceCount,
		GitAvailable: p.git.IsAvailable(),
		LastCommit:   p.git.GetCurrentCommitHash(),
	}

	if p.config != nil {
		status.Kind = p.config.Kind
		status.WikiBaseURL = p.config.WikiBaseURL
	} else if cfg, err := LoadConfig(p.configPath); err == nil {
		status.Kind = cfg.Kind
		status.WikiBaseURL = cfg.WikiBaseURL
	}

	return status, nil
}

func (p *Pipeline) StatusJSON() (string, error) {
	status, err := p.Status()
	if err != nil {
		return "", err
	}
	data, err := json.MarshalIndent(status, "", "  ")
	return string(data), err
}

func (p *Pipeline) rebuildIndexMd() {
	p.index.mu.RLock()
	pages := make([]*Page, 0, len(p.index.pages))
	for _, pg := range p.index.pages {
		pages = append(pages, pg)
	}
	p.index.mu.RUnlock()
	p.governance.UpdateIndexMd(pages)
}
