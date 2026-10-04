# Declarative Loading, Reconciliation, and HMR

The Cordis loader turns the theory into daily operation: a whole component
set is described declaratively (components plus configuration), and the
runtime reconciles that description with the running system. Operators edit
the description; the loader diffs desired vs. running state and moves only
what differs. Hot module replacement applies an edited component in place,
preserving unrelated state — **(observed on v3)** caches stay warm and live
connections elsewhere in the system survive.

## Reconciling configuration

1. Diff the declarative description against running state per component.
2. Report every mismatch with a resolution: adopt desired, keep running, or
   merge where the key's operations allow it.
3. Apply changes component by component: affected dependents deactivate and
   reactivate; unaffected components are untouched.
4. Never reconcile by restarting the process. A full restart that changes
   startup order and loses unrelated components is the failure mode this
   loader exists to prevent.

| Conflict                                             | Resolution                                                   |
| ---------------------------------------------------- | ------------------------------------------------------------ |
| Desired differs from running, key commutes           | Adopt desired for that component only                        |
| Desired differs, operation order-sensitive           | Serialize: drain dependents, apply, reactivate in order      |
| Description contradicts running state irreconcilably | Refuse with the mismatch report — do not guess               |
| Dependency unavailable at load                       | Component stays inactive until it appears; rest of set loads |

## Hot replacement

Replace one component while the system runs: drain its dependents, apply its
accumulated inverses, load the replacement, reactivate what its new
specification allows. If the replacement changes its dependency
specification, treat it as a new contract — reclassify all dependents
before reactivating.

## Gotchas

- **Restart-shaped "reload".** Anything that restarts the process and
  replays startup is not HMR, however fast. Symptom: unrelated plugins drop
  connections on every deploy. Check: replace one component and confirm
  neighbor state (caches, connections) is preserved.
- **Silent auto-merge.** Guessing a resolution for an irreconcilable
  mismatch trades a loud, fixable error for quiet divergence. Symptom:
  running state drifts from the description with no report. Check: every
  applied change traces to a reported mismatch entry.
- **Spec-changing hot update.** A replacement with different dependencies
  silently keeps old dependents wired. Symptom: new code paths with stale
  providers. Check: hot updates carrying spec changes force dependent
  reclassification before reactivation.
- **Order drift on restart.** Startup-order-dependent systems break when a
  full restart shuffles the order. Symptom: deploys that fail only
  sometimes. Check: the loader, not startup sequence, determines activation
  order.

## Verification

- Change one entry in the description and confirm only affected components
  reactivate; all others keep running undisturbed.
- Introduce a conflicting entry and confirm the loader reports the mismatch
  with a resolution instead of applying or crashing.
- Hot-replace a component and confirm neighbor caches and connections
  survive, and that reload-after-replace behaves like first load.
