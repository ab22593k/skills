# Transparency + Adaptation — See It, Then Change It Safely

Source: Release It! Ch.16-18. Black Friday story proves visibility + component
restart beats reboot-the-world. Without transparency, system decays; without
adaptation, change costs more than it returns (must be exoeconomic).

## Transparency — four perspectives, different consumers

- Historical (last week = history): orders yesterday vs same weekday last year,
  disk Q1, last spike's limiter, traffic vs CPU 3yr. Store in OpsDB, explore via
  BI/Excel, never BI directly on OLTP prod.
- Future (yesterday's weather, 70% rule): capacity = "if next N users cost like
  last N." Correlative models OK for web commerce (not Neptune math); revalidate
  after every release (derivatives break). Sensitive, not for dashboard. "Can we
  survive holidays?" = projection of projection (error squared).
- Present status (fat man jogging: behavior OK, status one thump from MI):
  hardware+app+job state from events (required vs abnormal low/med/high) +
  params (OS: CPU/mem/swap/net/disk; pools: size/in-use/high-low-watermark/
  blocked/backlog; traffic: total/avg/aborts/rps/last/accepting; business: per-type
  count/abort/$/aging/conversion; users: demo/techno/registered/errors;
  integration: breaker state/override/uses/avg/fail-split/endpoint/concurrency;
  cache: items/RAM/hit/evicted/limit/build-time). Nominal = mean ±2σ for hour-
  of-week (retail overlays week-of-year; travel/floral count back from event).
  Dashboard red/yellow/green per Fig17.1 (green = all expected, no abnormal, all
  nominal; yellow = missing expected OR med abnormal OR off-nominal OR noncritical
  degraded; red = missing required OR high abnormal OR far-off OR critical wrong).
  Facets per role (ops=components, dev=apps, sponsor=features) with linkage
  (net failure -> affected business processes). Include batch expected-events
  (33-day silent batch failure = business bug).
- Instantaneous (what the ****?): thread dumps, stack traces, log errors, JMX.
  Monitoring watches this. Restrict dangerous channels (JMX shutdown), but don't
  hide status from sponsors — they need dashboard/history/projection, not traps/
  dumps. Tension dissolves when status is transparent.

## Enabling tech

Black-box (outside, ops can add later; help by making observable) vs white-box
(inside, must build in). Monitoring needs exoskeleton, not weave-in; policy
(thresholds, rollups) outside app (changes at different rate).

- Logging (white-box, still most versatile; every tool scrapes logs): configurable
  path (separate spindle, not under install; symlink/mount if must), levels for
  operators (ERROR = must act; user bad input = WARN at most; breaker trip/DB
  fail = ERROR; NPE != auto-ERROR), catalog with codes via Externalize Strings
  (`(FulfillmentClient.2) Timeout...` + Messages.getString prepending key; runbook
  lookup; accurate ops<->dev comms), human factors (columnar, level letter I/W/A
  - code, scannable; WebLogic default and j.u.l 2-line formats defeat eye+grep),
    txn IDs on every line, log state transitions even if also SNMP/JMX (post-mortem
    gold). No DEBUG in prod (build strips it; one commit leaks noise burying real).
    Voodoo ops warning: ambiguous "Reset required" debug left on caused 6mo of
    weekly peak-hour DB failovers from pure temporal coincidence — wording matters.
- Monitoring (black-box, dead procs log nothing): agents (OS stats, procs, log
  regex, ports, syslog/eventlog) + heartbeat (agent death vs net death) + reliable
  transport on separate VLAN (prod worm shouldn't kill monitoring; contains host/
  user/IP/log snippets — sensitive). Commercial (IBM/CA/HP + EAM suites from
  acquired app vendors) mature but IT-centric: missing business-feature linkage
  (which servers = which feature? impact of event on feature?) and user perspective
  (all green but users failing from profile/cookie/browser; Tealeaf-style edge).
  Design to standards (SNMP/CIM/JMX), not to vendor.
- Standards: SNMP (1988, "everything is variable": get/set/enumerate + traps;
  SMI/MIB in ASN.1, e.g. `1.3.6.1.4.1.2334...trapDestAdd`; platforms expose
  thousands of vars; custom MIB = specialized heavy lift + ops reluctance to
  install untrusted MIBs + C-struct vs objects mismatch). CIM/DMTF (OO, dynamic
  discovery, brokered; OS/HW adopting, app support thin — future). JMX (object
  view: MBean proxy per component, MBeanServer + RMI/HTTP connectors; pre-1.5
  needed impl (Sun RI/MX4J), 1.5+ built into JVM; JBoss kernel = JMX registry,
  WebSphere/WebLogic/Spring expose; scriptable shells wsadmin/wslt/twiddle =
  admin love). Expose every pool/cache/breaker/integration as MBean (StandardMBean
  for zero-pollution wrap); avoid dynamic-model overkill for app dev (platform
  builders' toy). What to expose: traffic, pool health, DB health, integration
  health, cache health (see SKILL.md list) — visibility now, policy later.
  JMX->SNMP bridge (AdventNet) maps props->vars, methods->sets, notifications->
  traps + generates MIB + agent — trivializes SNMP integration.
  Suitability: logging (behavior well, status with effort, history/future poor),
  monitoring (behavior+status well, history/future gap until EAM matures), OpsDB
  (history/future/status well).
- OpsDB (complementary, single pane + correlation): Apps (status vars, business
  - internal metrics) + Servers (perf/util) + Batch (start/end/abort/status/count)
    -> OpsDB -> capacity planning, dashboard, reports. Model: Feature (business
    function SLA/capacity unit, spans hosts/apps/firewalls/switches/SAN) — needs —
    Node (host/app/job, unique ID blocks per team, optional depends-on for cascade
    tracing) — reports — Observation (Measurement periodic kept / Status transition
    last-is-dashboard + history for flapping; + ObservationType defining universe).
    Feed via simple client API + CLI for scripts (record total vs processed vs abort;
    Java generic sampling MBean + notification listener). Use: Expectation per
    ObservationType (range/window/allowed status -> monitoring alerts), seeded from
    history to avoid false positives (Chiles alarm-fatigue story; pager 3x/night =
    normal is broken), tightening over time (80% -> 50% -> envelope/step fn by hour).
    Don't forget Steady State: condense minute samples >1wk or OpsDB becomes capacity
    risk.
- Supporting processes (data without loop = Outlook auto-delete report): OODA
  (Observe-Orient-Decide-Act, Boyd; orientation unbiased, no spin; each loop
  updates map + world, reinforcing -> speed inside enemy cycle = agility argument)
  / Deming Plan-Do-Check-Act. Rituals: weekly tickets (recurring/time-sinks/
  subsystem/third-party), monthly volume/severity (down + sawtooth on releases),
  daily/weekly exceptions+helpdesk (top categories + random hmmms), 4-6mo
  revalidate correlations, monthly volumes/query plans (top expensive, plan flips,
  table scans = missing index), demand vs metric envelopes (plateau = limiter,
  popularity drop = slowness). Per metric: vs history (OpsDB expectations), if trend
  continues what correlated metric breaks, what limiter hits first and result
  (orders↑ -> CPU? how long? add/opt/deter/optimize?). Shift reactive->predictive
  over time; retire dead metrics.

## Adaptation — release is birth, not death (40-90% cost after 1.0)

Form follows failure (Petroski): paperclip/fork evolve by fixing flaws; each
release fills gaps/files bumps if exoeconomic (returns > activation energy).

- Software: DI via interfaces (Pico/Spring/Avalon; Fowler's term; loose coupling
  - testability + rewiring; don't confuse with framework IoC), object design
    (loose coupling = few shared method-subsets across callers; tight cohesion =
    methods touch same state; extract hidden objects; small crystals = malleable,
    palace where every object touches all = dead, tiptoe; one object in many patterns
    = Gordian knot; minimize cross-crystal ties), XP (refactoring + unit tests twins;
    TDD+YAGNI -> adaptable; test forces DI + small context; Customer+persistence
    split shrinks crystal), agile DBs (behavior vs data false dichotomy; rigid schema
    -> semantic pollution in CLOBs/enums; ORM + version row + fail-fast on mismatch +
    Rails Migrations; bump version on semantic change too).
- Enterprise: top-down Colossus/Zachman/TOGAF assumes finishable + freezable —
  both false; stasis = death; version-locked ESB change = deploy-everything-at-once
  risk -> ossify/subvert (like static schema). Prefer ecosystem (niches, symbionts,
  7 SAPs inefficient but robust + independently adaptable; monoculture = Ada fate).
  Test: does it make IT respond better to users? Within system: loose clusters
  (lose one Apache of 12 = noise; no unique roles — WebLogic/WebSphere masters
  violate; bring up/down unordered; depend on VIP/service not members; no O(N^2)
  membership knowledge; broadcast via pub/sub not unicast). Between systems:
  version protocols so either end upgrades alone (Fig18.3 overlap, not Fig18.2 big
  bang; 2-wk agile throttled to quarterly partner otherwise); low-level = version
  in handshake (keep simple, immutable), RMI/CORBA = parallel interface names,
  XML = version field (beware JAXB dual-binding pain), files = auto-detect + old-gen
  support; overlap minutes (deploy) to quarters (slow partner). DBs: never integrate
  via DB (encapsulation violation, untrusted rows, bypassed logic, rigidity nexus;
  bigot's "logic in DB" = wrong place/tools). Need bulk? ETL quotas + select-only ID,
  materialized views, BCV SAN copies. Need fresh? check decision latency — hourly
  snapshot usually as actionable as realtime.
- Releases shouldn't hurt (haircut, not NASA): cost = branch/label/build + notes/
  training + marketing + deploy/verify + hotfixes + downtime (planned = still down
  to user; ops 99.5% excluding planned is dodge). Frequent + small wins (lean/agile/
  incremental funding: delight + outpace + force deploy skill + tighten feedback).
  Don't rush for arbitrary date (4pm go with QA failing = risk customers for calendar).
  Assume positive intent: dev/sponsor see value, ops sees risk — all correct.
  Zero-downtime via expand-migrate-contract: Expand (new URLs /static/1.2/,
  new WS endpoints/interface names, new tables/cols nullable no constraints, triggers
  to dual-write old<->new, explicit cols never SELECT *), Rollout (bake subset,
  separate LB pools per version to contain session failover, orderly drain), Cleanup
  (drop triggers/pools/old files/cols, add NOT NULL/FKs when all new). Needs dev+ops
  collab upfront; eliminates $10k/hr x4hr =$40k deploy tax.
