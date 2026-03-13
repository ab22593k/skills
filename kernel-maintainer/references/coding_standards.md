# Rust For Linux Coding Standards

This document covers the coding standards and conventions used in the Rust For Linux (RFL) project.

## General Principles

- **Kernel Context**: Write code that is suitable for the Linux kernel environment
- **Safety**: Leverage Rust's safety guarantees while maintaining kernel compatibility
- **Consistency**: Follow existing patterns in the codebase

## Formatting and Style

### Basic Rules

- Follow the standard Rust formatting (run `cargo fmt` before submitting)
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters (soft limit, 120 hard limit)
- Use `rustfmt.toml` from the kernel tree

### Naming Conventions

- **Types**: `PascalCase` (e.g., `KernelPtr`, `FileOperations`)
- **Functions**: `snake_case` (e.g., `read_kernel_memory`, `allocate_buffer`)
- **Constants**: `SCREAMING_SNAKE_CASE` (e.g., `PAGE_SIZE`, `MAX_BUFFER`)
- **Traits**: `PascalCase` with optional `Verb` or `Noun` suffix (e.g., `Alloc`, `Drop`)
- **Modules**: `snake_case` (e.g., `kernel`, `ffi`)

## Kernel-Specific Guidelines

### Error Handling

- Use `kernel::error::Result` and `kernel::error::Error` for kernel errors
- Never use `panic!()` in kernel code (use `WARN()`, `BUG()`, or return errors)
- Propagate errors using the `?` operator
- Provide meaningful error messages

### Memory Management

- Use kernel allocation functions (`kernel::alloc::flags::*`)
- Always check for allocation failures
- Follow the kernel's memory allocation patterns
- Prefer stack allocation when size is known at compile time

### Safety

- Use `unsafe` blocks sparingly and document why they're necessary
- Use kernel-provided wrappers for unsafe operations
- Never bypass safety checks in pursuit of performance
- Use `Pin` for types that must not be moved

### Concurrency

- Use kernel synchronization primitives (`spinlock`, `mutex`, `rwlock`)
- Follow the kernel's locking conventions
- Be aware of interrupt context restrictions
- Use proper memory barriers when needed

## Module Organization

### Core Modules

```
kernel/          - Main kernel abstractions
  ├── alloc/     - Memory allocation
  ├── error.rs   - Error handling
  ├── ioctl.rs   - IOCTL support
  ├── sync/      - Synchronization primitives
  └── fs/        - Filesystem abstractions
```

### Module Visibility

- Use `#[cfg(...)]` for conditional compilation
- Keep public APIs minimal and well-documented
- Use `pub(crate)` for internal APIs within a crate

## Documentation

### Requirements

- All public APIs must have doc comments (`///`)
- Include examples for complex functions
- Document safety invariants for unsafe code
- Note any kernel-specific behavior differences

### Format

```rust
/// Short description (one line)
///
/// Longer description if needed.
/// 
/// # Arguments
/// 
/// * `arg1` - Description of first argument
/// 
/// # Safety
/// 
/// Caller must ensure...
/// 
/// # Examples
/// 
/// ```ignore
/// let result = unsafe { function() };
/// ```
```

## Testing

### Unit Tests

- Place unit tests in a `tests` module (conditional with `#[cfg(test)]`)
- Use the kernel's testing infrastructure when available
- Mock kernel dependencies appropriately

### Integration Tests

- Follow kernel testing conventions
- Use `kunit` where applicable
- Test error paths thoroughly

## Foreign Function Interface (FFI)

### C to Rust Bindings

- Use `bindgen` to generate bindings automatically
- Wrap unsafe C functions in safe Rust wrappers
- Maintain soundness invariants at the boundary

### Rust to C Exports

- Use `#[no_mangle]` and `extern "C"` for C-compatible functions
- Document memory ownership clearly
- Use the kernel's module initialization macros

## Common Patterns

### Error Type Pattern

```rust
use kernel::error::Error;

#[derive(Debug, Clone, Copy)]
pub enum MyError {
    #[error("Invalid parameter: {0}")]
    InvalidParam(i32),
    #[error("Out of memory")]
    OutOfMemory,
    // ... other variants
}

impl From<MyError> for Error {
    fn from(err: MyError) -> Error {
        Error::EINVAL // or appropriate kernel error
    }
}
```

### Static Object Pattern

```rust
use kernel::sync::Mutex;
use static_mut::static_mut;

static MY_DATA: Mutex<Option<MyData>> = Mutex::new(None);

pub fn initialize() -> Result {
    let mut data = MY_DATA.lock();
    *data = Some(MyData::new()?);
    Ok(())
}
```

## Resources

- [Rust For Linux Book](https://rust-for-linux.com/)
- [Linux Kernel Coding Style](https://www.kernel.org/doc/html/latest/process/coding-style.html)
- [Kernel Documentation](https://www.kernel.org/doc/html/latest/)
