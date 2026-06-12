# Chapter 10: Macros and the Outside World

## Full Paths in Generated Code

Always use full paths (`std::collections::HashMap` not `HashMap`) to:

- Avoid name collisions with user-defined types
- Hide implementation details
- Work without imports in the caller's scope

## Multiple Macros in One Library

A `proc-macro` crate can export any number of macro entry points, but cannot export normal functions, structs, or modules:

```rust
#[proc_macro]
pub fn config(item: TokenStream) -> TokenStream { ... }

#[proc_macro_attribute]
pub fn config_struct(attr: TokenStream, item: TokenStream) -> TokenStream { ... }
```

## Feature Flags

```toml
[features]
default = ["functional"]
struct = []
functional = []
```

```rust
#[cfg(feature = "struct")]
#[proc_macro_attribute]
pub fn config_struct(attr: TokenStream, item: TokenStream) -> TokenStream { ... }
```

Features must be **additive** — never remove existing functionality behind a feature.

## Documentation

````rust
/// Generates a `Config` struct from a YAML file.
///
/// ```rust
/// use config_macro::config;
/// config!();
/// let cfg = Config::new();
/// assert!(cfg.0.contains_key("user"));
/// ```
#[proc_macro]
pub fn config(item: TokenStream) -> TokenStream { ... }
````

- Use `///` for per-macro documentation
- Doctests must be valid — they run under `cargo test`
- Use `#[cfg(any(feature = "struct", doc))]` to document feature-gated items
- `cargo doc --open` generates HTML docs with examples

## Publishing Checklist

- Clean `Cargo.toml` with correct metadata
- `README.md` with quick-start example
- Documentation with runnable doctests
- Feature flags documented
- Compile-failure tests via `trybuild`
- Semantic versioning (breaking changes to macro syntax = major bump)
