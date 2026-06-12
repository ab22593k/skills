# Chapter 7 — Getting Input from Users

## Core concepts

- Every form field is a question — minimize the number of questions you ask
- Label placement affects scan speed: top-aligned (fastest), left-aligned (moderate), right-aligned (slowest, space-efficient)
- Defaults and autocomplete dramatically reduce input friction
- Forgiving input (Postel's Law) applies everywhere: phone formats, date formats, case sensitivity
- Inline validation catches errors early; avoid validating before the user finishes a field (on blur, not keystroke)

## Frameworks introduced

- **Label alignment** — Top: fastest completion, best for mobile. Left: good for dense desktop forms. Right: compact but slow scanning. Placeholder-as-label: problematic (disappears on input, accessibility issues).
- **Input types** — Text, textarea, select, checkbox, radio, date picker, toggle, slider, autocomplete. Match type to data.
- **Autocomplete / Typeahead** — Real-time suggestions from a known list (countries, products). Distinguish from autofill.
- **Inline validation** — Validate on blur (not on keypress). Show error message below the field. Green checkmark on success. Submit button disabled until all fields pass.
- **Forgiving input** — Accept flexible formats, normalize on the server, show the cleaned version
- **Wizard / Stepper** — Break long forms (~7+ fields) into multi-step flows with progress indicator. Allow back.
- **Form sections** — Group related fields with section headers. Use a single column for clarity.

## Key techniques

- **Smart defaults**: Pre-fill common values. Set sensible date ranges. Remember previous selections.
- **Error message design**: Be specific ("Enter a valid email address", not "Invalid input"). Be polite. Don't use all-caps or red-only.
- **Disabled state**: Gray out unavailable options rather than removing them (keeps layout stable).
- **Date input**: Use a date picker for known dates. Allow typing in any format (DD/MM/YYYY or MM/DD/YYYY). Show the expected format hint.
- **Checklist (checkbox group)**: At least "Select all" / "Clear all" for 7+ items. Show count of selected items.

## Connection to other chapters

Input patterns connect to action patterns in Ch5 (submit buttons). Mobile forms (Ch8) adapt these patterns for small screens + touch. Visual hierarchy (Ch9) governs form layout and emphasis. Design systems (Ch11) standardize form components and validation states.
