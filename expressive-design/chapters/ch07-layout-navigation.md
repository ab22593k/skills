# Layout & Navigation

## Core concepts
- Three canonical window size classes (compact, medium, expanded) define layout strategy
- Navigation switches between `NavigationBar`/`Rail`/`Drawer` per class
- Flutter's `LayoutBuilder` is the idiomatic tool for responsive layout

## Frameworks introduced

**Window size classes in Flutter —** Use `LayoutBuilder` to read `BoxConstraints.maxWidth` and choose layout + navigation variant. No dedicated `WindowSizeClass` widget in core Flutter — the `adaptive_breakpoints` package provides it.
```dart
LayoutBuilder(builder: (context, constraints) {
  if (constraints.maxWidth < 600) return _CompactLayout();
  if (constraints.maxWidth < 840) return _MediumLayout();
  return _ExpandedLayout();
});
```

**Navigation by size class:**
```dart
Widget _navigationForSize(double width) {
  if (width < 600) return NavigationBar(destinations: destinations);
  if (width < 840) return NavigationRail(destinations: destinations);
  return NavigationDrawer(destinations: destinations);
}
```

**8dp spacing system —** 8dp base grid. Margins: compact=16dp, medium=24dp, expanded=24dp+. Gutters: 24dp. Content padding inside cards: 16dp.

**Canonical layouts —** Feed (single scrollable list), List-detail (master-detail with `SplitView` or manual side-by-side), Multi-pane (panels), Supporting pane (primary + supplementary).

## Key techniques

**Responsive scaffold:**
```dart
@override
Widget build(BuildContext context) {
  return LayoutBuilder(builder: (context, constraints) {
    final width = constraints.maxWidth;
    if (width < 600) {
      return _compactScaffold();
    } else if (width < 840) {
      return _mediumScaffold();
    } else {
      return _expandedScaffold();
    }
  });
}

Widget _compactScaffold() => Scaffold(
  body: _body(),
  bottomNavigationBar: NavigationBar(destinations: _dests),
);

Widget _mediumScaffold() => Scaffold(
  body: Row(children: [
    NavigationRail(destinations: _dests, onDestinationSelected: ...),
    Expanded(child: _body()),
  ]),
);
```

**Edge-to-edge in Flutter:** Use `SafeArea` or `MediaQuery.removePadding` to draw behind system bars. `SystemUiOverlayStyle` for status bar icon colors.

**Foldable support:** Use `LayoutBuilder` — foldables report their window size correctly. Don't check `Platform.isAndroid` or device models.

## Reference tables

| Window class | Width | Nav widget | Margin |
|-------------|-------|-----------|--------|
| Compact | <600dp | `NavigationBar` | 16dp |
| Medium | 600–839dp | `NavigationRail` | 24dp |
| Expanded | ≥840dp | `NavigationDrawer` | 24dp+ |

## Connection to other chapters
Navigation widgets (ch06) vary by size class. Spacing is a design token (ch08). Responsive shape radius (ch04) can vary per breakpoint.
