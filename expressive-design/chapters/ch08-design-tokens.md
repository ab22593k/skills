---
chapter: 8
topic: Design Tokens
when: User needs token architecture, custom token class, ThemeData extension, or the 3-layer reference/system/component token model
queries:
  [
    "design token",
    "token architecture",
    "custom token class",
    "ThemeData extension",
    "reference token",
    "system token",
    "component token",
    "token layers",
  ]
---

# Design Tokens

## Core concepts

- Tokens are single source-of-truth values for every visual attribute
- Three-layer architecture: Reference → System → Component
- In Flutter, `ThemeData` is the token system container

## Frameworks introduced

**Token architecture —** Reference tokens are raw values (e.g., brand hex, font file path). System tokens are semantic (`ColorScheme.primary`, `TextTheme.bodyLarge`). Component tokens bridge system to widget-specific properties (`FilledButtonTheme.style`).

**Token categories in Flutter:**

- **Color:** `ColorScheme` (29+ roles)
- **Typography:** `TextTheme` (15+ `TextStyle` values)
- **Shape:** Per-theme properties (`CardTheme.shape`, `DialogTheme.shape`)
- **Elevation:** `ColorScheme.surfaceContainer*` (tonal) + `Material.elevation` (shadow)
- **Spacing:** Not a built-in token — define custom `EdgeInsets` constants from an 8dp base
- **Motion:** `Curves` (easing) + `Duration` constants

**Flutter theme inheritance:**

```dart
ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: brandPrimary),
  textTheme: GoogleFonts.interTextTheme(),
  cardTheme: CardTheme(shape: RoundedRectangleBorder(...)),
  filledButtonTheme: FilledButtonThemeData(
    style: FilledButton.styleFrom(shape: ...),
  ),
);
```

## Key techniques

**Custom token class:** Extract raw values into a constants class for reuse.

```dart
class AppTokens {
  static const Color seedColor = Color(0xFF1A73E8);
  static const double cardRadius = 12;
  static const double dialogRadius = 32;
  static const EdgeInsets pageMargin = EdgeInsets.all(16);
  static const Duration motionMedium = Duration(milliseconds: 300);
  static const Curve emphasized = Curves.emphasized;
}
```

**ThemeData extension:** Access tokens consistently.

```dart
extension TokenX on ThemeData {
  Color get surfaceContainerHigh => colorScheme.surfaceContainerHigh;
  ShapeBorder get cardShape => RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(AppTokens.cardRadius),
  );
}
```

**Dark mode:** Generate both schemes from the same seed.

```dart
ThemeData lightTheme(Color seed) => ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(seedColor: seed, brightness: Brightness.light),
);
ThemeData darkTheme(Color seed) => ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(seedColor: seed, brightness: Brightness.dark),
);
```

## Reference table

| Token Layer | Flutter container                     | Example               |
| ----------- | ------------------------------------- | --------------------- |
| Reference   | Constants class                       | `AppTokens.seedColor` |
| System      | `ThemeData.colorScheme` / `textTheme` | `colorScheme.primary` |
| Component   | `XxxTheme` / `XxxThemeData`           | `CardTheme.shape`     |

## Connection to other chapters

Color tokens (→ ch02), type tokens (→ ch03), shape tokens (→ ch04), motion tokens (→ ch05). Token customization via `ThemeData` (→ ch10).
