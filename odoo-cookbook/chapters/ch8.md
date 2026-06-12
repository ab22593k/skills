---
chapter: 8
topic: "Advanced Server-Side Development Techniques"
when: "User needs wizards, onchange, SQL views, custom settings, init hooks"
queries:
  [
    "wizard",
    "onchange",
    "sql view",
    "settings",
    "init hook",
    "precompute",
    "raw sql",
  ]
---

## Core Concepts

- **Wizards**: Transient models (`TransientModel` or `AbstractAction`) for guided user dialogs. Created via `models.TransientModel` — data auto-clears after configurable time.
- **Custom settings**: `res.config.settings` with `group_`, `module_`, and `default_` field prefixes for feature toggles.
- **SQL views**: `_auto = False; _table = None` + custom `init()` method with `CREATE or REPLACE VIEW` — read-only model backed by a database view.

## Techniques

- **Onchange**: `@api.onchange('field')` — triggers client-side on field edit. Use `onchange` for client hints, `compute` for stored logic.
- **Precompute**: `@api.depends` with `compute` + `precompute = True` in field definition — computes at install time instead of on first access.
- **Raw SQL**: `self.env.cr.execute("SELECT ...", params)` + `self.env.cr.fetchall()`. Always re-apply security: `self.env[model].search([('id', 'in', ids)])`.
- **sudo()**: `self.sudo().write({...})` bypasses all ACLs and record rules. For non-admin elevation: `self.with_user(uid)`.
- **Init hooks**: `pre_init_hook`, `post_init_hook` in manifest — run before/after module install. Useful for data migration.

## Pitfalls

- `sudo()` bypasses ALL security — use only for internal operations, never on user-facing paths.
- Raw SQL writes require `self.invalidate_model()` afterwards to refresh ORM cache.
- Settings `module_` prefix: unchecking the box silently uninstalls the add-on — risk of data loss. (`→ ch10`)
