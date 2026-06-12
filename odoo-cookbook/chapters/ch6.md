---
chapter: 6
topic: "Managing Module Data"
when: "User needs to load data via XML/CSV, use noupdate, handle data migration"
queries:
  [
    "xml data",
    "csv data",
    "external id",
    "noupdate",
    "demo data",
    "data migration",
  ]
---

## Core Concepts

- **External IDs (XML IDs)**: `<record id="my_id" model="x">` — uniquely identifies records across modules. Format: `module.record_id`.
- **noupdate flag**: Records in `data/` with `noupdate="1"` are created on install but NOT updated on upgrade. Use for manually editable reference data.

## Techniques

- **XML data**: `<record model="hostel.room"><field name="name">Room A</field></record>`. Use `eval` for computed values.
- **CSV data**: Used for ACLs (`ir.model.access.csv`) with columns: `id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink`.
- **Function invocation from XML**: `<function model="..." name="method_name" eval="[args]"/>` — runs during module load.
- **Demo data**: Place in `demo/` directory — only loaded if `--demo=all` or when creating a database with demo data.
- **Data migration**: Override `_post_init_hook` or module `post_init_hook` in manifest for data transforms on upgrade.

## Pitfalls

- `noupdate=""` records with `forcecreate="false"` won't create missing records on upgrade — only update existing ones.
- CSV `id` column must be globally unique — prefix with module namespace.
- `eval` in XML can execute arbitrary Python — avoid on user-provided data.
