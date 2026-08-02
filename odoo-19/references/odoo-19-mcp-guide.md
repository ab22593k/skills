# Odoo 19 — odoomcp MCP Guide

How to use the **odoomcp** MCP server (`https://gitmcp.io/odoo/odoo`) to ground
Odoo work in the real 19.0 source code with narrow, purpose-built tools —
instead of running raw grep/SQL-style queries against a local checkout.

- [What odoomcp is](#what-odoomcp-is)
- [Setup](#setup)
- [Tool map (verified behavior)](#tool-map-verified-behavior)
- [Find → Fetch → Trace workflow](#find--fetch--trace-workflow)
- [Query pattern bank](#query-pattern-bank)
- [Local checkout fallback patterns](#local-checkout-fallback-patterns)
- [Reading file content](#reading-file-content)
- [Odoo 19 source layout (what actually moved)](#odoo-19-source-layout-what-actually-moved)
- [Limitations & troubleshooting](#limitations--troubleshooting)

---

## What odoomcp is

odoomcp is a GitMCP server that serves the `odoo/odoo` GitHub repository from
the **`19.0` branch**. It exposes a handful of narrow, single-purpose tools. It
does **not** give agents raw database/SQL access — it only lets them find and
read Odoo's source and docs, so answers stay grounded in real code.

## Setup

OpenCode / Claude Code (`~/.config/opencode/opencode.json` or `opencode.json`):

```json
"mcp": {
  "odoomcp": {
    "type": "local",
    "command": ["npx", "mcp-remote", "https://gitmcp.io/odoo/odoo"]
  }
}
```

Claude Desktop:

```json
{
  "mcpServers": {
    "odoomcp": {
      "command": "npx",
      "args": ["mcp-remote", "https://gitmcp.io/odoo/odoo"]
    }
  }
}
```

## Tool map (verified behavior)

| Tool                        | Signature                      | Behavior verified on 19.0                                                                                                                                                                     | Use for                                                          |
| --------------------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `search_odoo_code`          | `query: string, page?: number` | GitHub **exact-match** code search scoped to odoo/odoo@19.0. Returns repo-relative paths + `github.com`/`api.github.com` URLs + a score. Paginated (13 pages for `_read_group`, 386 matches). | Finding where a symbol/string is implemented. **The core tool.** |
| `fetch_odoo_documentation`  | `(no args)`                    | Returns an llms.txt index of the repo `doc/` folder. On 19.0 that folder is `doc/cla/*` — legal contributor agreements, **not** developer docs. 1000+ entries, ~all corporate CLA signatures. | Almost never for development.                                    |
| `search_odoo_documentation` | `query: string`                | Semantic search over the fetched docs only (i.e. the CLA index). Results link to `raw.githubusercontent.com/odoo/odoo/19.0/doc/...`.                                                          | Almost never for development.                                    |
| `fetch_generic_url_content` | `url: string`                  | **Fails on GitHub hosts** — `github.com`, `raw.githubusercontent.com`, and `api.github.com` all return "could not be retrieved".                                                              | Use your own fetch tool (`webfetch`) or `curl` instead.          |

Key takeaway: the useful surface is **`search_odoo_code`** (find files) +
**your own fetch tool** (read files).

## Find → Fetch → Trace workflow

### 1. Find — `search_odoo_code`

GitHub code search is **literal/exact-match**, so use the exact symbol or
string, not a paraphrase:

- `search_odoo_code(query="models.Constraint")`
- `search_odoo_code(query="def _read_group")`
- `search_odoo_code(query="class SaleOrder(models.Model)")`
- `search_odoo_code(query="@api.private")`
- `search_odoo_code(query="models.Index")`

Results are ranked by match score, not relevance. **Skim the returned paths**
to pick the right file (the first hit is often an `_inherit` extension, not the
base definition — e.g. `addons/web/models/ir_model.py` extends the real
`ir.model` defined in `odoo/addons/base/models/ir_model.py`). Use the `page`
parameter to walk results.

### 2. Fetch — read the file

`search_odoo_code` returns paths, not contents. Read the file with your
environment's fetch tool:

```
https://raw.githubusercontent.com/odoo/odoo/19.0/<repo-relative-path>
```

- `webfetch` (works on raw.githubusercontent.com), or
- `curl -s https://raw.githubusercontent.com/odoo/odoo/19.0/odoo/orm/models.py`

Reading the actual implementation gives you real signatures, edge cases, and
**line numbers** — the difference between "probably" and "verified".

### 3. Trace — callers and real usage

Search again to map the call chain and find canonical examples:

- Find callers of a method: `search_odoo_code(query="<method_name>(")` e.g. `_read_group(`
- Find a model: `search_odoo_code(query="class SaleOrder(models.Model)")`
- Find real usage of a decorator: `search_odoo_code(query="@api.ondelete")`
- Find tests that exercise a feature: `search_odoo_code(query="<feature>")` and pick paths under `*/tests/*`

Then fetch each file to read it.

## Query pattern bank

| Goal                              | odoomcp `search_odoo_code` query                        |
| --------------------------------- | ------------------------------------------------------- |
| Find a model class definition     | `class <ModelName>(models.Model)`                       |
| Find a Python-inherited extension | `class <ModelName>(models.Model)` then check `_inherit` |
| SQL constraints (Odoo 19)         | `models.Constraint`                                     |
| Database indexes (Odoo 19)        | `models.Index`                                          |
| Delete validation                 | `@api.ondelete`                                         |
| Private (non-RPC) methods         | `@api.private`                                          |
| Batch aggregation                 | `def _read_group`                                       |
| Public read-group API             | `formatted_read_group`                                  |
| Safe SQL queries                  | `from odoo.tools import SQL`                            |
| Query-count tests                 | `assertQueryCount`                                      |
| x2many command helpers            | `Command.create(`                                       |
| Privilege groups (19)             | `res.groups.privilege`                                  |
| Record rules                      | `domain_force`                                          |
| List view decorations             | `decoration-danger`                                     |
| Migration hooks                   | `def migrate(`                                          |
| Computed field w/ inverse         | `inverse=`                                              |
| Field aggregator                  | `aggregator=`                                           |
| Any error string                  | `"<error text you saw>"`                                |

## Local checkout fallback patterns

If odoomcp is unavailable **and** you have a local Odoo 19 checkout, use grep.
The grep bank below covers every major Odoo 19 feature.

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

## Reading file content

`fetch_generic_url_content` does **not** work for GitHub hosts, so read files
with your own tools:

```bash
curl -s https://raw.githubusercontent.com/odoo/odoo/19.0/odoo/orm/models.py
```

or `webfetch` on the same URL. For local checkouts, plain `read` is fine and
preferable (no network).

## Odoo 19 source layout (what actually moved)

Odoo 19 restructured the framework. If a path from an older guide 404s, use
these:

```
odoo/
├── orm/                         # the ORM moved here (was odoo/models.py, odoo/fields.py, odoo/api.py)
│   ├── models.py                # BaseModel, Model, search/create/write/unlink, _read_group, _search, Query
│   ├── fields.py                # field classes (Char, Many2one, One2many, Monetary, properties...)
│   ├── decorators.py            # @api.* (depends, constrains, ondelete, private, model, model_create_multi...)
│   ├── commands.py              # Command helpers for x2many
│   ├── domains.py               # Domain class / operators
│   ├── environments.py          # Environment
│   ├── registry.py              # Registry / pool
│   └── utils.py                 # check_object_name, parse_field_expr, SUPERUSER_ID, READ_GROUP_*
├── http.py                      # Controller base, route, request, response, auth (unchanged)
├── exceptions.py                # UserError, ValidationError, AccessError, AccessDenied (unchanged)
├── osv/expression.py            # domain parsing engine (unchanged)
├── tools/
│   ├── sql.py                   # SQL class for safe query building
│   ├── translate.py             # i18n machinery
│   ├── profiler.py              # SQL/trace profiler
│   └── float_utils.py           # float precision
├── addons/
│   └── base/                    # BASE ADDON MOVED INSIDE odoo/ in 19.0
│       ├── models/              # ir_model.py, ir_ui_view.py, ir_actions.py, ir_ui_menu.py,
│       │                        #   res_partner.py, res_lang.py, ir_cron.py ...
│       ├── security/            # ir.model.access.csv ...
│       ├── data/                # ir_cron_data.xml ...
│       └── __init__.py
└── release.py                   # version info

addons/                          # ~400+ community modules (unchanged location)
├── web/models/ir_model.py       # e.g. extensions (_inherit) of base ir.model — NOT the definition
├── sale/, account/, stock/, purchase/, project/, hr/, mail/, portal/, mrp/ ...
```

Base-model gotcha: `search_odoo_code(query="class IrModel")` returns many
`_inherit` extensions across `addons/web`, `addons/sms`, `addons/mail`... The
**definition** is in `odoo/addons/base/models/ir_model.py`. When you need the
definition, prefer paths under `odoo/addons/base/`; when you need real-world
usage, prefer the community addons.

## Limitations & troubleshooting

| Symptom                                                    | Explanation                                                                                           | What to do                                                                                               |
| ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `fetch_generic_url_content` fails on a GitHub URL          | The tool currently can't retrieve `github.com`/`raw.githubusercontent.com`/`api.github.com`           | Use your own `webfetch` or `curl` on the `raw.githubusercontent.com/odoo/odoo/19.0/...` URL              |
| `search_odoo_code` returns an old path that 404s           | Paths changed in 19.0 (`odoo/models.py` → `odoo/orm/models.py`, `addons/base/` → `odoo/addons/base/`) | Search the moved location or fetch the file to confirm                                                   |
| Docs tools return only CLA content                         | On 19.0 the repo `doc/` folder only holds legal files                                                 | Don't rely on them for dev questions; use code search + fetch                                            |
| Result file is an `_inherit` extension, not the definition | GitHub search ranks by score, extensions often outrank definitions                                    | Prefer paths under `odoo/addons/base/` for framework models, or check for `_inherit` in the fetched file |
| `search_odoo_code` doesn't support regex                   | GitHub code search is literal                                                                         | Use the exact symbol/string; split broad patterns into multiple searches                                 |
| You have the module checked out locally                    | Local `read`/`grep` is faster than network                                                            | Prefer the local checkout when it matches the target version                                             |
