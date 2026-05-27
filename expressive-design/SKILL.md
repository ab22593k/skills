---
name: expressive-design
description: "Apply Google's Material Design 3 (MD3) and M3 Expressive system in Flutter: dynamic color, responsive layout, design tokens, spring motion, 35-shape library, and 30+ accessible components. Use for Flutter theming, ColorScheme.fromSeed, adaptive LayoutBuilder, NavigationBar/Rail/Drawer, surface container elevation, Curves.emphasized, and WCAG-compliant accessibility."
---

## Core mental models

### Dynamic Color System

**When to use** — Generating accessible color palettes that adapt to user wallpaper or in-app content.
**The idea** — A source color seeds a tonal palette; algorithms derive 29+ semantic color roles that meet WCAG contrast ratios across light and dark modes.
**How to apply** — Use `ColorScheme.fromSeed(seedColor: brandPrimary)` in `ThemeData`. Flutter dynamically generates light/dark schemes from the seed for Android 12+; falls back to the seed-derived palette on other platforms. Never hardcode `Color` values — use `Theme.of(context).colorScheme.primary` everywhere.
**Pitfalls** — Content-based dynamic color requires manual source extraction via `PaletteGenerator`; always seed with a fallback color.

### Design Tokens as a Separation Layer

**When to use** — Maintaining consistent theming across your app.
**The idea** — Tokens store single source-of-truth values mapped to platform-specific implementations. In Flutter, tokens live in `ThemeData` (colors via `ColorScheme`, typography via `TextTheme`, shape via `MaterialStateProperty`).
**How to apply** — Build a lightweight token class holding seed, radii, font families. Translate into `ThemeData` via `Material3Theme` (community) or manual mapping. Change the seed once and all derivatives cascade.
**Pitfalls** — Avoid token proliferation; keep tokens at 3 layers (raw → semantic → component) and don't expose raw hex outside the token class.

### Expressive Shape Hierarchy

**When to use** — Creating visual distinction and brand personality through container shapes.
**The idea** — Shape radius communicates containment level: tighter = utilitarian, larger = elevated/important. M3 Expressive adds a 35-shape library for decorative moments.
**How to apply** — Use `ShapeBorder` subclasses (e.g. `RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))`) with semantic constants. Flutter `Card` defaults to M3 shape; override via `shape` parameter or `CardTheme`.
**Pitfalls** — Too many distinct radii in one view creates visual noise; stick to 2–3 levels per screen.

### Adaptive Layout via Window Size Classes

**When to use** — Building UIs that work across phones, tablets, foldables, and desktop.
**The idea** — Three breakpoints (compact < 600dp, medium 600–839dp, expanded ≥ 840dp) define layout shifts. Components switch per class — nav bar on compact, nav rail on medium, nav drawer on expanded.
**How to apply** — Use `WidgetsBinding.instance.platformDispatcher.views.first.physicalSize` or the `adaptive_breakpoints`/`responsive_framework` packages. Flutter's `LayoutBuilder` with `BoxConstraints.maxWidth` is the simplest idiomatic approach.
**Pitfalls** — Don't check `Platform.isX` — respond to actual window size. Foldables and desktop resize make device assumptions invalid.

### Spring-Based Motion

**When to use** — Animating component state changes with natural-feeling physics.
**The idea** — Springs respond dynamically to gesture velocity with no fixed duration. Flutter's `AnimationController` with `SpringDescription(mass, stiffness, damping)` gives direct control. M3 Expressive adds standard and bouncy schemes.
**How to apply** — Use `FlutterSlider`, `AnimatedContainer`, and implicit animations where possible. For custom work, pair `SpringDescription` with `AnimationController.drive()`. Example: `SpringDescription.withDampingRatio(0.68)` matches the MD3 standard spring.
**Pitfalls** — Avoid springs for permanent enter/exit transitions — use eased motion (300–400ms) via `Curves.emphasized` instead.

### Component State Layers

