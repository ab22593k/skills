# Accessibility

## Core concepts
- Accessibility by default — Flutter's Material widgets embed WCAG-compliant accessibility
- Flutter's `Semantics` widget provides fine-grained control
- Use `FlutterSemanticsDebugger` to visualize the accessibility tree

## Frameworks introduced

**Flutter Semantics system —** Every Material widget emits semantic information automatically. `Semantics` widget overrides or extends it. `MergeSemantics` groups children. `ExcludeSemantics` hides decorative elements.

```dart
// Automatic: Text, IconButton, etc. include Semantics
// Manual override:
Semantics(
  label: 'Open menu',
  hint: 'Double tap to open navigation menu',
  child: IconButton(icon: Icon(Icons.menu), onPressed: () {}),
);
```

**Color contrast in Flutter —** `ColorScheme.fromSeed` generates WCAG AA-compliant roles automatically. Verify with `SemanticsDebugger.enabled = true` in `MaterialApp`.

**Focus and navigation —** Use `Focus`, `FocusScope`, `AutofocusGroup`. Flutter's `Shortcuts` and `Actions` widgets handle keyboard navigation. Test with Tab key on desktop/web.

## Key techniques

**Semantics debugger:**
```dart
MaterialApp(
  showSemanticsDebugger: true, // Toggle during development
  // ...
);
```
Enables overlay showing semantic labels, roles, actions. Verify every interactive element has `label` + `action` pair.

**Touch targets:** Flutter's `Material` widgets default to ≥48×48dp. For custom tappable areas:
```dart
GestureDetector(
  behavior: HitTestBehavior.opaque,
  onTap: () {},
  child: SizedBox(
    width: 48, height: 48,
    child: icon,
  ),
);
```

**Accesibility checklist in Flutter:**
- `Semantics(label: ...)` on all `IconButton`s
- `ExcludeSemantics` on decorative `Icon`s
- `MergeSemantics` on tightly coupled elements (e.g., chip text + icon)
- `MediaQuery.textScaler` respects user font size preference
- `MediaQuery.boldText` adapts to bold text setting
- Test with `AccessibilityNodeInfo` on Android, `UIAccessibility` on iOS

## Connection to other chapters
Color contrast depends on `ColorScheme.fromSeed` (ch02). Type size respects `MediaQuery.textScaler` (ch03). Focus indicators use shape tokens (ch04). Component states (ch01) require accessible contrast.
