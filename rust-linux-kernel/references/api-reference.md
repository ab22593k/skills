# Rust for Linux kernel crate API Reference (v7.1)

Condensed reference for the `kernel` crate at rust.docs.kernel.org v7.1.
All types live in `kernel::*` unless noted.

## Prelude (`kernel::prelude`)

Import via `use kernel::prelude::*`.

Re-exports: `Pin`, `Box`, `KBox`, `VBox`, `KVec`, `VVec`, `Vec`, `KVBox`, `KVVec`,
`Error`, `Result`, `ThisModule`, `CStr`, `CStrExt`, `UserPtr`, `InPlaceInit`,
`build_assert`, `GFP_*` flags, `error::code::*` (ERRNO constants).

## Module Entry Point

```rust
use kernel::prelude::*;

module! {
    type: MyModule,
    name: "my_module",
    authors: ["Author"],
    description: "My kernel module",
    license: "GPL",
}

struct MyModule { /* driver state */ }

impl kernel::Module for MyModule {
    fn init(_module: &'static ThisModule) -> Result<Self> { Ok(Self { }) }
}

impl Drop for MyModule {
    fn drop(&mut self) { /* cleanup */ }
}
```

Use `InPlaceModule` for pin-initialized modules:
```rust
impl kernel::InPlaceModule for MyModule {
    fn init(_module: &'static ThisModule) -> impl PinInit<Self, Error> { ... }
}
```

## Error Handling (`kernel::error`)

- `Error` — Generic integer kernel error. Wraps negative errno.
- `Result<T> = Result<T, Error>` — Kernel result type.
- `error::code::*` — Errno constants: `EPERM`, `ENOENT`, `ENOMEM`, `EINVAL`, `ENODEV`, `EIO`, `EBUSY`, `EAGAIN`, `EFAULT`, `ENOSPC`, `ENOSYS`, `ENOTSUP`, `ERANGE`, `EXDEV`, etc.
- `from_err_ptr(ptr)` — Transform kernel error pointer to normal pointer.
- `to_result(val)` — Convert C int return (0=OK, <0=errno) to `Result<()>`.
- `from_result(f)` — Call closure returning `Result<T>`, convert to C int for FFI.

## Memory Allocation (`kernel::alloc`)

### Types
- `KBox<T>` — Box backed by kernel allocator (GFP-aware).
- `KVec<T>` — Vec backed by kernel allocator (GFP-aware).
- `VBox<T>` — Box for pages (virtually contiguous).
- `VVec<T>` — Vec backed by virtually-contiguous pages.
- `Box<T>` — Alias for `KBox<T>`.
- `Vec<T>` — Alias for `KVec<T>`.

### Allocation Flags (`kernel::alloc::flags`)
- `GFP_KERNEL` — Typical allocation, caller can reclaim.
- `GFP_KERNEL_ACCOUNT` — GFP_KERNEL accounted to kmemcg.
- `GFP_ATOMIC` — Cannot sleep, allocation must succeed.
- `GFP_NOWAIT` — No reclaim, may fail even for small allocs.
- `__GFP_HIGHMEM` — Allow allocation in high memory.
- `__GFP_ZERO` — Zero out allocated memory.
- `__GFP_NOWARN` — Suppress allocation failure reports.

### Usage
```rust
let mut v: KVec<u8> = KVec::new();
v.push(42, GFP_KERNEL)?;

let b = KBox::new(value, GFP_KERNEL)?;
```

- `AllocError` — Allocation failure error type.
- `Allocator` trait — The kernel's allocation interface.
- `Flags` — Flags to use when allocating memory.
- `NumaNode` — NUMA node identifier.
- `layout` — Memory layout utilities.

## Synchronization (`kernel::sync`)

