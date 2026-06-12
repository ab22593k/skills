# Cheatsheet

## Choosing Field Type

| Data                           | Field Type       | Notes                                                          |
| ------------------------------ | ---------------- | -------------------------------------------------------------- |
| Short text                     | `Char`           | Use `size` for max length                                      |
| Long text                      | `Text`           | No size limit                                                  |
| Integer                        | `Integer`        |                                                                |
| Float (configurable precision) | `Float`          | `digits='Name'` refs `decimal.precision` or tuple `(total, d)` |
| Money                          | `Monetary`       | Requires `currency_id` Many2one field                          |
| Date                           | `Date`           | `Date.today()`, `Date.context_today()`                         |
| Date+Time                      | `Datetime`       | `Datetime.now()`, `Datetime.context_timestamp()`               |
| Boolean                        | `Boolean`        |                                                                |
| Selection                      | `Selection`      | Static list or computed via function                           |
| Relation (N:1)                 | `Many2one`       |                                                                |
| Relation (1:N)                 | `One2many`       | Requires inverse `Many2one`                                    |
| Relation (N:N)                 | `Many2many`      |                                                                |
| Computed                       | Any + `compute=` | Use `@api.depends` + `store=True` for persistence              |
| Related                        | Any + `related=` | Read-only proxy to source field                                |
| Binary/Large                   | `Binary`         | Use `image.mixin` for images                                   |
| Dynamic relation               | `Reference`      | String like `'res.partner,42'`                                 |

## Model Inheritance Strategies

| Goal                         | Pattern                           | When                                                 |
| ---------------------------- | --------------------------------- | ---------------------------------------------------- |
| Add fields to existing model | `_inherit = 'model'`              | Extending sales.order, res.partner                   |
| Copy def to new model        | `_inherit + _name`                | Variation of base model                              |
| Proxy fields from parent     | `_inherits = {'parent': 'field'}` | Hierarchical data (e.g., product template → product) |
| Reusable feature mixin       | `_abstract = True`                | Share methods without DB table                       |

## View Inheritance Positions

| Position           | Effect                                |
| ------------------ | ------------------------------------- |
| `after` / `before` | Insert sibling after or before target |
| `replace`          | Replace target node entirely          |
| `attributes`       | Modify attributes of target node      |
| `inside`           | Insert as last child                  |
| `//` (prepend)     | Insert as first child                 |

## Security Layers (order matters)

| Layer         | File                           | Mechanism                      |
| ------------- | ------------------------------ | ------------------------------ |
| Menu          | `security/groups.xml`          | `groups="..."` on `<menuitem>` |
| Model ACL     | `security/ir.model.access.csv` | CRUD per group                 |
| Field         | Python/XML                     | `groups="..."` on field def    |
| Record rules  | `security/<model>_rules.xml`   | `domain_force` filter          |
| View elements | View XML                       | `groups="..."` on any tag      |

## Recordset Operators

| Operator              | Effect                                       |
| --------------------- | -------------------------------------------- |
| `r1 + r2`             | Concatenation (may duplicate)                |
| `r1 \| r2`            | Union (no duplicates)                        |
| `r1 & r2`             | Intersection                                 |
| `r1 - r2`             | Difference                                   |
| `\|=` on field        | Union-assign to O2M/M2M                      |
| `filtered(lambda)`    | In-memory filter (use domain for large sets) |
| `mapped('field.sub')` | Traverse relation paths                      |
| `sorted('field')`     | Sort by field (db or python)                 |

## Performance Decision Table

| Need                 | Approach                             | When to avoid                                   |
| -------------------- | ------------------------------------ | ----------------------------------------------- |
| Many records at once | `search()` with domain               | Counting only → use `count=True`                |
| Group aggregation    | `read_group()`                       | Need one field per record → use `search_read()` |
| Bulk create          | `create([{...}, {...}])`             | One record at a time                            |
| Bulk write           | `write({'field': val})` on recordset | Per-record attribute assignment                 |
| Cache repeated calls | `@ormcache('arg1', 'arg2')`          | Unique args every call                          |
| Image handling       | `image.mixin`                        | Need custom sizes                               |
| Full-text needs      | `name_search()` / `_name_search()`   | Complex scoring                                 |

## RPC Decision Table

| Protocol            | Endpoint           | Best for             | Status                   |
| ------------------- | ------------------ | -------------------- | ------------------------ |
| XML-RPC             | `/xmlrpc/2/object` | Legacy integration   | Deprecated (EOL Odoo 22) |
| JSON-RPC            | `/jsonrpc`         | New integrations     | Deprecated (EOL Odoo 22) |
| REST API            | Custom controller  | Legacy system bridge | Active                   |
| External JSON-2 API | `odoo-client-lib`  | Future-proof         | Recommended              |
| OCA odoorpc         | Python library     | Python clients       | Active                   |
