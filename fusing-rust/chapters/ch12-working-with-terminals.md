# Working with Terminals

## Core concepts

- Terminal I/O = reading keyboard input + writing formatted output
- **`crossterm`** and **`termion`** abstract terminal control sequences (cursor positioning, colors, clearing)
- **Raw mode** (`terminal::enable_raw_mode()`) captures individual keypresses without waiting for Enter
- **`tui-rs`** provides pre-built widgets: `Block`, `Table`, `Layout`, `Row`, `Cell`, `Paragraph`
- **Focus management** enables keyboard navigation between UI elements
- Mouse events handled via `crossterm::event::read()` with `MouseEventKind::Down`, `Up`, `Drag`

## Frameworks introduced

**Terminal as UI canvas** — Beyond simple text output, terminals support precise cursor positioning, 16M colors, mouse tracking, and widget-based layouts — making them viable for rich interactive applications.

## Key techniques

- Cursor movement: `execute!(stdout, MoveTo(col, row))`
- Text styling: `"Hello".with(Color::Red).on(Color::Cyan).attribute(Attribute::Bold)`
- Raw mode + key reading: `terminal::enable_raw_mode(); let event = crossterm::event::read()?;`
- TUI table: `Table::new(rows).block(Block::default().borders(Borders::ALL)).widths(&[Constraint::Percentage(50), Constraint::Percentage(50)])`

## Code examples

```rust
use crossterm::{execute, style::*, cursor::MoveTo};
execute!(
    stdout,
    MoveTo(20, 10),
    SetForegroundColor(Color::Yellow),
    Print("Hello styled terminal!")
)?;

// Raw mode keyboard input
terminal::enable_raw_mode()?;
loop {
    match crossterm::event::read()? {
        Event::Key(KeyEvent { code: KeyCode::Char('q'), .. }) => break,
        Event::Mouse(MouseEvent { kind: MouseEventKind::Down(MouseButton::Left), .. }) => { /* handle click */ },
        _ => {}
    }
}
```

## Connection to other chapters

Terminal I/O builds on device I/O (Ch11) and stdio (Ch13). The shell program in Ch13 uses terminal output extensively.
