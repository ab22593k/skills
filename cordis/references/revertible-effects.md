# Revertible Effects (Temporal Composability)

A _revertible effect_ is a component's change to its environment that carries
its own undo. When a component performs a context-mediated change, the
operation returns both the changed context and an _inverse_; the runtime
retains the inverse and composes inverses last-in, first-out. Removing (or
deactivating) the component applies its accumulated inverses, restoring the
prior context. This is what makes temporal composability local to one
component: each component cleans up exactly itself, so removal never forces
a process restart that would discard other components' caches, connections,
or partial computations.

## How to structure a component's side effects

1. Route every change the component makes — registrations, subscriptions,
   handles, bindings — through a context key, so each yields an inverse at
   perform time.
2. Never rely on teardown-time reasoning: no hand-written "undo everything"
   callback, no require-cache deletion, no restart. The runtime's
   accumulator is the teardown plan.
3. On removal the runtime enters the asynchronous unloading state and
   applies the accumulator LIFO. Deactivation (dependency lost) follows the
   same path — see [reactive-coeffects](reactive-coeffects.md).

## When revertible handling applies

| Situation                                                                             | Handling                                     | Why                                         |
| ------------------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------- |
| Change goes through a context key                                                     | Revertible effect; runtime holds the inverse | Removal restores pre-load-equivalent state  |
| One-off setup with no observable residue                                              | Plain setup/teardown                         | No inverse needed; nothing to restore       |
| Change outside the mediated context (sent message, foreign process state)             | Out of scope — say so                        | The runtime never saw it; it cannot undo it |
| Physically irreversible but interface-hiding (allocator high-water mark, heap layout) | Accept the representation difference         | Recovery is observational, not physical     |

## Gotchas

- **Cache deletion is not a revert.** Dropping a module from the loader
  cache re-runs its top-level code on next load but undoes none of its
  registrations. Symptom: "disabled" plugin still receives events. Check:
  list the component's context keys before and after removal — both lists
  must match the pre-load state.
- **In-flight effects at removal time.** An inverse may run after another
  component changed the same context. The context paradigm covers this only
  where the operations commute (distinct keys are independent by
  construction; shared keys need commuting operations — serialize
  order-sensitive ones like middleware insertion). Symptom: revert succeeds
  in isolation but corrupts under load. Check: exercise removal while a
  neighbor component is active, not just in a quiet system.
- **Failed inverses must be contained, never skipped silently.** If an
  inverse cannot be applied, surface which key failed and quarantine the
  component (do not leave it half-removed and do not let the failure spill
  into other fibers). Symptom: removal "succeeds" but a later load of the
  same component behaves differently. Check: reload-after-remove must behave
  identically to first load.
- **Deactivation is removal's twin.** A component that loses a dependency
  must travel the same inverse path, not a cheaper "pause" that leaks
  subscriptions. Symptom: flapping dependency accumulates duplicate
  handlers. Check: activate → deactivate → reactivate must leave exactly one
  live set of registrations.

## Verification

- Before removal, record the component's context keys and each key's
  observable state through its declared operations.
- After removal, confirm every key reads as before load (interface behavior,
  not byte identity) and no subscriptions, timers, or handles from the
  component remain.
- Reload the component and confirm behavior is identical to first load.
