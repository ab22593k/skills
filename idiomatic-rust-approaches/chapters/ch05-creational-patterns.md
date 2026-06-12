# Creational Patterns: Making Things

## Core concepts

- Factory Method works cleanly with associated types and Result returns
- Abstract Factory is rarely needed in Rust — use generics or closures instead
- Builder is natural in Rust thanks to method chaining and consuming builders
- Singleton is mostly unnecessary — use module-level constants or lazy_static
- Prototype is trivial with Clone

## Frameworks introduced

- **Associated types for factories** — Traits define factory output via `type Output;`, letting implementations decide the concrete type at compile time.
- **Consuming builders** — Builder methods consume and return self (not &mut self) for compile-time guarantees about completeness.

## Key techniques

- **Factory Method with traits**: Define a `Factory` trait with `type Output` and a `create()` method returning `Result<Self::Output>`.
- **Builder pattern**: Use builder methods returning `Self` (consuming) or `&mut Self` (non-consuming). Add a `build()` → `Result<T>` for validation.
- **Singleton in Rust**: Use `once_cell::sync::Lazy<T>` or `std::sync::OnceLock<T>` for global state. Better: just use module-level constants.
- **Prototype**: `#[derive(Clone)]` and call `.clone()`. The built-in `Clone` trait is the Prototype pattern.

## Connection to other chapters

First chapter of Part 2, transitioning from anti-patterns to correct implementations. Ch6 continues with structural patterns.
