# Reactive Coeffects (Spatial Composability)

A _reactive coeffect_ is a component's declared requirement from its
environment, managed at runtime. Each component carries a coeffect
specification over context keys; every context change is classified against
it, and the classification drives the component's lifecycle. This makes
spatial composability local to one component: dependencies are not a static
install-time list but a live contract the runtime enforces.

## Classifying context changes

| Change                                             | Classification | Runtime action                                                     |
| -------------------------------------------------- | -------------- | ------------------------------------------------------------------ |
| All required keys available (including first load) | Activating     | Start the component                                                |
| A satisfied requirement becomes unavailable        | Deactivating   | Deactivate, then apply accumulated inverses (same path as removal) |
| Anything else                                      | Neutral        | Nothing; the component is undisturbed                              |

A component whose dependency is unavailable simply stays inactive until the
dependency appears — it must not poll, retry-loop, or crash. **(observed on
v3)**

## Ordering rules

- A component begins only when its declared dependencies are present.
- A provider withdraws a binding only after dependent fibers have
  deactivated. Never pull a service out from under live dependents; drain
  them first.
- Components whose provisions overlap another's declarations are
  _entangled_: the lifecycle rules order them instead of treating them as
  independent. When two components declare conflicting requirements on the
  same context, resolve the conflict explicitly (pick a provider, scope the
  keys, or keep one inactive) — the runtime will not guess.

## Gotchas

- **Health-check spaghetti.** Hand-rolled polling ("is the service back
  yet?") duplicates the classifier badly. Symptom: N components each
  polling the same dependency on different intervals. Check: delete the
  polling code — activation must still happen exactly when the context
  changes.
- **Pause that leaks.** Deactivation must run the inverse path, not a flag
  flip that keeps subscriptions alive. Symptom: dependency flaps and handler
  counts grow. Check: activate → deactivate → reactivate leaves exactly one
  live registration set.
- **Undeclared needs.** A component that reads a context key its spec does
  not declare is invisible to the classifier and will keep running with a
  dead client. Symptom: errors after a provider restart that no lifecycle
  event explains. Check: every key the component touches appears in its
  specification.
- **Synchronous-teardown expectations.** Cordis unloads asynchronously;
  code that assumes dependents vanish in the same tick will race the drain.
  Symptom: use-after-withdraw under rapid provider churn. Check: exercise
  provider withdrawal while dependents are mid-request.

## Verification

- With the dependency absent, confirm the component stays inactive and
  reports the missing requirement (no polling, no crash).
- Provide the dependency and confirm activation; withdraw it and confirm
  clean deactivation with inverses applied.
- Restore the dependency and confirm reactivation leaves exactly one live
  registration set.
