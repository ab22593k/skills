---
chapter: 1
topic: "Installing the Odoo Development Environment"
when: "User needs to set up Odoo from source, configure PostgreSQL, Nginx, or IDE"
queries:
  [
    "install odoo",
    "setup dev environment",
    "odoo source install",
    "database management",
    "developer mode",
    "nginx odoo",
  ]
---

## Core Concepts

- **Two editions**: Community (LGPLv3, open source) vs Enterprise (proprietary, adds accounting, IoT, studio, VoIP). Enterprise runs on top of Community. (`→ §Odoo editions`)
- **Git repos**: `odoo/odoo` (Community), `odoo/enterprise` (partners only), `odoo-dev/odoo` (development). (`→ §Git repositories`)
- **Runbot**: Automated testing environment at `runbot.odoo.com`. Green = tests pass, red = failures. (`→ §Runbot`)
- **OCA**: Odoo Community Association — non-profit with community modules, migration tools, accounting localizations. (`→ §Odoo Community Association`)

## Key Steps

1. **Source install**: Clone repo, create venv (`python3 -m venv ~/odoo19-venv`), `pip install -r requirements.txt`, run `odoo-bin --addons-path=...`
2. **PostgreSQL**: Create `odoo` user with `CREATEDB` privilege. Configure `pg_hba.conf` for local trust.
3. **Nginx proxy_pass**: Terminate SSL, forward to Odoo backend. Config: `proxy_pass http://odoo_backend; proxy_set_header Host $host;`
4. **Database ops**: Create, duplicate, backup, restore via web interface (`/web/database/manager`) or command line.
5. **Developer mode**: Activate via Settings → Activate Developer Mode (or URL parameter `?debug=1`).

## Techniques

- **`--dev all`**: Enables auto-reload, qweb debugging, asset recompilation. Essential for development. (`→ ch7`)
- **Performance tuning**: Increase `shared_buffers` (25% of RAM), `effective_cache_size` (50% of RAM), `work_mem` (32-64MB). Odoo's `limit_request`, `limit_memory_soft/hard`, `workers` for multiprocessing. (`→ §Fine-tuning PostgreSQL`)

## Pitfalls

- Community-only modules may use proprietary APIs (IoT, accounting) — check license before attempting Enterprise features.
- Runbot is a public test environment — others may overwrite your test data.
