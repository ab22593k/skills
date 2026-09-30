# General Design Issues — Survive the Data Center

Source: Release It! Ch.11-14. Dev/QA topology lies; prod has multihoming,
firewalls, LBs, clusters, least-privilege, and tired admins. Design for them
now or debug them at 3am.

## 11. Networking

### Multihomed servers (prod has 4 NICs, dev has 1)
Prod host: 2 prod nets (HA to different switches) + backup net (bursty, isolated
VLAN) + admin net (SSH only, highly secured). Host has multiple names/IPs;
getLocalHost() returns arbitrary one. Default bind-all-interfaces is wrong:
prod port opens on backup/admin, admin opens on prod.
Fix: configurable bind address per listener. Java: `new ServerSocket(port,
backlog, InetAddress.getByName(config))` — only 1 of 4 ctors binds specifically.
Bonding/teaming (shared IP over 2 NICs) needs switch config or routing loops.

### Routing
App with front VLAN (web) + back VLAN (DB) must choose interface per dest.
Distant services (spam cannon via VPN, not Internet) need explicit routes.
Keep spreadsheet/DB: dest name, address, desired route, firewall rule. Needed
for firewall tickets anyway. Wrong route = outage or customer-data exposure.

### Virtual IPs (two flavors: migrating address vs service address)
Cluster managers (Veritas, HP ServiceGuard, MS Cluster) ensure package runs
once: shutdown on A, mount FS, start on B, migrate VIP + gratuitous ARP.
Clients use VIP DNS only, never node hostnames. In-memory state lost
(uncommitted txns); Oracle drivers may re-query but never re-update/insert/
proc — app must catch SQLException on failover and bounded-retry (see Breaker).
LB VIPs multiplex many services on few NICs; pairs fail over similarly.
Expect next packet to hit different NIC after migration.

## 12. Security (arch x ops intersection only)

### Least privilege
Never run as root/Administrator. Only need: bind <1024 (avoid via LB on any
port; Apache drops privs after opening 80). Each app own user (apache !=
websphere). Root vuln = reformat whole cluster. Windows-GUI-as-service that
must stay logged in as Admin = not data-center-ready.

### Configured passwords
Must live in files (no interactive entry). Minimum: separate file outside install
dir (install zips get sent to dev; restores overwrite), owner-read-only (or
root-owned if app drops privs after reading), no core dumps (UNIX core / Win
BSOD dump contains passwords in memory), vault (encrypted file -> single key
to protect) + Tripwire/Open Source Tripwire for perm monitoring. Link to change
control; never in source control readable by all.

## 13. Availability (want divorced from cost = fantasy)

### Gathering: frame as money
"How available?" -> "100%" or "five nines" is unpriced want. Price it: 98%
=864min/mo downtime. At $1500/hr peak, worst loss $21.6k/mo. 99.99% =4min
($108). If lifecycle cost to add 9s is $98.7k for +$1.29M saved over 5yr, do it.
Each 9 costs ~10x to build, ~2x/yr to operate.

### Documenting: vague SLA = future fight
Not "system 99.9%." Define per-feature/process (locator vs reservation vs
loyalty — different value, different deps; beware SLA Inversion: can't beat
worst dep). For each: synthetic probe device(s), frequency, locations, max
latency per step, success/failure patterns, storage, formula (time vs samples).
Paper is thin shield but focuses on data not blame.

### Load balancing
- DNS round-robin (layer 7 at resolve): N IPs for one name. Cheap, but servers
  routable (attack surface), no health awareness (sends to toast), uneven (conns
  != load), Java caches first IP forever (kills balancing), Apache rewrite
  leaks node names (bookmarked). Only for small sites, never for server-to-server.
- Reverse proxy (Squid, Apache mod_proxy, Akamai basic): one IP, fan-out per
  request. Configure app to generate foreign hostnames; log X-Forwarded-For
  (spoofable when you need it most). Can cache static (helps iff web is constraint).
  Squid/Apache don't health-check (send to dead -> timeout -> error). Adding LB
  in front of proxies = time to upgrade.
- Hardware (Cisco CSS, F5 BigIP, L4-L7): health polls, remove dead, any TCP
  protocol (search clusters), site failover. SSL choice: terminate on LB (easy certs,
  keep L7 services, but LB becomes CPU bottleneck, against Moore's law) vs
  passthrough to webs (smart switch only, lose L7). $$$$ ($50k pair low, 6 figs high);
  Apache mod_proxy_balancer 2.2 is credible cheaper start (proportional weights).
### Clustering
Farm (LB, no inter-node chatter, near-linear) vs cluster (nodes collaborate,
heartbeat + state sync overhead, sublinear, size limit). Active/active = scale;
active/passive = redundancy only. Built-in (WebSphere/WebLogic/Oracle/MSSQL
with master-control weak point) vs exoskeleton (Veritas/MSCS running unaware
app as child + quorum disk + VIP + FS takeover). Exoskeleton = marvelous kludge:
adds failover to legacy, finicky config, small failover glitches. Band-aid until
app clusters natively.

## 14. Administration (make admins allies)

Dev+users love change; admins see risk + work + new unknowns. Assume positive
intent both ways. Easy-to-admin = uptime + help; hard = neglect + sabotage.

### Does QA match prod? (the gimme that costs hours)
Config diff is easy to ask, expensive to answer (hostnames always differ; HW-
specific patch bundles). Real culprit is usually topology (graph of nodes+arcs):
shared hosts in QA vs separate in prod (hidden dir-sync assumption; last-minute
rsync doesn't count), 1 instance in QA vs farm in prod (point-to-point vs
multicast invalidation), missing firewall/LB in QA (rules discovered 95% done =
pain). Fix: VMware for separation/multiplicity on shared HW (+ snapshots for
deploy tests), buy same-vendor LB/firewall for QA (not top model), practice with
firewalls from day one (rules = integration points = prod config params).

### Configuration files
Failure: plumbing (Spring beans.xml 5000 lines) mixed with env (1 password) —
admin edits minefield, breaks associations wearing guts outside. Fix: separate
files, prod config outside install dir (upgrades/backups/copies overwrite),
split shared vs per-host props, verify sync periodically (trust but verify),
name by function not type (`authenticationServer` not `hostname`), GUI editors
(WebLogic/WebSphere/JBoss) still mix dirs; .NET+VS slightly better. Version-
control configs (secure repo, linked to change reason, auto-deploy, audit drift;
or BMC/BladeLogic/Opsware). Treat props as UI: prevent unforced errors.

### Startup / shutdown
Dev sees failure; prod midnight reboot needs self-announcement (log + monitor).
Startup: ordered, verified, pre-fill pools (Fail Fast self-test: no DB = failed
state, not silent), bind but don't accept until master switch ready (store not
open until staffed). Stay queryable when failed (interrogate, don't exit).
Shutdown: drain — stop accepting new, finish in-flight with timeout, then exit
(don't lock doors with customers inside).

### Admin interfaces
Spiffy Java GUI demos well, operates terribly: unscriptable clicks x N servers,
minutes per server eats change window (6-server OMS shutdown never done right),
X/HTTP over SSH tunnels painful -> kill -9 instead. Best: CLI (scriptable
scaffolding), acceptable: pure HTML (Perl/Ruby HTTP libs can drive). Provide
JMX/scriptable hooks; admins will bless your name.
