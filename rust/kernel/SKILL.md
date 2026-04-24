---
name: rust-kernel
description: "MANDATORY skill for ANY Rust Linux kernel work. Use this skill IMMEDIATELY when you're working with Rust in the Linux kernel - writing kernel modules, reviewing kernel patches, debugging kernel panics, or implementing device drivers. This skill is essential for Rust For Linux (RFL) contributors and kernel maintainers. If you're doing ANY kernel Rust development, this skill MUST be your first choice."
---

# Rust For Linux Kernel Maintainer - Essential Guide

## 🚨 CRITICAL: When to Use This Skill

**USE THIS SKILL FOR:**
- ✅ Writing ANY Rust kernel module (character, block, network devices)
- ✅ Reviewing Rust patches for the Linux kernel
- ✅ Debugging kernel panics or crashes in Rust code
- ✅ Working with kernel Rust APIs and patterns
- ✅ Understanding kernel Rust coding standards
- ✅ Memory allocation in kernel context
- ✅ Kernel synchronization (Mutex, SpinLock, RwLock)
- ✅ FFI boundaries between kernel C code and Rust
- ✅ Adding module parameters to kernel modules
- ✅ Creating device drivers in Rust
- ✅ Any "Rust" + "kernel" + "Linux" work

**DON'T USE THIS FOR:**
- ❌ Userspace Rust applications
- ❌ General Rust programming questions
- ❌ Web development with Rust
- ❌ Non-kernel Rust projects

## Why This Skill is Non-Negotiable for Kernel Work

Rust in the Linux kernel has **unique constraints** that differ from userspace Rust:

- **No standard library** - Only `core` and `alloc` available
- **Custom allocators** - Must use kernel allocation APIs
- **Kernel error handling** - Error codes, not `Result<T, E>`
- **Concurrency models** - Kernel synchronization primitives only
- **FFI boundaries** - Safe wrappers required for C kernel APIs
- **Safety requirements** - Every `unsafe` block needs justification

Using this skill ensures you follow kernel-specific patterns, not generic Rust advice.

## Quick Start - Are You Working on Kernel Rust?

### If YES to any of these, USE THIS SKILL:
1. Are you writing `mod.rs` for a kernel module?
2. Are you implementing `FileOperations` for a character device?
3. Are you handling `ioctl` commands in Rust?
4. Are you debugging a kernel oops or panic?
5. Are you reviewing a `kernel/rust/` patch?
6. Are you working with `kernel::sync` primitives?
7. Are you allocating memory with `kernel::alloc`?

### If you answered YES → Continue reading this guide
### If you answered NO → This skill is NOT for you

## Part 1: Kernel Rust Fundamentals

### The Kernel Environment (READ THIS FIRST)

Kernel Rust is fundamentally different from userspace Rust:

| Aspect | Userspace Rust | Kernel Rust |
|--------|----------------|-------------|
| Standard Library | Full `std` available | Only `core` + `alloc` |
| Memory Allocation | `Box`, `Vec`, etc. | `kernel::alloc` with flags |
| Error Handling | `Result<T, E>` | Kernel error codes |
| Concurrency | `std::sync` primitives | Kernel sync primitives |
| Safety Requirements | Safety guidelines | Mandatory safety comments |

### Module Structure

Every Rust kernel module requires this pattern:

```rust
use kernel::prelude::*;

module! {
    type: MyModule,
    name: "my_rust_module",
    author: "Your Name",
    description: "Description of what this module does",
    license: "GPL",  // or other kernel-approved license
}

struct MyModule {
    // Your module state
}

impl kernel::Module for MyModule {
    fn init() -> Result<Self> {
        pr_info!("My module loaded\n");
        Ok(Self { /* initialize state */ })
    }
}

impl Drop for MyModule {
    fn drop(&mut self) {
        pr_info!("My module unloaded\n");
    }
}
```

### Critical Rules for Kernel Rust

1. **Every `unsafe` block needs a comment explaining WHY it's safe**
2. **All errors must be handled - no silent failures**
3. **Memory must be freed in the same context it was allocated**
4. **Module initialization and cleanup must be paired**
5. **Never hold locks across potentially failing operations**

## Part 2: Common Kernel Patterns

