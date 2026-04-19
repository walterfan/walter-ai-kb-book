/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     code-layer-reference-impl
// source_path:     reference-impl/code-kg/graph.go
// commit_sha:      7afa52003fd6  (dirty — uncommitted changes)
// captured_at:     2026-04-18T01:15:58Z
// content_sha256:  b77b58ea907158577ed51f5e1132006b083a7a0f9e777271f41af60edf4df751
// regenerate with: make book-refresh-excerpts
 */

package ckg

import (
	"path/filepath"
	"regexp"
	"strings"
	"unicode"

	"example.com/reference-impl/code-kg-repo/internal/rag"
)

var goBuiltinTypes = map[string]bool{
	"string": true, "bool": true, "byte": true, "rune": true,
	"int": true, "int8": true, "int16": true, "int32": true, "int64": true,
	"uint": true, "uint8": true, "uint16": true, "uint32": true, "uint64": true, "uintptr": true,
	"float32": true, "float64": true, "complex64": true, "complex128": true,
	"error": true, "any": true, "comparable": true,
}

var goBuiltinFunctions = map[string]bool{
	"append": true, "cap": true, "clear": true, "close": true, "complex": true,
	"copy": true, "delete": true, "imag": true, "len": true, "make": true,
	"max": true, "min": true, "new": true, "panic": true, "print": true,
	"println": true, "real": true, "recover": true,
	"string": true, "int": true, "int64": true, "int32": true,
	"float64": true, "float32": true, "byte": true, "rune": true, "bool": true,
}

func isNoiseEntity(name, entityType string) bool {
	if name == "" {
		return true
	}
	if goBuiltinTypes[name] {
		return true
	}
	if len(name) <= 1 && entityType != "file" {
		return true
	}
	if !unicode.IsUpper(rune(name[0])) && entityType == "class" {
		return true
	}
	return false
}

func isNoiseFunction(name string) bool {
	return name == "" || goBuiltinFunctions[name]
}

// isNoiseImport filters out imports that are too generic to be useful in the
// code knowledge graph. Currently only filters empty strings; extend this to
// skip standard library imports if graph size becomes a concern.
func isNoiseImport(importPath string) bool {
	return importPath == ""
}

type RelationType string

const (
	RelationCalls      RelationType = "CALLS"
	RelationImplements RelationType = "IMPLEMENTS"
	RelationImports    RelationType = "IMPORTS"
	RelationContains   RelationType = "CONTAINS"
	RelationEmbeds     RelationType = "EMBEDS"
	RelationDependsOn  RelationType = "DEPENDS_ON"
	RelationReturns    RelationType = "RETURNS"
	RelationAccepts    RelationType = "ACCEPTS"
)

type CodeRelation struct {
	SourceID string       `json:"source_id"`
	TargetID string       `json:"target_id"`
	Type     RelationType `json:"type"`
	Weight   float64      `json:"weight"`
	Context  string       `json:"context"`
}

type GraphStore interface {
	UpsertRepositoryGraph(repoID, projectName string, entities []Entity, relations []CodeRelation) error
}

type parsedFile struct {
	RepoID   string
	FullPath string
	RelPath  string
	Metadata *rag.CodeMetadata
	Entities []Entity
}

func buildGraphData(repoID string, parsedFiles []parsedFile) ([]Entity, []CodeRelation) {
	parseResult := buildParseResult(repoID, parsedFiles)

	var graphEntities []Entity
	for _, entity := range parseResult.Entities {
		graphEntities = append(graphEntities, codeEntityToEntity(entity))
	}
	return graphEntities, parseResult.Relations
}

