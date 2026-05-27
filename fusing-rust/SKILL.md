---
name: fusing-rust
description: "Master Rust systems programming — ownership, concurrency, FFI, embedded, WebAssembly, and scripting."
effort: high
---

## Core Mental Models

### Ownership Principle
- **Use:** Safe memory management without GC
- **Idea:** One owner per value; compiler enforces at compile time
- **Apply:** Track ownership; borrow (`&T`, `&mut T`) for temporary access; clone for shared ownership
- **Pitfall:** Fighting borrow checker → restructure design

### Send and Sync Traits
- **Use:** Concurrent/multi-threaded programs
- **Idea:** `Send` = transfer across threads; `Sync` = share references across threads
- **Apply:** `Arc<T>` for shared ownership; `Mutex<T>` for interior mutability
- **Pitfall:** Raw pointers aren't Send/Sync → wrap in newtypes after safety verification

### Error Handling with Result
- **Use:** Fallible operations (I/O, parsing, network)
- **Idea:** `Result<T, E>` for recoverable errors; `?` propagates; `panic!` for unrecoverable
- **Apply:** Return `Result` from fallible functions; use `?` for propagation
- **Pitfall:** Swallowing errors with `.ok()` → use `thiserror` or `anyhow`

### `unsafe` Superpowers
- **Use:** FFI, raw pointers, performance-critical hot paths
- **Idea:** Five operations require `unsafe` — caller responsible for memory safety
- **Apply:** Minimize unsafe blocks; encapsulate in safe abstractions
- **Pitfall:** Undefined behavior from mistakes

## How to Use

Load when writing/reviewing Rust code (ownership, concurrency, unsafe, FFI, embedded, WASM).

```
@fusing-rust load chapter 7    # Generics and traits
@fusing-rust glossary          # Term lookups
@fusing-rust patterns          # Techniques and anti-patterns
```

## Chapter Index

| # | Title | Topic |
|---|-------|-------|
| 1 | Getting Started | rustup, cargo, profiles |
| 2 | Fundamentals | Variables, types, functions |
| 3 | Ownership | Ownership, borrowing, slices |
| 4 | Structs/Enums | Structs, enums, collections |
| 5 | Modules | Module system, crates |
| 6 | Error Handling | Result, panic!, abort |
| 7 | Generics/Traits | Generic types, trait bounds |
| 8 | File Systems | std::fs, paths, metadata |
| 9 | Text Processing | String, Unicode, format! |
| 10 | Concurrency | thread::spawn, Mutex, channels |
| 11 | Device I/O | BufReader, stdin/stdout |
| 12 | Terminals | crossterm, tui-rs |
| 13 | Processes | Command, child processes, signals |
| 14 | Databases | SQLite, MongoDB, CRUD |
| 15 | Network | TcpListener, TcpStream, Tokio |
| 16 | Unsafe Rust | raw pointers, mutable statics |
| 17 | FFI | extern "C", CString, #[repr(C)] |
| 18 | Embedded | HAL, microcontrollers |
| 19 | WebAssembly | wasm-pack, wasm-bindgen |
| 20 | Rhai | Scripting, Engine API |

## Reference Files

- `glossary.md` — Term definitions
- `patterns.md` — Techniques and anti-patterns
- `cheatsheet.md` — Decision tables
- `chapters/chXX-*.md` — Deep dives (load on demand)

## Token Efficiency

Apply `@token-efficiency` for model selection and tool optimization strategies when implementing Rust code.