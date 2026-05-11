# Leaning into Rust

## Core concepts
- Use patterns natural to the language rather than force-fitting foreign ones
- Allow the compiler and type system to help you design better software
- The three projects (Bad Calculator, Correct Calculator, Samsa) each taught distinct lessons
- "Thinking in Rust" is the ultimate goal — internalizing Rust's philosophy

## Frameworks introduced
- **Compiler-driven development** — Write code, let the compiler guide corrections. Each error message is design feedback. Over time, you anticipate what the compiler will accept.
- **Ownership as design philosophy** — Ownership isn't just about memory — it's about responsibility for data. Clear ownership chains produce clean architectures.
- **Zero-cost abstractions as mindset** — Abstractions that compile away to efficient machine code. Traits, closures, and iterators cost nothing when not used polymorphically.

## Key techniques
- **Recognize natural patterns**: When a design feels effortless in Rust and the compiler is happy, you're working with the language.
- **Explicitness as a core value**: Rust makes you state your intent clearly (mut, dyn, move, etc.). This produces self-documenting, reviewable code.
- **Safety without paranoia**: Once the compiler accepts your code, memory safety and data-race freedom are guaranteed. Trust the compiler.
- **Composition over inheritance**: Rust makes this natural by design. Favor trait bounds, generics, and composition over type hierarchies.

## Connection to other chapters
Synthesizes all 12 previous chapters into guiding principles. The capstone of the book's narrative arc from frustration to mastery.
