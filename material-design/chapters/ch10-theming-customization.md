# Theming & Customization

## Core concepts
- Customize M3 by overriding `ThemeData` — never fight the system
- Seed color drives the entire `ColorScheme` automatically
- Flutter's `Material3Theme` (community package) provides structured token overrides

## Frameworks introduced

**Seed to ThemeData pipeline:**
```dart
ThemeData buildTheme(Color seed, Brightness brightness) {
  final scheme = ColorScheme.fromSeed(seedColor: seed, brightness: brightness);
  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    textTheme: _buildTextTheme(),
    cardTheme: CardTheme(shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12),
    )),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        shape: StadiumBorder(),
      ),
    ),
  );
}
```

**Dynamic color on Android 12+ —** Flutter automatically picks up the system dynamic color scheme. No special API needed when `useMaterial3: true`. The `ColorScheme.fromSeed` call provides a fallback for pre-Android 12 devices.

**Material Theme Builder for Flutter:** Export from the web tool → produces Dart code with `ColorScheme` definitions. Import directly into your `ThemeData`.

## Key techniques

**Full Flutter app setup:**
```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final brandSeed = const Color(0xFF6750A4);
    return MaterialApp(
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: brandSeed,
          brightness: Brightness.light,
        ),
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: brandSeed,
          brightness: Brightness.dark,
        ),
      ),
      themeMode: ThemeMode.system,
    );
  }
}
```

**Dark mode:** Never manually invert colors. Use `ColorScheme.fromSeed(seedColor:, brightness: Brightness.dark)`. Surface tones invert automatically (tone 6 for dark surfaces, tone 90 for text). `ThemeMode.system` follows the device setting.

**Brand customization beyond seed:**
```dart
// If brand has explicit secondary/tertiary
ColorScheme.fromSeed(
  seedColor: brandPrimary,
  secondary: brandSecondary,       // explicit override
  brightness: brightness,
);
```

**Material3Theme package (community):** Provides `Material3ThemeData` with structured color, typography, and shape tokens that map directly to M3 spec layers. Useful for complex token overrides beyond basic `ThemeData`.

## Expressive theming

M3 Expressive (May 2025 / Google I/O 2026) adds for Flutter:

**Check current Flutter SDK version for availability:**
- `Curves.emphasized` family — available
- `ColorScheme.surfaceContainer*` — available since Flutter 3.22
- Spring-based `AnimationController` — always available
- Expressive components (flexible nav bar, Xl buttons, FAB menus) — check latest SDK

## Connection to other chapters
Consumes `ColorScheme` (ch02), `TextTheme` (ch03), shape (ch04), motion (ch05), tokens (ch08). Platform affects component availability (ch06) and dynamic color support (ch02).
