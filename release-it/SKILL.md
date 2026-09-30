---
name: release-it
description: Turn feature-complete code into production-ready systems. Use whenever user says feature complete, production ready, production readiness, release readiness, pre-launch review, will it survive launch, stability review, capacity review, X-nines availability, hardening, or asks about timeouts, circuit breaker, bulkheads, cascading failure, blocked threads, integration points, load testing, or operations readiness. Also use for design reviews of distributed systems, SOA, microservices, ecommerce, or any system that must stay up under real users, flash traffic, or failing dependencies.
---

# Release It! — Feature Complete != Production Ready

QA-passing code is designed for the lab. Production-ready code is designed
for cynical, hostile reality: crazy users, failing dependencies, flash mobs,
slow networks, full disks. This skill applies Nygard's stability, capacity,
design, transparency, and adaptation patterns.

## Core truths — why this exists

1. **Failures are inevitable. Design failure modes, or get random ones.**
   Every integration point will fail. Every crack (small fault) propagates
   under stress unless stopped by a crackstopper. If you do not design
   what fails first, physics will decide for you.
2. **Stability before capacity before features.** An unstable system has no
   future — short-term firefighting dominates. A stable but under-capacity
   system loses revenue. Only then do features matter.
3. **Follow the money.** Each stability/capacity decision is financial:
   one-time dev cost vs. recurring ops cost + downtime cost. Never save
   $5k in dev to spend $200k in downtime. Downtime math: at $100k/hr,
   98% vs 99.99% uptime = ~$17M/year difference.

## When to use / when not to

Use for: production-readiness reviews, pre-launch audits, stability or
capacity design, incident post-mortem hardening, SOA/microservice
boundary design, ops handoff, release-safety work.

Do NOT use for: pure functional correctness, unit-test logic, UI copy,
or one-line typo fixes. Defer to `production-grade` for code-shape
and to language/framework docs for API syntax.

## Workflow — 5 phases in order

Do phases in order. Skip a phase only by naming why it does not apply.

### 1. Stability triage (stay up)

Ask: "What kills us first when a dependency fails?"

- List every integration point (socket, HTTP/SOAP/REST, DB, queue,
  vendor SDK, DNS, filesystem). For each, demand: timeout + failure
  mode + caller behavior on failure. No unbounded blocking call survives.
- Trace chain of failure: crack -> propagation -> amplification.
  Mark tight coupling, shared threads, shared pools as accelerants.
- Map findings to `references/01-stability-antipatterns.md`.
  Most common killers: Integration Points, Blocked Threads,
  Cascading Failures, Unbounded Result Sets.
- Apply mitigations from `references/02-stability-patterns.md`.
  Default stack: Timeouts + Circuit Breaker + Fail Fast. Add Bulkheads
  for critical vs. non-critical separation, Steady State for sludge,
  Test Harness for out-of-spec simulation, Decoupling Middleware where
  sync is not required.

Read `references/01-stability-antipatterns.md` when you see hangs,
cascades, thread exhaustion, slow dependency, or "works in QA, dies
in prod." Read `references/02-stability-patterns.md` to choose the fix.

### 2. Capacity triage (handle load)

Ask: "What is the single constraint, and what happens 2x past it?"

- Define terms precisely: performance (single-txn speed) != throughput
  (txn/sec) != capacity (max sustained throughput at acceptable latency
  for a given workload). There is no single capacity number — it moves
  with workload mix.
- Find the constraint (Theory of Constraints): the one resource that hits
  its ceiling first. Improving non-constraints does not improve capacity.
  Look for the knee in load-test charts where correlation breaks.
- Distrust linear projection ("50% CPU at 10k users => 20k max").
  Hunt multiplier effects: 250ms extra/txn x 1M txn/day = 69 extra
  CPU-hours/day. 1KB junk/page x 1M pages/day = 1GB wasted transfer
  plus RAM, switch, firewall, web-server cost at every hop.
- Map findings to `references/03-capacity-antipatterns.md` and fix with
  `references/04-capacity-patterns.md`.

Read capacity references when you see slow pages, memory pressure,
DB saturation, session floods, or pre-holiday scaling questions.

### 3. General design issues (survive the data center)

Ask: "Will this behave on multihomed hosts behind real networks?"

Load `references/05-design-issues.md` for any deploy, networking,
security, availability-SLA, or operability review. Non-negotiables:

- Bind sockets to explicit interfaces, never all-interfaces by default.
- Track every integration's destination, route, firewall rule.
- Use virtual IPs / service names for clustered dependencies; expect
  IOException/SQLException on failover and retry once, bounded.
- Run as least-privilege user; passwords in separate files outside
  install dir, owner-read-only, no core dumps; vault + Tripwire where
  possible.
- Define availability per-feature (not "system 99.99%"), with probe,
  threshold, success pattern, frequency, locations, and formula.
  Never promise more than your worst dependency (SLA inversion).
- Keep QA topology faithful: separate hosts stay separate (VMware
  if needed), >1 instance where prod clusters, same firewall/LB vendor.
- Separate plumbing (DI wiring) from environment config; config lives
  outside install dir, versioned, with env-specific overrides in one place.
