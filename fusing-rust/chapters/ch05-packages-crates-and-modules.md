# Packages, Crates, and Modules

## Core concepts

- **Package** = a `Cargo.toml` file + one or more crates. Max one library crate, multiple binary crates.
- **Crate** = a compilation unit. Two kinds: binary crate (produces executable) and library crate (produces `.rlib`).
- **Module** = organizes code within a crate. Declared with `mod`. Private by default; `pub` exposes items.
- **Paths** reference items in the module tree: absolute (`crate::module::item`) or relative (`self::item`, `super::item`).
- **`use`** brings items into scope. Grouped imports: `use crate::cook_food::italian_food::{cook_pizza, cook_pasta}`.

## Frameworks introduced

**Module tree hierarchy** — Source files → Modules → Crates → Package → Workspace. Each level adds organizational scope.

## Key techniques

- Create library crate: `cargo new --lib my-library`
- Create binary crate: `cargo new --bin my-binary` (or omit `--bin`)
- Declare module: `mod chinese_food;` in `lib.rs`
- Public API: `pub fn cook_samosa()`
- Absolute path: `crate::cook_food::indian_food::cook_samosa`
- Relative path: `self::chinese_food::cook_noodles`
- Group imports: `use crate::cook_food::italian_food::{cook_pizza, cook_pasta}`

## Code examples

```rust
// lib.rs — module tree
pub mod cook_food {
    pub mod chinese_food { pub fn cook_noodles() {} }
    pub mod indian_food { pub fn cook_samosa() {} }
    mod italian_food { fn cook_pizza() {} }  // private module
}
// main.rs — consuming a library crate
use my_library_crate::hello_lib_crate;
fn main() { hello_lib_crate(); }
```

## Connection to other chapters

Module system structures all projects beyond "hello world". Used implicitly throughout every subsequent chapter.
