---
name: expressive-design
description: Material Expressive. Comprehensive guidance on expressive design system for Flutter with platform support for Android and Linux desktop. Covers color tokens, typography scales, motion specifications, shape tokens, spacing ramps, and component enhancements for creating emotionally engaging UIs. Includes migration guidance from standard M3 and platform-specific integration notes. Use when Codex needs to apply expressive design to a specific widget (passed as a parameter).
---

# Material Expressive Design System

Material Expressive is Google's most researched design system update, based on 46 studies with 18,000+ participants. It creates emotionally engaging user experiences through strategic use of color, shape, size, motion, and containment.

## Workflows

### Apply Expressive Design

**Arguments:**
- `widget`: The Flutter widget code or description to be transformed.

**Steps:**

1.  **Identify Component Category**: Match the `widget` to a category in [COMPONENTS.md](references/COMPONENTS.md) (e.g., Button, Navigation, Surface, Input).
2.  **Apply Color System**: 
    - Select tonal palettes from [COLOR.md](references/COLOR.md).
    - Apply container tiers for hierarchy.
3.  **Apply Shape System**: 
    - Use expressive radii (e.g., Full, Extra Large) from [SHAPES.md](references/SHAPES.md).
    - Ensure consistent rounding for component families.
4.  **Optimize Size and Spacing**:
    - Increase touch targets to 48dp-56dp (see [SPACING.md](references/SPACING.md)).
    - Apply generous internal padding.
5.  **Inject Motion**:
    - Add energetic state transitions from [MOTION.md](references/MOTION.md).
    - Use expressive easing and durations.
6.  **Verify**: Cross-reference with [CHECKLIST.md](references/CHECKLIST.md).

## Quick Reference

| Category      | Reference                                       | Description                              |
| ------------- | ----------------------------------------------- | ---------------------------------------- |
| Foundations   | [FOUNDATIONS.md](references/FOUNDATIONS.md)     | Principles, communication, core elements |
| Checklist     | [CHECKLIST.md](references/CHECKLIST.md)         | High-density design review verification  |
| Color         | [COLOR.md](references/COLOR.md)                 | Tokens, palettes, contrast specs         |
| Typography    | [TYPOGRAPHY.md](references/TYPOGRAPHY.md)       | Scales, values, treatments               |
| Motion        | [MOTION.md](references/MOTION.md)               | Durations, easing, transitions           |
| Shapes        | [SHAPES.md](references/SHAPES.md)               | Radii, tokens, containment               |
| Spacing       | [SPACING.md](references/SPACING.md)             | Spacing ramps, touch targets             |
| Components    | [COMPONENTS.md](references/COMPONENTS.md)       | Component specifications                 |
| Usability     | [USABILITY.md](references/USABILITY.md)         | Design tactics, best practices, testing  |
| Accessibility | [ACCESSIBILITY.md](references/ACCESSIBILITY.md) | Compliance, testing                      |
| Platforms     | [PLATFORMS.md](references/PLATFORMS.md)         | Android and Linux desktop                |

## Core Expressive Elements

1. **Color** - Expanded tonal palettes, container tiers, emotional selection
2. **Shape** - Expressive radii, containment, visual boundaries
3. **Size** - Larger touch targets, visual hierarchy
4. **Motion** - Energetic transitions, emotional timing
5. **Containment** - Surface elevation, tonal separation

## When to Use M3 Expressive

- Media and entertainment applications
- Communication apps (email, messaging)
- Social platforms
- Creative tools
- Consumer-facing products

## When to Avoid M3 Expressive

- Banking and financial applications
- Safety-critical interfaces
- Healthcare and medical software
- Productivity tools requiring efficiency
- Forms-heavy applications

## Platform Support

- **Android** - Dynamic color, Android 16 integration, native behaviors
- **Linux Desktop** - Keyboard navigation, focus management, desktop interactions

## Key Research Findings

- 87% preference among 18-24 age group
- 4x faster element recognition
- 32% increase in subculture perception
- 34% boost in modernity
- Erases age-related usability gaps

## Next Steps

1. Review [FOUNDATIONS.md](references/FOUNDATIONS.md) for core principles
2. Apply systems (Color, Typography, Motion, Shapes, Spacing)
3. Implement components from [COMPONENTS.md](references/COMPONENTS.md)
4. Apply usability tactics from [USABILITY.md](references/USABILITY.md)
5. Perform final verification using [CHECKLIST.md](references/CHECKLIST.md)
6. Configure platform-specifics from [PLATFORMS.md](references/PLATFORMS.md)
