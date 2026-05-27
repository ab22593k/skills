# Working with File Systems

## Core concepts

- `std::fs` wraps Linux system calls (`open`, `read`, `write`, `chmod`, `link`, `symlink`) for safe file I/O
- **File I/O**: `File::create()`, `File::open()`, `read_to_string()`, `write_all()`
- **Directory operations**: `create_dir()`, `create_dir_all()`, `remove_dir()`, `remove_dir_all()`, `rename()`, `read_dir()`
- **Path types**: `Path` (immutable borrowed) and `PathBuf` (owned mutable) — platform-independent path manipulation
- **Hard links** share the same inode; **symbolic links** point to a path
- **Metadata queries**: size, permissions, timestamps, ownership, type, existence, disk space

## Frameworks introduced

**BufReader/BufWriter buffering pattern** — Wraps a reader/writer with an internal buffer to reduce system call frequency. Dramatically improves I/O throughput for many small reads/writes.

## Key techniques

- Read entire file: `fs::read_to_string("file.txt")?`
- Write to file: `file.write_all(b"Hello")`
- Recursive directory creation: `fs::create_dir_all("a/b/c")?`
- Iterate directory: `for entry in fs::read_dir(".")? { let entry = entry?; }`
- Check metadata: `fs::metadata("file.txt")?.len()`
- Create symlink: `fs::symlink("original", "link")` (Unix)
- Path joining: `Path::new("/tmp").join("file.txt")`

## Code examples

```rust
// Read file
let mut file = File::open("example.txt")?;
let mut contents = String::new();
file.read_to_string(&mut contents)?;

// Directory operations
fs::create_dir_all("tmp/my/nested/directory")?;
fs::rename("mydir", "newdir")?;
for entry in fs::read_dir(".")? {
    println!("{:?}", entry?.path());
}

// File metadata
let meta = fs::metadata("example.txt")?;
println!("size: {}, created: {:?}", meta.len(), meta.created()?);
```

## Connection to other chapters

File I/O uses `Result` (Ch6) extensively. Directory walking connects to text processing (Ch9). Device file interaction (Ch11) extends similar patterns to hardware.
