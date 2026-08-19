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

Examples of what IS high benefit for P1 specifically (the items to do first): fixing failing tests, adding a project-level lint configuration (ruff.toml, coverage config) so residuals become enforceable, fixing known test gaps in critical extraction backends. These unblock all downstream work.

Examples of what IS NOT high benefit: missing language specifiers on fenced code blocks (cosmetic, no semantic impact), missing label references in markdown that are internal references (often intentional), empty keys in auto-generated lock files, heading hierarchy skips in documentation, micro-simplifications like SIM103 (needless `if...return True/else return False`). These are purely mechanical and should be P2/P4.

**Easy to review** means: fully automated (auto-fix, formatting); mechanical and repetitive (reviewer can scan quickly); small in scope (single file or single rule); and does not introduce behavioural changes (pure refactoring).

**"Out of scope" convention:** If a scan surfaces findings in auto-generated files (lockfiles, build artifacts) or files the user has explicitly excluded, list them briefly in a dedicated "Out of scope / generated artifacts" section rather than assigning them a priority. This prevents the same noise from being re-surfaced on every scan.

## Backlog Format

Store the backlog at the repository root as `pomona.md`; put it into .gitignore if not existed there.

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

## Workflow

### Step 1: Check or Initialize the Backlog

Check if `pomona.md` exists in the repository root. If it doesn't, or if high-priority tasks (P1 and P2) are empty, run the **Scanning** workflow first (Step 2), then return here.

**Important:** When running the full cycle (scan + repair), ALWAYS perform a fresh scan (Step 2) even if the backlog already exists. The scan discovers the current state of the project — without it, the cycle drifts into fixing stale or low-value items while missing newly introduced issues. A backlog without a matching scan is just a wishlist.

### Step 2: Scanning — Discover Code Quality Tasks

Launch multiple sub-agents IN PARALLEL, each exploring a different discovery area:

**Sub-agent 1 — Static analysis expansion:**

- Identify linting rules that could be enabled or tightened for this project. Look at the project's language and existing config files (e.g., `.ruff.toml`, `.eslintrc`, `.golangci.yml`, `pyproject.toml`).
- Find violations of rules that have auto-fixes available. These are P1/P2 because they're high-benefit (catch bugs) and easy to review (automated).
- **When reporting ruff residuals, report under both the currently enabled rule set and the broader suggested rule set.** "0 errors under default rules but 100+ under SIM/E501/PTH" is honest; "0 errors" alone is misleading when the user should enable more rules.
- **Collapse all auto-fixable style violations into one backlog ticket per tool** (e.g., "Apply all ruff auto-fixes" instead of listing each `COM812`, `D209`, `I001` separately). The reviewer can batch-approve them as a single mechanical change.
- **Triage markdown label references**: when ESLint reports `markdown/no-missing-label-refs`, quickly distinguish real broken links from intentional template placeholders (tags like `{install odoo}`, `{setup dev environment}`). Only backlog the real broken links.
- Look for type checking strictness that can be increased.
- **Flag the absence of tool configuration files** (missing `.ruff.toml`, `pyproject.toml`, `tsconfig.json`) as the single highest-leverage process finding — once a project has an agreed lint baseline, everything else becomes easier to implement and enforce.

**Sub-agent 2 — TODO/dead code audit:**

Scan ALL languages present in the repository, not just the primary language. For each language (Python, TypeScript, Rust, Go, Markdown, shell, config files), apply the appropriate search tools.

- Search the codebase for `TODO|FIXME|HACK|XXX` comments and classify each:
  - Self-documenting removals (the code is already done) → P1
  - Clear fixes with obvious solutions → P1/P2
  - Fixes requiring further domain investigation → P3
  - Aspirational comments → P4