- `Arc<T>` — Reference-counted pointer. Use `Arc::pin_init(init, GFP_KERNEL)?`.
- `ArcBorrow<'a, T>` — Borrowed reference to an `Arc`.
- `UniqueArc<T>` — Arc known to have refcount 1.
- `Refcount` — Atomic reference counter.
- `Mutex<T>` — Sleeping mutex. `new_mutex!(name)` macro for init.
- `MutexGuard<'a, T>` — RAII guard.
- `SpinLock<T>` — Spin lock. `new_spinlock!(name)` macro for init.
- `SpinLockGuard<'a, T>` — RAII guard.
- `CondVar` — Conditional variable. `new_condvar!(name)` macro.
  - `wait()` / `wait_timeout()` / `wake()` / `wake_all()`
- `CondVarTimeoutResult` — Return type of `wait_timeout()`.
- `GlobalLock<T>` — Global lock type. `global_lock!` macro.
- `LockedBy<T, L>` — Data serialized by a lock not wrapping it.
- `SetOnce<T>` — Container populated at most once. Thread-safe.
- `LockClassKey` — Represents a lockdep class.
- `Completion` — Completion support.

### Mutex Pattern
```rust
use kernel::sync::{Mutex, new_mutex};

struct MyState {
    value: u32,
}

#[pin_data]
struct MyDriver {
    #[pin]
    lock: Mutex<MyState>,
}

impl MyDriver {
    fn new() -> impl PinInit<Self, Error> {
        pin_init!(Self {
            lock <- new_mutex!(MyState { value: 0 }, "MyDriver::lock"),
        })
    }

    fn do_thing(self: Pin<&Self>) {
        let mut guard = self.lock.lock();
        guard.value += 1;
    }
}
```

### Arc Pattern
```rust
use kernel::sync::Arc;

let my_arc = Arc::pin_init(pin_init!(MyType { field: value }), GFP_KERNEL)?;
// Clone to pass around:
let clone = my_arc.clone();
```

## String & Data Types (`kernel::str`)

- `CStr` — Borrowed C string (NUL-terminated).
- `CString` — Owned NUL-terminated string.
- `BStr` — Byte string without UTF-8 guarantee.
- `CStrExt` — Extension trait: `to_cstring()`, `as_str()`.
- `Formatter` — Format `fmt::Arguments` into raw buffer.
- `RawFormatter` — Format into byte buffer.
- `NullTerminatedFormatter` — Format into NUL-terminated buffer.
- `as_char_ptr_in_const_context(offset)` — C pointer from const context.
- `kstrtobool(s)` — Parse "Y/y/1" / "N/n/0" to bool.

## Printing (`kernel::print` + macros)

### Console messages
- `pr_emerg!(fmt, ...)` — Emergency (level 0)
- `pr_alert!(fmt, ...)` — Alert (level 1)
- `pr_crit!(fmt, ...)` — Critical (level 2)
- `pr_err!(fmt, ...)` — Error (level 3)
- `pr_warn!(fmt, ...)` — Warning (level 4)
- `pr_notice!(fmt, ...)` — Notice (level 5)
- `pr_info!(fmt, ...)` — Info (level 6)
- `pr_debug!(fmt, ...)` — Debug (level 7)
- `pr_cont!(fmt, ...)` — Continue same line
- `pr_*_once!(fmt, ...)` — Print-at-most-once variants

### Device-aware messages
- `dev_emerg!(dev, fmt, ...)`
- `dev_alert!(dev, fmt, ...)`
- `dev_crit!(dev, fmt, ...)`
- `dev_err!(dev, fmt, ...)`
- `dev_warn!(dev, fmt, ...)`
- `dev_notice!(dev, fmt, ...)`
- `dev_info!(dev, fmt, ...)`
- `dev_dbg!(dev, fmt, ...)`

### Other
- `dbg!(expr)` — Like `std::dbg!` but uses `pr_info!`.
- `container_of!(ptr, type, field)` — Get container pointer from field pointer.

## I/O Memory (`kernel::io_mem` → `kernel::io`)

```rust
use kernel::io;
```

- `Io<T>` — Memory-mapped IO region. Generic over width (u8/u16/u32/u64).
- Methods: `read(offset)`, `write(val, offset)`, `read_relaxed()`, `write_relaxed()`, etc.
- For PCI: `Bar::IoRegion()` — Get Io from a PCI BAR.

## Device Model (`kernel::device`)

