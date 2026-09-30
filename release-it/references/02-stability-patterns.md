# Stability Patterns — 8 Crackstoppers

Source: Release It! Ch.5. Apply wisely, not by count. Goal: contain damage,
preserve partial function. Explain why, not just how.

## 1. Use Timeouts — stop waiting for answers that may never come

Networks are fallible forever. Blocked-forever is never acceptable.
- Cover: socket connect + read (setSoTimeout), pool checkout, wait()/poll()/
  offer()/tryLock() with timeout arg, HTTP conn + read separately.
- Organize long ops into Gateway/Template (e.g. Spring JdbcTemplate,
  QueryObject): acquire -> execute -> map -> release with timeouts in one place.
  Easier to add Breaker later.
- Retries: immediate retry usually re-hits same fault (non-transient in DC)
  and pushes you past caller's timeout. Prefer queue-and-slow-retry later
  (store-and-forward like mail) and return fast (success/fail/queued).
  For web SOA, "fast enough" is <250ms.
- Pairs with: Breaker (tabulates timeouts to trip), Fail Fast (inbound side
  of same coin; Timeouts = outbound protection).
Remember: apply to Integration Points, Blocked Threads, Slow Responses.
Delayed retry, not immediate.

## 2. Circuit Breaker — don't do it if it hurts

Electrical fuse that resets. States: Closed (pass through, count failures)
-> Open (fail immediately with distinct exception, no attempt) after threshold
-> Half-Open (single trial after sleep) -> Closed on success, Open on fail.
Use Leaky Bucket for counting.
- Track failure types separately (timeout vs refused may have different thresholds).
- Business decision: what to do when open? Accept order without availability/
  CC check? Involve stakeholders upfront — breaker forces the conversation.
- Ops: log every transition, expose current state for query/monitor, chart
  transition frequency (leading indicator), allow manual trip/reset via JMX/admin.
Protects: integration points, cascades, unbalanced capacities, slow responses.

## 3. Bulkheads — partition to save part of the ship

Ship compartments; one flood does not sink all.
- Granularities: thread-group per function (incl. reserved admin pool so hung
  app still answers diagnostics/shutdown), CPU binding (contain runaway to
  one CPU, less cache bashing), server farm per client (Foo pool vs Bar pool
  for shared service Baz), farm per criticality (check-in vs flight-status).
- Trade-off: less efficient when healthy (each partition needs own reserve;
  shared pool tolerates skew). Regain efficiency with virtualization (VMs per
  client, live-migrate in seconds, shift capacity administratively).
- In SOA, every shared service is a company-wide SPOF without bulkheads.
Decide granularity by business impact x technical feasibility. Test for aggregate
throughput, not single-server latency.

## 4. Steady State — no fiddling, no sludge

Every touch is an unforced-error chance. System must run a full deploy cycle
with no logins. For every accumulator, build a recycler (calculus bucket).
- Data purging: never makes release 1.0 but fuse is lit at launch. Symptoms:
  rising I/O at constant load, latency creep. Purge in app logic (ORM-safe),
  not just DBA scripts. Measure shortest fuse first (highest-volume tables).
- Logs: rotate by size (RollingFileAppender / FileHandler limit+count /
  logrotate), copy off prod for analysis, never fill prod FS. Full FS ->
  IOException -> reentrant loggers multiply exceptions -> eat CPUs+RAM -> crash.
  SOX: web logs do not prove financial controls; involve compliance early.
- In-memory cache: ask (a) is key space finite? (b) do items change? If
  unbounded/changing, enforce max + invalidation (TTL flush usually beats
  LRU). Java: SoftReference payloads so GC reclaims before OOM. Cache flush
  itself needs rate-limit or it becomes self-denial.
Helps avoid Slow Responses + builds ops discipline.

## 5. Fail Fast — slow failure is the worst waste

DMV line then "wrong form, go back." If you know you will fail, say so now
so caller reclaims capacity.
- At txn start (mise en place): checkout needed conns, check breaker states,
  start DB txn. If any missing, fail immediately.
- Validate input in servlet/controller before acquiring heavy resources, but
  keep domain invariants in domain/facade (don't leak encapsulation).
- Distinguish system failure (no resources) from app failure (bad input) in
  error contract — or upstream Breakers trip on user typos + Reloads.
- Preallocate (memory, disk, fonts/images/masks) and check existence upfront;
  black-image print story: minutes of render wasted for missing asset that
  could have been checked in ms.
With Timeouts, averts cascades; preserves capacity under partial failure.

## 6. Handshaking — let server throttle demand

RS-232 / modem / TCP handshake at low layers; almost nothing at app layer.
HTTP 503 exists but most clients treat non-200/302/403 as fatal. CORBA/DCOM/
RMI equally bad.
- Workarounds: LB health-check page returning 503/error HTML when busy;
  explicit health-check query before real call (doubles conns — only if
  health << real cost); build version+ready signaling into custom socket
  protocols from day one.
- Best where unbalanced capacities cause slow responses and caller can back off.
- Breaker is stopgap when callee cannot handshake (infer health from results
  instead of asking).
Underused; build into any custom protocol.

## 7. Test Harness — be devious, not just correct

Integration envs only test in-spec behavior + lock whole enterprise to one
version at a time (unitary integration test). Need out-of-spec simulation per
integration point, runnable anywhere in isolation.
- Socket harness modes by port: refuse, hang in listen queue, SYN/ACK then
  silence, RESET storm, full window never drained, conn then no bytes, packet
  loss/retransmit, headers but no body, 1 byte/30s, HTML instead of XML,
  MB instead of KB, auth always fails, /dev/random reply.
- One killer server, many ports, request logging (victim may die silently).
  Framework with pluggable app-protocol perversions. Doubles as functional
  isolation stub.
- Complement, not replace: unit + acceptance + FIT still needed. Harness owns
  nonfunctional cruelty under load (JMeter/Marathon + all switches flipped).
Difference from mocks: mocks obey interface in-process; harness as separate
server may violate any OSI layer.

## 8. Decoupling Middleware — integrate + decouple

Plumbing between islands that were never meant to meet. Sync (RPC/HTTP/
RMI/CORBA/DCOM) requires both ends up simultaneously — amplifies shocks,
enables cascades. Async (MQ, pub/sub, SMTP/SMS, tuplespaces like JavaSpaces)
decouples in space + time — cannot cascade via blocking.
Spectrum: in-process call -> IPC (shm/pipe) -> RPC -> message-oriented ->
tuplespace (least coupled).
- Sync wins on mental simplicity (CC auth: proceed vs back-to-payment?).
  Async forces hard design: exception queues, late replies, callbacks,
  business risk calls (what if auth ultimately fails?).
- Cost: products expensive, style change is architectural (RPC->tuplespace
  rewrites thinking at all layers), often decided enterprise-wide before you.
Decide at last responsible moment, but know switching cost is near-irreversible.
Total decoupling avoids most integration/cascade/slow/blocked pain and
eases independent change.
