# Navigation

Resolution, tracing, and version honesty for the Linux kernel source tree. Every location is verified
against `$KERNEL_SRC` before it is presented.

## Resolution procedure

1. **Name the observable.** Syscall, device, configuration symbol, log line, or symbol name.
2. **Narrow to candidate areas.** Use `references/map.json`: match the observable to one or more
   area ids, then read their `roots` and `symbols`.
3. **Confirm before presenting.** For each candidate, run its `verify_commands` in `$KERNEL_SRC`.
   A path that fails becomes `unverified`, never `verified`.
4. **Disambiguate.** If a symbol has many implementations, name the subsystem, bus, or
   configuration that selects one. Never silently choose a driver.
5. **Label.** Apply the answer envelope and the degradation rules from
   `contracts/answer-contract.md` section 5.

## Answer shape (navigation)

- `Roots:` one to four tree-relative directories.
- `Entry symbols:` at least one, each `path:symbol — one-line role`.
- `Config gate:` one `CONFIG_*` symbol or `ALWAYS`.
- `Trace:` when the question names an entry point. At least three hops.
- `Observation point:` when behavior must be watched.
- `Verify:` one runnable command with its expected observable.
- `Unverified:` named gaps, or `none`.

## Trace recipe

An end-to-end trace has at least three hops:

```text
userspace -> syscall -> VFS -> subsystem -> driver -> hardware
```

Each hop is `boundary: path:symbol`. Include the operations structure when one is involved:

| Boundary       | Typical operations structure      | Concrete callback          |
| -------------- | --------------------------------- | -------------------------- |
| VFS            | `struct file_operations`          | `.read`, `.open`, `.ioctl` |
| inode          | `struct inode_operations`         | `.lookup`, `.create`       |
| address space  | `struct address_space_operations` | `.readpage`, `.writepage`  |
| network device | `struct net_device_ops`           | `.ndo_start_xmit`          |
| block device   | `struct block_device_operations`  | `.submit_bio`              |

Example, `read(2)`:

1. `userspace: read(2)` entry in libc
2. `syscall: arch/x86/entry/syscall_64.c:do_syscall_64`
3. `vfs: fs/read_write.c:ksys_read`
4. `vfs: fs/read_write.c:vfs_read`
5. `driver: <file>:<file_operations.read>`

Example, `openat(2)` returning `EACCES`:

1. `userspace: openat(2)`
2. `syscall: arch/x86/entry/syscall_64.c:do_syscall_64`
3. `vfs: fs/open.c:do_sys_openat2`
4. `vfs: fs/namei.c:do_filp_open`
5. `permission: fs/namei.c:may_lookup` or the LSM hook that denies

Observation point: attach a kprobe or tracepoint at the decision function, or use
`/sys/kernel/tracing` function tracing on the entry symbol.

## Disambiguation

When a symbol is implemented by many drivers, never silently choose one. Instead:

- Name the subsystem, bus, or configuration that selects the implementation.
- Return the candidates with that discriminator, or
- Return one implementation and state the discriminator that makes it representative.

Examples of discriminators: `CONFIG_NET`, `bus_type` (PCI vs USB vs platform), `file_operations`
vs `block_device_operations`, architecture (`arch/x86` vs `arch/arm64`).

## Architecture

The map shows x86 paths where architecture matters. For any other target:

- State the assumed architecture explicitly.
- Re-resolve inside the target tree before presenting.
- Never present an x86 path for an arm64 or RISC-V target without that re-resolution.

## Version scope and refresh procedure

- Verified version: **Linux 6.18.58 LTS** (released 2026-10-21).
- Delta-check target: **7.3 mainline** (2026-10-18), used only to detect drift.
- Refresh procedure:
  1. Obtain the new tree and set `KERNEL_SRC`.
  2. Run `scripts/check_map.py --map references/map.json --tree "$KERNEL_SRC"`.
  3. For each failing entry, re-resolve: search the new tree for the symbol, update `file`,
     `roots`, and `verify_commands`, and record the new version in `kernel_version`.
  4. Update `verified_at` and `kernel_version` in `map.json` only when every entry passes or is
     explicitly re-resolved.
  5. Run the eval suite; the stale-path case must still fail when an entry is wrong.

Detecting a moved or renamed file:

- `git log --follow -- <path>` in a git checkout, or
- `grep -R "<symbol>" "$KERNEL_SRC"` and compare the new location to the old.

## Forks and out-of-tree modules

- Vendor, Android, and RT trees may carry newer code in an older version. Treat upstream paths as
  candidates and verify inside that tree; name the likely divergence.
- Out-of-tree and DKMS modules are not mapped. Navigation and authoring need the module tree;
  module-specific paths stay unverified until it is supplied.
- Built-in versus loadable: a module-only path is not always present. State the config state.

## Generated and Rust sources

- Distinguish source files from build-generated files (`*.o`, `*.cmd`, generated headers).
- Point at the source or template that generates the file; do not present the generated path as the
  place to read or change behavior.
- Rust-for-Linux bindings are experimental and version-sensitive; never present them as equivalent
  to C modules without stating the supported version.

## When no tree is available

- `Tree: none`, `Status: unverified`.
- Provide the exact search that would confirm the answer, for example
  `grep -rn "do_sys_openat2" "$KERNEL_SRC/fs"`.
- Never present a recalled path as verified.
