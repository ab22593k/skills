# Rust For Linux API Reference

This document provides a reference for key APIs and abstractions used in Rust For Linux (RFL).

## Core Modules

### kernel::alloc

Memory allocation in the kernel.

```rust
use kernel::alloc::flags::*;

// Flags available:
PAGE_SIZE       // Allocate page-aligned memory
GFP_KERNEL       // Kernel allocation (may sleep)
GFP_ATOMIC      // Atomic allocation (cannot sleep)
GFP_USER        // User allocation
__GFP_ZERO      // Zero-initialize memory
```

**Functions**:
- `kernel::alloc::Allocator::new()` - Create a new allocator instance
- `alloc()` - Allocate memory with given flags
- `free()` - Free allocated memory

### kernel::error

Error handling types.

```rust
use kernel::error::{Error, Result};
```

**Error Codes**:
- `Error::EINVAL` - Invalid argument
- `Error::ENOMEM` - Out of memory
- `Error::EFAULT` - Bad address
- `Error::ENODEV` - No such device
- `Error::EBUSY` - Device or resource busy
- `Error::ENOENT` - No such file or directory
- `Error::EIO` - I/O error

**Pattern**:
```rust
fn my_function() -> Result<ReturnType> {
    // Use ? to propagate errors
    let data = some_kernel_call()?;
    Ok(data)
}
```

### kernel::sync

Synchronization primitives.

```rust
use kernel::sync::{Mutex, SpinLock, RwLock, Ref, RefMut};
```

**Mutex**:
```rust
static MY_LOCK: Mutex<MyData> = Mutex::new(MyData::default());

fn access_data() {
    let mut data = MY_LOCK.lock();
    data.modify();
} // Lock automatically released
```

**SpinLock** (for interrupt context):
```rust
static SPIN_DATA: SpinLock<SharedData> = SpinLock::new(SharedData::default());

fn interrupt_handler() {
    let mut data = SPIN_DATA.lock();
    data.update();
}
```

**RwLock** (for read-heavy workloads):
```rust
static RW_DATA: RwLock<BigData> = RwLock::new(BigData::default());

fn read_data() -> Ref<'static, BigData> {
    RW_DATA.read()
}

fn write_data() -> RefMut<'static, BigData> {
    RW_DATA.write()
}
```

### kernel::fs

Filesystem abstractions.

```rust
use kernel::fs::{File, Dirent, inode, dentry};
```

**File Operations**:
```rust
use kernel::fs::FileOperations;

struct MyFileOps;

impl FileOperations for MyFileOps {
    type OpenData = MyData;
    type ReadWriteBits = u32;

    fn open(data: &MyData, _f: &File) -> Result<()> {
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

    // Other operations: write, mmap, llseek, etc.
}

kernel::module_file_ops!(MyFileOps);
```

### kernel::device

Device driver support.

```rust
use kernel::device::{Device, DeviceRef};
use kernel::device::Driver;
```

**Device Registration**:
```rust
struct MyDevice {
    name: &'static str,
}

impl Device for MyDevice {
    fn probe(&self) -> Result<()> {
        // Initialize device
        Ok(())
    }

    fn remove(&self) {
        // Clean up
    }
}
```

### kernel::ioctl

IOCTL interface.

```rust
use kernel::ioctl::{IOCTL, _IOC};
```

**IOCTL Commands**:
```rust
const MY_IOCTL_BASE: u8 = b'K';

const MY_GET_VALUE: IOCTL<u32> = _IOC!(
    _IOC_READ,
    MY_IOCTL_BASE,
    0x01,
    u32
);

const MY_SET_VALUE: IOCTL<u32> = _IOC!(
    _IOC_WRITE,
    MY_IOCTL_BASE,
    0x02,
    u32
);
```

### kernel::miscdev

Miscellaneous device driver.

```rust
use kernel::miscdev::{MiscDevice, Registration};
```

