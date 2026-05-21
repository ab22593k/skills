# Implementation Success Stories

## Core concepts

- **Vibe coding** (coined by Andrej Karpathy): fully delegating code writing to AI, accepting all suggestions without reading diffs, and copy-pasting errors back to the AI until they go away. Works for throwaway weekend projects but is dangerous for production code.
- Pieter Levels built a browser-based flight simulator in 3 hours using Cursor — 5,000 concurrent players, $87k ad revenue in 17 days. This proves AI can compress MVP development from months to hours for solo entrepreneurs.
- Shopify's Samuel Path describes a disciplined workflow: invest heavily in prompting (include full context + coding standards), let AI generate code, then double down on code review (AI review + human peer review).

## Frameworks introduced

**Vibe coding** — Karpathy's term for full surrender to AI code generation. "Accept All always, I don't read diffs anymore." Characterized by: no existing codebase, no existing business (low cost of failure), solo work (all context in one brain). Antidote: vibe debugging — spending more time fixing AI bugs than you would writing the code yourself.

**Planning-Prompting-Review workflow (Shopify)** — Three-phase process: (1) write detailed prompts with functional context and implementation guidelines, (2) let AI generate code, (3) review AI output with another tool + human peer review. This is the disciplined alternative to vibe coding for production teams.

## Key techniques

**Architect, not draftsman:** Senior engineers shift from writing code to designing architectures, discussing trade-offs with AI, and reviewing generated code. Jeff Tunnell's lead coder stopped writing code entirely but the project improved faster than ever.

**AI experimentation team:** Shopify created a dedicated team to evaluate every new AI tool, test for productivity gains and data protection compliance, then roll out approved tools company-wide.

## Historical parallels

| Innovation | Jobs eliminated | Jobs created/expanded |
|-----------|----------------|----------------------|
| ATMs (1970s) | None (teller jobs grew) | More bank branches |
| Elevator buttons | Elevator operators | None (narrow role) |
| Excel (1980s) | Bookkeeping clerks | Accountants, analysts, financial managers |
| AI coding tools | Pure boilerplate coders | Prompt engineers, AI integration specialists, code reviewers |

## Connection to other chapters

Applies all frameworks from Chapters 1-7 to real-world scenarios. The AI + Human principle, Planning-Prompt-Review workflow, and evaluation methodology converge here. The historical parallels provide the book's final thesis: AI will not replace software engineers — it will evolve the role toward architecture, review, and strategic thinking.
