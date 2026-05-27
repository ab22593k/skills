# Processes and Signal Handling

## Core concepts

- **`std::process::Command`** spawns and manages child processes — configure args, environment, stdio
- **`Child`** represents a running child process. Use `.wait()` or `.wait_with_output()` to synchronize.
- **Environment variables**: `std::env::var("HOME")` reads, `std::env::set_var("K", "V")` writes
- **Standard streams**: stdin (read from child), stdout (capture output), stderr (capture errors)
- **Signals** are async OS notifications. The `nix` crate handles them: `signal::signal(Signal::SIGINT, handler)`
- **Error propagation**: `?` operator with `Result` for clean fallible code

## Frameworks introduced

**Process lifecycle management** — A process goes through: creation → configuration → spawning → I/O interaction → waiting/termination. Rust's `Command` API models each phase explicitly.

## Key techniques

- Spawn and capture: `let output = Command::new("ls").arg("-l").output()?;`
- Spawn detached: `let child = Command::new("sleep").arg("5").spawn()?;`
- Pipe stdin: `.stdin(Stdio::piped())` then write to `child.stdin.take().unwrap()`
- Get PID: `std::process::id()`, `child.id()`
- Signal handler (nix): `extern "C" fn handler(_: i32) {}` then `signal::signal(Signal::SIGINT, SigHandler::Handler(handler))?;`
- Basic shell loop: `loop { print!("> "); read input; execute_command(input); }`

## Code examples

```rust
// Spawn and capture output
let output = Command::new("echo")
    .arg("Hello from Rust")
    .stdout(Stdio::piped())
    .output()?;
println!("stdout: {}", String::from_utf8_lossy(&output.stdout));

// Basic shell program
fn main() {
    loop {
        print!("> ");
        io::stdout().flush().unwrap();
        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        let input = input.trim();
        if input == "exit" { break; }
        let output = Command::new("sh").arg("-c").arg(input).output().unwrap();
        print!("{}", String::from_utf8_lossy(&output.stdout));
    }
}
```

## Connection to other chapters

Process management uses `Result` (Ch6), file I/O patterns (Ch8), and terminal output (Ch12). Signal handling connects to FFI (Ch17) via `extern "C"` handlers.
