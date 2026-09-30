# Capacity Antipatterns — 10 Ways to Turn Electricity into Heat

Source: Release It! Ch.8-9. Capacity = max sustained throughput at acceptable
latency for a given workload. Performance = single-txn speed. Throughput =
txn/sec (bottleneck-limited). Scalability = how throughput moves with load /
how you add capacity (wide = more servers, big = bigger servers).

## Constraint thinking (read first)

One constraint sets capacity. Improving non-constraints is waste. Find it via
driving variables (outside control: demand, clock) vs following variables
(CPU, RAM, I/O, swap, bandwidth). Strong correlation until knee, then break.
Knee + falloff = constraint hit. Elevate by adding resource or using less.
Horizontal (shared-nothing behind VIP/LB, near-linear) vs vertical (bigger
chassis, forklift at limit, $$$/CPU spikes: Sun440 1.2x at break, Fire6900
$200k chassis, E25K $1M+ for 73rd CPU). Prefer wide; pay incrementally.

Myths with multipliers: CPU is NOT cheap (250ms x 1M txn = 69 CPU-hrs/day +
web-server RAM/sockets held + 5th CPU needs new chassis+RAM+licenses+cooling).
Storage is NOT cheap (1GB x 20 servers x RAID1 2x = 40GB + backups window +
managed $7/GB). Bandwidth is NOT cheap (pair OC3 $15-24k/mo, 310Mbps max;
broadband users eat 13x dialup; 1KB junk x 1M pages = 1GB/day + per-hop cost).

## 1. Resource Pool Contention

Blocking for pooled resource (DB conn: 400-500ms to create, so pool, but...).
Contention % -> 80%+ at 30 threads on 4 conns; throughput flattens at knee
(threads > resources). Fix: size to request threads for regular peak (no
contention normally), bounded wait (maxWait/blocking-timeout) returning
null/exception that code handles, monitor high-water/blocked-waits/created.
Watch DB side: 20 hosts x5 instances x50 conns =5000 conns x1MB =5GB RAM;
Oracle MTS needs priesthood. Contention <-> latency vicious cycle; infinite
wait = stability bug.

## 2. Excessive JSP Fragments / Excessive Templating (code-as-content)

25k content JSPs compiled to classes in PermGen with -noclassgc = fill PermGen,
GC thrash, crash before serving. Code-as-content. Fix: HTML fragments in
content repo + cache, not classes. General rule: don't load code for content.

## 3. AJAX Overkill

Gmail/Maps pattern misapplied: single-master-page breaking Back button,
250ms polls for autocomplete, missing session affinity (failover storm),
HTML fragments instead of JSON (verbose). Requests shift 5-10s think time to
1-3s. Fix: AJAX only for single user-task chains; debounce (500ms after typing
stops); session cookie on every call; JSON data not HTML; grow web tier
(MaxClients) and measure.

## 4. Overstaying Sessions

30-min default keeps dead sessions (user gone at start of timeout) eating RAM.
Set timeout to mean think-time +1 sigma (~10min retail, 5 media, 20 travel).
Better: make session a pure cache of persistent state (cart/search saved in DB),
keys not objects, SoftRefs if must hold objects. Users don't understand
timeouts except for security; cart must survive 24 + work interruption.

## 5. Wasted Space in HTML

200KB->150KB saves 10s on dialup + CPU to generate + RAM/bandwidth at every
hop (app NIC -> switch -> firewall -> web RAM -> firewall -> router) + holds
web conns open (finite!) blocking revenue txns.
- Whitespace: 100 JSP includes -> 600KB page, 1/3 newlines. Cost real
  ($15k/yr bandwidth alone). Filter via interceptor if cheaper than RAM/bw.
- Spacer GIFs: 53B `<img>` -> 5B `&nbsp;` or CSS. 48B x12 x1M =576MB/day +
  extra cache-validation hits. Kill 1px images.
- Tables for layout: resend superstructure every page. CSS file once. Halves
  page size (see csszengarden).

## 6. The Reload Button

Slow page (>10s, e.g. full-GC pause) -> user Reloads -> browser drops old conn,
opens new, app keeps processing old (buffered connector hides drop until done).
Second txn may block/deadlock on first (profile update, tracking). No perfect
fix; make Reload irrelevant via speed. Don't serialize on source IP (breaks
behind Akamai/corporate proxy; queues frustrated Reloads). Code must tolerate
same user running same txn N times concurrently.

## 7. Handcrafted SQL

ORM SQL is predictable -> tunable. Hand SQL is idiomatic: non-indexed joins,
5-table x8-way UNION (40 table scans/page to print), procedural N+1 loops,
exotic features. Tuned-for-rest hurts one-offs and vice versa. Dev DBs too small
to show it. Fix: minimize hand SQL, prefer hints/indexes/views; laugh-test with
DBA; verify on prod-sized scrubbed data or generator. Dynamic WHERE assembly
belongs in reporting, not OLTP.

## 8. Database Eutrophication — lake dies from sludge

ORM relations without DBA review -> missing FK indexes -> table scans (fast on
toy data, minutes in prod). Schema designed early drifts from access pattern
(agile churn); keep architect involved. Growth-rate guesses wrong (1GB/yr ->
1GB/day audit). Fix: index association targets, partition by small finite key
(day-of-week: reorganize one partition online), purge/archive rigorously,
never report in OLTP (star schema in warehouse; cap prod visibility to 90d/6mo
to discourage abuse).

## 9. Integration Point Latency — house advantage

Remote >=1000x local. Location transparency lies: different failures + chatty
1+N (parent +3 calls/child; UK tree expand 1s -> 20min over WAN). Blocked thread
holds RAM/CPU/DB conn/row locks; opportunity cost (could serve queued work).
Fix: coarse interfaces (Summary objects in one call), fewest round trips,
never chatty.

## 10. Cookie Monsters — bottle rockets invite self-harm

Cookies for <100B IDs, not 4KB serialized carts/XML. Old serialized carts break
on code change (IOException as routine), bypass referential integrity, allow
price-tampering ($0.01), resend+reparse 2-4x per request (web->app), hurt
upstream (asymmetric broadband). Storing anon carts to avoid purge job trades
cents of DB for daily ops+maintenance cost. Fix: IDs in cookies, state on server
where client cannot lie; still validate (proxy/Firefox extensions lie).
