# Data Patterns for Low Latency

Optimizing data storage and access is often the highest-leverage activity for reducing latency. This reference covers strategies for placing, copying, and slicing data.

## 1. Colocation
Bringing data closer to computation to minimize signal propagation delay.

### Internode (Distributed Systems)
- **Geographical**: Host data in the same region as the user.
- **Edge Computing**:
    - **Near Edge**: Points of Presence (PoPs) in major metro areas (e.g., Cloudflare PoPs).
    - **Far Edge**: Moving compute to user devices, home Wi-Fi, or IoT gateways to eliminate last-mile latency.
- **CDNs**: Use programmable CDNs (e.g., Cloudflare Workers) to serve dynamic content from the edge.

### Intranode (Single Machine)
- **Network Stack**:
  - **TCP_NODELAY**: Disable **Nagle's Algorithm** to stop the OS from batching small packets, which introduces queuing delay.
  - **Kernel-bypass**: Use DPDK or XDP to process packets in userspace, bypassing kernel interrupts.
  - **Interrupt Affinity**: Pin NIC interrupts to the same CPU core as the application thread to preserve cache locality.
- **Memory Topology (NUMA)**: Ensure threads access local DRAM. Remote NUMA node access is 2x+ slower.

## 2. Replication
Maintaining multiple copies of data for availability and lower read latency.

### Replication Strategies
- **Single-Leader**: Simple, but all writes must go to one node (potentially far away).
- **Multi-Leader**: Writes go to the nearest leader (low write latency), but requires resolution of concurrent updates.
- **Leaderless**: Uses quorums (W + R > N). Fastest writes as no single node is a bottleneck.

### Consistency Models
- **Strong Consistency**: High latency due to cross-region acks.
- **Eventual Consistency**: Lowest latency; replicas converge asynchronously.
- **Read-your-writes**: Guarantees a user sees their own updates immediately, even with eventual consistency elsewhere.

### State Machine Replication
- Uses consensus algorithms (Raft, Paxos, VSR) to keep replicas in sync.
- **Trade-off**: Trades latency for fault tolerance (requires majority quorum).

## 3. Partitioning (Sharding)
Slicing data into smaller, independent chunks to reduce contention and increase concurrency.

### Physical Strategies
- **Horizontal (Sharding)**: Split rows into different tables/nodes (e.g., Users 1-1000 on Node A). Best for OLTP.
- **Vertical**: Split columns into different storage (e.g., separating "Blob" columns from metadata). Best for OLAP/Analytics.
- **Hybrid**: Combine both (e.g., vertical partition first, then horizontally shard the columns).

### Logical Strategies
- **Functional**: Separate by business domain (e.g., Catalog vs. Orders).
- **Geographical**: Partition by user location (e.g., EU users in Frankfurt).
- **Time-based**: Partition by time (e.g., Logs per day). Useful for time-series.

### Request Routing
- **Direct**: Client knows topology and calls partition directly (Fastest, high coupling).
- **Proxy**: Client calls proxy, which routes to partition (Extra hop, decoupled).
- **Forward**: Client calls any node, node forwards if it doesn't own the data (P2P).

### Mitigating Imbalance
- **Hot Partitions**: Caused by poor key choice or "celebrity" records. Use better hashing or over-partitioning.
- **Skewed Workloads**: Temporal skew (Black Friday). Requires overprovisioning or dynamic splitting.

## 4. Caching
Temporary storage of expensive-to-fetch data.

### Strategies
- **Cache-Aside**: App reads cache; on miss, app reads DB and updates cache. (Robust, but stale data risk).
- **Read-Through**: App reads cache; on miss, cache reads DB. (Simplifies app, transparent).
- **Write-Through**: Write to cache; cache writes to DB synchronously. (Safe, high write latency).
- **Write-Behind**: Write to cache; cache writes to DB asynchronously. (Fastest writes, risk of data loss).

### Replacement Policies
- **LRU (Least Recently Used)**: Good for temporal locality.
- **LFU (Least Frequently Used)**: Good for stable popularity distributions.
- **FIFO/SIEVE**: Low overhead, often outperforms LRU in practice.

### Advanced
- **Materialized Views**: Precomputed query results stored as tables. incremental updates hide complex query latency.
- **Memoization**: Caching function results (e.g., in-memory map of input->output).
