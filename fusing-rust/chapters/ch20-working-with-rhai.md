# Working with Rhai: An Embedded Scripting for Rust

## Core concepts

- **Rhai** is a fast, embedded scripting language for Rust — syntax is a subset of JavaScript
- Dynamic typing with type inference. Supports integers, floats, bools, strings, arrays, maps
- Variables are immutable by default (`mut` for mutable), lexically scoped with shadowing
- All standard operators: arithmetic, assignment, comparison, logical, bitwise
- Control flow: `if`/`else if`/`else`, `for`, `while`, `loop`, `break`, `continue`
- Functions: `fn add(a, b) { return a + b; }` — positional and named arguments
- **Engine API**: `Engine::new()` to create, `engine.eval::<T>("code")` to execute
- **Bidirectional calls**: Rust ↔ Rhai via `register_fn`, `call_fn`

## Frameworks introduced

**Dynamic extensibility via scripting** — Embed Rhai in a Rust application to let users extend behavior without recompiling. Define a kernel of Rust functions, register them with the engine, and let Rhai scripts orchestrate them.

## Key techniques

- Execute expression: `engine.eval::<i64>("40 + 2")?`
- Pass variables: `scope.push("x", 42); engine.eval_with_scope::<i64>(&scope, "x * 2")?;`
- Load script file: `engine.eval_file::<()>("script.rhai".into())?`
- Register Rust function: `engine.register_fn("add", add_fn);`
- Call Rhai from Rust: `engine.call_fn::<i64>("square", &scope, (5,))?`
- Rust types in Rhai: `engine.register_type::<Person>()` + `engine.register_get("name", |p: &mut Person| p.name.clone())`
- Plugin system: `#[export_module]` on a module, register with `engine.register_global_module(Module::new())`

## Code examples

```rust
use rhai::{Engine, Scope};

let engine = Engine::new();
let scope = &mut Scope::new();

// Rust registers a function
engine.register_fn("add", |a: i64, b: i64| a + b);
// Rhai script calls it
let result = engine.eval::<i64>("add(10, 20)")?;

// Call Rhai function from Rust
engine.eval::<()>(
    "fn square(x) { return x * x; }"
)?;
let result = engine.call_fn::<i64>("square", scope, (5,))?;
```

## Connection to other chapters

Rhai's dynamic typing contrasts with Rust's static type system (Ch2). The plugin system is similar to the module system (Ch5). Rhai can be used to script embedded devices (Ch18) or customize WASM front-ends (Ch19).