**When to use** — Communicating interactivity through consistent visual feedback.
**The idea** — Every interactive component has 6 states; each uses opacity overlays from `onSurface` at specific opacities.
**How to apply** — Flutter `Material` widget handles state layers via `MaterialStateColor` and `MaterialStateProperty`. For custom widgets, apply `InkWell` or `InkResponse` which implement the MD3 state layer spec. Never change base color — overlay only.
**Pitfalls** — Disabled state (38% opacity) can fail contrast checks if base color is too light. Test with `SemanticsDebugger`.

### Tonal Elevation (Not Shadows)

**When to use** — Communicating surface hierarchy without drop shadows.
**The idea** — Higher surfaces get lighter tonal fills via surface container color levels. Shadows only for floating elements over busy content.
**How to apply** — Use `ColorScheme.surfaceContainerLow` through `.surfaceContainerHighest` for surface levels. Flutter 3.22+ exposes these in `ColorScheme`. Reserve `elevation` parameter on `Material` for FABs, dialogs, menus over images.
**Pitfalls** — Mixing tonal elevation with shadows creates conflicting depth cues; pick one system per surface.

## Query routing

When a user asks about a M3/Flutter topic, load the corresponding chapter:

| User asks about... | Load this chapter |
|---|---|
| Theme generation, brand color → `ThemeData`, dark mode, Material Theme Builder | ch10 |
| `ColorScheme.fromSeed`, dynamic color, tonal palettes, color roles | ch02 |
| Responsive layout, `LayoutBuilder`, window size classes, navigation switching | ch07 |
| NavigationBar / Rail / Drawer, FAB, Cards, Dialogs, Buttons, Chips, TextField | ch06 |
| `TextTheme`, Google Fonts, brand vs plain typefaces, type scale | ch03 |
| Shape radii, `ShapeBorder`, tonal elevation, `surfaceContainer*` | ch04 |
| `Curves.emphasized`, spring physics, `AnimationController`, `AnimatedContainer` | ch05 |
| `Semantics`, contrast ratios, touch targets, `SemanticsDebugger`, a11y checklist | ch09 |
| Design token architecture, custom token class, `ThemeData` extension | ch08 |
| Interaction states, state layers, `InkWell`, MD3 principles, widget selection | ch01 |
| Implementation patterns, anti-patterns, decision trees | patterns.md |
| Quick code snippets, radius/opacity/easing reference tables | cheatsheet.md |
| M3 term definitions, Flutter API name lookup | glossary.md |

## Chapter index

| #   | Title                   | Topic                                                             | Best for |
| --- | ----------------------- | ----------------------------------------------------------------- | -------- |
| 01  | Foundations             | Principles, accessibility, interaction states, usability          | MD3 overview, state layer pattern, widget selection guidance |
| 02  | Color System            | Dynamic color, tonal palettes, color roles, Flutter `ColorScheme` | Accessible palette generation, `ColorScheme.fromSeed`, brand-to-seed mapping |
| 03  | Typography              | Type scale, `TextTheme`, brand vs plain, Google Fonts in Flutter  | Custom type scales, Google Fonts setup, emphasized type, component type mapping |
| 04  | Shape & Elevation       | Corner radii, `ShapeBorder`, tonal elevation, Flutter `Material`  | Shape radius decisions, `surfaceContainer*` elevation, shape morphing |
| 05  | Motion                  | Spring physics, `AnimationController`, `Curves.emphasized`        | Spring vs eased motion, implicit animations, enter/exit transitions |
| 06  | Components              | All 30+ widgets with Flutter class names and usage                | Widget selection, button hierarchy, FAB sizes, navigation switching |
| 07  | Layout & Navigation     | `LayoutBuilder`, breakpoints, `NavigationBar`/`Rail`/`Drawer`     | Responsive scaffolds, canonical layouts, edge-to-edge, foldable support |
| 08  | Design Tokens           | Token architecture, `TokenTheme` extension, platform mapping      | Custom token class, 3-layer architecture, `ThemeData` extension |
| 09  | Accessibility           | `Semantics`, contrast, `MediaQuery`, `MergeSemantics`             | Contrast auditing, `SemanticsDebugger`, focus navigation, touch targets |
| 10  | Theming & Customization | Seed-to-`ThemeData`, `Material3Theme`, dark mode, Expressive      | Full app theme setup, dark mode, brand customization beyond seed, Expressive theming |
