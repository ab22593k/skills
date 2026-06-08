---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

The planning process is split into three phases — work through them in order.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Save plans to:** `.agents/plans/MM-DD-<feature-name>.md`

- (User preferences for plan location override this default)

---

## Phase 1: Deep Comprehension

Understand the problem before proposing a solution. A plan built on shallow reading produces the wrong thing, efficiently.

### Read the Spec — Extract the Map

Read the spec or requirements closely. Document what you find:

- **Explicit constraints:** Technology choices, performance targets, budget, timeline, compliance requirements. These are non-negotiable — plan around them, not against them.
- **Implicit needs:** What the spec assumes but doesn't say. Common examples: authentication/authorization for any multi-user feature, idempotency for payment flows, audit logging for data mutations, rate limiting for public endpoints.
- **Unstated assumptions:** Every spec leaves gaps. Identify them explicitly so the engineer can validate them.

### Identify the "Why"

Understand the business value the feature delivers. This guards against gold-plating:

- What problem does this solve for the user?
- What does success look like from the business side?
- **Equally important — what NOT to build:** If the spec is ambiguous about scope, document the boundary. Building 80% of a feature that delivers 100% of the value is better than building 120%.

### Define Success Criteria

Write down exactly how you will prove the feature works. These become the acceptance tests:

- **Functional criteria:** The happy-path behavior — "user can X and sees Y"
- **Non-functional criteria:** Performance threshold, max latency, concurrent users supported
- **Verification method:** Automated test, manual QA script, or monitoring dashboard

### Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

---

> **If the spec requires multi-source research (technology comparisons, regulatory requirements, competitive analysis):** Load the deep-research skill → `skill:deep-research` before starting Phase 2. It produces a structured research report you can reference directly in the Architecture Decisions and Tech Stack sections of the plan header.

## Phase 2: Architecture & Data Flow

Design the shape of the solution. Decisions made here ripple through every task — get them right before writing code.

### Map the Data Lifecycle

Sketch how data enters, changes, and leaves the system. For each data entity:

- **Source:** Where does it originate? (user input, webhook, cron, upstream service)
- **Transformation:** What processing happens? (validation, enrichment, aggregation)
- **Storage:** Where does it live? (DB table, cache, blob storage, message queue)
- **Egress:** When and how is it consumed or emitted? (API response, event, export file)

### Design the Schema

Define database tables, key relationships, and data types early. Include:

- Table/collection names and columns/fields with types
- Primary and foreign key relationships
- Indexes needed for query patterns
- Migration strategy (new tables vs. altering existing ones)

### Choose API Contracts

Write out the JSON payloads for endpoints before coding them. This surfaces mismatches between frontend and backend expectations early:

- Request body shape, required vs. optional fields, validation rules
- Response shape, pagination format, error response structure
- Status codes for each outcome (200, 201, 400, 404, 409, 500)

### File Structure

Map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.
- **Efficient pre-work inspection:** When you need to understand an existing file, use `head -50`, `wc -l`, `grep -n 'class\|def \|function\|export'` to get the shape before deciding to read the full file. Include these inspection commands in your plan steps rather than bare "Read the file" instructions.
- **Hard limits in plan code:** Functions ≤ 80 lines, files ≤ 200 lines, nesting ≤ 3 levels. If plan code exceeds these, the task must include a decomposition step.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

### Pre-Work: Dependency Audit

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

### Plan Document Header

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

### Bite-Sized Task Granularity

**Each step is one action:**

- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

---

## Phase 3: Risk & Edge Case Analysis

Anticipate what breaks before it breaks. Every plan looks good on the happy path — the quality is in how it handles the unhappy ones.

### Identify Failure Points

Plan for what happens when things go wrong. For every operation in the plan, consider:

- **Network failures:** API call timeout, dropped connection, DNS resolution failure. How does the system retry or degrade?
- **Slow queries:** What happens when a DB query takes 10x longer than expected? Does the endpoint have a timeout? Can it be paginated or cached?
- **Bad user input:** Malformed JSON, excessively large payloads, injection attempts. Where is validation enforced? (Prefer at the boundary, not deep in business logic.)
- **Downstream outages:** The service your feature depends on is unreachable. Does it fail open (graceful degradation) or fail closed?

### List the Edge Cases

Define behavior for the boundaries of your input space:

- **Empty states:** What does the UI show when a list has zero items? When a query returns no results?
- **Null / optional values:** Every nullable field in the schema — what does the system do with null? Crash? Skip? Show a placeholder?
- **Extreme limits:** Max-length strings, max-page-size pagination, concurrent users at the same moment, file uploads at the size limit.
- **Duplicate / conflicting data:** Idempotency keys for writes, unique constraint violations, concurrent updates to the same row.

### Plan Data Migration

If the feature changes existing data structures, define the migration before coding the feature:

- **Schema changes:** New tables, altered columns, backfills — order them so there is no window where the old and new code conflict.
- **Existing data:** How will current production data be transformed to fit the new schema? Is a one-time migration script needed, or can it be done lazily?
- **Rollback strategy:** How do you undo the migration if the deployment is rolled back? Forward-only migrations are a trap.

### Task Structure

```markdown
### Task N: [Component Name]

**Layer:** `domain | use-case | adapter | infrastructure`
**Files:**

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Write minimal implementation**
- [ ] **Step 4: Run test to verify it passes**
```

### No Placeholders

Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

### Remember

- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits

### Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps. (Use `grep -c '^### Task'` to quickly check you have enough tasks for the spec's scope.)

**2. Placeholder scan:** Run `grep -in 'TBD\|TODO\|FIXME\|implement later\|placeholder'` on the plan file to catch red flags from "No Placeholders" above. Fix any matches.

**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

**4. Decomposition check:** Does any step's code exceed 80-line functions or 200-line files? If yes, flag for a split. Does any step introduce a `utils`/`helpers`/`common` module? If yes, replace with a domain-specific name.

**5. Phase coverage:** Does every question raised in Phase 1 (success criteria, implicit needs) and Phase 3 (failure points, edge cases) have a corresponding task? If not, add it.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.

### Efficient Implementation

The plan should guide implementers toward token-efficient execution. Embed these principles in your task steps:

- **Filter before you read:** Always `grep` for the relevant line/number/function before reading a file. A step that says "check existing tests" should include `grep -n 'class\|def ' tests/path/to/` rather than a bare Read.
- **Shape before detail:** Use `head -30`, `wc -l`, `ls -la`, and `grep -c` to size up unknowns before deciding what to read in full.
- **Bash for verification:** Test commands (`pytest`, `cargo test`, `npm test`) are already bash — keep them that way. Plan steps should also use `grep -c PASS` or `wc -l` for quick pass/fail checks before reading full test output.
- **Scope tool to task:** A step that inspects 3 files in unrelated parts of the codebase should be 3 separate steps, not one step with 3 parallel reads. Each step is bite-sized.
- **Progressive disclosure:** If a reference skill bundles large EXAMPLES.md files, the plan should reference them by line range rather than loading the full file (`grep -n 'pattern name' REFERENCES.md` then read only the matching section).

---

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `.agents/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**

- **REQUIRED SUB-SKILL:** Load skill → `skill:subagent-driven-development` with Fresh subagent per task + two-stage review

**If Inline Execution chosen:**

- **REQUIRED SUB-SKILL:** Load skill → `skill:executing-plans` and Batch execution with checkpoints for review
