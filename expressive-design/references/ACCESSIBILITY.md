# Material 3 Expressive Accessibility

The M3 Expressive accessibility guidelines ensure that expressive design elements remain usable by all users, including those with visual, motor, cognitive, and auditory impairments. Expressive design should enhance accessibility, not compromise it.

## Accessibility Philosophy

Expressive design creates interfaces that are both emotionally engaging AND accessible to everyone. M3 Expressive research found that expressive designs are more accessible to users of all ages and abilities when properly implemented.

## Color Contrast Requirements

### Minimum Contrast Ratios

| Context | Minimum Ratio | Preferred Ratio | Level |
|---------|---------------|-----------------|-------|
| Normal text (7-18pt) | 4.5:1 | 7:1 | AA / AAA |
| Large text (18pt+) | 3:1 | 4.5:1 | AA / AAA |
| UI components | 3:1 | 4.5:1 | AA / AAA |
| Graphical objects | 3:1 | - | AA |
| Error states | 4.5:1 | 7:1 | AAA |

### Text Contrast Matrix

| Text Size | Light Theme | Dark Theme | Token |
|-----------|-------------|------------|-------|
| Body small (12sp) | 4.5:1 minimum | 4.5:1 minimum | `md.sys.color.on-surface` |
| Body medium (14sp) | 4.5:1 minimum | 4.5:1 minimum | `md.sys.color.on-surface` |
| Body large (16sp) | 4.5:1 minimum | 4.5:1 minimum | `md.sys.color.on-surface` |
| Title small (14sp) | 4.5:1 minimum | 4.5:1 minimum | `md.sys.color.on-surface` |
| Title medium (16sp) | 4.5:1 minimum | 4.5:1 minimum | `md.sys.color.on-surface` |
| Headline small (24sp) | 3:1 minimum | 3:1 minimum | `md.sys.color.on-surface` |
| Headline medium (28sp) | 3:1 minimum | 3:1 minimum | `md.sys.color.on-surface` |

### Component Contrast

| Component | Element | Minimum Ratio | Token |
|-----------|---------|---------------|-------|
| Button | Text on filled | 4.5:1 | `md.sys.color.on-primary` |
| Button | Text on outlined | 4.5:1 | `md.sys.color.primary` |
| Button | Text on text | 4.5:1 | `md.sys.color.primary` |
| Text Field | Text on unfilled | 4.5:1 | `md.sys.color.on-surface` |
| Text Field | Label on unfilled | 4.5:1 | `md.sys.color.on-surface-variant` |
| Card | Text on surface | 4.5:1 | `md.sys.color.on-surface` |
| Dialog | Text on surface | 4.5:1 | `md.sys.color.on-surface` |

### Container Contrast

| Element | Background | Foreground | Ratio | Token Pair |
|---------|------------|------------|-------|------------|
| Primary container | Primary container | On primary container | 4.5:1 minimum | `primary-container` / `on-primary-container` |
| Secondary container | Secondary container | On secondary container | 4.5:1 minimum | `secondary-container` / `on-secondary-container` |
| Tertiary container | Tertiary container | On tertiary container | 4.5:1 minimum | `tertiary-container` / `on-tertiary-container` |
| Error container | Error container | On error container | 4.5:1 minimum | `error-container` / `on-error-container` |

## Touch Target Requirements

### Minimum Sizes

| Target Type | Minimum Size | Recommended Size | Rationale |
|-------------|--------------|-------------------|-----------|
| Standard touch | 48dp × 48dp | 56dp × 56dp | WCAG 2.1 minimum |
| Emphasized action | 56dp × 56dp | 64dp × 64dp | M3 Expressive recommendation |
| Critical action | 64dp × 64dp | 72dp × 72dp | High-importance targets |
| Touch target spacing | 8dp | 12dp | Prevent accidental taps |

### Touch Target Placement

| Context | Spacing | Rationale |
|---------|---------|-----------|
| Between adjacent targets | 8dp minimum | Prevent overlap activation |
| From screen edge | 16dp minimum | Safe area for gestures |
| From safe areas | 8dp minimum | Avoid system UI conflicts |

### M3 Expressive Touch Targets

