---
name: rust-linux-kernel
description: >-
  Expert in writing Linux kernel modules and drivers in Rust using the kernel
  crate (v7.1). Trigger whenever the user asks to write, modify, debug, or
  analyze any in-kernel Rust code: kernel modules, platform/PCI/USB/I2C drivers,
  file systems, workqueues, synchronization primitives, memory allocation, ioctl
  handlers, or device tree bindings. If the task involves Rust code that runs
  inside the Linux kernel (not userspace), this skill should be used. Also
  trigger on questions about the Rust for Linux project, out-of-tree module
  setup, kernel crate APIs, pin-init patterns, or porting C drivers to Rust.
  Do NOT use for general Rust programming, userspace drivers, eBPF programs, or
  kernel C code that happens to be compiled with rustc — only Rust code that
  depends on the kernel crate.
---

# Writing Linux Kernel Modules in Rust

This skill teaches you how to write Linux kernel modules in Rust using the
[`kernel` crate](https://rust.docs.kernel.org) (v7.1). The kernel crate wraps
core kernel APIs (memory allocation, synchronization, driver model, I/O,
workqueues, IRQs, etc.) for safe use from Rust.

## Prerequisites & Build System

Before writing code, understand the environment:

- **Required**: A Linux kernel tree with `CONFIG_RUST=y` (Rust support enabled).
- **Toolchain**: Rust compiler (rustc) built with the `rust-src` component and
  the LLVM/Clang toolchain the kernel was built with.
- **Build**: Use `make -C $KDIR M=$PWD LLVM=1` (same as C modules but LLVM is
  required for Rust).
- **Minimal Kbuild**: `obj-m := my_module.o` in a `Kbuild` or `Makefile`.
- **Out-of-tree**: The template at
  https://github.com/Rust-for-Linux/rust-out-of-tree-module is the reference.

## Module Structure

Every module needs three things:

1. **`module!` macro invocation** — declares type, name, author, description,
   license, and optional parameters.
2. **A struct** — holds module state (allocations, driver data).
3. **`Module` trait impl** — `init()` runs on load, `Drop::drop()` runs on unload.

For modules with pinned fields (required when using `Mutex`, `SpinLock`, `Work`,
`DelayedWork`, `Arc`-based types, or any field marked `#[pin]`), use
`InPlaceModule` instead of `Module` and `try_pin_init!` / `pin_init!` instead of
returning `Ok(...)`.

The `references/module-skeleton.md` file has complete templates for all these
variants — look there first.

## Key API Concepts

### Allocation

All kernel allocations use GFP flags. The standard flag is `GFP_KERNEL` (can
sleep/reclaim). `GFP_ATOMIC` for atomic contexts. `GFP_NOWAIT` for when you
cannot stall at all. All fallible allocations return `Result` — always check it.

```rust
let mut v: KVec<u8> = KVec::new();
v.push(42, GFP_KERNEL)?;
let b = KBox::new(my_data, GFP_KERNEL)?;
```

### Error Handling

Kernel errors use `Error` (wraps negative errno). `Result<T>` is `Result<T, Error>`.
The `error::code` module has constants (`EINVAL`, `ENOMEM`, `ENODEV`, etc.).
Use `?` everywhere — Kernel Rust is `Result`-heavy.

### Synchronization

- `SpinLock<T>` — For short critical sections, no sleeping. Must be pinned.
- `Mutex<T>` — For longer sections, can sleep. Must be pinned.
- `Arc<T>` — Reference-counted ownership. Use `Arc::pin_init()`.
- `CondVar` — For condition variable patterns. Must be pinned.

All initialized via the `pin_init!` / `try_pin_init!` + `new_mutex!` /
`new_spinlock!` macros. The pin-init crate is how kernel Rust works — you
cannot directly construct most sync types.

### Pin-Init

This is the single most important concept to get right:

- Types with self-referential C structs (most sync types, workqueues, etc.) use
  `#[pin_data]` and `#[pin]` fields.
- Initialize pinned fields with `field <- init_expr` syntax in `pin_init!`.
- Non-pinned fields use `field: value` syntax.
- The `pin_init!` macro returns `impl PinInit<T, Error>`.

### The Driver Model

Bus-specific drivers implement a `Driver` trait, then get wrapped in an `Adapter`
and registered via `module_*_driver!` macro:

| Bus      | Trait              | Adapter                | Macro                     |
| -------- | ------------------ | ---------------------- | ------------------------- |
| Platform | `platform::Driver` | `platform::Adapter<T>` | `module_platform_driver!` |
| PCI      | `pci::Driver`      | `pci::Adapter<T>`      | `module_pci_driver!`      |
| USB      | `usb::Driver`      | `usb::Adapter<T>`      | `module_usb_driver!`      |
| I2C      | `i2c::Driver`      | `i2c::Adapter<T>`      | `module_i2c_driver!`      |

### Synchronization Patterns

Always think about what context your code runs in:

- **Module init/exit**: Called in process context. Can sleep. GFP_KERNEL is OK.
- **Driver probe/unbind**: Process context. Can sleep.
- **IRQ handlers**: Atomic context. Must use `GFP_ATOMIC`, `SpinLock` (not `Mutex`).
- **Workqueue callbacks**: Process context (but might be reentrant).
- **File operations**: Depends. Some operations can sleep, others not.
  Check the C API contract for each operation.

## Reference Files

- `references/api-reference.md` — Condensed API surface for the v7.1 kernel
  crate: all modules, types, traits, macros, and their signatures.
- `references/module-skeleton.md` — Copy-pasteable templates: minimal module,
  module with params, pin-init module, module with workqueue, KUnit tests.
- `references/driver-patterns.md` — Complete driver implementations: platform,
  PCI, USB, I2C, misc device, with device ID tables, BAR access, IRQ
  registration, and workqueue integration.

When writing code, read `module-skeleton.md` first for the module structure,
then `driver-patterns.md` if the user asked about a driver, and cross-reference
types/signatures in `api-reference.md`.

## Safety

- The `kernel` crate uses `unsafe` internally to wrap C APIs. When writing a
  module, you should rarely need `unsafe` yourself. If you find yourself writing
  `unsafe`, first check if the kernel crate already has a safe wrapper for what
  you need.
- All `extern "C"` FFI calls into the kernel must be `unsafe`.
- Verify invariants in comments, especially for `Opaque<T>` usage.
- Follow the kernel's coding style: use `// SAFETY:` comments for every unsafe
  block (not `// Safety:` or just `// safe`), explaining which precondition
  makes the operation safe.
- Module init must not panic. Panics in init cause undefined behavior.
