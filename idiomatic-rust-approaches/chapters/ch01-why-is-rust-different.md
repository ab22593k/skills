# Why Is Rust Different?

## Core concepts
- Traditional design patterns from OO languages often don't work in Rust
- "Hitting the wall" — a common experience where Rust suddenly becomes difficult after initial progress
- Learning to "think in Rust" is more important than learning syntax
- New design patterns require a shift in mental models, not just new techniques

## Frameworks introduced
- **The Five Stages of Rust Grief** — Optimism → Frustration → Doubt → Epiphany → Mastery. A framework for understanding the emotional journey of learning Rust.
- **Hitting the Wall** — The phenomenon where developers who feel proficient suddenly face insurmountable compiler errors when tackling complex projects.

## Key techniques
- **Recognize structural vs. local errors**: If fixing one compiler error creates another, the design is fundamentally wrong — not just the code.
- **Move semantics awareness**: Understand that passing a value to a function moves it unless explicitly borrowed. This changes how you design APIs.
- **Parse messages in place without copying**: Use references and slices carefully, understanding that you cannot return a reference to data you also move.

## Connection to other chapters
This chapter sets the foundation for all anti-patterns (Ch2-4) by explaining *why* familiar patterns fail. The Bad Calculator project introduced here is the running example through Part 1.
