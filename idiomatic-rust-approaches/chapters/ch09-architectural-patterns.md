# Architectural Patterns

## Core concepts
- Data flows downward — producers send to brokers, brokers to consumers, never back up
- Mutability stays contained at system boundaries, not shared
- Modules become interfaces via `pub` visibility and re-exports
- Pack lightly — avoid heavy structs, prefer zero-copy views

## Frameworks introduced
- **Samsa architecture** — A publish/subscribe microservice pattern: Producer → Broker → Consumer + Storage. Each layer has specific responsibilities and ownership rules.
- **Downward data flow** — The fundamental architectural principle: data moves in one direction. The borrow checker enforces this naturally.
- **Zero-copy views** — Use `&[u8]` slices or borrowed references rather than owned copies when passing data through intermediary layers.

## Key techniques
- **Producer pattern**: Holds a sender or connection to the broker. Generates data but never receives it from downstream.
- **Broker pattern**: Owns the routing logic. Uses channels to fan out data to consumers. Controls mutation.
- **Consumer pattern**: Owns and isolates state. Only receives data, never sends it upstream.
- **Module-as-interface**: Use `pub mod storage { pub trait Store { ... } }` with re-exports. The module file defines the contract.
- **Lightweight messages**: Design messages as small, owned structs or `Vec<u8>` payloads that can be transferred without shared references.

## Connection to other chapters
Begins Part 3 (Samsa project). Ch10-12 continue with type-system, functional, and core-feature patterns within the Samsa context.
