# Rust For Linux Debugging Guide

This guide covers common issues and debugging strategies for Rust code in the Linux kernel.

## Common Issues

### Compilation Errors

#### "cannot find crate `kernel`"

**Cause**: Kernel crate not in search path

**Solution**:
```bash
# Ensure kernel is built with Rust support
make LLVM=1 rustavailable

# Or set the kernel source path
export RUST_KERNEL_SRC=/path/to/linux
```

#### "function is not safe to call from this context"

**Cause**: Calling function in wrong context (e.g., atomic context)

**Solution**:
- Move code to process context
- Use different kernel API
- Check current context with `in_atomic()` or `in_interrupt()`

#### "trait bound not satisfied"

**Cause**: Missing trait implementation or wrong generic parameter

**Solution**:
- Add required trait imports
- Check trait bounds on generics
- Verify generic parameters

### Runtime Issues

#### Module Won't Load

**Check**:
```bash
# Check dmesg for errors
dmesg | tail -100

# Check module info
modinfo my_module.ko

# Verify symbols
nm my_module.ko | grep -i unresolved
```

**Common Causes**:
- Missing dependencies (`modprobe` order)
- Symbol version mismatch
- Wrong kernel version
- Initialization failure

#### Kernel Panic on Load

**Check**:
```bash
dmesg | tail -50
```

**Common Causes**:
- NULL pointer dereference in `init()` or `probe()`
- Invalid memory access
- Deadlock on module initialization

**Debugging**:
```rust
fn init() -> Result {
    pr_info!("Starting initialization\n");
    
    // Add checkpoints
    let data = MyData::new()?;
    pr_info!("Data created: {:?}\n", data);
    
    // ...
    Ok(())
}
```

#### Oops/Segmentation Fault

**Check**:
```bash
dmesg | grep -A 20 "Oops"
```

**Common Causes**:
- Use after free
- Invalid pointer arithmetic
- Race condition
- Stack overflow

### Memory Issues

#### Allocation Failures

**Pattern**:
```rust
// Always check allocations
fn allocate_something() -> Result<Box<MyData>> {
    let data = Box::try_new(MyData::new())
        .ok_or(Error::ENOMEM)?;  // Handle failure
    
    Ok(data)
}
```

**Debugging**:
```bash
# Check memory pressure
free -h
cat /proc/meminfo
vmstat 1
```

#### Memory Leaks

**Detection**:
- Check with `kmemleak`:
```bash
echo scan > /sys/kernel/debug/kmemleak
cat /sys/kernel/debug/kmemleak
```

**Prevention**:
```rust
impl Drop for MyResource {
    fn drop(&mut self) {
        // Always free allocated resources
        unsafe {
            kernel::alloc::free(self.ptr);
        }
    }
}
```

### Concurrency Issues

#### Deadlock

**Signs**:
- System hangs on module load
- Specific operations hang
- Lockdep warning in dmesg

**Debugging**:
```bash
# Check lockdep
dmesg | grep -i "lockdep"

# Check for circular dependencies
cat /proc/lock_stat
```

**Prevention**:
- Always acquire locks in consistent order
- Use `Mutex::try_lock()` for timeouts
- Document lock ordering

#### Race Condition

**Signs**:
- Intermittent crashes
- Data corruption
- Non-deterministic behavior

**Debugging**:
```bash
# Use lockdep to detect
dmesg | grep -i "possible"

# Check for data races with kernel tools
```

**Prevention**:
- Use proper synchronization
- Minimize lock scope
- Use atomic operations where appropriate

## Debugging Techniques

### Printing

#### pr_info!, pr_warn!, pr_err!

```rust
pr_info!("Variable value: {}\n", value);
pr_warn!("Unexpected condition at {}:{}\n", file!(), line!());
pr_err!("Failed with code: {}\n", error);
```

#### Debug Builds

```rust
#[cfg(debug_assertions)]
fn debug_only() {
    pr_debug!("Debug info: {:?}\n", self);
}
```

