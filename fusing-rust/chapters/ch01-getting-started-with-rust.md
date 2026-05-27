# Getting Started with Rust

## Core concepts

- Rust is installed and managed by `rustup` — one tool to install, update, and uninstall
- `cargo` is both the build system and package manager: `cargo new`, `cargo build`, `cargo run`, `cargo check`
- `rustc` is the compiler, but you'll almost always use `cargo` instead
- Four build profiles: `dev` (default), `release` (optimized), `test` (test executables), `bench` (benchmarks)
- `cargo check` verifies compilability without producing an executable — faster for iterative development

## Frameworks introduced

**The rustup toolchain manager** — Manages Rust installations, updates, and cross-compilation targets. Use `rustup update` to stay current, `rustup target add` for embedded/WASM targets.

**Cargo build profiles** — Each profile controls optimization level and debug info. `--release` optimizes for speed; `dev` optimizes for fast compile times.

## Key techniques

1. Install Rust: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
2. Verify: `rustc --version && cargo --version && rustdoc --version`
3. New project: `cargo new hello_world`
4. Build and run: `cargo run`
5. Check without building: `cargo check`
6. Release build: `cargo build --release`

## Code examples

```rust
fn main() {
    println!("Hello, world...");
}
```

## Connection to other chapters

Sets up the tooling used throughout the entire book. Every subsequent chapter assumes `cargo` and `rustup` are installed.
