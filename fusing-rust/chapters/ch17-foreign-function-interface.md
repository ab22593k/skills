# Foreign Function Interface

## Core concepts

- **`extern "C"`** declares functions defined in another language using the C ABI
- **`#[no_mangle]`** prevents the Rust compiler from name-mangling exported symbols
- **`#[repr(C)]`** ensures struct memory layout matches C's expectations
- **`CString`** and `CStr` safely convert between Rust strings and C null-terminated strings
- **`crate-type = ["cdylib"]`** in Cargo.toml produces a dynamic library (.so/.dylib/.dll)
- **`build.rs`** compiles and links external C/C++ libraries during the build process

## Frameworks introduced

**Safe FFI boundary pattern** — Keep `unsafe extern "C"` functions minimal. Create safe Rust wrappers that validate inputs before calling the FFI boundary. Never expose raw pointers in the safe public API.

## Key techniques

- Call C from Rust: `extern "C" { fn add_numbers(x: i32, y: i32) -> i32; }`
- Call Rust from C: `#[no_mangle] pub extern "C" fn add(a: i32, b: i32) -> i32 { a + b }`
- Pass strings: `CString::new("hello")?.into_raw()` for C; `CStr::from_ptr(ptr).to_str()?` from C
- Pass structs: `#[repr(C)] struct MyStruct { x: c_int, y: c_int }`
- Pass arrays: `std::slice::from_raw_parts(ptr, len)` converts C array to Rust slice
- Callbacks: `extern "C" fn callback(result: i32) { }` passed as function pointer to C
- Link C code: compile to `.so`, reference in `build.rs`, call via `extern "C"`

## Code examples

```rust
// Calling C from Rust
extern "C" {
    fn add_numbers(x: i32, y: i32) -> i32;
    static EXTERN_VAL: i32;
}
unsafe {
    println!("{}", add_numbers(5, 3));
    println!("{}", EXTERN_VAL);
}

// Exposing Rust to C
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}

// Cargo.toml
// [lib]
// crate-type = ["cdylib"]
```

## Connection to other chapters

FFI always uses `unsafe` (Ch16) for external function calls and pointer dereferencing. Embedded Rust (Ch18) uses FFI for AVR-Libc. WASM (Ch19) uses `extern "C"` conventions.
