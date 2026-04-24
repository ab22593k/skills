# Rust For Linux Patch Review Guide

This guide provides a checklist and patterns for reviewing Rust patches in the Linux kernel.

## Review Process Overview

1. **Understand the Context**
   - What problem does this patch solve?
   - Is this a new feature, bug fix, or refactoring?
   - What are the dependencies (other patches, kernel versions)?

2. **Verify Basic Requirements**
   - Does it compile?
   - Does it follow kernel coding standards?
   - Are there proper error handlers?

3. **Deep Review**
   - Safety guarantees
   - Performance implications
   - API design
   - Documentation

4. **Provide Actionable Feedback**
   - Be specific about issues
   - Suggest solutions
   - Acknowledge good work

## Pre-Review Checklist

### Compilation & Build

- [ ] Code compiles without warnings
- [ ] `cargo clippy` passes (if applicable)
- [ ] `cargo fmt` has been run
- [ ] Build succeeds with appropriate kernel config
- [ ] No linker errors

### Basic Quality

- [ ] Commit message follows kernel conventions
- [ ] Patch is minimal and focused
- [ ] Changes are properly separated (one logical change per patch)
- [ ] No unintended whitespace changes

## Detailed Review Checklist

### 1. Safety & Correctness

#### Memory Safety

- [ ] No raw pointers without proper bounds checking
- [ ] All allocations are checked for failure
- [ ] No use of `unsafe` without justification
- [ ] `unsafe` blocks have safety comments
- [ ] Proper lifetime management
- [ ] No use-after-free potential
- [ ] No buffer overflows

#### Concurrency

- [ ] Proper use of synchronization primitives
- [ ] No race conditions
- [ ] Correct lock ordering (if multiple locks)
- [ ] Appropriate use of atomic operations
- [ ] Interrupt context considerations addressed
- [ ] No blocking in atomic context

#### Error Handling

- [ ] All errors are propagated or handled
- [ ] Error messages are meaningful
- [ ] No silent failures
- [ ] Error codes are appropriate
- [ ] No resource leaks on error paths

### 2. Coding Standards

#### Formatting

- [ ] Follows Rust formatting conventions
- [ ] Consistent indentation (4 spaces)
- [ ] No trailing whitespace
- [ ] Lines under 100 characters (soft limit)

#### Naming

- [ ] Types use PascalCase
- [ ] Functions use snake_case
- [ ] Constants use SCREAMING_SNAKE_CASE
- [ ] Names are descriptive and consistent

#### Style

- [ ] Follows kernel Rust style guide
- [ ] Uses kernel idioms (not generic Rust patterns)
- [ ] Consistent with surrounding code

### 3. API Design

#### Public APIs

- [ ] Well-documented with doc comments
- [ ] Safety invariants documented for unsafe APIs
- [ ] Error conditions documented
- [ ] Examples provided for complex APIs
- [ ] Stable API surface (if public)

#### Module Structure

- [ ] Clean module boundaries
- [ ] No unnecessary public exposure
- [ ] Proper re-exports

### 4. Documentation

#### Code Documentation

- [ ] All public items have doc comments
- [ ] Unsafe code has `# Safety` sections
- [ ] Complex logic is explained
- [ ] Examples are provided

#### Commit Messages

- [ ] Follows kernel format
- [ ] First line under 72 characters
- [ ] Body explains "what" and "why", not "how"
- [ ] References related issues/PRs
- [ ] Signed-off-by line present

### 5. Testing

- [ ] Unit tests added (if applicable)
- [ ] Tests cover error paths
- [ ] No test compilation issues
- [ ] Tests follow kernel patterns

### 6. Performance

- [ ] No unnecessary allocations
- [ ] Appropriate data structures used
- [ ] Lock contention considered
- [ ] No O(n²) algorithms without justification
- [ ] Hot paths optimized

### 7. Kernel Integration

#### Module Definition

- [ ] Proper `module!` macro usage
- [ ] Correct license (usually GPL)
- [ ] All parameters properly defined
- [ ] Cleanup handlers implemented

#### FFI Boundaries

- [ ] Safe wrappers around C functions
- [ ] Proper ownership transfer
- [ ] Soundness maintained at boundary

#### Resource Management

- [ ] Proper init/cleanup pairing
- [ ] No resource leaks
- [ ] Correct module lifetime

## Review Anti-Patterns

### Don't Do

1. **Don't nitpick style** - Focus on correctness first
2. **Don't suggest rewrites** without clear benefit
3. **Don't block on preferences** - Rust has multiple idioms
4. **Don't ignore context** - Understand the problem first
5. **Don't review in isolation** - Consider the whole patch series

### Do

1. **Do question assumptions** - Kernel differs from userspace
2. **Do consider backports** - Will this apply cleanly?
3. **Do check similar code** - Look for patterns
4. **Do test locally** - Build and run if possible
5. **Do be constructive** - Explain why, not just what

## Example Reviews

### Good Review

```
The patch looks good overall. A few suggestions:

1. Line 45: Consider checking for NULL before dereferencing.
   This prevents a potential panic if allocation fails.

2. Line 78: The error message could be more descriptive.
   Instead of "Operation failed", consider "Failed to allocate
   memory for buffer of size {size}"

3. The documentation is excellent. The safety comments on
   the unsafe block are clear and comprehensive.

Overall: Acked-by: Reviewer Name <email>
```

### Needs Work Review

```
This patch needs revision before it can be merged:

Critical Issues:
- Line 23: Unchecked pointer dereference - must add bounds check
- Line 67: Missing error check after allocation - this can cause use-after-free

Minor Issues:
- Consider using kernel's `UserSlicePtr` instead of manual copy
- The module name could be more descriptive

Please address the critical issues and resend.
```

## Common Patterns to Look For

### Good Patterns

```rust
// Proper error handling
fn do_something() -> Result<()> {
    let data = allocate()?;
    // Use data...
    Ok(())
}

// Safe FFI wrapper
fn safe_wrapper(raw: *const c_void) -> Result<SafeType> {
    // Validate pointer...
    Ok(SafeType::from_raw(raw)?)
}

// Proper initialization
impl MyStruct {
    fn new() -> Result<Self> {
        let inner = KernelStruct::new()?;
        Ok(Self { inner })
    }
}
```

### Warning Signs

```rust
// Danger: No error check
let ptr = alloc(GFP_KERNEL);
ptr.write(42); // Could panic if ptr is null

// Danger: Unsafe without comment
unsafe {
    *ptr = value; // Why is this unsafe?
}

// Danger: Silent failure
fn risky() -> Result<()> {
    if rand() > 0.5 {
        return Ok(()); // What about the other 50%?
    }
    Ok(())
}
```

## Tools for Review

### Building

```bash
# Build the kernel with Rust support
make ARCH=arm64 LLVM=1 rustavailable
make ARCH=arm64 LLVM=1 M=rust
```

### Static Analysis

```bash
# Run clippy
cargo clippy --all-targets

# Run fmt
cargo fmt --check
```

### Testing

```bash
# Run module tests
insmod my_module.ko
dmesg | tail -50
rmmod my_module
```

## References

- [Linux Kernel Patch Submission](https://www.kernel.org/doc/html/latest/process/submitting-patches.html)
- [Rust For Linux Contributing](https://rust-for-linux.com/contributing)
- [Kernel Code of Conduct](https://www.kernel.org/doc/html/latest/process/code-of-conduct.html)
