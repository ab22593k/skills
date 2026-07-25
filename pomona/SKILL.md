---
name: pomona
description: "Run the Pomona continuous code-quality improvement cycle: scan a project for lint violations, TODO/FIXME comments, dead code, test gaps, and long functions; prioritize findings into a P1-P4 backlog; then pick the top task and create a tiny (~10 line diff) PR. Use whenever the conversation involves: automated code maintenance, technical debt reduction, scanning a repo for quality issues, setting up a cleanup pipeline, making small incremental fixes (Kaizen-style), cleaning up TODOs or dead code, enabling stricter linter rules, or filing small focused PRs one at a time. Also trigger if the user mentions Pomona by name, asks for a 'backlog of code quality tasks', or describes a workflow where the agent repeatedly finds one small issue, fixes it."
---

# Pomona: Continuous Code Quality Improvement

Pomona system at Bloomberg implements a Kaizen-inspired cycle of automated discovery and incremental repair. It uses two coordinated workflows — **Scanning** and **Repair** — connected by a structured backlog.

## Priority Matrix for Task Management

All tasks are categorized into four priority levels:

|                  | Easy to review      | Hard to review                       |
| ---------------- | ------------------- | ------------------------------------ |
| **High benefit** | **P1 — Do first**   | **P3 — Worth doing, plan the split** |
| **Low benefit**  | **P2 — Quick wins** | **P4 — Parking lot (don't pick)**    |

**High benefit** means: catches real bugs or prevents future bugs (mutable defaults, loop variable capture, missing exception chains); reduces maintenance burden (removing dead code, fixing misleading comments); or improves developer experience (better error messages, clearer code).

Examples of what IS high benefit: security issues (unsafe temp directories, missing input validation), test gaps in core logic modules, dead code that could mislead maintainers, complex functions that are hard to reason about, commented-out code that has accumulated.

Examples of what IS NOT high benefit: missing language specifiers on fenced code blocks (cosmetic, no semantic impact), missing label references in markdown that are internal references (often intentional), empty keys in auto-generated lock files, heading hierarchy skips in documentation. These are purely mechanical and should be P2/P4.

**Easy to review** means: fully automated (auto-fix, formatting); mechanical and repetitive (reviewer can scan quickly); small in scope (single file or single rule); and does not introduce behavioural changes (pure refactoring).

**"Out of scope" convention:** If a scan surfaces findings in auto-generated files (lockfiles, build artifacts) or files the user has explicitly excluded, list them briefly in a dedicated "Out of scope / generated artifacts" section rather than assigning them a priority. This prevents the same noise from being re-surfaced on every scan.

## Backlog Format

Store the backlog at the repository root as `pomona_backlog.md` put it into .gitignore if not existed there. Each entry follows this format:

```markdown
## P1 — Do First

- [ ] **Description of the task**
  - **File**: `path/to/file.*`
  - **Source**: ruff rule violation / TODO comment / dead code / test gap / long function
  - **Details**: More context for the fix
  - **Sub-tasks** (if needed):
    - [ ] Sub-task 1
```

## Workflow

### Step 1: Check or Initialize the Backlog

Check if `pomona_backlog.md` exists in the repository root. If it doesn't, or if high-priority tasks (P1 and P2) are empty, run the **Scanning** workflow first (Step 2), then return here.

### Step 2: Scanning — Discover Code Quality Tasks

Launch multiple sub-agents IN PARALLEL, each exploring a different discovery area:

**Sub-agent 1 — Static analysis expansion:**

- Identify linting rules that could be enabled or tightened for this project. Look at the project's language and existing config files (e.g., `.ruff.toml`, `.eslintrc`, `.golangci.yml`, `pyproject.toml`).
- Find violations of rules that have auto-fixes available. These are P1/P2 because they're high-benefit (catch bugs) and easy to review (automated).
- Look for type checking strictness that can be increased.

**Sub-agent 2 — TODO/dead code audit:**

Scan ALL languages present in the repository, not just the primary language. For each language (Python, TypeScript, Rust, Go, Markdown, shell, config files), apply the appropriate search tools.

- Search the codebase for `TODO|FIXME|HACK|XXX` comments and classify each:
  - Self-documenting removals (the code is already done) → P1
  - Clear fixes with obvious solutions → P1/P2
  - Fixes requiring further domain investigation → P3
  - Aspirational comments → P4
- Search for comments that contradict the surrounding code.
- Identify dead code: unused imports, commented-out code blocks (>3 consecutive commented lines), unreachable code after early returns.
- For each category, enumerate which languages/files were examined and what tool/command was used (e.g., `ruff check --select F401`, `grep -rn "TODO"`). Include the exact command and its output so findings are reproducible.
- If a finding count is zero, confirm it by showing the command and its empty output — don't just assert "0 found."

**Sub-agent 3 — Test coverage gaps and code structure:**

- Compare source modules with test modules to find untested modules.
- Prioritize pure-logic modules without heavy data dependencies (easiest to test) and modules with complex branching logic (highest value).
- Check compliance with the repository's coding standards (agent config files, project conventions).
- Find functions longer than 50 lines that could be decomposed.

**Aggregate results:**

1. Concatenate all findings and remove duplicates.
2. Assign each unique finding a priority (P1–P4) using the priority matrix above. Err on the side of lower priority (P2/P4) when the benefit is marginal.
3. Convert each finding to the backlog format and append to the appropriate priority section of `pomona_backlog.md`.
4. If a scan uncovered items outside the requested scope (e.g., package hygiene during a TODO audit), place them in a clearly labeled "Additional observations" section — never mix them into the priority backlog.

### Step 3: Repair — Pick and Fix a Task

Select the first task from the highest non-empty priority category (P1 → P2 → P3 → P4). If a task has sub-tasks, pick the first sub-task.

**Critical: verify the task exists in the backlog before starting.** If the selected task is not already an entry in `pomona_backlog.md`, add it first. The backlog must accurately reflect what is being worked on at all times — this is the core of the continuous improvement cycle. Never fix an issue that isn't tracked.

**Implement the fix:**

1. Make the code change. Aim for **at most 10 lines of diff** (insertions + deletions). This is critical — small diffs are the #1 factor for PR acceptance. If a change exceeds 10 lines, you have two options: find a smaller slice of the same issue, or split into multiple backlog tasks.
2. The 10-line budget includes everything: code changes, formatting, comments. Only whitespace-only changes and file renames are free. If you're at 11+ lines, stop and find a narrower fix.
3. After making changes, validate with the project's test and linting commands.
4. If validation fails, fix the issues and re-validate.

**Update the backlog:**

- Mark the completed task as done: change `- [ ]` to `- [x]` and add a completion note.
- Preserve completed tasks in the backlog (don't delete them) — they serve as an audit trail and prevent re-scanning the same issue.
- Add any follow-up tasks discovered during the fix as new entries.

### Step 4: Loop

Return to Step 1 to check the backlog again. This creates the continuous improvement cycle.

## Design Rationale

**Why small changes?** Bloomberg's deployment achieved 88% acceptance (15/17 PRs merged) with a median time-to-close under 2 hours. 90% of surveyed engineers cited small diffs as the most appealing feature. Small changes reduce reviewer skepticism and cognitive load.

**Why the backlog?** A visible, prioritized backlog in the repository gives engineers control and transparency. They can see what's being worked on, add their own tasks, and adjust priorities. The backlog format also makes the system's behavior predictable and auditable.

**Why human-in-the-loop?** Engineers (especially senior ones with 10+ years experience) remain wary of fully automated agentic judgment. The PR format with mandatory human review builds trust while still delivering value. The paper's survey found 8/10 engineers wanted to try Pomona, but many wanted control over prioritization.

**Why parallel scanning sub-agents?** Different kinds of issues require different expertise. Running sub-agents in parallel is faster and each can focus on its domain. The aggregation step deduplicates and prioritizes, so the result is coherent.
