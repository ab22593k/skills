**Abstract Factory** — A creational pattern that provides an interface for creating families of related objects. In Rust, rarely needed — prefer generics or closures. (Ch5)

**Adapter** — Wraps an existing interface into one expected by clients. Implement with a thin struct that delegates. (Ch6)

**Associated types** — Trait type aliases (`type Output;`) that let implementations decide concrete types at compile time. (Ch5)

**Bad Calculator** — A deliberately broken calculator project demonstrating anti-patterns throughout Part 1 (Ch1-4).

**Borrow checker** — Rust's compile-time analyzer ensuring references never outlive their data and exclusive mutable access. (Ch4)

**Bridge** — Separates abstraction from implementation so both can vary independently. Use generic trait parameters. (Ch6)

**Broker** — A component in the Samsa architecture that routes data from producers to consumers. Controls mutation. (Ch9)

**Builder** — A creational pattern using step-by-step construction with method chaining and validation. Natural in Rust. (Ch5)

**Chain of Responsibility** — Passes requests along a chain of handlers until one processes it. Use a `Vec<Box<dyn Handler>>`. (Ch7)

**Clone hammer** — The anti-pattern of using clone() everywhere to avoid ownership issues. (Ch3)

**Command** — Encapsulates an operation as an object with an execute method. Use trait objects or closures. (Ch7)

**Compiler-driven development** — Writing code and letting compiler errors guide design improvements. (Ch4, Ch13)

**Composite** — Treats individual objects and compositions uniformly. Implement with enum variants holding Box<dyn Component>. (Ch6)

**Consumer** — In Samsa, the component that owns and processes data. Only receives, never sends upstream. (Ch9)

**Correct Calculator** — The second project (Ch5-8) implementing GoF patterns idiomatically in Rust.

**Decorator** — Wraps an object to add behavior at runtime. Use trait objects with wrapper structs. (Ch6)

**Deref (misuse)** — Using Deref to simulate inheritance. Anti-pattern — Deref is for smart pointers only. (Ch2)

**Downward data flow** — Architectural principle: data moves in one direction (downstream) without upward references. (Ch9)

**Drop** — Rust's RAII destructor trait. Runs automatically when a value goes out of scope. (Ch12)

**Enum-based state machines** — Using enums with variant-specific data to implement the State pattern with compile-time exhaustiveness. (Ch8)

**Facade** — Provides a unified interface to a subsystem. Rust modules naturally serve as facades. (Ch6)

**Factory Method** — Defines an interface for creating objects, letting subclasses decide the type. Use associated types in Rust. (Ch5)

**Five stages of Rust grief** — Optimism → Frustration → Doubt → Epiphany → Mastery. (Ch1)

**Flyweight** — Shares fine-grained objects for efficiency. Largely handled by Rust's lack of object overhead. (Ch6)

**Hitting the wall** — The sudden difficulty spike when moving from basic to advanced Rust projects. (Ch1)

**Interior mutability** — Mutation through a shared reference via Cell, RefCell, or Mutex. Use when mutation is needed but ownership is shared. (Ch3, Ch4)

**Iterator** — Implements sequential traversal over a collection. In Rust, implement the Iterator trait. (Ch8)

**Mediator** — Centralizes communication between components to reduce coupling. (Ch7)

**Memento** — Captures and externalizes an object's state for later restoration. Use serde for serialization. (Ch8)

**NewType** — A zero-cost wrapper around a primitive that adds semantic meaning and type safety. (Ch10)

**Observer** — Notifies interested parties when state changes. Use channels (mpsc) or callback traits. (Ch8)

**Parse, don't validate** — Create types that make invalid states unrepresentable rather than validating raw values at runtime. (Ch10)

**Producer** — In Samsa, generates data and sends it to the broker. Never receives data from downstream. (Ch9)

**Prototype** — Creates new objects by cloning an existing instance. In Rust, use `#[derive(Clone)]`. (Ch5)

**Proxy** — Provides a surrogate for another object. Largely handled by Rust's smart pointers (Box, Rc). (Ch6)

**RAII** — Resource Acquisition Is Initialization. Resources are acquired during construction and released via Drop. (Ch12)

**Samsa** — The third project (Ch9-12): a publish/subscribe microservice demonstrating Rust-native architectural patterns.

**Sealed traits** — Traits that can only be implemented within the defining crate, using a private super-trait bound. (Ch10)

**Singleton** — Ensures a class has only one instance. In Rust, use module-level constants or once_cell. (Ch5)

**State pattern** — Allows an object to change behavior when its internal state changes. Use enum-based state machines. (Ch8)

**Strategy** — Enables selecting an algorithm at runtime. Use trait objects or closures. (Ch7)

**Template Method** — Defines the skeleton of an algorithm in a trait method with overridable steps. (Ch7)

**TypeState** — Encodes state transitions in the type system so the compiler rejects invalid state changes. (Ch10)

**Visitor** — Represents an operation to be performed on elements of an object structure. Use a Visitor trait with accept methods. (Ch8)

**Zero-copy views** — Using borrowed slices (`&[u8]`) instead of owned data when passing through intermediary layers. (Ch9)
