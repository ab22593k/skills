---
name: expressive-design
description: Material 3 Expressive design system for Flutter (Android & Linux). You MUST use this skill whenever the user asks to improve, modernize, or transform a Flutter UI, especially for consumer, media, or communication apps. It provides exact specs for Bento Grids, Masonry, color convergence, variable fonts, and expressive motion. Trigger this for any request involving 'modern' or 'emotionally engaging' Flutter widgets, even if they don't explicitly mention 'Expressive' design. Do NOT use for banking or safety-critical apps where standard M3 is required.
---

# Material Expressive Design System

Material Expressive is Google's most researched design system update, based on 46 studies with 18,000+ participants. It creates emotionally engaging user experiences through strategic use of layout patterns, color, shape, size, motion, and containment.

## Core Expressive Elements

1. **Layout Patterns** - Modular grids (Bento), masonry, card-based, split-screen, and specialized page structures.
2. **Color & Typography** - Expanded tonal palettes, container tiers, emotional selection, and dynamic convergence. Utilizing variable fonts (like Roboto Flex) for flexible text weight and width.
3. **Shape** - Expanded library of 35 shapes, expressive radii, containment, visual boundaries, and built-in shape morph motion for decorative visual elements.
4. **Size** - Larger touch targets, visual hierarchy. Reintroduces clear functional signifiers to reduce user uncertainty and improve scanning speed.
5. **Motion** - New physics-based motion system including spatial springs for realistic object movement and effects springs for seamless color/opacity transitions.
6. **Containment** - Surface elevation, tonal separation.
7. **New & Updated Components** - Flexible Toolbars, Split Buttons, Progress Indicators (with customizable waveforms and thickness), Button Groups (shape-shifting interactions), and FAB Menus (overflow into mini-menus).

## Workflows

### Apply Expressive Design

**Arguments:**
- `widget`: The Flutter widget code or description to be transformed.

**Steps:**

1.  **Select Layout Pattern**: 
    - Read [PATTERNS.md](references/PATTERNS.md) to choose a pattern based on the UI's purpose (e.g., Bento Grid for dashboards, Masonry for portfolios). Apply the grid/structure to the `widget`.
2.  **Identify Component Category**: Match the `widget` to a category in [COMPONENTS.md](references/COMPONENTS.md) (e.g., Button, Navigation, Surface, Input).
3.  **Apply Color System**: 
    - Read [COLOR.md](references/COLOR.md) to select tonal palettes and apply container tiers for hierarchy.
    - **Apply Color Convergence**: Merge brand identity with user settings using harmonization and `ThemeExtension` (see [PLATFORMS.md](references/PLATFORMS.md)).
4.  **Apply Shape System**: 
    - Read [SHAPES.md](references/SHAPES.md) to use expressive radii (e.g., Full, Extra Large). Ensure consistent rounding for component families.
5.  **Optimize Size and Spacing**:
    - Read [SPACING.md](references/SPACING.md) to increase touch targets to 48dp-56dp and apply generous internal padding.
6.  **Inject Motion**:
    - Read [MOTION.md](references/MOTION.md) to add energetic state transitions and use expressive easing and durations.
7.  **Verify**: Cross-reference with [CHECKLIST.md](references/CHECKLIST.md).

## Topic References

Load these references only when working on a specific aspect of the design system:

- **Foundations & Principles**: Core principles, communication, and when to use. See [FOUNDATIONS.md](references/FOUNDATIONS.md).
- **Usability**: Design tactics, best practices, and testing. See [USABILITY.md](references/USABILITY.md).
- **Typography**: Scales, values, and type treatments. See [TYPOGRAPHY.md](references/TYPOGRAPHY.md).
- **Accessibility**: Compliance, screen reader compatibility, and testing. See [ACCESSIBILITY.md](references/ACCESSIBILITY.md).
- **Layout Patterns**: Bento grid, masonry, cards, hero sections, and page structures. See [PATTERNS.md](references/PATTERNS.md).
- **Platform Specifics**: Android (Dynamic Color, Android 16) and Linux Desktop integration. See [PLATFORMS.md](references/PLATFORMS.md).
