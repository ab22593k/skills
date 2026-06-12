---
chapter: 9
topic: "Building and Customizing Backend Views"
when: "User needs to design form/list/kanban/search/calendar/graph/pivot views, view inheritance"
queries:
  [
    "form view",
    "list view",
    "kanban view",
    "search view",
    "view inheritance",
    "xpath",
    "domain",
    "context",
    "widget",
  ]
---

## Core Concepts

- **View types**: `form`, `list`/`tree`, `kanban`, `search`, `calendar`, `graph`, `pivot`, `cohort`, `gantt`, `activity`, `map`.
- **Window action**: `ir.actions.act_window` binds model + view modes + domain + context. Used via menu items.
- **View inheritance**: `<record id="..." model="ir.ui.view"><field name="inherit_id" ref="original_view"/>` + `<xpath expr="..." position="..."/>`

## Techniques

- **Form view elements**: `<header>` (buttons/workflow), `<sheet>` (main content), `<group>` (2-column layout), `<notebook>/<page>` (tabs), `<field>`, `<button>`, `<separator>`.
- **Context**: `<field name="context">{'default_field': value, 'force_detailed_view': True}</field>` — passes parameters to child views and new records.
- **Domain**: `<field name="domain">[('field', 'operator', value)]</field>` — filters selection fields.
- **Widgets**: `widget="monetary"`,`"many2many_tags"`,`"selection_badge"`,`"progressbar"`,`"handle"`, etc.
- **Search view**: `<filter name="..." domain="[...]"/>` (context-independent), `<separator/>`, `<group expand="0">` (side panel).
- **Kanban**: Card-based view with QWeb template. `<t-foreach="records" t-as="card">` loop. Columns by `default_group_by` or `group_create="true"`.
- **View inheritance positions**: `after`, `before`, `replace`, `attributes`, `inside`, `//` (prepend).

## Pitfalls

- View inheritance evaluation order = module dependency order — later modules win conflicts.
- Always `name` XML nodes for debuggable inheritance targeting.
- Domains with `|` (OR) operator: the first two conditions after `|` form one OR group, the rest AND with the group.
- `[('active', 'in', (True, False))]` does NOT work — use `context={'active_test': False}` instead.
