## Choosing an AI code generation tool

| If you need                               | Use                | Why                                                |
| ----------------------------------------- | ------------------ | -------------------------------------------------- |
| Quick script, one-off question, prototype | ChatGPT / Gemini   | No install, fast, good for single-file tasks       |
| Production work on existing codebase      | Cursor             | Best IDE integration, full codebase context, 9/10  |
| Enterprise team, structured adoption      | Copilot            | Familiar IDE integration, 77k+ organizations, 8/10 |
| Maximum autonomy, agentic workflow        | Windsurf           | Cascade creates files/folders autonomously, 9/10   |
| UI design + working code from prompt      | Bolt.new / Lovable | Both 10/10, generate TypeScript frontend + preview |

## Choosing a code review tool

| If you need                               | Use        | Score |
| ----------------------------------------- | ---------- | ----- |
| Block PRs on security issues              | Codacy     | 8/10  |
| Deep explanation + open source references | DeepCode   | 6/10  |
| Fast PR comments, team-friendly           | CodeRabbit | 7/10  |

## Choosing a testing tool

| If you need                                      | Use            | Score |
| ------------------------------------------------ | -------------- | ----- |
| Enterprise, complex workflows, existing QA infra | Katalon Studio | 9/10  |
| Startup, rapid iteration, no testing infra       | testRigor      | 7/10  |

## Choosing a data analysis tool

| If you need                                            | Use     | Score |
| ------------------------------------------------------ | ------- | ----- |
| Chat-style analysis with context                       | Julius  | 7/10  |
| Quick charts, less contextualization needed            | Akkio   | 5/10  |
| General-purpose analysis (use local scripts to verify) | ChatGPT | 6/10  |

## Choosing a documentation tool

| If you need                               | Use     | Score |
| ----------------------------------------- | ------- | ----- |
| In-repo code documentation                | Swimm   | 6/10  |
| Best quality general-purpose docs         | ChatGPT | 7/10  |
| IDE-integrated, full codebase context     | Cursor  | 8/10  |
| Visual user guides from screen recordings | Scribe  | 5/10  |

## Choosing a chatbot builder

| If you need                                  | Use       | Score |
| -------------------------------------------- | --------- | ----- |
| Deploy a bot in 2 minutes, no coding         | Chatbase  | 9/10  |
| Visual workflow builder, more control        | Botpress  | 8/10  |
| Full control, agentic workflows, multi-agent | LangChain | 10/10 |

## Quick reference

- **Browser tools** for ≤10 files. **IDE tools** for everything larger.
- AI code must always be reviewed — by another AI tool AND a human.
- The best prompt includes: language + framework + requirements + coding standards + edge cases.
- AI-generated forecasts are unreliable — always verify with local scripts.
- Let AI generate 80-90% of any deliverable, then spend the remaining time on review.
- No-design tools (Bolt.new, Lovable) are mature enough for production frontend work.
- LangChain is the gold standard for LLM-powered application development.
- "Vibe coding" is fine for weekend prototypes. Use the Planning-Prompting-Review workflow for production.
