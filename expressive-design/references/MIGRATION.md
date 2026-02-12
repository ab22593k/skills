# Migration Guide: Standard M3 to M3 Expressive

This guide provides step-by-step instructions for migrating Flutter applications from standard Material 3 to Material 3 Expressive (M3 Expressive).

## Migration Overview

M3 Expressive builds upon standard M3 with enhancements to color, typography, motion, and component specifications. The migration involves updating theming, component configurations, and design tokens while maintaining backward compatibility.

## Key Differences

### Color System Changes

| Aspect | Standard M3 | M3 Expressive |
|--------|-------------|---------------|
| Container hierarchy | Basic containers | Expanded container tiers |
| Surface system | 3 levels | 5 surface container levels |
| Contrast emphasis | Standard | Enhanced for accessibility |
| Emotional selection | Functional only | Emotion-driven guidance |

### Typography Changes

| Aspect | Standard M3 | M3 Expressive |
|--------|-------------|---------------|
| Scale | 15 styles | 15 styles + emphasized variants |
| Hierarchy | Size-based | Size + weight emphasis |
| Application | Functional | Expressive treatments |

### Motion Changes

| Aspect | Standard M3 | M3 Expressive |
|--------|-------------|---------------|
| Duration | Fixed ranges | Extended ranges |
| Easing | Standard curves | Expressive curves |
| Application | Functional | Emotion-driven timing |

### Component Changes

| Aspect | Standard M3 | M3 Expressive |
|--------|-------------|---------------|
| Touch targets | 48dp minimum | 56dp+ recommended |
| Container emphasis | Subtle | Expressive containers |
| Shape | Consistent | Emphasized variations |
| Motion | Functional | Energetic transitions |

## Step 1: Update Dependencies

### Add M3 Expressive Package

```yaml
dependencies:
  flutter:
    sdk: flutter
  m3e_design: ^0.2.1        # M3 Expressive design tokens
  dynamic_color: ^1.8.1      # Dynamic color support (Android 12+)
```

### Update Existing Dependencies

```yaml
dependencies:
  flutter:
    sdk: flutter
  # Ensure material package is up to date
  material_color_utilities: ^0.8.0
```

## Step 2: Update Theme Configuration

### Basic Theme Migration

**Before (Standard M3):**

```dart
MaterialApp(
  theme: ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.blue,
    ),
  ),
  home: MyApp(),
)
```

**After (M3 Expressive):**

```dart
import 'package:m3e_design/m3e_design.dart';

MaterialApp(
  theme: ColorScheme.fromSeed(
    seedColor: Colors.blue,
  ).toM3EThemeData(),
  home: MyApp(),
)
```

### With Dynamic Color

**Before (Standard M3):**

```dart
DynamicColorBuilder(
  builder: (lightDynamic, darkDynamic) {
    return MaterialApp(
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: lightDynamic,
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        colorScheme: darkDynamic,
      ),
      home: MyApp(),
    );
  },
)
```

**After (M3 Expressive):**

```dart
DynamicColorBuilder(
  builder: (lightDynamic, darkDynamic) {
    final light = lightDynamic ?? ColorScheme.fromSeed(seedColor: Colors.blue);
    final dark = darkDynamic ?? ColorScheme.fromSeed(
      seedColor: Colors.blue,
      brightness: Brightness.dark,
    );
    return MaterialApp(
      theme: light.toM3EThemeData(),
      darkTheme: dark.toM3EThemeData(),
      home: MyApp(),
    );
  },
)
```

### Using withM3ETheme Wrapper

```dart
MaterialApp(
  theme: withM3ETheme(
    ThemeData(
      colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
      useMaterial3: true,
    ),
  ),
  home: MyApp(),
)
```

## Step 3: Update Color Tokens

### Container Color Migration

**Before (Standard M3):**

```dart
ColorScheme(
  primary: Colors.blue,
  secondary: Colors.teal,
  tertiary: Colors.orange,
)
```