- Search for comments that contradict the surrounding code.
- Identify dead code: unused imports, commented-out code blocks (>3 consecutive commented lines), unreachable code after early returns, unused variables and functions.
- For unused variable/function detection, use a **semantic tool** (e.g., `ruff check --select F841` for Python, `vulture` for deeper analysis) in addition to grep-based heuristics. String searches alone miss unused functions, dead conditional branches, and code behind `if TYPE_CHECKING` or `if False:` guards.
- For each category, enumerate which languages/files were examined and what tool/command was used (e.g., `ruff check --select F401`, `grep -rn "TODO"`). Include the exact command and its output so findings are reproducible.
- If a finding count is zero, confirm it by showing the command and its empty output — don't just assert "0 found."
- **Include the exact git revision or tree hash** that was scanned so the result is anchored to a specific point in the project's history.
- **Qualify "clean" results** with the methodology used: "No unused imports found via `ruff check --select F401`" is precise. "No unused imports found" is over-confident — it implies a level of semantic analysis the tool doesn't perform.
- **State what was NOT checked** explicitly — e.g., "Unused functions/methods not assessed (ruff F841 only covers local variables, not function definitions)." This prevents readers from over-interpreting a narrow negative result.

**Sub-agent 3 — Test coverage gaps and code structure:**

- Compare source modules with test modules to find untested modules.
- Prioritize pure-logic modules without heavy data dependencies (easiest to test) and modules with complex branching logic (highest value).
- Check compliance with the repository's coding standards (agent config files, project conventions).
- Find functions longer than 50 lines that could be decomposed.
- **For each long function, propose a concrete extraction boundary** (e.g., "Pull chapter-heading detection into a pure function returning an enum" rather than just "decompose main()"). Specific proposals are reviewable; general ones are not.
- **Report function-level coverage**, not just module presence. "All modules have test files" is not the same as "extraction backends are tested." Count specifically which functions lack tests (e.g., "extract_with_pymupdf: untested, extract_with_ebooklib: untested, \_handle_pdf_extraction: untested, main(): untested").

**Aggregate results:**

1. Concatenate all findings and remove duplicates.
2. Assign each unique finding a priority (P1–P4) using the priority matrix above. Err on the side of lower priority (P2/P4) when the benefit is marginal.
3. Convert each finding to the backlog format and append to the appropriate priority section of `pomona.md`.
4. If a scan uncovered items outside the requested scope (e.g., package hygiene during a TODO audit), place them in a clearly labeled "Additional observations" section — never mix them into the priority backlog.
5. **Collapse repeated items of the same rule/tool into a single ticket** — both within and across priority levels. For example, 22 fenced-code-language violations across different files should be one P2 ticket, not 22 separate ones. If they span multiple priority levels, put them all at the lower priority.
6. **For each P1 and P2 item, include a measurable acceptance criterion** (e.g., "Reduce ESLint errors from 117 to <50" or "Add tests for 3 untrusted extraction backends"). Without criteria, the loop has no stopping condition.
7. **Include a "Measurement" block at the top of the backlog** with current baseline numbers and scanned surface:
   - Total lint errors by tool (e.g., "ruff: 48 errors, ESLint: 102 errors")
   - Files and lines of code scanned (e.g., "4 Python files, ~1.5 kLOC")
   - Current test coverage % (or "no coverage tool configured")
   - Number of functions exceeding 50 lines
   - Number of untested source modules
   - These baselines make progress trackable across iterations.

### Step 3: Repair — Pick and Fix a Task

Select the first task from the highest non-empty priority category (P1 → P2 → P3 → P4). If a task has sub-tasks, pick the first sub-task.

**Critical: verify the task exists in the backlog before starting.** If the selected task is not already an entry in `pomona.md`, add it first. The backlog must accurately reflect what is being worked on at all times — this is the core of the continuous improvement cycle. Never fix an issue that isn't tracked.

**Implement the fix:**

1. Make the code change. Aim for **at most 10 lines of diff** (insertions + deletions). This is critical — small diffs are the #1 factor for PR acceptance. If a change exceeds 10 lines, you have two options: find a smaller slice of the same issue, or split into multiple backlog tasks.
2. The 10-line budget includes everything: code changes, formatting, comments. Only whitespace-only changes and file renames are free. If you're at 11+ lines, stop and find a narrower fix.
3. After making changes, validate with the project's test and linting commands.
4. If validation fails, fix the issues and re-validate.
5. **Report after-state metrics** in the PR description: how many errors remain after the fix (e.g., "ruff — 48 → 42 errors"). This turns progress from narrative to quantitative.
6. If the fix addresses a security issue, include the **CWE reference** and explain why the old code was unsafe — not just what changed, but why the old pattern is dangerous.

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
