---
name: Integrating Rust
description: |
  This is the complete superpower for systematically converting ANY existing codebase
  (C/C++, Python, Java, Go, JavaScript, etc.) into safe, idiomatic, high-performance Rust.

  Trigger aggressively whenever the user mentions:
  - “convert my [language] code to Rust”
  - “migrate legacy codebase”
  - “rewrite in Rust”
  - “port from C++ / Python / Java”
  - “how to make this Rust-safe”
  - performance, memory safety, concurrency, or FFI concerns during migration

  Default first response: “Perfect. Let’s follow a structured 7-phase migration workflow from Integrating Rust. Shall we start with Phase 1: Assessment of your current codebase?”
compatibility: none (pure conversational + templates + optional code_execution for verification)
---

#### Core Rule (never break this)

**Incremental, Safety-First Migration**  
Never do a big-bang rewrite. Always follow the 7-phase workflow:

1. Assessment
2. Planning & Incremental Strategy
3. Language Mapping & Translation
4. FFI / Interop Layer (if needed)
5. Idiomatic Rust Refactoring
6. Testing & Verification
7. Optimization & Polish

#### When to Use This Skill – Trigger Matrix

| Situation                   | Immediate Action                              |
| --------------------------- | --------------------------------------------- |
| User has C/C++ legacy code  | Start with FFI + ownership mapping            |
| Python / Java service       | Focus on ownership + concurrency patterns     |
| Performance-critical module | Emphasize zero-cost abstractions + benchmarks |
| Embedded or systems code    | Use AVR / embedded chapter patterns           |
| Web backend or Wasm target  | WebAssembly + Rhai integration path           |

**Default behavior**: Begin with “Let’s run a quick assessment of your codebase first” and guide through the 7 phases.

#### The Structured 7-Phase Migration Workflow

**Phase 1: Assessment**

- Inventory all modules, dependencies, and performance-critical paths.
- Identify memory management patterns (malloc/free, GC, manual ownership).
- Map concurrency model (threads, async, locks).

**Phase 2: Planning & Incremental Strategy**

- Decide on migration strategy: strangler fig, module-by-module, or parallel implementation.
- Create a dependency graph and migration order.
- Define success metrics (safety, performance, test coverage).

**Phase 3: Language Mapping & Translation**

- Use language-specific conversion maps (C++ → Rust ownership, Python → Result/Option, etc.).
- Translate core data structures and algorithms first.

**Phase 4: FFI / Interop Layer**

- Build safe FFI bindings using `bindgen` or manual `extern "C"`.
- Create Rust-friendly wrappers around foreign code.

**Phase 5: Idiomatic Rust Refactoring**

- Apply ownership, borrowing, traits, and generics.
- Replace raw pointers, manual memory, and unsafe blocks with safe Rust patterns.
- Use `Cow`, `Rc`/`Arc`, and smart pointers judiciously.

**Phase 6: Testing & Verification**

- Port or write comprehensive tests.
- Run property-based testing and fuzzing.
- Compare performance and memory usage before/after.

**Phase 7: Optimization & Polish**

- Apply zero-cost abstractions.
- Add benchmarks and profiling.
- Final safety audit and documentation.

#### Ready-to-Use Templates (copy-paste)

**1. Migration Assessment Template**

```markdown
**Codebase Assessment**

- Language: [C++/Python/Java/...]
- Size: [LOC / modules]
- Memory model: [manual / GC / ...]
- Concurrency: [threads / async / locks]
- Critical paths: [list]
- Dependencies: [list]
```

**2. Language Mapping Example (C++ → Rust)**

```rust
// C++: raw pointer + manual delete
T* ptr = new T();
// Rust: ownership + RAII
let ptr = Box::new(T::new());
```

**3. Incremental Migration Checklist**

- [ ] Phase 1 complete
- [ ] FFI layer written
- [ ] Core module ported
- [ ] Tests passing at 90%+
- [ ] Performance benchmarked

#### Core Process Checklist (use every time)

1. Run Phase 1 Assessment
2. Create migration roadmap
3. Translate one module at a time
4. Add FFI wrapper if needed
5. Refactor to idiomatic Rust
6. Verify with tests + benchmarks
7. Polish and document

#### Output Formats This Skill Always Uses

- 7-phase migration plan
- Language-specific mapping table
- Before/after code comparison
- Safety & performance checklist
- Next-phase recommendation
