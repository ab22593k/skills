# Don't Fight the Borrow Checker

## Core concepts
- The borrow checker is a design consultant, not an adversary
- unsafe is almost never the right answer for ownership/lifetime issues
- Mutable statics and globals create problems worse than the ones they solve
- Lifetime annotation gymnastics indicate design-level problems

## Frameworks introduced
- **Compiler-driven development** — Treating compiler errors as design feedback rather than obstacles. When the borrow checker rejects code, the design has a structural flaw.
- **Redesign, don't work around** — If you can't make ownership work, change the data architecture rather than fighting the compiler.

## Key techniques
- **Split types to clarify ownership** — If one struct holds data and references to it, split into separate structs with clear ownership.
- **Use arenas or pools for cyclic references** — Instead of Rc cycles, use a central store and index-based references.
- **Contain unsafe in small, verified boundaries** — If unsafe is necessary, isolate it behind safe abstractions with thorough safety comments.
- **Use interior mutability correctly** — Cell<T> for Copy types, RefCell<T> for checked borrowing, Mutex<T> for threads.

## Connection to other chapters
Directly follows from the anti-patterns in Ch2-3. The "don't fight the compiler" principle becomes the positive foundation for Ch5-8's correct patterns.
