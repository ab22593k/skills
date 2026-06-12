---
chapter: 7
topic: "Debugging Modules"
when: "User encounters bugs, needs to debug with shell, logger, or pdb"
queries:
  [
    "debug module",
    "odoo shell",
    "python debugger",
    "server log",
    "auto reload",
    "dev options",
  ]
---

## Core Concepts

- **`--dev all`**: Enables auto-reload, QWeb debugging, asset recompilation, XML validation. Use during active development.
- **Logging**: `import logging; _logger = logging.getLogger(__name__); _logger.info/warning/error/debug(msg)`.
- **Odoo shell**: `odoo-bin shell -d <db>` — interactive Python with full ORM access on `self.env`.

## Techniques

- **pdb**: Insert `import pdb; pdb.set_trace()` or `breakpoint()` in any method. Run Odoo with stdin for interactive debugging.
- **`--dev xml`**: Validates XML views on load — catches syntax errors early.
- **Debug mode options**: `?debug=1` (developer tools), `?debug=assets` (force asset recompile), `?debug=tests` (test details).
- **Profiler**: Built-in profiling at Technical → Profiling. Use to find SQL queries, time-per-request, memory usage.

## Pitfalls

- Server actions with Python code cannot be debugged with breakpoints — only logging works. (`→ ch12`)
- Auto-reload may not detect changes in new files — restart if new files aren't picked up.