**After (M3 Expressive):**

```dart
ColorScheme(
  // Primary colors
  primary: Colors.blue,
  onPrimary: Colors.white,
  primaryContainer: Colors.blue[100]!,
  onPrimaryContainer: Colors.blue[900]!,
  
  // Secondary colors
  secondary: Colors.teal,
  onSecondary: Colors.white,
  secondaryContainer: Colors.teal[100]!,
  onSecondaryContainer: Colors.teal[900]!,
  
  // Tertiary colors
  tertiary: Colors.orange,
  onTertiary: Colors.white,
  tertiaryContainer: Colors.orange[100]!,
  onTertiaryContainer: Colors.orange[900]!,
  
  // Surface system
  surface: Colors.white,
  surfaceDim: Colors.grey[100]!,
  surfaceBright: Colors.white,
  surfaceContainerLowest: Colors.white,
  surfaceContainerLow: Colors.grey[50]!,
  surfaceContainer: Colors.grey[100]!,
  surfaceContainerHigh: Colors.grey[200]!,
  surfaceContainerHighest: Colors.grey[300]!,
  
  // Surface variants
  surfaceVariant: Colors.grey[200]!,
  onSurfaceVariant: Colors.grey[700]!,
  
  // Error colors
  error: Colors.red,
  onError: Colors.white,
  errorContainer: Colors.red[100]!,
  onErrorContainer: Colors.red[900]!,
)
```

## Step 4: Update Typography

### Typography Migration

**Before (Standard M3):**

```dart
Typography(
  displayLarge: TextStyle(fontSize: 57, height: 64),
  displayMedium: TextStyle(fontSize: 45, height: 52),
  displaySmall: TextStyle(fontSize: 36, height: 44),
  headlineLarge: TextStyle(fontSize: 32, height: 40),
  headlineMedium: TextStyle(fontSize: 28, height: 36),
  headlineSmall: TextStyle(fontSize: 24, height: 32),
  titleLarge: TextStyle(fontSize: 22, height: 28),
  titleMedium: TextStyle(fontSize: 16, height: 24),
  titleSmall: TextStyle(fontSize: 14, height: 20),
  bodyLarge: TextStyle(fontSize: 16, height: 24),
  bodyMedium: TextStyle(fontSize: 14, height: 20),
  bodySmall: TextStyle(fontSize: 12, height: 16),
  labelLarge: TextStyle(fontSize: 14, height: 20),
  labelMedium: TextStyle(fontSize: 12, height: 16),
  labelSmall: TextStyle(fontSize: 11, height: 16),
)
```

**After (M3 Expressive):**

