# Code Generation and Autocompletion

## Core concepts

- AI tools fall into two categories: **browser-based** (ChatGPT, Gemini) and **IDE-based** (Copilot, Cursor, Windsurf). IDE tools win for multi-file projects because they ingest the whole codebase as context.
- AI-generated code must always be reviewed. Treat it like a junior engineer's PR — test, validate, and own the result.
- Interview-style algorithmic challenges are trivial for current models. The real differentiator is how tools handle multi-file application generation with dependencies, databases, and API integrations.

## Frameworks introduced

**Browser vs IDE categorization** — Browser tools require manual context sharing (copy/paste), limiting them to single-file tasks. IDE tools embed in your development environment and can create/modify files directly. This is the primary axis for tool selection.

**Agentic vs Assisted modes** — Windsurf's Cascade acts as an independent agent creating folders, files, and making changes autonomously. Cursor offers both chat and optional agentic mode. Copilot stays closer to assisted autocomplete+chat. More autonomy means more productivity but also more risk of breaking working code.

## Key techniques

**Prompt engineering for code generation:** Include language, framework, requirements, coding standards, and edge cases in your prompt. Treat the prompt as executable specifications.

**Review workflow:** Always review AI-generated diffs before accepting. Run test suites covering happy path, edge cases, and error states. Use a second AI tool to review the first's output.

## Code examples

The book tests tools on two challenges: (1) a 2D array rectangle-finding algorithm, (2) a full Kanban to-do app with OpenAI API integration, React frontend, and Express backend. All tools solved challenge 1 perfectly (10/10). Challenge 2 exposed differences: ChatGPT 8/10, Gemini 4/10 (broken UI, hardcoded API key), Copilot 8/10, Cursor 9/10, Windsurf 9/10.

## Connection to other chapters

Sets up the evaluation methodology (same prompt, same criteria, 1-10 scale) used throughout the book. The AI + Human review principle established here applies to every subsequent chapter.
