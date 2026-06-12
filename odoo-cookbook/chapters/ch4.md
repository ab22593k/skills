---
chapter: 4
topic: "Building Application Models"
when: "User needs to define models, fields, constraints, inheritance, computed fields"
queries:
  [
    "model definition",
    "fields",
    "monetary field",
    "computed field",
    "model inheritance",
    "constraints",
    "reference field",
  ]
---

## Core Concepts

- **Model representation**: `_name = 'hostel.room'`, `_description = 'Hostel Room'`, `_order = 'name'`, `_rec_name = 'name'`.
- **Field types**: `Char`, `Text`, `Boolean`, `Integer`, `Float`, `Monetary`, `Date`, `Datetime`, `Selection`, `Html`, `Binary`, `Many2one`, `One2many`, `Many2many`, `Reference`.

## Techniques

- **Monetary field**: Requires companion `Many2one('res.currency')` + `fields.Monetary('Rent', currency_field='currency_id')`.
- **Configurable float precision**: Use `digits='Rating Value'` referencing a `decimal.precision` record, or tuple `(total, decimals)`.
- **Computed fields**: `@api.depends('field1', 'field2')` + `store=True` for persistence. Write via `self.field_name = value`.
- **Related fields**: `related='source_id.target_field'` with optional `store=True` and `readonly=True`.
- **Model inheritance**: `_inherit = 'existing.model'` adds features. `_inherit + _name = 'new.model'` copies definition to new model.
- **Delegation inheritance**: `_inherits = {'parent.model': 'parent_field_id'}` — proxies field access to parent.
- **Abstract models**: `_name + _abstract = True` for reusable feature mixins (e.g., `mail.thread`, `image.mixin`).

## Techniques

- **Constraint validation**:
  - Python: `@api.constrains('field')` raising `ValidationError`.
  - SQL: `_sql_constraints = [('name_unique', 'UNIQUE(name)', 'Name must be unique')]`
- **Hierarchy**: `parent_id = fields.Many2one('same.model')` with `parent_name` and `parent_store=True` for fast subtree queries.

## Pitfalls

- `active=True` is default filter — the domain `[('active', 'in', (True, False))]` does NOT behave as expected. Use context `{'active_test': False}` instead.
- Reserved field names: `id`, `create_date`, `create_uid`, `write_date`, `write_uid` — Odoo auto-generates them.
