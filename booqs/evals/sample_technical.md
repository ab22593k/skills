# Practical Go: Patterns for Production Systems

## Foreword

This book is for Go developers building production services. It focuses on patterns that have been proven at scale.

## Chapter 1: Error Handling

Go's error handling is explicit by design. The language forces you to deal with errors where they occur, not defer them to a catch block.

### Sentinel Errors

Define sentinel errors as package-level variables:

```go
var ErrNotFound = errors.New("item not found")
```

Use `errors.Is()` to check for sentinel errors. This works through wrapped errors.

### Error Types

Define custom error types when callers need to inspect structured information:

```go
type ValidationError struct {
    Field string
    Value any
    Msg   string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed on %s: %s", e.Field, e.Msg)
}
```

Use `errors.As()` to extract typed errors from the chain.

### Wrapping Errors

Always wrap errors with context:

```go
if err != nil {
    return fmt.Errorf("reading config: %w", err)
}
```

_Anti-pattern:_ Using `%v` or `%s` instead of `%w` breaks the error chain and prevents callers from using `errors.Is()` and `errors.As()`.

## Chapter 2: Concurrency Patterns

Go's concurrency model is based on communicating sequential processes (CSP). Share memory by communicating, don't communicate by sharing memory.

### Pipeline Pattern

Connect stages with channels:

```go
func generate(ctx context.Context, nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, n := range nums {
            select {
            case out <- n:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}
```

_Principle:_ Always let the receiver close channels in a fan-in pattern. The generator closes its output when done.

### Fan-Out, Fan-In

Distribute work across multiple goroutines, then merge results:

- Fan-Out: Start N goroutines reading from the same input channel
- Fan-In: Merge multiple output channels into one using reflection or a merge function

### Context Propagation

Pass `context.Context` as the first parameter to every function that makes a network call or blocks. This ensures cancellation propagates correctly through the call chain.

## Chapter 3: Testing

### Table-Driven Tests

```go
func TestParseDuration(t *testing.T) {
    tests := []struct {
        name     string
        input    string
        expected time.Duration
        wantErr  bool
    }{
        {"valid seconds", "30s", 30 * time.Second, false},
        {"valid minutes", "5m", 5 * time.Minute, false},
        {"invalid", "abc", 0, true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := parseDuration(tt.input)
            if tt.wantErr != (err != nil) {
                t.Errorf("unexpected error status")
            }
            if result != tt.expected {
                t.Errorf("got %v, want %v", result, tt.expected)
            }
        })
    }
}
```

### Test Fixtures

Put test data in `testdata/` directories. Use `io/fs` to access them. This is a Go convention — tools like `go vet` understand it.

## Appendix: Decision Tables

| Pattern             | When to Use                  | Trade-off                              |
| ------------------- | ---------------------------- | -------------------------------------- |
| Pipeline            | Sequential processing stages | Bounded channel memory                 |
| Fan-Out             | Independent parallel work    | Goroutine management overhead          |
| Context propagation | Any blocking call            | Passes through entire call chain       |
| Table-driven tests  | Multiple input cases         | Slightly more verbose for simple cases |
