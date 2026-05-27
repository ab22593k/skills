---
name: fusing-rust
description: "Master Rust systems programming — ownership, concurrency, FFI, embedded, WebAssembly, and scripting — to build secure, scalable, and high-performance applications."
effort: high
---

## Core mental models

### Ownership Principle

- **When to use** — Managing memory safely without a garbage collector in any Rust program.
- **The idea** — Every value has exactly one owner. When the owner goes out of scope, the value is dropped. The compiler enforces this at compile time — no runtime overhead, no data races.
- **How to apply** — Track who owns each piece of data. Use borrowing (`&T`, `&mut T`) when you need temporary access without transferring ownership. Clone explicitly when shared ownership is needed.
- **Pitfalls** — Fighting the borrow checker usually means your design shares ownership too broadly. Restructure to minimize long-lived references.

### Send and Sync Traits

- **When to use** — Designing concurrent or multi-threaded Rust programs.
- **The idea** — `Send` types are safe to transfer ownership across threads. `Sync` types are safe to share references across threads. Most types auto-implement both.
- **How to apply** — Use `Arc<T>` for shared ownership across threads. Use `Mutex<T>` for interior mutability in concurrent contexts. The compiler prevents you from accidentally sending non-Send types across threads.
- **Pitfalls** — Raw pointers and some FFI types are neither Send nor Sync. Wrap them in newtypes and implement the traits only after verifying safety.

### Error Handling with Result

- **When to use** — Any operation that can fail — I/O, parsing, network calls.
- **The idea** — Rust divides errors into recoverable (`Result<T, E>`) and unrecoverable (`panic!`). The `?` operator propagates errors up the call stack ergonomically.
- **How to apply** — Return `Result` from fallible functions. Use `?` to unwrap early on error. Use `unwrap()` or `expect()` only when failure is truly impossible or you want a controlled crash.
- **Pitfalls** — Swallowing errors with `.ok()` or ignoring `Result` warnings leads to silent failures. Define custom error types with `thiserror` or `anyhow` for production code.

### `unsafe` Superpowers

- **When to use** — FFI, raw pointer manipulation, performance-critical hot paths where the borrow checker is too restrictive.
- **The idea** — Five operations require `unsafe`: dereferencing raw pointers, calling unsafe functions, accessing mutable statics, implementing unsafe traits, and accessing union fields. The caller bears responsibility for memory safety.
- **How to apply** — Minimize unsafe blocks. Encapsulate each unsafe operation in a safe abstraction. Validate invariants before entering unsafe code.
- **Pitfalls** — Unsafe code is not checked by the compiler. A single mistake can introduce undefined behavior — segfaults, use-after-free, or corrupted data.

## How to use this skill

Load this skill when writing or reviewing Rust systems-level code — ownership, concurrency, unsafe, FFI, embedded, or WebAssembly. The chapter files are loaded on demand by referencing the index below.

- `skill integrating-rust` — loads this SKILL.md (mental models + index)
- Read `chapters/chXX-*.md` for deep-dive on a specific topic
- `glossary.md` for quick term lookups
- `patterns.md` for reusable techniques
- `cheatsheet.md` for decision tables

## Chapter index

| #   | Title                           | Topic                                                                      | Tokens |
| --- | ------------------------------- | -------------------------------------------------------------------------- | ------ |
| 1   | Getting Started with Rust       | Installation, rustup, cargo, Hello World, profiles                         | ~1K    |
| 2   | Fundamentals of Rust            | Variables, mutability, data types, functions, control flow                 | ~1K    |
| 3   | Ownership and Memory Management | Ownership rules, stack vs heap, move/clone/copy, borrowing, slices         | ~1K    |
| 4   | Structs, Enums, and Collections | Structs, field init shorthand, update syntax, enums, match, Vec, HashMap   | ~1K    |
| 5   | Packages, Crates, and Modules   | Module system, packages, binary/library crates, paths, `use`               | ~1K    |
| 6   | Error Handling                  | Result, panic!, backtrace, unwrap, expect, abort strategy                  | ~1K    |
| 7   | Generics and Traits             | Generic types, trait definition, impl Trait, trait bounds, multiple traits | ~1K    |
| 8   | Working with File Systems       | std::fs, file I/O, directories, paths, hard/soft links, metadata queries   | ~1K    |
| 9   | Text Processing                 | String vs &str, Unicode/UTF-8, format!, println!, pattern matching         | ~1K    |
| 10  | Concurrency and Parallelism     | thread::spawn, Mutex, channels, Arc, Send/Sync, data race prevention       | ~1K    |
| 11  | Device Input/Output             | Device files, BufReader/BufWriter, stdin/stdout/stderr, USB detection      | ~1K    |
| 12  | Working with Terminals          | Terminal I/O, crossterm, tui-rs, cursor control, styling, keyboard/mouse   | ~1K    |
| 13  | Processes and Signal Handling   | Command::new, child processes, signals, environment vars, basic shell      | ~1K    |
| 14  | Working with Databases          | SQLite (rusqlite), MongoDB, CRUD, transactions, SQL vs NoSQL               | ~1K    |
| 15  | Network Programming             | std::net, TcpListener, TcpStream, UDP, Tokio async, DNS resolution         | ~1K    |
| 16  | Unsafe Rust                     | unsafe keyword, raw pointers, mutable statics, unsafe traits, unions       | ~1K    |
| 17  | Foreign Function Interface      | extern "C", FFI, CString, #[repr(C)], callbacks, build.rs                  | ~1K    |
| 18  | Embedded Rust                   | Microcontrollers, HAL, AVR-Rust, Arduino Uno, LED blink                    | ~1K    |
| 19  | Running Rust from Web Browsers  | WebAssembly, wasm-pack, wasm-bindgen, cargo-generate, login app            | ~1K    |
| 20  | Working with Rhai               | Rhai scripting, Engine API, Rust↔Rhai interop, plugins                    | ~1K    |

## Reference files

- **glossary.md** — Alphabetized terms across all chapters
- **patterns.md** — Reusable techniques, principles, anti-patterns
- **cheatsheet.md** — Decision tables and quick-reference
