---
chapter: 3
topic: "Creating Odoo Add-On Modules"
when: "User needs to create a new module, structure it, write manifest, scaffold"
queries:
  [
    "create module",
    "module manifest",
    "scaffold",
    "addon structure",
    "module files",
  ]
---

## Core Concepts

- **Module = Python package** with `__init__.py` + `__manifest__.py`. Technical name = valid Python identifier (lowercase, digits, underscores).
- **Manifest keys**: `name`, `summary`, `description`, `author`, `website`, `category`, `version` (`'19.0.1.0.0'`), `depends` (min `['base']`), `data` (ordered file list), `demo`, `assets`, `license`.

## Techniques

- **Scaffold**: `odoo-bin scaffold <module_name> <addons_path>` — generates skeleton with models, views, security, data dirs.
- **File structure**: `__init__.py` → `__manifest__.py` → `models/` → `views/` → `security/` → `data/` → `static/description/icon.png` → `wizards/` → `report/`
- **Icon**: Must be a 256×256 PNG at `static/description/icon.png`.
- **Category**: Set `'category': 'Hostel'` in manifest — Odoo auto-generates `ir.module.category` XML ID `base.module_category_hostel`.

## Frameworks

- **Module lifecycle**: Install → (upgrade) → (uninstall). Use `pre_init_hook`, `post_init_hook`, `uninstall_hook` for custom hooks.
- **Glue modules**: `auto_install = True` with `depends` listing both parent modules — auto-installs when both parents are present.

## Pitfalls

- Version mismatch between Odoo major versions breaks modules — no backwards compatibility across versions.
- Manifest `depends` must include ALL modules whose XML IDs or models are referenced, or loading fails silently.