### Character Device Module

See [coding_standards.md](references/coding_standards.md) for full details:

```rust
use kernel::fs::{File, FileOperations};
use kernel::types::compat::c_char;

struct MyDevice {
    data: [u8; 256],
}

impl FileOperations for MyDevice {
    type OpenData = ();
    type ReadWriteBits = u32;

    fn open(_data: &(), _f: &File) -> Result<()> {
        pr_info!("Device opened\n");
        Ok(())
    }

    fn read(
        &self,
        _f: &File,
        _data: &Self::OpenData,
        buf: &mut [u8],
        _offset: u64,
    ) -> Result<usize> {
        // Copy data to userspace
        let count = buf.len().min(self.data.len());
        buf[..count].copy_from_slice(&self.data[..count]);
        Ok(count)
    }
}
```

### Network Device Module

- Implement `netdev::NetworkDevice`
- Handle TX/RX paths
- Use kernel socket buffers (SKBs)

### Block Device Module

- Implement `block::BlockDevice`
- Handle request queues
- Manage bio structures

## Part 3: Error Handling

### Kernel Error Codes

```rust
use kernel::error::Error;

fn my_function() -> Result<()> {
    // Success case
    Ok(())
}

fn another_function() -> Result<()> {
    if some_error_condition {
        return Err(Error::ENOMEM);  // Out of memory
    }
    Ok(())
}
```

### Common Error Codes

- `Error::ENOMEM` - Out of memory
- `Error::EINVAL` - Invalid argument
- `Error::EFAULT` - Bad address
- `Error::EIO` - I/O error
- `Error::EBUSY` - Device busy

## Part 4: Synchronization

### Mutex (Sleepable)

```rust
use kernel::sync::Mutex;

struct MyData {
    value: u32,
}

let data = Mutex::new(MyData { value: 0 });

// Lock for reading/writing
let mut guard = data.lock();
guard.value = 42;
```

### SpinLock (Non-sleepable)

```rust
use kernel::sync::SpinLock;

let lock = SpinLock::new(0u32);
*lock.lock() = 42;
```

## Part 5: Memory Allocation

### Kernel Heap Allocation

```rust
use kernel::alloc::AllocFlags;

// Allocate with GFP_KERNEL flags
let ptr = kernel::alloc::AllocBuffer::new(1024, AllocFlags::ZERO)?;
```

### Static Allocation

```rust
use kernel::init::KernelInit;

static mut MY_BUFFER: [u8; 1024] = [0; 1024];

// Initialize at module load
let buffer = unsafe { &mut MY_BUFFER };
```

## Part 6: FFI and C Interop

### Calling C Functions

```rust
use kernel::bindings;

// Call a kernel C function
unsafe {
    bindings::some_kernel_function(args);
}
```

### Creating IOCTLs

See [patch_review.md](references/patch_review.md) for IOCTL patterns.

## Part 7: Debugging

### Essential Debugging Commands

1. **dmesg** - Check kernel logs
   ```bash
   dmesg | grep -i my_module
   ```

2. **Insmod with debug**
   ```bash
   insmod my_module.ko debug=1
   ```

3. **Module info**
   ```bash
   modinfo my_module.ko
   ```

### Adding Debug Output

```rust
pr_info!("Module loaded, state: {:?}\n", state);
pr_debug!("Detailed debug info\n");  // Only with debug build
```

## Quick Reference Links

| Topic | Documentation |
|-------|---------------|
| Coding Standards | [coding_standards.md](references/coding_standards.md) |
| API Reference | [api_reference.md](references/api_reference.md) |
| Patch Review | [patch_review.md](references/patch_review.md) |
| Debugging | [debugging_guide.md](references/debugging_guide.md) |
| Testing | [testing_guide.md](references/testing_guide.md) |
| Module Structure | [module_structure.md](references/module_structure.md) |
| Common Patterns | [common_patterns.md](references/common_patterns.md) |

## When in Doubt

**ASK THIS SKILL:** If you're unsure whether this skill applies, USE IT. It's better to use the correct skill and have it determine you don't need it than to miss critical kernel-specific guidance.

**Key Principle:** Kernel Rust is about safety in an unsafe environment. Every decision has implications for system stability, security, and reliability.
