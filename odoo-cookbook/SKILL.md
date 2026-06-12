---
name: odoo-cookbook
description: "Provides practical recipes for building, extending, and deploying Odoo 19 ERP applications — covering backend models, server-side logic, views, security, OWL frontend, RPC, performance, POS, emails, and IoT."
---

## Core Mental Models

### 1. ORM-First Architecture

**When:** Modeling any business entity or extending existing ones.
**Idea:** Odoo's ORM is the central abstraction — models define fields, relations, constraints, computed values, and security. Views, menus, and controllers are secondary consumers of the model layer.
**Apply:** Start every feature by defining/identifying the model. Add fields, relations, and constraints before building views. Use inheritance (`_inherit`) to extend existing models instead of replacing them.
**Pitfalls:** Avoid `_name = None` delegation inheritance for simple reuse — use `_inherit` with `_name`. Computed fields with `store=True` must have `depends()` decorator or won't recompute. (`→ ch4`)

### 2. Recordset vs. Raw SQL

**When:** Accessing or manipulating data.
**Idea:** Prefer ORM recordsets (search/filtered/mapped) for 90% of operations — they handle security, caching, prefetching, and cross-version compatibility. Reserve raw SQL for bulk operations, complex aggregations, or fields the ORM cannot express.
**Apply:** Use `self.env.cr.execute()` + `self.env[model].search([('id', 'in', ids)])` to re-apply security after SQL. Use `read_group()` for grouped aggregations.
**Pitfalls:** Raw SQL bypasses all ACLs and record rules — always re-filter results through ORM search. After SQL writes, call `self.invalidate_model()` to clear cache. (`→ ch8, ch18`)

### 3. View Inheritance Layer Cake

**When:** Customizing existing backend views without modifying original modules.
**Idea:** Odoo applies view inheritance in ordered passes: expressions can `//` (prepend), replace, `after`, `before`, `attributes`, or remove. The order of evaluation across inherited views is deterministic by module dependency order.
**Apply:** Use `xpath` with `expr` for precision targeting. Use `position="attributes"` to toggle `invisible`, `readonly`, `required`. Prefer `name` attribute matching over generic expressions.
**Pitfalls:** Inherited views are evaluated in module load order — later modules override earlier ones. Multiple inheriting views with the same `inherit_id` can conflict. Always add a `name` to child nodes for debuggability. (`→ ch9`)

### 4. OWL Component Lifecycle

**When:** Building interactive UI elements beyond standard widgets.
**Idea:** OWL follows a strict lifecycle: `setup()` → `willStart()` → `rendered()` → `mounted()` → `willUpdateProps()` → `willPatch()`/`patched()` → `willUnmount()`. State is managed via hooks (`useState`, `useEffect`, `useRef`).
**Apply:** Use `onWillStart` for async data fetching before first render. Use `useState` for reactive local state. Register subcomponents in `static components`. Use `t-out` for safe value interpolation in QWeb templates.
**Pitfalls:** Data fetching in `onWillRender` (every render cycle) causes unnecessary RPC calls. Never mutate `state` directly — always replace. Props are read-only from the child's perspective. (`→ ch15`)

### 5. Security Layering

**When:** Controlling access to features, data, and UI elements.
**Idea:** Odoo security has 5 independent layers that compose: (1) menu visibility by group, (2) model ACLs (CRUD per group), (3) field-level `groups` attribute, (4) record rules (domain filters per group), (5) view element `groups` attribute.
**Apply:** Define groups in `security/groups.xml` first, then ACLs in `ir.model.access.csv`, then record rules. Add `groups="..."` attributes to menus and view elements. Use `sudo()` sparingly — only for internal cross-model operations.
**Pitfalls:** Superuser bypasses ALL layers except `groups` on view elements. Admin does NOT auto-get ACLs — they must be defined. `sudo()` bypasses record rules — risk of data leakage. (`→ ch10`)

## Query Routing

| When user asks...                                         | Load |
| --------------------------------------------------------- | ---- |
| "Install Odoo / set up dev environment"                   | ch1  |
| "Create a module / scaffold / manifest"                   | ch3  |
| "Define models / fields / relations / inheritance"        | ch4  |
| "Server-side logic / recordsets / search / CRUD"          | ch5  |
| "Data files / XML / CSV / noupdate / migration"           | ch6  |
| "Debug / shell / profiler / logs"                         | ch7  |
| "Wizards / onchange / SQL views / settings"               | ch8  |
| "Backend views / form / list / kanban / search / inherit" | ch9  |
| "Security / groups / ACLs / record rules"                 | ch10 |
| "Internationalization / translations"                     | ch11 |
| "Automation / workflows / reports / stat buttons"         | ch12 |
| "Web controllers / routes / REST API"                     | ch13 |
| "Web client / custom widgets / QWeb / tours"              | ch14 |
| "OWL components / hooks / lifecycle"                      | ch15 |
| "Testing / Python tests / HOOT / tours"                   | ch16 |
| "RPC / XML-RPC / JSON-RPC / REST / API keys"              | ch17 |
| "Performance / profiling / caching / bulk ops"            | ch18 |
| "Point of Sale / POS customization"                       | ch19 |
| "Email / chatter / templates / aliases"                   | ch20 |
| "IoT Box / Raspberry Pi / printers"                       | ch21 |

## Reference Files

- `chapters/chN.md` — One file per chapter with core ideas, frameworks, techniques, trade-offs
- `glossary.md` — Key Odoo terms with chapter backlinks
- `patterns.md` — Design patterns, techniques, and anti-patterns
- `cheatsheet.md` — Decision tables for quick reference
