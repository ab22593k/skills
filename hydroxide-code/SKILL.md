---
name: hydroxide-code
description: Guidelines for adopting modern Rust features. Use this skill whenever working with async code (async closures, AsyncFn traits), upgrading crates past Rust 1.85, modernizing async services, writing FFI or embedded code (naked functions), or migrating to the 2024 edition. Essential for anyone maintaining performance-critical libraries, tokio/async-std services, embedded systems code, or crates that need to stay current with stable Rust. Also use when replacing manual Future implementations, implementing trait upcasting, working with const generics, or needing safe raw pointer operations.
---

**SKILL: Guidelines for Using Modern Rust Features**

### Overview

This skill provides precise, production-ready guidelines for adopting every major language and standard-library feature stabilized between Rust 1.85.0 AND beyond.
It begins with the flagship feature — **async closures** — and proceeds chronologically.

**Target audience**: Intermediate-to-advanced Rust developers maintaining libraries, async services, embedded code, or performance-critical crates who want to stay on the latest stable toolchain without nightly features.

### When to Use This Skill

- You are upgrading a crate past 1.85 and want to remove `async {}` blocks or manual `Future` impls.
- You need cleaner trait-object upcasting, naked functions for FFI/embedded, const-generic inference, or safe raw-pointer unions.
- You want to future-proof code against the stabilization of the never type (`!`).
- You are writing async-heavy code, low-level systems code, or performance-critical libraries.

**Do NOT use** if your MSRV is below 1.85 or if you must stay on an older edition for downstream compatibility.

### Core Principles (apply to every feature below)

- Always add the feature to your MSRV and document the bump.
- Prefer the new syntax over older workarounds (e.g. `async move {}` blocks).
- Enable `#![warn(...)]` lints introduced in the same release.

### Feature-by-Feature Guidelines

#### 1.85.0 – Async Closures (the starting point)

**Stabilized**: `async |args| { ... }`, traits `AsyncFn`, `AsyncFnMut`, `AsyncFnOnce`.

**When to use**:

- Any place you previously wrote `|| async { ... }` or a manual `Future` impl.
- Higher-order async functions (`fn foo<F: AsyncFnMut(i32)>(f: F)`).

**How to use**:

```rust
// Before (1.84 and earlier)
let f = |x: i32| async move { x * 2 };

// After (1.85+)
let f = async |x: i32| x * 2;   // returns impl Future<Output = i32>

// With traits
async fn call_async_fn<F: AsyncFn(i32) -> i32>(f: F, arg: i32) {
    f(arg).await;
}
```

**Best practices**:

- Capture by `move` only when necessary (async closures capture like normal closures).
- Use `AsyncFnMut` for repeated calls, `AsyncFnOnce` for one-shot.
- Combine with `Pin`/`Box` only when you need `dyn AsyncFn`.
- In 2024 edition, lifetime elision is stricter — annotate when returning borrowed data.

**Pitfalls to avoid**:

- Do not mix with `async fn` in the same closure signature without explicit `impl Future`.
- `?` works inside async closures exactly like `async fn`.

#### 1.86.0 – Trait Upcasting + Safe Multi-Element Mutable Indexing

**Key stabilizations**:

- Trait objects can now be upcast to supertraits (`&dyn Sub as &dyn Super`).
- `slice::get_many_mut` / `HashMap::get_many_mut` (and `_unchecked` variants).

**Usage guideline**:

```rust
trait Super {}
trait Sub: Super {}

fn upcast(x: &dyn Sub) -> &dyn Super {
    x as _   // no more transmute or manual vtable
}
```

For indexing:

```rust
let mut v = vec![1, 2, 3, 4];
let [a, b] = v.get_many_mut([0, 2]).unwrap();  // safe, checked
```

**Best practice**: Use `get_many_mut` instead of multiple `&mut` borrows or `split_at_mut`.

#### 1.87.0 – Anonymous Pipes + asm_goto

- `std::io::pipe()` → returns `(Reader, Writer)` pair.
- `asm_goto` for inline assembly that jumps to Rust labels.

**Guideline**:

```rust
let (mut rx, mut tx) = std::io::pipe().unwrap();
std::thread::spawn(move || tx.write_all(b"hello").unwrap());
let mut buf = [0; 5];
rx.read_exact(&mut buf).unwrap();
```

**Best practice**: Prefer `pipe()` over `std::process::Command` for intra-process IPC. Use `asm_goto` only in `#[naked]` or kernel code (see 1.88).

#### 1.88.0 – Naked Functions + let_chains (2024 edition)

**Naked functions** (`#![feature(naked_functions)]` stabilized):

```rust
#[naked]
pub unsafe extern "C" fn my_entry() {
    core::arch::asm!("mov rax, 42; ret", options(noreturn));
}
```

**let_chains** (2024 edition only):

```rust
if let Some(x) = maybe && x > 10 && let Ok(y) = parse(x) {
    // ...
}
```

**Guideline**: Use naked functions for interrupt handlers, boot code, or FFI entry points. Always pair with `options(noreturn)` or explicit `ret`.

#### 1.89.0 – Const Generic Inference (`_`)

```rust
fn take_array<const N: usize>(arr: [u8; N]) {}

take_array([1, 2, 3, 4]);  // N inferred as 4 — no turbofish needed
```

