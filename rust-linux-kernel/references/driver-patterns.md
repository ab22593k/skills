# Linux Kernel Driver Patterns (Rust, v7.1)

## Architecture

The driver framework uses several layers:

1. **Bus-specific Driver trait** — Implement `platform::Driver`, `pci::Driver`, `usb::Driver`, etc.
2. **Adapter** — Generic `Adapter<T: Driver>` bridges C callbacks to Rust.
3. **Registration** — `Registration<T: RegistrationOps>` registers with the kernel.
4. **Device** — `Device<Ctx>` is the Rust-side device reference.

## Platform Driver

```rust
// SPDX-License-Identifier: GPL-2.0

use kernel::prelude::*;
use kernel::platform;
use kernel::device::Device;
use kernel::device;

module! {
    type: platform::Adapter<MyPlatDrv>,
    name: "my_platform_driver",
    author: "Author",
    description: "My platform driver",
    license: "GPL",
}

#[pin_data]
struct MyPlatDrv {
    #[pin]
    lock: kernel::sync::Mutex<DriverState>,
}

struct DriverState {
    enabled: bool,
    irq_number: u32,
}

impl platform::Driver for MyPlatDrv {
    type IdInfo = ();

    const OF_ID_TABLE: Option<kernel::of::IdTable<Self::IdInfo>> = None;

    fn probe(dev: &Device<device::Core>, _id_info: &()) -> impl PinInit<Self, Error> {
        // dev is the matched device — use it for dev_info!, etc.
        dev_info!(dev, "Probing my platform driver\n");

        // Access platform resources here (IO memory, IRQs, etc.)
        try_pin_init!(MyPlatDrv {
            lock <- kernel::sync::new_mutex!(DriverState {
                enabled: true,
                irq_number: 0,
            }, "MyPlatDrv::lock"),
        })
    }
}
```

### Device Tree Match Table

```rust
const OF_ID_TABLE: Option<kernel::of::IdTable<Self::IdInfo>> = Some(
    kernel::of::IdTable::new(&[
        kernel::of::DeviceId::new_with_info("vendor,device", ()),
    ])
);
```

Use `module_device_table!` for modpost alias:
```rust
kernel::module_device_table! {
    of::IdTable<()>,
    &[
        of::DeviceId::new_with_info("vendor,device", ()),
    ]
}
```

## PCI Driver

```rust
// SPDX-License-Identifier: GPL-2.0

use kernel::prelude::*;
use kernel::pci;
use kernel::device::Device;
use kernel::device;

module! {
    type: pci::Adapter<MyPciDrv>,
    name: "my_pci_driver",
    author: "Author",
    description: "My PCI driver",
    license: "GPL",
}

#[pin_data]
struct MyPciDrv {
    #[pin]
    lock: kernel::sync::Mutex<DriverState>,
}

struct DriverState {
    mmio_base: usize,
    irq: u32,
}

impl pci::Driver for MyPciDrv {
    type IdInfo = ();

    fn probe(dev: &Device<device::Core>, _id: &()) -> impl PinInit<Self, Error> {
        dev_info!(dev, "Probing PCI device\n");

        // PCI-specific initialization (BAR access, etc.)
        try_pin_init!(MyPciDrv {
            lock <- kernel::sync::new_mutex!(DriverState {
                mmio_base: 0,
                irq: 0,
            }, "MyPciDrv::lock"),
        })
    }

    // Optional: implement unbind
    // fn unbind(dev: &Device<device::Core>, this: Pin<&Self>) { ... }
}
```

### PCI Device ID Table

```rust
use kernel::pci::DeviceId;

// In the module! or as a separate table:
kernel::module_device_table! {
    pci::IdTable,
    &[DeviceId::new(0x1234, 0x5678, pci::ANY_ID, pci::ANY_ID, 0, 0)],
}
```

`DeviceId::new(vendor, device, subvendor, subdevice, class, class_mask)`

Constants: `pci::ANY_ID` matches anything, `pci::DeviceId::ANY`.

### PCI BAR Access

```rust
// Each BAR (0-5) can be accessed:
let bar0: pci::Bar = ...;
let io = bar0.io_region(0, 0x1000)?;  // offset, size
io.write(42u32, 0x10);                 // write to offset 0x10
let val: u32 = io.read(0x10);          // read from offset 0x10
```

### PCI IRQ Allocation

