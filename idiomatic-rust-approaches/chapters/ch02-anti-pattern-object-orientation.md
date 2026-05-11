# Anti-Pattern: Designing for Object Orientation

## Core concepts
- Rust is not an OO language — structs are not classes, traits are not interfaces
- Trying to simulate inheritance leads to unidiomatic, brittle code
- The borrow checker prevents the free movement of objects foundational to OO design
- Enums are sometimes the right tool for polymorphism in Rust, but overusing them is also a trap

## Frameworks introduced
- **Structs as data, not behavior** — Unlike classes, structs are plain data aggregates. Methods are attached via impl blocks but don't define the type's identity.
- **Traits as contracts, not base classes** — Traits define what a type can do, not what it is. Trait inheritance is contract composition, not hierarchical extension.

## Key techniques
- **Use enums for fixed-variant polymorphism** — When the set of variants is known, enums are more natural than trait objects.
- **Use Box<dyn Trait> for open polymorphism** — When callers need to extend behaviors, trait objects on the heap provide runtime dispatch without class hierarchies.
- **Never use Deref to simulate inheritance** — Deref is for smart pointer types, not subclassing. It creates confusing semantics.
- **Avoid generic-heavy class-like wrappers** — Generics are for compile-time polymorphism, not for emulating class hierarchies.

## Connection to other chapters
Builds on Ch1's insight that Rust needs different patterns. Ch3 and Ch4 continue the anti-pattern theme. Ch5-8 show the correct way to implement traditional GoF patterns in Rust.