- `Device<Ctx>` — Generic device. Context parameter (`device::Core`, bus-specific).
- `DeviceContext` trait — Links driver to device model.
- `DeviceId` — Generic device ID.
- For bus-specific: `platform::Device`, `pci::Device`.

## Driver Framework (`kernel::driver`)

- `Driver` trait (bus-specific) — `probe()`, `unbind()`.
- `Adapter<T: Driver>` — Bridge between C callbacks and Rust trait.
- `Registration<T: RegistrationOps>` — Register a driver.
- `RegistrationOps` trait — Implement per-bus register/unregister.
- `module_driver!` macro — Create module with exactly one driver registration.
- `DeviceId` types: `of::DeviceId`, `acpi::DeviceId`, bus-specific.

## Platform Driver (`kernel::platform`)

```rust
use kernel::platform;

struct MyPlatformDrv { /* private data */ }

impl platform::Driver for MyPlatformDrv {
    type IdInfo = ();

    const OF_ID_TABLE: Option<of::IdTable<Self::IdInfo>> = None;

    fn probe(dev: &Device<device::Core>, _info: &()) -> impl PinInit<Self, Error> {
        pin_init!(MyPlatformDrv { })
    }
}

kernel::module_platform_driver! {
    type: platform::Adapter<MyPlatformDrv>,
    name: "my_plat_drv",
    authors: ["Author"],
    description: "My platform driver",
    license: "GPL",
}
```

## PCI Driver (`kernel::pci`)

```rust
use kernel::pci;

struct MyPciDrv { /* private data */ }

impl pci::Driver for MyPciDrv {
    type IdInfo = ();

    fn probe(dev: &Device<device::Core>, _info: &()) -> impl PinInit<Self, Error> {
        pin_init!(MyPciDrv { })
    }
}

kernel::module_pci_driver! {
    type: pci::Adapter<MyPciDrv>,
    name: "my_pci_drv",
    authors: ["Author"],
    description: "My PCI driver",
    license: "GPL",
}
```

### PCI Types
- `pci::Device` — PCI device representation.
- `pci::Bar` — PCI BAR for I/O.
- `pci::ConfigSpace` — PCI configuration space access.
- `pci::IrqVector` — Allocated IRQ vector.
- `pci::IrqType` — IRQ type flags.
- `pci::DeviceId` — PCI device ID struct.
- `pci::Vendor` — PCI vendor IDs.
- `pci::Class` / `pci::ClassMask` — PCI class codes.

## USB Driver (`kernel::usb`)

- `usb::Driver` trait — USB driver.
- `usb::Device` — USB device.
- `kernel::module_usb_driver!` macro.

## I2C Driver (`kernel::i2c`)

- `i2c::Driver` trait — I2C driver.
- `i2c::Device` — I2C device.
- `kernel::module_i2c_driver!` macro.

## File Operations (`kernel::fs`, `kernel::file`)

- `fs::File` — Kernel file.
- `fs::LocalFile` — Kernel local file.
- `fs::Kiocb` — Wrapper for `struct kiocb`.

## Workqueues (`kernel::workqueue`)

### Types
- `Queue` — A kernel work queue. Get system queues via `system()`, `system_highpri()`, `system_long()`, `system_bh()`, `system_unbound()`, `system_power_efficient()`, `system_freezable()`, etc.
- `Work<T, const ID: u64 = 0>` — Work item link. Use `#[pin]` attribute.
- `DelayedWork<T, const ID: u64 = 0>` — Delayed work item link.

### Traits
- `WorkItem<const ID: u64 = 0>` — Implement `run(this: Self::Pointer)`.
- `HasWork<T, const ID: u64 = 0>` — Declares a type has a `Work<T, ID>` field.
- `HasDelayedWork<T, const ID: u64 = 0>` — Declares a type has a `DelayedWork<T, ID>` field.
- `RawWorkItem` / `RawDelayedWorkItem` — Raw (unsafe) work item traits.
- `WorkItemPointer` — Pointer-level work item trait.

