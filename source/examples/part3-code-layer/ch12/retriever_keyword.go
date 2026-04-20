/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     code-layer-reference-impl
// source_path:     reference-impl/code-kg/retriever/keyword.go
// commit_sha:      7afa52003fd6  (dirty — uncommitted changes)
// captured_at:     2026-04-18T01:15:58Z
// content_sha256:  61515af58d2236dc287200475d0c042168ae220a4c558aa04c7a02b497bbe212
// regenerate with: make book-refresh-excerpts
 */

package retriever

import "strings"

type Document struct {
	ID   string
	Name string
	Body string
}

type ScoredDocument struct {
	ID    string
	Score int
}

func RankByKeyword(query string, docs []Document, topK int) []ScoredDocument {
	queryLower := strings.ToLower(query)
	words := strings.Fields(queryLower)

	var results []ScoredDocument
	for _, doc := range docs {
		score := 0
		nameLower := strings.ToLower(doc.Name)
		bodyLower := strings.ToLower(doc.Body)
		for _, word := range words {
			if strings.Contains(nameLower, word) {
				score += 3
			}
			if strings.Contains(bodyLower, word) {
				score += 1
			}
		}
		if score > 0 {
			results = append(results, ScoredDocument{ID: doc.ID, Score: score})
		}
	}

	for i := 0; i < len(results); i++ {
		for j := i + 1; j < len(results); j++ {
			if results[j].Score > results[i].Score {
				results[i], results[j] = results[j], results[i]
			}
		}
	}

	if topK > 0 && len(results) > topK {
		return results[:topK]
	}
	return results
}
