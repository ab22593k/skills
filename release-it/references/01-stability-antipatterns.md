# Stability Antipatterns — 11 Ways Cracks Propagate

Source: Release It! Ch.3-4. Use to name the killer during triage.
For each: symptoms to grep, why it accelerates cracks, cheapest fix pointer.

Core model: transaction = business unit of work. System = hosts+apps+nets
that process it. Resilient = keeps processing under impulse (sudden shock:
flash mob, Slashdot, 12M queued msgs) or stress (prolonged force: slow
processor) or component failure. Strain = deformation under stress.
Crack = initial fault. Crackstopper = designed failure mode (crumple zone).
Chain of failure = coupled steps where each failure raises next-failure odds.

## 1. Integration Points (No.1 killer)

Every socket/pipe/RPC/DB call can hang, refuse, dribble, or lie.

- Socket: fast fail (refused/reset in ms) vs slow fail (listen-queue full,
  firewall idle-drop, half-open conn). Slow ties up caller thread for
  minutes (OS TCP timeout 10-30min; Java blocks forever by default).
- Firewall idle timeout: idle pooled conns dropped silently; next write
  blocks on retransmit. LIFO pools reuse 1 conn, leave N-1 to go stale —
  5am hang when traffic ramps. Fix: DB dead-connection ping, validate on
  checkout with timeout, discard idle > firewall timeout.
- HTTP via URLConnection: single blocking getInputStream(), no timeout
  pre-Java5, no socket access. Use Apache HttpClient with conn+read timeouts.
- Vendor SDKs: hidden pools, hidden sync, no timeouts. Decompile, load-test
  to 20x parallelism, look for throughput cliff.
  Defend: Timeouts + Circuit Breaker + Decoupling Middleware + Handshaking

* Test Harness that simulates refused/slow/dribble/garbage/reset.

## 2. Chain Reactions — one node dies, rest follow

Homogeneous load-balanced farm: 8 nodes at 12.5% each. One dies -> 7 at
14.3% (+15% per survivor). 2-node cluster: survivor doubles. If first died
from load-linked defect (leak, race), survivors now more likely to die.
Gap shrinks: 5min -> 3min -> seconds. Seen in search-engine memory leak
(noon crash cascade).
Hunt leaks + timing bugs under load. Defend: fix defect (only cure) +
Bulkheads to split one cascade into slower separate ones + Breaker on caller.

## 3. Cascading Failures — crack jumps layers

Caller layer fails because callee failed. Jump mechanism is usually blocked
threads or drained pool. Example: DB dark -> app tears down conn on any
SQLException -> every page creates conn, fails, logs stacktrace.
Integration Points without Timeouts guarantees this.
Defend: Timeouts + Circuit Breaker. Scrutinize pool wait policy.

## 4. Users — terrible, necessary

- Traffic: every session = RAM + CPU + bandwidth. 30-min default timeout
  means dead sessions linger. Keep session tiny; prefer keys over objects;
  SoftReference for expensive cached values (recompute on null).
- Expensive to serve: buyers (checkout: 4-5 pages + CC/tax/address/inventory)
  cost >> grazers. Test at 2-3x expected conversion (e.g. 6-10% if prod is 2%),
  not 100% (that overprovisions 10x).
- Unwanted: misconfigured proxies re-requesting, spiders/scrapers ignoring
  cookies (new session per hit), shopbots polling PS2 availability, Navy-base
  flood updating last-login row -> deadlock on one DB row -> all threads stuck.
  Session creation on deep link without cookie is the Achilles heel.
  Defend: require cookies, URL-rewrite fallback, throttle gateway, block by IP/
  User-Agent anomaly, static landing for bots, robots.txt (only honest obey).
- Malicious: DDoS/botnets, app-layer floods. Session creation is weakest point.
  Need network mitigation (Cisco/Juniper/CheckPoint) + per-host breaker, tuned
  above AJAX rate (15 conn/min rule breaks AJAX apps).

## 5. Blocked Threads — proximate cause of most outages

