---
name: odoo-19
description: >-
  Odoo 19 development knowledge base with 18 specialized guides and a
  systematic methodology for reverse-engineering Odoo's core codebase
  directly. Covers all Odoo 19 API patterns — Actions (ir.actions.*, cron
  jobs, server actions), Controllers (HTTP routing, endpoints, auth types),
  Data files (XML/CSV records, shortcuts, noupdate), API Decorators
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
  when you need to understand undocumented behavior by digging into Odoo's own
  framework source code and core addons. ALWAYS prefer reading Odoo's actual
  source code over guessing — the framework code in odoo/models.py,
  odoo/fields.py, odoo/api.py, and the addons/ directory are the ground truth.
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

All guides are based on analysis of Odoo 19 source code:

- `odoo/models.py` - ORM implementation
- `odoo/fields.py` - Field types
- `odoo/api.py` - Decorators
- `odoo/http.py` - HTTP layer
- `odoo/exceptions.py` - Exception types
- `odoo/tools/translate.py` - Translation system
- `odoo/addons/base/models/res_lang.py` - Language model
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

1. **Search first** — grep Odoo's own source before reaching for docs or guessing
2. **Read framework code** — `odoo/models.py`, `odoo/fields.py`, `odoo/api.py` contain the real implementations
3. **Find real examples** — Odoo's core addons (`sale`, `account`, `stock`, `purchase`, `project`) are the best documentation
4. **Trace the call chain** — search for where a method is defined, then where it's called, to understand its contract
5. **Trust the source, not assumptions** — Odoo's internals are complex and often have subtle edge cases the docs don't mention

### Source Code Navigation Map

```
odoo/                          # Framework core — the source of truth for API behavior
├── models.py                  # ORM: BaseModel, search, create, write, unlink, browse,
│                              #   fields_view_get, _read_group, _auto_init, init, etc.
├── fields.py                  # All field class implementations: Char.__init__, Many2one,
│                              #   One2many, Command class, Domain class, Date, Datetime
├── api.py                     # Decorator implementations: depends, constrains, ondelete,
│                              #   onchange, model, model_create_multi, private, returns
├── http.py                    # HTTP layer: Controller base, route decorator, request,
│                              #   response, authentication, session
├── osv/
│   └── expression.py          # Domain parsing engine: normalize, evaluate, combine
├── tools/
│   ├── sql.py                 # SQL class for safe query building
│   ├── translate.py           # Translation machinery (i18n)
│   ├── render.py              # QWeb template rendering engine
│   ├── profiler.py            # Profiler class for SQL/trace collection
│   └── float_utils.py         # Float precision utilities
├── exceptions.py              # All exception types: UserError, ValidationError,
│                              #   AccessError, AccessDenied, RedirectWarning
├── conf.py                    # Configuration handling
└── release.py                 # Version info (major/minor/micro)

addons/                        ~400+ modules — real-world usage of every framework feature
├── base/                      # Framework models (res.users, res.partner, ir.model,
│                              #   ir.ui.view, ir.actions.*, res.groups, res.lang)
├── sale/                      # Sales: Many2one/One2many/Many2many patterns, state machines
├── account/                   # Accounting: complex computed fields, constraints,
│                              #   ondelete validation, multi-company, performance patterns
├── stock/                     # Inventory: state machines, move tracking, scheduled actions,
│                              #   quantitative fields, complex domain filters
├── purchase/                  # Purchase: similar patterns to sale, procurement
├── project/                   # Project: task workflows, hierarchy, collaboration mixins
├── hr/                        # HR: hierarchical org structures, reporting lines
├── web/                       # Web client (OWL framework), JS services, view components
├── mail/                      # Messaging: mail.thread, mail.activity.mixin, email gateways
├── product/                   # Product catalog: variant management, attribute system
├── mrp/                       # Manufacturing: complex state machines, BOM structures
└── portal/                    # Portal: frontend routes, authentication, sharing
```

### Search Patterns for Codebase Discovery

Use these grep patterns to find **real usage** of every Odoo feature. This is faster and more reliable than reading the reference guides for edge cases.

