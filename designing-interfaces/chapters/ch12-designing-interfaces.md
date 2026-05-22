# Chapter 12 — Smart Systems

## Core concepts
- Smart systems go beyond static interfaces — they sense context, anticipate needs, and adapt behavior
- Machine learning enables personalization but introduces opacity: users must trust and understand the system
- Not every interface needs AI — use smart features only when they clearly reduce user effort
- Transparency and control are essential: users should know why a system made a suggestion and be able to override it

## Frameworks introduced
- **Anticipatory interface** — Predicts user intent and takes action before the user asks (e.g., calendar suggesting travel time). Requires good data and clear fallback.
- **Contextual interface** — Adapts based on environment: location, time of day, device, user role, recent behavior. Reduces choices to what's relevant now.
- **Assistive interface** — Guides the user step-by-step through a task. More directive than a wizard — actively helps rather than just presenting steps.
- **Natural user interface (NUI)** — Interaction through voice, gesture, touch, gaze, or thought. Moves beyond WIMP (windows, icons, menus, pointer).
- **Feedback loop** — System action → user reaction → system learns → improves → new action. Design for graceful failure when predictions are wrong.
- **Progressive AI** — Start as a simple rules-based system. Add ML as data accumulates. Don't promise intelligence you can't deliver.

## Key techniques
- **Explainable AI**: Surface why a recommendation was made ("Because you watched X..."). Show confidence level for uncertain predictions.
- **Control and override**: Every automated action must be reversible. Allow users to customize, disable, or correct the system's behavior.
- **Safe failure modes**: When the system can't predict (no data, ambiguous), fall back to a neutral default. Never guess with high confidence.
- **Privacy-first design**: Collect minimum data. Be transparent about what's stored. Allow data export and deletion. On-device processing where possible.
- **Calm technology (Weiser)**: Technology that moves to the periphery when not needed and re-emerges when relevant. Design for attention, not for engagement.

## Connection to other chapters
Smart systems sit on top of all prior chapters — they use the same patterns for navigation (Ch3), layout (Ch4), input (Ch7), and visual style (Ch9), augmented with contextual and predictive behavior. Mobile (Ch8) is a primary context for smart features (location, notifications, anticipatory actions). Design systems (Ch11) need smart-system extensions for contextual states and AI-driven UIs.
