# Patterns

## Two-Editions Architecture

**Type:** Architecture pattern
**Context:** Choosing between Community and Enterprise editions.
**When it fails:** Community-only modules referencing Enterprise APIs (IoT, accounting, cohort) break on CE. Enterprise patches don't exist for CE. (`→ §Odoo editions`)
**Solution:** Develop on CE, test Enterprise features separately. Keep `depends` clean — don't add Enterprise-only deps to CE modules.
**Consequences:** CE covers 90%+ use cases. Enterprise adds <10% premium features.

## ORM Recordset Safety Wrapper

**Type:** Technique
**Context:** After executing raw SQL, data bypasses ORM security.
**When it fails:** Without re-filtering, multi-company or restricted users see forbidden data.
**Solution:** `self.env[model].search([('id', 'in', tuple(sql_ids))]).ids` re-applies all record rules.
**Related:** Closely tied to `sudo()` anti-pattern. (`→ ch8, ch18`)

## View Inheritance Resolution Order

**Type:** Design knowledge
**Context:** Multiple modules modify the same view.
**When it fails:** Inherited views evaluated in module dependency order — later modules silently override earlier ones. No conflict detection.
**Solution:** Name every inheriting child node for traceability. Use specific `xpath` with `expr` targeting unique attributes. Document inherited views in the module's readme.
**Consequences:** Helps debug inheritance chain during upgrades. (`→ ch9`)

## OWL Data Fetch Strategy

**Type:** Technique
**Context:** Fetching data in OWL component lifecycle.
**When it fails:** `onWillRender` fetches data on every render cycle → N+1 RPC calls on hover/scroll interactions.
**Solution:** Use `onWillStart` for one-time fetches, `onWillUpdateProps` for prop-driven fetches. Only use `onWillRender` when data must refresh every render.
**Related:** N+1 RPC anti-pattern. (`→ ch15`)

## Security Layer Composition

**Type:** Framework
**Context:** Securing a feature across all access paths.
**When it fails:** Relying only on ACLs without record rules lets users see all records. Relying only on menu hiding without ACLs leaves direct URL access open.
**Solution:** Compose all 5 layers: menu groups → ACLs → field groups → record rules → view element groups. Test with a non-admin user.
**Consequences:** Defense in depth — one layer's gap is caught by another. (`→ ch10`)

---

## Anti-Patterns

### `sudo()` for convenience

**Risk:** Calling `sudo()` without considering security implications bypasses ACLs AND record rules — data leaks across companies/users.
**Fix:** Use `self.with_user(uid)` for non-admin elevation, or scope `sudo()` to the minimum SQL operation.

### Raw HTML in controllers

**Risk:** XSS injection, no localization, no asset management.
**Fix:** Always use `request.render('template_name', context_dict)` with QWeb templates.

### State mutation in OWL

**Risk:** Direct `this.state.field = value` doesn't trigger re-render — silent UI staleness bugs.
**Fix:** Always `Object.assign(this.state, {field: value})` or use `useState`'s setter pattern.

### Server action Python for complex logic

**Risk:** No breakpoint debugging, hard-to-find behavior (no module code), stack traces less informative.
**Fix:** For complex logic, write a proper module method and call it from the server action with `model.method()`.

### Hardcoded stage name filters

**Risk:** Stage names are translatable — filters break in non-English interfaces.
**Fix:** Use `stage_id` numeric/XML ID references instead of string matching in domains.
