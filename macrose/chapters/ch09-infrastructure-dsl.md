# Chapter 9: Infrastructure DSL

## Concept
A function-like macro (`iac!`) that parses a custom DSL to create AWS infrastructure (S3 buckets + Lambda functions) using the AWS SDK for Rust.

## DSL Syntax

```
iac! { bucket uniquename }
iac! { lambda my_name mem 1024 time 15 }
iac! { bucket b => lambda l }  // bucket event triggers lambda
```

## Custom Keywords
```rust
pub(crate) mod kw {
    syn::custom_keyword!(bucket);
    syn::custom_keyword!(lambda);
    syn::custom_keyword!(mem);
    syn::custom_keyword!(time);
}
```
Each becomes a struct implementing `Parse` and works with `peek`/`parse`.

## Parsing Approaches

### Approach 1: Sequential (Chapter usage)
Loop over input, `peek` for keywords, `parse` the corresponding struct:

```rust
impl Parse for IacInput {
    fn parse(input: ParseStream) -> syn::Result<Self> {
        loop {
            if input.peek(kw::bucket) { bucket = Some(input.parse()?); }
            else if input.peek(kw::lambda) { lambda = Some(input.parse()?); }
            else if !input.is_empty() { return Err(/* unknown resource */); }
            else { break; }
        }
        // validate event linking
    }
}
```

### Approach 2: Punctuated + custom struct
Use `parenthesized!` and `Punctuated<KeyValue, Comma>` for key=value syntax:

```
iac! { lambda (name = my_name, mem = 1024, time = 15) }
```

## Combining Declarative + Procedural
Use declarative macros (`macro_rules!`) as a user-friendly wrapper that dispatches to the procedural macro, providing ergonomic syntax for common cases.

## Testing with trybuild
Test compile failures for invalid DSL input:
- Missing names, wrong keywords, invalid numeric ranges
- `trybuild::TestCases::new().compile_fail("tests/fails/*.rs")`
