## Choosing a creational pattern

| If                                    | Then                                           |
| ------------------------------------- | ---------------------------------------------- |
| Creating objects with varying types   | Factory Method with associated types           |
| Creating families of related objects  | Abstract Factory (rarely needed); use generics |
| Complex construction with validation  | Builder pattern                                |
| Exactly one instance needed           | Module constant or `once_cell::sync::Lazy`     |
| Creating copies of an existing object | `#[derive(Clone)]` + `.clone()`                |

## Choosing a structural pattern

| If                                        | Then                           |
| ----------------------------------------- | ------------------------------ |
| Wrapping an external interface            | Adapter                        |
| Adding behavior to existing objects       | Decorator via trait objects    |
| Simplifying a complex subsystem           | Facade (use module re-exports) |
| Treating individuals and groups uniformly | Composite via enum variants    |
| Multiple independent variation axes       | Bridge pattern                 |

## Choosing a behavioral pattern

| If                                                  | Then                                 |
| --------------------------------------------------- | ------------------------------------ |
| Queue or log operations for undo                    | Command pattern                      |
| Route requests through processing stages            | Chain of Responsibility              |
| Swap algorithms at runtime                          | Strategy (trait objects or closures) |
| Coordinate multiple components                      | Mediator                             |
| Define an algorithm skeleton with overridable steps | Template Method                      |
| Traverse a collection without exposing internals    | Iterator trait                       |
| Change behavior based on state                      | State (enum-based)                   |
| Save/restore state snapshots                        | Memento (serde)                      |
| React to events from another component              | Observer (channels)                  |
| Add operations to a closed type hierarchy           | Visitor                              |

## Choosing an architectural approach

| If                                            | Then                                             |
| --------------------------------------------- | ------------------------------------------------ |
| Data enters the system and needs routing      | Downward data flow with Producer/Broker/Consumer |
| Mutability needed across component boundaries | Isolate mutation inside Consumer                 |
| Encapsulating subsystem internals             | Module-as-interface pattern                      |
| Avoiding large data copies between layers     | Zero-copy views (`&[u8]`)                        |

## Type system patterns quick reference

| Pattern              | Problem                            | Solution                               | Cost                       |
| -------------------- | ---------------------------------- | -------------------------------------- | -------------------------- |
| NewType              | Confusing primitive types          | Tuple struct wrapper                   | Zero                       |
| Parse don't validate | Runtime validation errors          | Types that guarantee validity          | Slight parsing boilerplate |
| TypeState            | Invalid runtime state transitions  | Compile-time state machine via markers | Zero                       |
| Sealed traits        | Uncontrolled trait implementations | Private super-trait                    | Slight trait complexity    |

## Quick rules

- When the compiler fights you, the design is wrong — not the code
- `unsafe` is not a workaround for ownership problems
- `Rc<RefCell<T>>` reintroduces the bugs Rust prevents
- Implement `Iterator` → get dozens of methods for free
- Enums + match = compile-time state machine correctness
- `?` operator chains fallible operations without nesting
- Modules ARE facades — use `pub use` to control API surface
- Closures can replace single-method trait implementations
- Zero-cost abstractions mean abstractions compile away
- Trust the compiler for safety guarantees
