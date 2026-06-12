# Glossary

**ACL (Access Control List)** — CSV file defining `perm_read/write/create/unlink` per model per group. (`→ ch10`)

**Add-ons path** — Comma-separated directories Odoo scans for modules. (`→ ch2`)

**Chatter** — Threaded message log and activity feed from `mail.thread` mixin. (`→ ch20`)

**Computed field** — Field whose value is computed via `@api.depends` decorator. Optionally `store=True` for persistence. (`→ ch4`)

**Context** — Dictionary (`self.env.context`) carrying session metadata (active IDs, default values, language, company). (`→ ch9`)

**Controller** — Python class inheriting `odoo.http.Controller` with `@http.route()` decorated methods. (`→ ch13`)

**Domain** — List of filter tuples `[('field', 'operator', value)]` used in `search()` and view filters. (`→ ch9`)

**External ID (XML ID)** — Globally unique record identifier (`module.record_id`). Used for data references across modules. (`→ ch6`)

**HOOT** — Headless Odoo Testing framework for client-side JavaScript tests. (`→ ch16`)

**Inheritance (view)** — `<field name="inherit_id" ref="parent"/>` + `<xpath>` to modify existing views. (`→ ch9`)

**IoT Box** — Raspberry Pi-based device connecting POS peripherals to Odoo (printers, scales, scanners). Enterprise-only. (`→ ch21`)

**Manifest** — `__manifest__.py` dictionary with module metadata: name, version, depends, data, assets. (`→ ch3`)

**Monetary field** — Financial field type requiring companion `currency_id` Many2one to `res.currency`. (`→ ch4`)

**OCA** — Odoo Community Association: non-profit hosting community modules, migration tools, accounting localizations. (`→ ch1`)

**ORM** — Odoo's Object-Relational Mapping layer. Central abstraction for model definition, CRUD, security, caching. (`→ ch4, ch5`)

**ORM cache (ormcache)** — `@tools.ormcache` decorator: LRU in-memory cache keyed by method arguments. (`→ ch18`)

**OWL** — Odoo Web Library: Odoo's component-based JavaScript framework for reactive UI. (`→ ch15`)

**Prefetching** — ORM fetches all fields for all records on first field access (O(1) queries vs O(n)). (`→ ch18`)

**Record rule** — Domain-based access filter per security group. `domain_force` on `ir.rule`. (`→ ch10`)

**Recordset** — Ordered collection of ORM records. Methods: `search()`, `filtered()`, `mapped()`, `sorted()`. (`→ ch5`)

**Runbot** — Odoo's automated testing environment at `runbot.odoo.com`. Green = tests pass. (`→ ch1`)

**Scaffold** — `odoo-bin scaffold <name> <path>` — generates module skeleton. (`→ ch3`)

**Server action** — Configurable action (Python code, email, create, write) triggerable from automation rules or menus. (`→ ch12`)

**Settings (res.config.settings)** — Configuration model with `group_`, `module_`, `default_` field prefixes. (`→ ch8`)

**Stat button** — `<button type="object" class="oe_stat_button">` showing aggregate counts on form headers. (`→ ch12`)

**TransientModel** — SQL-backed temporary model for wizard dialogs. Auto-cleaned periodically. (`→ ch8`)

**View inheritance** — Mechanism to modify existing view XML via `inherit_id` + `xpath`. Positions: `after`, `before`, `replace`, `attributes`, `inside`, `//`. (`→ ch9`)

**Wizard** — Multi-step form dialog using `TransientModel`. (`→ ch8`)

**XML-RPC/JSON-RPC** — Deprecated external APIs for remote Odoo access. Scheduled for removal in Odoo 22. (`→ ch17`)
