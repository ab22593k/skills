---
name: Performance Troubleshoot
description: Diagnose and resolve Linux performance bottlenecks in production. Use when the user mentions high CPU usage, memory issues (leaks, OOM, swapping), slow I/O, network latency, container performance, or needs to identify system resource bottlenecks using modern tools like perf, eBPF, and bpftrace. Applies USE method, Little's Law, and structured latency analysis to trace problems across CPU scheduling, memory management, I/O, and networking layers. Includes tuning prescriptions for sysctl, schedulers, NUMA, and storage.
---

# Linux Performance Troubleshooting

This skill provides a structured approach to diagnosing and resolving Linux performance issues in production environments using modern tools and proven methodologies.

## When to Use This Skill

Trigger this skill when the user:

- Reports slow application response times or latency spikes
- Experiences high CPU but low throughput, or unexplained resource contention
- Sees memory exhaustion, OOM kills, or excessive swapping
- Has I/O bottlenecks despite available disk bandwidth
- Notices network drops, retransmits, or throughput degradation
- Troubleshoots container or VM performance issues
- Needs capacity planning or scalability analysis

## Core Diagnostic Framework

### USE Method

For every resource, examine:

1. **Utilization**: How busy is the resource? (%)
2. **Saturation**: Is the resource queued? Queue length
3. **Errors**: Any failures? Retries, timeouts, drops

### Bottleneck Chain

Performance issues rarely occur in isolation. Trace the chain:

```
Application → System call → Kernel → Device driver → Hardware
```

Downstream bottlenecks manifest upstream. High I/O wait may be storage or network.

### Little's Law

For queuing systems: `L = λ × W`

- L = average queue length
- λ = arrival rate (requests/second)
- W = residence time (seconds)

Useful for: validating if observed latency matches measured throughput

## CPU Performance

### What to Measure

| Metric            | Command                       | Target            |
| ----------------- | ----------------------------- | ----------------- |
| Utilization       | `top`, `htop`, `mpstat -u 1`  | < 70% sustained   |
| Load average      | `uptime`, `cat /proc/loadavg` | < number of cores |
| Context switches  | `vmstat 1`, `pidstat -w 1`    | < 10K/sec total   |
| Run queue length  | `vmstat 1` (r column)         | < number of cores |
| Scheduler latency | `schedstat` per process       | < 10ms            |

### Diagnostic Steps

1. **Identify if CPU-bound**: High %CPU in top, low I/O wait
2. **Check load average**: Compare to core count (4-core = ~4.0 load)
3. **Analyze context switches**: High cswtch with low %CPU indicates scheduling overhead
4. **Per-process analysis**: `pidstat -p PID 1` for specific process CPU time
5. **Scheduler analysis**: Check /proc/PID/sched for scheduler latency

### CPU Flamegraphs

Generate with:

```bash
perf record -F 99 -a -g -- sleep 30
perf script | ./flamegraph.pl > cpu.svg
```

Look for: hot code paths consuming CPU cycles

### Frequency Scaling Issues

Check with: `turbostat --interval 100 --num_iterations 5`

Look for: CPU throttling (P0 → P-states), thermal throttling

### CPU Tuning Prescriptions

```bash
# Disable hyperthreading if causing contention
echo 1 > /sys/devices/system/cpu/cpuN/online  # disable sibling

# CPU isolation (disable scheduler balancing)
echo 1 > /sys/kernel/debug/sched_autogroup_enabled  # or use isolcpus=

# Real-time priority
chrt -f -p 99 $PID  # FIFO at priority 99
```

## Memory Performance

### What to Measure

| Metric      | Command                        | Target           |
| ----------- | ------------------------------ | ---------------- | ------------------ |
| Utilization | `free -h`, `cat /proc/meminfo` | < 80% used       |
| Available   | `free -h`                      | > 20% available  |
| Swap usage  | `swapon -s`, `vmstat 1`        | Minimal (near 0) |
| Page faults | `vmstat 1` (fault column)      | Varies by app    |
| OOM events  | `dmesg                         | grep -i oom`     | Zero in production |

### Memory Leak Detection

1. **Baseline**: Note RSS baseline for process
2. **Monitor**: `pmap -x PID` every 5 minutes
3. **Observe**: Growing RSS without return indicates leak
4. **Deep dive**: `valgrind --leak-check=full --show-leak-kinds=all ./app`

### NUMA Issues

Check with: `numactl -- hardware`

