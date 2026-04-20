/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     prose-layer-reference-impl
// source_path:     reference-impl/prose-wiki/frontmatter.go
// commit_sha:      working-tree  (dirty — uncommitted changes)
// captured_at:     2026-04-17T21:13:41Z
// content_sha256:  596b62c305aea4dd09e1de6ca966154ade116f91f4c0b8fa4717a9f167e5650c
// regenerate with: make book-refresh-excerpts
 */

package wiki

import (
	"bytes"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"gopkg.in/yaml.v3"
)

const frontmatterDelimiter = "---"

// ParseFrontmatter extracts YAML frontmatter and body from Markdown content.
// Returns the Frontmatter struct and the body (everything after the closing ---).
func ParseFrontmatter(content string) (*Frontmatter, string, error) {
	trimmed := strings.TrimSpace(content)
	if !strings.HasPrefix(trimmed, frontmatterDelimiter) {
		return nil, content, nil
	}

	rest := trimmed[len(frontmatterDelimiter):]
	idx := strings.Index(rest, "\n"+frontmatterDelimiter)
	if idx < 0 {
		return nil, content, nil
	}

	yamlBlock := rest[:idx]
	body := rest[idx+len("\n"+frontmatterDelimiter):]
	if strings.HasPrefix(body, "\n") {
		body = body[1:]
	}

	var fm Frontmatter
	if err := yaml.Unmarshal([]byte(yamlBlock), &fm); err != nil {
		return nil, "", fmt.Errorf("invalid frontmatter YAML: %w", err)
	}

	return &fm, body, nil
}

// SerializeFrontmatter produces the YAML frontmatter block + body Markdown.
func SerializeFrontmatter(fm *Frontmatter, body string) (string, error) {
	yamlBytes, err := yaml.Marshal(fm)
	if err != nil {
		return "", fmt.Errorf("failed to marshal frontmatter: %w", err)
	}

	var buf bytes.Buffer
	buf.WriteString(frontmatterDelimiter + "\n")
	buf.Write(yamlBytes)
	buf.WriteString(frontmatterDelimiter + "\n")
	buf.WriteString(body)
	return buf.String(), nil
}

// InferFrontmatter creates a Frontmatter with sensible defaults for a file
// that has no frontmatter. Title is derived from filename, timestamps from mtime.
func InferFrontmatter(filePath string) *Frontmatter {
	base := filepath.Base(filePath)
	name := strings.TrimSuffix(base, filepath.Ext(base))

	title := strings.ReplaceAll(name, "-", " ")
	title = strings.ReplaceAll(title, "_", " ")
	title = strings.Title(title) //nolint:staticcheck

	slug := GenerateSlug(base)

	now := time.Now().UTC()
	if info, err := os.Stat(filePath); err == nil {
		now = info.ModTime().UTC()
	}

	return &Frontmatter{
		Title:              title,
		Slug:               slug,
		Created:            now,
		CreatedBy:          "human",
		Updated:            now,
		Status:             PageStatusPublished,
		DocType:            DocTypeReference,
		VerificationStatus: VerificationSupported,
	}
}

// DefaultVerificationStatus returns the appropriate default verification status
// based on who created the page.
func DefaultVerificationStatus(createdBy string) VerificationStatus {
	if createdBy == "ai" {
		return VerificationUnreviewed
	}
	return VerificationSupported
}

// MergeFrontmatterUpdate applies update fields to an existing frontmatter,
// preserving immutable fields (created_by, created, source).
func MergeFrontmatterUpdate(existing, update *Frontmatter) *Frontmatter {
	merged := *update

	// Immutable fields — always preserve from existing
	merged.Created = existing.Created
	merged.CreatedBy = existing.CreatedBy
	if existing.Source != nil {
		merged.Source = existing.Source
	}

	// Auto-set updated timestamp
	merged.Updated = time.Now().UTC()

	return &merged
}

// DeriveCategory extracts the Category from a file path relative to contentDir.
func DeriveCategory(contentDir, filePath string) Category {
	rel, err := filepath.Rel(contentDir, filePath)
	if err != nil {
		return Category{Path: "", DisplayName: "root"}
	}

	dir := filepath.Dir(rel)
	if dir == "." {
		return Category{Path: "", DisplayName: "root"}
	}

	dir = filepath.ToSlash(dir)
	parts := strings.Split(dir, "/")
	displayName := parts[len(parts)-1]
	displayName = strings.ReplaceAll(displayName, "-", " ")
	displayName = strings.ReplaceAll(displayName, "_", " ")
	displayName = strings.Title(displayName) //nolint:staticcheck

	var parent *Category
	if len(parts) > 1 {
		parentPath := strings.Join(parts[:len(parts)-1], "/")
		parentName := parts[len(parts)-2]
		parentName = strings.ReplaceAll(parentName, "-", " ")
		parentName = strings.ReplaceAll(parentName, "_", " ")
		parentName = strings.Title(parentName) //nolint:staticcheck
		parent = &Category{Path: parentPath, DisplayName: parentName}
	}

	return Category{
		Path:        dir,
		DisplayName: displayName,
		Parent:      parent,
	}
}
