# Patterns

## Seed-to-ThemeData Pipeline
**Type:** technique
**Context:** You have a brand color and need a complete Flutter theme across light + dark.
**Solution:**
```dart
ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(
    seedColor: brandPrimary,
    brightness: Brightness.light,
  ),
);
// Dark: same seed, brightness: Brightness.dark
```
Map additional brand colors via `secondary:` / `tertiary:` parameters. Set both `theme` and `darkTheme` on `MaterialApp`. Use `ThemeMode.system` to follow device preference.
**Consequences:** Automatic accessible palette. Light/dark generated from same seed. Tertiary auto-generated unless overridden.
**Related:** Dynamic Color System (SKILL.md), Theming (→ ch10)

## State Layer Overlay Pattern
**Type:** technique
**Context:** Communicating component interactivity consistently without changing base colors.
**Solution:** Let Flutter's `Material` widget handle overlays automatically. For custom widgets, wrap in `InkWell` or `InkResponse`. For state-specific styling, use `WidgetStateProperty.resolveWith`.
```dart
style: ButtonStyle(
  backgroundColor: WidgetStateProperty.resolveWith((states) {
    if (states.contains(WidgetState.disabled)) return Colors.grey.withAlpha(97);
    if (states.contains(WidgetState.hovered)) return primaryColor.withAlpha(20);
    return primaryColor;
  }),
);
```
**Consequences:** Consistent state behavior across all widgets. Contrast ratios stay predictable.
**Related:** Interaction States (→ ch01), Component States (→ ch06)

## Responsive Navigation Switch
**Type:** technique
**Context:** Your Flutter app needs navigation that works across phone, tablet, and desktop.
**Solution:**
```dart
LayoutBuilder(builder: (context, constraints) {
  final width = constraints.maxWidth;
  if (width < 600) return _CompactShell();
  if (width < 840) return _MediumShell();
  return _ExpandedShell();
});
```
Compact → `NavigationBar` (bottom), Medium → `NavigationRail` (side), Expanded → `NavigationDrawer`. Wire destinations once, shell switches per class.
**Consequences:** Single destination definition, three visual presentations. Works on foldables and desktop.
**Related:** Window Size Classes (→ ch07), Navigation Widgets (→ ch06)

## Surface Container Elevation
**Type:** principle
**Context:** Creating visual hierarchy between surfaces without drop shadows.
**Solution:** Use `ColorScheme.surfaceContainerLow` through `surfaceContainerHighest` instead of `elevation` on `Material`. Only use `elevation` for FABs, dialogs, and menus over visually busy content.
```dart
Container(
  color: Theme.of(context).colorScheme.surfaceContainerHigh,
  child: child,
);
```
**Consequences:** Cleaner visual hierarchy. Works in light and dark modes. No shadow rendering overhead.
**Pitfalls:** Mixing tonal elevation + shadows creates conflicting depth cues. Pick one system per surface.
**Related:** Tonal Elevation (→ ch04), Color Roles (→ ch02)

## Brand Theme Customization
**Type:** technique
**Context:** Customizing M3 for a specific brand while staying within the design system.
**Solution:** 1) Set brand primary as `ColorScheme.fromSeed(seedColor:)` 2) Override `TextTheme` via `GoogleFonts.interTextTheme()` 3) Set `CardTheme`, `FilledButtonTheme`, etc. for shape 4) Keep all other tokens as defaults. Use Material Theme Builder to preview → export Dart code.
```dart
ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(seedColor: brandPrimary),
  textTheme: GoogleFonts.playfairDisplayTextTheme(),
  cardTheme: CardTheme(shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(12),
  )),
);
```
**Consequences:** Brand identity expressed through M3. Light/dark modes, dynamic color, and accessibility preserved.
**Related:** Theming (→ ch10), Design Tokens (→ ch08)

## Content-Based Dynamic Color
**Type:** technique
**Context:** A Flutter media app that should adapt to current content (album art, photo).
**Solution:** Use `PaletteGenerator` from the `palette_generator` package to extract dominant colors.
```dart
final PaletteGenerator palette = await PaletteGenerator.fromImageProvider(
  NetworkImage(albumArtUrl),
);
final Color? dominant = palette.dominantColor?.color;
setState(() => _seedColor = dominant ?? fallbackColor);
// Then: ColorScheme.fromSeed(seedColor: _seedColor)
```
Apply scheme only to content-adjacent area, not navigation chrome. Fall back to baseline when no content.
**Consequences:** Visually coherent content presentation. More effort than user-generated color.
**Related:** Dynamic Color (→ ch02), Color Roles (→ ch02)

## Anti-pattern: Hardcoded Color Values
**Type:** anti-pattern
**Context:** Using `Color(0xFF...)` literals in widget build methods instead of semantic color roles.
**Solution:** Never write `color: Color(0xFF1A73E8)` — use `Theme.of(context).colorScheme.primary`. If needing a non-standard color, add a custom `ColorScheme` override or an extension getter.
**Consequences:** Theme changes propagate automatically. Consistent color intent across the app.
**Related:** Design Tokens (→ ch08), Color System (→ ch02)

## Anti-pattern: Device-Based Layout
**Type:** anti-pattern
**Context:** Using `Platform.isAndroid` or `Platform.isIOS` to determine layout.
**Solution:** Use `LayoutBuilder` to respond to actual available width. Flutter runs on foldables, desktop, web — device assumptions are invalid.
```dart
// Bad
if (Platform.isAndroid) _compactLayout();

// Good
LayoutBuilder(builder: (_, c) => c.maxWidth < 600 ? _compactLayout() : ...);
```
**Consequences:** Layout correctly adapts to resize, multi-window, foldable hinge. Future-proof for new form factors.
**Related:** Adaptive Layout (→ ch07), Layout Patterns (→ ch07)

## Choosing Widget Shape
**Type:** decision tree
**Context:** Determining what `ShapeBorder` to use for a custom widget.
**Solution:** Identify containment level: container (card) → `RoundedRectangleBorder(12)`, overlay (dialog) → `RoundedRectangleBorder(32)`, input (field) → `RoundedRectangleBorder(top: 4)`, floating action (FAB) → `RoundedRectangleBorder(20)`, single action (button) → `StadiumBorder()`.
**Consequences:** Consistent shape language. Users intuitively understand containment relationships.
**Related:** Shape Scale (→ ch04), Component Shape Mapping (→ ch04)

## Spring vs Eased Motion in Flutter
**Type:** decision tree
**Context:** Choosing between spring physics and easing curves for an animation.
**Solution:** If the element tracks a gesture (drag, fling) → `SpringDescription.withDampingRatio(0.68)` via `SpringSimulation`. If the element transitions between fixed states (enter, exit, move) → `Curves.emphasized` with `AnimatedContainer` or `TweenAnimationBuilder`. If the widget has an implicit animation variant (`AnimatedOpacity`, `AnimatedScale`) → prefer that with `curve: Curves.emphasized`.
**Consequences:** Springs = interactive input-driven feel. Eased = predictable transitions.
**Related:** Motion (→ ch05), Implicit Animations (→ ch05)
