---
chapter: 6
topic: Components
when: User needs Flutter M3 widget selection, button hierarchy, FAB sizes, navigation switching, card variants, or MaterialStateProperty usage
queries:
  [
    "FilledButton",
    "NavigationBar",
    "NavigationRail",
    "NavigationDrawer",
    "FAB",
    "Card",
    "Chip",
    "TextField",
    "MaterialStateProperty",
    "button hierarchy",
    "widget selection",
  ]
---

# Components

## Core concepts

- 30+ Material widgets implementing MD3 specifications
- Every widget color-correct for `useMaterial3: true`
- M3 Expressive adds: flexible nav bar, extra-large button, expressive lists, FAB menus, split buttons

## Frameworks introduced

**Widget categories with Flutter class names:**

**Action:** `FilledButton`, `FilledButton.tonal`, `OutlinedButton`, `TextButton`, `IconButton`, `SegmentedButton`, `FloatingActionButton` (regular = 56dp, large = 96dp, small = 40dp, `ExtendedFloatingActionButton`)
**Containment:** `Card` (with `CardVariant`), `AlertDialog`, `BottomSheet` (`showModalBottomSheet`), `showSideSheet`, `CarouselView`
**Communication:** `Badge`, `MaterialBanner`, `SnackBar`, `Tooltip`, `LinearProgressIndicator`, `CircularProgressIndicator`
**Navigation:** `NavigationBar` (bottom, compact), `NavigationRail` (side, medium), `NavigationDrawer` (side, expanded), `SearchBar`, `SearchAnchor`
**Selection:** `Checkbox`, `Switch`, `Radio`, `Slider`, `SegmentedButton`, `Chip` (`InputChip`, `FilterChip`, `ChoiceChip`, `ActionChip`, `AssistChip`)
**Text input:** `TextField` (filled/outlined), `DatePickerDialog`, `TimePickerDialog`

**FAB size decisions:**

```dart
FloatingActionButton.small()    // 40×40dp (replaces "mini")
FloatingActionButton()          // 56×56dp default
FloatingActionButton.large()    // 96×96dp for feature screens
ExtendedFloatingActionButton()  // Label + icon, on surface
```

**Navigation by window size:**

- Compact (<600dp): `NavigationBar` (3–5 destinations)
- Medium (600–839dp): `NavigationRail` (collapsed or expanded)
- Expanded (≥840dp): `NavigationDrawer`

## Key techniques

**State via MaterialStateProperty:** All Flutter M3 widgets accept uniform state overrides via `MaterialStateProperty`.

```dart
FilledButton.styleFrom(
  backgroundColor: WidgetStateProperty.resolveWith((states) {
    if (states.contains(WidgetState.disabled)) return Colors.grey;
    if (states.contains(WidgetState.hovered)) return primaryColor.withAlpha(0xCC);
    return primaryColor;
  }),
);
```

**Card selection:** Use `Card()` (filled) for default containers. Use `Card(elevation: 2)` for elevated. Use `Card(surfaceTintColor: ...)` for tonal. Flutter `Card` defaults to M3 styling when `useMaterial3: true`.

**Button hierarchy:** One primary action → `FilledButton`. Secondary → `OutlinedButton` or `TextButton`. Multiple equal → `SegmentedButton`. Destructive → `TextButton.styleFrom(foregroundColor: colorScheme.error)`.

## Connection to other chapters

Widgets consume `ColorScheme` (→ ch02), `TextTheme` (→ ch03), shape (→ ch04), motion (→ ch05). Navigation widgets connect to `LayoutBuilder` (→ ch07). States connect to `MaterialStateProperty` (→ ch01).
