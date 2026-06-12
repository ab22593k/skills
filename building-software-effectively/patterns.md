## AI as Co-Pilot

**Type:** principle
**Context:** Any coding task — generation, debugging, refactoring, learning.
**Solution:** Let AI produce a first draft. Review, test, and own every line. Never accept output without verification.
**Consequences:** Dramatic productivity gains when used correctly. Subtle bugs and security holes when used carelessly. The skill shifts from writing code to reviewing code.
**Related:** Planning-Prompting-Review workflow, Vibe coding (anti-pattern)

## Self-Healing Tests

**Type:** technique
**Context:** Maintaining automated tests as the application evolves.
**Solution:** Use AI testing tools (Katalon, testRigor) that automatically detect UI/code changes and update test scripts accordingly.
**Consequences:** Eliminates the common pattern of tests becoming deprecated and commented out. Reduces QA maintenance burden significantly.
**Related:** Pareto Principle in QA

## Tool Evaluation Methodology

**Type:** technique
**Context:** Assessing any new AI tool for adoption.
**Solution:** Define a representative benchmark task. Run it once per tool with the same prompt. Score on a 1-10 scale for code quality, UX, security, and ease of integration. Compare outputs against ground truth.
**Consequences:** Objective comparison across tools. Reveals hallucination and black-box issues that surface-level demos hide.
**Related:** Black box effect (anti-pattern)

## RAG Chatbot Architecture

**Type:** technique
**Context:** Building a chatbot that answers questions about specific data.
**Solution:** Upload training data (CSV, documents, spreadsheets) as a knowledge base. The AI retrieves relevant context from this data to ground its answers, reducing hallucination.
**Consequences:** Produces accurate, domain-specific answers with minimal setup. Output quality still depends on the underlying LLM.
**Related:** LangChain, Chatbase

## Planning-Prompting-Review Workflow

**Type:** technique
**Context:** Using AI code generation in a team setting with production requirements.
**Solution:** (1) Write detailed prompts with functional context, coding standards, and edge cases. (2) Let AI generate code. (3) Review AI output with a second AI tool, then have a human peer review before merge.
**Consequences:** Higher quality code, fewer regressions, clear separation between design and implementation. Requires upfront investment in prompt writing.
**Related:** AI as Co-Pilot principle, Vibe coding (anti-pattern)

## Black Box Effect

**Type:** anti-pattern
**Context:** Using AI tools for data analysis, forecasting, or any task where the reasoning process is opaque.
**Solution:** Always run local scripts to verify AI-calculated figures. Treat AI insights as hypotheses to validate, not conclusions to act on. Never rely on a single AI tool's output for business decisions.
**Consequences:** Can lead to flawed business decisions based on convincing-looking but incorrect analysis.
**Related:** Tool Evaluation Methodology

## Vibe Coding

**Type:** anti-pattern
**Context:** Using AI code generation on production codebases or team projects.
**Solution:** Never "Accept All" without reviewing diffs. Never copy-paste error messages back without understanding the root cause. Always run tests, review changes, and have a human peer review the PR.
**Consequences:** Vibe debugging — spending more time fixing AI-generated bugs than writing the code manually would have taken. Unmaintainable codebases with random dependencies and missing functionality.
**Related:** AI as Co-Pilot (positive version), Planning-Prompting-Review workflow

## Dependency Sprawl

**Type:** anti-pattern
**Context:** Agentic AI tools choosing libraries and dependencies autonomously.
**Solution:** Restrict AI tools to approved libraries. When an agentic tool (like Windsurf) adds problematic dependencies, prompt it to remove them and restart. Prefer minimal dependencies and in-memory storage for prototypes.
**Consequences:** Unnecessary complexity, broken builds, version conflicts. The AI may spend more time debugging library issues than solving the actual problem.
**Related:** Vibe coding

## Skipping Human Code Review

**Type:** anti-pattern
**Context:** Teams using AI code-review tools.
**Solution:** Never skip human code review because AI already reviewed the code. AI misses context-specific issues, business logic gaps, and nuanced domain knowledge that senior engineers catch. Use AI to augment, not replace, human reviewers.
**Consequences:** Context-specific bugs slip to production. Team knowledge sharing decreases. Junior engineers lose learning opportunities.
**Related:** AI as Co-Pilot principle
