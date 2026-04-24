# Rust For Linux Common Patterns

This guide documents common patterns and idioms used in Rust For Linux (RFL) development.

## Initialization Patterns

### Simple Initialization

```rust
struct MyModule {
    data: Box<MyData>,
}

impl MyModule {
    fn new() -> Result<Self> {
        let data = Box::try_new(MyData::new()?)?;
        Ok(Self { data })
    }
}
```

### Initialization with Multiple Resources

```rust
struct MyModule {
    device: DeviceHandle,
    buffer: Box<[u8]>,
    lock: Mutex<()>,
}

impl MyModule {
    fn new() -> Result<Self> {
        let device = DeviceHandle::open("/dev/mydevice")?;
        let buffer = Box::try_new(vec![0u8; PAGE_SIZE])?;
        let lock = Mutex::new(());
        
        Ok(Self { device, buffer, lock })
    }
}

impl Drop for MyModule {
    fn drop(&mut self) {
        // Cleanup happens automatically through Drop impls
    }
}
```

### Deferred Initialization

```rust
struct MyModule {
    state: Mutex<State>,
}

enum State {
    Uninitialized,
    Initialized(InitializedData),
    Failed(Error),
}

impl MyModule {
    fn init(&self) -> Result<()> {
        let mut state = self.state.lock();
        *state = State::Initialized(InitializedData::new()?);
        Ok(())
    }
}
```

## Error Handling Patterns

### Error Type with Conversion

```rust
use kernel::error::Error;

#[derive(Debug)]
pub enum MyError {
    InvalidParam(i32),
    DeviceNotFound,
    IoError(i32),
    OutOfMemory,
}

impl From<MyError> for Error {
    fn from(err: MyError) -> Error {
        match err {
            MyError::InvalidParam(_) => Error::EINVAL,
            MyError::DeviceNotFound => Error::ENODEV,
            MyError::IoError(e) => Error::from_errno(e),
            MyError::OutOfMemory => Error::ENOMEM,
        }
    }
}

impl core::fmt::Display for MyError {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            MyError::InvalidParam(v) => write!(f, "Invalid parameter: {}", v),
            MyError::DeviceNotFound => write!(f, "Device not found"),
            MyError::IoError(e) => write!(f, "I/O error: {}", e),
            MyError::OutOfMemory => write!(f, "Out of memory"),
        }
    }
}
```

### Error Context

```rust
fn complex_operation() -> Result<()> {
    let data = fetch_data()
        .map_err(|e| MyError::FetchFailed(e))?;
    
    let processed = process(data)
        .map_err(|e| MyError::ProcessFailed(e))?;
    
    save(processed)
        .map_err(|e| MyError::SaveFailed(e))?;
    
    Ok(())
}
```

## Synchronization Patterns

### Mutex Guard

```rust
use kernel::sync::Mutex;

struct SharedData {
    counter: u64,
    name: String,
}

static SHARED: Mutex<SharedData> = Mutex::new(SharedData {
    counter: 0,
    name: kernel::c_str!("default").to_string(),
});

fn increment() {
    let mut data = SHARED.lock();
    data.counter += 1;
    pr_info!("Counter: {}\n", data.counter);
}

fn read() -> u64 {
    let data = SHARED.lock();
    data.counter
}
```

### Read-Write Lock

```rust
use kernel::sync::RwLock;

static CONFIG: RwLock<Config> = RwLock::new(Config::default());

fn read_config() -> Config {
    let guard = CONFIG.read();
    guard.clone()
}

fn update_config(new: Config) {
    let mut guard = CONFIG.write();
    *guard = new;
}
```

### Spinlock for Interrupt Context

```rust
use kernel::sync::SpinLock;

static INTERRUPT_DATA: SpinLock<InterruptState> = SpinLock::new(InterruptState::default());

fn interrupt_handler() {
    let mut data = INTERRUPT_DATA.lock();
    data.count += 1;
    data.timestamp = jiffies();
}
```

### Static with Lazy Init

