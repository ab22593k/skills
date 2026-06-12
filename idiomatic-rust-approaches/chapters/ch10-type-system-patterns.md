# Patterns That Leverage the Type System

## Core concepts

- NewType wrappers add semantic meaning and type safety at zero runtime cost
- "Parse, don't validate" encodes data validity in types, eliminating runtime checks
- TypeState makes illegal state transitions impossible at compile time
- Sealed Traits restrict implementation to controlled sets of types

## Frameworks introduced

- **NewType pattern** — Wrap a primitive in a tuple struct (`struct UserId(String)`) to prevent mixing up semantically different values and add domain-specific methods.
- **Parse, Don't Validate** — Create types that enforce invariants at construction. A `ParsedConfig` type can only be created by parsing raw input, so any value of that type is guaranteed valid.
- **TypeState** — Use zero-sized marker types and generic structs to encode state transitions. The compiler rejects invalid state changes at compile time.
- **Sealed Traits** — Place a private super-trait that only crate-local types can implement, restricting trait extension to controlled types.

## Key techniques

- **NewType**: `struct Email(#[serde(with = "...")] String);` — wrap and implement `From`, `Deref`, and domain methods.
- **Parse don't validate builder**: Builder `ConfigBuilder` collects raw values, `build() -> Result<ParsedConfig>` validates all at once.
- **TypeState generic markers**: `struct Connection<State>(TcpStream, PhantomData<State>)` with methods gated on `Disconnected`, `Connected`, `Authenticated`.
- **Sealed trait**: Define a `pub trait Sealed {}` that is not re-exported. Your public trait has a super-trait bound on `Sealed`. Only crate-local types can implement it.

## Connection to other chapters

Deepens Ch9's architectural patterns with type-level safety. Ch11 continues with functional programming patterns.
