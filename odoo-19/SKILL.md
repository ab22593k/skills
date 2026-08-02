---
name: odoo-19
description: >-
  Odoo 19 development knowledge base with 18 specialized guides, a systematic
  methodology for reverse-engineering Odoo's core codebase, and odoomcp — the
  Odoo MCP server (https://gitmcp.io/odoo/odoo, serving the 19.0 branch) that
  gives agents narrow, purpose-built source-access tools (search_odoo_code,
  fetch_odoo_documentation, search_odoo_documentation) instead of exposing raw
  database queries. Covers all Odoo 19 API patterns — Actions (ir.actions.*,
  cron jobs, server actions), Controllers (HTTP routing, endpoints, auth
  types), Data files (XML/CSV records, shortcuts, noupdate), API Decorators
  (@api.depends, @api.constrains, @api.ondelete, @api.onchange, @api.model,
  @api.private), SQL Constraints (models.Constraint replacing
  _sql_constraints), Database Indexes (models.Index), Module development
  (manifest, wizards, reports), Field types (Char, Text, Monetary, relational
  fields), Manifest configuration (__manifest__.py, dependencies, asset
  bundles), Mixins (mail.thread, mail.activity.mixin, mail.alias.mixin,
  utm.mixin), ORM Model methods (search, CRUD, domain filters, recordsets,
  CamelCase model naming), Migration scripts (pre/post/end hooks, data
  migration), OWL frontend components (hooks, services, lifecycle),
  Performance optimization (N+1 prevention, batch ops, _read_group), QWeb
  Reports (PDF/HTML, paper formats, barcodes, t-out), Security/ACL (record
  rules, field permissions, privilege-based groups, @api.private), Testing
  (TransactionCase, HttpCase, mocking, query count assertions), Transactions
  (savepoints, UniqueViolation, serialization failures), Translations (i18n,
  PO files, translatable fields), XML Views (list/form/search, kanban card
  templates, xpath inheritance, QWeb templates). Use whenever writing,
  reviewing, or debugging any Odoo 19 Python or XML code, creating or
  modifying modules, fixing performance issues, looking up API patterns, OR
  when you need to verify behavior against Odoo's real 19.0 source. ALWAYS
  prefer the actual source over guessing — reach it via the odoomcp MCP server
  (search_odoo_code) when available, else fetch raw files from the 19.0 branch.
  Framework code lives in odoo/orm/models.py, odoo/orm/fields.py,
  odoo/orm/decorators.py, odoo/addons/base/, and the addons/ directory.
---

# Odoo 19 Skill - Master Index

Master index for all Odoo 19 development guides. Read the appropriate guide from `references/` based on your task.

## Quick Reference

| Topic          | File                                      | When to Use                                             |
| -------------- | ----------------------------------------- | ------------------------------------------------------- |
| Actions        | `references/odoo-19-actions-guide.md`     | Creating actions, menus, scheduled jobs, server actions |
| API Decorators | `references/odoo-19-decorator-guide.md`   | Using @api decorators, compute fields, validation       |
| Controllers    | `references/odoo-19-controller-guide.md`  | Writing HTTP endpoints, routes, web controllers         |
| Data Files     | `references/odoo-19-data-guide.md`        | XML/CSV data files, records, shortcuts                  |
| Development    | `references/odoo-19-development-guide.md` | Creating modules, manifest, reports, security, wizards  |
| Field Types    | `references/odoo-19-field-guide.md`       | Defining model fields, choosing field types             |
| Manifest       | `references/odoo-19-manifest-guide.md`    | **manifest**.py configuration, dependencies, hooks      |
| Migration      | `references/odoo-19-migration-guide.md`   | Upgrading modules, data migration, version changes      |
| Mixins         | `references/odoo-19-mixins-guide.md`      | mail.thread, activities, email aliases, tracking        |
| Model Methods  | `references/odoo-19-model-guide.md`       | Writing ORM queries, CRUD operations, domain filters    |
| OWL Components | `references/odoo-19-owl-guide.md`         | Building OWL UI components, hooks, services             |
| Performance    | `references/odoo-19-performance-guide.md` | Optimizing queries, fixing slow code, preventing N+1    |
| Reports        | `references/odoo-19-reports-guide.md`     | QWeb reports, PDF/HTML, templates, paper formats        |
| Security       | `references/odoo-19-security-guide.md`    | Access rights, record rules, field permissions          |
| Testing        | `references/odoo-19-testing-guide.md`     | Writing tests, mocking, assertions, browser testing     |
| Transactions   | `references/odoo-19-transaction-guide.md` | Handling database errors, savepoints, UniqueViolation   |
| Translation    | `references/odoo-19-translation-guide.md` | Adding translations, localization, i18n                 |
| Views & XML    | `references/odoo-19-view-guide.md`        | Writing XML views, actions, menus, QWeb templates       |
| odoomcp        | `references/odoo-19-mcp-guide.md`         | Source-grounding with the Odoo MCP server               |

## Odoo Source Access via odoomcp (MCP)

Ground every non-trivial answer in Odoo's **actual 19.0 source**. The curated
guides are summaries; the source is ground truth. The **odoomcp** MCP server
(`https://gitmcp.io/odoo/odoo`, served from the `19.0` branch) exposes narrow,
purpose-built tools so you can find and read Odoo's code without a local
checkout and without running raw grep/SQL-style queries.

### Tool map

| Tool                               | What it does                                                                                                                     | Use it for                                                                                                                                                                      |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `search_odoo_code(query, page)`    | GitHub **exact-match** code search across odoo/odoo@19.0. Returns repo-relative file paths + URLs + a score; paginated (`page`). | **Finding where something is implemented.** The core tool — use it before writing new code or when a guide feels incomplete.                                                    |
| `fetch_odoo_documentation()`       | Returns an llms.txt index of the repo `doc/` folder.                                                                             | Rarely — on 19.0 it indexes only `doc/cla/*` legal files, not developer docs.                                                                                                   |
| `search_odoo_documentation(query)` | Semantic search over the fetched docs.                                                                                           | Same caveat: only CLA content. Don't rely on it for dev questions.                                                                                                              |
| `fetch_generic_url_content(url)`   | Generic URL fetcher.                                                                                                             | Known limitation: fails on `github.com`, `raw.githubusercontent.com`, `api.github.com`. To read a file's content, use your environment's own fetch tool (`webfetch`) or `curl`. |

### The 3-step workflow: Find → Fetch → Trace

1. **Find** — `search_odoo_code(query="<exact symbol or string>")`. GitHub code
   search is literal, so use the precise symbol: `models.Constraint`,
   `def _read_group`, `class SaleOrder(models.Model)`, `@api.private`. Skim the
   returned **paths** — results rank by score, not relevance, and the first hit
   is often an `_inherit` extension rather than the base definition.
2. **Fetch** — read the file at
   `https://raw.githubusercontent.com/odoo/odoo/19.0/<repo-relative-path>` with
   your environment's fetch tool or `curl -s ...`. This yields the real
   implementation, signatures, and line numbers.
3. **Trace** — search again for the method name (`_read_group(`), a caller
   (`search_fetch(`), or a class (`class SaleOrder(models.Model)`) to map call
   chains and real usage, then fetch each file to read it.

Full query pattern bank, local-checkout fallback patterns, and
troubleshooting: `references/odoo-19-mcp-guide.md`.

### When odoomcp is unavailable

If the odoomcp tools aren't exposed in your session, don't guess — fetch raw
source files directly (same URL pattern above; the navigation map below tells
you where things live), or if you have a local checkout, use the grep patterns
in `references/odoo-19-mcp-guide.md`.

## File Structure

```
skills/odoo-19.0/
├── SKILL.md                          # This file - master index
└── references/                       # Development guides
    ├── odoo-19-actions-guide.md
    ├── odoo-19-controller-guide.md
    ├── odoo-19-data-guide.md
    ├── odoo-19-decorator-guide.md
    ├── odoo-19-development-guide.md
    ├── odoo-19-field-guide.md
    ├── odoo-19-manifest-guide.md
    ├── odoo-19-mcp-guide.md
    ├── odoo-19-migration-guide.md
    ├── odoo-19-mixins-guide.md
    ├── odoo-19-model-guide.md
    ├── odoo-19-owl-guide.md
    ├── odoo-19-performance-guide.md
    ├── odoo-19-reports-guide.md
    ├── odoo-19-security-guide.md
    ├── odoo-19-testing-guide.md
    ├── odoo-19-transaction-guide.md
    ├── odoo-19-translation-guide.md
    └── odoo-19-view-guide.md
```

## Base Code Reference (Odoo 19)

All guides are based on analysis of Odoo 19 source code (verified against the `19.0` branch):

- `odoo/orm/models.py` - ORM implementation (BaseModel, Model, search/create/write, _read_group)
- `odoo/orm/fields.py` - Field types
- `odoo/orm/decorators.py` - API decorators (@api.*) — moved from `odoo/api.py`
- `odoo/orm/commands.py` - Command helpers for x2many fields
- `odoo/orm/domains.py` - Domain class and operators
- `odoo/http.py` - HTTP layer
- `odoo/exceptions.py` - Exception types
- `odoo/tools/sql.py` - SQL class for safe query building
- `odoo/tools/translate.py` - Translation system
- `odoo/addons/base/models/` - base framework models (ir_model.py, ir_ui_view.py, ir_actions.py, res_partner.py, res_lang.py, ir_cron.py) — the `base` addon moved inside the `odoo` package in 19.0
- `addons/web/static/src/core/l10n/translation.js` - JS translations

## Common Odoo 19 Pitfalls

Watch for these specific gotchas that differ from prior versions or are easy to get wrong:

| Pitfall                                                                                                                   | Wrong ❌                                         | Correct ✅                                             |
| ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------ |
| **`_read_group` return format** — returns a list of **tuples**, not dicts                                                 | `r['field_name']`                                | `for related, count in stats_data:`                    |
| **`user.id` in record rules** — `user` is `res.users`, so comparing against a `res.partner` Many2one field silently fails | `[('instructor_id', '=', user.id)]`              | `[('instructor_id', '=', user.partner_id.id)]`         |
| **`today` in view expressions** — use the `today` context variable, not `today()` or `datetime.date.today()`              | `decoration-danger="start_date < today()"`       | `decoration-danger="start_date < today"`               |
| **`len(record.one2many)` in computed fields** — triggers prefetch of all related records (N+1)                            | `record.session_count = len(record.session_ids)` | Use `_read_group` to aggregate in 1 query              |
| **`formatted_read_group` vs `_read_group`** — the public API returns dicts, the internal returns tuples                   | Using `dict` access on `_read_group` result      | `_read_group` → tuples; `formatted_read_group` → dicts |
| **List vs Tree** — Odoo 19 replaced `<tree>` with `<list>` everywhere, including `view_mode` strings                      | `view_mode="tree,form"`                          | `view_mode="list,form"`                                |

---

## Codebase Discovery & Reverse Engineering

The reference guides above are curated knowledge. But Odoo's real source code is the **ground truth** — always prefer reading it over guessing. This section teaches you _how_ to systematically explore Odoo's 1M+ line codebase.

### The Real Difficulty: Business Logic, Not Code

Odoo development is deceptive. Writing a model class, a view, or a controller is straightforward — the code itself is simple. The real difficulty comes from mastering complex business logic across a massive, deeply interconnected ecosystem. A single `sale.order` touches accounting, inventory, procurement, invoicing, shipping, and CRM. Changing one field can cascade across 20+ modules you didn't know existed.

This means **reading and tracing code is more important than writing it**. You'll spend far more time understanding what already exists than creating new code. Every time you reach for your keyboard to write something new, first ask: "Does Odoo already have this pattern somewhere? Let me go find it." The answer is almost always yes — and that existing code will teach you the edge cases you'd miss if you wrote it from scratch.

### Mindset: Source-First Discovery

When you face an unknown behavior, an undocumented parameter, or a pattern not covered in any guide:

1. **Search first** — use `search_odoo_code` on Odoo's own source before reaching for docs or guessing
2. **Read framework code** — `odoo/orm/models.py`, `odoo/orm/fields.py`, `odoo/orm/decorators.py` contain the real implementations
3. **Find real examples** — Odoo's core addons (`sale`, `account`, `stock`, `purchase`, `project`) are the best documentation
4. **Trace the call chain** — search for where a method is defined, then where it's called, to understand its contract
5. **Trust the source, not assumptions** — Odoo's internals are complex and often have subtle edge cases the docs don't mention

### Source Code Navigation Map

Odoo 19 restructured the framework — the ORM moved under `odoo/orm/` and the
`base` addon moved inside the `odoo` package. Use these paths (all verifiable
on the `19.0` branch):

```
odoo/                          # Framework core — the source of truth for API behavior
├── orm/                       # ORM package (was odoo/models.py, fields.py, api.py)
│   ├── models.py              # BaseModel, Model, search/create/write/unlink/browse,
│   │                          #   _read_group, formatted_read_group, _search, Query, etc.
│   ├── fields.py              # All field class implementations: Char.__init__, Many2one,
│   │                          #   One2many, Command class, Date, Datetime, properties
│   ├── decorators.py          # @api decorators: depends, constrains, ondelete, onchange,
│   │                          #   model, model_create_multi, private, returns
│   ├── commands.py            # Command helpers for x2many fields
│   ├── domains.py             # Domain class and operators
│   ├── environments.py        # Environment
│   ├── registry.py            # Registry / pool
│   └── utils.py               # check_object_name, parse_field_expr, SUPERUSER_ID, READ_GROUP_*
├── http.py                    # HTTP layer: Controller base, route decorator, request,
│                              #   response, authentication, session
├── osv/
│   └── expression.py          # Domain parsing engine: normalize, evaluate, combine
├── tools/
│   ├── sql.py                 # SQL class for safe query building
│   ├── translate.py           # Translation machinery (i18n)
│   ├── profiler.py            # Profiler class for SQL/trace collection
│   └── float_utils.py         # Float precision utilities
├── exceptions.py              # All exception types: UserError, ValidationError,
│                              #   AccessError, AccessDenied, RedirectWarning
├── addons/
│   └── base/                  # BASE ADDON MOVED HERE in 19.0 (was addons/base/)
│       ├── models/            # ir_model.py, ir_ui_view.py, ir_actions.py, ir_ui_menu.py,
│       │                      #   res_partner.py, res_lang.py, ir_cron.py
│       ├── security/          # ir.model.access.csv, ir.rule
│       └── data/              # ir_cron_data.xml, ir_module_category_data.xml
└── release.py                 # Version info (major/minor/micro)

addons/                        ~400+ modules — real-world usage of every framework feature
├── sale/                      # Sales: Many2one/One2many/Many2many patterns, state machines
├── account/                   # Accounting: complex computed fields, constraints,
│                              #   ondelete validation, multi-company, performance patterns
├── stock/                     # Inventory: state machines, move tracking, scheduled actions,
│                              #   quantitative fields, complex domain filters
├── purchase/                  # Purchase: similar patterns to sale, procurement
├── project/                   # Project: task workflows, hierarchy, collaboration mixins
├── hr/                        # HR: hierarchical org structures, reporting lines
├── web/                       # Web client (OWL framework), JS services, view components
│   └── models/                # e.g. ir_model.py, ir_ui_view.py — _inherit EXTENSIONS, not definitions
├── mail/                      # Messaging: mail.thread, mail.activity.mixin, email gateways
├── product/                   # Product catalog: variant management, attribute system
├── mrp/                       # Manufacturing: complex state machines, BOM structures
└── portal/                    # Portal: frontend routes, authentication, sharing
```

### Search Patterns for Codebase Discovery

Use **odoomcp** to find **real usage** of every Odoo feature — faster and more
reliable than reading reference guides for edge cases, and no local checkout
needed. `search_odoo_code` is exact-match, so search for the precise symbol:

| Goal                          | `search_odoo_code` query        |
| ----------------------------- | ------------------------------- |
| Find a model class definition | `class SaleOrder(models.Model)` |
| SQL constraints (Odoo 19)     | `models.Constraint`             |
| Database indexes (Odoo 19)    | `models.Index`                  |
| Delete validation             | `@api.ondelete`                 |
| Private (non-RPC) methods     | `@api.private`                  |
| Batch aggregation             | `def _read_group`               |
| Public read-group API         | `formatted_read_group`          |
| Safe SQL queries              | `from odoo.tools import SQL`    |
| Query-count tests             | `assertQueryCount`              |
| x2many command helpers        | `Command.create(`               |
| Privilege groups (19)         | `res.groups.privilege`          |
| Record rules                  | `domain_force`                  |
| List view decorations         | `decoration-danger`             |
| Migration hooks               | `def migrate(`                  |
| Any error string you saw      | `"<error text>"`                |

Then **fetch** each matching file via
`https://raw.githubusercontent.com/odoo/odoo/19.0/<path>` (webfetch/curl) to
read the implementation. Note: for framework models (e.g. `ir.model`,
`ir.ui.view`) prefer hits under `odoo/addons/base/` — results ranked higher are
often `_inherit` extensions in `addons/web`, `addons/mail`, etc.

The full pattern bank including local-checkout `grep` fallbacks for every
major feature: `references/odoo-19-mcp-guide.md`.

### Reverse Engineering Workflow

Follow this systematic process when you need to understand something the guides don't cover:

**Step 1: Identify what you need to understand**

- A specific ORM method's behavior
- How a decorator processes its arguments
- What a field parameter actually does
- How Odoo renders a specific view type

**Step 2: Locate the implementation in the framework** — via odoomcp (`search_odoo_code` then fetch the file):

- Python decorators → `odoo/orm/decorators.py` (search for the decorator function)
- ORM methods → `odoo/orm/models.py` (search for the method name)
- Field types → `odoo/orm/fields.py` (search for the field class)
- HTTP/routing → `odoo/http.py`
- View rendering → `odoo/addons/base/models/ir_ui_view.py`
- Exception types → `odoo/exceptions.py`
- Domain parsing → `odoo/osv/expression.py`

**Step 3: Read the implementation, not just the signature**

- Look at the method's full source — parameter handling, edge cases, error paths
- Check if it calls `super()` and what the parent does
- Note any decorators on the method that modify behavior

**Step 4: Find real callers in core addons**

- `search_odoo_code(query="<method_name>(")` then fetch 3-5 different callers to understand the range of usage patterns
- Pay attention to how they handle edge cases

**Step 5: Find the test coverage**

- Look for test files that exercise the feature: `addons/*/tests/test_*.py` (or `search_odoo_code` filtered to `*/tests/*` paths)
- Tests reveal expected behavior, edge cases, and error conditions
- Search for asserts related to the feature name

**Example — Understanding a new decorator:**

```
1. search_odoo_code("@<decorator_name>") → fetch odoo/orm/decorators.py to read the implementation
2. Note what it does to the method (wraps it, sets attributes, etc.)
3. search_odoo_code("@<decorator_name>") → read real usage in addons/
4. Read the method it decorates in context — what parameters does it expect?
5. Check tests in addons/*/tests/ that exercise the decorator
```

### Discovering Patterns from Core Addons

The `addons/` directory is the largest repository of Odoo examples. Use it strategically:

**by Framework:**

| Want to see...          | Look in...                              | Why                                                  |
| ----------------------- | --------------------------------------- | ---------------------------------------------------- |
| Basic model structure   | `sale/models/sale_order.py`             | Clean, well-organized, standard patterns             |
| Complex computed fields | `account/models/account_move.py`        | Many computed + stored fields with batch _read_group |
| Constraint examples     | `stock/models/stock_move.py`            | Extensive models.Constraint usage                    |
| State machines          | `project/models/project_task.py`        | Clean state field + action methods                   |
| Multi-company patterns  | `account/models/account_move.py`        | Full multi-company with security rules               |
| Performance patterns    | `sale/models/sale_order.py`             | Batched _read_group, prefetch patterns               |
| Controller examples     | `portal/controllers/portal.py`          | Auth types, routes, CRUD endpoints                   |
| QWeb reports            | `sale/report/sale_order_report.xml`     | Standard report templates                            |
| Security rules          | `account/security/account_security.xml` | Complex record rules with multi-company              |
| Mixin usage             | `project/models/project_task.py`        | mail.thread, activity.mixin, rating.mixin            |
| Migration scripts       | `account/migrations/`                   | Pre/post migration hooks                             |
| OWL components          | `web/static/src/core/`                  | Core OWL framework components                        |

**by Pattern:**

| Pattern               | Search                                | What you'll learn                                   |
| --------------------- | ------------------------------------- | --------------------------------------------------- |
| Batch computed fields | `_read_group` in `account/models/`    | How to aggregate in one query instead of per-record |
| Delete validation     | `@api.ondelete` in `stock/models/`    | When to allow/block deletion, at_uninstall patterns |
| Invisible attributes  | `invisible="state == 'draft'"` in XML | Direct expression syntax vs. old attrs              |
| List decorations      | `decoration-danger` in XML            | Row-level vs. column-level styling                  |
| Scheduled actions     | `ir.cron` in XML files                | How to define periodic tasks                        |
| Server actions        | `ir.actions.server` in XML            | Automated action workflows                          |
| Excel exports         | Add `export_xml` in `base/`           | Custom data export patterns                         |

### Deriving API Contracts from Core Source

When you need to understand _exactly_ what an ORM method does (not just the documented surface):

```python
# Example: understanding what _read_group returns
# Step 1: read the implementation signature in odoo/orm/models.py (via search_odoo_code + fetch)
def _read_group(self, domain, fields, groupby, offset=0, limit=None,
                orderby=False, lazy=True):
    """..."""

# Step 2: read the return value handling
# _read_group returns list[tuple] — each tuple is (group_value, *aggregates)
# For Many2one groupby values: the group value is a singleton recordset
# For regular fields: the raw field value

# Step 3: search_odoo_code("_read_group(") → fetch callers to see how they unpack
# account/models/account_move.py:
#   for journal, move_count in self._read_group(...):
#       ...
```

This approach works for ANY method in Odoo — the source code is always the definitive documentation.

### What to Do When the Skill's Reference Guides Fall Short

1. **Feature not in any guide?** → `search_odoo_code("<feature/symbol>")` to find its definition, then fetch the file
2. **Parameter not documented?** → Read the field class `__init__` in `odoo/orm/fields.py`
3. **View attribute not working?** → Check `odoo/addons/base/models/ir_ui_view.py` for how it's processed
4. **Decorator behavior unclear?** → Read `odoo/orm/decorators.py` for the actual implementation
5. **Error message confusing?** → `search_odoo_code("<error string>")` in Odoo's source
6. **Testing a new pattern?** → Find similar patterns in `addons/*/tests/`
7. **Migration concern?** → Check `odoo/addons/base/migrations/` for framework migration helpers

## External Documentation
