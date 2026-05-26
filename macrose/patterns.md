# Patterns

## Builder Generation (Ch 3–6, 8)
Generate a builder struct with `setter` methods for each field in the annotated struct. Use `parse_macro_input!` + `quote!` to transform fields into builder methods. Add optional `#[rename]` attribute for custom setter names.

## Compile-time DSL (Ch 5, 9)
Use function-like macros with custom `Parse` implementations to create domain-specific languages. Support both free-form keyword parsing and structured `Punctuated`-based parsing for key=value syntax.

## Attribute-based Customization (Ch 8)
Use derive macro helper attributes to let users customize generated code. Parse `Meta::List` (bare args) or `Meta::NameValue` (key=value) depending on ergonomics. Fall back to sensible defaults when attributes are absent.

## Type State Builder (Ch 8)
Encode required configuration steps as generic type parameters on the builder. `impl` blocks exist only for specific states (e.g., `Builder<HasName>`), making invalid states unrepresentable at compile time.

## Modular Parser Architecture (Ch 9, 10)
Separate parsing (`input.rs`) from code generation (`output.rs`). The parser validates input and produces clean structs; the generator consumes those structs and produces `TokenStream`. Enables independent testing and future backend changes.

## Error-returning Parsers (Ch 7, 9)
Construct `syn::Error` with targeted `Span` information for every user-facing failure. Use `expect("precondition checked")` only internally when the parser has already verified state via `peek`.

## Feature-gated Macro Sets (Ch 10)
Put optional macros behind Cargo features. Use `#[cfg(feature = "...")]` on both the `use` import and the macro entry point. Move feature-specific code to separate modules that are imported only when the feature is active.

## Full-path Generated Output (Ch 10)
Always use fully-qualified paths (`std::collections::HashMap`, `std::vec::Vec`) in generated code. Prevents name collisions with types the user may have defined in their crate.

## Debug-by-write-normal-code (Ch 5, 4, 3)
Before writing macro code, write the expected output as normal Rust to verify it compiles and behaves correctly. Then transliterate into `quote!` blocks. Most effective debugging technique.
