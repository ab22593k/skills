---
chapter: 2
topic: "Managing Odoo Server Instances"
when: "User needs to configure add-ons paths, manage modules, work with GitHub add-ons"
queries:
  [
    "addons path",
    "install module",
    "update module",
    "upgrade module",
    "github addons",
    "pull request",
  ]
---

## Core Concepts

- **Add-ons path**: Odoo scans comma-separated directories for valid module folders. Standard layout: `odoo/addons/,local-addons/,extra-addons/`.
- **Instance directory**: Standardized layout with `local-addons/`, `etc/`, `data/`, `logs/`, `bin/`. Use symlinks for versioned add-ons.

## Techniques

- **Install from CLI**: `odoo-bin -d <db> -i <module>` — installs module and dependencies.
- **Upgrade from CLI**: `odoo-bin -d <db> -u <module>` — updates the module. Use `--stop-after-init` for one-shot commands.
- **GitHub add-ons**: Clone OCA repos into `extra-addons/` and add path. Pin to version-specific branches (e.g., `19.0`).
- **Test PRs**: `git fetch origin pull/<PR>/head:test-pr && git checkout test-pr`. Run with test database.

## Pitfalls

- Module update (`-u`) runs test cases if `--test-enable` is set — can slow down deployments.
- Third-party modules may conflict via same XML IDs — namespace your module's data files.
