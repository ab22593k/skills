# Rust For Linux Module Structure Guide

This guide covers how to structure Rust kernel modules for the Linux kernel.

## Module Organization

### Basic Structure

```
my_module/
├── Cargo.toml
├── src/
│   ├── lib.rs          # Module entry point
│   ├── main.rs         # Or main.rs for binaries
│   ├── module.rs       # Module definition
│   ├── device.rs       # Device-specific code
│   ├── ioctl.rs        # IOCTL handlers
│   ├── data.rs         # Data structures
│   └── [other].rs      # Split as needed
├── tests/              # Integration tests (optional)
└── examples/          # Example usage (optional)
```

### Minimal Module

```rust
// src/lib.rs
use kernel::prelude::*;

module! {
    type: MyModule,
    name: "my_rust_module",
    author: "Your Name",
    description: "A brief description",
    license: "GPL",
    params: {
        my_param: u32 {
            default: 42,
            permissions: 0o644,
            description: "Description of parameter",
        },
    },
}

struct MyModule {
    // State
}

impl MyModule {
    fn new() -> Result<Self> {
        Ok(Self {})
    }
}

impl kernel::Module for MyModule {
    fn init() -> Result<Self> {
        pr_info!("Module loaded\n");
        Self::new()
    }
}

impl Drop for MyModule {
    fn drop(&mut self) {
        pr_info!("Module unloaded\n");
    }
}
```

## Module Types

### Character Device

```rust
// src/chardev.rs
use kernel::fs::File;
use kernel::fs::FileOperations;
use kernel::miscdev::{MiscDevice, Registration};
use kernel::prelude::*;

pub struct MyCharDevice {
    // Device state
}

impl FileOperations for MyCharDevice {
    type OpenData = ();
    type ReadWriteBits = u32;

    fn open(_data: &(), _file: &File) -> Result<()> {
        Ok(())
    }

    fn read(
        &self,
        _file: &File,
        _data: &Self::OpenData,
        buf: &mut [u8],
        _offset: u64,
    ) -> Result<usize> {
        let data = b"Hello from Rust!\n";
        let len = data.len().min(buf.len());
        buf[..len].copy_from_slice(&data[..len]);
        Ok(len)
    }
}

pub struct MyCharDevRegistration {
    registration: Registration<MyCharDevice>,
}

impl MyCharDevRegistration {
    pub fn new() -> Result<Self> {
        Ok(Self {
            registration: Registration::new(),
        })
    }

    pub fn register(&self) -> Result<()> {
        self.registration.register(kernel::c_str!("my_chardev"), &MyCharDevice)
    }
}
```

### Block Device

```rust
// src/blockdev.rs
use kernel::block::{BlockDevice, BlockDeviceOps, DiskEvents};
use kernel::prelude::*;

pub struct MyBlockDevice {
    // Block device state
}

impl BlockDevice for MyBlockDevice {
    fn read(&self, _sector: u64, _buf: &mut [u8]) -> Result<usize> {
        // Read logic
        Ok(0)
    }

    fn write(&self, _sector: u64, _buf: &[u8]) -> Result<usize> {
        // Write logic
        Ok(0)
    }

    fn submit_flush(&self, _flush: DiskEvents) -> Result<u64> {
        Ok(0)
    }
}
```

### Network Device

```rust
// src/netdev.rs
use kernel::net::Device;
use kernel::prelude::*;

pub struct MyNetDevice {
    // Network device state
}

impl Device for MyNetDevice {
    fn open(&self) -> Result<()> {
        Ok(())
    }

    fn stop(&self) -> Result<()> {
        Ok(())
    }

    fn xmit(&self, _skb: &mut impl Skb) -> Result {
        Ok(())
    }

    fn set_mac_address(&self, _addr: &[u8]) -> Result<()> {
        Ok(())
    }
}
```

### Platform Device

```rust
// src/platform.rs
use kernel::device::{Device, Driver, DriverLike};
use kernel::platform::{PlatformDevice, Registration};

pub struct MyPlatformDriver {
    _registration: Registration<MyPlatformDriver>,
}

impl MyPlatformDriver {
    pub fn new() -> Result<Self> {
        Ok(Self {
            _registration: Registration::new(),
        })
    }
}

impl Driver for MyPlatformDriver {
    type DeviceType = PlatformDevice;

    fn probe(&self, device: &Self::DeviceType) -> Result<()> {
        pr_info!("Probing platform device: {}\n", device.name());
        Ok(())
    }

    fn remove(&self, device: &Self::DeviceType) {
        pr_info!("Removing platform device: {}\n", device.name());
    }
}
```

