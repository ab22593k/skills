# Triage

Decode a panic, oops, WARNING, soft lockup, or hung-task report into a culprit subsystem, the
trustworthy frames, and the next diagnostic step. Address layout is never presented.

## Classification

| Kind          | Signature                              | First question                                              |
| ------------- | -------------------------------------- | ----------------------------------------------------------- |
| `oops`        | `Oops:`, `RIP:`/`PC:`                  | Which function faulted and on which access?                 |
| `panic`       | `Kernel panic - not syncing`           | Did an oops escalate, or did `panic()` get called directly? |
| `warning`     | `WARNING: CPU:` with stack             | Which condition fired and is it recoverable?                |
| `soft-lockup` | `softlockup: hung tasks`               | Which CPU and which task are stuck?                         |
| `hung-task`   | `INFO: task ... blocked for more than` | What is the task waiting on?                                |
| `kasan`       | `KASAN:`                               | Out-of-bounds or use-after-free; which access?              |
| `ubsan`       | `UBSAN:`                               | Undefined behavior; which operation?                        |
| `lockdep`     | `WARNING: .../lockdep`                 | Lock ordering violation                                     |

## Symbolization

Use the kernel's own scripts; do not reimplement KASLR-aware resolution.

```bash
# From a splat file, with vmlinux and a modules directory:
./scripts/decode_stacktrace.sh /path/to/vmlinux auto /path/to/modules < splat.txt

# Single symbol:
./scripts/faddr2line /path/to/vmlinux func+0x12/0x34
```

`scripts/symbolize.py` wraps both and names the missing artifact when one is absent.

Rules:

- If `vmlinux`, `System.map`, or the module's `.ko` is missing, name it and mark the frame
  `reliable: no`. Never map an unresolved address to a plausible-looking function.
- A `?` in a frame means unresolved; keep it unresolved.
- Tainted kernels or out-of-tree modules block upstream attribution until the module's own symbols
  are supplied.

## Answer shape (triage)

- `Report kind:` one of the kinds above.
- `Kernel:` version from the splat, plus taint flags, or `unknown`.
- `Faulting frame:` frame index and `path:symbol`, or `unresolved`.
- `Call chain:` table `frame | symbol | artifact | reliable | role`.
- `Artifacts used:` and `Missing artifacts:` naming the exact file.
- `Subsystem:` a map area id, or `unknown`.
- `Next evidence:` the specific check that would confirm or clear the hypothesis.

## Faulting frame versus call chain

- The faulting frame is where the bad access happened. The call chain shows how execution got there.
- Attribute the fault to the faulting frame, not to a caller.
- `?` or unresolved frames are `reliable: no` and cannot be the sole basis for a subsystem claim.

## Taint

- Read the `Tainted:` line from the splat and `/proc/sys/kernel/tainted`.
- Flags include out-of-tree (`P`/`O`), forced module (`F`), staging driver (`S`), and others.
- A tainted trace is not attributable to upstream code without the module's own symbols.

## Subsystem mapping

Map the resolved symbol to an area in `references/map.json` and read that area's entry symbols and
roots. If the symbol is not in the map, state `unknown` and give the search that would confirm it.

## Next evidence

Name one concrete check: a kprobe on the faulting function, a tracepoint, a `pr_debug`/dynamic
debug toggle, a crash dump capture, or a reproduction under `KASAN`. Do not recommend a probe when
`dmesg` or the splat already answers the question.

## Forbidden

- Address layout, `System.map` contents, or memory maps.
- Fabricated frames or symbols.
- Upstream attribution for tainted traces without module symbols.
- Presenting an unresolved address as a function name.
