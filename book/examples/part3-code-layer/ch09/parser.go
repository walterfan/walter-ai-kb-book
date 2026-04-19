/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     code-layer-reference-impl
// source_path:     reference-impl/code-kg/parser/parser.go
// commit_sha:      7afa52003fd6  (dirty — uncommitted changes)
// captured_at:     2026-04-18T01:15:58Z
// content_sha256:  1d17d43b0020dfad0a4cfca21264021089b8376f13d34e9a4fabf6e54d15c25e
// regenerate with: make book-refresh-excerpts
 */

package parser

import (
	"os"
	"path/filepath"

	"example.com/reference-impl/code-kg-repo/internal/rag"
)

type Service struct {
	parser   *rag.CodeParser
	skipDirs map[string]bool
}

func New() *Service {
	return &Service{
		parser: rag.NewCodeParser(),
		skipDirs: map[string]bool{
			"vendor": true, "node_modules": true, ".git": true,
			"__pycache__": true, ".idea": true, ".vscode": true,
			"dist": true, "build": true, "target": true, ".next": true,
		},
	}
}

var supportedExtensions = map[string]bool{
	".go":   true,
	".java": true,
	".py":   true,
}

func (s *Service) CollectSupportedFiles(rootPath string) ([]string, error) {
	var files []string
	err := filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return nil
		}
		if info.IsDir() {
			if s.skipDirs[info.Name()] {
				return filepath.SkipDir
			}
			return nil
		}
		if supportedExtensions[filepath.Ext(path)] {
			files = append(files, path)
		}
		return nil
	})
	return files, err
}

func (s *Service) CollectGoFiles(rootPath string) ([]string, error) {
	return s.CollectSupportedFiles(rootPath)
}

func (s *Service) ParseFile(filePath string) (*rag.CodeMetadata, error) {
	return s.parser.ParseCode(filePath)
}

func RelativePath(repoRoot, filePath string) string {
	relPath, _ := filepath.Rel(repoRoot, filePath)
	if relPath == "" {
		return filePath
	}
	return relPath
}
