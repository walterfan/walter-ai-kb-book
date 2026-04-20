/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     prose-layer-reference-impl
// source_path:     reference-impl/prose-wiki/service.go
// commit_sha:      working-tree  (dirty — uncommitted changes)
// captured_at:     2026-04-17T21:13:41Z
// content_sha256:  67d640322f74b33b5a12dd867ef74d87ef47838131bec91538b7747fdb4aa7dd
// regenerate with: make book-refresh-excerpts
 */

package wiki

import (
	"fmt"
	"sort"
	"strings"
)

type PageResponse struct {
	Page     PageSummary `json:"page"`
	HTML     string      `json:"html"`
	Body     string      `json:"body"`
	TOC      []TOCEntry  `json:"toc"`
	Sections []Section   `json:"sections,omitempty"`
}

type PageListResponse struct {
	Pages []PageSummary `json:"pages"`
	Total int           `json:"total"`
	Page  int           `json:"page"`
	Size  int           `json:"size"`
}

type PageFilter struct {
	Category           string
	DocType            DocType
	VerificationStatus VerificationStatus
	CreatedBy          string
	Tag                string
}

type WikiService struct {
	repo       *FileRepository
	renderer   *WikiRenderer
	index      *IndexEngine
	git        *GitService
	governance *GovernanceManager
}

func NewWikiService(repo *FileRepository, index *IndexEngine, apiBaseURL string) *WikiService {
	svc := &WikiService{
		repo:  repo,
		index: index,
	}
	svc.renderer = NewWikiRenderer(index.LookupSlug, apiBaseURL)
	return svc
}

func (s *WikiService) SetGitService(git *GitService) {
	s.git = git
}

func (s *WikiService) SetGovernanceManager(gov *GovernanceManager) {
	s.governance = gov
}

func (s *WikiService) LoadAndIndex() error {
	files, err := s.repo.ListFiles(s.repo.ContentDir)
	if err != nil {
		return fmt.Errorf("failed to list files: %w", err)
	}

	var pages []*Page
	for _, f := range files {
		p, err := s.repo.ReadPage(f)
		if err != nil {
			continue
		}
		pages = append(pages, p)
	}

	return s.index.BuildAll(pages)
}

func (s *WikiService) GetPageBySlug(slug string) (*PageResponse, error) {
	file := s.findFileBySlug(slug)
	if file == "" {
		return nil, fmt.Errorf("page not found: %s", slug)
	}

	page, err := s.repo.ReadPage(file)
	if err != nil {
		return nil, err
	}

	rendered, err := s.renderer.RenderPage(page)
	if err != nil {
		return nil, err
	}

	return &PageResponse{
		Page:     pageSummaryFromPage(page),
		HTML:     rendered.HTML,
		Body:     page.Body,
		TOC:      rendered.TOC,
		Sections: rendered.Sections,
	}, nil
}

func (s *WikiService) ListPages(filter PageFilter, page, size int) (*PageListResponse, error) {
	if page < 1 {
		page = 1
	}
	if size < 1 {
		size = 20
	}

	s.index.mu.RLock()
	var all []PageSummary
	for _, p := range s.index.pages {
		ps := pageSummaryFromPage(p)
		if matchesFilter(ps, p, filter) {
			all = append(all, ps)
		}
	}
	s.index.mu.RUnlock()

	sort.Slice(all, func(i, j int) bool {
		return all[i].Updated > all[j].Updated
	})

	total := len(all)
	start := (page - 1) * size
	if start >= total {
		return &PageListResponse{Pages: []PageSummary{}, Total: total, Page: page, Size: size}, nil
	}
	end := start + size
	if end > total {
		end = total
	}

	return &PageListResponse{Pages: all[start:end], Total: total, Page: page, Size: size}, nil
}

func matchesFilter(ps PageSummary, p *Page, filter PageFilter) bool {
	if filter.Category != "" && ps.Category != filter.Category {
		return false
	}
	if filter.DocType != "" && ps.DocType != filter.DocType {
		return false
	}
	if filter.VerificationStatus != "" && ps.VerificationStatus != filter.VerificationStatus {
		return false
	}
	if filter.CreatedBy != "" && ps.CreatedBy != filter.CreatedBy {
		return false
	}
	if filter.Tag != "" {
		found := false
		for _, t := range ps.Tags {
			if strings.EqualFold(t, filter.Tag) {
				found = true
				break
			}
		}
		if !found {
			return false
		}
	}
	return true
}

func (s *WikiService) SearchPages(query, searchType string, page, size int) (*SearchResult, error) {
	if page < 1 {
		page = 1
	}
	if size < 1 {
		size = 20
	}
	return s.index.Search(query, searchType)
}

func (s *WikiService) GetTitleIndex() map[rune][]PageSummary {
	return s.index.GetTitleIndex()
}

func (s *WikiService) GetCategoryIndex() CategoryNode {
	return s.index.GetCategoryIndex()
}

func (s *WikiService) GetWordIndex() map[string]int {
	return s.index.GetWordIndex()
}

func (s *WikiService) GetRecentChanges(limit int) []PageSummary {
	return s.index.GetRecentChanges(limit)
}

func (s *WikiService) GetDocTypeIndex() map[DocType][]PageSummary {
	return s.index.GetDocTypeIndex()
}

func (s *WikiService) findFileBySlug(slug string) string {
	s.index.mu.RLock()
	defer s.index.mu.RUnlock()
	if p, ok := s.index.pages[slug]; ok {
		return p.FilePath
	}
	return ""
}
