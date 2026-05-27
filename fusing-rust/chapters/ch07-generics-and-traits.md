# Generics and Traits

## Core concepts

- **Generics** parameterize types and functions with `<T>`, reducing code duplication
- **Traits** define shared behavior (like Java interfaces or C++ abstract classes) — can have abstract and concrete methods
- **`impl Trait` syntax** — concise way to accept any type implementing a trait as a parameter
- **Trait bound syntax** — `T: TraitName` constrains generic type parameters
- **`+` syntax** for multiple trait bounds: `T: Trait1 + Trait2`
- Generic types can be used in structs, enums, functions, and methods

## Frameworks introduced

**Generics + Traits = Reusable abstractions** — Generics handle "any type." Traits handle "any type with X behavior." Combined, they enable zero-cost polymorphism: the compiler monomorphizes generic code into concrete implementations.

## Key techniques

- Define generic struct: `struct Circle<T> { cx: T, cy: T, r: T }`
- Generic function with trait bound: `fn area<T: Mul<Output=T>>(a: T, b: T) -> T`
- Define trait: `trait ShapeUtils { fn area(&self) -> f64; fn perimeter(&self) -> f64; }`
- Implement trait: `impl ShapeUtils for Circle<f64> { ... }`
- Default method implementation in trait body (optional override)
- Impl trait syntax: `fn draw(shape: &impl ShapeUtils)`
- Trait bound syntax: `fn draw<T: ShapeUtils>(shape: &T)`
- Multiple bounds: `fn foo<T: ShapeUtils + Display>(t: &T)`

## Code examples

```rust
// Generic struct
struct Circle<T> { cx: T, cy: T, r: T }

// Generic enum
enum Option<T> { Some(T), None }

// Trait definition
trait ShapeUtils {
    fn area(&self) -> f64;
    fn description(&self) -> &str { "A shape" }  // default impl
}

// Trait implementation
impl ShapeUtils for Circle<f64> {
    fn area(&self) -> f64 { 3.14 * self.r * self.r }
}

// Trait as parameter — two equivalent syntaxes
fn draw1(shape: &impl ShapeUtils) {}
fn draw2<T: ShapeUtils>(shape: &T) {}
```

## Connection to other chapters

Generics underpin Rust's standard library (Option, Result, Vec, HashMap). Traits are essential for the Send/Sync system (Ch10) and error handling with From/Into (Ch6).
