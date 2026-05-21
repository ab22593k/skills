---
name: building-software-effectively
description: "Evaluate, select, and integrate generative AI tools across the software development lifecycle — from code generation and UI design to testing, documentation, chatbots, and data analytics."
effort: medium
---

## Core mental models

### AI as Co-Pilot

**When to use:** Any task where you'd normally write code from scratch — generation, debugging, refactoring, or learning a new stack.
**The idea:** The AI produces a first draft; you review, refine, and own the result. Treat output like a junior engineer's pull request — never accept blindly.
**How to apply:** Prompt with full context (requirements, code style, constraints), review every diff, run tests, and use a second AI tool to double-check the first.
**Pitfalls:** Blind acceptance ("vibe coding") leads to subtle bugs, security holes, and unmaintainable code that takes longer to debug than writing from scratch.

### Tool Evaluation Framework

**When to use:** Assessing any new AI tool for your team or workflow.
**The idea:** Test every tool with the same prompt and criteria — code quality, UX, security, ease of integration. Rate 1–10 consistently across categories.
**How to apply:** Define your benchmark task (ideally representative of real work), run it once per tool, compare outputs, and score against a rubric before adopting.
**Pitfalls:** Surface-level demos hide hallucination, security issues, or "black box" calculation errors. Always verify AI outputs against ground truth.

### Browser vs IDE-Based Tooling

**When to use:** Deciding which class of AI tool fits your project size and workflow.
**The idea:** Browser tools (ChatGPT, Gemini) are convenient but require manual copy/paste of context and code. IDE tools (Cursor, Copilot, Windsurf) ingest your whole codebase and make changes in-place.
**How to apply:** Use browser tools for small scripts, one-off questions, and quick prototypes. Use IDE tools for production work on existing codebases. IDE tools win for any multi-file project.
**Pitfalls:** Browser tools become error-prone beyond ~10 files. IDE tools' agentic mode can silently break working code — always review before accepting.

### AI + Human Principle

**When to use:** Any process where AI automates a task that humans used to do alone — code review, testing, documentation, data analysis.
**The idea:** AI excels at repetitive grunt work (writing boilerplate, running regression tests, generating first drafts). Humans provide context, judgment, edge-case handling, and quality control.
**How to apply:** Let AI generate the first 80–90% of any deliverable. Spend the remaining time on review, refinement, and adding context-specific nuance.
**Pitfalls:** Assuming AI output is complete or correct. The black-box effect makes errors look convincing. Human review is not optional — it's the most critical step.

### Planning-Prompt-Review Workflow (Shopify Model)

**When to use:** Any feature implementation using AI code generation in a team setting.
**The idea:** Separate implementation into three phases — (1) plan and write a detailed prompt with functional context and style guidelines, (2) let the AI generate code, (3) double down on code review (developer reviews AI output, then peer reviews the PR).
**How to apply:** Write prompts as if instructing a colleague — include ticket context, coding standards, and edge cases. Review AI code with another AI tool, then have a human peer review before merge.
**Pitfalls:** Skipping the prompt phase leads to generic, off-target output. Skipping review leads to production bugs.

### Pareto Principle in QA

**When to use:** Prioritizing testing effort when resources are limited.
**The idea:** 20% of testing effort (defining workflows, mapping edge cases, UAT) creates 80% of value. The other 80% (writing and executing individual test cases) is grunt work AI can handle.
**How to apply:** Have humans define test scope and acceptance criteria. Use AI tools (Katalon, testRigor) to generate test scripts from natural language and self-heal when UI changes.
**Pitfalls:** Letting AI define test scope misses business-specific edge cases and ad-hoc exceptions that only humans know about.

### Historical Parallels Framework

**When to use:** Evaluating whether AI will replace or augment software engineering jobs.
**The idea:** ATMs didn't eliminate bank tellers — they lowered branch costs and grew the industry, creating more teller jobs. Excel killed bookkeeping clerks but created more accountant and analyst roles. Elevator operators disappeared because their role was too narrow.
**How to apply:** Roles focused on repetitive, closed-scope tasks (pure boilerplate coding) are at risk. Roles requiring judgment, architecture, review, and cross-functional collaboration will expand.
**Pitfalls:** Assuming all automation follows the same pattern. Job evolution depends on how narrow the automated task is and whether it enables new markets.

---

## How to use this skill

Load the skill with `load building-software-effectively` and reference the chapter index below to load specific chapters on demand:

- For tool evaluations (ratings, comparisons) → load the relevant chapter
- For quick reference tables → load `cheatsheet.md`
- For patterns and anti-patterns → load `patterns.md`
- For terminology → load `glossary.md`

---

## Chapter index

| #   | Title                                             | Topic                                                                                                        | Est. tokens |
| --- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ----------- |
| 1   | Code Generation and Autocompletion                | Browser vs IDE tools, ChatGPT, Gemini, Copilot, Cursor, Windsurf evaluation (2D array challenge, Kanban app) | ~1,000      |
| 2   | UI and UX Design                                  | Uizard, Bolt.new, Lovable, QoQo, Research Studio — design-to-code workflow compression                       | ~1,000      |
| 3   | Bug Detection and Code Review                     | Codacy, DeepCode, CodeRabbit — SQL injection, XSS, memory leaks, inefficient loops                           | ~1,000      |
| 4   | Automated Testing and QA                          | Katalon Studio, testRigor — AI test generation, self-healing tests, functional vs nonfunctional testing      | ~1,000      |
| 5   | Predictive Analytics and Performance Optimization | Julius, Akkio, ChatGPT for data analysis — retail dataset, customer segmentation, forecasting pitfalls       | ~1,000      |
| 6   | Documentation and Technical Writing               | Swimm, ChatGPT, Cursor, Scribe — API docs, internal docs, user guides, changelogs                            | ~1,000      |
| 7   | Chatbots and Virtual Assistants                   | Chatbase, Botpress, LangChain — no-code, drag-drop, code-based chatbot implementation                        | ~1,000      |
| 8   | Implementation Success Stories                    | Pieter Levels (vibe coding, flight sim in 3 hours), Shopify (enterprise AI adoption), historical parallels   | ~1,000      |

---

## Reference files

- **glossary.md** — All key terms alphabetized with chapter references
- **patterns.md** — Techniques, principles, and anti-patterns organized by type
- **cheatsheet.md** — Decision tables for tool selection, quick-reference rules
