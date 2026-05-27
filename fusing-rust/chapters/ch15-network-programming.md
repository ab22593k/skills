# Network Programming

## Core concepts

- **`std::net::TcpListener`** binds to an address, accepts incoming connections. **`TcpStream`** represents a TCP connection.
- **`UdpSocket`** connectionless — use `send_to` and `recv_from` for datagram communication
- **TCP flow**: Server creates `TcpListener`, accepts connections in a loop. Client creates `TcpStream` and connects.
- **UDP flow**: Both sides bind a socket. Server `recv_from`, client `send_to`.
- **Tokio** provides async I/O: `tokio::net::TcpListener`, `.accept().await`, `tokio::spawn`
- **DNS resolution**: `(hostname, port).to_socket_addrs()` — resolves to IP addresses

## Frameworks introduced

**TCP vs UDP decision** — TCP: connection-oriented, reliable, ordered. Use for web servers, APIs, databases. UDP: connectionless, faster, unreliable. Use for streaming, gaming, DNS, real-time protocols.

**Async networking with Tokio** — Event-driven I/O that handles thousands of connections without one OS thread per connection. `.await` yields control when waiting for I/O.

## Key techniques

- TCP bind: `TcpListener::bind("127.0.0.1:8080")?`
- Accept loop: `for stream in listener.incoming() { let stream = stream?; }`
- Spawn per connection: `thread::spawn(|| handle_client(stream))`
- UDP send: `socket.send_to(b"Hello", "127.0.0.1:8888")?`
- UDP recv: `socket.recv_from(&mut buffer)?`
- Tokio TCP: `let listener = TcpListener::bind("127.0.0.1:8080").await?;`
- DNS: `let addrs = ("example.com", 80).to_socket_addrs()?;`

## Code examples

```rust
// TCP echo server
let listener = TcpListener::bind("127.0.0.1:8080")?;
for stream in listener.incoming() {
    let mut stream = stream?;
    thread::spawn(move || {
        let mut buffer = [0; 1024];
        stream.read(&mut buffer).unwrap();
        stream.write_all(&buffer).unwrap();
    });
}

// UDP server
let socket = UdpSocket::bind("127.0.0.1:8888")?;
let mut buf = [0; 1024];
let (amt, src) = socket.recv_from(&mut buf)?;
socket.send_to(&buf[..amt], src)?;
```

## Connection to other chapters

Network programming uses `Result` (Ch6) and threads (Ch10). FFI (Ch17) could wrap native socket libraries. WASM (Ch19) brings Rust networking to browsers.
