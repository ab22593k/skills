---
name: kernel-maintainer
description: "YOU MUST use this skill for ANY Rust Linux kernel work. This includes: writing kernel modules in Rust, reviewing Rust kernel patches, debugging kernel panics/crashes, working with kernel APIs (Mutex, SpinLock, UserPtr, IOCTL), adding module parameters, creating device drivers (character/block/network), handling kernel errors, memory allocation in kernel, and following kernel Rust coding standards. If the user mentions 'kernel' and 'Rust' together, USE THIS SKILL. Essential for kernel maintainers, patch contributors, and developers working with Rust For Linux (RFL)."
---

# Rust For Linux Kernel Maintainer

A comprehensive skill for working with Rust code in the Linux kernel. This skill provides guidance on coding standards, API usage, patch review, debugging, and code navigation for the Rust For Linux (RFL) project.

## When to Use This Skill

Use this skill when:
- Writing or maintaining Rust kernel modules
- Reviewing Rust patches for the kernel
- Learning Rust For Linux development
- Debugging kernel Rust issues
- Understanding kernel Rust APIs
- Following kernel Rust coding conventions

## Overview

Rust For Linux (RFL) brings Rust as a second language to the Linux kernel, enabling memory-safe kernel module development. This skill helps you navigate the unique constraints and patterns of kernel development with Rust.

Key differences from userspace Rust:
- **No standard library** - Use `core` and `alloc`
- **Custom allocators** - Use kernel allocation functions
- **Different error handling** - Kernel-style error codes
- **Concurrency models** - Kernel synchronization primitives
- **FFI boundaries** - Safe wrappers around C kernel APIs

## Quick Start

### New to Rust For Linux?

1. Start with [coding standards](references/coding_standards.md) to understand kernel Rust conventions
2. Reference the [API guide](references/api_reference.md) for common patterns
3. Review the [patch review guide](references/patch_review.md) to understand expectations

### Working on a Specific Task?

- **Writing a module** → See [coding standards](references/coding_standards.md) + [API reference](references/api_reference.md)
- **Reviewing patches** → See [patch review guide](references/patch_review.md)
- **Debugging issues** → See [debugging guide](references/debugging_guide.md)

---

## Part 1: Fundamentals

Start here to understand Rust For Linux basics.

### Coding Standards

The kernel has specific conventions for Rust code. Always follow these when writing kernel Rust:

- [Coding Standards Guide](references/coding_standards.md)

Key topics:
- Formatting and style (4 spaces, line length limits)
- Naming conventions (PascalCase, snake_case, SCREAMING_SNAKE_CASE)
- Kernel-specific guidelines (error handling, memory management, safety)
- Module organization
- Documentation requirements

### API Reference

Understanding kernel Rust APIs is essential for effective kernel development:

- [API Reference Guide](references/api_reference.md)

Core modules covered:
- `kernel::alloc` - Memory allocation with kernel flags
- `kernel::error` - Error handling with kernel error codes
- `kernel::sync` - Mutex, SpinLock, RwLock
- `kernel::fs` - Filesystem abstractions
- `kernel::device` - Device driver support
- `kernel::ioctl` - IOCTL interface
- `kernel::miscdev` - Miscellaneous devices

---

## Part 2: Code Navigation

### Finding Your Way Around

The Rust For Linux codebase is organized into several key areas:

```
rust/                          - Main Rust support
  ├── bindings/                - Generated C bindings
  ├── core/                    - Core kernel abstractions
  ├── alloc/                   - Memory allocation
  ├── kernel/                  - Main kernel module support
  └── samples/                 - Example modules
```

### Key Patterns

1. **Module Structure**: Each kernel subsystem has Rust wrappers in `rust/kernel/`
2. **FFI Layer**: C bindings are in `rust/bindings/`
3. **Samples**: Example modules in `rust/samples/`

### Navigation Tips

- Use `rust/` as the root for Rust-specific code
- Check `rust/core/` for core abstractions
- Look at `rust/samples/` for working examples
- The RFL directory contains indexed search data for quick lookup

---

## Part 3: Patch Review

