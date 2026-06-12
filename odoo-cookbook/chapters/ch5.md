---
chapter: 5
topic: "Basic Server-Side Development"
when: "User needs to implement business logic, search/filter records, CRUD operations"
queries:
  [
    "recordset",
    "search",
    "filtered",
    "mapped",
    "create write",
    "api decorator",
    "recordset operators",
  ]
---

## Core Concepts

- **API decorators**: `@api.model` (static-like, no recordset), `@api.depends` (computed fields), `@api.constrains` (validation), `@api.onchange` (form interaction), `@api.returns` (return type hint).
- **Environment**: `self.env` gives access to `cr` (cursor), `uid` (user), `context`, `company`, `lang`. `self.env['res.partner']` fetches a model's empty recordset.

## Techniques

- **Search**: `model.search([('field', 'operator', value)], offset=0, limit=N, order='field desc', count=True)`. Default operator is `&` (AND).
- **Create**: `model.create({'field': value, 'line_ids': [(0, 0, {...})]})` — returns new recordset.
- **Write**: `record.field = value` (single) or `record.write({'field': value})` (batch). `record.update({...})` for multi-field on single record.
- **Recordset operators**: `+` (concat), `|` (union), `&` (intersection), `-` (difference). Use `|=` for O2M/M2M field updates.
- **Filtered**: `records.filtered(lambda r: r.field > 5)` — in-memory. Use `filtered('field_name')` for truthy check.
- **Mapped**: `records.mapped('partner_id.name')` — traverses dot-separated paths. Returns recordset if last is relational, else list.
- **Extend logic**: Override `create()` or `write()` — call `super().create(vals)` / `super().write(vals)` then add custom logic.
- **Read group**: `read_group(domain, fields, groupby, offset, limit, orderby)` — SQL GROUP BY aggregation.

## Pitfalls

- `filtered()` and `mapped()` operate in-memory — use `search()` with domain for large datasets.
- `mapped()` with dot-paths deduplicates and loses order for relational paths.
- Overriding `create()/write()` without calling `super()` breaks field computation and ORM invariants.
