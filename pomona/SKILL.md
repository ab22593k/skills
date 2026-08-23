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

Store the backlog at the repository root as `pomona.md` (paper §2.3 stores it in the repository so `git log -- pomona.md` is the audit trail). Only add it to `.gitignore` if you explicitly want a local-only backlog — doing so opts out of the paper's git-history audit trail.

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

Check if `pomona.md` exists in the repository root. If it doesn't, or if high-priority tasks (P1 and P2) are empty, run the **Scanning** workflow first (Step 2), then return here. Per paper §2.2 + §2.3, scanning is an **on-demand refill** triggered as part of Repair only when the backlog runs low on high-priority tasks ("when the backlog runs low on high-priority tasks (P1 and P2 categories are empty)") — not on every cycle.

Do **not** perform a fresh scan when P1/P2 still contain open tasks; work through the existing prioritized backlog first. This lazy refill is intentional — it avoids redundant scanning. Only force a full rescan when explicitly requested by the user or when priorities have gone stale and need a refresh.

### Step 2: Scanning — Discover Code Quality Tasks

**Canonical Pomona is language-agnostic** (paper §1, §2.2) — the framework applies to any language/stack. The paper's scanning + aggregation is only the 2-step concat+dedup → Table 1 priority described below.

> **Bloomberg example — Suggested extensions per §2.2 "our specific implementation" (not canonical Pomona):** The three sub-agents below are _one_ Bloomberg instantiation. Demoted from canonical — presented as suggested extensions. Adapt, replace, or omit per your language/stack; do not present as canonical Pomona.

Launch multiple sub-agents IN PARALLEL, each exploring a different discovery area _(Bloomberg example)_:

**Sub-agent 1 — Static analysis expansion (Bloomberg example — suggested):**

- Identify linting rules that could be enabled or tightened for this project. Look at the project's language and existing config files (e.g., `.ruff.toml`, `.eslintrc`, `.golangci.yml`, `pyproject.toml`).
- Find violations of rules that have auto-fixes available. These are P1/P2 because they're high-benefit (catch bugs) and easy to review (automated).
- **When reporting ruff residuals, report under both the currently enabled rule set and the broader suggested rule set.** "0 errors under default rules but 100+ under SIM/E501/PTH" is honest; "0 errors" alone is misleading when the user should enable more rules.
- **Collapse all auto-fixable style violations into one backlog ticket per tool** (e.g., "Apply all ruff auto-fixes" instead of listing each `COM812`, `D209`, `I001` separately). The reviewer can batch-approve them as a single mechanical change.
- **Triage markdown label references**: when ESLint reports `markdown/no-missing-label-refs`, quickly distinguish real broken links from intentional template placeholders (tags like `{install odoo}`, `{setup dev environment}`). Only backlog the real broken links.
- Look for type checking strictness that can be increased.
- **Flag the absence of tool configuration files** (missing `.ruff.toml`, `pyproject.toml`, `tsconfig.json`) as the single highest-leverage process finding — once a project has an agreed lint baseline, everything else becomes easier to implement and enforce.

**Sub-agent 2 — TODO/dead code audit (Bloomberg example — suggested):**

