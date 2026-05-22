# Chapter 10 — Making It Look Good

## Core concepts
- Craft is in the details: alignment, spacing, and sizing consistency separate amateur from professional
- A grid system (12-column, 8px base spacing) enforces visual rhythm
- Images need consistent treatment: aspect ratio, border radius, placeholder handling
- Responsive design is not just fluid widths — it restructures content at breakpoints
- Consistency across a product builds trust — use a spacing scale and type system

## Frameworks introduced
- **Grid system** — 12-column flexible grid with fixed gutters. Column count collapses at breakpoints: 4 (mobile), 8 (tablet), 12 (desktop). Baselines can be 4px, 8px, or 12px.
- **Spacing scale** — A geometric progression (4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96px) for consistent whitespace. Every margin and padding picks from this scale.
- **Image aspect ratio** — Consistent ratio (e.g., 16:9, 4:3, 1:1) for all content images. Use object-fit CSS. Add placeholder skeleton before load.
- **Drop shadow / Elevation** — Layered z-depths (0, 1, 2, 4, 8, 16dp) for cards, modals, dropdowns. Only use shadows to indicate elevation, not decoration.
- **Content-out vs. layout-in** — Content-out: layout adjusts to content (best for text). Layout-in: content fills defined boxes (best for galleries/dashboards).

## Key techniques
- **Optical alignment**: Align text by its visual center (typically the cap height), not the bounding box. Center icons visually with text.
- **Pairing fonts**: One heading font + one body font maximum. Avoid system default stacking without tuning line-height.
- **Loading states**: Skeleton screens (gray rectangular placeholders) over spinners. Gives the impression of speed.
- **Empty states**: Every data view needs an empty state with an illustration, explanation, and suggested action.
- **Responsive images**: Serve appropriate resolution per viewport. Use srcset and sizes attributes. Lazy load below-fold images.

## Connection to other chapters
Ch10 implements the visual principles from Ch9 into concrete systems: spacing, grids, image treatment. Layout patterns (Ch4) use these grids. Mobile (Ch8) determines breakpoint choices. Design systems (Ch11) formalize spacing, grid, and typography tokens from Ch10's practices.
