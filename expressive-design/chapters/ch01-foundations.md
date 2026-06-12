---
chapter: 1
topic: Foundations
when: User needs an MD3 overview, state layer patterns, widget selection guidance, or understanding of Material as a design system in Flutter
queries:
  [
    "MD3 overview",
    "state layers",
    "InkWell",
    "MaterialApp setup",
    "M3 vs M2",
    "widget naming migration",
  ]
---

# Foundations

## Core concepts

- M3 is Google's design system; Flutter's Material library implements it with `useMaterial3: true` (default since Flutter 3.x)
- Three pillars: Foundations (basics), Styles (color/type/shape/motion), Components (30+ widgets)
- Flutter's widget tree mirrors the M3 component hierarchy automatically

## Frameworks introduced

**Material as a design system in Flutter** — `MaterialApp` configures the complete M3 environment. `ThemeData` holds all design decisions. Widgets like `FilledButton`, `NavigationBar`, and `Card` read their styling from `MaterialTheme` — no manual wiring needed.

**Accessibility by default** — Flutter's Material widgets embed WCAG-compliant contrast, focus, and screen-reader markup via `Semantics`. Use `FlutterSemanticsDebugger` to audit.

**Interaction states** — Flutter's `Material` widget implements the MD3 state layer spec natively. `InkWell`, `InkResponse`, and `MaterialStateProperty` handle hover=8%, focus=12%, pressed=12%, dragged=16% overlays.

## Key techniques

**State layer pattern:** Apply `Material(color: theme.colorScheme.surface, child: InkWell(...))`. The `InkWell` resolves state overlays from `ThemeData.useMaterial3` — no manual opacity calculation.

**M3 widget selection:** Flutter 3.x renamed many widgets: `FlatButton` → `TextButton`, `RaisedButton` → `FilledButton`, `OutlineButton` → `OutlinedButton`. Use the M3 variants only.

**Customizing Material:** Override `ThemeData` properties. Flutter's theme system merges component themes (`FilledButtonTheme`, `CardTheme`) with the global `colorScheme`. Override at the component theme level for targeted changes.

## Connection to other chapters

Accessibility connects to color contrast (→ ch02) and `Semantics` (→ ch09). States connect to `MaterialStateProperty` (→ ch06). Layout foundations connect to `LayoutBuilder` (→ ch07). Branding connects to theme generation (→ ch10).
