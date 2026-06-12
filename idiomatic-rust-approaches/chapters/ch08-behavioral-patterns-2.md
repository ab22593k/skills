# Behavioral Patterns 2: Keeping Track

## Core concepts

- Iterator pattern is built into Rust via the Iterator trait — implement `next()` and get everything else for free
- State pattern maps to enum-based state machines with compile-time exhaustiveness checking
- Memento for undo/redo works naturally with serialization and generics
- Observer benefits from Rust's channels (mpsc) and callback traits
- Visitor enables open-ended operations on closed type hierarchies

## Frameworks introduced

- **Enum-based state machines** — Rust enums with variants carrying state-specific data naturally implement the State pattern. The compiler ensures all transitions are handled via match exhaustiveness.
- **Custom iterators on expression trees** — By implementing the Iterator trait with a stack-based traversal strategy, you can iterate over complex tree structures without exposing internals.

## Key techniques

- **Iterator from scratch**: Implement `Iterator` trait with `type Item` and `next(&mut self) -> Option<Self::Item>`. Consider `DoubleEndedIterator` for bidirectional traversal.
- **State pattern with enums**: `enum CalculatorState { Idle, Inputting { buffer: String }, Computing }`. Match exhaustively to handle transitions.
- **Memento with serde**: Use `#[derive(Serialize, Deserialize)]` on state snapshots. Store in a `Vec<T>` for undo/redo.
- **Observer with channels**: Subject owns a `Vec<Sender<Event>>`. Observers hold `Receiver<Event>` and process on receive.
- **Visitor pattern**: Define a `Visitor` trait with visit methods for each expression type. Implement `accept(&self, visitor: &mut dyn Visitor)` on each type.

## Connection to other chapters

Finishes the Correct Calculator (Part 2). Ch9 transitions to the Samsa microservice project with different architectural concerns.