- Startup: verify in dependency order, pre-fill pools, do not accept
  work until ready, but stay queryable. Shutdown: drain, stop accepting
  new work, finish in-flight with timeout, then exit. Admin must be
  scriptable (CLI > HTML > GUI).

### 4. Transparency (see what is happening)

Ask: "If this fails at 3am, what tells us why in under 5 minutes?"

Load `references/06-transparency-adaptation.md` §Transparency when
adding observability or debugging prod.

- Expose everything you might need later: traffic, pool health
  (size/in-use/high-water/blocked-waiters), DB errors + latency,
  integration latency + error split (network/protocol/app), cache
  hit-rate + evictions, breaker state + transitions, GC time.
  Leave policy (thresholds, alerting, rollups) outside the app.
- Log for operators, not developers: ERROR = human must act.
  Externalize strings with codes (e.g. `(FulfillmentClient.2)`), include
  txn/session/user ID on every line, rotate by size, keep logs off
  prod disks after copy. Never leave DEBUG on in prod by accident.
- Assume monitoring is SNMP/JMX/CIM-based and chosen for you —
  expose via those standards, do not hard-couple to one vendor.
  Feed an OpsDB (Feature/Node/Observation + Expectation) for history,
  baselining, and capacity correlation. Review weekly tickets, monthly
  volumes, exceptions, help-desk clusters, top queries, demand envelopes.

### 5. Adaptation (change without pain)

Ask: "What is the activation energy of the next change?"

Load `references/06-transparency-adaptation.md` §Adaptation for
refactors, versioning, or release planning.

- Keep crystals small: loose coupling, tight cohesion, DI via interfaces,
  TDD + refactoring to prevent calcification. Version your schema
  (single version row, fail-fast on mismatch, expand-migrate-contract).
- Between systems: depend on service names, not instances. Version
  protocols so either end can upgrade independently (overlap period).
  Never integrate via another system's DB — wrap with a service,
  use ETL/materialized views for bulk reads.
- Make releases boring: automate to <1hr, no heroics. Time releases by
  readiness, not calendar. Use expand -> rollout -> contract for
  zero-downtime: add new tables/columns/endpoints/URLs first (nullable,
  no new constraints), dual-write via triggers/adapters, rollout with
  bake time, then enforce constraints and drop old artifacts.

## Output format — production-readiness review

ALWAYS structure a review as:

```markdown
## Production-readiness verdict: [SHIP / SHIP WITH FIXES / DO NOT SHIP]
## Top 3 risks (chain of failure for each)
1. [Crack] -> [propagation] -> [business impact + $/hr if known]
## Stability findings
- [Antipattern]: evidence, affected integration/thread-pool, fix -> Pattern
## Capacity findings
- [Constraint + evidence]: headroom, what breaks at 2x, fix
## Design / Transparency / Adaptation gaps
- [Gap]: cheapest fix that holds
## Suggested diff order (smallest safe first)
```

Keep it concrete: name files, pools, timeouts in ms, pool sizes,
endpoints. No generic "add resilience" without where and how.

## Pattern map (antipattern -> first patterns to try)

- Integration Points, Blocked Threads, Cascading Failures,
  Slow Responses -> Timeouts + Circuit Breaker + Fail Fast
- Chain Reactions -> Bulkheads + Circuit Breaker (caller side)
- Unbalanced Capacities -> Circuit Breaker + Handshaking + Bulkheads
- SLA Inversion -> decouple SLA per-feature + Circuit Breaker
- Unbounded Result Sets -> Handshaking (caller declares limit) + Timeouts
  as stopgap + explicit LIMIT/TOP/rownum
- Resource Contention, Pool Exhaustion -> Pool Connections (sized,
  bounded wait) + Fail Fast
- Cache bloat, stale data -> Use Caching Carefully (bounded, SoftRef,
  flush/invalidation strategy)
- Repeated dynamic rendering -> Precompute Content + punch-outs
- GC pauses -> Tune GC + reduce allocation (see Profanity Masker story)

Full matrices: Figure 3.1 interactions in references. When stuck,
expand scope (bigger purpose) or relax constraints to test value,
then re-tighten.

## Case studies to cite (not to repeat)

- Grounded Airline (Ch.2): uncaught SQLException on Statement.close()
  leaked connections -> pool exhaustion -> RMI (no timeout) hung
  kiosks + IVR. Fix was nested try/finally + timeouts + breaker.
- Trampled by Customers (Ch.7): 1.2k tested, 250k sessions on launch
  from spiders/scrapers/bots without cookies + 404s creating sessions.
  Fix was throttle/gateway, static home, kill scrapers, shrink sessions.
- Black Friday (Ch.16): 3000 front threads -> 450 mid threads ->
  25-capable scheduling singleton. Fix was dynamic pool max->0 +
  component restart, not full reboot.

## References — load only what you need

- `references/01-stability-antipatterns.md` — 11 killers, symptoms, chain
- `references/02-stability-patterns.md` — 8 crackstoppers, when/how
- `references/03-capacity-antipatterns.md` — 10 waste/multiplier traps
- `references/04-capacity-patterns.md` — pool, cache, precompute, GC
- `references/05-design-issues.md` — networking, security, availability, admin
- `references/06-transparency-adaptation.md` — observability + safe change
- `references/07-checklist.md` — one-page ship gate + incident questions
