# Device Input/Output Handling

## Core concepts

- Device files in `/dev` (Linux/Unix) represent hardware — `open`, `read`, `write`, `close` treat them like regular files
- **Buffered I/O**: `BufReader` wraps a reader with an internal buffer; `BufWriter` buffers writes before flushing
- **Standard streams**: `std::io::Stdin`, `Stdout`, `Stderr` for terminal interaction
- **USB detection**: `rusb` crate provides `Context`, `DeviceList`, and `DeviceDescriptor` for USB subsystem interaction
- Error handling with `Result<T, E>` and `?` operator

## Frameworks introduced

**File-as-device abstraction** — Unix treats hardware devices as files. Same API (`File::open`, `read`, `write`) works for regular files, `/dev/tty`, `/dev/lp0`, and input event devices.

## Key techniques

- Read from device: `File::open("/dev/input/event0")?; file.read(&mut buffer)?;`
- Write to device: `File::create("/dev/lp0")?; file.write_all(data)?;`
- Buffered reading: `BufReader::new(file).lines()`
- Buffered writing: `BufWriter::new(file); writeln!(writer, "line")`
- stdin/stdout: `io::stdin().read_line(&mut input)?; io::stdout().write_all(msg.as_bytes())?;`
- USB discovery: `let context = rusb::Context::new()?; for device in context.devices()?.iter() { ... }`

## Code examples

```rust
// Buffered file reading
let file = File::open("data.txt")?;
let reader = BufReader::new(file);
for line in reader.lines() {
    println!("{}", line?);
}

// USB device detection
let context = Context::new()?;
for device in context.devices()?.iter() {
    let desc = device.device_descriptor()?;
    println!("Vendor: {:04x}, Product: {:04x}", desc.vendor_id(), desc.product_id());
}
```

## Connection to other chapters

Device I/O extends file I/O patterns (Ch8) to hardware. BufReader/BufWriter appear in Ch8 for files and Ch12 for terminals.
