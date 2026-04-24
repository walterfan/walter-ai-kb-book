package main

import "os"

// Config holds all runtime settings for the code-kg service.
type Config struct {
	Embedding  EmbeddingConfig
	Graph      GraphConfig
	Retrieval  RetrievalConfig
	Generation GenerationConfig
	Sync       SyncConfig
}

type EmbeddingConfig struct {
	APIKey  string
	BaseURL string
	Model   string
}

type GraphConfig struct {
	Host     string
	Port     int
	Enabled  bool
}

type RetrievalConfig struct {
	DefaultTopK int
}

type GenerationConfig struct {
	BaseURL     string
	APIKey      string
	Model       string
	Temperature float64
}

type SyncConfig struct {
	DefaultTriggerSource string
}

// LoadConfigFromEnv reads configuration from environment variables.
func LoadConfigFromEnv() Config {
	return Config{
		Embedding: EmbeddingConfig{
			APIKey:  os.Getenv("EMBEDDING_API_KEY"),
			BaseURL: getEnv("EMBEDDING_BASE_URL", "https://api.openai.com/v1"),
			Model:   getEnv("EMBEDDING_MODEL", "text-embedding-3-small"),
		},
		Graph: GraphConfig{
			Host:    getEnv("GRAPH_HOST", "localhost"),
			Port:    7687,
			Enabled: os.Getenv("GRAPH_ENABLED") == "true",
		},
		Retrieval: RetrievalConfig{
			DefaultTopK: 10,
		},
		Generation: GenerationConfig{
			BaseURL:     getEnv("LLM_BASE_URL", "https://api.openai.com/v1"),
			APIKey:      os.Getenv("LLM_API_KEY"),
			Model:       getEnv("LLM_MODEL", "gpt-4o-mini"),
			Temperature: 0.2,
		},
		Sync: SyncConfig{
			DefaultTriggerSource: "manual",
		},
	}
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
