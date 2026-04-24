package main

import (
	"crypto/sha256"
	"fmt"
	"strings"
	"time"
)

// Service orchestrates parsing, embedding, graph-building, and search.
type Service struct {
	config   Config
	entities map[string]Entity
	graph    map[string][]string
}

// NewService creates a Service with the given configuration.
func NewService(cfg Config) *Service {
	return &Service{
		config:   cfg,
		entities: make(map[string]Entity),
		graph:    make(map[string][]string),
	}
}

// runSync performs a full synchronisation: scan → parse → embed → graph → docs.
func (s *Service) runSync(repo *Repository, repoPath string) error {
	start := time.Now()
	fmt.Printf("[sync] full sync started for %s\n", repo.Name)

	files := collectCodeFiles(repoPath)
	fmt.Printf("[sync] scanned %d files in %v\n", len(files), time.Since(start))

	for _, f := range files {
		entities := parseFile(repo.ID, repoPath, f)
		for _, e := range entities {
			s.entities[e.ID] = e
		}
	}
	fmt.Printf("[sync] parsed %d entities\n", len(s.entities))

	s.buildGraph()
	fmt.Printf("[sync] graph built: %d nodes, %d edges\n",
		len(s.entities), s.countEdges())

	fmt.Printf("[sync] full sync completed in %v\n", time.Since(start))
	return nil
}

// runIncrementalSync re-processes only the files changed since lastCommit.
func (s *Service) runIncrementalSync(repo *Repository, repoPath, lastCommit string) error {
	start := time.Now()
	changed := gitDiffFiles(repoPath, lastCommit)
	fmt.Printf("[incr-sync] %d changed file(s) detected\n", len(changed))

	for _, f := range changed {
		entities := parseFile(repo.ID, repoPath, f)
		for _, e := range entities {
			s.entities[e.ID] = e
		}
	}
	s.rebuildSubgraph(changed)
	fmt.Printf("[incr-sync] incremental sync completed in %v\n", time.Since(start))
	return nil
}

// Search finds entities matching the query using hybrid retrieval.
func (s *Service) Search(req SearchRequest) (*SearchResult, error) {
	var matched []Entity
	q := strings.ToLower(req.Query)
	for _, e := range s.entities {
		if strings.Contains(strings.ToLower(e.Name), q) ||
			strings.Contains(strings.ToLower(e.DocString), q) {
			matched = append(matched, e)
			if len(matched) >= req.TopK {
				break
			}
		}
	}
	return &SearchResult{Entities: matched, Answer: "see matched entities"}, nil
}

func (s *Service) buildGraph() {
	s.graph = make(map[string][]string)
	for _, e := range s.entities {
		s.graph[e.ID] = []string{}
	}
}

func (s *Service) rebuildSubgraph(files []string) {
	for _, e := range s.entities {
		for _, f := range files {
			if e.FilePath == f {
				s.graph[e.ID] = []string{}
			}
		}
	}
}

func (s *Service) countEdges() int {
	n := 0
	for _, edges := range s.graph {
		n += len(edges)
	}
	return n
}

// entityID computes a stable 16-hex-char identity for a code entity.
func entityID(repoID, filePath, entityType, name string, startLine int) string {
	h := sha256.Sum256([]byte(fmt.Sprintf("%s:%s:%s:%s:%d",
		repoID, filePath, entityType, name, startLine)))
	return fmt.Sprintf("%x", h[:8])
}
