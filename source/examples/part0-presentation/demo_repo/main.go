package main

import (
	"fmt"
	"net/http"
)

func main() {
	cfg := LoadConfigFromEnv()
	svc := NewService(cfg)
	handler := NewHandler(svc)

	mux := http.NewServeMux()
	handler.RegisterRoutes(mux)

	addr := ":8080"
	fmt.Printf("code-kg server listening on %s\n", addr)
	if err := http.ListenAndServe(addr, mux); err != nil {
		fmt.Printf("server error: %v\n", err)
	}
}
