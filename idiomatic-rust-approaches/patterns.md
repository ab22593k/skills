## NewType Wrapper

**Type:** technique
**Context:** When you need to distinguish between semantically different values that share the same primitive type (e.g., `UserId` vs `UserName`, both `String`).
**Solution:** Wrap the primitive in a tuple struct with domain-specific methods. Implement `From`, `Deref` (sparingly), and `Display`.
**Consequences:** Zero runtime cost. Type safety at compile time. Slightly more verbose construction.
**Related:** Parse Don't Validate, TypeState

## Parse Don't Validate

**Type:** principle
**Context:** When handling external input (configs, user data, API payloads) that requires validation.
**Solution:** Create types that can only be constructed through validated parsing. Any value of the type is guaranteed valid. Parse at system boundaries, use types everywhere else.
**Consequences:** Eliminates scattered validation checks. Runtime errors are caught early at the boundary. May require custom parsing logic.
**Related:** NewType, Builder pattern

## TypeState

**Type:** technique
**Context:** When an object has a lifecycle with distinct states and operations are only valid in specific states.
**Solution:** Use zero-sized marker types (e.g., `struct Disconnected;`) and a generic struct `Connection<State>`. Implement methods only on specific state variants using `impl Connection<Connected>`.
**Consequences:** Compile-time state machine verification. Zero runtime cost. Complex type signatures.
**Related:** Enum-based state machines (Ch8)

## Sealed Traits

**Type:** technique
**Context:** When you want to limit which types can implement a trait to a controlled set.
**Solution:** Define a `pub(crate)` or private super-trait that your public trait requires. Only types in your crate can implement the super-trait.
**Consequences:** Controlled extensibility. Prevents downstream breakage from trait changes. Slight increase in trait complexity.
**Related:** NewType

## Compiler-Driven Development

**Type:** principle
**Context:** When facing persistent compiler errors that don't seem fixable.
**Solution:** Treat compiler errors as design feedback. If the borrow checker rejects your code, the architecture has a structural flaw. Redesign data ownership rather than working around the error.
**Consequences:** Better architectures. Less fighting with the compiler. Requires willingness to rethink designs.
**Related:** Downward data flow, Ownership as philosophy

## Downward Data Flow

**Type:** architectural pattern
**Context:** When architecting a multi-component system (microservice, pipeline, event processor).
**Solution:** Structure components in layers. Data moves from producers → brokers → consumers. Never create upward references. Mutability is contained at the consumer/boundary level.
**Consequences:** Clean ownership chains the borrow checker can verify. Easier to reason about data flow. Harder to retrofit into existing bidirectional designs.
**Related:** Contained mutability, Modules as interfaces

## Enum-Based State Machine

**Type:** technique
**Context:** When an object needs to change behavior based on internal state and the states are known at compile time.
**Solution:** Define an enum with variant-specific data. Use match exhaustiveness for all state transitions. The compiler verifies all states are handled.
**Consequences:** Compile-time verification of state transitions. No dynamic dispatch overhead. Match arms can be long for complex state machines.
**Related:** TypeState (compile-time alternative), Strategy pattern

## Closures as Strategies

**Type:** technique
**Context:** When you need to swap algorithms at runtime but each algorithm is a single operation.
**Solution:** Use `Box<dyn Fn(&Input) -> Output>` instead of defining a full Strategy trait and implementations. Closures capture relevant context.
**Consequences:** Less boilerplate than trait-based Strategy. Functions cannot be used directly (need closure coercion). More flexible.
**Related:** Strategy pattern, Chain of Responsibility

## Result Composition

**Type:** technique
**Context:** When chaining multiple fallible operations.
**Solution:** Use the `?` operator for early returns, `and_then` for chaining, `map`/`map_err` for transformations, and `collect::<Result<Vec<_>, _>>()` for batch processing.
**Consequences:** Concise error handling. Clear error propagation paths. Can obscure exact error location without context.
**Related:** Sequential fallback, Error collection

## Anti-Pattern: Clone Hammer

**Type:** anti-pattern
**Context:** Making the compiler happy by cloning values instead of borrowing.
**Solution:** Don't default to clone(). Restructure ownership so references work naturally. Use clone() only when the semantics genuinely require owned data.
**Consequences:** Performance degradation. Hides real design problems. Spreads across codebase as a habit.
**Related:** Anti-Pattern: Rc Everywhere

## Anti-Pattern: Rc RefCell Everywhere

**Type:** anti-pattern
**Context:** Wrapping everything in `Rc<RefCell<T>>` to avoid ownership constraints.
**Solution:** Redesign data structures so one clear owner exists. Use `Rc<T>` only for genuinely shared read-only data. Use `RefCell<T>` only for interior mutability with single ownership.
**Consequences:** Reintroduces the bugs Rust's ownership model prevents. Runtime panics from RefCell borrowing violations. Confusing code.
**Related:** Clone hammer, unsafe abuse

## Anti-Pattern: OO Design in Rust

**Type:** anti-pattern
**Context:** Creating deep type hierarchies, using Deref for inheritance, treating traits as base classes.
**Solution:** Accept that Rust is not OO. Use composition, enums for polymorphism, and traits as contracts. Redesign in terms of data flow and ownership.
**Consequences:** Unidiomatic code that fights the language. Compiler errors everywhere. Fragile, hard-to-maintain code.
**Related:** Anti-Pattern: Clone Hammer
