# Cheatsheet

## Integer Type Selection

| Bits | Unsigned | Signed | Range (signed) |
|------|----------|--------|----------------|
| 8 | `u8` | `i8` | -128 to 127 |
| 16 | `u16` | `i16` | -32,768 to 32,767 |
| 32 | `u32` | `i32` | -2³¹ to 2³¹-1 |
| 64 | `u64` | `i64` | -2⁶³ to 2⁶³-1 |
| 128 | `u128` | `i128` | -2¹²⁷ to 2¹²⁷-1 |
| arch | `usize` | `isize` | pointer-width |

Default: `i32` for integers, `f64` for floats.

## Ownership Quick Reference

| Operation | Stack types (i32, bool, char) | Heap types (String, Vec) |
|-----------|-------------------------------|--------------------------|
| Assignment (`y = x`) | Copy | Move (x invalidated) |
| Pass to function | Copy | Move (can't use after) |
| `.clone()` | N/A (already copy) | Deep copy (both valid) |
| `&x` | Borrow (immutable) | Borrow (immutable) |
| `&mut x` | Borrow (mutable, exclusive) | Borrow (mutable, exclusive) |

## Reference Rules

| Scenario | Allowed? |
|----------|----------|
| Multiple `&T` (immutable) | Yes |
| One `&mut T` (mutable) | Yes |
| `&T` + `&mut T` same scope | No |
| `&mut T` after previous `&mut T` scope ends | Yes |

## Error Handling Patterns

| Pattern | When to use | Syntax |
|---------|-------------|--------|
| `?` operator | Fallible functions, propagate errors | `let val = fallible()?;` |
| `.unwrap()` | Truly infallible or test code | `let val = result.unwrap();` |
| `.expect(msg)` | Panic with context message | `let val = result.expect("file should exist");` |
| `panic!` | Unrecoverable error | `panic!("invalid state: {}", x);` |
| `match` on Result | Need different handling per variant | `match result { Ok(v) => ..., Err(e) => ... }` |

## Concurrency Decision Table

| Need | Solution |
|------|----------|
| One-way communication between threads | `mpsc::channel()` + `sender.send(data)` |
| Shared mutable state across threads | `Arc<Mutex<T>>` — lock before access |
| Read-only shared data across threads | `Arc<T>` — no mutex needed |
| Wait for thread to finish | `handle.join()` |
| Spawn thread with owned data | `thread::spawn(move || { ... })` |
| Async I/O (hundreds of connections) | Tokio: `tokio::spawn` + `.await` |

## Build Profile Quick Reference

| Profile | Command | Optimization | Debug info | Use case |
|---------|---------|--------------|------------|----------|
| dev | `cargo build` | None | Full | Development iteration |
| release | `cargo build --release` | Speed (O3) | Minimal | Production deployment |
| test | `cargo test` | None | Full | Running tests |
| bench | `cargo bench` | Speed | Minimal | Performance benchmarks |

## Cargo.toml Dependency Types

| Section | Purpose |
|---------|---------|
| `[dependencies]` | Runtime library dependencies |
| `[dev-dependencies]` | Test/benchmark only (not propagated) |
| `[build-dependencies]` | Dependencies for `build.rs` scripts |
| `[target.'cfg(...)'.dependencies]` | Platform-specific dependencies |

## Thread Safety Traits

| Trait | Meaning | Auto-implemented? |
|-------|---------|-------------------|
| `Send` | Owned transfer across threads | Yes (most types) |
| `Sync` | Shared reference across threads | Yes (most types) |

Not `Send`/`Sync`: `Rc<T>`, `RefCell<T>`, raw pointers. Wrap in newtypes to opt in after verification.

## Quick rules

- Variables are immutable by default — add `mut` to change
- `match` must be exhaustive — use `_` as catch-all
- `?` only works in functions returning `Result` or `Option`
- `cargo check` is faster than `cargo build` for compile verification
- One `&mut T` XOR many `&T` — never both in same scope
- Always validate inputs at FFI boundaries
- Minimize `unsafe` — wrap in safe abstractions
- `#[repr(C)]` required for FFI struct compatibility
- Prefer `expect("msg")` over `unwrap()` for actionable panic messages
- A package can have 0 or 1 library crates and many binary crates
