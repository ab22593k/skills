# Shape & Elevation

## Core concepts
- Shape radius communicates containment hierarchy — larger radius = more important container
- Elevation uses tonal surface colors (`ColorScheme.surfaceContainer*`) not shadows
- M3 Expressive adds a 35-shape library and updated radii

## Frameworks introduced

**Shape scale in Flutter** — 10 levels from none (0) to full (9999). Flutter's `ShapeBorder` subclasses (`RoundedRectangleBorder`, `CircleBorder`, `StadiumBorder`) map to these. Apply via widget `shape:` parameter or theme (`CardTheme(shape: ...)`).

```dart
// Flutter shape constants
ShapeBorder none = RoundedRectangleBorder(borderRadius: BorderRadius.zero);
ShapeBorder small = RoundedRectangleBorder(borderRadius: BorderRadius.circular(8));
ShapeBorder medium = RoundedRectangleBorder(borderRadius: BorderRadius.circular(12));
ShapeBorder large = RoundedRectangleBorder(borderRadius: BorderRadius.circular(20));
ShapeBorder extraLarge = RoundedRectangleBorder(borderRadius: BorderRadius.circular(32));
ShapeBorder full = StadiumBorder();
```

**Tonal elevation** — Flutter 3.22+ exposes `ColorScheme.surfaceContainerLow` through `.surfaceContainerHighest`. These replace shadow-based elevation on non-floating surfaces.

```dart
// Level mapping in Flutter
Color level0 = theme.colorScheme.surface;
Color level1 = theme.colorScheme.surfaceContainerLow;
Color level2 = theme.colorScheme.surfaceContainer;
Color level3 = theme.colorScheme.surfaceContainerHigh;
Color level4 = theme.colorScheme.surfaceContainerHighest;
```

## Key techniques

**Apply shape via theme:**
```dart
ThemeData(
  cardTheme: CardTheme(
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
  ),
  dialogTheme: DialogTheme(
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(32)),
  ),
);
```

**Elevation via surface color:**
```dart
// Instead of elevation: 2, use tonal surface
Container(
  color: Theme.of(context).colorScheme.surfaceContainerHigh,
  child: child,
);
```

**Shape morphing:** Flutter's `AnimatedContainer` handles border-radius animation automatically. Pair with `Curves.emphasized` from `Curves` for MD3-appropriate feel.

## Component shape mapping

| Widget | Shape |
|--------|-------|
| `FilledButton` / `TextButton` | `StadiumBorder` (full) |
| `Card` | 12dp rounded |
| `AlertDialog` | 32dp rounded |
| `BottomSheet` | 48dp top rounded |
| `FloatingActionButton` | 20dp rounded (56dp) |
| `Chip` | 8dp rounded |
| `TextField` | 4dp top rounded |

## Connection to other chapters
`ShapeBorder` values are design tokens (ch08). Tonal elevation depends on `ColorScheme` surface container roles (ch02). Shape morphing uses `Curves.emphasized` (ch05).
