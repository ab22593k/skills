# Glossary

**Arc (Atomic Reference Counting)** — Thread-safe shared ownership via reference counting. Use `Arc::clone()` to increment the count. Combined with `Mutex` for shared mutable state across threads. (Ch10)

**associated function** — A function defined on a type with `impl` that doesn't take `self`. Called with `::` syntax (e.g., `String::from("hello")`). (Ch4)

**backtrace** — Stack trace printed on panic when `RUST_BACKTRACE=1` is set. Shows the call chain leading to the unrecoverable error. (Ch6)

**borrowing** — Creating a reference (`&T` or `&mut T`) to access data without taking ownership. References don't drop the underlying value when they go out of scope. (Ch3)

**cargo** — Rust's package manager and build system. Commands: `new`, `build`, `run`, `check`, `test`, `bench`, `clean`. (Ch1)

**crate** — A compilation unit — either a binary crate (executable) or a library crate (`.rlib`). (Ch5)

**CString** — A C-compatible, null-terminated string for safe FFI string exchange. Created with `CString::new("text")`. (Ch17)

**device file** — A special file in `/dev` representing a hardware device. Read/written with the same `File` API as regular files. (Ch11)

**enum** — A type that can be one of several named variants. `Option<T>` and `Result<T, E>` are the most common. (Ch4)

**extern "C"** — ABI specification for FFI. Declares that a function uses the C calling convention, enabling cross-language calls. (Ch17)

**FFI (Foreign Function Interface)** — Mechanism to call functions written in other languages (typically C/C++) from Rust, and vice versa. (Ch17)

**generics** — Type parameters `<T>` that allow functions, structs, enums, and methods to operate on many types. Monomorphized at compile time — zero runtime cost. (Ch7)

**HAL (Hardware Abstraction Layer)** — A portability layer that provides a uniform API for microcontroller peripherals (GPIO, timers, UART, ADC) across different hardware. (Ch18)

**Mutex** — Mutual exclusion primitive. `lock()` returns a `MutexGuard` that unlocks on drop. Only one thread can hold the lock at a time. (Ch10)

**move** — Transfer of ownership from one binding to another. The source binding is invalidated. Default for heap-allocated types like `String` and `Vec`. (Ch3)

**module** — An organizational unit within a crate. Declared with `mod`, made public with `pub`. Modules form a tree: `crate::module::submodule::item`. (Ch5)

**`#[no_mangle]`** — Attribute that prevents Rust from name-mangling a symbol, required for exported FFI functions so other languages can find them by name. (Ch17)

**ownership** — Rust's core memory management model: every value has exactly one owner, and memory is freed when the owner goes out of scope. No garbage collector needed. (Ch3)

**panic!** — Macro for unrecoverable errors. By default unwinds the stack (calling destructors). Can be changed to abort with `panic = 'abort'` in Cargo.toml. (Ch6)

**Path / PathBuf** — Platform-independent path types. `Path` is an immutable borrowed slice; `PathBuf` is an owned, mutable path. Created with `Path::new()` / `PathBuf::from()`. (Ch8)

**raw pointer** — `*const T` (immutable) or `*mut T` (mutable) pointer that bypasses Rust's ownership and borrowing rules. Dereferencing requires `unsafe`. (Ch16)

**reference** — A non-owning pointer to a value. Immutable (`&T`) — many allowed simultaneously. Mutable (`&mut T`) — exclusive access required. (Ch3)

**`#[repr(C)]`** — Attribute that lays out a struct's fields in C-compatible order, ensuring binary compatibility across FFI boundaries. (Ch17)

**Result** — Enum with variants `Ok(T)` (success) and `Err(E)` (failure). Used for recoverable errors. Propagated with the `?` operator. (Ch6)

**Rhai** — An embedded scripting language for Rust with JavaScript-like syntax. Scripts run via `Engine::eval()` or `Engine::eval_file()`. (Ch20)

**rustup** — The Rust toolchain installer and version manager. Installs `rustc`, `cargo`, `rustdoc`, and cross-compilation targets. (Ch1)

**Send** — Unsafe marker trait: types that implement `Send` can be transferred across threads safely. Auto-implemented for most types. (Ch10)

**slice** — A reference (`&[T]` or `&str`) to a contiguous sequence of elements. Created with range syntax: `&collection[start..end]`. (Ch3)

**struct** — A named grouping of typed fields. Can have methods via `impl` blocks. Supports field init shorthand and update syntax. (Ch4)

**Sync** — Unsafe marker trait: types that implement `Sync` can be shared (via reference) across threads safely. `Mutex<T>` implements Sync; `RefCell<T>` does not. (Ch10)

**trait** — A collection of method signatures that types can implement. Similar to interfaces in Java. Supports default method implementations. (Ch7)

**tuple struct** — A named tuple with positional, un-named fields. Useful for newtype patterns. `struct Point3D(i32, i32, i32);`. (Ch4)

**Unicode** — Rust's default text encoding. Every `char` is a 32-bit Unicode scalar value. Strings are UTF-8 encoded by default. (Ch9)

**unsafe** — Keyword that enables raw pointer dereference, unsafe functions, mutable statics, unsafe traits, and union field access. Responsibility for safety shifts to the programmer. (Ch16)

**Wasm (WebAssembly)** — Binary instruction format for near-native execution in web browsers. Rust compiles to Wasm via `wasm-pack` and `wasm-bindgen`. (Ch19)