Scan ALL languages present in the repository, not just the primary language. For each language (Python, TypeScript, Rust, Go, Markdown, shell, config files), apply the appropriate search tools. _(Suggested extension — paper is language-agnostic; this breadth is Bloomberg's choice.)_

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

**Sub-agent 3 — Test coverage gaps and code structure (Bloomberg example — suggested):**

- Compare source modules with test modules to find untested modules.
- Prioritize pure-logic modules without heavy data dependencies (easiest to test) and modules with complex branching logic (highest value).
- Check compliance with the repository's coding standards (agent config files, project conventions).
- Find functions longer than 50 lines that could be decomposed.
- **For each long function, propose a concrete extraction boundary** (e.g., "Pull chapter-heading detection into a pure function returning an enum" rather than just "decompose main()"). Specific proposals are reviewable; general ones are not.
- **Report function-level coverage**, not just module presence. "All modules have test files" is not the same as "extraction backends are tested." Count specifically which functions lack tests (e.g., "extract_with_pymupdf: untested, extract_with_ebooklib: untested, \_handle_pdf_extraction: untested, main(): untested").

> **I1–I9 demotion:** All detailed heuristics above (dual-rule reporting, collapse same-rule, markdown triage, missing-config flag, command enumeration + git-hash anchoring, clean-result qualification, NOT-checked disclosure, concrete extraction boundary, function-level coverage counting) are **Suggested extensions / Bloomberg example per §2.2 "our specific implementation" — not canonical Pomona**. Keep as optional examples; do not present as canonical aggregation.

**Aggregate results (per paper §2.2 — 2 steps only):**

1. Concatenate all findings and remove duplicates — dedupe against each other and against current open `- [ ]` entries in `pomona.md`. Since completed tasks are deleted per §2.3 (audit = `git log`), do not dedupe against `- [x]` history; a regressed issue should legitimately be re-added on next scan.
2. Assign each unique finding a priority (P1–P4) using the priority matrix (Table 1) above. Err on the side of lower priority (P2/P4) when the benefit is marginal.

> **Skill extensions — not in paper §2.2:** Steps 3–7 below are skill additions. Paper stops at the 2 steps above; do not attribute these to §2.2. 3. Convert each finding to the backlog format (Fig. 2) and append to the appropriate priority section of `pomona.md` (open tasks only). 4. If a scan uncovered items outside the requested scope (e.g., package hygiene during a TODO audit), place them in a clearly labeled "Additional observations" section — never mix them into the priority backlog. 5. Collapse repeated items of the same rule/tool into a single ticket — both within and across priority levels (e.g., 22 fenced-code-language violations → one P2 ticket; if spanning priorities, use the lower). 6. For each P1 and P2 item, optionally include a measurable acceptance criterion (e.g., "Reduce ESLint errors from 117 to <50") — useful but not paper-required. 7. Optionally include a "Measurement" block at the top of the backlog with baseline numbers (lint errors by tool, files/LOC scanned, coverage %, functions >50 lines, untested modules) — skill polish, not paper.

### Step 3: Repair — Pick and Fix a Task

Select the first task from the highest non-empty priority category (P1 → P2 → P3 → P4). If a task has sub-tasks, pick the first sub-task.

**Paper deduplication (missing detail added):** Before starting, check **open PRs** for an existing PR covering the same file/rule/task — paper §2.3 deduplicates against open PRs to avoid duplicate work. If a matching open PR exists, skip and pick the next task.

**Critical: verify the task exists in the backlog before starting.** If the selected task is not already an entry in `pomona.md`, add it first. The backlog must accurately reflect what is being worked on at all times — this is the core of the continuous improvement cycle. Never fix an issue that isn't tracked.

**Implement the fix:**

1. Make the code change targeting **~10 lines of diff** (Abstract + §2.3: "targeting ~10 lines of diff" / "aim for roughly 10 lines") as an aspiration, not a hard cap — small diffs are the #1 factor for PR acceptance.
2. Per Evaluation §3.1.1 this is aspirational: **median 16, mean 29.4, range 5–139** (max 139 merged in ~1h). If a coherent fix exceeds ~10, apply the paper's split strategy — e.g., _"enable rules / add tests for one directory at a time"_ — or slice the task and add follow-up backlog entries, rather than enforcing a hard "≤10, stop at 11+" budget. Do not apply invented counting rules (e.g., "whitespace/renames free") not in the paper.
3. After making changes, validate with the project's test and linting commands.
4. If validation fails, fix the issues and re-validate.
5. Create the PR via **MCP using the paper's PR template** with an **emoji-prefixed title** (paper §2.3/Fig. 3: e.g., `✨`, `🧹`, `🐛` prefix) — missing detail added; do not use plain titles.
6. **Report after-state metrics** in the PR description: how many errors remain after the fix (e.g., "ruff — 48 → 42 errors"). This turns progress from narrative to quantitative. Include **backlog-excluded metrics** separately (paper §2.3: overall repo metrics not added to the P1–P4 backlog, reported only in the PR/description) — do not inject them into `pomona.md` priorities.
7. If the fix addresses a security issue, include the **CWE reference** and explain why the old code was unsafe — not just what changed, but why the old pattern is dangerous.

**Update the backlog (per §2.3):**

- Delete the completed task entry from `pomona.md`.
- Add any follow-up tasks discovered during the fix as new entries in the appropriate priority section.
- Do not mark tasks as `- [x]` or preserve completed entries in-file — the audit trail is `git log` / `git history` of `pomona.md` (paper §2.3: "Since the backlog is stored in the repository, there is no need to maintain a separate log... git history tracks changes"). Preserving `- [x]` entries in-file was a divergence: it changes `git diff` semantics (completed tasks appear as modified lines rather than deletions) and breaks deduplication logic (re-scan should dedupe against current open `- [ ]` entries only; a deleted entry correctly allows re-discovery if the underlying issue regresses, while a retained `- [x]` entry accumulates stale history in the working tree).

### Step 4: Loop

Return to Step 1 to check the backlog again. This creates the continuous improvement cycle.

## Design Rationale

**Why small changes?** Bloomberg's deployment achieved 88% acceptance (15/17 PRs merged) with a median time-to-close under 2 hours. 90% of surveyed engineers cited small diffs as the most appealing feature. Small changes reduce reviewer skepticism and cognitive load.

**Why the backlog?** A visible, prioritized backlog in the repository gives engineers control and transparency. They can see what's being worked on, add their own tasks, and adjust priorities. The backlog format also makes the system's behavior predictable and auditable.

**Why human-in-the-loop?** Engineers (especially senior ones with 10+ years experience) remain wary of fully automated agentic judgment. The PR format with mandatory human review builds trust while still delivering value. The paper's survey found 8/10 engineers wanted to try Pomona, but many wanted control over prioritization.

**Why parallel scanning sub-agents?** Different kinds of issues require different expertise. Running sub-agents in parallel is faster and each can focus on its domain. The aggregation step deduplicates and prioritizes, so the result is coherent.
