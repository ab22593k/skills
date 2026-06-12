# Chapter 6: Composing Effective Code Review Comments

## Core Concepts

- **Focus on the Code, Not the Developer:** Comments should criticize the technical implementation and suggest solutions, never attack the author's ability.
- **Objective Justification:** Every change request should explain _why_ it is necessary, citing style guides, security, performance, or correct logic.
- **Clarity of Intent:** Reviewers must clearly communicate if a comment is a critical blocker (`[MUST]`) or an optional improvement (`[COULD]`).

## Frameworks Introduced

- **The 5P Comment Process:**
  - **Pause:** Stop before commenting to collect your thoughts.
  - **Ponder:** Ask _why_ the change is needed and if it is objective.
  - **Pass:** Don't comment if it's purely personal preference or subjective.
  - **Propose:** Leave a clear, polite comment with objective reasoning.
  - **Postpone:** Note out-of-scope ideas for later tickets or discussions.
- **Maintainable Middle Ground (MMG) Exchange:** A 5-step dispute resolution workflow for resolving opposing viewpoints on code.
- **Comment Signal Framework:** Using explicit prefixes like `[MUST]`, `[SHOULD]`, `[COULD]`, and `[NIT]` to classify review comments.

## Key Techniques

- ** Empathetic Writing Style:** Framing comments with questions rather than absolute demands (e.g. "What do you think about..." vs. "Change this to...").
- **Leaving Clear Action Items:** Providing concrete code examples or refactoring snippets in comments.

## Connection to Other Chapters

- Constructive comments keep **psychological safety high (Chapter 1)** and prevent comments from becoming **lazy or mean (Chapter 7)**, keeping delays low.

## Technical Code Examples

### Comment Refactoring (Empathic & Objective)

```markdown
❌ BAD NITPICK (Subjective & demanding):
"I hate this variable name `df`. Change it to `data_frame`. It looks lazy."

✅ GOOD NITPICK (Objective & using comment signals):
"[NIT] To stay consistent with our TWA coding convention (Section 3.2),
would you mind renaming the variable `df` to `billing_data_frame`?
This makes the context clearer for future developers reading this module."
```

## Reference Tables

### Comment Signaling (MoSCoW Rules)

| Tag            | Priority             | Meaning                                                          | Example                                                                                         |
| -------------- | -------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **`[MUST]`**   | Blocker              | Critical logical flaw, security vulnerability, or TWA violation. | `[MUST] This SQL query is vulnerable to injection. We need to use parametrized inputs...`       |
| **`[SHOULD]`** | Highly Recommended   | Significant code quality, readability, or performance concern.   | `[SHOULD] Defining this helper as a static function will prevent unnecessary instantiation...`  |
| **`[COULD]`**  | Optional Improvement | Nice-to-have suggestion or minor optimization.                   | `[COULD] We could extract this inline function to clean up the readability of the main loop...` |
| **`[NIT]`**    | Cosmetic/Minor       | Simple formatting issue or minor typo that doesn't block merge.  | `[NIT] Typo in docstring: "calculate" is misspelled as "calclate".`                             |
