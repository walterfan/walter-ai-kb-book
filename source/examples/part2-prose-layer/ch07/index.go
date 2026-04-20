/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     prose-layer-reference-impl
// source_path:     reference-impl/prose-wiki/index.go
// commit_sha:      working-tree  (dirty — uncommitted changes)
// captured_at:     2026-04-17T21:13:41Z
// content_sha256:  c3c7c0b56dd865c67353409b4b5cbb10cd5745b9e3b3d0eb9324af64d98d837e
// regenerate with: make book-refresh-excerpts
 */

package wiki

import (
	"sort"
	"strings"
	"sync"
	"unicode"
)

type PageSummary struct {
	Slug               string             `json:"slug"`
	Title              string             `json:"title"`
	Category           string             `json:"category"`
	DocType            DocType            `json:"doc_type"`
	Tags               []string           `json:"tags"`
	Created            string             `json:"created"`
	Updated            string             `json:"updated"`
	CreatedBy          string             `json:"created_by"`
	UpdatedBy          string             `json:"updated_by"`
	VerificationStatus VerificationStatus `json:"verification_status"`
	Summary            string             `json:"summary"`
}

func pageSummaryFromPage(p *Page) PageSummary {
	summary := p.Frontmatter.Summary
	if summary == "" && len(p.Body) > 200 {
		summary = p.Body[:200]
	} else if summary == "" {
		summary = p.Body
	}
	return PageSummary{
		Slug:               p.Frontmatter.Slug,
		Title:              p.Frontmatter.Title,
		Category:           p.Category.Path,
		DocType:            p.Frontmatter.DocType,
		Tags:               p.Frontmatter.Tags,
		Created:            p.Frontmatter.Created.Format("2006-01-02T15:04:05Z"),
		Updated:            p.Frontmatter.Updated.Format("2006-01-02T15:04:05Z"),
		CreatedBy:          p.Frontmatter.CreatedBy,
		UpdatedBy:          p.Frontmatter.UpdatedBy,
		VerificationStatus: p.Frontmatter.VerificationStatus,
		Summary:            summary,
	}
}

type CategoryNode struct {
	Name     string         `json:"name"`
	Path     string         `json:"path"`
	Pages    []PageSummary  `json:"pages,omitempty"`
	Children []CategoryNode `json:"children,omitempty"`
}

type SectionRef struct {
	PageSlug string `json:"page_slug"`
	Anchor   string `json:"anchor"`
	Heading  string `json:"heading"`
	Excerpt  string `json:"excerpt"`
}

type SearchResult struct {
	Pages    []PageSummary `json:"pages,omitempty"`
	Sections []SectionRef  `json:"sections,omitempty"`
	Total    int           `json:"total"`
}

type IndexEngine struct {
	mu sync.RWMutex

	pages         map[string]*Page
	titleIndex    map[rune][]PageSummary
	categoryIndex CategoryNode
	wordIndex     map[string]int
	recentChanges []PageSummary
	docTypeIndex  map[DocType][]PageSummary
	authorIndex   map[string][]PageSummary
	sourceIndex   map[SourceType][]PageSummary
	trustIndex    map[VerificationStatus][]PageSummary
	searchTerms   map[string][]string // term -> []slug
}

func NewIndexEngine() *IndexEngine {
	return &IndexEngine{
		pages:       make(map[string]*Page),
		searchTerms: make(map[string][]string),
	}
}

func (idx *IndexEngine) BuildAll(pages []*Page) error {
	idx.mu.Lock()
	defer idx.mu.Unlock()

	idx.pages = make(map[string]*Page)
	for _, p := range pages {
		idx.pages[p.Frontmatter.Slug] = p
	}

	idx.rebuildAllLocked()
	return nil
}

func (idx *IndexEngine) AddPage(page *Page) error {
	idx.mu.Lock()
	defer idx.mu.Unlock()
	idx.pages[page.Frontmatter.Slug] = page
	idx.rebuildAllLocked()
	return nil
}

func (idx *IndexEngine) UpdatePage(oldSlug string, page *Page) error {
	idx.mu.Lock()
	defer idx.mu.Unlock()
	delete(idx.pages, oldSlug)
	idx.pages[page.Frontmatter.Slug] = page
	idx.rebuildAllLocked()
	return nil
}

func (idx *IndexEngine) RemovePage(slug string) error {
	idx.mu.Lock()
	defer idx.mu.Unlock()
	delete(idx.pages, slug)
	idx.rebuildAllLocked()
	return nil
}

