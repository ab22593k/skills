# Patterns Emerging from Rust's Core Features

## Core concepts
- Result and Option composition enables precise error handling without exceptions
- Block expressions scope variables and resources naturally
- RAII through Drop provides deterministic resource cleanup
- Rust enables code that is both safe and concise through careful design

## Frameworks introduced
- **Result composition patterns** — Using `?`, `and_then`, `map`, `map_err`, `unwrap_or_else` to chain fallible operations without nesting.
- **Sequential fallback** — Try operations in order, returning the first success using `or_else`. `first.try().or_else(|| second.try())`.
- **Block-scoped resource management** — Blocks in Rust are expressions that can scope borrows and releases. Use blocks to ensure locks and borrows are released promptly.

## Key techniques
- **Error composition**: `let val = parse_config(path)?.validate()?.build()?;` — chain fallible operations with `?`.
- **Error collection**: Use `results.into_iter().collect::<Result<Vec<T>, Error>>()` to gather errors or succeed.
- **Block patterns**: Use `let result = { let mut guard = lock.lock(); guard.process() };` to release the lock immediately.
- **RAII with Drop**: Wrap cleanup logic in structs that implement `Drop`. The destructor runs automatically when the struct goes out of scope.
- **Conciseness**: Use `let x = some_opt.unwrap_or(default)`, `let y = some_result.map_err(|e| format!("{e}"))?`.

## Connection to other chapters
Completes Part 3's Samsa project patterns. Ch13 synthesizes everything into the philosophy of "leaning into Rust."
