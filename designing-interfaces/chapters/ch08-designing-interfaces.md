# Chapter 8 — Mobile Design

## Core concepts

- Thumb zones: easy (bottom-center), stretch (middle), hard (top corners) — place primary actions in easy zones
- Touch targets must be ≥ 44px (Apple HIG) or ≥ 48px (Material Design)
- Gestures (swipe, pinch, long-press) are invisible — must be taught or signposted
- Mobile first: design for the smallest screen, expand to larger ones
- One primary action per screen; everything else is secondary

## Frameworks introduced

- **Thumb zone map** — The screen divided into zones: safe (bottom, easy reach), neutral (middle, slight stretch), hard (top, thumb stretch/phone tilt). Bottom nav + primary action at bottom.
- **Bottom navigation** — 3-5 tabs at the screen bottom. Always visible. Active tab highlighted. Never more than 5.
- **Card list** — Vertically scrolling list of cards with thumbnail + title + summary. Pull to refresh. Infinite scroll or load more.
- **Mobile form** — One field per step (or few). Top-aligned labels. Full-width inputs. Big touch targets.
- **Action sheet / Bottom sheet** — Slide-up panel for actions or options. Contextual to the current screen.
- **Undo bar** — Snackbar/toast with "Undo" button. Replaces modal confirmations for destructive actions (delete, archive).
- **Gesture design** — Swipe: reveal actions, navigate back. Pinch: zoom. Long-press: context menu. Tap: primary action. Every gesture needs a visible fallback.

## Key techniques

- **Mobile navigation hierarchy**: Bottom tab bar (top 3-5) + secondary entries in a top app bar menu or drawer
- **One-thumb design**: Everything reachable within thumb arc on a 6" phone
- **Touch feedback**: Visual (highlight on tap), haptic (on confirmation), or both. Instant response (under 100ms).
- **Offline awareness**: Show cached content when offline, with "Last updated" timestamp. Queue actions for later sync.
- **Responsive adaptation**: Mobile nav (bottom tabs) → tablet (side nav + tabs) → desktop (side nav + content). Not just stacking.

## Connection to other chapters

Mobile design applies navigation patterns from Ch3, layout from Ch4, actions from Ch5, input from Ch7, and visual hierarchy from Ch9 — all adapted for touch and small screens. Smart systems (Ch12) overlays contextual and assistive behaviors for mobile.
