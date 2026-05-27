# Color System

## Core concepts
- Color roles are semantic — use `Theme.of(context).colorScheme.primary` not a literal `Color(0xFF...`
- 29+ color roles in Flutter's `ColorScheme` class: primary, secondary, tertiary, surface, error + container variants
- Dynamic color derives a full accessible palette from a single seed color

## Frameworks introduced

**Dynamic color** — Source color seeds a tonal palette. Flutter's `ColorScheme.fromSeed(seedColor:)` generates the complete light scheme; pass `brightness: Brightness.dark` for dark. On Android 12+, `MaterialApp` can read the wallpaper-based dynamic color automatically.

**Tonal palettes** — 13 tones per hue (0–100). Key tones define primary (40 light / 80 dark), on-primary (100 light / 20 dark), and container roles (90 light / 30 dark).

**ColorScheme in Flutter** — `ColorScheme` is the authoritative color source for all Material widgets. Exposed via `Theme.of(context).colorScheme`. Contains `.primary`, `.onPrimary`, `.primaryContainer`, `.onPrimaryContainer`, `.secondary`, `.tertiary`, `.surface`, `.error`, and more.

## Key techniques

**Generate a Flutter theme from seed:**
```dart
final ColorScheme lightScheme = ColorScheme.fromSeed(
  seedColor: const Color(0xFF1A73E8),
  brightness: Brightness.light,
);
final ColorScheme darkScheme = ColorScheme.fromSeed(
  seedColor: const Color(0xFF1A73E8),
  brightness: Brightness.dark,
);
```

**Dynamic color on Android 12+:**
```dart
bool useDynamic = true; // Platform check or user toggle
ColorScheme colorScheme;
if (useDynamic && Theme.of(context).platform == TargetPlatform.android) {
  // Flutter automatically picks up dynamic color when useMaterial3: true
  colorScheme = ColorScheme.fromSeed(seedColor: Colors.blue);
} else {
  colorScheme = ColorScheme.fromSeed(seedColor: brandColor);
}
```

**Brand color mapping:** Map brand primary → seed. Map brand secondary → `ColorScheme.fromSeed(secondary: brandSecondary)`. Never hardcode roles — always go through the scheme.

## Reference table

| ColorScheme property | M3 Role | Typical light tone |
|---------------------|---------|-------------------|
| `primary` | Primary | 40 |
| `onPrimary` | Text/icons on primary | 100 |
| `primaryContainer` | Container fill | 90 |
| `secondary` | Secondary | 40 |
| `surface` | Surface / backgrounds | 98 |
| `surfaceContainerLow` → `highest` | Elevation levels L0–L5 | 96 → 90 |
| `onSurface` | Text on surface | 10 |
| `error` | Error | 40 |

## Connection to other chapters
`ColorScheme` consumed by every widget (ch06). Tonal elevation via surface containers (ch04). Contrast to accessibility (ch09). Theme generation (ch10).
