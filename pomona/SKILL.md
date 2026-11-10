---
name: pomona
description: "Continuous code-quality cycle: Automate verification, Enforce standards, and Maintain system health over time"
---

# **Pomona:** Continuous Code Quality Improvement

Pomona system at Bloomberg implements a Kaizen-inspired cycle of automated discovery and incremental repair. It uses two coordinated workflows — **Scanning** and **Repair** — connected by a structured roadmap.

## Priority Matrix for Task Management

All tasks are categorized into four priority levels:

| Quadrant         | Easy to review      | Hard to review            |
| ---------------- | ------------------- | ------------------------- |
| **High benefit** | **P1 — Do first**   | **P3 — Worth doing**      |
| **Low benefit**  | **P2 — Quick wins** | **P4 — Eliminate / Drop** |

**Do First (Crisis Management):** Critical production bugs, outages, immediate security vulnerabilities, or hard regulatory deadlines.

**Worth doing (Strategic Capability):** Software architecture, refactoring, automated testing, edge-cases, technical debt reduction, system decoupling, and career growth.

**Quick wins (Reactive Noise):** Constant interruptions, minor operational chatter, or low-impact feature requests demanding immediate attention.

**Eliminate / Drop (Waste & Vanity):** Low-value distractors, speculative future-proofing (YAGNI), or vanity metrics.

## Roadmap Format

Store the roadmap at the repository root as `ROADMAP.md`.

Each entry follows this format:

```markdown
## P1 — Do First

- [ ] **Description of the task**
  - **File**: `path/to/file.*`
  - **Source**: ruff rule violation / TODO comment / dead code / test gap / long function
  - **Details**: More context for the fix
  - **Sub-tasks** (if needed):
    - [ ] Sub-task 1
```

## Roadmap Bun Script

A zero-dependency Bun script bundled with this skill manages the roadmap lifecycle deterministically. Scanning stays with agents; mutations go through this script for predictable dedupe, priority, and delete-on-done semantics.

```sh
bun run pomona/scripts/roadmap.ts init                    # create ROADMAP.md with P1–P4 headings
bun run pomona/scripts/roadmap.ts status                  # counts per priority + total
bun run pomona/scripts/roadmap.ts list [--priority P1]    # open tasks, P1→P4 order [--json]
bun run pomona/scripts/roadmap.ts add --priority P1 --title "Fix X" --file "src/x.ts" --source "bun check" [--details "..."] [--subtask "..."]
bun run pomona/scripts/roadmap.ts next                    # first open task in P1→P4 order
bun run pomona/scripts/roadmap.ts dedupe                  # remove duplicate open entries (keep first)
bun run pomona/scripts/roadmap.ts move --id 2 --to P2     # reprioritize
bun run pomona/scripts/roadmap.ts done --id 3             # delete completed (audit = git log) / --match "..."
```

Notes:

- `--roadmap <path>` overrides the default `./ROADMAP.md`.
- `--json` on `list`/`status`/`next` yields machine-readable output for agents.
- `add` is idempotent: a duplicate open entry (same normalized title + file) is rejected, not doubled.
- `done`/`remove` **delete** the entry, never mark `- [x]` in-file.
- `dedupe` mirrors the canonical aggregation step: dedupe against open `- [ ]` entries only; a regressed issue with no open entry should be re-added on next scan.

Use this script for all roadmap mutations in **Step 3** (Repair) and after scanning **Step 2** — hand-editing `ROADMAP.md` bypasses dedupe and risks formatting drift.

## Workflow

### Step 1: Check or Initialize the Roadmap

Check if `ROADMAP.md` exists in the repository root. If it doesn't, or if high-priority tasks (P1 and P2) are empty, run the **Scanning** workflow first (Step 2), then return here. Scanning is an **on-demand refill** triggered as part of Repair only when the roadmap runs low on high-priority tasks ("when the roadmap runs low on high-priority tasks (P1 and P2 categories are empty)") — not on every cycle.

Do **not** perform a fresh scan when P1/P2 still contain open tasks; work through the existing prioritized roadmap first. This lazy refill is intentional — it avoids redundant scanning. Only force a full rescan when explicitly requested by the user or when priorities have gone stale and need a refresh.

### Step 2: Scanning — Discover Code Quality Tasks

**Canonical language-agnostic pomona** The framework applies to any language/stack. Launch multiple sub-agents IN PARALLEL, each exploring a different discovery areas:

**Sub-agent 1 — Static analysis expansion:**

