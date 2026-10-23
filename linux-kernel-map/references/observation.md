# Observation

Choose the least invasive way to see kernel behavior. Ordered least invasive first.

## Decision table

| Question type        | Mechanism                          | Config gate                    | Availability check                                  | Invasiveness (1-5) | Fallback    | Notes                             |
| -------------------- | ---------------------------------- | ------------------------------ | --------------------------------------------------- | ------------------ | ----------- | --------------------------------- |
| Already logged       | `dmesg`, `pstore`, `journalctl -k` | `ALWAYS`                       | `dmesg \| tail`                                     | 1                  | tracepoints | No instrumentation; read first    |
| Scheduler latency    | ftrace function tracer             | `CONFIG_FTRACE`                | `test -d /sys/kernel/tracing`                       | 2                  | perf        | Use `function_graph` for duration |
| Block I/O latency    | blktrace / ftrace                  | `CONFIG_BLK_DEV_IO_TRACE`      | `which blktrace`                                    | 2                  | perf        | Per-device tracing                |
| Driver probe failure | dynamic debug                      | `CONFIG_DYNAMIC_DEBUG`         | `grep -c . /sys/kernel/debug/dynamic_debug/control` | 2                  | ftrace      | `dyndbg="..."` on command line    |
| Syscall error rate   | ftrace + filter                    | `CONFIG_FTRACE`                | `test -f /sys/kernel/tracing/set_ftrace_filter`     | 2                  | bpftrace    | Filter by function name           |
| CPU sampling         | perf                               | `CONFIG_PERF_EVENTS`           | `perf --version`                                    | 3                  | ftrace      | System-wide or per-PID            |
| Custom probe         | kprobe / eBPF                      | `CONFIG_KPROBES`, `CONFIG_BPF` | `bpftrace -l 'kprobe:*' \| head`                    | 4                  | crash dump  | Requires root; can destabilize    |
| Post-mortem          | kdump / pstore                     | `CONFIG_CRASH_DUMP`            | `test -f /proc/vmcore`                              | 5                  | none        | Last resort                       |

## Selection rules

1. Start with the least invasive row that answers the question.
2. If the preferred mechanism is disabled, return the next viable row and the check for it.
3. If no instrumentation is needed, say so instead of recommending a probe.
4. Every recommendation states the configuration gate and a one-line availability check that runs on
   a stock kernel.
5. kprobes and eBPF require root and can destabilize the system; recommend them last.
