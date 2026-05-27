# Ownership and Memory Management

## Core concepts

- **Every value has exactly one owner.** When the owner goes out of scope, `drop` is called automatically.
- **Move** transfers ownership — the original binding is invalidated. Default for heap-allocated types like `String`.
- **Clone** performs a deep copy (stack + heap). Explicit via `.clone()`.
- **Copy** is an implicit bitwise copy for types on the stack (integers, bools, chars, tuples of Copy types).
- **References** (`&T`) borrow without owning. Mutable references (`&mut T`) allow mutation but only one at a time.
- **Slices** (`&[T]` or `&str`) are references to a contiguous sequence of elements.

## Frameworks introduced

**Ownership rules** — 1) Each value has one owner. 2) When owner goes out of scope, value is dropped. These rules eliminate garbage collectors and manual memory management.

**Stack vs Heap** — Stack: LIFO, fast, fixed-size data. Heap: dynamic allocation, slower, requires pointer indirection. Rust decides which to use based on the type.

## Key techniques

- Passing a reference: `fn foo(s: &String)` and call with `foo(&x)`
- Mutable reference: `fn update(s: &mut String)` and call with `update(&mut s)`
- String slicing: `&x[start..end]`, `&x[..7]`, `&x[8..]`, `&x[..]`
- Clone heap data: `let s2 = s1.clone();`

## Code examples

```rust
// Move (String does not implement Copy)
let s1 = String::from("hello");
let s2 = s1;        // s1 is MOVED — can't use s1 after this

// Clone (deep copy)
let s1 = String::from("hello");
let s2 = s1.clone(); // both s1 and s2 are valid

// Borrowing
fn foo(s: &String) { /* s is borrowed */ }
foo(&x);            // x still usable after call

// Mutable reference — only one allowed per scope
let mut s = String::from("hello");
update_string(&mut s);
```

## Connection to other chapters

Ownership is Rust's defining feature. It underpins thread safety (Ch10) and is relaxed only with `unsafe` (Ch16).
