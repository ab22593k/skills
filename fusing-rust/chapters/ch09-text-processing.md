# Text Processing

## Core concepts

- **`String`** — owned, growable, heap-allocated UTF-8 buffer. Use for dynamic text.
- **`&str`** — borrowed, immutable string slice. Usually a view into a `String` or string literal.
- Rust uses **UTF-8** encoding by default. The `char` type is a 32-bit Unicode scalar value.
- `println!` prints to stdout; `format!` creates a `String` without printing.
- **Pattern matching** with `match` handles integers, enums, tuples, ranges (`2..=9`), and catch-all `_`.

## Frameworks introduced

**String vs &str duality** — `&str` is the "view" type for text; `String` is the "owned" type. Functions should accept `&str` for flexibility (accepts both `&String` and `&str`).

## Key techniques

- Create String: `String::from("text")`, `"text".to_string()`
- Build string: `let mut s = String::new(); s.push_str("hello")`
- Concatenate: `format!("{} {}", a, b)`, or `s1 + &s2`
- Unicode support: `char::from_u32(0x1F600)` — any emoji
- Text ops: `.split(" ")`, `.replace("old", "new")`, `.to_uppercase()`, `.trim()`, `.lines()`
- Pattern matching:
  ```rust
  match value {
      1 => println!("one"),
      2..=9 => println!("two through nine"),
      _ => println!("everything else"),
  }
  ```

## Code examples

```rust
fn main() {
    let hello = String::from("Hello, 세계 !");
    println!("{}", hello);

    let text = "The brown fox jumps";
    let words: Vec<&str> = text.split(" ").collect();
    let replaced = text.replace("brown", "red");
    println!("{}", replaced.to_uppercase()); // "THE RED FOX JUMPS"

    // Pattern matching
    let direction = Direction::East;
    match direction {
        Direction::North => println!("N"),
        Direction::South => println!("S"),
        _ => println!("Other"),
    }
}
```

## Connection to other chapters

Text processing builds on String from Ch4 and is essential for building CLI tools (Ch12), shell programs (Ch13), and parsing database queries (Ch14).