| Component | Standard M3 | M3 Expressive | Change |
|-----------|-------------|---------------|--------|
| Button | 48dp height | 56dp height | +8dp |
| FAB | 56dp | 56dp + | No change |
| Icon button | 48dp | 48dp | No change |
| List item | 56dp | 56dp + | +4dp optional |
| Navigation item | 48dp touch | 56dp touch | +8dp |

## Screen Reader Compatibility

### Semantic Expectations

| Component | Semantics Required | Flutter Implementation |
|-----------|-------------------|------------------------|
| Button | Button role, label | `Semantics(button: true)` |
| Icon button | Button role, label, icon description | `Semantics(button: true, label: 'Description')` |
| Text field | Text field role, label, value | `Semantics(textField: true)` |
| Checkbox | Checkbox role, checked state | `Semantics(checked: isChecked)` |
| Radio button | Radio role, selected state | `Semantics(selected: isSelected)` |
| Switch | Switch role, checked state | `Semantics(checked: isOn)` |
| Slider | Slider role, value range | `Semantics(value: current, min: min, max: max)` |
| Navigation item | Button role, label, selected state | `Semantics(selected: isSelected)` |

### Content Description Guidelines

| Element | Do | Don't |
|---------|-----|-------|
| Icon button | "Search for items" | "Search" |
| Image | "Photo of mountain landscape" | "Image" |
| Button with icon | "Send message" | "Send icon" |
| Navigation destination | "Home - Current page" | "Home" |
| Custom component | "Color picker showing 5 options" | "Picker" |

### Navigation Order

| Priority | Element | Reasoning |
|----------|---------|-----------|
| 1 | Primary actions | Most common user goal |
| 2 | Secondary actions | Supporting tasks |
| 3 | Navigation | Content exploration |
| 4 | Supplementary actions | Less frequent tasks |

## Keyboard Navigation

### Focus Order

| Component | Expected Behavior | Implementation |
|-----------|-------------------|----------------|
| Buttons | Tab to reach, Enter/Space to activate | `FocusableActionDetector` |
| Text fields | Tab to reach, Enter for new line | `TextField` with focus |
| Checkboxes | Tab to reach, Space to toggle | `Checkbox` with semantics |
| Radio buttons | Tab to reach, Arrow keys to navigate group | `Radio` with group |
| Sliders | Tab to reach, Arrow keys to adjust | `Slider` with semantics |
| Navigation | Tab/D-pad to navigate | `NavigationDestination` |

### Focus Indicators

| Theme | Focus Style | Visibility |
|-------|-------------|------------|
| Light | Primary color outline | 2dp width |
| Dark | Primary color outline | 2dp width |
| High contrast | White/black outline | 3dp width |

## Motor Accessibility

### Gesture Requirements

| Gesture Type | Target Size | Success Rate Target |
|--------------|-------------|---------------------|
| Tap | 48dp minimum | 95%+ |
| Double tap | 48dp minimum | 90%+ |
| Long press | 48dp minimum | 90%+ |
| Swipe | 48dp minimum | 90%+ |
| Drag | 48dp minimum | 90%+ |

### Timing Considerations

| Interaction | Minimum Time | Maximum Time |
|-------------|---------------|---------------|
| Press and hold | 400ms | 1000ms |
| Double tap | 300ms | 1000ms |
| Long press | 400ms | Unlimited |

## Visual Accessibility

### Color Blindness Considerations

| Type | Prevalence | Design Consideration |
|------|-------------|----------------------|
| Protanopia | ~1% | Don't use red/green alone |
| Deuteranopia | ~5% | Don't use red/green alone |
| Tritanopia | ~0.1% | Don't use blue/yellow alone |
| Achromatopsia | ~0.003% | Use pattern + color |

### Patterns and Indicators

| Information | Color-Only | Color + Pattern | Recommendation |
|-------------|------------|------------------|----------------|
| Error state | Red color | Red + underline | Use both |
| Success state | Green color | Green + checkmark | Use both |
| Warning state | Yellow color | Yellow + icon | Use both |
| Disabled state | Grey color | Grey + opacity | Use both |

## Cognitive Accessibility

### Clear Visual Hierarchy

| Principle | Implementation | Benefit |
|-----------|----------------|---------|
| Size hierarchy | 1.4x minimum between levels | Clear scanning order |
| Color hierarchy | 3:1 minimum between levels | Visual distinction |
| Spacing hierarchy | 1.5x minimum between levels | Grouping clarity |

