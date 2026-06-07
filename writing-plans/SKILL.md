---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Save plans to:** `.agents/plans/MM-DD-<feature-name>.md`

- (User preferences for plan location override this default)

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.
- **Efficient pre-work inspection:** When you need to understand an existing file, use `head -50`, `wc -l`, `grep -n 'class\|def \|function\|export'` to get the shape before deciding to read the full file. Include these inspection commands in your plan steps rather than bare "Read the file" instructions.
- **Hard limits in plan code:** Functions ≤ 80 lines, files ≤ 200 lines, nesting ≤ 3 levels. If plan code exceeds these, the task must include a decomposition step.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Bite-Sized Task Granularity

**Each step is one action:**

- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL:subagent-driven-development (recommended) or SUB-SKILL:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Architecture Decisions:**
- **Bounded contexts & layers:** [Which contexts/layers the work touches, and how they stay separated]
- **Naming conventions:** [Key domain names to use; note any banned generic names like `utils`/`helpers`/`common`]
- **Dependency rationale:** [For each custom component, why no existing library was chosen — or which libraries ARE used and why]

**Tech Stack:** [Key technologies/libraries]

**Test Strategy:**
- **Risk-based prioritization:** What to test first based on failure impact (critical paths, security, data integrity, core domain logic)
- **Oracle choice:** How to determine correct behavior — deterministic assertions, property-based testing, snapshot testing, or comparison against a reference implementation
- **Edge case areas:** Boundary conditions, error states, empty/null/zero inputs, concurrency, and failure modes specific to this feature

---
```

## Pre-Work: Dependency Audit

Before writing any task code, every plan MUST include a **Task 0: Dependency Audit**. This prevents NIH syndrome — building what already exists.

```markdown
### Task 0: Dependency Audit

- [ ] **Step 1: Search for existing solutions**

Check npm, Maven, PyPI, SaaS APIs, or whatever registry the tech stack uses for each major piece of functionality. For each, note what was found and whether it was adopted or rejected and why.

- [ ] **Step 2: Document decisions**

Save a dependency decision table:
| Need | Library/Solution Considered | Chosen? | Rationale |
|---|---|---|---|
| Auth | supabase-js, next-auth, custom | next-auth | Lightweight, fits Next.js App Router |
| State | Zustand, Redux, Jotai | Zustand | Minimal boilerplate, sufficient for this case |
```
Custom code is justified only for: specific domain logic, performance-critical paths, security-sensitive code, or when no suitable library exists after thorough evaluation.

## Task Structure

````markdown
### Task N: [Component Name]

**Layer:** `domain | use-case | adapter | infrastructure`

**Files:**

- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## No Placeholders

Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

## Remember

- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits

## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps. (Use `grep -c '^### Task'` to quickly check you have enough tasks for the spec's scope.)

**2. Placeholder scan:** Run `grep -in 'TBD\|TODO\|FIXME\|implement later\|placeholder'` on the plan file to catch red flags from "No Placeholders" above. Fix any matches.

**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

**4. Decomposition check:** Does any step's code exceed 80-line functions or 200-line files? If yes, flag for a split. Does any step introduce a `utils`/`helpers`/`common` module? If yes, replace with a domain-specific name.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.

## Efficient Implementation

The plan should guide implementers toward token-efficient execution. Embed these principles in your task steps:

- **Filter before you read:** Always `grep` for the relevant line/number/function before reading a file. A step that says "check existing tests" should include `grep -n 'class\|def ' tests/path/to/` rather than a bare Read.
- **Shape before detail:** Use `head -30`, `wc -l`, `ls -la`, and `grep -c` to size up unknowns before deciding what to read in full.
- **Bash for verification:** Test commands (`pytest`, `cargo test`, `npm test`) are already bash — keep them that way. Plan steps should also use `grep -c PASS` or `wc -l` for quick pass/fail checks before reading full test output.
- **Scope tool to task:** A step that inspects 3 files in unrelated parts of the codebase should be 3 separate steps, not one step with 3 parallel reads. Each step is bite-sized.
- **Progressive disclosure:** If a reference skill bundles large EXAMPLES.md files, the plan should reference them by line range rather than loading the full file (`grep -n 'pattern name' REFERENCES.md` then read only the matching section).

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `.agents/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**

- **REQUIRED SUB-SKILL:** Use SUB-subagent-driven-development
- Fresh subagent per task + two-stage review

**If Inline Execution chosen:**

- **REQUIRED SUB-SKILL:** Use executing-plans
- Batch execution with checkpoints for review
