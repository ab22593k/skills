# Linux Kernel Module Skeleton (Rust, v7.1)

## Build System

### Makefile
```makefile
# SPDX-License-Identifier: GPL-2.0
KDIR ?= /lib/modules/`uname -r`/build

default:
	$(MAKE) -C $(KDIR) M=$$PWD

modules_install: default
	$(MAKE) -C $(KDIR) M=$$PWD modules_install

clean:
	$(MAKE) -C $(KDIR) M=$$PWD clean
```

### Kbuild
```makefile
# SPDX-License-Identifier: GPL-2.0
obj-m := my_module.o
```

### Build
```sh
make KDIR=/path/to/linux-with-rust-support LLVM=1
```

The kernel must have `CONFIG_RUST=y`. The kernel tree must have Rust metadata available (generated during kernel build).

## Minimal Module

```rust
// SPDX-License-Identifier: GPL-2.0

//! My kernel module

use kernel::prelude::*;

module! {
    type: MyModule,
    name: "my_module",
    author: "Your Name",
    description: "My first Rust kernel module",
    license: "GPL",
}

struct MyModule {
    message: KVec<u8>,
}

impl kernel::Module for MyModule {
    fn init(_module: &'static ThisModule) -> Result<Self> {
        pr_info!("my_module loaded\n");

        let mut message = KVec::new();
        message.extend_from_slice(b"Hello, kernel!", GFP_KERNEL)?;

        Ok(MyModule { message })
    }
}

impl Drop for MyModule {
    fn drop(&mut self) {
        pr_info!("my_module unloaded\n");
    }
}
```

## Module with Parameters

```rust
// SPDX-License-Identifier: GPL-2.0

use kernel::prelude::*;
use kernel::module_param::ModuleParam;

module! {
    type: MyParamModule,
    name: "my_param_module",
    author: "Author",
    description: "Module with parameters",
    license: "GPL",
    params: {
        count: i32 {
            default: 1,
            permissions: 0o644,
            description: "Number of times to print",
        },
        name: [u8; 32] {
            default: b"default\0",
            permissions: 0o444,
            description: "A name string",
        },
    },
}

struct MyParamModule {
    count: i32,
}

impl kernel::Module for MyParamModule {
    fn init(module: &'static ThisModule) -> Result<Self> {
        pr_info!("count = {}\n", module.count);
        pr_info!("name = {:?}\n", module.name);
        Ok(MyParamModule { count: module.count })
    }
}

impl Drop for MyParamModule {
    fn drop(&mut self) {
        pr_info!("my_param_module unloaded\n");
    }
}
```

## Pin-Initialized Module

For modules with pinned fields (needed when containing `Work`, `Mutex`, `SpinLock`, etc.):

```rust
// SPDX-License-Identifier: GPL-2.0

use kernel::prelude::*;
use kernel::sync::{Mutex, new_mutex};

module! {
    type: MyPinnedModule,
    name: "my_pinned_module",
    author: "Author",
    description: "Module with pinned initialization",
    license: "GPL",
}

#[pin_data]
struct MyPinnedModule {
    #[pin]
    lock: Mutex<InnerState>,
    counter: u32,
}

struct InnerState {
    value: u32,
}

impl kernel::InPlaceModule for MyPinnedModule {
    fn init(_module: &'static ThisModule) -> impl PinInit<Self, Error> {
        try_pin_init!(MyPinnedModule {
            lock <- new_mutex!(InnerState { value: 0 }, "MyPinnedModule::lock"),
            counter: 0,
        })
    }
}
```

## Module with Arc + Workqueue

```rust
// SPDX-License-Identifier: GPL-2.0

use kernel::prelude::*;
use kernel::sync::Arc;
use kernel::workqueue::{self, impl_has_work, new_work, Work, WorkItem};

module! {
    type: MyAsyncModule,
    name: "my_async_module",
    author: "Author",
    description: "Module demonstrating async work",
    license: "GPL",
}

#[pin_data]
struct MyAsyncModule {
    #[pin]
    work: Work<MyAsyncModule>,
    data: u32,
}

impl_has_work! {
    impl HasWork<Self> for MyAsyncModule { self.work }
}

impl WorkItem for MyAsyncModule {
    type Pointer = Arc<MyAsyncModule>;

    fn run(this: Arc<MyAsyncModule>) {
        pr_info!("Work executed, data = {}\n", this.data);
    }
}

impl kernel::InPlaceModule for MyAsyncModule {
    fn init(_module: &'static ThisModule) -> impl PinInit<Self, Error> {
        try_pin_init!(MyAsyncModule {
            work <- new_work!("MyAsyncModule::work"),
            data: 42,
        })
    }
}

impl Drop for MyAsyncModule {
    fn drop(&mut self) {
        pr_info!("my_async_module unloaded\n");
    }
}

// To enqueue work from somewhere:
fn schedule_work(module: Arc<MyAsyncModule>) {
    let _ = workqueue::system().enqueue(module);
}
```

## KUnit Tests

```rust
use kernel::prelude::*;

kernel::kunit_tests! {
    my_tests {
        #[test]
        fn test_addition() {
            // Standard Rust test assertions
            assert_eq!(2 + 2, 4);
        }

        #[test]
        fn test_string() {
            let s = CStr::from_bytes_with_nul(b"hello\0").unwrap();
            assert_eq!(s.to_bytes(), b"hello");
        }
    }
}
```