**Example**:
```rust
struct MyMisc;

impl MiscDevice for MyMisc {
    fn open(&self, _file: &File) -> Result<()> {
        Ok(())
    }

    fn read(&self, _file: &File, _buf: &mut [u8]) -> Result<usize> {
        Ok(0)
    }
}

static MY_MISC: Registration<MyMisc> = Registration::new();
```

### kernel::miscellaneous

Miscellaneous utilities.

```rust
use kernel::miscellaneous::*;
```

## Important Traits

### Disposable

For types that need cleanup.

```rust
use kernel::Disposable;

struct MyResource {
    ptr: *mut u8,
}

impl Disposable for MyResource {
    fn dispose(self) {
        unsafe { kernel::alloc::free(self.ptr); }
    }
}
```

### AString / CString

String types for kernel interfaces.

```rust
use kernel::str::{AString, CString};
use kernel::c_types::c_char;
```

## Data Types

### Kernel Types

```rust
use kernel::c_types::{c_int, c_uint, c_void, size_t, ptrdiff_t};

// Kernel-specific
use kernel::types::{UserPtr, UserSlicePtr};
```

### smart_ptr

Smart pointers with kernel semantics.

```rust
use kernel::types::{Arc, Box, Pin};
```

## Helper Macros

### module! 

Define a kernel module.

```rust
module! {
    type: MyModule,
    name: "my_rust_module",
    author: "Your Name",
    description: "Description of what this module does",
    license: "GPL",
    params: {
        my_param: u32 {
            default: 42,
            permissions: 0o644,
            description: "Description of parameter",
        },
    },
}
```

### pr_info!, pr_warn!, pr_err!

Logging macros.

```rust
pr_info!("Module loaded with param: {}\n", param);
pr_warn!("Something unexpected: {}\n", value);
pr_err!("Critical failure: {}\n", error);
```

### static_mut!

Thread-safe static mutable data.

```rust
use static_mut::static_mut;

static_mut! {
    static MY_GLOBAL: Mutex<MyData> = Mutex::new(MyData::new());
}
```

## Pinning

Types that must not be moved in memory.

```rust
use std::pin::Pin;

struct PinnedData {
    data: [u8; 256],
}

impl PinnedData {
    fn new() -> Pin<Box<PinnedData>> {
        Box::pin(PinnedData { data: [0; 256] })
    }
}
```

## User/Kernel Boundary

### UserPtr

Safe pointer to user memory.

```rust
use kernel::types::UserPtr;

fn copy_from_user(dest: &mut [u8], src: UserPtr<u8>) -> Result<usize> {
    unsafe { src.read(dest) }
}
```

### UserSlicePtr

Read/write to user memory with bounds checking.

```rust
use kernel::types::UserSlicePtr;

fn process_user_buffer(ptr: UserSlicePtr) -> Result<usize> {
    let len = ptr.len();
    let mut buf = vec![0u8; len];
    ptr.copy_from(&mut buf)?;
    // Process...
    Ok(len)
}
```

## Common Operations

### Registration Pattern

```rust
use kernel::Registration;

static MY_REGISTRATION: Registration<MyType> = Registration::new();

pub fn init() -> Result {
    MY_REGISTRATION.register(
        kernel::c_str!("my_device"),
        &MyType,
    )
}
```

### File Operations Registration

```rust
use kernel::fs::File;

kernel::module_fs_ops!(MyFileOps);
```

## Best Practices

1. **Always check for NULL** before dereferencing pointers
2. **Use proper error codes** from `kernel::error`
3. **Initialize all fields** in structures
4. **Document safety requirements** for unsafe code
5. **Use kernel-provided wrappers** instead of raw C calls
6. **Handle all error paths** including allocation failures

## Resources

- [Rust For Linux Repository](https://github.com/Rust-for-Linux/linux)
- [Kernel API Documentation](https://docs.kernel.org/)
- [Linux Device Drivers](https://lwn.net/Kernel/LDD3/)