```dart
Typography(
  // Display styles
  displayLarge: TextStyle(
    fontSize: 57,
    lineHeight: 64,
    fontWeight: FontWeight.w400,
    letterSpacing: -0.25,
  ),
  displayMedium: TextStyle(
    fontSize: 45,
    lineHeight: 52,
    fontWeight: FontWeight.w400,
  ),
  displaySmall: TextStyle(
    fontSize: 36,
    lineHeight: 44,
    fontWeight: FontWeight.w400,
  ),
  
  // Headline styles
  headlineLarge: TextStyle(
    fontSize: 32,
    lineHeight: 40,
    fontWeight: FontWeight.w400,
  ),
  headlineMedium: TextStyle(
    fontSize: 28,
    lineHeight: 36,
    fontWeight: FontWeight.w400,
  ),
  headlineSmall: TextStyle(
    fontSize: 24,
    lineHeight: 32,
    fontWeight: FontWeight.w400,
  ),
  
  // Title styles
  titleLarge: TextStyle(
    fontSize: 22,
    lineHeight: 28,
    fontWeight: FontWeight.w500,
  ),
  titleMedium: TextStyle(
    fontSize: 16,
    lineHeight: 24,
    fontWeight: FontWeight.w500,
    letterSpacing: 0.15,
  ),
  titleSmall: TextStyle(
    fontSize: 14,
    lineHeight: 20,
    fontWeight: FontWeight.w500,
    letterSpacing: 0.1,
  ),
  
  // Body styles
  bodyLarge: TextStyle(
    fontSize: 16,
    lineHeight: 24,
    fontWeight: FontWeight.w400,
    letterSpacing: 0.5,
  ),
  bodyMedium: TextStyle(
    fontSize: 14,
    lineHeight: 20,
    fontWeight: FontWeight.w400,
    letterSpacing: 0.25,
  ),
  bodySmall: TextStyle(
    fontSize: 12,
    lineHeight: 16,
    fontWeight: FontWeight.w400,
    letterSpacing: 0.4,
  ),
  
  // Label styles
  labelLarge: TextStyle(
    fontSize: 14,
    lineHeight: 20,
    fontWeight: FontWeight.w500,
    letterSpacing: 0.1,
  ),
  labelMedium: TextStyle(
    fontSize: 12,
    lineHeight: 16,
    fontWeight: FontWeight.w500,
    letterSpacing: 0.5,
  ),
  labelSmall: TextStyle(
    fontSize: 11,
    lineHeight: 16,
    fontWeight: FontWeight.w500,
    letterSpacing: 0.5,
  ),
  
  // Emphasized variants
  displayLargeEmphasized: TextStyle(
    fontSize: 57,
    lineHeight: 64,
    fontWeight: FontWeight.w600,
    letterSpacing: -0.25,
  ),
  headlineLargeEmphasized: TextStyle(
    fontSize: 32,
    lineHeight: 40,
    fontWeight: FontWeight.w600,
  ),
  // ... additional emphasized variants
)
```

## Step 5: Update Component Configurations

### Button Updates

**Before (Standard M3):**

```dart
ElevatedButton(
  onPressed: () {},
  style: ElevatedButton.styleFrom(
    minimumSize: Size(0, 48),
  ),
  child: Text('Button'),
)
```

**After (M3 Expressive):**

```dart
ElevatedButton(
  onPressed: () {},
  style: ElevatedButton.styleFrom(
    minimumSize: Size(0, 56),  // Increased touch target
    padding: EdgeInsets.symmetric(horizontal: 24, vertical: 10),
  ),
  child: Text(
    'Button',
    style: Theme.of(context).textTheme.labelLarge,
  ),
)
```

### Navigation Updates

**Before (Standard M3):**

```dart
NavigationBar(
  destinations: [
    NavigationDestination(icon: Icon(Icons.home), label: 'Home'),
    NavigationDestination(icon: Icon(Icons.search), label: 'Search'),
  ],
)
```

**After (M3 Expressive):**

```dart
NavigationBar(
  height: 80,  // Increased height
  destinations: [
    NavigationDestination(
      icon: Icon(Icons.home),
      label: 'Home',
      selectedIcon: Icon(Icons.home),  // Expressive active state
    ),
    NavigationDestination(
      icon: Icon(Icons.search),
      label: 'Search',
      selectedIcon: Icon(Icons.search),
    ),
  ],
)
```

## Step 6: Update Shape Tokens

### Shape Migration

**Before (Standard M3):**

```dart
ThemeData(
  shapeTheme: ShapeTheme(
    small: RoundedCornerBorder(8),
    medium: RoundedRectangleBorder(12),
    large: RoundedRectangleBorder(16),
  ),
)
```

**After (M3 Expressive):**

```dart
ThemeData(
  shapeTheme: ShapeTheme(
    extraSmall: RoundedCornerBorder(4),
    small: RoundedRectangleBorder(8),
    medium: RoundedRectangleBorder(12),
    large: RoundedRectangleBorder(16),
    extraLarge: RoundedRectangleBorder(24),
    full: RoundedRectangleBorder.circular(999),
  ),
)
```

