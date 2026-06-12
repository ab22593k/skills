# Chapter 2: Declarative Macros

## Syntax

`macro_rules! name { ($matcher) => {$transcriber}; }`

Matchers define capture groups (`$name:type`), transcribers emit the matched code with `$name` substitution.

## Metavariable Types

| Fragment   | Matches           | Example                     |
| ---------- | ----------------- | --------------------------- |
| `expr`     | Expressions       | `x + 1`                     |
| `ident`    | Identifiers       | `foo`                       |
| `ty`       | Types             | `Vec<u8>`                   |
| `tt`       | Token trees       | `{ ... }`, `[...]`          |
| `block`    | Block expressions | `{ stmts; }`                |
| `stmt`     | Statements        | `let x = 1;`                |
| `pat`      | Patterns          | `Some(x)`                   |
| `path`     | Paths             | `std::collections::HashMap` |
| `meta`     | Attributes        | `#[inline]`                 |
| `literal`  | Literals          | `42`, `"hi"`                |
| `lifetime` | Lifetimes         | `'a`                        |

## Common Patterns

- **Varargs/default args** — `$(, $arg:expr)*` for flexible interfaces
- **DSLs** — small domain languages with hygienic expansion
- **Newtype wrappers** — generate `Deref`, `From`, etc.
- **Composing/inlining functions** — avoid closure indirection

## Hygiene

Declarative macros are **partially hygienic** — identifiers declared within are unique, but items (structs, fns) are visible in the calling scope. `$crate` ensures paths resolve to the macro's crate.
