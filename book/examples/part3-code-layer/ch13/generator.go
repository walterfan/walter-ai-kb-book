/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     code-layer-reference-impl
// source_path:     reference-impl/code-kg/generator/generator.go
// commit_sha:      7afa52003fd6  (dirty — uncommitted changes)
// captured_at:     2026-04-18T01:15:58Z
// content_sha256:  64ed5b81dd4ac815119617d12552c80a42ece6fc83cc58cf07b00bdda748366d
// regenerate with: make book-refresh-excerpts
 */

package generator

import (
	"fmt"
	"path/filepath"
	"strings"
)

type RepoMapEntity struct {
	Name       string
	EntityType string
	Language   string
	FilePath   string
	StartLine  int
}

type OverviewEntity struct {
	Name       string
	EntityType string
	FilePath   string
	StartLine  int
	Signature  string
}

type Snippet struct {
	EntityType string
	Name       string
	FilePath   string
	StartLine  int
	EndLine    int
	Body       string
}

func BuildDirTree(rootPath string, codeFiles []string) string {
	dirs := map[string]int{}
	for _, filePath := range codeFiles {
		relPath, _ := filepath.Rel(rootPath, filePath)
		if relPath == "" {
			relPath = filePath
		}
		dir := filepath.Dir(relPath)
		dirs[dir]++
	}

	var lines []string
	for dir, count := range dirs {
		lines = append(lines, fmt.Sprintf("%-50s (%d files)", dir+"/", count))
	}

	for i := 0; i < len(lines); i++ {
		for j := i + 1; j < len(lines); j++ {
			if lines[j] < lines[i] {
				lines[i], lines[j] = lines[j], lines[i]
			}
		}
	}

	return strings.Join(lines, "\n")
}

func BuildRepoMapContent(repoName, repoPath string, codeFiles []string, entities []RepoMapEntity) string {
	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("# Repository Map: %s\n\n", repoName))
	sb.WriteString("## Directory Structure\n\n```\n")
	sb.WriteString(BuildDirTree(repoPath, codeFiles))
	sb.WriteString("```\n\n")

	langCount := map[string]int{}
	typeCount := map[string]int{}
	for _, entity := range entities {
		langCount[entity.Language]++
		typeCount[entity.EntityType]++
	}

	sb.WriteString("## Language Breakdown\n\n")
	sb.WriteString("| Language | Entities |\n|---|---|\n")
	for lang, count := range langCount {
		sb.WriteString(fmt.Sprintf("| %s | %d |\n", lang, count))
	}

	sb.WriteString("\n## Entity Summary\n\n")
	sb.WriteString("| Type | Count |\n|---|---|\n")
	for entityType, count := range typeCount {
		sb.WriteString(fmt.Sprintf("| %s | %d |\n", entityType, count))
	}

	sb.WriteString("\n## Key Entry Points\n\n")
	for _, entity := range entities {
		if entity.EntityType == "function" && IsEntryPoint(entity.Name) {
			sb.WriteString(fmt.Sprintf("- **%s** — `%s:%d`\n", entity.Name, entity.FilePath, entity.StartLine))
		}
	}

	sb.WriteString(fmt.Sprintf("\n## Stats\n\n- **Total files**: %d\n- **Total entities**: %d\n", len(codeFiles), len(entities)))
	return sb.String()
}

func BuildOverviewPrompt(repoName, repoPath string, codeFiles []string, entities []OverviewEntity, maxEntities int) (string, string) {
	systemPrompt := `You are a senior engineer writing a concise project overview for an AI-readable knowledge base.
Follow this structure:
1. Purpose — what problem the project solves (1-2 sentences)
2. Technology Stack — languages, frameworks, databases
3. Architecture — high-level module structure
4. Key Components — most important modules/packages and their roles
5. Entry Points — where the app starts, main routes, CLI commands

Be specific. Reference actual file paths and function names from the provided data.
Keep it under 500 words. Use Markdown.`

	var summary strings.Builder
	summary.WriteString(fmt.Sprintf("Repository: %s\nPath: %s\nFiles: %d\n\n", repoName, repoPath, len(codeFiles)))

	shown := 0
	for _, entity := range entities {
		if maxEntities > 0 && shown >= maxEntities {
			break
		}
		summary.WriteString(fmt.Sprintf("[%s] %s — %s:%d %s\n", entity.EntityType, entity.Name, entity.FilePath, entity.StartLine, entity.Signature))
		shown++
	}

	return systemPrompt, summary.String()
}

func BuildAnswerPrompt(query string, snippets []Snippet) (string, string) {
	systemPrompt := `You are a code knowledge base expert. Answer the user's question based on the code entities provided.
Always cite specific function/file locations. If the code context is insufficient, say so honestly.`

	var contextParts []string
	for i, snippet := range snippets {
		part := fmt.Sprintf("### [%d] %s `%s` (%s:%d-%d)\n```\n%s\n```",
			i+1, snippet.EntityType, snippet.Name, snippet.FilePath, snippet.StartLine, snippet.EndLine, snippet.Body)
		contextParts = append(contextParts, part)
	}

	return systemPrompt, fmt.Sprintf("## Code Context\n%s\n\n## Question\n%s", strings.Join(contextParts, "\n\n"), query)
}

func IsEntryPoint(name string) bool {
	return name == "main" || name == "init" ||
		strings.HasPrefix(name, "New") ||
		strings.HasPrefix(name, "Handle") ||
		strings.HasPrefix(name, "Setup")
}