Interpreter runs, all request threads wait forever. Causes: pool checkout with
infinite wait, sync on domain objects, remote call on request thread, vendor lib.
Java: synchronized in subclass violates Liskov (caller cannot see blocking).
Example: synchronized get() + overridden create() doing seconds-long remote
avail check + undersized inventory -> one stuck create() blocks all getters.
No one designed it in; no one designed it out.
Defend: bounded waits everywhere (wait(timeout), poll(timeout), tryLock),
proven concurrency libs (java.util.concurrent), per-thread copies over sync,
timeouts on pools, isolate dangerous vendor calls in worker pool with rendezvous.

## 6. Attacks of Self-Denial

You DDoS yourself. Marketing email with deep link bypassing CDN, coupon
code going viral, Xbox preorder at fixed time, lock-manager hotspot (one
RepositoryItem write-lock serializes 100s of servers). Shared-nothing or
horizontally scalable shared resource + fallback (pessimistic->optimistic).
For promos: dedicated Bulkhead pool + Fail Fast when dark + static landing

- throttle % + no session IDs in URLs. Keep marketing <-> eng comms open.

## 7. Scaling Effects — O(n^2) bites in prod only

Dev=1 server, QA=1-2, prod=100. Point-to-point chatter = n*(n-1)/2 conns.
Fine for 2, deadly for 100. Replace with UDP broadcast -> multicast ->
pub/sub / queues (simplest that works). Shared resources (lock/cluster mgr)
saturate -> backlog -> listen-queue overflow -> failed txn / stale data.
Cannot test at prod scale (unless Google); must design out. Check prod vs QA
counts and fan-in.

## 8. Unbalanced Capacities — front can always flood back

Fixed hardware over short horizons (weeks to add servers; heroic 36hr re-cable
aside). 3000 front threads -> 75 back threads is not in the ballpark.
Marketing spike (free install day) turns trickle to flood. Cannot build back
to front size (99% idle waste). Must make both resilient: front Breaker +
back Handshaking/throttle + Bulkheads reserving back capacity for other txns.
Test: front sees slow/hung back; back sees 10x worst-case on costliest txn —
must slow + recover, not crash/hang/lie.

## 9. Slow Responses — worse than errors

Slow ties up caller AND callee resources (threads, conns, locks, web-server
sockets+RAM). Causes: overload (no idle handlers), GC thrash (looks like high
CPU), WAN chattiness, TCP stall from undrained buffers. Propagates upward
as gradual cascade. Users hit Reload -> duplicate work, possible deadlock
(serializing on IP fails behind Akamai/corporate proxy; second req may hit
different server). Defend: self-monitored SLA -> Fail Fast (503 with documented
contract) when p99/avg exceeds allowance. Hunt leaks/contention.

## 10. SLA Inversion — promising what dependencies cannot deliver

Frammitz promises 99.99% (4min/mo) but depends on Partner1 (no SLA),
Inventory 99.9%, DNS 99%, Spam 98.5%. Joint P(up) = product of P(up) if naive:
5 externals at 99.9% => 99.5% best case. Service levels only decrease downstream
(2nd Law of Thermodynamics for SLAs). Fix: decouple (degrade gracefully,
Breaker per dependency) + define SLA per-feature with probe, threshold,
success pattern, frequency, locations, formula — never bare "99.99% available."

## 11. Unbounded Result Sets — caller lets callee dictate terms

`SELECT all FROM msg_table` expecting 1k rows gets 10M -> each of 100 instances
locks rows (SELECT FOR UPDATE), OOMs building objects, crashes, rolls back,
next instance repeats (Black Monday). Same via RMI/WS/AJAX traversing
customer->orders, audit trails. Dev datasets too small to show it.
Fix: caller declares limit in protocol (TCP window, search offset/limit).
SQL: TOP/LIMIT/rownum<=N; ORM: limit queries AND associations. Better than
nothing: break after N (still wastes DB). Test with prod-sized data. Only
sensible counts: 0, 1, lots — unless exactly 1, bound it.
