# Odoo 19 Documentation - AI Agents Setup

Setup guide for using Odoo 19 documentation with AI coding assistants (Cursor, Claude Code, Windsurf, Aider, etc.).

## Quick Start

### Install via skills.sh (Recommended)

```bash
# Add Odoo 19 skill to your project
npx skills add unclecatvn/agent-skills
```

Visit [https://skills.sh/](https://skills.sh/) for more installation options.

### Cursor IDE - Remote Rule

Configure once in Cursor settings:

- `Settings` → `Rules` → `Add Remote Rule`
- Source: `Git Repository`
- URL: `git@github.com:unclecatvn/agent-skills.git`
- Branch: `19.0`
- Subfolder: `skills/odoo-19.0/`

---

## Odoo MCP Server (odoomcp)

This skill is designed around the **odoomcp** MCP server
(`https://gitmcp.io/odoo/odoo`, serving the **`19.0`** branch). It gives
agents narrow, purpose-built source-access tools — so answers can be grounded
in Odoo's real 19.0 source **without a local checkout and without raw
database/grep queries**.

### OpenCode / Claude Code config

Add to `~/.config/opencode/opencode.json` (or your project `opencode.json`):

```json
{
  "mcp": {
    "odoomcp": {
      "type": "local",
      "command": ["npx", "mcp-remote", "https://gitmcp.io/odoo/odoo"]
    }
  }
}
```

### Claude Desktop config

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

### What it exposes

| Tool                               | Purpose                                                                                                         |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `search_odoo_code(query, page)`    | Exact-match code search over odoo/odoo@19.0; returns file paths + URLs (paginated). **Core tool.**              |
| `fetch_odoo_documentation()`       | llms.txt index of the repo `doc/` folder (mostly legal CLA files on 19.0 — rarely useful for dev).              |
| `search_odoo_documentation(query)` | Semantic search over those docs (same CLA limitation).                                                          |
| `fetch_generic_url_content(url)`   | Generic URL fetcher — note it currently fails on `github.com` / `raw.githubusercontent.com` / `api.github.com`. |

`search_odoo_code` returns paths, not contents. To read a file, fetch
`https://raw.githubusercontent.com/odoo/odoo/19.0/<path>` with your own
`webfetch`/`curl`.

See `SKILL.md` → "Odoo Source Access via odoomcp (MCP)" and
`references/odoo-19-mcp-guide.md` for the full workflow, query pattern bank,
and troubleshooting.

---

## Documentation Structure

```
skills/odoo-19.0/
├── SKILL.md                       # Master index (all agents)
├── references/                    # Development guides (18 files)
│   ├── odoo-19-actions-guide.md     # ir.actions.*, cron, bindings
│   ├── odoo-19-controller-guide.md  # HTTP, routing, controllers
│   ├── odoo-19-data-guide.md        # XML/CSV data files, records
│   ├── odoo-19-decorator-guide.md   # @api decorators
│   ├── odoo-19-development-guide.md # Manifest, wizards (overview)
│   ├── odoo-19-field-guide.md       # Field types, parameters
│   ├── odoo-19-manifest-guide.md    # __manifest__.py reference
│   ├── odoo-19-mcp-guide.md         # odoomcp MCP source-access workflow
│   ├── odoo-19-mixins-guide.md      # mail.thread, activities, etc.
│   ├── odoo-19-model-guide.md       # ORM, CRUD, search, domain
│   ├── odoo-19-migration-guide.md   # Migration scripts, hooks
│   ├── odoo-19-owl-guide.md         # OWL components, services
│   ├── odoo-19-performance-guide.md # N+1 prevention, optimization
│   ├── odoo-19-reports-guide.md     # QWeb reports, PDF/HTML
│   ├── odoo-19-security-guide.md    # ACL, record rules, security
│   ├── odoo-19-testing-guide.md     # Test classes, decorators
│   ├── odoo-19-transaction-guide.md # Savepoints, errors
│   ├── odoo-19-translation-guide.md # Translations, i18n
│   └── odoo-19-view-guide.md        # XML views, QWeb
├── CLAUDE.md                      # Claude Code specific
└── AGENTS.md                      # THIS FILE - setup guide
```

---

## Guide Reference

| File                                      | Purpose                               | When to Use                             |
| ----------------------------------------- | ------------------------------------- | --------------------------------------- |
| `SKILL.md`                                | Master index for all guides           | Find the right guide for your task      |
| `references/odoo-19-actions-guide.md`     | Actions (window, URL, server, cron)   | Creating actions, menus, scheduled jobs |
| `references/odoo-19-controller-guide.md`  | HTTP controllers, routing             | Writing endpoints                       |
| `references/odoo-19-data-guide.md`        | XML/CSV data files, records           | Creating data files                     |
| `references/odoo-19-decorator-guide.md`   | @api decorators usage                 | Using @api decorators                   |
| `references/odoo-19-development-guide.md` | Module structure, wizards             | Creating new modules                    |
| `references/odoo-19-field-guide.md`       | Field types, parameters               | Defining model fields                   |
| `references/odoo-19-manifest-guide.md`    | **manifest**.py reference             | Configuring module manifest             |
| `references/odoo-19-mixins-guide.md`      | mail.thread, activities, mixins       | Adding messaging, activities            |
| `references/odoo-19-model-guide.md`       | ORM methods, CRUD, domains            | Writing model methods                   |
| `references/odoo-19-migration-guide.md`   | Migration scripts, hooks              | Upgrading modules                       |
| `references/odoo-19-owl-guide.md`         | OWL components, hooks, services       | Building OWL UI                         |
| `references/odoo-19-performance-guide.md` | Performance optimization              | Fixing slow code                        |
| `references/odoo-19-reports-guide.md`     | QWeb reports, templates               | Creating reports                        |
| `references/odoo-19-security-guide.md`    | ACL, record rules, security           | Configuring security                    |
| `references/odoo-19-testing-guide.md`     | Test classes, decorators, mocking     | Writing tests                           |
| `references/odoo-19-transaction-guide.md` | Database transactions, error handling | Savepoints, UniqueViolation             |
| `references/odoo-19-translation-guide.md` | Translations, localization, i18n      | Adding translations                     |
| `references/odoo-19-view-guide.md`        | XML views, actions, menus             | Writing view XML                        |

---

## AI Agent Configuration

### Cursor IDE

| Setting   | Value                                        |
| --------- | -------------------------------------------- |
| Source    | Git Repository                               |
| URL       | `git@github.com:unclecatvn/agent-skills.git` |
| Branch    | `19.0`                                       |
| Subfolder | `skills/odoo-19.0/`                          |

**Globs patterns used by Cursor:**

| File                                      | globs Pattern                |
| ----------------------------------------- | ---------------------------- |
| `SKILL.md`                                | `**/*.{py,xml}`              |
| `references/odoo-19-actions-guide.md`     | `**/*.{py,xml}`              |
| `references/odoo-19-controller-guide.md`  | `**/controllers/**/*.py`     |
| `references/odoo-19-data-guide.md`        | `**/*.{xml,csv}`             |
| `references/odoo-19-decorator-guide.md`   | `**/models/**/*.py`          |
| `references/odoo-19-development-guide.md` | `**/*.{py,xml,csv}`          |
| `references/odoo-19-field-guide.md`       | `**/models/**/*.py`          |
| `references/odoo-19-manifest-guide.md`    | `**/__manifest__.py`         |
| `references/odoo-19-mixins-guide.md`      | `**/models/**/*.py`          |
| `references/odoo-19-model-guide.md`       | `**/models/**/*.py`          |
| `references/odoo-19-migration-guide.md`   | `**/migrations/**/*.py`      |
| `references/odoo-19-owl-guide.md`         | `static/src/**/*.{js,xml}`   |
| `references/odoo-19-performance-guide.md` | `**/*.{py,xml}`              |
| `references/odoo-19-reports-guide.md`     | `**/report/**/*.xml`         |
| `references/odoo-19-security-guide.md`    | `**/security/**/*.{csv,xml}` |
| `references/odoo-19-testing-guide.md`     | `**/tests/**/*.py`           |
| `references/odoo-19-transaction-guide.md` | `**/models/**/*.py`          |
| `references/odoo-19-translation-guide.md` | `**/*.{py,js,xml}`           |
| `references/odoo-19-view-guide.md`        | `**/views/**/*.xml`          |

### Claude Code

```bash
# Install via skills.sh
npx skills add unclecatvn/agent-skills
```

Claude Code reads:

- `CLAUDE.md` - Project overview and quick reference
- `SKILL.md` - Master index for all guides
- Individual guides in `references/` - Detailed information

### Other Agents

| Agent    | Setup                                                      |
| -------- | ---------------------------------------------------------- |
| Windsurf | Same as Cursor (uses `.mdc` files)                         |
| Continue | Place `CLAUDE.md` or `SKILL.md` in root                    |
| Aider    | Place `CLAUDE.md` or add to prompt                         |
| OpenCode | Copy skill folder to project - no additional config needed |

---

## Cursor / Claude Skills Folder

After installing via `npx skills add unclecatvn/agent-skills`, the skill is placed at:

```
.cursor/skills/
└── odoo-19/
    └── SKILL.md

.claude/skills/
└── odoo-19/
    └── SKILL.md
```

---

## Key Odoo 19 Changes

| Change             | Old                            | New                                     |
| ------------------ | ------------------------------ | --------------------------------------- |
| List view tag      | `<tree>`                       | `<list>`                                |
| Dynamic attributes | `attrs="{'invisible': [...]}"` | `invisible="..."`                       |
| Delete validation  | Override `unlink()`            | `@api.ondelete(at_uninstall=False)`     |
| Field aggregation  | `group_operator=`              | `aggregator=`                           |
| SQL queries        | `cr.execute()`                 | `SQL` class with `execute_query_dict()` |

---

## Repository

**URL**: `git@github.com:unclecatvn/agent-skills.git`
**Branch**: `19.0`
**License**: MIT
