/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     code-layer-reference-impl
// source_path:     reference-impl/code-kg/domain_types.go
// commit_sha:      7afa52003fd6  (dirty — uncommitted changes)
// captured_at:     2026-04-18T01:15:58Z
// content_sha256:  4c9d23323613b9699f3cd98e8ff358dfd5215835933d2e97b869842ae8e4678e
// regenerate with: make book-refresh-excerpts
 */

package ckg

type CodeEntityType string

const (
	EntityTypePackage   CodeEntityType = "package"
	EntityTypeFile      CodeEntityType = "file"
	EntityTypeFunction  CodeEntityType = "function"
	EntityTypeClass     CodeEntityType = "class"
	EntityTypeStruct    CodeEntityType = "struct"
	EntityTypeInterface CodeEntityType = "interface"
	EntityTypeVariable  CodeEntityType = "variable"
	EntityTypeConstant  CodeEntityType = "constant"
)

type CodeEntity struct {
	ID         string            `json:"id"`
	RepoID     string            `json:"repo_id"`
	EntityType CodeEntityType    `json:"entity_type"`
	Name       string            `json:"name"`
	FilePath   string            `json:"file_path"`
	StartLine  int               `json:"start_line"`
	EndLine    int               `json:"end_line"`
	Signature  string            `json:"signature"`
	DocString  string            `json:"doc_string"`
	Body       string            `json:"body,omitempty"`
	Summary    string            `json:"summary,omitempty"`
	Language   string            `json:"language,omitempty"`
	Metadata   map[string]string `json:"metadata,omitempty"`
}

type ParseResult struct {
	RepoID    string         `json:"repo_id"`
	RootPath  string         `json:"root_path,omitempty"`
	Files     []string       `json:"files,omitempty"`
	Entities  []CodeEntity   `json:"entities"`
	Relations []CodeRelation `json:"relations"`
}

type SubGraph struct {
	SeedIDs []string       `json:"seed_ids,omitempty"`
	MaxHops int            `json:"max_hops,omitempty"`
	Nodes   []CodeEntity   `json:"nodes"`
	Edges   []CodeRelation `json:"edges"`
}

type AnalysisKind string

const (
	AnalysisCallers    AnalysisKind = "callers"
	AnalysisCallees    AnalysisKind = "callees"
	AnalysisImpact     AnalysisKind = "impact"
	AnalysisDependency AnalysisKind = "dependency"
	AnalysisDeadCode   AnalysisKind = "dead_code"
)

type GraphPath struct {
	NodeIDs       []string       `json:"node_ids,omitempty"`
	RelationTypes []RelationType `json:"relation_types,omitempty"`
	Summary       string         `json:"summary,omitempty"`
}

type AnalysisRequest struct {
	RepoID     string            `json:"repo_id"`
	EntityID   string            `json:"entity_id,omitempty"`
	EntityName string            `json:"entity_name,omitempty"`
	Analysis   AnalysisKind      `json:"analysis"`
	MaxHops    int               `json:"max_hops,omitempty"`
	Filters    map[string]string `json:"filters,omitempty"`
}

type AnalysisResult struct {
	Request AnalysisRequest `json:"request"`
	Graph   SubGraph        `json:"graph"`
	Summary string          `json:"summary,omitempty"`
	Paths   []GraphPath     `json:"paths,omitempty"`
}

func entityToCodeEntity(entity Entity) CodeEntity {
	return CodeEntity{
		ID:         entity.ID,
		RepoID:     entity.RepoID,
		EntityType: CodeEntityType(entity.EntityType),
		Name:       entity.Name,
		FilePath:   entity.FilePath,
		StartLine:  entity.StartLine,
		EndLine:    entity.EndLine,
		Signature:  entity.Signature,
		DocString:  entity.DocString,
		Body:       entity.Body,
		Summary:    entity.Summary,
		Language:   entity.Language,
	}
}

func codeEntityToEntity(entity CodeEntity) Entity {
	return Entity{
		ID:         entity.ID,
		RepoID:     entity.RepoID,
		EntityType: string(entity.EntityType),
		Name:       entity.Name,
		FilePath:   entity.FilePath,
		StartLine:  entity.StartLine,
		EndLine:    entity.EndLine,
		Signature:  entity.Signature,
		DocString:  entity.DocString,
		Body:       entity.Body,
		Summary:    entity.Summary,
		Language:   entity.Language,
	}
}
