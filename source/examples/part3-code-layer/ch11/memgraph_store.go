/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     code-layer-reference-impl
// source_path:     reference-impl/code-kg/memgraph_store.go
// commit_sha:      7afa52003fd6  (dirty — uncommitted changes)
// captured_at:     2026-04-18T01:15:58Z
// content_sha256:  10168a74589a37fe7523f8ec568b03c935121a2be00202408db5caab94eec35b
// regenerate with: make book-refresh-excerpts
 */

package ckg

import (
	"context"

	"example.com/reference-impl/code-kg/store/memgraph"
	ilog "example.com/reference-impl/code-kg-repo/internal/log"
)

type MemgraphStore struct {
	store memgraph.Store
}

type failingGraphStore struct {
	err error
}

func (f *failingGraphStore) UpsertRepositoryGraph(_, _ string, _ []Entity, _ []CodeRelation) error {
	return f.err
}

func NewMemgraphStore(uri, username, password, project string) (*MemgraphStore, error) {
	store, err := memgraph.NewFull(uri, username, password, project)
	if err != nil {
		return nil, err
	}
	return &MemgraphStore{store: store}, nil
}

func newGraphStoreFromConfig(config GraphConfig) GraphStore {
	if config.Disabled {
		return nil
	}
	store, err := memgraph.NewFull(config.URI, config.Username, config.Password, config.Namespace)
	if err != nil {
		ilog.GetLogger().Warnf("Failed to initialize Memgraph store: %v", err)
		return &failingGraphStore{err: err}
	}
	return &MemgraphStore{store: store}
}

func (s *MemgraphStore) Close(ctx context.Context) error {
	if s == nil || s.store == nil {
		return nil
	}
	return s.store.Close(ctx)
}

func (s *MemgraphStore) UpsertRepositoryGraph(repoID, projectName string, entities []Entity, relations []CodeRelation) error {
	if s == nil || s.store == nil {
		return nil
	}
	nodes, edges := buildMemgraphPayload(repoID, projectName, entities, relations)
	return s.store.UpsertRepositoryGraph(repoID, nodes, edges)
}

func buildMemgraphPayload(repoID, projectName string, entities []Entity, relations []CodeRelation) ([]memgraph.Node, []memgraph.Edge) {
	var nodes []memgraph.Node
	for _, entity := range entities {
		nodes = append(nodes, memgraph.Node{
			ID:         entity.ID,
			RepoID:     repoID,
			Label:      graphLabel(entity.EntityType),
			Name:       entity.Name,
			FilePath:   entity.FilePath,
			Signature:  entity.Signature,
			Doc:        entity.DocString,
			Summary:    entity.Summary,
			EntityType: entity.EntityType,
			StartLine:  entity.StartLine,
			EndLine:    entity.EndLine,
			Language:   entity.Language,
			Project:    projectName,
		})
	}

	var edges []memgraph.Edge
	for _, relation := range relations {
		edge := memgraph.Edge{
			SourceID: relation.SourceID,
			TargetID: relation.TargetID,
			Type:     string(relation.Type),
			Weight:   relation.Weight,
			Context:  relation.Context,
		}
		if relation.Type == RelationImports && relation.TargetID != "" {
			edge.TargetLabel = "Package"
			edge.TargetName = relation.Context
		}
		edges = append(edges, edge)
	}
	return nodes, edges
}

func graphLabel(entityType string) string {
	switch entityType {
	case "function":
		return "Function"
	case "class":
		return "Class"
	case "struct":
		return "Struct"
	case "interface":
		return "Interface"
	case "file":
		return "File"
	case "package":
		return "Package"
	default:
		return "CodeEntity"
	}
}
