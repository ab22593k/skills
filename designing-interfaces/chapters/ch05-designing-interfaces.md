# Chapter 5 — Doing Things

## Core concepts
- Actions need clear affordances: buttons look pressable, links look clickable, drag handles look grippable
- Direct manipulation (drag, resize, reorder) feels natural but must be visually taught
- Distinguish: buttons (immediate action), links (navigation), toggles (binary state), menus (multiple options)
- Keyboard shortcuts and command palettes (Ctrl+K) power users; don't reveal to beginners

## Frameworks introduced
- **Button hierarchy** — Primary (one, filled/high-contrast), secondary (outline, multiple), tertiary (text-only, low emphasis). Never more than one primary per view.
- **Toggle / Switch** — Binary controls that change state immediately. Label should describe the controlled item ("Notifications"), not the state.
- **Context menu / Popover** — Right-click or long-press reveals action menu. Avoid hiding primary actions here.
- **Command palette** — Modal overlay triggered by keyboard shortcut (Ctrl+K/Cmd+K). Lists available commands as typeahead. Essential for keyboard-heavy apps.
- **Split button** — Primary action + dropdown of related alternatives (e.g., "Save" + "Save as...")
- **Toolbar** — Row of icon+label action buttons, usually at top of content area. Group related tools.

## Key techniques
- **Affordance design**: Buttons should have visual depth (shadow, gradient). Links should be underlined (or use color consistently). Draggable items show a grip handle.
- **Undo / Redo**: Support beyond one level. Show toast confirming the undone action with "Redo" button.
- **Drag and drop**: Show a visual preview during drag. Indicate drop targets with highlight. Support keyboard once initiated.
- **Action confirmation**: Only confirm destructive actions. No confirmation needed for common actions (delete shows undo bar instead).

## Connection to other chapters
Action patterns use visual hierarchy from Ch9 (button styling). Forms (Ch7) include action buttons. Mobile (Ch8) changes how actions are presented (bottom sheets, gestures). Design systems (Ch11) standardize button, toggle, and toolbar components.
