# Unsafe Rust

## Core concepts

- The `unsafe` keyword enables five superpowers the borrow checker cannot verify
- **Raw pointers**: `*const T` (immutable) and `*mut T` (mutable) — bypass ownership rules
- **Unsafe functions/methods** — code that relies on invariants the compiler can't check
- **Mutable static variables** — `static mut COUNTER: i32 = 0` — accessed only in `unsafe` blocks
- **Unsafe traits** — `unsafe trait Send {}` — implemented manually when compiler can't auto-derive
- **Union fields** — accessing a union's field is unsafe because the compiler can't track which variant is active

## Frameworks introduced

**Unsafe abstraction boundary** — Encapsulate unsafe code behind a safe API. The `unsafe` block should be as small as possible. Callers of the safe API don't need `unsafe`.

## Key techniques

- Raw pointer dereference: `let ptr: *mut i32 = &mut num; unsafe { *ptr += 10; };`
- Define unsafe function: `unsafe fn dangerous() {}` — callers need `unsafe { dangerous() }`
- Mutable static: `static mut COUNTER: i32 = 0; unsafe { COUNTER += 1; }`
- Unsafe trait: `unsafe trait Foo { fn method(&self); } unsafe impl Foo for MyType { ... }`
- Union access: `union MyUnion { i: i32, f: f32 } unsafe { let v = u.i; }`

## Code examples

```rust
// Raw pointer dereference
let mut num = 10;
let raw_ptr: *mut i32 = &mut num;
unsafe {
    *raw_ptr += 10;
    println!("*raw_ptr = {}", *raw_ptr);
}

// Mutable static
static mut COUNTER: i32 = 0;
unsafe {
    COUNTER += 1;
    println!("COUNTER = {}", COUNTER);
}

// Union
union IntOrFloat { i: i32, f: f32 }
let mut u = IntOrFloat { i: 42 };
unsafe { println!("int = {}", u.i); }
```

## Connection to other chapters

Unsafe is required for FFI (Ch17) — calling C functions, dereferencing C pointers. Also needed for embedded register manipulation (Ch18) and some WASM bindings (Ch19).