### USB Device

```rust
// src/usb.rs
use kernel::usb::{UsbDevice, UsbDriver, UsbInterface};

pub struct MyUsbDriver;

impl UsbDriver for MyUsbDriver {
    type Device = MyUsbDevice;
    type Config = MyUsbConfig;

    fn probe(&self, device: &Self::Device, _interface: &UsbInterface) -> Result<()> {
        pr_info!("USB device plugged: {}\n", device.product_name());
        Ok(())
    }

    fn disconnect(&self, _device: &Self::Device) {
        pr_info!("USB device unplugged\n");
    }
}
```

## Splitting Modules

### When to Split

Split your module when:
- File exceeds 500-1000 lines
- Distinct functional areas emerge
- Multiple people will work on it
- Code is reused elsewhere

### How to Split

```rust
// src/lib.rs
pub mod module;
pub mod device;
pub mod ioctl;
pub mod data;

// Re-export for convenience
pub use device::MyDevice;
pub use ioctl::*;
pub use data::*;
```

### Cross-Module Dependencies

```rust
// src/device.rs
use crate::data::{MyData, MyDataError};

pub struct MyDevice {
    data: MyData,
}

impl MyDevice {
    pub fn new() -> Result<Self, MyDataError> {
        Ok(Self {
            data: MyData::new()?,
        })
    }
}
```

## Module Parameters

### Simple Parameter

```rust
module! {
    // ...
    params: {
        debug_level: u32 {
            default: 0,
            permissions: 0o644,
            description: "Debug level (0=off, 1=info, 2=debug)",
        },
    },
}
```

### Array Parameter

```rust
module! {
    params: {
        device_ids: &[u32] {
            default: &[0x1234, 0x5678],
            permissions: 0o644,
            description: "Supported device IDs",
        },
    },
}
```

### String Parameter

```rust
module! {
    params: {
        device_name: &str {
            default: "my_device",
            permissions: 0o644,
            description: "Device name",
        },
    },
}
```

## Testing Structure

### Unit Tests

```rust
// src/data.rs

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_creation() {
        let data = MyData::new();
        assert!(data.is_ok());
    }

    #[test]
    fn test_failure() {
        let data = MyData::new_err();
        assert!(data.is_err());
    }
}
```

### Integration Tests

```
tests/
├── test_module.rs
└── test_device.rs
```

```rust
// tests/test_module.rs
use kernel_test::test;

#[test]
fn test_module_load() {
    // Test module loading
}
```

## Error Handling Patterns

### Module-Level Errors

```rust
// src/errors.rs
use kernel::error::Error;

#[derive(Debug, Clone, Copy)]
pub enum ModuleError {
    #[error("Invalid parameter: {0}")]
    InvalidParam(i32),
    #[error("Device not found")]
    DeviceNotFound,
    #[error("Already initialized")]
    AlreadyInitialized,
}

impl From<ModuleError> for Error {
    fn from(err: ModuleError) -> Error {
        match err {
            ModuleError::InvalidParam(_) => Error::EINVAL,
            ModuleError::DeviceNotFound => Error::ENODEV,
            ModuleError::AlreadyInitialized => Error::EBUSY,
        }
    }
}
```

## Cargo.toml Configuration

```toml
[package]
name = "my_rust_module"
version = "0.1.0"
edition = "2021"

[dependencies]
kernel = { path = "/path/to/linux/rust/kernel" }
rustc-std-workspace-core = { path = "/path/to/linux/rust/rustc-std-workspace-core" }

[lib]
crate-type = ["cdylib"]

[profile.release]
opt-level = 2
lto = true
codegen-units = 1
```

## Best Practices

1. **Keep init focused** - Minimal work in init, defer to workqueues if needed
2. **Clean up properly** - Implement Drop or explicit cleanup
3. **Handle errors** - All fallible operations must handle errors
4. **Document APIs** - Public functions need doc comments
5. **Test early** - Write tests alongside code
6. **Version control** - Keep related files together
7. **Split reasonably** - Don't over-engineer, but don't dump everything in one file
