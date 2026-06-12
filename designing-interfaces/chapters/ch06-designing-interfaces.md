# Chapter 6 — Showing Complex Data

## Core concepts

- Data display must match the user's task: compare, monitor, explore, or export
- Choose the right format: table (comparison), list (scanning), chart (trends), dashboard (at-a-glance)
- Filter, sort, and search are inseparable from data display
- Large datasets need progressive disclosure: show summary first, details on demand

## Frameworks introduced

- **Data table** — Sortable columns, row actions, sticky header, alternating row stripes for scanning. Add column chooser for wide tables.
- **Data list** — Vertical list of items with thumbnail + primary info. Supports sort, filter, infinite scroll or pagination.
- **Chart types** — Bar (comparison), line (trends), scatter (correlation), pie (composition — use sparingly). Add tooltip on hover.
- **Dashboard** — Aggregation of data views (cards, charts, lists) on a single screen. Each widget is self-contained.
- **Tree / Hierarchy view** — Expandable node tree for taxonomies, file systems, org charts.
- **Map-based display** — Geospatial data with markers, clustering for density, info windows on selection.
- **Data filter** — Combined filter panel + results. Presets for common filters. Search within filters.

## Key techniques

- **Mini-table / Sparkline**: Compact inline chart showing trend in a table cell
- **Column sorting**: Click to sort asc → desc → unsorted. Multi-column shift-click for power users.
- **Dynamic table features**: Resizable columns, row grouping, export to CSV, frozen columns for key identifiers
- **Pagination vs infinite scroll**: Paginate when users need to find specific items or bookmarks in a list. Infinite scroll for discovery (social, image feeds).

## Connection to other chapters

Data display depends on layout (Ch4) for structure. Forms (Ch7) feed data into these views. Charts and colors apply visual principles from Ch9. Data-heavy apps benefit from design systems (Ch11) with standardized table, chart, and filter components.
