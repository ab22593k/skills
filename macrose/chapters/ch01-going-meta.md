# Chapter 1: Going Meta

## What is Metaprogramming?

Code that writes code. Rust's macros are special because they operate at compile time — they transform the AST before type checking and code generation, making the output fully type-safe and as fast as hand-written code.

## Why Rust Macros Are Special

- **Compile-time** — no runtime overhead, errors caught early
- **Safe** — hygienic (tokens know their `Span`), no arbitrary text splicing
- **Expressive** — limited only by what Rust's type system can represent

## Three Procedural Macro Kinds

| Kind          | Attribute                    | Input                                    | Output                         |
| ------------- | ---------------------------- | ---------------------------------------- | ------------------------------ |
| Derive        | `#[proc_macro_derive(Name)]` | `TokenStream` of item                    | `TokenStream` appended to item |
| Attribute     | `#[proc_macro_attribute]`    | (attr `TokenStream`, item `TokenStream`) | `TokenStream` replacing item   |
| Function-like | `#[proc_macro]`              | `TokenStream` of arguments               | `TokenStream` replacing call   |

Plus declarative (`macro_rules!`) for pattern-matching token trees — simpler but less flexible.

## When to Use Macros

- **Boilerplate reduction** — builder pattern, serialization impls
- **Ease of use** — wrap complex APIs behind simple incantations
- **Simulating missing capabilities** — variadic functions, custom DSLs
- **Compile-time computation** — cache derived data

## When NOT to Use Macros

- A function works fine — prefer functions, generics, or `const fn`
- Business logic — macos are harder to debug, profile, and instrument
- IDE support matters — code generation confuses jump-to-definition
- The alternative is clearer — macros can make code mysterious ("magic")