**Best practice**: Replace verbose `::<4>` everywhere in generic-heavy code.

#### 1.90–1.91 – Minor but useful

- 1.91: `pattern` binding drop order is now strictly left-to-right; C variadics stabilized on more ABIs.

#### 1.92.0 – Never-type (`!`) stabilization push

Lints `never_type_fallback_flowing_into_unsafe` and `dependency_on_unit_never_type_fallback` are now **deny-by-default**.

**Action**: Fix any code that relied on `!` falling back to `()` in unsafe contexts. The never type is now a true first-class citizen.

#### 1.93.0 – `slice::as_array`

```rust
let slice: &[u8] = ...;
if let Ok(arr) = slice.as_array::<32>() {  // const-generic
    // arr is [u8; 32]
}
```

**Best practice**: Replace manual `chunks_exact().next().unwrap().try_into().unwrap()` patterns.

#### 1.94.0 (latest) – RISC-V target features + dead_code inheritance

- 29 new RISC-V features (including RVA22/RVA23 profiles).
- `impl` blocks now inherit `#[allow(dead_code)]` from the trait definition.

**Guideline**: If you maintain RISC-V crates, enable the new target features via `#[target_feature]`. For library authors, you can now clean up dead_code annotations on trait impls.

### Recommended Migration Checklist

3. Replace all manual async blocks with `async |...|`.
4. Enable new deny-by-default lints (`clippy::all` + the never-type lints).
5. Add `#![warn(mismatched_lifetime_syntaxes, unused_visibilities)]`.
6. Test with `cargo +1.94 check --all-features`.
7. Update documentation with the new MSRV.

### Quickly Locate Old-Style Code

These one-liners (using **ripgrep** `rg` — install with `cargo install ripgrep` or `apt install ripgrep`) let agents, CI scripts, or humans instantly find legacy patterns that can be upgraded to 1.85–1.94 features.  
Run from repo root. Use `--files-with-matches` to get only filenames for bulk edits.

#### 1. Pre-1.85 manual async closures / blocks (replace with `async |...|`)

```bash
rg --type rust '(\|\s*[^|]+\s*\|\s*async\s*(move)?\s*\{|async\s*(move)?\s*\{[^}]*\})' --context 3
# or list files only:
rg --type rust '(\|\s*[^|]+\s*\|\s*async|async\s*(move)?\s*\{)' --files-with-matches
```

#### 2. Legacy trait-object casts (replace with native upcasting `as _`)

```bash
rg --type rust '(transmute|std::mem::transmute|as\s+&dyn|as\s+dyn)' --context 2
```

#### 3. Multiple mutable borrows (replace with `get_many_mut` / `get_many_mut_unchecked`)

```bash
rg --type rust '&mut\s+\w+[^,]*,\s*&mut' --context 3
# also catch index chains that can become get_many_mut:
rg --type rust '\[\s*\d+\s*,\s*\d+' --type rust
```

#### 4. Manual array / slice conversions (replace with `slice::as_array` or const-generic inference)

```bash
rg --type rust '(\.try_into\(\)|\.chunks_exact\(\)|\.as_slice\(\)\.try_into)' --context 2
```

#### 5. Turbofish const generics that can now be inferred (1.89+)

```bash
rg --type rust '::<\s*[0-9]' --context 1
```

#### 6. Old editions (quick health check)

```bash
# Find crates still on 2018/2021 edition
rg 'edition\s*=\s*"(2018|2021)"' --glob '**/Cargo.toml'
```

#### 7. Naked-function candidates (unsafe extern "C" without #[naked])

```bash
rg --type rust 'unsafe\s+extern\s+"C"\s+fn' --context 2
```

#### 8. Full legacy scan (all patterns above in one command)

```bash
rg --type rust '(async\s*(move)?\s*\{|\|\s*[^|]+\s*\|\s*async|transmute|&mut\s+\w+[^,]*,\s*&mut|\.try_into\(\)|::<[0-9]|unsafe\s+extern\s+"C"\s+fn)' --files-with-matches | xargs -I {} echo "=== {} ===" && cat {}
```

**Agent tips**:

- Pipe to `xargs -I {} sh -c 'echo "=== {} ===" && rg --type rust "TODO|FIXME|async" {}'` for quick review.
- Run in CI: `rg ... --files-with-matches | wc -l` → fail if >0 after migration.
- Use `fd -e rs` instead of `--type rust` if you prefer `fd-find`.
- Combine with `git grep` for git-only repos: `git grep -E 'async move|transmute' -- '*.rs'`

### Example: Full Modern Async Service (1.85–1.94)

```rust
#![edition = "2024"]
use std::io::pipe;

#[tokio::main]
async fn main() {
    let (rx, mut tx) = pipe().unwrap();
    let handler = async |data: Vec<u8>| {
        tx.write_all(&data).await.unwrap();
        Ok::<_, std::io::Error>(())
    };

    // handler is AsyncFnMut
    call_handler(handler, b"hello".to_vec()).await;
}

async fn call_handler<F: AsyncFnMut(Vec<u8>) -> Result<(), std::io::Error>>(
    mut f: F,
    data: Vec<u8>,
) {
    f(data).await.unwrap();
}
```
