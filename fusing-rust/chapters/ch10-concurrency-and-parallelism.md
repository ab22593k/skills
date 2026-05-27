# Concurrency and Parallelism

## Core concepts

- **`thread::spawn`** creates a new OS thread. Returns a `JoinHandle`. Call `.join()` to wait for completion.
- **`Mutex<T>`** provides mutual exclusion. `lock()` returns a `MutexGuard` that automatically unlocks on drop.
- **Channels** (`mpsc`) enable message-passing concurrency. Multi-Producer, Single-Consumer. `sender.send()`, `receiver.recv()`.
- **`Arc<T>`** (Atomic Reference Counting) enables shared ownership across threads. Combine with `Mutex` for shared mutable state.
- **`Send` trait** — types safe to transfer across threads. Most types implement it automatically.
- **`Sync` trait** — types safe to share references across threads. `Mutex<T>` is Sync; `RefCell<T>` is not.

## Frameworks introduced

**Message-passing vs shared-state concurrency** — Message-passing (channels) transfers data between threads. Shared-state (`Arc<Mutex<T>>`) gives threads access to the same data. Rust supports both; the ownership system prevents data races at compile time even in shared-state mode.

## Key techniques

- Spawn thread: `thread::spawn(move || { /* use captured data */ })`
- Channel: `let (tx, rx) = mpsc::channel(); tx.send(val)?; rx.recv()?`
- Shared counter: `let counter = Arc::new(Mutex::new(0))`
- Lock: `let mut num = counter.lock().unwrap(); *num += 1;`

## Code examples

```rust
// Message-passing
let (tx, rx) = mpsc::channel();
thread::spawn(move || {
    tx.send(String::from("hello")).unwrap();
});
let received = rx.recv().unwrap();

// Shared-state
let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];
for _ in 0..5 {
    let c = Arc::clone(&counter);
    handles.push(thread::spawn(move || {
        let mut num = c.lock().unwrap();
        *num += 1;
    }));
}
```

## Connection to other chapters

Concurrency relies on ownership (Ch3) — `Send` and `Sync` are unsafe traits (Ch16) at their foundation. Arc is a generic container (Ch7). Async networking with Tokio (Ch15) builds on thread concepts.