```bash
# --- Model / ORM patterns ---

# Find models using auto-derived _name (Odoo 19)
grep -rn "^class.*\(models.Model\)" addons/ --include="*.py" | head -30

# Find models.Constraint usage in real modules
grep -rn "models.Constraint" addons/ --include="*.py" | head -30

# Find models.Index usage across the codebase
grep -rn "models.Index" addons/ --include="*.py" | head -20

# Find computed fields with search method
grep -rn "search=" addons/ --include="*.py" | head -20

# Find computed fields with inverse method
grep -rn "inverse=" addons/ --include="*.py" | head -15

# --- Decorator patterns ---

# Find @api.ondelete examples (delete validation)
grep -rn "@api.ondelete" addons/ --include="*.py" | head -20

# Find @api.private usage (Odoo 19 non-RPC methods)
grep -rn "@api.private" addons/ --include="*.py" | head -15

# Find @api.autovacuum usage
grep -rn "@api.autovacuum" addons/ --include="*.py" | head -10

# Find @api.model_create_multi examples
grep -rn "@api.model_create_multi" addons/ --include="*.py" | head -10

# --- Performance / query patterns ---

# Find _read_group usage (batch aggregation)
grep -rn "_read_group" addons/ --include="*.py" | head -30

# Find formatted_read_group usage (public API)
grep -rn "formatted_read_group" addons/ --include="*.py" | head -10

# Find SQL class usage for safe queries
grep -rn "from odoo.tools import SQL" addons/ --include="*.py" | head -10

# Find assertQueryCount in tests
grep -rn "assertQueryCount" addons/ --include="*.py" | head -20

# --- Field patterns ---

# Find fields with aggregator parameter
grep -rn "aggregator=" addons/ --include="*.py" | head -20

# Find Image fields with dimension constraints
grep -rn "max_width\|max_height" addons/ --include="*.py" | head -10

# Find Monetary fields with custom currency_field
grep -rn "currency_field=" addons/ --include="*.py" | head -15

# --- Relational field commands ---

# Find Command.create usage
grep -rn "Command.create(" addons/ --include="*.py" | head -20

# Find Command.set usage (replace all)
grep -rn "Command.set(" addons/ --include="*.py" | head -15

# --- Security patterns (Odoo 19 privilege system) ---

# Find res.groups.privilege records in XML
grep -rn "res.groups.privilege" addons/ --include="*.xml" | head -20

# Find ir.rule with non-standard domains
grep -rn "domain_force" addons/ --include="*.xml" | head -30

# --- View patterns ---

# Find list view with decoration-danger expressions
grep -rn "decoration-danger" addons/ --include="*.xml" | head -20

# Find views using invisible with direct expressions
grep -rn "invisible=" addons/ --include="*.xml" | head -30 | grep -v "attrs="

# --- Migration patterns ---

# Find pre/post migration hooks
grep -rn "def migrate\|pre-migration\|post-migration" addons/ --include="*.py" \
  | grep "migrations" | head -15
```

### Reverse Engineering Workflow

Follow this systematic process when you need to understand something the guides don't cover:

**Step 1: Identify what you need to understand**

- A specific ORM method's behavior
- How a decorator processes its arguments
- What a field parameter actually does
- How Odoo renders a specific view type

**Step 2: Locate the implementation in the framework**

- Python decorators → `odoo/api.py` (search for the decorator function)
- ORM methods → `odoo/models.py` (search for the method name)
- Field types → `odoo/fields.py` (search for the field class)
- HTTP/routing → `odoo/http.py`
- View rendering → `odoo/addons/base/models/ir_ui_view.py`
- Exception types → `odoo/exceptions.py`
- Domain parsing → `odoo/osv/expression.py`

**Step 3: Read the implementation, not just the signature**

- Look at the method's full source — parameter handling, edge cases, error paths
- Check if it calls `super()` and what the parent does
- Note any decorators on the method that modify behavior

**Step 4: Find real callers in core addons**

- Grep for the method name in `addons/` to see how Odoo's own modules use it
- Look at 3-5 different callers to understand the range of usage patterns
- Pay attention to how they handle edge cases

**Step 5: Find the test coverage**

- Look for test files that exercise the feature: `addons/*/tests/test_*.py`
- Tests reveal expected behavior, edge cases, and error conditions
- Search for asserts related to the feature name

**Example — Understanding a new decorator:**

```
1. Read odoo/api.py → find the decorator implementation
2. Note what it does to the method (wraps it, sets attributes, etc.)
3. Grep addons/ for @<decorator_name> to see real usage
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
# Step 1: read the implementation signature in odoo/models.py
def _read_group(self, domain, fields, groupby, offset=0, limit=None,
                orderby=False, lazy=True):
    """..."""

# Step 2: read the return value handling
# _read_group returns list[tuple] — each tuple is (group_value, *aggregates)
# For Many2one groupby values: the group value is a singleton recordset
# For regular fields: the raw field value

# Step 3: grep for callers to see how they unpack
# account/models/account_move.py:
#   for journal, move_count in self._read_group(...):
#       ...
```

This approach works for ANY method in Odoo — the source code is always the definitive documentation.

### What to Do When the Skill's Reference Guides Fall Short

1. **Feature not in any guide?** → Grep `odoo/` for the class/function name to find its definition
2. **Parameter not documented?** → Read the field class `__init__` in `odoo/fields.py`
3. **View attribute not working?** → Check `ir_ui_view.py` in `addons/base/models/` for how it's processed
4. **Decorator behavior unclear?** → Read `odoo/api.py` for the actual implementation
5. **Error message confusing?** → Search Odoo's source for the error string
6. **Testing a new pattern?** → Find similar patterns in `addons/*/tests/`
7. **Migration concern?** → Check `addons/base/migrations/` for framework migration helpers

## External Documentation