func (idx *IndexEngine) rebuildAllLocked() {
	summaries := make([]PageSummary, 0, len(idx.pages))
	for _, p := range idx.pages {
		summaries = append(summaries, pageSummaryFromPage(p))
	}

	idx.buildTitleIndex(summaries)
	idx.buildCategoryIndex(summaries)
	idx.buildWordIndex()
	idx.buildRecentChanges(summaries)
	idx.buildDocTypeIndex(summaries)
	idx.buildAuthorIndex(summaries)
	idx.buildSourceIndex()
	idx.buildTrustIndex(summaries)
	idx.buildSearchIndex()
}

func (idx *IndexEngine) buildTitleIndex(summaries []PageSummary) {
	idx.titleIndex = make(map[rune][]PageSummary)
	sorted := make([]PageSummary, len(summaries))
	copy(sorted, summaries)
	sort.Slice(sorted, func(i, j int) bool {
		return strings.ToLower(sorted[i].Title) < strings.ToLower(sorted[j].Title)
	})
	for _, s := range sorted {
		if len(s.Title) > 0 {
			first := unicode.ToUpper(rune(s.Title[0]))
			idx.titleIndex[first] = append(idx.titleIndex[first], s)
		}
	}
}

func (idx *IndexEngine) buildCategoryIndex(summaries []PageSummary) {
	type catNode struct {
		Name     string
		Path     string
		Pages    []PageSummary
		Children []*catNode
	}

	root := &catNode{Name: "root", Path: ""}
	catMap := map[string]*catNode{"": root}

	getOrCreate := func(path string) *catNode {
		if n, ok := catMap[path]; ok {
			return n
		}
		n := &catNode{Name: lastSegment(path), Path: path}
		catMap[path] = n
		parentPath := parentCategoryPath(path)
		parent := catMap[parentPath]
		if parent == nil {
			parent = &catNode{Name: lastSegment(parentPath), Path: parentPath}
			catMap[parentPath] = parent
			root.Children = append(root.Children, parent)
		}
		parent.Children = append(parent.Children, n)
		return n
	}

	for _, s := range summaries {
		if s.Category == "" {
			root.Pages = append(root.Pages, s)
		} else {
			getOrCreate(s.Category).Pages = append(getOrCreate(s.Category).Pages, s)
		}
	}

	var toValue func(n *catNode) CategoryNode
	toValue = func(n *catNode) CategoryNode {
		cn := CategoryNode{Name: n.Name, Path: n.Path, Pages: n.Pages}
		for _, child := range n.Children {
			cn.Children = append(cn.Children, toValue(child))
		}
		return cn
	}
	idx.categoryIndex = toValue(root)
}

func lastSegment(path string) string {
	parts := strings.Split(path, "/")
	return parts[len(parts)-1]
}

func parentCategoryPath(path string) string {
	parts := strings.Split(path, "/")
	if len(parts) <= 1 {
		return ""
	}
	return strings.Join(parts[:len(parts)-1], "/")
}

func (idx *IndexEngine) buildWordIndex() {
	idx.wordIndex = make(map[string]int)
	for _, p := range idx.pages {
		for _, tag := range p.Frontmatter.Tags {
			idx.wordIndex[strings.ToLower(tag)]++
		}
	}
}

func (idx *IndexEngine) buildRecentChanges(summaries []PageSummary) {
	sorted := make([]PageSummary, len(summaries))
	copy(sorted, summaries)
	sort.Slice(sorted, func(i, j int) bool {
		return sorted[i].Updated > sorted[j].Updated
	})
	idx.recentChanges = sorted
}

func (idx *IndexEngine) buildDocTypeIndex(summaries []PageSummary) {
	idx.docTypeIndex = make(map[DocType][]PageSummary)
	for _, s := range summaries {
		if s.DocType != "" {
			idx.docTypeIndex[s.DocType] = append(idx.docTypeIndex[s.DocType], s)
		}
	}
}

func (idx *IndexEngine) buildAuthorIndex(summaries []PageSummary) {
	idx.authorIndex = make(map[string][]PageSummary)
	for _, s := range summaries {
		if s.CreatedBy != "" {
			idx.authorIndex[s.CreatedBy] = append(idx.authorIndex[s.CreatedBy], s)
		}
	}
}

func (idx *IndexEngine) buildSourceIndex() {
	idx.sourceIndex = make(map[SourceType][]PageSummary)
	for _, p := range idx.pages {
		s := pageSummaryFromPage(p)
		if p.Frontmatter.Source != nil {
			idx.sourceIndex[p.Frontmatter.Source.Type] = append(idx.sourceIndex[p.Frontmatter.Source.Type], s)
		} else {
			idx.sourceIndex[SourceTypeOriginal] = append(idx.sourceIndex[SourceTypeOriginal], s)
		}
	}
}

