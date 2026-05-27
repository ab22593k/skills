# Patterns

## Move, Clone, Copy Decision

**Type:** technique
**Context:** Assigning or passing a value to another variable or function.
**Solution:**
- **Copy** — Use for stack-only types (integers, bools, chars). Implicit, no runtime cost.
- **Move** — Default for heap types (`String`, `Vec`). Ownership transfers; source is invalidated.
- **Clone** — Explicit `.clone()` for heap types when both copies must remain valid.
**Consequences:** Move prevents double-free bugs. Clone has runtime cost. Copy is free but only for simple types.
**Related:** Ch3 Ownership

## Safe Unsafe Boundary

**Type:** technique
**Context:** Writing `unsafe` code that must be used safely by callers.
**Solution:** Minimize unsafe blocks to a single operation. Wrap each unsafe block in a safe function that validates preconditions. Never expose raw pointers in the safe public API.
**Consequences:** Callers get a safe interface. Bugs are contained within the unsafe wrapper.
**Related:** Ch16 Unsafe Rust, Ch17 FFI

## Newtype Pattern

**Type:** technique
**Context:** Creating a distinct type from an existing one for type safety.
**Solution:** Use a tuple struct: `struct Kilometers(i32)`. Implement `Deref` for transparent access, or add methods directly.
**Consequences:** Compiler prevents mixing `Kilometers` with plain `i32`. No runtime overhead.
**Related:** Ch4 Structs

## Message-Passing Concurrency

**Type:** technique
**Context:** Communicating between threads without shared memory.
**Solution:** Use `std::sync::mpsc::channel()`. Send data from one or more producers. The single consumer receives in FIFO order. Ownership of sent data transfers to the receiver.
**Consequences:** No data races by construction. Ownership rules guarantee safe transfer.
**Related:** Ch10 Concurrency

## Shared-State Concurrency with Arc+Mutex

**Type:** technique
**Context:** Multiple threads need access to shared mutable state.
**Solution:** `Arc<Mutex<T>>` — `Arc` for shared ownership, `Mutex` for interior mutability and mutual exclusion. Clone the `Arc` for each thread, lock before access.
**Consequences:** Thread-safe mutable shared state. Lock contention can hurt performance.
**Related:** Ch10 Concurrency

## RAFT (Read-After-Function Type) — Generics with Trait Bounds

**Type:** principle
**Context:** Writing a function that works across multiple types with specific capabilities.
**Solution:** Use generic `<T>` with trait bounds: `fn process<T: Display + Debug>(item: &T)`. Two syntaxes: `impl Trait` (concise) and trait bound `T: Trait` (flexible with multiple params).
**Consequences:** Zero-cost polymorphism. Errors caught at compile time.
**Related:** Ch7 Generics and Traits

## Error Propagation with `?`

**Type:** technique
**Context:** A function that calls several fallible operations and should fail fast on any error.
**Solution:** Return `Result<T, E>`. Use `?` after each fallible call. On `Err`, return early. On `Ok`, unwrap the value.
**Consequences:** Concise, readable error handling. Errors propagate to the caller who decides how to handle them.
**Related:** Ch6 Error Handling

## Buffered I/O

**Type:** technique
**Context:** Reading or writing a large file or stream in small amounts.
**Solution:** Wrap a `File` or `TcpStream` with `BufReader` or `BufWriter`. The buffer pre-fetches data, reducing system calls.
**Consequences:** Dramatically faster I/O for many small reads/writes. Slightly more memory per stream.
**Related:** Ch8 File Systems, Ch11 Device I/O

## RAII Guard Pattern

**Type:** principle
**Context:** Managing resources (locks, file handles, memory) that must be released.
**Solution:** Resource acquisition ties to initialization. Resource release ties to `Drop`. `MutexGuard` unlocks on drop; `File` closes on drop. The compiler guarantees destructors run.
**Consequences:** No forgotten releases. Exception-safe even on panic (during unwind).
**Related:** Ch3 Ownership, Ch10 Concurrency

## Module Tree Organization

**Type:** technique
**Context:** Structuring a Rust project beyond a single file.
**Solution:** Define modules with `mod` (one file per module mirrors the module tree). Make items `pub` to expose them. Use `crate::module::item` paths internally. Re-export public API at the crate root with `pub use`.
**Consequences:** Clean, navigable codebase. Clear public API boundary.
**Related:** Ch5 Packages, Crates, Modules

## Compile-Time Memory Safety (no garbage collector)

**Type:** principle
**Context:** Ensuring safe memory management without runtime overhead or a GC.
**Solution:** Ownership rules + borrow checker verify every memory access at compile time. No dangling pointers, no double frees, no use-after-free. Zero-cost — all checks happen before the binary runs.
**Consequences:** Safe code runs at C-like speed. The borrow checker can be frustrating until ownership patterns become intuitive.
**Related:** Ch3 Ownership, Ch10 Concurrency

## Testing with `#[cfg(test)]`

**Type:** technique
**Context:** Writing unit tests in the same file as production code.
**Solution:** Add `#[cfg(test)] mod tests { use super::*; #[test] fn test_fn() { ... } }`. Build and run with `cargo test`. Test-only dependencies go in `[dev-dependencies]`.
**Consequences:** Tests live next to code. Never compiled into release builds.
**Related:** Ch1 Cargo basics

## FFI Safety Boundary

**Type:** anti-pattern
**Context:** Declaring an FFI function that takes or returns raw pointers without validation.
**Problem:** Passing null pointers, invalid lengths, or dangling references across the FFI boundary causes undefined behavior.
**Solution:** Validate all inputs at the FFI boundary. Use `CStr` instead of raw `*const c_char`. Check pointer nullity. Never trust external input.
**Consequences:** Prevents memory corruption at the cross-language seam.
**Related:** Ch17 FFI

## God Struct (anti-pattern)

**Type:** anti-pattern
**Context:** A single struct that accumulates too many responsibilities.
**Problem:** The struct becomes impossible to reason about, test, or change safely.
**Solution:** Split into smaller structs that each own one responsibility. Use traits to share behavior across types.
**Consequences:** More files, but each is testable and composable.
**Related:** Ch4 Structs, Ch7 Traits
