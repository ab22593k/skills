---
chapter: 3
topic: Typography
when: User needs custom type scales, Google Fonts setup, emphasized type styles, brand vs plain typefaces, or component type mapping
queries:
  [
    "TextTheme",
    "Google Fonts",
    "type scale",
    "emphasized type",
    "brand font",
    "component text style",
    "font family",
  ]
---

# Typography

## Core concepts

- 15 baseline type styles in 5 categories × 3 sizes: Display, Headline, Title, Body, Label
- 15 emphasized variants (increase weight by 100) for selection, primary actions, unread badges
- Two typeface roles: Brand (Display, Headline) and Plain (Title, Body, Label)

## Frameworks introduced

**Flutter TextTheme** — `TextTheme` holds all 15+ type styles. Accessed via `Theme.of(context).textTheme`. Each property returns a `TextStyle`. Default: Google's Roboto font. Override via `ThemeData(textTheme: ...)` or the `google_fonts` package.

**Baseline styles in Flutter:**

```dart
TextTheme(
  displayLarge: const TextStyle(fontSize: 57, fontWeight: FontWeight.w400),
  displayMedium: const TextStyle(fontSize: 45, fontWeight: FontWeight.w400),
  headlineLarge: const TextStyle(fontSize: 32, fontWeight: FontWeight.w400),
  titleLarge: const TextStyle(fontSize: 22, fontWeight: FontWeight.w400),
  titleMedium: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
  bodyLarge: const TextStyle(fontSize: 16, fontWeight: FontWeight.w400),
  bodyMedium: const TextStyle(fontSize: 14, fontWeight: FontWeight.w400),
  labelLarge: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500),
  labelSmall: const TextStyle(fontSize: 11, fontWeight: FontWeight.w500),
);
```

**Google Fonts in Flutter:**

```dart
// pubspec.yaml: google_fonts: ^6.x
ThemeData(
  textTheme: GoogleFonts.interTextTheme(),
  // Or per-style:
  textTheme: TextTheme(
    displayLarge: GoogleFonts.playfairDisplay(),
    bodyLarge: GoogleFonts.inter(),
  ),
);
```

## Key techniques

**Brand + Plain typefaces:** Apply brand typeface to Display/Headline via custom `TextStyle`, plain to Title/Body/Label. Flutter doesn't enforce the two-role separation — you must manually compose.

**Emphasized styles:** Increase weight by 100. Flutter does not ship emphasized variants as separate `TextTheme` properties; apply manually: `textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700)`.

**Custom typeface:** Use `ThemeData(fontFamily: 'Inter')` to set a global font, or `google_fonts` for per-style control.

## Component type mapping

| Widget              | TextTheme style |
| ------------------- | --------------- |
| `TextButton`        | `labelLarge`    |
| `Card` title        | `titleMedium`   |
| `AppBar` title      | `titleLarge`    |
| `AlertDialog` title | `headlineSmall` |
| `Chip` label        | `labelLarge`    |
| `TextField` input   | `bodyLarge`     |
| `SnackBar`          | `bodyMedium`    |

## Connection to other chapters

`TextTheme` is set in `ThemeData` (→ ch10). Readability affects accessibility (→ ch09). Component-specific usage links to each widget (→ ch06).