When reviewing Rust kernel patches, follow a systematic approach:

### Review Checklist

See [Patch Review Guide](references/patch_review.md) for detailed checklist:

1. **Safety** - Memory safety, concurrency, error handling
2. **Standards** - Coding style, naming, formatting
3. **API Design** - Public interfaces, documentation
4. **Testing** - Unit tests, error path coverage
5. **Performance** - Allocations, data structures, locking

### Key Review Points

- Always verify unsafe code has proper safety comments
- Check error handling is comprehensive
- Ensure kernel idioms are followed (not generic Rust)
- Verify module initialization/cleanup pairing

---

## Part 4: Debugging

When things go wrong, use systematic debugging:

### Common Issues

See [Debugging Guide](references/debugging_guide.md) for:

- Compilation errors
- Runtime issues (module won't load, panics)
- Memory issues (allocation failures, leaks)
- Concurrency issues (deadlocks, race conditions)

### Debugging Techniques

1. **Check dmesg first** - Most kernel issues leave traces
2. **Add pr_info! checkpoints** - Narrow down failure location
3. **Use kernel debugging tools** - DebugFS, tracepoints
4. **Test incrementally** - Small changes, test often

---

## Part 5: Resources

### Templates

#### Module Template

```rust
use kernel::prelude::*;

module! {
    type: MyModule,
    name: "my_rust_module",
    author: "Your Name",
    description: "Description",
    license: "GPL",
}

struct MyModule;

impl kernel::Module for MyModule {
    fn init() -> Result<Self> {
        pr_info!("Module initializing\n");
        Ok(Self)
    }
}
```

#### File Operations Template

```rust
use kernel::fs::{File, FileOperations};

struct MyFileOps;

impl FileOperations for MyFileOps {
    type OpenData = ();
    type ReadWriteBits = u32;

    fn open(_data: &(), _f: &File) -> Result<()> {
        Ok(())
    }
    
    fn read(
        _f: &File,
        _data: &Self::OpenData,
        _buf: &mut [u8],
        _offset: u64,
    ) -> Result<usize> {
        Ok(0)
    }
}
```

### Reference Quick Links

| Topic | File |
|-------|------|
| Coding conventions | [coding_standards.md](references/coding_standards.md) |
| API usage | [api_reference.md](references/api_reference.md) |
| Patch review | [patch_review.md](references/patch_review.md) |
| Debugging | [debugging_guide.md](references/debugging_guide.md) |
| Module structure | [module_structure.md](references/module_structure.md) |
| Testing | [testing_guide.md](references/testing_guide.md) |
| Common patterns | [common_patterns.md](references/common_patterns.md) |

### External Resources

- [Rust For Linux Book](https://rust-for-linux.com/)
- [Linux Kernel Documentation](https://www.kernel.org/doc/html/latest/)
- [Kernel Coding Style](https://www.kernel.org/doc/html/latest/process/coding-style.html)
- [Rust For Linux GitHub](https://github.com/Rust-for-Linux/linux)

---

## Part 6: Module Development

When creating new kernel modules, follow established patterns:

### Module Structure

See [Module Structure Guide](references/module_structure.md) for:
- Directory organization
- Character, block, and network device templates
- Module parameters
- Cargo.toml configuration

### Common Patterns

See [Common Patterns](references/common_patterns.md) for:
- Initialization patterns
- Error handling idioms
- Synchronization primitives
- Memory management
- Device registration

---

## Part 7: Testing

Comprehensive testing is essential for kernel modules:

### Testing Guide

See [Testing Guide](references/testing_guide.md) for:
- Unit tests
- KUnit integration
- Error path testing
- Property-based testing
- Performance testing

---

## Best Practices Summary

1. **Always check allocations** - Never assume memory is available
2. **Document unsafe code** - Safety comments are mandatory
3. **Handle all errors** - No silent failures
4. **Follow kernel patterns** - Kernel idioms, not generic Rust
5. **Test thoroughly** - Error paths, edge cases
6. **Keep modules focused** - One logical change per module
7. **Write good commit messages** - Explain what and why, not how
