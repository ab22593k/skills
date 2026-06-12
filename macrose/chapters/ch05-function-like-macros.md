# Chapter 5: Function-like Macros

## Signature

```rust
#[proc_macro]
pub fn my_macro(item: TokenStream) -> TokenStream
```

Invoked as `my_macro!(args...)`. The input `TokenStream` is arbitrary — implement `Parse` for any custom syntax.

## Hiding Information

Use function-like macros to encapsulate implementation details the user shouldn't see:

```rust
getters!(Animal { name: String, age: u8 });
// → generates pub fn name(&self) -> &String and pub fn age(&self) -> &u8
```

## Ident and Span

```rust
use proc_macro2::{Ident, Span};
let method_name = Ident::new(&field_name, Span::call_site());
```

- `Span::call_site()` — tokens appear as if written at the macro call site
- `Span::mixed_site()` — access to both local and call-site namespaces (rare)

## Debugging

**Write the generated code as normal Rust first**, then convert it into macro output. This is the single most effective debugging technique.

## Composing with Custom DSL

```rust
#[proc_macro]
pub fn compose(input: TokenStream) -> TokenStream {
    let ComposeInput { methods } = parse_macro_input!(input);
    // generate a call chain: method1().method2().method3()
}
```

Implement custom `Parse` for `ComposeInput` to parse dot-separated method names — enables mini-DSLs like `compose!(add_one double to_string)`.
