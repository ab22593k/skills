---
name: designing-interfaces
description: Apply the pattern language from Designing Interfaces (3rd ed.) to create intuitive, usable interaction designs for web and mobile — choosing the right patterns for navigation, layout, data input, mobile gestures, and visual hierarchy.
effort: medium
---

# Designing Interfaces

A pattern-driven reference from Tidwell, Brewer, and Valencia (O'Reilly, 3rd ed., 2020) for screen-based interaction design.

## Core mental models

### Users form mental models from surface behavior

- **When to use** — Any design decision where user expectations matter
- **The idea** — Users build an internal model of how the system works based only on what they see and do. They don't read the manual. Your interface is the implementation. Every affordance, animation, and label shapes their mental model — whether you intend it or not.
- **How to apply** — Test your design against the question: "If I only saw this screen, would I understand the model?" Prefer direct manipulation (drag a slider to set a value) over indirect (type a number in a field). Use progressive disclosure to reveal complexity only as needed.
- **Pitfalls** — Leaking implementation details (e.g., showing raw database IDs) or hiding affordances forces users to build a wrong model.

### Postel's Law for interaction design

- **When to use** — Designing inputs, forms, search, or any user-to-system communication
- **The idea** — "Be liberal in what you accept, conservative in what you send." Accept flexible input (case-insensitive, forgiving of typos, multiple formats) but return precise, clear output.
- **How to apply** — Normalize phone numbers, tolerate extra spaces, accept partial matches in search, show auto-suggest. Return cleanly formatted results.
- **Pitfalls** — Being too liberal creates ambiguity; too conservative creates frustration.

### Fitts's Law governs target acquisition

- **When to use** — Placing any clickable/tappable element: buttons, links, menus, controls
- **The idea** — Time to acquire a target is a function of distance and size. Larger targets closer to the cursor (or thumb) are faster to hit. Corners and edges act as infinite-size targets on screens.
- **How to apply** — Make primary actions large. Place destructive actions away from primary ones. Put navigation in the thumb zone on mobile. Use screen edges for menus on desktop.
- **Pitfalls** — Tiny touch targets (below 44px), placing common actions at opposite corners, or ignoring thumb reach on large phones.

### The 3 types of memory constrain UI

- **When to use** — Deciding between recognition vs. recall, designing navigation, onboarding
- **The idea** — Sensory memory (ms), working memory (~7±2 items, seconds), and long-term memory (indefinite but slow). Never rely on working memory for complex tasks. Recognition (showing options) is far easier than recall (remembering and typing).
- **How to apply** — Use menus not command lines. Show recently used items. Keep navigation consistent. Provide visual cues rather than expecting memorization. Break complex forms into chunks (Miller's Law).
- **Pitfalls** — Overloading working memory with too many simultaneous choices, or forcing recall of arbitrary codes/IDs.

### Norman's gulfs of execution and evaluation

- **When to use** — Debugging why users fail at a task
- **The idea** — The gulf of execution is the gap between what users intend and what the interface lets them do. The gulf of evaluation is the gap between what the system does and what users perceive it did. Good design closes both.
- **How to apply** — Execution: make affordances visible, match controls to user goals. Evaluation: provide clear feedback after every action (confirmation, error, animation). Test whether users can form a goal, find the control, and understand the result.
- **Pitfalls** — Focusing on only one gulf (e.g., making beautiful buttons that give no feedback).

### Visual hierarchy determines scanning order

- **When to use** — Any screen layout: dashboards, forms, data tables, article pages
- **The idea** — Users scan in a Z or F pattern, weighted by visual weight (size, color, contrast, whitespace). What stands out visually is read first, assumed most important. If your visual hierarchy doesn't match your information hierarchy, users miss critical content.
- **How to apply** — Title is largest. Group related items with whitespace, not lines. Use size and weight (not just color) for primary actions. Make secondary content visually recessive. On mobile, layer with cards.
- **Pitfalls** — Making everything bold/navy (nothing stands out), or using color alone to convey hierarchy (accessibility failure).

## How to use this skill

To load a chapter's content on demand:

```
@designing-interfaces load chapter 4
@designing-interfaces lookup pattern "Responsive Disclosure"
@designing-interfaces glossary
```

The chapter index below shows what each chapter covers and its token count. Load only what you need.

## Chapter index

| #   | Title                        | Topic                                                                     | Tokens |
| --- | ---------------------------- | ------------------------------------------------------------------------- | ------ |
| 1   | What Users Do                | User behavior models, goals, tasks, decision-making                       | ~1K    |
| 2   | Organizing Content           | Information architecture, navigation, search, sitemaps                    | ~1K    |
| 3   | Getting Around               | Navigation patterns — nav bars, tabs, breadcrumbs, pagination, accordions | ~1K    |
| 4   | Organizing the Page          | Page layout patterns — cards, grids, visual hierarchy, responsive         | ~1K    |
| 5   | Doing Things                 | Actions and commands — buttons, menus, toolbars, command palettes         | ~1K    |
| 6   | Showing Complex Data         | Data display — tables, lists, charts, dashboards, maps                    | ~1K    |
| 7   | Getting Input from Users     | Forms — labels, validation, input types, autocomplete, wizards            | ~1K    |
| 8   | Mobile Design                | Mobile-specific — thumb zones, gestures, bottom nav, mobile forms         | ~1K    |
| 9   | Visual Style and Aesthetics  | Color, typography, iconography, accessibility, branding                   | ~1K    |
| 10  | Making It Look Good          | Layout grids, spacing, images, responsive frameworks, consistency         | ~1K    |
| 11  | UI Systems and Atomic Design | Design systems, component libraries, design tokens, pattern libraries     | ~1K    |
| 12  | Smart Systems                | Connected devices, contextual/anticipatory/assistive interfaces, NUI      | ~1K    |

## Reference files

- `glossary.md` — All key terms alphabetized with chapter references
- `patterns.md` — Full pattern catalog in type/context/solution/consequences format
- `cheatsheet.md` — Decision tables for choosing patterns by scenario
