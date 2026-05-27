---
chapter: 5
topic: Motion
when: User needs spring physics, Curves.emphasized, AnimationController with SpringDescription, implicit animations, or enter/exit transition decisions
queries: ["spring animation", "Curves.emphasized", "AnimationController", "SpringDescription", "implicit animation", "enter exit transition", "AnimatedContainer", "motion duration"]
---

# Motion

## Core concepts
- Spring-based physics replaces fixed-duration animations for natural, responsive motion
- Flutter's `AnimationController` with `SpringDescription` gives direct physics control
- Two MD3 schemes: Standard (utilitarian) and Expressive (bouncy)

## Frameworks introduced

**Spring physics in Flutter —** `SpringDescription` takes `mass`, `stiffness`, `damping`. `SpringDescription.withDampingRatio(0.68)` matches the MD3 standard spring. `withDampingRatio(0.48)` matches expressive/bouncy.

```dart
// MD3 Standard spring (utilitarian)
AnimationController(
  vsync: this,
  duration: null, // Spring has no fixed duration
)..animateWith(SpringSimulation(
    SpringDescription.withDampingRatio(0.68, stiffness: 100),
    0.0, 1.0, velocity,
  ));

// MD3 Expressive spring (bouncy)
SpringDescription.withDampingRatio(0.48, stiffness: 80);
```

**Emphasized easing —** Flutter 3.x ships `Curves.emphasized`, `Curves.emphasizedDecelerate`, `Curves.emphasizedAccelerate`. These match MD3's `cubic-bezier(0.2, 0, 0, 1)` family.

```dart
// Implicit animation with MD3 curve
AnimatedContainer(
  duration: const Duration(milliseconds: 500),
  curve: Curves.emphasized,
  // ...
);

// Explicit animation
controller.drive(CurveTween(curve: Curves.emphasizedDecelerate));
```

**Duration scale —** 16 levels (50ms–1000ms). Recommended pairings:
- Element stays on screen → Emphasized, 500ms
- Element enters → Emphasized Decelerate, 400ms
- Element exits permanently → Emphasized Accelerate, 200ms
- Small utility → Standard, 300ms

## Key techniques

**Implicit widgets:** Prefer `AnimatedContainer`, `AnimatedOpacity`, `AnimatedScale`, `TweenAnimationBuilder`. They accept `Curves.emphasized` directly — no manual controller needed.

**Flutter component animations:** `ExpansionTile`, `Drawer`, `BottomSheet` use MD3-appropriate defaults when `useMaterial3: true`. No additional configuration needed.

**Exit vs temporary:** Elements that exit permanently use Accelerate (shorter). Elements that exit temporarily (e.g., `BottomSheet` sliding back) use Emphasized (medium). Wrong choice causes jarring UX.

## Reference table

| Transition | Flutter curve | Duration |
|-----------|---------------|----------|
| Stay on screen | `Curves.emphasized` | 500ms |
| Enter | `Curves.emphasizedDecelerate` | 400ms |
| Exit permanently | `Curves.emphasizedAccelerate` | 200ms |
| Exit temporarily | `Curves.emphasized` | 300ms |

## Connection to other chapters
Shape morphing (→ ch04) uses `AnimatedContainer` + `Curves.emphasized`. Dialog/sheet enter/exit (→ ch06) use specific motion pairings. Dark mode toggle can animate via `AnimatedTheme`.
