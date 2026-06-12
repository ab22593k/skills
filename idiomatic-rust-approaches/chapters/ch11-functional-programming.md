# Patterns from Functional Programming

## Core concepts

- Function pipelines compose transformations through iterators and combinators
- Generics with trait bounds act like Haskell-style type classes
- Pattern matching handles complex data transformations exhaustively
- Closures serve as first-class architectural components (strategies, filters, callbacks)

## Frameworks introduced

- **Function composition through iterators** — Chained `.iter().map().filter().fold()` calls form a pipeline without intermediate collections (lazy evaluation).
- **Generics as type classes** — `fn process<T: Serialize + Deserialize>(data: T)` constrains types by capability, similar to Haskell's type classes.
- **Closures as architectural components** — Replace single-method traits with `Box<dyn Fn(&Input) -> Output>` for simpler, more flexible APIs.

## Key techniques

- **Pipeline pattern**: `data.iter().map(|x| transform(x)).filter(|x| predicate(x)).collect()`
- **Strategy with closures**: `struct Evaluator { strategy: Box<dyn Fn(&str) -> Result<f64, String>> }`
- **Pattern matching idioms**: Use `if let`, `while let`, and destructuring for control flow. Use `matches!()` macro for boolean checks.
- **Closure capture semantics**: `Fn` (immutable borrow), `FnMut` (mutable borrow), `FnOnce` (consumes). Choose the least restrictive bound.

## Connection to other chapters

Extends the patterns from Ch10 into functional territory. Ch12 completes Part 3 with patterns from Rust's unique core features.
