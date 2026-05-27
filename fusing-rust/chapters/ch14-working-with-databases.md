# Working with Databases

## Core concepts

- **SQL databases**: structured, predefined schema, ACID-compliant, vertical scaling. **SQLite** via `rusqlite`.
- **NoSQL databases**: flexible schema, document-based, horizontal scaling. **MongoDB** via `mongodb` crate.
- **SQLite CRUD**: `INSERT`, `SELECT`, `UPDATE`, `DELETE` via parameterized queries (`?1`, `?2`)
- **Transactions**: `connection.transaction()?`, then `tx.execute()`, `tx.commit()?` — ensure atomicity
- **MongoDB CRUD**: `insert_one()`, `find_one()`, `update_one()`, `delete_one()` via `doc!` macro

## Frameworks introduced

**SQL vs NoSQL decision framework** — Use SQL when schema is stable, relationships matter, and ACID is required. Use NoSQL when schema evolves rapidly, you need horizontal scalability, or data is document-oriented.

## Key techniques

- SQLite connect: `let conn = Connection::open("db.sqlite")?;`
- SQLite insert with params: `conn.execute("INSERT INTO users (name, age) VALUES (?1, ?2)", params![name, age])?;`
- SQLite query: `conn.prepare("SELECT id, name, age FROM users")?.query_map([], |row| { Ok(User { id: row.get(0)?, ... }) })?`
- MongoDB connect: `let client = Client::with_uri_str("mongodb://localhost:27017").await?;`
- MongoDB insert: `collection.insert_one(doc! { "name": "Abhishek", "age": 35 }, None).await?;`

## Code examples

```rust
// SQLite — create table and insert
let conn = Connection::open("my_database.db")?;
conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)", [])?;
conn.execute("INSERT INTO users (name, age) VALUES (?1, ?2)", params!["Alice", 30])?;

// SQLite — query
let mut stmt = conn.prepare("SELECT name, age FROM users")?;
let users = stmt.query_map([], |row| {
    Ok((row.get::<_, String>(0)?, row.get::<_, i32>(1)?))
})?;

// MongoDB — insert document
let collection = database.collection::<Document>("users");
let doc = doc! { "name": "Abhishek", "age": 35 };
collection.insert_one(doc, None).await?;
```

## Connection to other chapters

Database operations use `Result` (Ch6) pervasively. Connecting to MongoDB is async (Ch15 patterns with Tokio). The rusqlite crate demonstrates external dependency management from Ch5.
