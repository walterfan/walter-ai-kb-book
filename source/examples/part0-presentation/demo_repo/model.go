package main

import "time"

// Repository represents a registered code repository in the knowledge base.
type Repository struct {
	ID                   string     `json:"id"`
	Name                 string     `json:"name"`
	URL                  string     `json:"url"`
	Branch               string     `json:"branch"`
	LocalPath            string     `json:"local_path"`
	Status               string     `json:"status"`
	LastSync             *time.Time `json:"last_sync"`
	LastCommit           string     `json:"last_commit"`
	LastSuccessfulCommit string     `json:"last_successful_commit"`
}

// Entity is a parsed code element: function, struct, interface, or constant.
type Entity struct {
	ID         string `json:"id"`
	RepoID     string `json:"repo_id"`
	EntityType string `json:"entity_type"`
	Name       string `json:"name"`
	FilePath   string `json:"file_path"`
	StartLine  int    `json:"start_line"`
	EndLine    int    `json:"end_line"`
	Signature  string `json:"signature"`
	DocString  string `json:"doc_string"`
	Body       string `json:"body"`
	Language   string `json:"language"`
}

// SyncStatus tracks the current state of a repository synchronisation job.
type SyncStatus struct {
	JobID           string     `json:"job_id"`
	Status          string     `json:"status"`
	Phase           string     `json:"phase"`
	TotalFiles      int        `json:"total_files"`
	ProcessedFiles  int        `json:"processed_files"`
	EntitiesCreated int        `json:"entities_created"`
	EntitiesDeleted int        `json:"entities_deleted"`
	StartedAt       *time.Time `json:"started_at"`
	FinishedAt      *time.Time `json:"finished_at"`
	Error           string     `json:"error,omitempty"`
}

// SearchRequest describes a code-search query.
type SearchRequest struct {
	Query      string `json:"query"`
	RepoID     string `json:"repo_id"`
	EntityType string `json:"entity_type"`
	TopK       int    `json:"top_k"`
}

// SearchResult wraps matched entities and an optional generated answer.
type SearchResult struct {
	Entities []Entity `json:"entities"`
	Answer   string   `json:"answer"`
}
