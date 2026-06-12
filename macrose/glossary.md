# Glossary

| Term                                 | Definition                                                                                                                      |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| **AST**                              | Abstract Syntax Tree — Rust's parsed representation of code. Macros operate on this before type checking.                       |
| **`syn`**                            | Crate for parsing Rust's `TokenStream` into typed AST nodes (`DeriveInput`, `Field`, `Type`, etc.)                              |
| **`quote`**                          | Crate for generating `TokenStream` from Rust code template using `#var` interpolation                                           |
| **`proc_macro2`**                    | A wrapper around `proc_macro` that is `!Send`-free and usable in non-macro contexts (e.g., unit tests)                          |
| **`TokenStream`**                    | An ordered collection of tokens. The input and output type of every procedural macro.                                           |
| **`Span`**                           | Source location information attached to every token. Controls hygiene — which namespaces a token can resolve to.                |
| **Hygiene**                          | The property that identifiers from macro expansion don't accidentally collide with identifiers at the call site.                |
| **`parse_macro_input!`**             | `syn` convenience macro: parse a `TokenStream` into a `Parse`-implementing struct, or return a compile error                    |
| **Derive macro helper attribute**    | An attribute declared via `attributes(...)` in `#[proc_macro_derive(..., attributes(rename))]` that the derive macro recognizes |
| **`custom_keyword!`**                | `syn` macro that creates a keyword type implementing `Parse` and `peek`-able in parser streams                                  |
| **`Punctuated`**                     | `syn` type for comma- or semicolon-separated lists, commonly in field/argument parsing                                          |
| **`parenthesized!`** / **`braced!`** | `syn` macros to extract content from within `(...)` or `{...}` delimiters                                                       |
| **`trybuild`**                       | Crate for compile-failure tests — asserts that certain files produce specific compiler errors                                   |
| **`cargo expand`**                   | Tool to show macro-expanded code. Install via `cargo install cargo-expand`.                                                     |
| **`ToTokens`**                       | Trait that converts a Rust value into `TokenStream`. Implement it for custom structs you want to `quote!`.                      |
| **Inert attribute**                  | An attribute that survives macro expansion and is not consumed — typical for derive macro helper attributes                     |
| **`lookahead1`**                     | `syn` method on `ParseStream` that gives the next token and its span for precise error messages                                 |
| **`proc_macro_error`**               | Crate providing `abort!` for early termination with formatted error output                                                      |
| **Feature flag**                     | Cargo mechanism (`[features]` in `Cargo.toml`) for optional compilation of parts of a crate                                     |
