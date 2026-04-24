package main

import (
	"fmt"
	"sync"
)

// InMemoryStore is a thread-safe in-memory store for entities and repos.
type InMemoryStore struct {
	mu       sync.RWMutex
	repos    map[string]*Repository
	entities map[string][]Entity
}

// NewInMemoryStore returns an empty store.
func NewInMemoryStore() *InMemoryStore {
	return &InMemoryStore{
		repos:    make(map[string]*Repository),
		entities: make(map[string][]Entity),
	}
}

// SaveRepo persists a repository record.
func (s *InMemoryStore) SaveRepo(repo *Repository) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.repos[repo.ID] = repo
	return nil
}

// GetRepo looks up a repository by ID.
func (s *InMemoryStore) GetRepo(id string) (*Repository, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	r, ok := s.repos[id]
	if !ok {
		return nil, fmt.Errorf("repo %s not found", id)
	}
	return r, nil
}

// SaveEntities bulk-inserts entities for a given repo.
func (s *InMemoryStore) SaveEntities(repoID string, entities []Entity) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.entities[repoID] = entities
}

// GetEntities returns all entities for a repo.
func (s *InMemoryStore) GetEntities(repoID string) []Entity {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.entities[repoID]
}

// DeleteEntities removes all entities for a repo.
func (s *InMemoryStore) DeleteEntities(repoID string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	delete(s.entities, repoID)
}
