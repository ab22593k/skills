name: expressive-design
description: Material 3 Expressive (M3E) design system for Flutter. You MUST use this skill whenever the user asks to "modernize," "polish," "elevate," or create an "emotionally engaging" UI. It transforms standard Material 3 into a premium, editorial-style experience using Bento Grids, Masonry layouts, Variable Fonts (Roboto Flex), and Spring Physics motion. Trigger this for any consumer-facing, media, or communication app request, even if they don't explicitly mention "Expressive" design. Do NOT use for high-density enterprise data tables or safety-critical apps where standard utilitarian M3 is required.

# Material 3 Expressive (M3E)

Material 3 Expressive is the high-impact evolution of Google's design system. It moves beyond utility to create emotional resonance through **Bento Grids**, **Variable Typography**, **Color Convergence**, and **Spring Physics**.

## Core Workflows

### 1. Construct Bento Hierarchy
*Use this when the UI needs to showcase multiple features or data points with clear priority.*

1.  **Define Visual Loudness**: Assign a "loudness" level to each content block (Loud, Medium, Quiet).
2.  **Size Mapping**: 
    - **Loud**: 2x2 or full-width cells. High-contrast containers.
    - **Medium**: 1x2 or 2x1 cells. Tonal containers.
    - **Quiet**: 1x1 cells. Surface containers.
3.  **Implementation**: Use `flutter_staggered_grid_view` or `CustomMultiChildLayout`. Apply 16dp-24dp gaps and 28dp-32dp corner radii to cells.

### 2. Implement Variable Typography
*Use this for "Editorial Moments" (Hero sections, onboarding, headlines).*

1.  **Select Font**: Use `Roboto Flex` (variable font).
2.  **Define Axis values**: 
    - **Weight (`wght`)**: 100-1000 for precise emphasis.
    - **Width (`wdth`)**: 25-150% to fit headlines perfectly.
    - **Optical Size (`opsz`)**: 8-144 for readability at any scale.
3.  **Flutter Code**:
    ```dart
    Text('Editorial Headline', style: TextStyle(
      fontFamily: 'RobotoFlex',
      fontVariations: [FontVariation('wght', 850), FontVariation('wdth', 115)],
    ))
    ```

### 3. Apply Color Convergence
*Use this to blend Brand Identity with User Dynamic Color.*

1.  **Identify Brand Anchors**: Keep primary brand colors as "Anchors" (don't harmonize).
2.  **Apply Surface Bleed**: Tint background surfaces with a 5-8% opacity of the Dynamic Primary color.
3.  **Vibrant Schemes**: Use the `Vibrant` tonal palette for accents to create a "glowing" effect against dark/neutral surfaces.

### 4. Inject Spring Motion
*Use this for all primary transitions to replace robotic cubic-bezier curves.*

1.  **Choose Scheme**:
    - **Expressive**: High stiffness, low damping (overshoot/bounce). For FABs, Dialogs.
    - **Standard**: High damping, no overshoot. For list updates, subtle toggles.
2.  **Apply Spring Simulation**:
    ```dart
    // stiffness: 300, damping: 20
    final simulation = SpringSimulation(SpringDescription(mass: 1, stiffness: 300, damping: 20), 0, 1, 0);
    ```

## Layout Patterns

### Bento Grid (Modular)
- **Best For**: Dashboards, feature showcases, Apple-style "Pro" summaries.
- **Key Spec**: Unified external margin (24dp), internal gaps (16dp), varied cell aspect ratios.

### Masonry (Rhythmic)
- **Best For**: Image feeds, note-taking apps, mood boards.
- **Key Spec**: Fixed column count (2 or 3), variable height, staggered start.

### Editorial Hero
- **Best For**: Landing pages, article headers.
- **Key Spec**: Large Variable Headline (`wght`: 900), full-bleed background, "Surface Bleed" color convergence.

## Resource References

- **Patterns & Grids**: [PATTERNS.md](references/PATTERNS.md) (Updated M3E Specs)
- **Variable Type**: [TYPOGRAPHY.md](references/TYPOGRAPHY.md) (Roboto Flex Axis Guide)
- **Spring Motion**: [MOTION.md](references/MOTION.md) (Physics Tokens)
- **Convergence**: [COLOR.md](references/COLOR.md) (Surface Bleed Logic)
- **Component Specs**: [COMPONENTS.md](references/COMPONENTS.md)
- **Quality Audit**: [CHECKLIST.md](references/CHECKLIST.md)
