# Chapter 6: Testing a Builder Macro

## Multi-crate Workspace

```
builder-workspace/
├── builder-macro/       # proc-macro crate
├── builder-code/        # helper types (optional)
└── builder-usage/       # test + example crate
```

## Testing Strategy

### White-box Tests (in `builder-macro/`)

Test parsing logic, edge cases, intermediate data structures directly:

```rust
#[test]
fn test_parses_simple_struct() {
    let input: DeriveInput = parse_quote! {
        struct Foo { x: i32 }
    };
    let result = generate_builder(input);
    assert!(result.to_string().contains("fn x"));
}
```

### Black-box Tests (in `builder-usage/`)

Test the generated code compiles and behaves correctly:

```rust
#[test]
fn test_builder_creates_struct() {
    #[derive(Builder)]
    struct Person { name: String }
    let p = Person::builder().name("Al".into()).build();
    assert_eq!(p.name, "Al");
}
```

### Compile-failure Tests (with `trybuild`)

Test that invalid inputs produce the expected compilation errors:

```rust
#[test]
fn ui_tests() {
    let t = trybuild::TestCases::new();
    t.compile_fail("tests/fails/*.rs");
}
```

## Common Errors

- **Expected identifier** — forgetting to convert `LitStr` to `Ident`, or using wrong `Ident` type (`proc_macro` vs `proc_macro2`)
- **proc-macro crate types not exported** — proc-macro crates can only export `#[proc_macro]` items
- **`From`/`ToTokens` not available** — types from the proc_macro crate are only convertible to/from `TokenStream`
