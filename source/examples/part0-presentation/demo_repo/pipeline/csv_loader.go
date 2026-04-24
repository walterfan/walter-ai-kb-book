package pipeline

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"strings"
)

// CSVLoader reads CSV files and converts rows into key-value records.
type CSVLoader struct {
	Delimiter rune
	HasHeader bool
}

// NewCSVLoader creates a loader with sensible defaults.
func NewCSVLoader() *CSVLoader {
	return &CSVLoader{Delimiter: ',', HasHeader: true}
}

// Record is a single row parsed from a CSV file.
type Record struct {
	Fields map[string]string
	Line   int
}

// LoadFile reads a CSV file and returns a slice of Records.
func (l *CSVLoader) LoadFile(path string) ([]Record, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, fmt.Errorf("open csv: %w", err)
	}
	defer f.Close()
	return l.parse(f)
}

// parseCSV is the core parsing function that converts an io.Reader to Records.
func (l *CSVLoader) parse(r io.Reader) ([]Record, error) {
	reader := csv.NewReader(r)
	reader.Comma = l.Delimiter
	reader.LazyQuotes = true

	var headers []string
	var records []Record
	lineNum := 0

	for {
		row, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			return records, fmt.Errorf("csv read line %d: %w", lineNum, err)
		}
		lineNum++

		if lineNum == 1 && l.HasHeader {
			headers = make([]string, len(row))
			for i, h := range row {
				headers[i] = strings.TrimSpace(h)
			}
			continue
		}

		rec := Record{Fields: make(map[string]string), Line: lineNum}
		for i, val := range row {
			key := fmt.Sprintf("col_%d", i)
			if i < len(headers) {
				key = headers[i]
			}
			rec.Fields[key] = strings.TrimSpace(val)
		}
		records = append(records, rec)
	}
	return records, nil
}

// Validate checks that required columns are present in every record.
func Validate(records []Record, requiredCols []string) error {
	for _, rec := range records {
		for _, col := range requiredCols {
			if _, ok := rec.Fields[col]; !ok {
				return fmt.Errorf("line %d: missing required column %q", rec.Line, col)
			}
		}
	}
	return nil
}
