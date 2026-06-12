# Anti-Pattern: Using Clone and Rc Everywhere

## Core concepts

- Reaching for clone() as a default sidesteps ownership but masks deeper design problems
- Rc<RefCell<T>> reintroduces the very bugs Rust's ownership model prevents
- Smart pointers have legitimate uses but should not be the default
- Simpler designs without reference counting are almost always better

## Frameworks introduced

- **The Clone Hammer** — Using clone() everywhere to avoid ownership issues. It kills performance and hides fundamental design flaws.
- **Ownership matters because of aliasing** — Multiple owners of mutable data is where most concurrency bugs come from. Rust prevents this at compile time.

## Key techniques

- **Restructure to avoid shared ownership** — Instead of Rc<RefCell<T>>, redesign so one owner holds the data and others borrow it.
- **Use references with proper lifetimes** — Pass &T and &mut T instead of cloning. Let the borrow checker verify safety.
- **Use Rc only for genuinely shared read-only data** — When you truly need multiple owners and no mutation, Rc<T> is appropriate.
- **Use RefCell only for interior mutability with single ownership** — RefCell<T> is for when you need mutation through a shared reference, but only one owner exists.

## Connection to other chapters

Extends Ch2's anti-pattern theme with concrete coding mistakes. Ch4 shows the deeper issue: fighting the borrow checker. Ch5-8 show well-structured alternatives.
