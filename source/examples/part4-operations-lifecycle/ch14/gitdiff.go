/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     code-layer-reference-impl
// source_path:     reference-impl/code-kg/syncer/gitdiff.go
// commit_sha:      7afa52003fd6  (dirty — uncommitted changes)
// captured_at:     2026-04-18T01:15:58Z
// content_sha256:  e68c3f6c74314d9436bb0acf4d5a059545f24851ca084ba2b59b9ee1f7ca47e2
// regenerate with: make book-refresh-excerpts
 */

package syncer

import (
	"fmt"
	"os/exec"
	"path/filepath"
	"strings"
)

type FileChange struct {
	Path   string
	Status ChangeStatus
}

type ChangeStatus string

const (
	StatusAdded    ChangeStatus = "added"
	StatusModified ChangeStatus = "modified"
	StatusDeleted  ChangeStatus = "deleted"
)

type DiffResult struct {
	FromCommit string
	ToCommit   string
	Changes    []FileChange
	IsFullSync bool
}

func ComputeGitDiff(repoPath, fromCommit string) (*DiffResult, error) {
	headCommit, err := gitHeadCommit(repoPath)
	if err != nil {
		return nil, fmt.Errorf("get HEAD commit: %w", err)
	}

	if fromCommit == "" {
		return &DiffResult{
			ToCommit:   headCommit,
			IsFullSync: true,
		}, nil
	}

	if fromCommit == headCommit {
		return &DiffResult{
			FromCommit: fromCommit,
			ToCommit:   headCommit,
			Changes:    nil,
		}, nil
	}

	changes, err := gitDiffNameStatus(repoPath, fromCommit, headCommit)
	if err != nil {
		return &DiffResult{
			ToCommit:   headCommit,
			IsFullSync: true,
		}, nil
	}

	return &DiffResult{
		FromCommit: fromCommit,
		ToCommit:   headCommit,
		Changes:    changes,
	}, nil
}

func IsGitRepo(repoPath string) bool {
	cmd := exec.Command("git", "-C", repoPath, "rev-parse", "--is-inside-work-tree")
	out, err := cmd.Output()
	return err == nil && strings.TrimSpace(string(out)) == "true"
}

func HeadCommit(repoPath string) (string, error) {
	return gitHeadCommit(repoPath)
}

func gitHeadCommit(repoPath string) (string, error) {
	cmd := exec.Command("git", "-C", repoPath, "rev-parse", "HEAD")
	out, err := cmd.Output()
	if err != nil {
		return "", err
	}
	return strings.TrimSpace(string(out)), nil
}

func gitDiffNameStatus(repoPath, from, to string) ([]FileChange, error) {
	cmd := exec.Command("git", "-C", repoPath, "diff", "--name-status", from, to)
	out, err := cmd.Output()
	if err != nil {
		return nil, err
	}
	return parseNameStatus(string(out)), nil
}

func parseNameStatus(output string) []FileChange {
	var changes []FileChange
	for _, line := range strings.Split(strings.TrimSpace(output), "\n") {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		parts := strings.Fields(line)
		if len(parts) < 2 {
			continue
		}
		status := parts[0]
		path := parts[len(parts)-1]

		var cs ChangeStatus
		switch {
		case strings.HasPrefix(status, "A"):
			cs = StatusAdded
		case strings.HasPrefix(status, "M"):
			cs = StatusModified
		case strings.HasPrefix(status, "D"):
			cs = StatusDeleted
		case strings.HasPrefix(status, "R"):
			cs = StatusModified
		default:
			cs = StatusModified
		}
		changes = append(changes, FileChange{Path: path, Status: cs})
	}
	return changes
}

func FilterSupportedChanges(changes []FileChange, repoPath string) []FileChange {
	supported := map[string]bool{".go": true, ".java": true, ".py": true}
	var filtered []FileChange
	for _, c := range changes {
		ext := filepath.Ext(c.Path)
		if supported[ext] {
			filtered = append(filtered, c)
		}
	}
	return filtered
}
