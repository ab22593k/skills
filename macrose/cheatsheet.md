# Cheatsheet

## Cargo.toml Setup

```toml
[lib]
proc-macro = true

[dependencies]
syn = { version = "2.0", features = ["full", "extra-traits"] }
quote = "1.0"
proc-macro2 = "1.0"
# Optional
proc-macro-error = "1"
serde = "1"
serde_yaml = "0.9"

[dev-dependencies]
trybuild = "1.0"
```

## Macro Entry Points

```rust
// Derive
#[proc_macro_derive(MyTrait, attributes(custom))]
pub fn derive_my(item: TokenStream) -> TokenStream { ... }

// Attribute
#[proc_macro_attribute]
pub fn attr_my(attr: TokenStream, item: TokenStream) -> TokenStream { ... }

// Function-like
#[proc_macro]
pub fn my_fn(item: TokenStream) -> TokenStream { ... }
```

## Common Parse Patterns

```rust
use syn::{parse_macro_input, DeriveInput, Field, Type, Ident, LitStr, Token};
use syn::punctuated::Punctuated;
use syn::token::Comma;
use quote::quote;

// Parse DeriveInput
let ast = parse_macro_input!(item as DeriveInput);

// Iterate fields
if let syn::Data::Struct(data) = &ast.data {
    if let syn::Fields::Named(fields) = &data.fields {
        for field in &fields.named { /* ... */ }
    }
}

// Custom keyword
mod kw { syn::custom_keyword!(my_keyword); }
```

## Common Conversions

| From              | To                | Method                                                       |
| ----------------- | ----------------- | ------------------------------------------------------------ |
| `String`          | `Ident`           | `Ident::new(&s, Span::call_site())`                          |
| `&str`            | `LitStr`          | `LitStr::new(s, Span::call_site())`                          |
| `u16`             | `LitInt`          | `LitInt::new(&s, LitIntType::Unsuffixed, Span::call_site())` |
| `proc_macro2::TS` | `proc_macro::TS`  | `.into()`                                                    |
| `proc_macro::TS`  | `proc_macro2::TS` | `.into()`                                                    |

## Testing

```rust
// White-box
let input: DeriveInput = syn::parse_quote! { struct Foo { x: i32 } };
let result = generate(input);
assert!(result.to_string().contains("fn x"));

// Black-box (usage crate)
#[test]
fn builds_struct() { #[derive(Builder)] struct S { x: i32 }; S::builder().x(1).build(); }

// Compile-failure
#[test] fn ui() { trybuild::TestCases::new().compile_fail("tests/fails/*.rs"); }
```
