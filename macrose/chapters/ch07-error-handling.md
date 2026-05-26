# Chapter 7: Error Handling in Macros

## Principles

| Property | Pure Function | Impure Function |
|----------|--------------|-----------------|
| Returns | `Result<T, syn::Error>` | `syn::Result<T>` (alias) |
| Mutable input | No | Sometimes (ParseStream) |
| Panics | Never | Avoid if possible |

## Converting Panics to Results

```rust
// BAD: panics on bad input
fn parse_field(input: ParseStream) -> Field { ... }

// GOOD: returns Result with span info
fn parse_field(input: ParseStream) -> syn::Result<Field> { ... }
```

## Using `syn::Error`
```rust
return Err(syn::Error::new(
    field.span(),
    "expected a string literal for rename attribute"
));
```

## The `proc_macro_error` Crate
Adds `abort!` / `abort_call_site!` macros for non-recoverable errors with beautiful formatting:

```rust
use proc_macro_error::{proc_macro_error, abort};

#[proc_macro_error]
#[proc_macro_derive(MyMacro)]
pub fn derive(item: TokenStream) -> TokenStream { ... }

fn some_helper() {
    abort!(span, "unexpected input: expected identifier");
}
```

## When to Panic vs Return Error
- **Panic** — when something is logically impossible at the call site (e.g., `parse()` after `peek()` succeeded)
- **Return `syn::Error`** — for user-facing validation failures with span information
- **`abort!`** — when you want proc_macro_error's nice formatting and immediate termination
