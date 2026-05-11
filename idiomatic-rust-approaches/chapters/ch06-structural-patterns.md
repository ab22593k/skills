# Structural Patterns: Connecting and Aggregating Components

## Core concepts
- Decorator, Adapter, and Proxy map cleanly to trait objects and wrapper types
- Facade is well-served by Rust's module system — a module IS a facade
- Composite works naturally with traits and enums for hierarchical expression trees
- Flyweight is largely handled by Rust's lack of object overhead
- Bridge pattern works well with trait-generic separation

## Frameworks introduced
- **Modules as facades** — Rust's `pub use` re-exports and module hierarchy naturally implement the Facade pattern without wrapper structs.
- **Expression trees with enums** — `enum Expression { Literal(f64), Add(Box<Expression>, Box<Expression>), ... }` naturally implements Composite.

## Key techniques
- **Decorator with trait objects**: Wrap `Box<dyn Expression>` in a struct that implements the same trait, delegating with added behavior.
- **Adapter with wrapper types**: Create a thin struct that implements the target trait and delegates to an inner instance of the adapted type.
- **Composite with Box<dyn Trait>**: Leaf and composite variants share a trait; composite holds `Vec<Box<dyn Component>>`.
- **Bridge with generic trait parameters**: Separate abstraction from implementation using trait bounds on the abstraction side.

## Connection to other chapters
Continues Part 2's re-implementation of classic patterns. Ch7 and Ch8 cover behavioral patterns to complete the Correct Calculator.
