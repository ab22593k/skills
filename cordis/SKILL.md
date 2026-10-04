---
name: cordis
description: Dynamic composition for plugin systems and self-evolving agent harnesses via the Cordis context paradigm. Use whenever components must be added/removed at runtime with fully reverted side effects (revertible effects), activated/deactivated by declared dependencies (reactive coeffects), loaded from a declarative set with config reconciliation, or hot-replaced without restart. Use even when the user says only 'disable plugin without restart', 'keeps running with a dead dependency', or 'deploy one plugin without touching the rest'. Not for general plugin tutorials, dependency-injection frameworks, or formal proof work.
---

# Cordis

Cordis is a meta-framework of spatiotemporal composability: a runtime
discipline that lets independently written components share one long-running
process and still be added, removed, and updated without restarts or
collateral damage. Two orthogonal dimensions, from Shi, Zhang, and Cui's
"A Programming Paradigm for Spatiotemporal Composability" (arXiv 2608.25512):

- **Temporal composability** — removing a component completely reverts its
  side effects. Every context transformation carries an _inverse_ that the
  runtime holds; teardown applies the accumulated inverses, last-in
  first-out. See [revertible-effects](references/revertible-effects.md).
- **Spatial composability** — components declare their dependencies and the
  runtime manages them reactively. Every context change is _classified_
  against each component's coeffect specification to drive activation and
  deactivation. See [reactive-coeffects](references/reactive-coeffects.md).

Both dimensions are mediated through a **single context type** — the context
paradigm. Every effect and coeffect passes through the shared, recursively
structured context, and the mediation induces an observational equivalence:
up to what each key's operations can observe, the effects of distinct
components interleave without disturbing one another. The calculus carries
this per-component guarantee to whole systems of interleaved components
(running instances are called _fibers_; the recovery theorem covers fiber
accumulators up to key-induced equivalence).

The guarantee has a hard boundary: **only context-mediated interactions are
covered**. Operations outside the system boundary are not tracked or
reverted, and recovery restores behavior visible through the declared
interface — not physical identity. A sent message stays sent. Keep this
boundary in mind in every section below; each one names what it cannot do.

Cordis is not another service orchestrator. OSGi Declarative Services and
iPOJO react to service availability with hand-written, synchronous
deactivation callbacks; Cordis instead tears down with the runtime's
accumulated inverse effects and provides an asynchronous unloading state.
If the user actually wants DI-framework wiring or container orchestration,
say so and stop — this skill does not apply.

## Sources and evidence labels

- Theory: Shi/Zhang/Cui, arXiv 2608.25512 (presented as Cordis v4).
  Conceptual claims cite the paper; check behavior against the paper before
  writing it down.
- Practice: the Koishi ecosystem (4,000+ plugins) running Cordis v3 —
  live disable, HMR preserving caches and connections, affected-only
  reactivation, inactive-until-dependency. The core model is shared across
  v3/v4, but v3-observed behavior carried into v4 framing is marked
  **(observed on v3)**. The case study is observational (one ecosystem, one
  host language); overhead and productivity comparisons are stated future
  work — make no efficiency claims.
- Claims carried from the paper without local verification are marked
  **(unverified)**. Version-sensitive statements carry the verified version.

## Removing a component cleanly (temporal)

Structure every side effect as a revertible effect: perform each change
through a context key so it yields an inverse the runtime holds, and let
removal apply the accumulated inverses LIFO. Never substitute cache
deletion, hand-written mega-teardowns, or restarts.

| Situation                                     | Handling                                           |
| --------------------------------------------- | -------------------------------------------------- |
| Change goes through a context key             | Revertible effect; removal restores pre-load state |
| Residue-free setup                            | Plain setup/teardown                               |
| Change outside the mediated context           | Out of scope — say so explicitly                   |
| Irreversible representation, hidden interface | Accept the difference (observational recovery)     |

Verify: snapshot the component's keys before load and after removal (both
must match pre-load), confirm no subscriptions/handles remain, and confirm
reload-after-remove behaves identically to first load. Full mechanism,
in-flight-removal handling, and failed-inverse containment are in
[revertible-effects](references/revertible-effects.md) — read it when
implementing removal or diagnosing a "disabled but still active" plugin.

## Reacting to dependencies (spatial)

Declare every need as a coeffect specification over context keys and let the
runtime classify each change: all-required-available activates, a satisfied
requirement withdrawn deactivates (then inverses apply, same as removal),
anything else is neutral. Providers withdraw only after dependents
deactivate.

| Change                     | Classification                    |
| -------------------------- | --------------------------------- |
| Requirements met           | Activating — start                |
| Satisfied requirement lost | Deactivating — drain, then invert |
| Anything else              | Neutral — undisturbed             |

Rules of thumb: no polling loops (the classifier is the health check);
declare every key touched (undeclared reads are invisible to the
classifier); resolve conflicting declarations explicitly. Mechanism,
entangled-component ordering, and async-unload races are in
[reactive-coeffects](references/reactive-coeffects.md) — read it when a
component misbehaves across dependency churn.

## Loading declaratively and updating hot (loader)

Describe the component set declaratively; the loader diffs desired vs.
running and moves only what differs. Hot replacement swaps one component in
place with unrelated state preserved.

| Conflict                     | Resolution                                    |
| ---------------------------- | --------------------------------------------- |
| Commuting difference         | Adopt desired for that component only         |
| Order-sensitive difference   | Drain dependents, apply, reactivate in order  |
| Irreconcilable contradiction | Refuse with the mismatch report — never guess |
| Dependency unavailable       | Component stays inactive; rest of set loads   |

Never restart the process to "reload". Diffing, reconciliation reporting,
and spec-changing-update handling are in
[loader-and-hmr](references/loader-and-hmr.md) — read it when designing the
deploy flow or diagnosing drift between the description and the running
system.