- **Apply the Boy Scout Rule:** Establish a habit of performing small, continuous refactorings—renaming confusing variables, breaking up large functions, and removing duplication—on.
- **Enforce Automated Formatting and Style:** Integrate pre-commit hooks to automate code formatting (`dart format`, `gofmt`, `clang-format`) and verify file headers, license notices, and copyright years.
- **Run Linter and Static Analysis Pass:** Execute static analyzers with fatal warnings (e.g., `dart analyze --fatal-infos`, `clang-tidy`, `pylint`) to catch type errors, violations of rules that have auto-fixes available (e.g., Collapse all auto-fixable style violations into one roadmap ticket per tool), unsafe assignments, and language-specific pitfalls.
- **Audit Allowlist and Dependency Injections:** Review project dependency manifests and allowlists to prevent unauthorized third-party package additions or security vulnerabilities
- **Scan for Leftover TODO Markers and Commented-Out Code:** Run static checks to flag unresolved `TODO` comments or blocks of commented-out code.
- **Verify System Architectural Layering:** Scan dependencies to prevent unintended cross-layer coupling and architectural boundary violations

**Sub-agent 2 — Test coverage gaps and code structure:**

- **Audit Test Pyramid Alignment:** Verify that the test suite maintains the recommended ratio: **\~80% small unit tests**, **\~15% medium integration tests**, and **\~5% large system/E2E tests**.
- **Enforce the Humble Object Pattern on UI/Framework Boundaries:** Decouple business logic from hard-to-test UI, hardware, or third-party framework boundaries, keeping boundary code thin and anemic.
- **Verify Test Confirmability & DAMP Principles:** Ensure tests use **Descriptive And Meaningful Phrases (DAMP)**, avoid brittle over-mocking, and test resulting state rather than internal method call order.

> **I1–I9 demotion:** All detailed heuristics above (dual-rule reporting, collapse same-rule, markdown triage, missing-config flag, command enumeration + git-hash anchoring, clean-result qualification, NOT-checked disclosure, concrete extraction boundary, function-level coverage counting) are **Suggested extensions**. Keep as optional samples; do not present as canonical aggregation.

**Aggregate results (2 steps only):**

1. Concatenate all findings and remove duplicates — dedupe against each other and against current open `- [ ]` entries in `ROADMAP.md`. Since completed tasks are deleted (audit = `git log`), do not dedupe against `- [x]` history; a regressed issue should legitimately be re-added on next scan.
2. Assign each unique finding a priority (P1–P4) using the priority matrix (Table 1) above. Error on the side of lower priority (P2/P4) when the benefit is marginal.

### Step 3: Repair — Pick and Fix a Task

Select a scope-related batch tasks from the highest non-empty priority category (P1 → P2 → P3 → P4). If a task has sub-tasks, pick all sub-tasks.

**Deduplication:** Before starting, check **open PRs** for an existing PR covering the same file/rule/task — deduplicates against open PRs to avoid duplicate work. If a matching open PR exists, skip and pick the next task.

**Critical: verify the task exists in the roadmap before starting.** If the selected task is not already an entry in `ROADMAP.md`, add it first. The roadmap must accurately reflect what is being worked on at all times — this is the core of the continuous improvement cycle. Never fix an issue that isn't tracked.

**Implement the fix:**

1. Make the code change targeting **~10 lines of diff** ("targeting ~10 lines of diff" / "aim for roughly 10 lines") as an aspiration, not a hard cap.
2. **median 16, mean 29.4, range 5–139** (max 139 merged in ~1h). If a coherent fix exceeds ~10, apply the split strategy — e.g., _"enable rules / add tests for one directory at a time"_ — or slice the task and add follow-up roadmap entries, rather than enforcing a hard "≤10, stop at 11+" budget. Do not apply invented counting rules (e.g., "whitespace/renames free").
3. After making changes, return into **Step 2: Scanning — Discover Code Quality Tasks**.

**Roadmap update:**

- Delete the completed task entry from `ROADMAP.md`.
- Add any follow-up tasks discovered during the fix as new entries in the appropriate priority section.
- Do not mark tasks as `- [x]` or preserve completed entries in-file — the audit trail is `git log` / `git history` of `ROADMAP.md` (paper §2.3: "Since the roadmap is stored in the repository, there is no need to maintain a separate log... git history tracks changes"). Preserving `- [x]` entries in-file was a divergence: it changes `git diff` semantics (completed tasks appear as modified lines rather than deletions) and breaks deduplication logic (re-scan should dedupe against current open `- [ ]` entries only; a deleted entry correctly allows re-discovery if the underlying issue regresses, while a retained `- [x]` entry accumulates stale history in the working tree).

### Step 4: Loop

Return to Step 1 to check the roadmap again. This creates the continuous improvement cycle.

**Feedback Loops & Kaizen (Deming Cycle):** Return to **step 1** and establish continuous feedback loops that feed production incidents, user metrics, and post-incident reviews back into `ROADMAP.md`.