```rust
use kernel::pci::IrqType;

let vectors = dev.alloc_irq_vectors(1, 1, IrqType::MSI | IrqType::MSIX)?;
let irq = vectors.get_irq(0)?;
```

## USB Driver

```rust
// SPDX-License-Identifier: GPL-2.0

use kernel::prelude::*;
use kernel::usb;
use kernel::device::*;

module! {
    type: usb::Adapter<MyUsbDrv>,
    name: "my_usb_driver",
    author: "Author",
    description: "My USB driver",
    license: "GPL",
}

struct MyUsbDrv;

impl usb::Driver for MyUsbDrv {
    type IdInfo = ();

    fn probe(dev: &Device<device::Core>, _info: &()) -> impl PinInit<Self, Error> {
        dev_info!(dev, "USB device probed\n");
        pin_init!(MyUsbDrv)
    }
}

// USB device ID table
kernel::module_device_table! {
    usb::IdTable,
    &[usb::DeviceId::new(0x1234, 0x5678)],
}
```

## I2C Driver

```rust
// SPDX-License-Identifier: GPL-2.0

use kernel::prelude::*;
use kernel::i2c;
use kernel::device::*;

module! {
    type: i2c::Adapter<MyI2cDrv>,
    name: "my_i2c_driver",
    author: "Author",
    description: "My I2C driver",
    license: "GPL",
}

#[pin_data]
struct MyI2cDrv {
    address: u16,
}

impl i2c::Driver for MyI2cDrv {
    type IdInfo = ();

    fn probe(dev: &Device<device::Core>, _info: &()) -> impl PinInit<Self, Error> {
        try_pin_init!(MyI2cDrv {
            address: 0x50,
        })
    }
}
```

## Misc Device

```rust
// SPDX-License-Identifier: GPL-2.0

use kernel::prelude::*;
use kernel::miscdevice;

#[pin_data]
struct MyMisc {
    #[pin]
    lock: kernel::sync::Mutex<u32>,
}

impl miscdevice::MiscDevice for MyMisc {
    fn open(dev: &miscdevice::MiscDeviceRegistration<Self>) -> Result<()> {
        pr_info!("misc device opened\n");
        Ok(())
    }

    fn release(dev: &miscdevice::MiscDeviceRegistration<Self>) {
        pr_info!("misc device closed\n");
    }
}
```

## File Operations

For full file operation handlers, see:
- `kernel::file` — File and file descriptor types.
- `kernel::fs` — Kiocb wrapper, file system support.

## Auxiliary Driver

For auxiliary bus devices (sub-devices of a parent driver):

```rust
// SPDX-License-Identifier: GPL-2.0

use kernel::auxiliary;

struct MyAuxDrv;

impl auxiliary::Driver for MyAuxDrv {
    type IdInfo = ();

    fn probe(dev: &Device<device::Core>, _info: &()) -> impl PinInit<Self, Error> {
        pin_init!(MyAuxDrv)
    }
}
```

## Common Patterns

### Registering an IRQ handler
```rust
use kernel::irq;

struct MyIrqHandler;

impl irq::Handler for MyIrqHandler {
    type Data = Arc<MyDrv>;

    fn handle(data: &Arc<MyDrv>, _irq: u32) -> irq::Return {
        // Handle interrupt
        irq::Return::Handled
    }
}

// Register with:
let reg = irq::Registration::new(irq_number, Arc::clone(&my_drv), GFP_KERNEL)?;
// Registration is automatically cleaned up when `reg` is dropped.
```

### Using I/O memory
```rust
use kernel::io::Io;

let mmio = Io::<u32>::new(phys_addr, size)?;
let val = mmio.read(0x00);          // Read register at offset 0
mmio.write(val | 0x01, 0x00);       // Set bit 0
```

### Workqueues
```rust
use kernel::workqueue::{self, Work, WorkItem, impl_has_work, new_work};

// See api-reference.md for full workqueue pattern.
// System queues:
workqueue::system()                     // system_wq
workqueue::system_highpri()             // system_highpri_wq
workqueue::system_long()                // system_long_wq
workqueue::system_bh()                  // system_bh_wq
workqueue::system_unbound()             // system_unbound_wq
workqueue::system_power_efficient()     // system_power_efficient_wq
workqueue::system_freezable()           // system_freezable_wq

// Enqueue:
queue.enqueue(arc_ref)?;               // Queue now
queue.enqueue_delayed(arc_ref, jiffies)?;  // Queue after delay
```
