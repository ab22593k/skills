# Structs, Enums, and Collections

## Core concepts

- **Structs** group named fields of potentially different types. Define with `struct`, instantiate with named fields.
- **Field init shorthand** — omit `field: field` when parameter and field names match.
- **Struct update syntax** — `..other_instance` copies remaining fields from an existing instance.
- **Tuple structs** — named tuples with positional fields, no field names. Useful for newtype patterns.
- **Enums** define a type with a fixed set of named variants. `Option<T>` is the most common.
- **`match`** is exhaustive pattern matching on enums and other types.
- **Collections**: `Vec<T>` (dynamic array), `HashMap<K, V>` (key-value store), `String` (growable UTF-8 text).

## Frameworks introduced

**The Option type** — `Option<T>` has variants `Some(T)` and `None`. Replaces null pointers from other languages. The compiler forces you to handle both cases.

## Key techniques

- Define a struct: `struct Student { name: String, age: u8 }`
- Instantiate with shorthand: `Student { name, age: 20 }`
- Update syntax: `let s2 = Student { name: String::from("Vijay"), ..student1 };`
- Match on enum:
  ```rust
  match direction {
      Direction::North => println!("N"),
      Direction::South => println!("S"),
  }
  ```
- Vector operations: `vec.push(4)`, `vec[0]`, `vec.get(1)`
- HashMap: `map.insert(key, val)`, `map.get(&key)`, `map.remove(&key)`

## Code examples

```rust
struct Student { name: String, id: String, age: u8, class: u8 }

fn create_student(name: String, id: String) -> Student {
    Student { name, id, age: 20, class: 10 }  // field init shorthand
}

// Enum with match
enum Direction { North, South, East, West }
fn move_avatar(dir: Direction) {
    match dir {
        Direction::North => println!("Moving north"),
        _ => println!("Other direction"),
    }
}
```

## Connection to other chapters

Structs and enums are the building blocks for all Rust data modeling. Traits (Ch7) add behavior to structs. Error handling (Ch6) uses `Result<T, E>` which is an enum.
