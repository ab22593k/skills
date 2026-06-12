# Chapter 13: Code Reviews and AI

## Core Concepts

- **AI as the First Responder:** Use AI tools to do the first pass on a PR (e.g., generating descriptions, running initial security checks, checking documentation).
- **Logical Limitations:** AI is incapable of analyzing complex business rules, architectural patterns, alignment with product goals, or team dynamics.
- **Avoiding Blind Trust:** Blindly accepting AI suggestions in code reviews creates a dangerous new form of rubber-stamping.

## Frameworks Introduced

- **The Human-AI Code Review Paradigm:** A split-responsibility framework:
  - **AI Check:** Syntactic nits, basic edge cases, docstring verification, automated test generation.
  - **Human Approval:** Domain architectural alignment, business logic correctness, team safety reviews.

## Key Techniques

- **AI-Assisted PR Creation:** Prompting models to generate detailed PR titles and summaries based on Git diffs.
- **Prompting for Review Feedback:** Instructing LLMs to focus strictly on technical correctness, requesting refactoring suggestions with explanations.

## Connection to Other Chapters

- AI-driven style and documentation checking serves as an advanced layer of **automation (Chapter 5)**, supporting the **TWA rules (Chapter 4)**.

## Technical Code Examples

### AI Review Assistant Prompt System

```markdown
System Prompt for AI Review Assistant:
"You are a constructive code reviewer assisting our software team.
Review the attached git diff and generate feedback following these rules:

1. Ignore formatting, whitespace, or bracket spacing (handled by formatters).
2. Look for logical flaws, resource leaks, or missing edge cases.
3. Keep comments polite and objective. Focus on the code, not the person.
4. Categorize feedback using [MUST], [SHOULD], [COULD] comment signals.
5. Provide code refactoring snippets with explanations."
```

## Reference Tables

### Human vs. AI Code Review Competencies

| Evaluation Dimension          | AI Reviewer                                      | Human Reviewer                                 |
| ----------------------------- | ------------------------------------------------ | ---------------------------------------------- |
| **Formatting & Syntax**       | ✅ Excellent (instant and objective)             | ❌ Poor (subjective, prone to nitpicking)      |
| **Typo / Typological checks** | ✅ Excellent (finds typos in variables/comments) | ❌ Moderate (can easily miss nits)             |
| **Complex Business Logic**    | ❌ Poor (hallucinates domain rules)              | ✅ Excellent (understands target requirements) |
| **Architectural Alignment**   | ❌ Moderate (local checks only)                  | ✅ Excellent (understands global patterns)     |
| **Psychological Safety**      | ❌ None (blind inputs)                           | ✅ Critical (crafts empathetic tone)           |