Look for: Process memory on remote nodes (interleaved = bad)

### Swap Analysis

```bash
# What's using swap?
for file in /proc/*/status; do grep VmSwap "$file"; done | sort -nk2

# Why swapping?
# High si/so in vmstat indicates memory pressure
```

### OOM Diagnostics

Check: `dmesg | grep -i "out of memory" | tail -20`

Look for: Which process was killed, why it was selected

### Memory Tuning Prescriptions

```bash
# Disable transparent huge pages (if causing latency variance)
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag

# vm.swappiness (lower = less swapping)
sysctl -w vm.swappiness=10

# Drop caches (carefully)
sync; echo 3 > /proc/sys/vm/drop_caches

# NUMA balancing
echo 0 > /proc/sys/kernel/numa_balancing  # disable if causing issues
```

## I/O Performance

### What to Measure

| Metric      | Command                      | Target           |
| ----------- | ---------------------------- | ---------------- |
| Utilization | `iostat -x 1` (%util column) | < 70%            |
| Queue depth | `iostat -x 1` (avgqu-sz)     | < 2              |
| Wait time   | `iostat -x 1` (await column) | < 10ms           |
| IOPS        | `iostat -x 1`                | Device-dependent |
| Throughput  | `iostat -x 1` (rB/s, wB/s)   | Device-dependent |

### I/O Wait Analysis

High %iowait in top indicates:

1. Storage is slow (HDD vs SSD)
2. Queue is saturated
3. Application making synchronous I/O

### Block Layer Tracing

```bash
# I/O request latency Distribution
biolatency

# Per-process I/O
iotop  # or pidstat -d 1

# Block layer events
blktrace -d /dev/sda  # then analyze with blkparse
```

### io_uring Analysis

For io_uring applications:

```bash
# Trace io_uring operations
bpftrace -e 'k:io_uring_* { }'
```

### Storage Tuning Prescriptions

```bash
# I/O scheduler (NVMe: none/mq-deadline, SSD: none, HDD: bfq)
echo none > /sys/block/sda/queue/scheduler

# Queue depth
echo 256 > /sys/block/sda/queue/nr_requests

# Read-ahead
echo 4096 > /sys/block/sda/queue/read_ahead_kb

# Disable barrier for data-only filesystems
mount -o nobarrier /dev/sda1 /mnt
```

## Network Performance

### What to Measure

| Metric        | Command                | Target                |
| ------------- | ---------------------- | --------------------- |
| Throughput    | `iftop`, `nethogs`     | < 80% link capacity   |
| Drops         | `netstat -su`          | Zero                  |
| Retransmits   | `netstat -s`           | Minimal               |
| Connections   | `ss -s`, `netstat -an` | Connection table size |
| Socket buffer | `ss -mem`              | No drops              |

### TCP Analysis

```bash
# Connection states
ss -tan state established

# Receive buffer errors
netstat -s | grep -i "buffer"

# TCP retransmits
netstat -s | grep -i retrans

# Socket memory
ss -mem
```

### Network Latency

```bash
# Path latency
mtr target.host

# TCP connection latency
# Time from SYN to SYN-ACK
```

### Network Tuning Prescriptions

```bash
# Increase socket buffers
sysctl -w net.core.rmem_max=16777216
sysctl -w net.core.wmem_max=16777216
sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216"
sysctl -w net.ipv4.tcp_wmem="4096 87380 16777216"

# Enable TCP timestamps
sysctl -w net.ipv4.tcp_timestamps=1

# BBR congestion control
sysctl -w net.ipv4.tcp_congestion_control=bbr

# Connection tracking table size
sysctl -w net.netfilter.nf_conntrack_max=1048576
```

## Latency Tracing

### eBPF for Latency Analysis

Use bpftrace for low-overhead per-request latency:

```bash
# I/O latency
bpftrace -e 'kprobe:blk_mq_start_request { @[comm] = elapsed(); }'

# Network latency
bpftrace -e 'kprobe:tcp_sendmsg { @[comm] = elapsed(); }'

# Request latency (application-level)
# Requires USDT probes in application
bpftrace -e 'usdt:app:request_start { @start = nsecs(); }'
bpftrace -e 'usdt:app:request_end { @latency = nsecs() - @start; }'
```

### Flamegraphs for Latency

CPU flamegraph shows where time is spent:

```bash
perf record -F 99 -p $PID -g -- sleep 30
perf script | flamegraph.pl > latency.svg
```

