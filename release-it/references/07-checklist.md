# Production-Readiness Ship Gate — One-Page Checklist

Use for go/no-go, design review, or incident hardening. Fail any CRITICAL =
DO NOT SHIP. Cite evidence (file:line, metric, chart), not vibes.

## Stability — CRITICAL

- [ ] Every outbound call (HTTP, RPC, DB, queue, SDK, DNS, FS) has connect
  timeout + read timeout + pool-checkout timeout in ms. No `wait()` without
  timeout, no `getInputStream()` without client timeouts. (Timeouts)
- [ ] Every integration has Circuit Breaker with distinct open exception,
  logged transitions, JMX-visible state, manual trip/reset, transition chart.
  Business owner signed off on open-behavior (fail open/closed/queued). (Breaker)
- [ ] Request threads never block unbounded on pools/locks/remotes. Pool
  max sized to threads for regular peak, bounded wait, caller handles
  null/exception. Vendor libs load-tested to 20x for hidden pools. (Blocked)
- [ ] Critical vs non-critical separated by Bulkhead (threads/CPUs/servers/VMs).
  Admin pool reserved. Shared service has per-client pools. (Bulkheads)
- [ ] Caller declares result limits on every query/call (LIMIT/TOP/rownum,
  offset/limit, max items). No `SELECT *`, no unbounded traversal
  (orders->lines, profile->visits, audit). Tested on prod-sized data. (Bounded)
- [ ] Slow dependency cannot cascade: Fail Fast at txn start (reserve conns,
  check breakers), 503 with documented contract when over SLA, Reload-safe
  (idempotent, no IP serialization). (FailFast)
- [ ] No single load-linked defect can chain-react whole tier: leak/timing hunt
  done, >1 instance in QA, bulkheads split blast radius. (Chain)
- [ ] SLA per feature documented (probe, threshold, success regex, freq,
  locations, formula). No feature promises more than worst dep. (SLA)

## Capacity — CRITICAL for launch/holiday

- [ ] Single constraint named with evidence (knee chart, correlation break).
  Non-constraints not "optimized." 2x test: slow+recover, not crash/hang/lie.
- [ ] Sessions: timeout = mean+1σ (~5-20min), keys not objects, SoftRef if objects,
  no session for bots/404s, affinity correct. Counted sessions, not "users."
- [ ] Pages: whitespace stripped, zero spacer GIFs (CSS/`&nbsp;`), CSS not tables,
  JSON not HTML for AJAX, debounced inputs, no polling. Measured bytes/page.
- [ ] DB: indexes on all association targets, no N+1, no hand SQL without DBA
  laugh-test + prod-sized EXPLAIN, partitioning/purge plan, reports off OLTP.
- [ ] Pools/caches/GC: pools monitored (wait/high-water), caches bounded +
  invalidation + hit-rate checked, hot content precomputed with punch-outs,
  GC tuned in prod-like load (<2% time), no object pooling except conns/threads.
- [ ] Multipliers computed: ms/txn x txn/day, bytes/page x pages/day, conns x
  hosts x instances. Bandwidth/CPU/storage priced with chassis/RAID/backup.

## Design — REQUIRED

- [ ] Sockets bind explicit interface (not 0.0.0.0); routes + firewall rules tabled
  per integration; clustered deps via VIP/service name with failover handling.
- [ ] Least privilege (own user, no root/Admin), passwords outside install dir,
  owner-only, no dumps, vaulted + Tripwire, out of source control.
- [ ] QA topology faithful (separate hosts separate, N>1 where prod clusters,
  same LB/firewall vendor). Plumbing separate from env config; config versioned,
  one place per prop, sync verified.
- [ ] Startup ordered + pool-prefilled + gated (no work until ready, still
  queryable); shutdown drains with timeout. Admin is CLI/scriptable (JMX),
  not click-ops.

## Transparency + Adaptation — REQUIRED for ops handoff

- [ ] Metrics exposed (traffic, pools, DB, integrations, caches, breakers, GC);
  ERROR means act; codes + txn IDs on logs; rotation on; DEBUG off; OpsDB
  feeding; dashboard with feature linkage; weekly/monthly review ritual set.
- [ ] Change is cheap: small crystals, DI via interfaces, schema versioned +
  fail-fast, protocol versioned for independent deploy, no DB integration,
  expand-migrate-contract release plan, automated <1hr deploy, date slips
  rather than ships broken.

## Incident questions (ask when red)

1. What is session/thread/pool high-water right now vs normal envelope?
2. Which breaker flipped first, and what is its downstream?
3. Which integration got slow first — network, protocol, or app?
4. Can we shed load (throttle %, disable pool max->0 + restart component)
   without rebooting world? What is the reversible throttle handle?
5. What did we change since last green (config, deploy, data volume, traffic mix)?
