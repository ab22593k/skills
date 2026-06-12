# Chapter 3 — Getting Around

## Core concepts

- Navigation must answer: Where am I? Where can I go? How do I get back?
- Persistent navigation (global nav, tabs) + contextual navigation (links, breadcrumbs) work together
- Flat navigation (all top-level) works for apps with few sections; hierarchical works for deep content
- Reduce navigation friction: Fitts's Law makes large targets near edges fast

## Frameworks introduced

- **Tab bar** — For 3-7 peer sections users switch between frequently. Active tab visually distinct. Mobile: bottom tab bar.
- **Breadcrumbs** — Show path depth; users can jump up levels. Use `>`, not `/`. Truncate deep paths.
- **Stepper / Wizard** — Sequential steps with progress + current step highlighted. Allow returning to completed steps.
- **Accordion** — Vertical stack of expandable panels. Good for FAQ and settings. Avoid nesting.
- **Contextual navigation** — Inline links, "related" sections, "next steps" that adapt to current content
- **Hamburger menu** — Use sparingly; hides navigation behind an icon. Prefer visible tabs when possible.

## Key techniques

- **Navigation audit**: List every page, its inbound links, and whether they're visually accessible
- **Mobile-first nav**: Start with mobile constraints (bottom tabs, hamburger), expand to desktop
- **Mega menu**: Large dropdown with categorized links for deep-content sites on desktop
- **Back vs. Up**: "Back" returns to previous screen (browser history); "Up" goes to parent in hierarchy

## Connection to other chapters

Navigation structure depends on information architecture (Ch2). Mobile navigation patterns (Ch8) extend these concepts. Visual hierarchy (Ch9) determines whether navigation elements are noticed. Design systems (Ch11) standardize navigation components.
