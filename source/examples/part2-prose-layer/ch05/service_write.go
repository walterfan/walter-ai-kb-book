/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     prose-layer-reference-impl
// source_path:     reference-impl/prose-wiki/service_write.go
// commit_sha:      working-tree  (dirty — uncommitted changes)
// captured_at:     2026-04-17T21:13:41Z
// content_sha256:  58410cc3ac60a300b846c9afc92b96f8f39fd3f2d8b3b932d815ae54e0114f7f
// regenerate with: make book-refresh-excerpts
 */

package wiki

import (
	"fmt"
	"os"
	"path/filepath"
	"time"

	"example.com/reference-impl/prose-wiki/auth"
)

type CreatePageRequest struct {
	Title              string             `json:"title" binding:"required"`
	Category           string             `json:"category"`
	Body               string             `json:"body" binding:"required"`
	Tags               []string           `json:"tags"`
	Summary            string             `json:"summary"`
	DocType            DocType            `json:"doc_type"`
	Source             *Source            `json:"source,omitempty"`
	VerificationStatus VerificationStatus `json:"verification_status,omitempty"`
}

type UpdatePageRequest struct {
	Title              string             `json:"title"`
	Body               string             `json:"body"`
	Tags               []string           `json:"tags"`
	Summary            string             `json:"summary"`
	DocType            DocType            `json:"doc_type"`
	Category           string             `json:"category"`
	VerificationStatus VerificationStatus `json:"verification_status,omitempty"`
}

func (s *WikiService) CreatePage(req CreatePageRequest, user *auth.User, wikiAuthor string) (*PageResponse, error) {
	slug := GenerateSlug(req.Title + ".md")

	if existing := s.findFileBySlug(slug); existing != "" {
		return nil, fmt.Errorf("page already exists: %s", slug)
	}

	now := time.Now().UTC()
	createdBy := "human"
	if user != nil {
		createdBy = user.Username
	}
	if wikiAuthor == "ai" {
		createdBy = "ai"
	}

	docType := req.DocType
	if docType == "" {
		docType = DocTypeReference
	}

	vs := req.VerificationStatus
	if vs == "" {
		vs = DefaultVerificationStatus(createdBy)
	}
	if wikiAuthor == "ai" && vs == "" {
		vs = VerificationUnreviewed
	}

	fm := Frontmatter{
		Title:              req.Title,
		Slug:               slug,
		Tags:               req.Tags,
		Summary:            req.Summary,
		Created:            now,
		CreatedBy:          createdBy,
		Updated:            now,
		UpdatedBy:          createdBy,
		Status:             PageStatusPublished,
		DocType:            docType,
		VerificationStatus: vs,
		Source:             req.Source,
	}

	if err := fm.Validate(); err != nil {
		return nil, fmt.Errorf("invalid frontmatter: %w", err)
	}

	catDir := SanitizeCategory(req.Category)

	filePath := filepath.Join(s.repo.ContentDir, catDir, slug+".md")
	page := &Page{
		Frontmatter: fm,
		Body:        req.Body,
		FilePath:    filePath,
		Category:    DeriveCategory(s.repo.ContentDir, filePath),
	}

	if err := s.repo.WritePage(page); err != nil {
		return nil, err
	}

	if s.git != nil {
		s.git.AutoCommit(filePath, "create: "+req.Title)
		if hash := s.git.GetCurrentCommitHash(); hash != "" {
			page.Frontmatter.Commit = hash
			s.repo.WritePage(page)
		}
	}

	s.index.AddPage(page)
	s.updateGovernance("Created page: " + req.Title)

	return s.GetPageBySlug(slug)
}

func (s *WikiService) UpdatePage(slug string, req UpdatePageRequest, user *auth.User, wikiAuthor string) (*PageResponse, error) {
	file := s.findFileBySlug(slug)
	if file == "" {
		return nil, fmt.Errorf("page not found: %s", slug)
	}

	page, err := s.repo.ReadPage(file)
	if err != nil {
		return nil, err
	}

	updatedBy := "human"
	if user != nil {
		updatedBy = user.Username
	}
	if wikiAuthor == "ai" {
		updatedBy = "ai"
	} else if wikiAuthor == "human+ai" {
		updatedBy = "human+ai"
	}

	if req.Title != "" {
		page.Frontmatter.Title = req.Title
	}
	if req.Body != "" {
		page.Body = req.Body
	}
	if req.Tags != nil {
		page.Frontmatter.Tags = req.Tags
	}
	if req.Summary != "" {
		page.Frontmatter.Summary = req.Summary
	}
	if req.DocType != "" {
		page.Frontmatter.DocType = req.DocType
	}
	if req.VerificationStatus != "" {
		page.Frontmatter.VerificationStatus = req.VerificationStatus
	}

	page.Frontmatter.Updated = time.Now().UTC()
	page.Frontmatter.UpdatedBy = updatedBy

	if err := page.Frontmatter.Validate(); err != nil {
		return nil, fmt.Errorf("invalid frontmatter: %w", err)
	}

	sanitizedCat := SanitizeCategory(req.Category)
	if sanitizedCat != "" && sanitizedCat != page.Category.Path {
		newDir := filepath.Join(s.repo.ContentDir, sanitizedCat)
		os.MkdirAll(newDir, 0755)
		newPath := filepath.Join(newDir, filepath.Base(file))
		if err := os.Rename(file, newPath); err != nil {
			return nil, fmt.Errorf("failed to move page to new category: %w", err)
		}
		page.FilePath = newPath
		file = newPath
	}

	if err := s.repo.WritePage(page); err != nil {
		return nil, err
	}

	if s.git != nil {
		s.git.AutoCommit(file, "update: "+page.Frontmatter.Title)
		if hash := s.git.GetCurrentCommitHash(); hash != "" {
			page.Frontmatter.Commit = hash
			s.repo.WritePage(page)
		}
	}

	s.index.UpdatePage(slug, page)
	s.updateGovernance("Updated page: " + page.Frontmatter.Title)

	return s.GetPageBySlug(slug)
}

func (s *WikiService) DeletePage(slug string, user *auth.User) error {
	file := s.findFileBySlug(slug)
	if file == "" {
		return fmt.Errorf("page not found: %s", slug)
	}

	page, _ := s.repo.ReadPage(file)

	if err := s.repo.DeletePage(file); err != nil {
		return err
	}

	if s.git != nil && page != nil {
		s.git.AutoCommit(file, "delete: "+page.Frontmatter.Title)
	}

	s.index.RemovePage(slug)
	title := slug
	if page != nil {
		title = page.Frontmatter.Title
	}
	s.updateGovernance("Deleted page: " + title)

	return nil
}

func (s *WikiService) GetPageHistory(slug string) ([]Revision, error) {
	file := s.findFileBySlug(slug)
	if file == "" {
		return nil, fmt.Errorf("page not found: %s", slug)
	}
	if s.git == nil {
		return nil, nil
	}
	return s.git.GetPageHistory(file)
}

func (s *WikiService) updateGovernance(logEntry string) {
	if s.governance != nil {
		s.governance.AppendLog(logEntry)
		s.index.mu.RLock()
		pages := make([]*Page, 0, len(s.index.pages))
		for _, p := range s.index.pages {
			pages = append(pages, p)
		}
		s.index.mu.RUnlock()
		s.governance.UpdateIndexMd(pages)
	}
}