func buildParseResult(repoID string, parsedFiles []parsedFile) ParseResult {
	var relations []CodeRelation
	var files []string

	entityByID := make(map[string]CodeEntity)
	functionByName := make(map[string]CodeEntity)
	relationSeen := make(map[string]struct{})

	addRelation := func(rel CodeRelation) {
		key := rel.SourceID + "|" + string(rel.Type) + "|" + rel.TargetID
		if _, exists := relationSeen[key]; exists {
			return
		}
		relationSeen[key] = struct{}{}
		relations = append(relations, rel)
	}

	for _, pf := range parsedFiles {
		files = append(files, pf.RelPath)
		fileID := entityID(repoID, pf.RelPath, "file", pf.RelPath, 0)
		lang := "go"
		if pf.Metadata != nil && pf.Metadata.Language != "" {
			lang = string(pf.Metadata.Language)
		}
		fileNode := CodeEntity{
			ID:         fileID,
			RepoID:     repoID,
			EntityType: EntityTypeFile,
			Name:       filepath.Base(pf.RelPath),
			FilePath:   pf.RelPath,
			Language:   lang,
		}
		entityByID[fileID] = fileNode

		for _, entity := range pf.Entities {
			if isNoiseEntity(entity.Name, entity.EntityType) {
				continue
			}
			codeEntity := entityToCodeEntity(entity)
			entityByID[entity.ID] = codeEntity
			if codeEntity.EntityType == EntityTypeFunction {
				functionByName[entity.Name] = codeEntity
			}
			addRelation(CodeRelation{
				SourceID: fileID,
				TargetID: entity.ID,
				Type:     RelationContains,
				Weight:   1.0,
				Context:  pf.RelPath,
			})
		}

		for _, importValue := range extractImportTargets(pf.Metadata.Imports) {
			if isNoiseImport(importValue) {
				continue
			}
			addRelation(CodeRelation{
				SourceID: fileID,
				TargetID: "package:" + importValue,
				Type:     RelationImports,
				Weight:   1.0,
				Context:  importValue,
			})
		}
	}

	for _, pf := range parsedFiles {
		for _, entity := range pf.Entities {
			if entity.EntityType != "function" {
				continue
			}
			for _, callee := range detectFunctionCalls(entity.Body, entity.Name, functionByName) {
				addRelation(CodeRelation{
					SourceID: entity.ID,
					TargetID: callee.ID,
					Type:     RelationCalls,
					Weight:   1.0,
					Context:  entity.Name,
				})
			}
		}
	}

	var graphEntities []CodeEntity
	for _, entity := range entityByID {
		graphEntities = append(graphEntities, entity)
	}

	return ParseResult{
		RepoID:    repoID,
		Files:     files,
		Entities:  graphEntities,
		Relations: relations,
	}
}

var (
	reGoImport     = regexp.MustCompile(`"([^"]+)"`)
	reJavaImport   = regexp.MustCompile(`^\s*import\s+(?:static\s+)?([a-zA-Z_][\w.]*)\s*;`)
	rePyFrom       = regexp.MustCompile(`^\s*from\s+(\S+)\s+import`)
	rePyBareImport = regexp.MustCompile(`^\s*import\s+(\S+)`)
)

func extractImportTargets(imports []string) []string {
	var out []string
	seen := make(map[string]struct{})

	add := func(target string) {
		target = strings.TrimSpace(target)
		if target == "" {
			return
		}
		if _, exists := seen[target]; exists {
			return
		}
		seen[target] = struct{}{}
		out = append(out, target)
	}

	for _, imp := range imports {
		imp = strings.TrimSpace(imp)
		if imp == "" {
			continue
		}

		if m := reJavaImport.FindStringSubmatch(imp); len(m) >= 2 {
			add(m[1])
			continue
		}
		if m := rePyFrom.FindStringSubmatch(imp); len(m) >= 2 {
			add(m[1])
			continue
		}
		if m := rePyBareImport.FindStringSubmatch(imp); len(m) >= 2 {
			add(m[1])
			continue
		}
		for _, m := range reGoImport.FindAllStringSubmatch(imp, -1) {
			if len(m) >= 2 {
				add(m[1])
			}
		}
	}
	return out
}

func detectFunctionCalls(body, selfName string, functionByName map[string]CodeEntity) []CodeEntity {
	var out []CodeEntity
	seen := make(map[string]struct{})
	for name, entity := range functionByName {
		if name == "" || name == selfName {
			continue
		}
		if isNoiseFunction(name) {
			continue
		}
		pattern := regexp.MustCompile(`\b` + regexp.QuoteMeta(name) + `\s*\(`)
		if !pattern.MatchString(body) {
			continue
		}
		if _, exists := seen[entity.ID]; exists {
			continue
		}
		seen[entity.ID] = struct{}{}
		out = append(out, entity)
	}
	return out
}
