# Rust For Linux Testing Guide

This guide covers testing strategies for Rust code in the Linux kernel.

## Testing Overview

Testing kernel Rust requires a different approach than userspace Rust due to:
- No standard library
- Kernel environment constraints
- Limited testing infrastructure
- Safety requirements

## Test Types

### 1. Unit Tests

Located in-module for testing internal logic:

```rust
// src/my_module.rs

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_operation() {
        let result = do_something(42);
        assert_eq!(result, Ok(84));
    }

    #[test]
    fn test_error_case() {
        let result = do_something(0);
        assert!(result.is_err());
    }

    #[test]
    #[should_panic(expected = "division by zero")]
    fn test_panic_case() {
        // Test that panics correctly
    }

    #[test]
    fn test_with_fixture() {
        let fixture = MyFixture::new();
        assert!(fixture.is_valid());
    }
}
```

### 2. KUnit Tests

Kernel unit testing framework:

```rust
use kernel::kunit::KUnitTest;

#[kunit_test]
fn test_example() {
    assert_eq!(2 + 2, 4);
}
```

Running KUnit:
```bash
# If available in your kernel
./tools/testing/kunit/kunit.py run --kunitconfig=rust
```

### 3. Integration Tests

Test module behavior in the kernel:

```bash
# Load module
insmod my_module.ko

# Check it loaded
lsmod | grep my_module
dmesg | tail -20

# Test functionality
echo "test" > /dev/my_device

# Check results
dmesg | tail -20

# Unload
rmmod my_module
```

### 4. Property-Based Testing

For functions with mathematical properties:

```rust
#[cfg(test)]
mod property_tests {
    use super::*;

    #[test]
    fn test_commutative() {
        for _ in 0..100 {
            let a = rand::random::<u32>();
            let b = rand::random::<u32>();
            assert_eq!(add(a, b), add(b, a));
        }
    }

    #[test]
    fn test_associative() {
        for _ in 0..100 {
            let a = rand::random::<u32>();
            let b = rand::random::<u32>();
            let c = rand::random::<u32>();
            assert_eq!(add(add(a, b), c), add(a, add(b, c)));
        }
    }
}
```

## Test Organization

### Directory Structure

```
my_module/
├── src/
│   ├── lib.rs
│   ├── module.rs
│   ├── data.rs       # Tests inline
│   └── device.rs     # Tests inline
├── tests/
│   ├── integration_test.rs
│   └── stress_test.rs
└── Cargo.toml
```

### Inline Tests Pattern

```rust
// src/data.rs

pub struct MyData {
    value: u32,
}

impl MyData {
    pub fn new(value: u32) -> Result<Self, Error> {
        if value == 0 {
            return Err(Error::EINVAL);
        }
        Ok(Self { value })
    }

    pub fn get(&self) -> u32 {
        self.value
    }

    // Tests below
    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn test_new_valid() {
            let data = MyData::new(42);
            assert!(data.is_ok());
            assert_eq!(data.unwrap().get(), 42);
        }

        #[test]
        fn test_new_invalid() {
            let data = MyData::new(0);
            assert!(data.is_err());
        }

        #[test]
        fn test_get() {
            let data = MyData::new(100).unwrap();
            assert_eq!(data.get(), 100);
        }
    }
}
```

## Mocking Kernel Dependencies

### Trait-Based Mocking

```rust
// Define trait
pub trait KernelAllocator {
    fn allocate(&self, size: usize) -> Result<*mut u8>;
    fn deallocate(&self, ptr: *mut u8);
}

// Real implementation
pub struct RealAllocator;

impl KernelAllocator for RealAllocator {
    fn allocate(&self, size: usize) -> Result<*mut u8> {
        // Use kernel allocator
        Ok(unsafe { kernel::alloc::alloc(size, GFP_KERNEL) })
    }

    fn deallocate(&self, ptr: *mut u8) {
        unsafe { kernel::alloc::free(ptr) }
    }
}

// Mock for testing
pub struct MockAllocator {
    allocations: Vec<Vec<u8>>,
}

impl MockAllocator {
    pub fn new() -> Self {
        Self {
            allocations: Vec::new(),
        }
    }
}

impl KernelAllocator for MockAllocator {
    fn allocate(&self, size: usize) -> Result<*mut u8> {
        let mut vec = vec![0u8; size];
        let ptr = vec.as_mut_ptr();
        // Note: In real implementation, manage memory differently
        Ok(ptr)
    }

    fn deallocate(&self, _ptr: *mut u8) {
        // Mock - no-op
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_with_mock() {
        let allocator = MockAllocator::new();
        // Test using mock
    }
}
```

### Compile-Time Feature Flags

```rust
#[cfg(not(test))]
use kernel::alloc::flags::GFP_KERNEL;

#[cfg(test)]
use kernel::alloc::flags::GFP_KERNEL; // Or custom mock flag
```

## Testing Error Paths

### Always Test Errors

```rust
#[cfg(test)]
mod error_tests {
    use super::*;

    #[test]
    fn test_allocation_failure() {
        // Test what happens when allocation fails
        // This might require mocking
    }

    #[test]
    fn test_invalid_input() {
        // Test all invalid input cases
        assert!(MyStruct::new(0).is_err());
        assert!(MyStruct::new(u32::MAX).is_err());
    }

    #[test]
    fn test_boundary_conditions() {
        // Test boundaries
        assert!(MyStruct::new(1).is_ok());  // Minimum
        assert!(MyStruct::new(u32::MAX - 1).is_ok());  // Near max
    }
}
```

