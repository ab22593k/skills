---
name: macrose
description: >-
  Master Rust macros — declarative (macro_rules!) and procedural (derive, attribute, function-like) —
  with the mental models, patterns, and techniques from Sam Van Overmeire's book.
  Use when writing, debugging, testing, or publishing Rust macros of any kind.
---

# Write Powerful Rust Macros — Skill Summary

A practical guide to Rust macro development, organized around 10 chapters.

## Core Mental Models

1. **Compile-time code generation** — Macros produce Rust AST at compile time. Everything is type-safe, hygienic via `Span`, and happens before the binary runs.

2. **Three procedural macro kinds** — `#[proc_macro_derive]` (adds methods to a struct/enum/union), `#[proc_macro_attribute]` (replaces the annotated item), `#[proc_macro]` (function-like, arbitrary tokens in → tokens out).

3. **syn + quote division of labor** — `syn` parses incoming `TokenStream` into typed AST nodes; `quote!` generates output `TokenStream` with `#var` interpolation.

4. **Parse, don't validate** — Use `Parse` trait + `parse_macro_input!` to reject malformed input at compile time with precise errors rather than panicking at expansion time.

5. **White-box vs black-box testing** — Unit test macro internals (white-box) from within the macro crate; integration test the generated code (black-box) from a usage crate, often with `trybuild` for compile-failure tests.

6. **Spans and hygiene** — Every token carries a `Span` (source location). `Span::call_site()` pretends tokens come from the macro call site; `Span::mixed_site()` gives access to both local and call-site namespaces.

7. **Full paths in generated code** — Always emit `std::collections::HashMap` not `HashMap` to avoid name collisions and hide implementation details.

8. **Feature gates for optional macros** — Use `[features]` + `#[cfg(feature = "...")]` so users only compile what they use. Default features expose the most common macros.

## Chapter Index

| Chapter | Title                        | Topic                                                            |
| ------- | ---------------------------- | ---------------------------------------------------------------- |
| 1       | Going Meta                   | What macros are, when to use them, tradeoffs                     |
| 2       | Declarative Macros           | `macro_rules!`, metavariables, hygiene, DSLs                     |
| 3       | Hello World Procedural Macro | Project setup, `syn`/`quote`, `cargo expand`                     |
| 4       | Attribute Macros             | `#[proc_macro_attribute]`, navigating `DeriveInput`              |
| 5       | Function-like Macros         | `#[proc_macro]`, information hiding, `Span`                      |
| 6       | Testing a Builder Macro      | Multi-crate workspace, white/black-box tests, `trybuild`         |
| 7       | Error Handling in Macros     | `syn::Error`, `proc_macro_error`, panic-to-Result conversion     |
| 8       | Builder with Attributes      | Custom attributes, type state, rename, sensible defaults         |
| 9       | Infrastructure DSL           | `custom_keyword!`, `Punctuated`, IaC macro combining decl + proc |
| 10      | Macros and the Outside World | Feature flags, docs, full paths, publishing                      |

## Quick Reference

```rust
// Derive macro (Ch 3-6, 8)
#[proc_macro_derive(Builder, attributes(rename))]
pub fn derive_builder(item: TokenStream) -> TokenStream { ... }

// Attribute macro (Ch 4, 10)
#[proc_macro_attribute]
pub fn make_public(attr: TokenStream, item: TokenStream) -> TokenStream { ... }

// Function-like macro (Ch 5, 9, 10)
#[proc_macro]
pub fn config(item: TokenStream) -> TokenStream { ... }

// Custom keywords (Ch 9)
pub(crate) mod kw {
    syn::custom_keyword!(bucket);
}

// Parse trait (Ch 3-5, 9)
impl Parse for MyInput {
    fn parse(input: ParseStream) -> syn::Result<Self> { ... }
}

// Publishable entry point (Ch 10)
// lib.rs exports all #[proc_macro] fns directly
```
