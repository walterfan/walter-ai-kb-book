/* 
// BOOK EXCERPT — vendored for citation, do not hand-edit
// source_repo:     code-layer-reference-impl
// source_path:     reference-impl/code-kg/enricher/service.go
// commit_sha:      7afa52003fd6  (dirty — uncommitted changes)
// captured_at:     2026-04-18T01:15:58Z
// content_sha256:  596598c489ca6dcf685a02e8cc1e0ca9e6c6be663e7cbe086b3e36a6b67375b7
// regenerate with: make book-refresh-excerpts
 */

package enricher

import (
	"fmt"
	"math"
	"time"

	"example.com/reference-impl/code-kg-repo/internal/rag"
)

type Embedder interface {
	GenerateEmbeddings(texts []string) ([][]float32, error)
	GenerateEmbedding(text string) ([]float32, error)
}

type Summarizer interface {
	SummarizeCode(language, name, body string) (string, error)
}

type Options struct {
	MaxRetries  int
	RetryBaseMs int
	RateLimit   int // max requests per minute, 0 = unlimited
}

type Service struct {
	embedder    Embedder
	summarizer  Summarizer
	maxRetries  int
	retryBaseMs int
	rateLimit   int
	lastCall    time.Time
}

func New(embedder *rag.EmbeddingService) *Service {
	if embedder == nil {
		return &Service{}
	}
	return &Service{
		embedder:    embedder,
		maxRetries:  3,
		retryBaseMs: 500,
	}
}

func NewWithOptions(embedder Embedder, opts Options) *Service {
	maxRetries := opts.MaxRetries
	if maxRetries <= 0 {
		maxRetries = 3
	}
	retryBase := opts.RetryBaseMs
	if retryBase <= 0 {
		retryBase = 500
	}
	return &Service{
		embedder:    embedder,
		maxRetries:  maxRetries,
		retryBaseMs: retryBase,
		rateLimit:   opts.RateLimit,
	}
}

func (s *Service) Available() bool {
	return s != nil && s.embedder != nil
}

func (s *Service) GenerateEmbeddings(texts []string) ([][]float32, error) {
	if !s.Available() {
		return nil, fmt.Errorf("embedding service unavailable")
	}
	s.throttle()
	var lastErr error
	attempts := 1 + s.maxRetries
	for i := 0; i < attempts; i++ {
		result, err := s.embedder.GenerateEmbeddings(texts)
		if err == nil {
			return result, nil
		}
		lastErr = err
		if i < attempts-1 {
			backoff := time.Duration(float64(s.retryBaseMs)*math.Pow(2, float64(i))) * time.Millisecond
			time.Sleep(backoff)
		}
	}
	return nil, lastErr
}

func (s *Service) GenerateEmbedding(text string) ([]float32, error) {
	if !s.Available() {
		return nil, fmt.Errorf("embedding service unavailable")
	}
	embs, err := s.GenerateEmbeddings([]string{text})
	if err != nil {
		return nil, err
	}
	if len(embs) == 0 {
		return nil, fmt.Errorf("no embedding returned")
	}
	return embs[0], nil
}

func (s *Service) GenerateSummary(language, name, body string) (string, error) {
	if s.summarizer == nil {
		return "", nil
	}
	return s.summarizer.SummarizeCode(language, name, body)
}

func (s *Service) SetSummarizer(summarizer Summarizer) {
	s.summarizer = summarizer
}

func (s *Service) throttle() {
	if s.rateLimit <= 0 {
		return
	}
	minInterval := time.Minute / time.Duration(s.rateLimit)
	elapsed := time.Since(s.lastCall)
	if elapsed < minInterval {
		time.Sleep(minInterval - elapsed)
	}
	s.lastCall = time.Now()
}

func BuildEntityInput(language, entityType, name, signature, docString string) string {
	return fmt.Sprintf("Language: %s\nType: %s\nName: %s\nSignature: %s\nDoc: %s",
		language, entityType, name, signature, docString)
}