### Macros
- `impl_has_work! { impl HasWork<Self, ID> for T { self.field } }`
- `impl_has_delayed_work! { ... }`
- `new_work!("name")` — Create initializer for `Work`.
- `new_delayed_work!("name")` — Create initializer for `DelayedWork`.

### Pattern
```rust
#[pin_data]
struct MyDrv {
    #[pin]
    work: Work<MyDrv>,
}

impl_has_work! { impl HasWork<Self> for MyDrv { self.work } }

impl WorkItem for MyDrv {
    type Pointer = Arc<MyDrv>;
    fn run(this: Arc<MyDrv>) {
        pr_info!("work executed\n");
    }
}

// Enqueue:
workqueue::system().enqueue(my_arc)?;
```

## IRQ (`kernel::irq`)

- `irq::Registration` — Register an IRQ handler.
- `irq::Handler` trait — Implement `handle()`.
- `irq::DeviceIrq` — Device IRQ registration.
- `irq::testing` — IRQ testing utilities.

## Types (`kernel::types`)

- `Opaque<T>` — Opaque value (for FFI struct fields).
- `ScopeGuard` — Run cleanup closure on drop.
- `ForeignOwnable` trait — Transfer ownership to/from C.
- `NotThreadSafe` — ZST to mark types not `Send`.

## Module Parameters (`kernel::module_param`)

```rust
use kernel::module_param::ModuleParam;

struct MyParams {
    debug: bool,
}
```

- `ModuleParam` trait — Types usable as module parameters.
- `ModuleParamAccess<T>` — Wrapper for kernel parameter access.

## Pin-Init (`kernel::init` + `pin_init` crate)

Most sync structs must be pinned (they contain C self-referential structs).

- `pin_init!(Type { fields, pinned <- init_expr })` — In-place initializer.
- `try_init!(...)` — Fallible version.
- `try_pin_init!(...)` — Fallible pinned version.
- `Opaque::ffi_init(|ptr| { ... })` — Init an Opaque<T> with unsafe FFI.

## Compile-Time Assertions

- `build_assert!(expr)` — Compile-time assertion.
- `static_assert!(expr)` — Static assertion.
- `const_assert!(expr)` — Assertion during const evaluation.
- `build_error!("msg")` — Fail build if code path is reachable.

## Device ID Tables

- `module_device_table!` — Create module device table alias.
- `of::IdTable<T>` — OpenFirmware/DeviceTree ID table.
- `acpi::IdTable<T>` — ACPI ID table.
- Bus-specific: `pci::IdTable`, `i2c_device_table!`, etc.

## Tracepoints

- `declare_trace!` — Declare Rust entry point for a tracepoint.

## Additional Utilities

- `bitmap` — Bitmap operations.
- `rbtree` — Red-black trees.
- `list` — Linked lists.
- `xarray` — XArray abstraction.
- `seq_file` — Seq file bindings.
- `firmware` — Firmware loading.
- `mm` — Memory management.
- `net` — Networking.
- `time` — Time primitives.
- `cred` — Credentials management.
- `task` — Tasks (threads/processes).
- `security` — Linux Security Modules.
- `kunit` — KUnit-based Rust unit tests.
- `fs` — Filesystem support.
- `drm` — DRM subsystem.
- `iov` — IO vectors.
- `scatterlist` — Scatter-gather lists.
- `iommu` — IOMMU support.
- `pwm` — PWM subsystem.
- `regulator` — Regulator control.
- `clk` — Clock framework.
- `cpufreq` — CPU frequency scaling.
- `cpumask` — CPU masks.
- `devres` — Devres (managed device resources).
- `revocable` — Revocable objects.
- `safety` — Safety-related APIs.
- `auxiliary` — Auxiliary bus.
- `faux` — Faux bus.
- `configfs` — ConfigFS interface.
- `jump_label` — Static keys.
- `interop` — Rust-C kernel interface infrastructure.
- `build_assert` — Build-time assertions.
- `bug` — BUG/WARN support.
- `ioctl` — ioctl number definitions.
- `sizes` — Common sizes.
- `id_pool` — ID pool backed by BitmapVec.
- `of` — Device Tree / Open Firmware.
