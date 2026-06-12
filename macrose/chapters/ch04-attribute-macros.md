# Chapter 4: Attribute Macros

## Signature

```rust
#[proc_macro_attribute]
pub fn make_public(attr: TokenStream, item: TokenStream) -> TokenStream
```

Unlike derive macros, attribute macros **replace** the annotated item entirely — you must reconstruct everything you want to keep.

## Navigating DeriveInput

```
DeriveInput
├── attrs: Vec<Attribute>
├── vis: Visibility
├── ident: Ident
├── generics: Generics
└── data: Data
    └── Data::Struct(DataStruct)
        └── fields: Fields
            ├── Named(FieldsNamed { named: Punctuated<Field, Comma> })
            ├── Unnamed(FieldsUnnamed { unnamed: Punctuated<Field, Comma> })
            └── Unit
```

## Parsing Fields

```rust
if let Data::Struct(DataStruct { fields: Fields::Named(named), .. }) = &ast.data {
    for field in &named.named {
        let name = field.ident.as_ref().unwrap();
        let ty = &field.ty;
        // generate setter for each field
    }
}
```

## Key Techniques

- **ToTokens trait** — custom structs can implement `ToTokens` to control their generated code
- **Parse trait** — implement `Parse` for custom DSLs within attribute arguments
- **Named vs unnamed fields** — `field.ident` is `Some(Ident)` for named, `None` for tuple structs
- **Reconstructing visibility** — capture `&ast.vis` and reuse it in the generated struct
