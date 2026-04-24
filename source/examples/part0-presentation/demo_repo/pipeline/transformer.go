package pipeline

import (
	"fmt"
	"strings"
)

// Transformer applies a sequence of transformations to records.
type Transformer struct {
	steps []TransformStep
}

// TransformStep is a single transformation applied to each record.
type TransformStep struct {
	Name string
	Fn   func(*Record) error
}

// NewTransformer creates a transformer with the given steps.
func NewTransformer(steps ...TransformStep) *Transformer {
	return &Transformer{steps: steps}
}

// Transform applies all steps to every record, returning errors per record.
func (t *Transformer) Transform(records []Record) ([]Record, []error) {
	var errs []error
	var out []Record
	for _, rec := range records {
		skip := false
		for _, step := range t.steps {
			if err := step.Fn(&rec); err != nil {
				errs = append(errs, fmt.Errorf("step %s, line %d: %w",
					step.Name, rec.Line, err))
				skip = true
				break
			}
		}
		if !skip {
			out = append(out, rec)
		}
	}
	return out, errs
}

// NormalizeWhitespace trims and collapses whitespace in all fields.
func NormalizeWhitespace() TransformStep {
	return TransformStep{
		Name: "normalize_whitespace",
		Fn: func(r *Record) error {
			for k, v := range r.Fields {
				r.Fields[k] = strings.Join(strings.Fields(v), " ")
			}
			return nil
		},
	}
}

// RequireNonEmpty rejects records where the named column is blank.
func RequireNonEmpty(column string) TransformStep {
	return TransformStep{
		Name: fmt.Sprintf("require_non_empty(%s)", column),
		Fn: func(r *Record) error {
			if strings.TrimSpace(r.Fields[column]) == "" {
				return fmt.Errorf("column %q is empty", column)
			}
			return nil
		},
	}
}
