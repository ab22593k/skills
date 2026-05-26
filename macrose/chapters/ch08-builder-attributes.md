# Chapter 8: Builder with Attributes

## Derive Macro Helper Attributes
Declare by appending to the derive attribute:

```rust
#[proc_macro_derive(Builder, attributes(rename))]
pub fn derive_builder(item: TokenStream) -> TokenStream { ... }
```

These are **inert** — they survive expansion and are only meaningful to the derive macro.

## Parsing Attributes
`syn::Field` has an `attrs: Vec<Attribute>` field. Each `Attribute` has:

- `meta: Meta` — enum of `Path`, `List`, or `NameValue`
- `parse_args()` — parse content inside `#[rename(...)]`
- `require_list()` / `require_path_only()` / `require_name_value()` — typed accessors

```rust
fn get_rename(field: &Field) -> Option<Ident> {
    let attr = field.attrs.iter().find(|a| a.path().is_ident("rename"))?;
    let meta = attr.require_list().ok()?;
    let lit: LitStr = meta.parse_args().ok()?;
    Some(Ident::new(&lit.value(), lit.span()))
}
```

## Type State Pattern
Convert runtime errors to compile-time errors by encoding build steps as generic type parameters:

```rust
struct Builder<T: BuildState> { /* ... */ }
struct HasName;
struct NoName;
impl Builder<NoName> { fn name(self, ...) -> Builder<HasName> { ... } }
impl Builder<HasName> { fn build(self) -> Final { ... } }
```

## Attribute Token Types
- `Meta::List` — `#[rename("value")]` — use `parse_args::<LitStr>()`
- `Meta::NameValue` — `#[rename = "value"]` — match `Meta::NameValue { value: Expr::Lit(ExprLit { lit: Lit::Str(s), .. }), .. }`
- `Meta::Path` — `#[rename]` — no arguments

## Sensible Defaults
Use `unwrap_or_else(|| default_value)` with lazy evaluation for performance — avoids constructing default `TokenStream` objects when every field already has an override.
