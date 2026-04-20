/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     prose-layer-reference-impl
// source_path:     reference-impl/prose-wiki/repository.go
// commit_sha:      working-tree  (dirty — uncommitted changes)
// captured_at:     2026-04-17T21:13:41Z
// content_sha256:  4a8734ade3bcc1adbae80b2d9270808a2c7ef1eed718c510e35ef317d953f43c
// regenerate with: make book-refresh-excerpts
 */

package wiki

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

type WikiRepository interface {
	ReadPage(filePath string) (*Page, error)
	WritePage(page *Page) error
	DeletePage(filePath string) error
	ListFiles(dir string) ([]string, error)
	ReadCategoryMeta(dir string) (*Category, error)
}

type FileRepository struct {
	ContentDir string
}

func NewFileRepository(contentDir string) *FileRepository {
	return &FileRepository{ContentDir: contentDir}
}

func (r *FileRepository) ReadPage(filePath string) (*Page, error) {
	data, err := os.ReadFile(filePath)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, fmt.Errorf("page not found: %s", filePath)
		}
		return nil, fmt.Errorf("failed to read page: %w", err)
	}

	content := string(data)
	fm, body, err := ParseFrontmatter(content)
	if err != nil {
		return nil, fmt.Errorf("failed to parse frontmatter: %w", err)
	}

	if fm == nil {
		fm = InferFrontmatter(filePath)
	}

	cat := DeriveCategory(r.ContentDir, filePath)

	return &Page{
		Frontmatter: *fm,
		Body:        body,
		FilePath:    filePath,
		Category:    cat,
	}, nil
}

func (r *FileRepository) WritePage(page *Page) error {
	dir := filepath.Dir(page.FilePath)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("failed to create directory: %w", err)
	}

	content, err := SerializeFrontmatter(&page.Frontmatter, page.Body)
	if err != nil {
		return fmt.Errorf("failed to serialize page: %w", err)
	}

	return os.WriteFile(page.FilePath, []byte(content), 0644)
}

func (r *FileRepository) DeletePage(filePath string) error {
	if err := os.Remove(filePath); err != nil {
		if os.IsNotExist(err) {
			return fmt.Errorf("page not found: %s", filePath)
		}
		return fmt.Errorf("failed to delete page: %w", err)
	}
	return nil
}

func (r *FileRepository) ListFiles(dir string) ([]string, error) {
	var files []string
	err := filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			base := filepath.Base(path)
			if strings.HasPrefix(base, "_") && path != dir {
				return filepath.SkipDir
			}
			return nil
		}
		if !strings.HasSuffix(path, ".md") {
			return nil
		}
		base := filepath.Base(path)
		if base == "_category.md" {
			return nil
		}
		files = append(files, path)
		return nil
	})
	return files, err
}

func (r *FileRepository) ReadCategoryMeta(dir string) (*Category, error) {
	metaPath := filepath.Join(dir, "_category.md")
	data, err := os.ReadFile(metaPath)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, nil
		}
		return nil, err
	}

	fm, _, err := ParseFrontmatter(string(data))
	if err != nil {
		return nil, err
	}

	cat := DeriveCategory(r.ContentDir, filepath.Join(dir, "dummy.md"))
	if fm != nil && fm.Title != "" {
		cat.DisplayName = fm.Title
	}
	return &cat, nil
}
