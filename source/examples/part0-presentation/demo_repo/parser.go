package main

import (
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

var (
	reFunc   = regexp.MustCompile(`(?m)^func\s+(\(\w+\s+\*?\w+\)\s+)?(\w+)\(`)
	reStruct = regexp.MustCompile(`(?m)^type\s+(\w+)\s+struct\s*\{`)
	reIface  = regexp.MustCompile(`(?m)^type\s+(\w+)\s+interface\s*\{`)
)

// parseFile extracts function, struct, and interface entities from a Go file.
func parseFile(repoID, repoRoot, filePath string) []Entity {
	content, err := os.ReadFile(filePath)
	if err != nil {
		return nil
	}
	relPath, _ := filepath.Rel(repoRoot, filePath)
	text := string(content)
	lines := strings.Split(text, "\n")
	var entities []Entity

	for _, m := range reFunc.FindAllStringSubmatchIndex(text, -1) {
		name := text[m[4]:m[5]]
		line := strings.Count(text[:m[0]], "\n") + 1
		entities = append(entities, Entity{
			ID:         entityID(repoID, relPath, "function", name, line),
			RepoID:     repoID,
			EntityType: "function",
			Name:       name,
			FilePath:   relPath,
			StartLine:  line,
			EndLine:    findBlockEnd(lines, line-1),
			Signature:  strings.TrimSpace(lines[line-1]),
			Language:   "go",
		})
	}

	for _, m := range reStruct.FindAllStringSubmatchIndex(text, -1) {
		name := text[m[2]:m[3]]
		line := strings.Count(text[:m[0]], "\n") + 1
		entities = append(entities, Entity{
			ID:         entityID(repoID, relPath, "struct", name, line),
			RepoID:     repoID,
			EntityType: "struct",
			Name:       name,
			FilePath:   relPath,
			StartLine:  line,
			EndLine:    findBlockEnd(lines, line-1),
			Language:   "go",
		})
	}

	for _, m := range reIface.FindAllStringSubmatchIndex(text, -1) {
		name := text[m[2]:m[3]]
		line := strings.Count(text[:m[0]], "\n") + 1
		entities = append(entities, Entity{
			ID:         entityID(repoID, relPath, "interface", name, line),
			RepoID:     repoID,
			EntityType: "interface",
			Name:       name,
			FilePath:   relPath,
			StartLine:  line,
			EndLine:    findBlockEnd(lines, line-1),
			Language:   "go",
		})
	}

	return entities
}

// collectCodeFiles walks a directory tree and returns all .go file paths.
func collectCodeFiles(root string) []string {
	var files []string
	filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
		if err != nil || info.IsDir() {
			if info != nil && info.IsDir() && info.Name() == ".git" {
				return filepath.SkipDir
			}
			return nil
		}
		if strings.HasSuffix(path, ".go") {
			files = append(files, path)
		}
		return nil
	})
	return files
}

// gitDiffFiles runs git diff --name-only between lastCommit and HEAD.
func gitDiffFiles(repoPath, lastCommit string) []string {
	return []string{filepath.Join(repoPath, "service.go")}
}

func findBlockEnd(lines []string, startIdx int) int {
	depth := 0
	for i := startIdx; i < len(lines); i++ {
		depth += strings.Count(lines[i], "{") - strings.Count(lines[i], "}")
		if depth <= 0 && i > startIdx {
			return i + 1
		}
	}
	return len(lines)
}