```rust
use kernel::sync::Mutex;
use static_init::dynamic;

static MY_DATA: Mutex<Option<MyData>> = Mutex::new(None);

pub fn get_data() -> Result<&'static MyData> {
    let mut data = MY_DATA.lock();
    if data.is_none() {
        *data = Some(MyData::new()?);
    }
    Ok(data.as_ref().unwrap())
}
```

## Memory Management Patterns

### Box with Fallible Allocation

```rust
struct LargeData {
    buffer: Box<[u8]>,
}

impl LargeData {
    fn new(size: usize) -> Result<Self> {
        let buffer = Box::try_new(vec![0u8; size].into_boxed_slice())?;
        Ok(Self { buffer })
    }
}
```

### Zero-Copy with Userptr

```rust
use kernel::types::UserSlicePtr;

fn process_user_buffer(ptr: UserSlicePtr, writer: &mut impl Writer) -> Result<usize> {
    let len = ptr.len();
    let mut buf = vec![0u8; len];
    ptr.copy_from(&mut buf)?;
    
    // Process in place
    for byte in &mut buf {
        *byte = process_byte(*byte);
    }
    
    writer.write(&buf)?;
    Ok(len)
}
```

### Pin for Self-Referential Data

```rust
use std::pin::Pin;

struct PinnedBuffer {
    data: [u8; 4096],
    offset: usize,
}

impl PinnedBuffer {
    fn new() -> Pin<Box<Self>> {
        Box::pin(Self {
            data: [0; 4096],
            offset: 0,
        })
    }
}
```

## Device Patterns

### Character Device Registration

```rust
use kernel::fs::{File, FileOperations};
use kernel::miscdev::{MiscDevice, Registration};

struct MyDevice;

impl FileOperations for MyDevice {
    type OpenData = Arc<DeviceState>;
    type ReadWriteBits = u32;

    fn open(data: &Self::OpenData, _f: &File) -> Result<()> {
        let mut state = data.lock();
        state.open_count += 1;
        Ok(())
    }

    fn read(
        _f: &File,
        data: &Self::OpenData,
        buf: &mut [u8],
        _offset: u64,
    ) -> Result<usize> {
        let state = data.lock();
        let msg = format!("Open count: {}\n", state.open_count);
        let bytes = msg.as_bytes();
        let len = bytes.len().min(buf.len());
        buf[..len].copy_from_slice(&bytes[..len]);
        Ok(len)
    }
}

pub fn register() -> Result<()> {
    static REGISTRATION: Registration<MyDevice> = Registration::new();
    REGISTRATION.register(kernel::c_str!("my_device"), &MyDevice)
}
```

### Device State with Reference Counting

```rust
use kernel::sync::Arc;
use kernel::sync::ArcBorrow;

struct DeviceState {
    refcount: RefCount,
    data: Mutex<InnerData>,
}

impl DeviceState {
    fn new() -> Result<Arc<Self>> {
        Ok(Arc::try_new(Self {
            refcount: RefCount::new(1),
            data: Mutex::new(InnerData::new()),
        })?)
    }
}
```

## IOCTL Patterns

### IOCTL Definition

```rust
use kernel::ioctl::_IOC;
use kernel::ioctl::_IOC_READ;
use kernel::ioctl::_IOC_WRITE;

const MY_IOCTL_BASE: u8 = b'K';

const MY_GET_INFO: IOCTL<MyInfo> = _IOC!(
    _IOC_READ,
    MY_IOCTL_BASE,
    0x01,
    MyInfo
);

const MY_SET_CONFIG: IOCTL<MyConfig> = _IOC!(
    _IOC_WRITE,
    MY_IOCTL_BASE,
    0x02,
    MyConfig
);
```

### IOCTL Handler

