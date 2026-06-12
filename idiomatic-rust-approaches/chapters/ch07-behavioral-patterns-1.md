# Behavioral Patterns 1: Taking Action

## Core concepts

- Command pattern maps naturally to closures and trait objects
- Chain of Responsibility works through linked handler traits
- Strategy pattern can use either trait objects or closures for different flexibility levels
- Mediator centralizes coordination between components
- Template Method defines algorithm skeletons with trait defaults

## Frameworks introduced

- **Closures as lightweight strategies** — Instead of defining full trait implementations, use closures for single-method strategies. `Box<dyn Fn(&Input) -> Output>` is often sufficient.
- **Trait default methods for Template Method** — Define required steps as trait methods without defaults, and optional/shared steps with default implementations.

## Key techniques

- **Command pattern**: Store `Box<dyn FnOnce()>` or define a `Command` trait with `execute(&mut self)`. Use a `CommandProcessor` for queuing.
- **Chain of Responsibility**: Each handler implements `handle(&self, request) -> Option<Response>`. Link handlers in a `Vec<Box<dyn Handler>>`.
- **Strategy pattern**: Define a trait, implement variants. Or use `Box<dyn Fn(&[u8]) -> Result<f64>>` for simpler cases.
- **Mediator**: A struct holds references to all components (via `Box<dyn Trait>`) and forwards messages between them.
- **Template Method**: A trait defines a method body calling abstract steps, concrete types implement only the steps.

## Connection to other chapters

Completes the action-oriented patterns. Ch8 finishes behavioral patterns with state-management patterns. Both chapters use the Correct Calculator project.