### Kernel Debugging Tools

#### DebugFS

```rust
use kernel::debugfs;

static MY_DEBUGFS: debugfs::Dir = debugfs::Dir::new();

pub fn init() -> Result {
    MY_DEBUGFS.create("my_module")?;
    
    // Create debug files
    MY_DEBUGFS.create_file("counter", &self.counter)?;
    Ok(())
}
```

#### Tracepoints

```rust
// Using kernel trace events
trace_my_event!(name, value);
```

### GDB Debugging

#### Setup

```bash
# Load kernel module symbols
add-symbol-file my_module.ko 0xffffffffffffffff

# Set breakpoints
break my_function
break rust_ kernelsymbol
```

#### Useful Commands

```gdb
# Print kernel types
ptype struct MyStruct

# Call kernel functions
print my_kernel_function()

# Watch memory
watch *(int*)0xffff...
```

### KUnit Tests

#### Writing Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_my_function() {
        let result = my_function();
        assert!(result.is_ok());
    }

    #[test]
    fn test_error_case() {
        let result = my_function_fails();
        assert_eq!(result.unwrap_err(), Error::EINVAL);
    }
}
```

#### Running Tests

```bash
# If integrated with kunit
./tools/testing/kunit/kunit.py run --kunitconfig=rust

# Or manual
insmod my_module.ko
dmesg | grep -i "test"
```

## Common Fixes

### Fix: "cannot borrow as mutable more than once"

```rust
// Problem
let mut data = self.data.lock();
let ref1 = &data;
let ref2 = &mut data; // Error!
```

```rust
// Solution: separate scopes
let mut data = self.data.lock();
let ref1 = &data;
drop(ref1); // Release first borrow
let ref2 = &mut data;
```

### Fix: "cannot move out of shared reference"

```rust
// Problem
fn take_ownership(data: &MyStruct) -> MyStruct {
    MyStruct { inner: data.inner } // Error: can't move
}

// Solution: derive/copy if possible, or redesign
#[derive(Clone)]
struct MyStruct {
    inner: SomeType,
}
```

### Fix: "lifetime mismatch"

```rust
// Problem: returning reference with wrong lifetime
fn get_ref(&self) -> &SomeType {
    &self.data // Must ensure data lives long enough
}

// Solution: ensure proper lifetime
fn get_ref<'a>(&'a self) -> &'a SomeType {
    &'a self.data
}
```

### Fix: "trait not implemented"

```rust
// Problem
struct MyType;

fn use_something<T: Display>(t: T) {}  // MyType doesn't implement Display

// Solution: implement trait or use different trait
impl fmt::Display for MyType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "MyType")
    }
}
```

## Debugging Checklist

1. **Check dmesg first** - Most issues leave traces
2. **Add pr_info! checkpoints** - Narrow down failure location
3. **Start simple** - Comment out complex code, add back gradually
4. **Check return values** - Don't ignore errors
5. **Verify assumptions** - Use assertions in debug builds
6. **Test incrementally** - Small changes, test often
7. **Use version control** - git diff helps identify changes

## Useful Commands

```bash
# View module info
modinfo my_module.ko

# Check kernel messages
dmesg -w | grep my_module

# Load with debug
insmod my_module.ko

# Unload
rmmod my_module

# Check symbols
nm -C my_module.ko | grep my_function

# Disassemble
objdump -d my_module.ko

# Check dependencies
lsmod | grep my_module

# Kernel config
zcat /proc/config.gz | grep -i rust
```

## Resources

- [Linux Kernel Debugging Guide](https://www.kernel.org/doc/html/latest/dev-tools/gdb-kdump-debugging.html)
- [Rust For Linux Debugging](https://rust-for-linux.com/debugging-rust-in-the-kernel)
- [Kernel Debugging Tips](https://elinux.org/Debugging_The_Linux_Kernel_Using_GDB)
