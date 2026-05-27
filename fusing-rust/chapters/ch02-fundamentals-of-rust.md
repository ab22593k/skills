# Fundamentals of Rust Programming Language

## Core concepts

- Variables are **immutable by default** — use `mut` to make them mutable
- Rust is **statically typed** with type inference; annotate with `: Type` when inference is ambiguous
- Integer types: `i8`-`i128` (signed), `u8`-`u128` (unsigned), `isize`/`usize` (architecture-dependent)
- Floating-point: `f32` (single-precision) and `f64` (double-precision, default)
- Compound types: **tuples** (fixed-length, heterogeneous) and **arrays** (fixed-length, homogeneous)
- Functions: declared with `fn`, return type after `->`, last expression is the return value (no `;`)
- Control flow: `if`/`else`/`else if`, `loop` (infinite + break), `while`, `for` with iterators

## Frameworks introduced

**Statement vs Expression distinction** — Statements perform actions (end with `;`). Expressions produce values (no `;`). The last expression in a function body is automatically returned.

## Key techniques

- Type annotation: `let x: u8 = "2".parse().unwrap();`
- Mutable binding: `let mut x = 2; x = 3;`
- Returning from `loop`: `let result = loop { break value; };`
- `for` over collections: `for val in values.iter()`

## Code examples

```rust
// Variables and mutability
let x = 2;          // immutable
let mut y = 3;      // mutable
y = 4;

// Function returning value
fn sum(x: i16, y: i16) -> i16 {
    x + y           // no semicolon = expression = return value
}

// Loop with return value
let result = loop {
    a -= 1;
    if a == 2 { break 2 * a; }
};
```

## Connection to other chapters

Foundation for Ch3 (ownership builds on mutability rules) and Ch7 (generics build on type system).
