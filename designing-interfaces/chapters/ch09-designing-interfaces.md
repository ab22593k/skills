# Chapter 9 — Visual Style and Aesthetics

## Core concepts

- Visual style communicates brand, guides attention, and supports readability
- Every visual choice must serve a purpose — decoration without meaning is noise
- Accessibility is not a constraint, it's a baseline: WCAG 2.1 AA minimum (4.5:1 contrast ratio)
- Color is a conveyor of meaning, not just decoration — use semantic color consistently
- Typography choices affect reading speed, hierarchy, and brand personality

## Frameworks introduced

- **Color theory for UI** — Use hue for meaning/category, saturation for emphasis, lightness for hierarchy. 60-30-10 rule: 60% neutral, 30% secondary, 10% accent.
- **Semantic color mapping** — Primary (brand actions), success (green), error (red), warning (yellow/amber), info (blue). Never use color alone to convey state (add icon or text).
- **Type scale** — A modular type scale (e.g., 1.25 ratio: 12 / 15 / 19 / 24 / 30 / 38 / 48px) ensures consistent hierarchy. Headline: bold. Body: regular. Caption: smaller, less contrast.
- **Accessible color contrast** — WCAG AA: 4.5:1 for normal text, 3:1 for large text. AAA: 7:1 and 4.5:1. Use contrast checkers.
- **Gestalt principles in visual design** — Proximity, similarity, closure, continuity, figure-ground — used to organize visual elements into perceived groups
- **Icon design** — Use consistent visual style (filled vs. outlined, stroke weight, corner radius). Label icons for accessibility.

## Key techniques

- **Dark mode**: Invert lightness scale, preserve saturation. Don't just invert colors. Test contrast ratios.
- **Visual noise reduction**: Every additional color, font, or icon competes for attention. Remove anything that doesn't serve the user's goal.
- **Whitespace as visual weight**: More whitespace around an element makes it feel important. Less whitespace groups related elements.
- **Color vision deficiency**: Avoid red/green only for status. Add patterns, icons, or text labels. Use tools to simulate CVD.

## Connection to other chapters

Visual style applies to every element from Ch2-Ch8. Navigation (Ch3) uses color for active states. Layout (Ch4) uses whitespace. Data (Ch6) uses semantic color. Ch10 (making it look good) builds on these foundations with spacing systems and image treatment. Design systems (Ch11) codify color and type tokens.
