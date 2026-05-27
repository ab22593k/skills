---
name: idiomatic-rust-approaches
description: "Apply Rust-specific design patterns, avoid anti-patterns, and build architectures that work with ownership, borrowing, and the type system rather than against them."
---

## Core mental models

### Thinking in Rust (not in Java/C++/Python)

**When to use:** Whenever you start a new Rust project or feel frustrated fighting the compiler.

**The idea:** Rust looks familiar (structs ≈ classes, traits ≈ interfaces) but is fundamentally different. The borrow checker, ownership model, and lack of inheritance mean traditional OO patterns lead to dead ends. Success requires unlearning habits from other languages and adopting Rust-native thinking.

**How to apply:** When the compiler rejects your design, step back and ask whether you're trying to express an OO pattern that doesn't fit. Redesign data flow so that ownership is clear and mutation is contained.

**Pitfalls:** Treating structs as classes and traits as interfaces leads to brittle code held together with clone() and Rc<RefCell<T>>.

### Ownership as a design philosophy

**When to use:** When architecting data structures, data flow, and module boundaries.

**The idea:** Ownership isn't just a compiler rule — it's a design tool. Data should have one clear owner at any time. Structure your system so that ownership flows naturally downward (from producers to brokers to consumers), and mutability stays at the edges, isolated from shared data paths.

**How to apply:** Design data flows downward. Producers send immutable data to brokers, brokers coordinate, consumers own and isolate state. Modules become interface boundaries.

**Pitfalls:** Fighting ownership with clone() everywhere masks design problems and destroys performance guarantees.

### The borrow checker as design consultant

**When to use:** When the compiler rejects code that seems correct in other languages.

**The idea:** The borrow checker isn't your enemy — it's catching real bugs (data races, dangling pointers, use-after-free) at compile time. When it rejects your code, the design likely has a fundamental flaw. Listen to its feedback and restructure rather than work around it.

**How to apply:** Instead of reaching for unsafe, Rc<RefCell<T>>, or lifetime gymnastics, redesign the data ownership structure. Split types, invert control, or use patterns like interior mutability properly.

**Pitfalls:** unsafe is almost never the answer. It shifts safety guarantees from the compiler to the programmer and can introduce UB even with experienced Rust developers.

### Parse, don't validate

**When to use:** When handling user input, configuration, or any external data that needs validation.

**The idea:** Instead of validating raw data and passing it around as untyped strings/numbers, create types that make invalid states unrepresentable. Parse data into these types at the boundary of your system, then use them throughout.

**How to apply:** Use the NewType pattern and builder methods that return Result to guarantee data validity. Once parsed, the type system ensures correctness without runtime checks.

**Pitfalls:** Scattered validation throughout the codebase creates duplication and means some code paths may skip validation entirely.

### TypeState: illegal states unrepresentable

**When to use:** When objects have distinct lifecycle phases where certain operations are only valid in certain states.

**The idea:** Encode state transitions in the type system itself using zero-sized marker types and generic structs. The compiler rejects invalid state transitions at compile time, eliminating runtime state-checking errors.

**How to apply:** Define empty marker types for each state (e.g., `struct Disconnected; struct Connected; struct Authenticated;`), then use a generic struct `Client<State>` with methods only available on specific state types.

**Pitfalls:** Over-application leads to complex type signatures. Reserve for state machines where correctness is critical.

### Composition over inheritance, naturally

**When to use:** When designing type hierarchies and behavior sharing.

**The idea:** Rust doesn't support inheritance, and that's a feature. Use traits as contracts, not as base classes. Compose behavior through trait bounds, associated types, and generic functions rather than deep type hierarchies.

**How to apply:** Prefer enum-based polymorphism for fixed variants, trait objects (Box<dyn Trait>) for open sets, and generics with trait bounds for compile-time dispatch. Use struct composition (one struct holds another) over trying to fake inheritance.

**Pitfalls:** Misusing Deref to simulate inheritance creates confusing semantics and bypasses Rust's intended encapsulation.

### Data flows downward, mutability stays contained

**When to use:** When designing system architecture, especially microservices or multi-component systems.

**The idea:** In a well-structured Rust system, data moves in one direction (downstream). Producers create data, brokers route it, consumers process it. Mutability is isolated at the consumer or local level, not shared. This creates clean ownership chains that the borrow checker can verify.

**How to apply:** Design modules as layers: top layer sends data down, middle layer routes, bottom layer owns and processes. Messages are immutable. Mutations happen only within consumers that own their data.

**Pitfalls:** Bidirectional data flow creates ownership cycles and fighting with the borrow checker.

## How to use this skill

Load this skill when working on Rust projects to access patterns for idiomatic Rust design. The chapter files contain detailed explorations of specific topics:

```
# Load the skill when you start a Rust project
# Then ask questions like:
# "What creational pattern should I use here?"
# "Show me how to implement the State pattern in Rust"
# "How do I avoid fighting the borrow checker?"
```

## Chapter index

| #   | Title                                          | Topic                                                                  | Tokens |
| --- | ---------------------------------------------- | ---------------------------------------------------------------------- | ------ |
| 1   | Why Is Rust Different?                         | The need for new patterns, hitting the wall, Rust learning curve       | ~1K    |
| 2   | Anti-Pattern: Designing for Object Orientation | Why structs ≠ classes, misusing traits/Deref/generics/enums            | ~1K    |
| 3   | Anti-Pattern: Using Clone and Rc Everywhere    | Ownership avoidance, cloning, Rc/RefCell misuse                        | ~1K    |
| 4   | Don't Fight the Borrow Checker                 | unsafe abuse, mutable statics, lifetime gymnastics                     | ~1K    |
| 5   | Creational Patterns: Making Things             | Factory Method, Abstract Factory, Builder, Singleton, Prototype        | ~1K    |
| 6   | Structural Patterns                            | Proxy, Decorator, Adapter, Facade, Composite, Flyweight, Bridge        | ~1K    |
| 7   | Behavioral Patterns 1: Taking Action           | Command, Chain of Responsibility, Strategy, Mediator, Template Method  | ~1K    |
| 8   | Behavioral Patterns 2: Keeping Track           | Iterator, State, Memento, Observer, Visitor                            | ~1K    |
| 9   | Architectural Patterns                         | Data flows downward, mutability contained, modules as interfaces       | ~1K    |
| 10  | Patterns That Leverage the Type System         | NewType, Parse Don't Validate, TypeState, Sealed Traits                | ~1K    |
| 11  | Patterns from Functional Programming           | Pipelines, generics as type classes, pattern matching, closures        | ~1K    |
| 12  | Patterns Emerging from Rust's Core Features    | Result/Option composition, block expressions, RAII, Drop               | ~1K    |
| 13  | Leaning into Rust                              | Compiler-driven development, ownership as philosophy, thinking in Rust | ~1K    |

## Reference files

- **glossary.md** — All key terms alphabetized with chapter references
- **patterns.md** — Techniques, algorithms, and architectural patterns with context/solution/consequences
- **cheatsheet.md** — Decision tables and quick-reference for picking the right pattern
