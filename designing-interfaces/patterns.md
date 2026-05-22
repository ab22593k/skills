# Pattern Catalog

## Chapter 2 — Organizing Content

### Hierarchical Organization
- **Type:** technique
- **Context:** Content has natural categories and subcategories
- **Solution:** Create a tree structure with broad, shallow categories. Top level: 5-7 items. Keep depth to 3 levels max.
- **Consequences:** Familiar, scannable. Users must know which category their target lives in.
- **Related:** Faceted Navigation, Flat Navigation

### Faceted Navigation
- **Type:** technique
- **Context:** Users search by multiple attributes (e.g., e-commerce filters for size + color + price)
- **Solution:** Show clickable filter values alongside results. Update both as selections change. Allow combining facets.
- **Consequences:** Powerful exploration. Can overwhelm with too many facets. Needs clear "clear all" affordance.
- **Related:** Search with filters

### Search with Autocomplete
- **Type:** technique
- **Context:** Large content sets — users may not know exact terms
- **Solution:** Show real-time suggestions (top 5-10) as user types. Surface category hints. Support typos loosely (Postel's Law).
- **Consequences:** Faster find. Reduces zero-result searches. Needs debounced backend queries.
- **Related:** Faceted Navigation, Pagination

## Chapter 3 — Getting Around

### Tab Bar
- **Type:** technique
- **Context:** 3-7 top-level sections the user switches between frequently
- **Solution:** A horizontal row of labeled tabs. Active tab is visually distinct. Content swaps without page reload.
- **Consequences:** Fast switching, always visible. Doesn't scale past ~7 items. Not for deep hierarchies.
- **Related:** Bottom Navigation (mobile)

### Breadcrumbs
- **Type:** technique
- **Context:** Deep hierarchical sites (e-commerce, docs, admin)
- **Solution:** Show "Home > Category > Subcategory > Current Page" with clickable links. Use ">" as separator. Truncate deep paths.
- **Consequences:** Gives context, supports jumping up levels. Takes horizontal space. Not useful on shallow sites.
- **Related:** Hierarchical Organization

### Stepper
- **Type:** technique
- **Context:** Multi-step forms or processes (checkout, setup wizard, onboarding)
- **Solution:** Show numbered/sequential steps with current step highlighted. Allow return to completed steps. Show completion per step.
- **Consequences:** Clear progress, reduces abandonment. Rigid linear flow; not for branching processes.
- **Related:** Wizard (Ch7)

## Chapter 4 — Organizing the Page

### Card Layout
- **Type:** technique
- **Context:** Heterogeneous content items with different amounts of information (dashboards, social feeds, portfolios)
- **Solution:** Each item in a visually bounded container. Cards reflow naturally in a responsive grid. Consistent internal padding.
- **Consequences:** Flexible, scannable, responsive. Can waste space if content is homogeneous. Too many cards feel cluttered.
- **Related:** Grid System, Visual Hierarchy

### Progressive Enhancement
- **Type:** principle
- **Context:** Building for diverse devices and network conditions
- **Solution:** Start with core content/functionality. Layer on enhancements (JS interactions, high-res images, animations) for capable clients.
- **Consequences:** Universal baseline. More work than graceful degradation. Keeps core accessible.
- **Related:** Responsive Design

## Chapter 6 — Showing Complex Data

### Sortable Table
- **Type:** technique
- **Context:** Tabular data requiring comparison and ordering
- **Solution:** Click header to sort asc/desc. Show sort indicator. Support multi-column sort for advanced cases. Keep the first row visible on scroll.
- **Consequences:** Fast data exploration. Doesn't replace filtering. Sorting alone insufficient for large sets.
- **Related:** Faceted Navigation, Pagination, Data Filter

### Infinite Scroll vs. Pagination
- **Type:** decision
- **Context:** Long lists of content items
- **Solution:** Infinite scroll for discovery-oriented browsing (social, image galleries). Pagination for task-oriented browsing (search results, product lists, tables).
- **Consequences:** Infinite scroll: smooth but hard to return to a specific item. Pagination: supports location/bookmarking but adds friction.
- **Related:** Data Table

## Chapter 7 — Getting Input

### Forgiving Input
- **Type:** principle
- **Context:** Text fields, search, data entry
- **Solution:** Accept varied formats (phone with/without dashes, case-insensitive). Apply Postel's Law: normalize on the backend, show cleaned version.
- **Consequences:** Fewer errors, happier users. More backend work.
- **Related:** Inline Validation

### Inline Validation
- **Type:** technique
- **Context:** Forms with required or format-constrained fields
- **Solution:** Validate on blur (not on each keystroke). Show error inline next to the field. Use green checkmark on success.
- **Consequences:** Immediate feedback, no submit-reload cycle. Aggressive validation before user finishes typing is jarring.
- **Related:** Forgiving Input

## Chapter 9 — Visual Style

### Visual Hierarchy
- **Type:** principle
- **Context:** Any page where some content is more important than other content
- **Solution:** Use size, weight, color, and whitespace — not just position — to lead the eye. Top-left is strongest. Make secondary content visually recessive.
- **Consequences:** Users see what matters. Poor hierarchy buries critical actions.
- **Related:** F Pattern, Gestalt Principles

### Color with Meaning
- **Type:** technique
- **Context:** Communicating status, categories, or interactivity
- **Solution:** Use consistent semantic color: red=error/destructive, green=success, blue=interactive links. Don't use color alone to convey info (add icons/text).
- **Consequences:** Faster scanning. Accessibility depends on contrast + non-color cues.
- **Related:** Visual Hierarchy
