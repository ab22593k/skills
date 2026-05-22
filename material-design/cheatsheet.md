# Cheatsheet

## Choosing Navigation Widget
| Window Width | Widget | Flutter class |
|-------------|--------|---------------|
| <600dp | Navigation bar | `NavigationBar` (bottom) |
| 600–839dp | Navigation rail | `NavigationRail` (side) |
| ≥840dp | Navigation drawer | `NavigationDrawer` (side) |

## ColorScheme Roles Quick Reference
| Use Case | Light tone | Dark tone | Flutter accessor |
|----------|-----------|-----------|-----------------|
| Primary accent | 40 | 80 | `colorScheme.primary` |
| Backgrounds | 98 | 6 | `colorScheme.surface` |
| Surface containers L0→L5 | 96→90 | darker tones | `colorScheme.surfaceContainerLow` → `highest` |
| Text on surface | 10 | 90 | `colorScheme.onSurface` |
| Error | 40 | 80 | `colorScheme.error` |

## Flutter Code Snippets

**Seed to theme:**
```dart
ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(
    seedColor: const Color(0xFF6750A4),
    brightness: Brightness.light,
  ),
);
```

**Responsive layout:**
```dart
LayoutBuilder(builder: (_, c) {
  if (c.maxWidth < 600) return _Compact();
  if (c.maxWidth < 840) return _Medium();
  return _Expanded();
});
```

**State layer:**
```dart
WidgetStateProperty.resolveWith((s) =>
  s.contains(WidgetState.hovered) ? hoverColor : baseColor);
```

## State Layer Opacities
| State | Opacity | Flutter equivalent |
|-------|---------|-------------------|
| Hover | 8% | `WidgetState.hovered` |
| Focus | 12% | `WidgetState.focused` |
| Pressed | 12% | `WidgetState.pressed` |
| Dragged | 16% | `WidgetState.dragged` |
| Disabled content | 38% | `WidgetState.disabled` |

## Shape Radius per Widget
| Widget | BorderRadius value | Flutter class |
|--------|-------------------|---------------|
| `FilledButton` | full | `StadiumBorder()` |
| `Card` | 12dp | `RoundedRectangleBorder(circular(12))` |
| `AlertDialog` | 32dp | `RoundedRectangleBorder(circular(32))` |
| `BottomSheet` (top) | 48dp | `RoundedRectangleBorder(topOnly: Radius(48))` |
| `FloatingActionButton` | 20dp | `RoundedRectangleBorder(circular(20))` |
| `Chip` | 8dp | `RoundedRectangleBorder(circular(8))` |
| `TextField` (top) | 4dp | `RoundedRectangleBorder(topOnly: Radius(4))` |

## Elevation via Surface Container
| Level | `ColorScheme` property | Use |
|-------|----------------------|-----|
| 0 | `surface` | Flattest surfaces |
| 1 | `surfaceContainerLow` | Default container |
| 2 | `surfaceContainer` | Elevated container |
| 3 | `surfaceContainerHigh` | Higher container |
| 4–5 | `surfaceContainerHighest` | Highest container |

## Easing Quick Reference
| Transition Type | Flutter curve | Duration |
|----------------|---------------|----------|
| Stay on screen | `Curves.emphasized` | 500ms |
| Enter | `Curves.emphasizedDecelerate` | 400ms |
| Exit permanently | `Curves.emphasizedAccelerate` | 200ms |
| Exit temporarily | `Curves.emphasized` | 300ms |

## Button Type by Intent
| Action Priority | Widget |
|----------------|--------|
| Primary action | `FilledButton` |
| Secondary action | `OutlinedButton` or `TextButton` |
| Destructive action | `TextButton(foregroundColor: colorScheme.error)` |
| Multiple equal actions | `SegmentedButton` |

## Accessibility Minimums
| Element | Requirement | Flutter tool |
|---------|------------|--------------|
| Normal text | 4.5:1 contrast | `SemanticsDebugger` |
| Large text (≥18px bold / ≥24px) | 3:1 | `SemanticsDebugger` |
| UI components | 3:1 | `SemanticsDebugger` |
| Touch targets | 48×48dp min | `SizedBox(width: 48, height: 48)` |
| Visual focus | Tab key visible | `Focus`, `FocusScope` |
