# Error Handling

## Core concepts

- Rust splits errors into **recoverable** (`Result<T, E>`) and **unrecoverable** (`panic!`)
- `Result<T, E>` is an enum with variants `Ok(T)` and `Err(E)` — the compiler forces handling
- Common `Result` methods: `is_ok()`, `is_err()`, `unwrap()`, `expect(msg)` — use `expect` over `unwrap` for context
- `panic!` either unwinds (default — walks stack and calls destructors) or aborts (configure with `panic = 'abort'`)
- `RUST_BACKTRACE=1` environment variable prints the full call stack on panic
- `?` operator propagates `Err` early and unwraps `Ok` — the primary ergonomic error handling tool

## Frameworks introduced

**Recoverable vs Unrecoverable distinction** — A design unique to Rust that forces explicit error handling at compile time. Other languages lump all errors into exceptions.

## Key techniques

- Return `Result` from fallible functions
- Use `?` to propagate: `fs::read_to_string(filename)?`
- Use `expect` with context: `parse::<i32>().expect("Failed to parse number")`
- Match on Result: `match result { Ok(val) => val, Err(e) => 0 }`
- Abort on panic: add `[profile.release] panic = 'abort'` to Cargo.toml

## Code examples

```rust
fn area_rectangle(length: f64, width: f64) -> Result<f64, String> {
    if length <= 0.0 || width <= 0.0 {
        return Err(String::from("Invalid dimensions"));
    }
    Ok(length * width)
}

// ? operator — early return on error
fn read_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}
```

## Connection to other chapters

Error handling is pervasive. I/O operations (Ch8), databases (Ch14), and networking (Ch15) all return `Result`. The `?` operator appears in nearly every example from Ch6 onward.
