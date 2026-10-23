# Security

Defensive review of a kernel path: where user-controlled data enters, which checks stand on the
path, and how each STRIDE category is answered. No live-target testing and no exploit code.

## Path model

1. **Entry points**: syscall, ioctl, sysfs attribute, proc file, netlink message, debugfs.
2. **Trust boundaries**: where user-controlled data crosses into the kernel.
3. **Copy sites**: `copy_from_user`, `get_user`, `strncpy_from_user`, and equivalents.
4. **Checks**: capabilities, permission checks, and LSM hooks on the path.
5. **Assets**: what the path protects (data, capability, resource).

## Check inventory

| Check                    | What it establishes                | Typical location          |
| ------------------------ | ---------------------------------- | ------------------------- |
| `capable` / `ns_capable` | Capability held by the caller      | `kernel/capability.c`     |
| `file_permission`        | Read/write/execute on an open file | `fs/namei.c`, `security/` |
| `inode_permission`       | Permission on an inode             | `fs/namei.c`              |
| `may_open`               | Whether a path may be opened       | `fs/namei.c`              |
| `security_*` LSM hooks   | Policy decision by a loaded LSM    | `security/security.c`     |

Every check is cited as `path:symbol`. If none exist, write `none` and the search that established
it.

## Absent versus bypassable

- **Absent in this tree**: the check is not on the path. Cite the failed search.
- **Present but bypassable**: the check exists but is reached after the dangerous operation, or is
  guarded by a condition the attacker controls. Cite the location and explain the bypass.

## STRIDE worksheet

For a named path or subsystem, produce one row per category:

| Category               | Status                                        | Evidence                         |
| ---------------------- | --------------------------------------------- | -------------------------------- |
| Spoofing               | mitigated / not-applicable / unverified / gap | verified `path:symbol` or reason |
| Tampering              | ...                                           | ...                              |
| Repudiation            | ...                                           | ...                              |
| Information disclosure | ...                                           | ...                              |
| Denial of service      | ...                                           | ...                              |
| Elevation of privilege | ...                                           | ...                              |

- `mitigated` requires a verified `path:symbol`.
- `not-applicable` requires the reason the category was ruled out.
- `gap` requires a hypothesis and the evidence that would confirm it.
- Generic hardening advice is not evidence.

## LINDDUN

Add LINDDUN categories (linkability, identifiability, non-repudiation, detectability,
disclosure, unawareness, non-compliance) only when the path handles personal data, such as tracing
buffers, keyrings, or audit logs.

## Answer shape (security)

- `Scope:`, `Assets:`, `Attacker capabilities:`, `Trust boundaries:`, `Checks:`,
  `STRIDE:` (six rows), `LINDDUN:` (when applicable), `Gaps:`, `Boundary:`.

## Boundary

Defensive review only. No live-target testing, no exploit code, no step-by-step intrusion guidance.
A request to attack a live system is declined with this boundary stated.