func (idx *IndexEngine) buildTrustIndex(summaries []PageSummary) {
	idx.trustIndex = make(map[VerificationStatus][]PageSummary)
	for _, s := range summaries {
		if s.VerificationStatus != "" {
			idx.trustIndex[s.VerificationStatus] = append(idx.trustIndex[s.VerificationStatus], s)
		}
	}
}

func (idx *IndexEngine) buildSearchIndex() {
	idx.searchTerms = make(map[string][]string)
	for slug, p := range idx.pages {
		terms := tokenize(p.Frontmatter.Title + " " + p.Body + " " + strings.Join(p.Frontmatter.Tags, " "))
		for _, term := range terms {
			idx.searchTerms[term] = append(idx.searchTerms[term], slug)
		}
	}
}

func tokenize(text string) []string {
	text = strings.ToLower(text)
	words := strings.FieldsFunc(text, func(r rune) bool {
		return !unicode.IsLetter(r) && !unicode.IsDigit(r)
	})
	seen := make(map[string]bool)
	var unique []string
	for _, w := range words {
		if len(w) >= 2 && !seen[w] {
			seen[w] = true
			unique = append(unique, w)
		}
	}
	return unique
}

// --- Read methods ---

func (idx *IndexEngine) GetTitleIndex() map[rune][]PageSummary {
	idx.mu.RLock()
	defer idx.mu.RUnlock()
	return idx.titleIndex
}

func (idx *IndexEngine) GetCategoryIndex() CategoryNode {
	idx.mu.RLock()
	defer idx.mu.RUnlock()
	return idx.categoryIndex
}

func (idx *IndexEngine) GetWordIndex() map[string]int {
	idx.mu.RLock()
	defer idx.mu.RUnlock()
	return idx.wordIndex
}

func (idx *IndexEngine) GetRecentChanges(limit int) []PageSummary {
	idx.mu.RLock()
	defer idx.mu.RUnlock()
	if limit <= 0 || limit > len(idx.recentChanges) {
		return idx.recentChanges
	}
	return idx.recentChanges[:limit]
}

func (idx *IndexEngine) GetDocTypeIndex() map[DocType][]PageSummary {
	idx.mu.RLock()
	defer idx.mu.RUnlock()
	return idx.docTypeIndex
}

func (idx *IndexEngine) GetAuthorIndex() map[string][]PageSummary {
	idx.mu.RLock()
	defer idx.mu.RUnlock()
	return idx.authorIndex
}

func (idx *IndexEngine) GetSourceIndex() map[SourceType][]PageSummary {
	idx.mu.RLock()
	defer idx.mu.RUnlock()
	return idx.sourceIndex
}

func (idx *IndexEngine) GetTrustIndex() map[VerificationStatus][]PageSummary {
	idx.mu.RLock()
	defer idx.mu.RUnlock()
	return idx.trustIndex
}

func (idx *IndexEngine) Search(query, searchType string) (*SearchResult, error) {
	idx.mu.RLock()
	defer idx.mu.RUnlock()

	terms := tokenize(query)
	if len(terms) == 0 {
		return &SearchResult{}, nil
	}

	slugScores := make(map[string]int)
	for _, term := range terms {
		for indexTerm, slugs := range idx.searchTerms {
			if strings.HasPrefix(indexTerm, term) {
				for _, slug := range slugs {
					slugScores[slug]++
				}
			}
		}
	}

	type scored struct {
		slug  string
		score int
	}
	var scoredSlugs []scored
	for slug, score := range slugScores {
		scoredSlugs = append(scoredSlugs, scored{slug, score})
	}
	sort.Slice(scoredSlugs, func(i, j int) bool {
		return scoredSlugs[i].score > scoredSlugs[j].score
	})

	result := &SearchResult{}
	for _, ss := range scoredSlugs {
		if p, ok := idx.pages[ss.slug]; ok {
			result.Pages = append(result.Pages, pageSummaryFromPage(p))
		}
	}
	result.Total = len(result.Pages)
	return result, nil
}

func (idx *IndexEngine) PageCount() int {
	idx.mu.RLock()
	defer idx.mu.RUnlock()
	return len(idx.pages)
}

// LookupSlug returns the slug and whether it exists, for wiki-link resolution.
func (idx *IndexEngine) LookupSlug(name string) (string, bool) {
	idx.mu.RLock()
	defer idx.mu.RUnlock()
	slug := GenerateSlug(name + ".md")
	_, exists := idx.pages[slug]
	return slug, exists
}
