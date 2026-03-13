# Latency Principles

Based on "Latency: Reduce delay in software systems" by Pekka Enberg.

## 1. Definition
Latency is the time delay between a **cause** and its **observed effect**.
- **Service Time**: Time spent actively processing a request.
- **Wait Time**: Time a request spends in a queue or network.
- **Response Time**: The sum of service time and wait time.

### Latency vs. Bandwidth vs. Throughput
- **Latency**: Time for a single request to travel and receive a response. You are "stuck" with bad latency.
- **Bandwidth**: The maximum possible data transmission rate (the "width" of the pipe).
- **Throughput**: The actual amount of data successfully delivered over a given time.
- **Relationship**: You can increase throughput by adding more pipes (bandwidth) or by pipelining tasks, but this can actually *increase* the latency of an individual task (the "laundry" pipelining example).

## 2. Impact on User Experience (UX)

User experience is the primary motivator for low-latency systems. 
- **Immediate (no delay perceived)**: < 100 ms.
- **Instant (feels fast)**: < 1 s.
- **Slow (delay perceived as slow)**: > 10 s. (Need feedback mechanisms like progress bars).
- **Economic Impact**: Google reports 1s delay reduces engagement by 20%. Akamai reports 100ms increase drops conversion by 7%.
- **Real-time Systems**:
    - **Hard Real-time**: Missing a deadline is a failure (e.g., heart pacemaker, car sensors).
    - **Soft Real-time**: Missing a deadline is a quality issue but not catastrophic (e.g., video streaming).

## 3. Laws of Latency

### Little's Law
Connects latency, throughput, and concurrency.
`Concurrency (L) = Throughput (λ) * Average Latency (W)`

- **Implication**: To increase throughput without increasing latency, you must increase concurrency (parallelism). If concurrency is fixed, increasing throughput increases latency (queuing).
- **Caveat**: Assumes independent mean throughput/latency. Real systems often see latency rise with throughput due to contention.

### Amdahl's Law
Quantifies theoretical speedup from parallelization.
`Speedup(N) = 1 / ((1 - P) + (P / N))`
- `P`: Parallel portion of the program.
- `N`: Number of processors.
- **Implication**: Speedup is limited by the serial portion (`1 - P`). Diminishing returns kick in quickly.

## 3. Latency Distribution
Average latency hides the truth.
- **Tail Latency**: High percentiles (p95, p99, p99.9, Max).
- **The Tail at Scale**: In systems with high fanout (parallel sub-requests), the probability of a user experiencing tail latency increases dramatically.
  - Probability of request > T = `1 - (1 - p)^N` where `p` is probability of single node > T, and `N` is fanout.

## 4. Sources of Latency
- **Physics**: Speed of light (distance between components).
- **Hardware**:
  - **CPU Caches**: L1 (1ns) vs DRAM (100ns). Cache misses cause variance.
  - **SMT (Hyperthreading)**: Shared resources can cause contention. Disable for ultra-low latency.
  - **Power Saving**: Frequency scaling (CPU sleeping) adds wakeup latency.
- **Virtualization**:
  - **Hypervisor Overhead**: Scheduling, exit/entry costs.
  - **Noisy Neighbors**: Resource contention in cloud.
- **Operating System**:
  - **Context Switching**: Saving/restoring thread state (~µs).
  - **Interrupts**: CPU stops to handle hardware events.
  - **Scheduler**: Queuing delays when waking up threads.
- **Runtimes (Managed)**:
  - **GC**: Stop-the-world pauses.
  - **JIT**: Compilation during execution causes spikes.

## 5. Compounding Latency
- **Serial Compounding**: Latency adds up (`L_total = L1 + L2 + ...`). Optimization requires improving individual steps.
- **Parallel Compounding**: Latency is determined by the slowest path (`L_total = max(L1, L2, ...)`). High fanout increases tail latency risk.

## 6. Trade-offs
- **Latency vs Throughput**: Batching/Pipelining improves throughput but increases per-item latency.
- **Latency vs Energy**: Polling/Busy-waiting lowers latency but wastes energy. Sleeping saves energy but adds wakeup latency.

## 7. Measurement & Visualization

Average latency is a lie. To understand your system, you must visualize the distribution.

### Histograms
- **What**: Bins of latency values showing frequency.
- **Benefit**: Reveals the "mode" (most common experience) and the spread of outliers.
- **Limitation**: Hard to read specific high-percentile values (p99.9).

### HDR (High Dynamic Range) Histograms
- **What**: Plots latency against percentiles on a logarithmic scale.
- **Benefit**: Compresses the p50-p90 range to focus on the "tail" (p99, p99.9, p99.99).
- **Tool**: `scripts/visualize_latency.py` uses the `HdrHistogram` library for this.

### eCDF (Empirical Cumulative Distribution Function)
- **What**: A curve where the Y-axis is the probability (0 to 1) and X-axis is latency.
- **Benefit**: Directly answers "What is the probability that a request finishes in < X ms?". It is the most robust way to check SLA compliance.

### Coordinated Omission
- **The Trap**: Benchmark tools often wait for one request to finish before sending the next. If the system stalls, the tool stalls too, omitting the samples that would have occurred during the stall.
- **The Fix**: Use **Fixed-Interval Benchmarking** (e.g., `scripts/ping_collector.py`). Send requests at a steady rate regardless of when previous ones finish.
