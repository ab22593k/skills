# Chapter 3: Hello World Procedural Macro

## Project Setup

Two directories in a Cargo workspace:

```
my-macro/
├── macro-impl/        # the proc-macro crate
│   ├── Cargo.toml     # [lib] proc-macro = true, deps: syn, quote
│   └── src/lib.rs
└── macro-usage/       # the user crate
    ├── Cargo.toml     # dep: macro-impl
    └── src/main.rs
```

## Key Dependencies

```toml
[dependencies]
syn = { version = "2.0", features = ["full"] }
quote = "1.0"
proc-macro2 = "1.0"
```

## Minimal Derive Macro

```rust
use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput};

#[proc_macro_derive(HelloMacro)]
pub fn hello_macro(item: TokenStream) -> TokenStream {
    let ast = parse_macro_input!(item as DeriveInput);
    let name = &ast.ident;
    let gen = quote! {
        impl #name {
            fn hello_world() {
                println!("Hello from {}", stringify!(#name));
            }
        }
    };
    gen.into()
}
```

## Code Flow

1. `proc_macro::TokenStream` arrives
2. `parse_macro_input!` parses into `syn::DeriveInput`
3. Logic extracts identifiers, fields, attributes
4. `quote!` generates output `TokenStream` using `#var`
5. `.into()` converts `proc_macro2::TokenStream` → `proc_macro::TokenStream`

## Tooling

- `cargo expand` — shows macro expansion output
- Without `syn`/`quote`: use only `proc_macro::TokenStream` (manual iteration)
- Alternative: `venial` crate for simpler derive-focused parsing