### Scheduler Latency

Per-process latency analysis:

```bash
# Wait time vs run time
cat /proc/PID/sched  | grep -E "(se.|sum.)

# Scheduler statistics
schedstat $PID
```

### Latency Tuning

```bash
# Reduce scheduler jitter
echo 1 > /proc/sys/kernel/sched_migration_cost_ns

# Increase scheduler granularity
sysctl -w kernel.sched_min_granularity_ns=10000000
```

## Container and Virtualization

### Container Performance

```bash
# Container CPU limit
cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us
cat /sys/fs/cgroup/cpu/cpu.cfs_period_us

# Container memory
cat /sys/fs/cgroup/memory/memory.usage_in_bytes

# Container I/O
cat /sys/fs/cgroup/blkio/blkio.throttle.io_service_bytes
```

### VM Performance

```bash
# KVM hypervisor
virsh domstats VM_NAME --cpu

# virtio stats
cat /sys/kernel/debug/virtio-net/*
```

### Container Tuning

```bash
# CPU period/quota
echo 100000 > /sys/fs/cgroup/cpu/cpu.cfs_period_us
echo 50000 > /sys/fs/cgroup/cpu/cpu.cfs_quota_us

# Memory limit
echo $((4*1024*1024*1024)) > /sys/fs/cgroup/memory/memory.limit_in_bytes
```

## Diagnostic Workflow

### Step 1: Identify the Symptom

1. User reports: slow response, high resource usage, crashes
2. Confirm: What resource? CPU, memory, I/O, network?
3. Context: Load pattern, recent changes, baseline

### Step 2: Measure with Modern Tools

1. Always use perf, eBPF, bpftrace first
2. Fall back to vmstat, iostat, netstat
3. Use top/htop only for overview

### Step 3: Apply USE Method

1. Check utilization
2. Check saturation (queue lengths)
3. Check for errors

### Step 4: Trace the Bottleneck Chain

1. Application → System call → Kernel → Device → Hardware
2. Identify where slowdown occurs
3. Address root cause, not symptoms

### Step 5: Validate Fix

1. Rerun workload
2. Confirm improvement
3. Document change

## Quick Reference Commands

### CPU

```bash
# Overview
htop
mpstat -u 1

# Per-process
pidstat -p $PID 1
perf record -F 99 -a -g -- sleep 10; perf report

# Flamegraph
git clone https://github.com/brendangregg/FlameGraph
perf record -F 99 -a -g -- sleep 30
perf script | ./flamegraph.pl > cpu.svg
```

### Memory

```bash
# Overview
free -h
cat /proc/meminfo

# Per-process
pmap -x $PID
cat /proc/$PID/status | grep -i vm

# Leaks
valgrind --leak-check=full ./app

# OOM
dmesg | grep -i oom
```

### I/O

```bash
# Overview
iostat -x 1

# Per-process
iotop
pidstat -d 1

# Deep
bpftrace -e 'k:blk_* { }'
```

### Network

```bash
# Overview
iftop
nethogs

# TCP stats
netstat -s
ss -tan

# Drops
ip -s link
```

## Case Study Patterns

Based on common production scenarios:

### Pattern 1: High CPU, Low Throughput

Symptoms: 100% CPU, low requests/sec
Diagnostic: Check for context switching, scheduler latency
Root cause: Often lock contention, bad NUMA placement
Fix: Pin CPU, enable nohz, adjust scheduler

### Pattern 2: Latency Spike Under Load

Symptoms: p50 fine, p99 spiking
Diagnostic: Use eBPF to trace request latency
Root cause: GC pause, I/O wait, lock contention
Fix: Enable profiling, identify outlier

### Pattern 3: Memory Growing Until OOM

Symptoms: RSS increasing, then killed
Diagnostic: Monitor RSS over time, check for leaks
Root cause: Memory leak or insufficient limit
Fix: Fix leak or adjust cgroup limits

### Pattern 4: I/O Wait High, Low IOPS

Symptoms: High iowait % in top, slow disk
Diagnostic: Check queue depth, scheduler
Root cause: HDD with wrong scheduler, queue saturation
Fix: Change scheduler, increase queue depth

### Pattern 5: Network Retransmits

Symptoms: Slow throughput, retransmit counters up
Diagnostic: Check NIC errors, congestion
Root cause: Duplex mismatch, network congestion
Fix: Fix duplex, enable BBR, check NIC stats
