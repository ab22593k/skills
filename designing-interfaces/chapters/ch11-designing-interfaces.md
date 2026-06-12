# Chapter 11 — UI Systems and Atomic Design

## Core concepts

- A design system is a living product, not a one-time deliverable — it requires maintenance and governance
- Atomic Design (Brad Frost): atoms (buttons, inputs) → molecules (search form) → organisms (header) → templates (page layout) → pages (specific instances)
- Design tokens (color values, spacing, type scale) are the single source of truth for visual consistency
- Component documentation is as important as the components themselves: usage guidelines, dos and don'ts, code examples
- Systems scale through composition, not creation — build small reusable pieces

## Frameworks introduced

- **Atomic Design** — Systematic hierarchy from atoms to pages. Each level is a composable building block. Enforces consistency through reuse.
- **Design tokens** — Named variables for every design decision: `--color-primary: #0055ff`, `--space-md: 16px`, `--font-body: Inter/400/16px/1.5`. Platform-agnostic (JSON/YAML) → translated to each tech stack.
- **Component documentation** — Name, description, usage guidelines, states (default, hover, active, disabled, error, loading), accessibility notes, code example, design spec.
- **Pattern library vs. style guide vs. design system** — Pattern library: reusable UI patterns. Style guide: visual standards. Design system: patterns + guidelines + tools + governance.
- **Governance model** — Centralized (design systems team owns all changes) vs. federated (teams contribute back). Centralized first, federated as maturity grows.

## Key techniques

- **Component audit**: Inventory every UI component across the product. Identify duplicates, inconsistencies, and gaps.
- **Figma ↔ code sync**: Design tokens as the bridge. Generate CSS custom properties from design tokens. Use tools to keep design and code in sync.
- **Versioning**: Semantic versioning for the design system. Breaking changes go in major releases. Communicate changes via changelog.
- **Adoption strategy**: Identify the top 5 most-used components, build them first. Provide migration guides. Measure adoption rate.
- **Contribution model**: Define how teams request new components, propose changes, and contribute back to the system.

## Connection to other chapters

Ch11 codifies everything from Ch2-Ch10 into a reusable system. It depends on consistent visual hierarchy (Ch9), grids and spacing (Ch10), and component patterns (Ch3-Ch7). Smart systems (Ch12) may extend the design system with contextual and behavioral patterns.