## Property Testing Patterns

### Invariants

```rust
#[cfg(test)]
mod invariants {
    use super::*;

    #[test]
    fn test_invariant_maintained() {
        let mut data = MyData::new();
        
        // Perform operations
        for _ in 0..100 {
            data.increment();
        }
        
        // Invariant: value should never exceed max
        assert!(data.get() <= MyData::MAX_VALUE);
    }
}
```

### State Machine Testing

```rust
#[cfg(test)]
mod state_machine_tests {
    use super::*;

    #[test]
    fn test_state_transitions() {
        let mut state = StateMachine::new();
        
        // Valid transitions
        assert!(state.transition_to(Ready).is_ok());
        assert!(state.transition_to(Running).is_ok());
        assert!(state.transition_to(Stopped).is_ok());
        
        // Invalid transition
        assert!(state.transition_to(Ready).is_err()); // Can't go back to Ready from Stopped
    }
}
```

## Performance Testing

```rust
#[cfg(test)]
mod performance_tests {
    use super::*;

    #[test]
    fn test_performance() {
        let start = std::time::Instant::now();
        
        // Perform operation many times
        for _ in 0..10000 {
            do_operation();
        }
        
        let duration = start.elapsed();
        
        // Should complete in reasonable time
        assert!(duration.as_millis() < 1000);
    }
}
```

## Running Tests

### Build Tests

```bash
# Build with tests
cargo test --no-run

# Or in kernel tree
make M=rust/modules/my_module LLVM=1
```

### Run In-Kernel Tests

```bash
# Load module
insmod my_module.ko

# Check test results in dmesg
dmesg | grep -i test

# Or with kunit
./tools/testing/kunit/kunit.py run --kunitconfig=rust
```

### Debug Test Failures

```rust
#[test]
fn test_debug() {
    pr_debug!("Debug info: {:?}\n", some_value);
    // Add checkpoints
    pr_info!("Reached point 1\n");
    
    let result = do_something();
    pr_info!("Result: {:?}\n", result);
    
    assert!(result.is_ok());
}
```

## Testing Best Practices

### Do

1. **Test error paths** - Don't just test happy path
2. **Test boundaries** - Min, max, zero, overflow values
3. **Test invariants** - Properties that should always hold
4. **Use descriptive names** - `test_invalid_input_returns_error`
5. **Keep tests independent** - No ordering dependencies
6. **Clean up after yourself** - Release resources in tests

### Don't

1. **Don't test implementation details** - Test behavior, not internals
2. **Don't skip error tests** - Error handling is critical in kernel
3. **Don't assume success** - Always assert explicitly
4. **Don't test multiple things** - One assertion per test ideally
5. **Don't forget edge cases** - Empty, null, max, min

## Test Coverage

### Manual Coverage

```rust
#[test]
fn test_coverage() {
    // Test each branch
    test_case_a();
    test_case_b();
    test_case_c();
    
    // All covered?
    // Check with: coverage report
}
```

### Assertions

```rust
// Basic
assert!(condition);
assert_eq!(a, b);
assert_ne!(a, b);

// With messages
assert!(result.is_ok(), "Expected Ok but got {:?}", result);
assert_eq!(value, expected, "Value mismatch: {}", value);

// Collections
assert!(vec.contains(&item));
assert!(!vec.is_empty());
```

## Common Test Patterns

### Constructor Tests

```rust
#[test]
fn test_constructor_valid() {
    let obj = MyObject::new(42);
    assert!(obj.is_ok());
}

#[test]
fn test_constructor_invalid() {
    assert!(MyObject::new(0).is_err());
    assert!(MyObject::new(u32::MAX).is_err());
}
```

### Builder Tests

```rust
#[test]
fn test_builder() {
    let obj = MyObject::builder()
        .value(42)
        .name("test")
        .build();
        
    assert!(obj.is_ok());
    let obj = obj.unwrap();
    assert_eq!(obj.value(), 42);
}

#[test]
fn test_builder_missing_required() {
    let obj = MyObject::builder()
        .optional("something")
        .build();
        
    assert!(obj.is_err());
}
```

### Async Tests

```rust
#[cfg(test)]
mod async_tests {
    use kernel::sync::Mutex;
    
    #[test]
    fn test_async_operation() {
        // Kernel async patterns are different
        // Test completion handlers, etc.
    }
}
```

## CI/Automation

### Simple Test Script

```bash
#!/bin/bash
set -e

echo "Building module..."
make M=rust/modules/my_module LLVM=1

echo "Loading module..."
insmod my_module.ko

echo "Checking dmesg..."
dmesg | tail -50

echo "Unloading module..."
rmmod my_module

echo "Tests complete!"
```

## References

- [Linux Kernel Testing](https://www.kernel.org/doc/html/latest/dev-tools/index.html)
- [KUnit Documentation](https://www.kernel.org/doc/html/latest/dev-tools/kunit/index.html)
- [Rust Testing Best Practices](https://rust-lang.github.io/rust-clippy/master/index.html)
