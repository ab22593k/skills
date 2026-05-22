# Cheatsheet

## Choosing a navigation pattern
| If | Then |
|----|------|
| 3-7 top-level sections, constant switching | Tab bar (Ch3) |
| Deep hierarchy, needs context | Breadcrumbs + sidebar (Ch3) |
| Mobile app, primary navigation | Bottom navigation (Ch8) |
| Content-heavy, secondary nav | Accordion (Ch3) |
| Multi-step process | Stepper / Wizard (Ch3, Ch7) |
| Many sections >7, infrequent switching | Hamburger menu (Ch3) |

## Choosing layout
| If | Then |
|----|------|
| Heterogeneous content of varying length | Card layout (Ch4) |
| Dense data requiring comparison | Sortable table (Ch6) |
| Text-heavy article | Single column, generous line height (Ch10) |
| Dashboard with mixed data types | Grid of cards + charts (Ch4, Ch6) |
| Must work across screen sizes | Responsive grid with breakpoints (Ch10) |

## Form decisions
| If | Then |
|----|------|
| 1-5 fields, simple | Inline labels (Ch7) |
| 5+ fields | Top-aligned labels (Ch7) |
| Complex data with dependencies | Wizard / Stepper (Ch7) |
| Must prevent bad data | Inline validation on blur (Ch7) |
| Accepting flexible input | Forgiving input, Postel's Law (Ch7) |

## Mobile-specific
| If | Then |
|----|------|
| Primary navigation | Bottom tab bar (Ch8) |
| Form on mobile | One field per step (Ch8) |
| List of items | Card list, pull to refresh (Ch8) |
| Confirm destructive action | Undo bar instead of confirmation dialog (Ch8) |
| Gesture for primary action | Make it obvious with visual affordance (Ch8) |

## Design system maturity
| Stage | What you have |
|-------|---------------|
| ad-hoc | No system, each screen built independently |
| standardized | Color palette, type scale, spacing defined |
| component library | Reusable UI components with docs |
| design system | Components + patterns + guidelines + tools (Ch11) |
| atomic design | Atoms → molecules → organisms → templates (Ch11) |

## Accessibility quick-check
| Check | If missing |
|-------|------------|
| Color not sole conveyor of info | Screen reader users miss status |
| Touch target ≥ 44px | Users miss the tap (Ch8) |
| Label associates with input | Screen reader can't identify field (Ch7) |
| Contrast ratio ≥ 4.5:1 | Low-vision users can't read (Ch9) |
| Focus indicator visible | Keyboard users don't know location |