```rust
use kernel::fs::File;
use kernel::ioctl::IOCTL;

fn ioctl(
    _file: &File,
    _data: &DeviceState,
    cmd: u32,
    arg: usize,
) -> Result<i32> {
    match cmd {
        MY_GET_INFO.cmd() => {
            let info = get_info();
            let ptr = arg as *mut MyInfo;
            unsafe { *ptr = info };
            Ok(0)
        }
        MY_SET_CONFIG.cmd() => {
            let ptr = arg as *const MyConfig;
            let config = unsafe { *ptr };
            set_config(config)?;
            Ok(0)
        }
        _ => Err(Error::EINVAL),
    }
}
```

## Module Parameters

### Simple Parameter

```rust
module! {
    type: MyModule,
    name: "my_module",
    author: "Author",
    description: "Description",
    license: "GPL",
    params: {
        debug: bool {
            default: false,
            permissions: 0o644,
            description: "Enable debug logging",
        },
    },
}

static DEBUG: Mutex<bool> = Mutex::new(false);

fn init() -> Result {
    *DEBUG.lock() = <bool as kernel::module::Param<bool>>::get();
    Ok(())
}
```

### Module Parameters Array

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

## Callback Patterns

### Workqueue

```rust
use kernel::workqueue::{Work, WorkQueue};

struct MyWork {
    data: u32,
}

impl Work for MyWork {
    fn run(&self) {
        pr_info!("Work running with data: {}\n", self.data);
    }
}

static MY_WQ: WorkQueue = WorkQueue::new(kernel::c_str!("my_wq"));

pub fn schedule_work(data: u32) {
    MY_WQ.schedule(MyWork { data });
}
```

### Deferred Call

```rust
use kernel::defer::DeferredCall;

static DCALL: DeferredCall<DeferredWork> = DeferredCall::new();

struct DeferredWork(u32);

impl DeferredCall<DeferredWork> for DeferredWork {
    fn run(val: u32) {
        pr_info!("Deferred call: {}\n", val);
    }
}

pub fn trigger_deferred(value: u32) {
    DCALL.schedule(value);
}
```

## Resource Management Patterns

### RAII Cleanup

```rust
struct Resource {
    handle: Handle,
    _lock: Mutex<()>,
}

impl Resource {
    fn new() -> Result<Self> {
        let handle = open_handle()?;
        Ok(Self {
            handle,
            _lock: Mutex::new(()),
        })
    }
}

impl Drop for Resource {
    fn drop(&mut self) {
        close_handle(self.handle);
    }
}

// Usage - automatically cleaned up
fn do_something() -> Result {
    let resource = Resource::new()?;
    // Use resource...
    // Automatically cleaned up when dropped
    Ok(())
}
```

### Explicit Cleanup

```rust
struct Resource {
    handle: Handle,
}

impl Resource {
    fn new() -> Result<Self> {
        let handle = open_handle()?;
        Ok(Self { handle })
    }

    pub fn release(&mut self) {
        if self.handle.is_valid() {
            close_handle(self.handle);
            self.handle = Handle::invalid();
        }
    }
}

impl Drop for Resource {
    fn drop(&mut self) {
        self.release();
    }
}
```

## Async/Event Patterns

### Poll-Based Operation

```rust
use kernel::file::File;
use kernel::fs::PollFlags;

impl FileOperations for MyDevice {
    type OpenData = Arc<DeviceState>;
    type PollBits = u32;

    fn poll(
        _file: &File,
        _data: &Self::OpenData,
    ) -> Result<PollFlags> {
        // Check if data is available
        if data_available() {
            Ok(PollFlags::POLLIN | PollFlags::POLLOUT)
        } else {
            Ok(PollFlags::empty())
        }
    }
}
```

## Best Practices Summary

1. **Use Result for fallible operations** - Always handle errors
2. **Implement Drop for cleanup** - RAII in kernel context
3. **Prefer Mutex over RefCell** - Kernel-compatible interior mutability
4. **Use Pin for self-referential data** - Prevent invalidation
5. **Check allocations** - Use try_new, check for NULL
6. **Document safety** - Unsafe blocks need comments
7. **Keep it simple** - Kernel code should be conservative