## Step 7: Add Motion Configurations

### Motion Duration Migration

**Before (Standard M3):**

```dart
ThemeData(
  duration: Duration(milliseconds: 200),
)
```

**After (M3 Expressive):**

```dart
ThemeData(
  // Expressive motion durations
  splashDuration: Duration(milliseconds: 400),
  pageTransitionDuration: Duration(milliseconds: 300),
  toastDuration: Duration(milliseconds: 250),
  
  // Expressive easing
  materialTapTargetSize: MaterialTapTargetSize.padded,
)
```

## Breaking Changes

### Component Differences

| Component | Standard M3 | M3 Expressive | Migration Action |
|-----------|-------------|---------------|------------------|
| NavigationBar height | 80dp | 80dp (increased emphasis) | Update visual hierarchy |
| Button touch target | 48dp | 56dp recommended | Increase minimum size |
| Card elevation | 1-2dp | 1-2dp + containers | Add container colors |
| Dialog radius | 16dp | 24dp recommended | Update border radius |
| FAB animation | Standard | Expressive | Update animation timing |

### Removed/Changed APIs

| Old API | New API | Migration |
|---------|---------|-----------|
| `ColorScheme.light()` | `ColorScheme.fromSeed()` | Regenerate schemes |
| Standard shapes | Extended shape scale | Update token values |
| Fixed durations | Extended durations | Update motion config |

## Compatibility Notes

### Android Compatibility

- Dynamic color requires Android 12+
- Fallback to seed-based colors on older versions
- Material ripple available on all versions
- Platform gestures unaffected

### Linux Desktop Compatibility

- All tokens work on Linux
- Motion preferences may vary
- No dynamic color support
- Desktop accessibility settings apply

## Testing Guidelines

### Visual Regression Testing

1. Capture baseline screenshots (standard M3)
2. Apply M3 Expressive changes
3. Compare visual differences
4. Verify intentional expressive changes
5. Check for unintended side effects

### Accessibility Testing

1. Verify touch target sizes (56dp minimum)
2. Check color contrast ratios
3. Test screen reader compatibility
4. Validate keyboard navigation
5. Test reduced motion preferences

### Performance Testing

1. Measure render performance
2. Check animation frame rates
3. Test on lower-end devices
4. Verify smooth transitions
5. Monitor memory usage

## Rollout Strategy

### Phase 1: Internal Testing

1. Apply changes to internal builds
2. Gather team feedback
3. Identify issues in controlled environment
4. Refine configurations

### Phase 2: Beta Release

1. Release to beta testers
2. Monitor crash reports
3. Gather user feedback
4. Identify platform-specific issues
5. Iterate on configurations

### Phase 3: Gradual Rollout

1. Enable M3 Expressive for percentage of users
2. Monitor metrics (crash, engagement)
3. Gradually increase rollout percentage
4. Address any issues discovered
5. Full rollout when confident

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Inconsistent colors | Missing container colors | Add all container color tokens |
| Broken layouts | Increased touch targets | Adjust layout constraints |
| Slow animations | Performance regression | Optimize motion settings |
| Contrast issues | Missing on-color tokens | Add on-primary, on-surface tokens |

### Debugging Tips

1. Use Theme.of(context) to verify theme application
2. Check debug paint for touch target visualization
3. Use timeline view for animation analysis
4. Test on multiple platforms
5. Verify token application with ThemeInspector

## Migration Checklist

- [ ] Dependencies updated
- [ ] ThemeData migrated to M3 Expressive
- [ ] Color tokens updated with containers
- [ ] Typography updated with specifications
- [ ] Component configurations updated
- [ ] Shape tokens extended
- [ ] Motion configurations added
- [ ] Visual regression tested
- [ ] Accessibility tested
- [ ] Performance tested
- [ ] Platform compatibility verified
- [ ] Rollout strategy defined
- [ ] Troubleshooting plan ready