### Predictable Interactions

| Pattern | Implementation | Benefit |
|---------|----------------|---------|
| Consistent navigation | Same position across screens | Learning curve |
| Standard gestures | Platform conventions | Familiarity |
| Clear feedback | Immediate visual response | Understanding |

### Reduce Cognitive Load

| Technique | Implementation | Benefit |
|-----------|----------------|---------|
| Clear labels | Descriptive text | No ambiguity |
| Progressive disclosure | Show/hide complexity | Focus |
| Grouped actions | Related items together | Organization |

## Age-Inclusive Design

### M3 Expressive Research Findings

| Finding | Implication |
|---------|-------------|
| Expressive designs erase age-related usability gaps | Designs work equally well for all ages |
| 45+ users perform equal to younger users | No accommodation necessary |
| Large touch targets help all users | Everyone benefits |
| Clear hierarchy helps everyone | Not disability-specific |

### Design Recommendations

| Age Group | Consideration | Implementation |
|-----------|---------------|----------------|
| 18-24 | Most receptive to expressive design | Full M3 Expressive implementation |
| 25-44 | Positive response to expressive | Full implementation with balance |
| 45-64 | Equal performance with expressive | Full implementation |
| 65+ | Equal performance with expressive | Full implementation |

## Platform-Specific Considerations

### Android

| Feature | Implementation | Consideration |
|---------|----------------|---------------|
| TalkBack | Semantics widget | Test with screen reader |
| Switch Access | Focus management | Ensure all actions reachable |
| Voice Access | Command recognition | Use clear labels |
| Large text | Scaled pixel sizing | Test at 200% scaling |

### Linux Desktop

| Feature | Implementation | Consideration |
|---------|----------------|---------------|
| Screen readers | Orca compatibility | Test with Orca |
| Keyboard navigation | Focus indicators | Visible focus states |
| Magnification | Zoom support | Test at 200% zoom |
| High contrast | Theme support | Test in high contrast mode |

## Testing Tools

### Automated Testing

| Tool | Checks | Implementation |
|------|--------|----------------|
| flutter_test | Semantic labels | `SemanticsTester` |
| golden_test | Visual appearance | Golden file testing |
| axe-core | Accessibility violations | Integration testing |

### Manual Testing

| Test | Description | Frequency |
|------|-------------|-----------|
| Screen reader | Test with TalkBack/Orca | Every release |
| Keyboard only | Navigate without touch | Every release |
| Color blindness | Simulate color deficiencies | Every release |
| Zoom | Test at 200% scaling | Every release |
| High contrast | Test in high contrast mode | Quarterly |

### Testing Checklist

- [ ] All text meets contrast ratios
- [ ] Touch targets meet minimum sizes
- [ ] All interactive elements have semantic labels
- [ ] Focus order is logical
- [ ] Screen reader announces correctly
- [ ] Keyboard navigation works
- [ ] Color is not the only indicator
- [ ] Test with color blindness simulators
- [ ] Test at 200% text scaling
- [ ] Test with high contrast mode
- [ ] Test with reduced motion
- [ ] Verify age-inclusive performance

## Accessibility Tokens

### Contrast Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `md.sys.color.on-primary` | High contrast on primary | Button text |
| `md.sys.color.on-secondary` | High contrast on secondary | Secondary button text |
| `md.sys.color.on-surface` | High contrast on surface | Primary text |
| `md.sys.color.on-surface-variant` | Medium contrast on surface | Secondary text |
| `md.sys.color.on-error` | High contrast on error | Error text |

### Accessibility Sizes

| Token | Value | Usage |
|-------|-------|-------|
| `md.sys.touch-target.minimum` | 48dp | WCAG minimum |
| `md.sys.touch-target.recommended` | 56dp | M3 Expressive |
| `md.sys.touch-target.critical` | 64dp | Critical actions |

## Implementation Checklist

- [ ] Color contrast meets minimums
- [ ] Touch targets adequate
- [ ] Semantic labels present
- [ ] Focus management implemented
- [ ] Screen reader tested
- [ ] Keyboard navigation works
- [ ] Color blindness considered
- [ ] Age-inclusive tested
- [ ] Platform accessibility verified
- [ ] Reduced motion supported
- [ ] High contrast tested
- [ ] Automated tests passing
