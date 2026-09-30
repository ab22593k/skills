# Capacity Patterns — 4 Ways to Buy Headroom with Software

Source: Release It! Ch.10. Hoare: forget small efficiencies 97% of time, but
architecture for scaling is not premature — it obviates optimization. Small
per-txn waste x millions = $10M hardware to survive holidays. These four
saved that.

## 1. Pool Connections — eliminate 400-500ms setup per txn

Perl-CGI open-use-close dies when DB spends more time managing conns than
txns. Pool always (no excuse), but:
- Bad conn poisons pool: checkout -> error -> return -> next victim gets it
  (1 bad in 10 causes >10% errors since good stay checked out). Need validation
  + eviction.
- Sizing: undersize = contention knee; oversize = DB RAM/process stress.
  Monitor wait time, high-water, created/destroyed.
- Checkout scope:
  * per-page (conn for whole page, single txn): deadlock-safe (global order),
    needs more conns (held longer).
  * per-fragment (each fragment own conn): higher throughput, fewer conns,
    deadlock-prone, isolated (no global txn knowledge).
  * hybrid (fragments manage conns, txn spans page): safe+isolated but large
    pools + phantom reads (fragment sees prior fragment's uncommitted data —
    hard to debug).
- Rule: bounded checkout wait + caller handles null/exception. Monitor
  contention or enhancer becomes killer.

## 2. Use Caching Carefully — powerful, double-edged

Good cache cuts DB + latency; bad cache eats RAM -> GC thrash -> slower than
no cache.
- Bound max memory (configurable). Unbounded = leak requiring nightly restarts.
- Hit-rate matters: cache miss + bookkeeping > regenerate? Don't cache
  single-space JSP conditionals, single-use or trivial objects.
- Java: SoftReference payloads — GC reclaims softly-reachable before OOM;
  code must handle null (recompute/redirect).
- Multilevel (RAM + disk) when working set > RAM, objects huge (images), or
  fetch crosses WAN.
- Invalidation strategy is capacity decision: point-to-point OK for 10 servers,
  queue/multicast for 100s (but avoid thundering herd reloading same row).
  Always have flush (clock/calendar/event) with rate-limit.
Compare access vs change frequency; don't cache what changes before reuse.

## 3. Precompute Content — render once, serve millions

Dynamic-by-default (JSP/ASP/Rails) renders category menu 1M/day though it
changes weekly. Even cached-query + render wastes strings/CPU.
- Identify content with change-rate << read-rate (top categories, home,
  Slashdot/Fark front). Regenerate on change event, serve static.
- Personalization vs precompute: if whole page personal, can't; if 100B
  personal in 100KB shared (greeting+cart in generic home), punch-outs:
  precompute 99.9%, inject personal fragments.
- Cost: storage + file-map/read (cache hot in RAM if needed). Generation cost
  moves from per-request to per-change (1/week vs 1M/day = win).
- Horror story: Profanity Masker — 20 droplets/page tokenizing every word vs
  Vector of 11 bad words, 10MB garbage/request, 5M views/day, on nightly-
  published static copy. Removed -> remake rate unchanged (contract forbade
  altering copy anyway).
Not all-or-nothing: precompute hot areas, keep cold dynamic.

## 4. Tune the Garbage Collector — quickest 8% win

Untuned prod Java spends ~10% in GC; tune to <2%. Bimodal lives: ephemeral
(eden, dies in µs, cheap if short-lived) vs long-lived (tenured, examined rarely)
+ PermGen (classes). -verbosegc + jconsole (heap by gen, GC time) to see.
Size heap + gen ratios for app + demand; Sun guides for 1.4.2/5 apply in spirit
to modern collectors (G1/ZGC: same — measure allocation rate, promotion rate,
pause vs throughput).
- Retune every major release + seasonally (promos shift feature mix).
  Tuning exposes leaks (heap never recovers).
- Don't pool ordinary objects (commons-pool NameFormatter test: 20-31% overhead
  pooled vs 10-23% disposable). Pool only truly expensive: conns, threads,
  sockets. Short-lived is GC's fast path; pooling adds bookkeeping + tenuring.
Remember: tune in prod-like load, not dev/QA; user patterns dominate optimum.
