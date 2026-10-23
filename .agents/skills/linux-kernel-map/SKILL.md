---
name: linux-kernel-map
description: Navigate, diagnose, and extend the Linux kernel source tree. Use whenever a user asks where a kernel behavior lives, traces a syscall or symptom to its implementation, decodes a panic/oops/WARNING/soft lockup/hung task, chooses an observation method (ftrace, perf, bpftrace), authors or modifies a kernel module or driver (character, platform, PCI, USB) with interrupts, DMA, and power management, or audits a driver/ioctl/sysfs/syscall path for security with a STRIDE worksheet. Also use for version and fork honesty, including moved files, vendor/Android/RT trees, out-of-tree or DKMS modules, generated and Rust sources, built-in versus loadable state. Non-goals are kernel address layout or System.map dumps, non-Linux kernels (Zephyr, FreeRTOS, Xen), distribution administration, datasheet-level register programming and hardware bring-up, exploit development against live systems, and certification sign-off. Verified against Linux 6.18.58 LTS.
license: MIT
compatibility: Requires a local Linux kernel source tree (default $HOME/src/linux-6.18.58) for verified answers; works offline once installed. Scripts need Python 3.10+. Packaging validation optionally needs uvx and skills-ref (Python 3.11+).
---

# Linux Kernel Map

One map, one verification rule, four workflows. Every answer is checked against a specific tree and
kernel version before it is called verified.

## Shared rules

1. **Version and tree first.** State `Verified against: <version> | Tree: <path|none> | Status:
<verified|partial|unverified>` on the first line of every answer. `Status: verified` requires a
   tree check; `Tree: none` forces `unverified`.
2. **No fabricated paths.** Resolve in the tree or label the gap. A plausible function name is not a
   location.
3. **No address layout.** `vmlinux`, `System.map`, and module `.ko` files may be consumed to
   resolve a symbol during triage; their layout is never presented.
4. **Architecture and fork honesty.** Never substitute an x86 path for arm64 or RISC-V, and never
   present an upstream path as verified in a vendor, Android, or RT tree.
5. **Generated is not source.** Point at the generator or template, not the generated file.
6. **One map, one rule.** Every workflow resolves against `references/map.json` and applies the
   same labeling rule. A workflow never introduces a location the refresh procedure cannot re-verify.

## Answer envelope

```text
Verified against: 6.18.58 | Tree: /path/to/linux | Status: verified|partial|unverified
```

See the per-workflow references for the required fields.

## Routing

| User signal                                                 | Workflow    | Read                        |
| ----------------------------------------------------------- | ----------- | --------------------------- |
| "where does X live", "which file owns Y", "trace syscall Z" | Navigation  | `references/navigation.md`  |
| panic, oops, WARNING, soft lockup, hung task, KASAN/UBSAN   | Triage      | `references/triage.md`      |
| "write a driver", "add a module", probe/remove/IRQ/DMA/PM   | Authoring   | `references/authoring.md`   |
| "is this path safe", "audit", "threat model", STRIDE        | Security    | `references/security.md`    |
| "how do I observe X", "least invasive way to see Y"         | Observation | `references/observation.md` |

Non-goals: address layout or `System.map` dumps, non-Linux kernels, distribution administration,
datasheet-level register programming and hardware bring-up, exploit development against live systems,
and certification sign-off.

## Map

`references/map.json` is the single source of truth: six layers, fifteen areas, one to five entry
symbols per area, config gates, and verification commands. It is verified against Linux 6.18.58 LTS
and re-resolved against the user's tree by `scripts/check_map.py` before any location is called
verified.

The layered organizing model is an inspiration from the Linux Kernel Map
(makelinux.github.io/kernel/map/); no GPL-3.0 or CC BY-SA content is copied, and every symbol is
verified independently.

## Verification

- `scripts/check_map.py --map references/map.json --tree "$KERNEL_SRC"` — re-verify every area.
- `scripts/check_package.py .` — frontmatter, budgets, references, attribution, eval schema.
- `scripts/symbolize.py` — decode splats from a supplied artifact.

## References

- `references/map.json` — layers, areas, symbols, gates, commands
- `references/navigation.md` — resolution, traces, version and fork honesty
- `references/triage.md` — splat classes, symbolization, taint, next evidence
- `references/authoring.md` — scaffolds, IRQ, DMA, PM, teardown
- `references/security.md` — trust boundaries, checks, STRIDE/LINDDUN
- `references/observation.md` — least-invasive observation decision table
