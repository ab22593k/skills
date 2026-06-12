---
name: looks-good-to-me
description: "Applies Adrienne Braganza's Constructive Code Reviews framework to build healthy team practices, write empathetic comments, automate nits, eliminate bottlenecks, and pair reviews with pair/mob programming and AI. Use whenever the user asks about code review process, PR feedback, review delays, team working agreements, automation in reviews, review comments, pair programming, or code review best practices."
effort: medium
---

# Constructive Code Reviews

Welcome to the **Constructive Code Reviews** skill. This skill is a structured, actionable knowledge base derived from Adrienne Braganza's book _Looks Good to Me: Constructive Code Reviews_ (Manning, 2025). It is designed to help software engineering teams transform their pull request processes from friction-filled gatekeeping into collaborative learning systems that promote psychological safety, high code quality, and shared ownership.

---

## How to Use This Skill

Your job when this skill triggers: the user has a code-review-related question or problem. Navigate to the right content quickly.

**Decision flow:**

1. If the user asks about a **specific term** (e.g., "what is review creep?"), load **[glossary.md](glossary.md)** first.
2. If the user asks **"how do I handle X situation"** (e.g., "reviews are taking too long"), use the **Topic Lookup** table below to find the right chapter, load it, and follow its guidance.
3. If the user asks about a **specific technique or anti-pattern** (e.g., "what is rubber stamping?"), load **[patterns.md](patterns.md)** for a structured catalog.
4. If the user wants a **quick decision or checklist** (e.g., "what SLA should we set?"), load **[cheatsheet.md](cheatsheet.md)**.
5. If the user's question is **broad or open-ended**, load this SKILL.md for the overview and the core frameworks, then drill into the relevant chapter.

When you load a chapter, also check its **Connection to Other Chapters** section and the **Chapter Dependency Map** below — related chapters often contain complementary guidance you should load too.

---

## Quick Reference

### Topic Lookup

| When the user asks about...                                    | Primary chapter                                    | Also load                                                                                                                                                  |
| -------------------------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Why code reviews matter / team benefits / psychological safety | [ch01](chapters/ch01-constructive-code-reviews.md) | Glossary                                                                                                                                                   |
| How PRs work / review workflows / roles & responsibilities     | [ch02](chapters/ch02-constructive-code-reviews.md) | Cheatsheet                                                                                                                                                 |
| Setting up a review process from scratch / phased rollout      | [ch03](chapters/ch03-constructive-code-reviews.md) | [ch04](chapters/ch04-constructive-code-reviews.md)                                                                                                         |
| Team Working Agreement / SLAs / codifying team norms           | [ch04](chapters/ch04-constructive-code-reviews.md) | Cheatsheet, [ch05](chapters/ch05-constructive-code-reviews.md)                                                                                             |
| Automating linting / CI checks / removing human friction       | [ch05](chapters/ch05-constructive-code-reviews.md) | [ch04](chapters/ch04-constructive-code-reviews.md)                                                                                                         |
| Writing better review comments / being empathetic / 5P process | [ch06](chapters/ch06-constructive-code-reviews.md) | Glossary, Patterns                                                                                                                                         |
| Toxic reviews / nitpicking / review creep / ego clashes        | [ch07](chapters/ch07-constructive-code-reviews.md) | [ch05](chapters/ch05-constructive-code-reviews.md), [ch06](chapters/ch06-constructive-code-reviews.md)                                                     |
| Slow reviews / reducing delays / unblocking PRs                | [ch08](chapters/ch08-constructive-code-reviews.md) | [ch04](chapters/ch04-constructive-code-reviews.md), [ch11](chapters/ch11-constructive-code-reviews.md), [ch12](chapters/ch12-constructive-code-reviews.md) |
| Loopholes / rubber-stamping / process gaps                     | [ch09](chapters/ch09-constructive-code-reviews.md) | [ch10](chapters/ch10-constructive-code-reviews.md)                                                                                                         |
| Emergency hotfixes / urgent production issues                  | [ch10](chapters/ch10-constructive-code-reviews.md) | [ch09](chapters/ch09-constructive-code-reviews.md), Cheatsheet                                                                                             |
| Pair programming as review / driver-navigator                  | [ch11](chapters/ch11-constructive-code-reviews.md) | [ch08](chapters/ch08-constructive-code-reviews.md), [ch12](chapters/ch12-constructive-code-reviews.md)                                                     |
| Mob programming / collective code ownership                    | [ch12](chapters/ch12-constructive-code-reviews.md) | [ch05](chapters/ch05-constructive-code-reviews.md), [ch11](chapters/ch11-constructive-code-reviews.md)                                                     |
| AI-assisted reviews / human-AI review split                    | [ch13](chapters/ch13-constructive-code-reviews.md) | [ch05](chapters/ch05-constructive-code-reviews.md)                                                                                                         |

### Common Situations

| Situation                                               | What to do                                                                 | Reference                                                                                              |
| ------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| "My PR has been sitting for 3 days with no review"      | Check SLAs, trigger escalation, rotate reviewers                           | [ch08](chapters/ch08-constructive-code-reviews.md), Cheatsheet SLA matrix                              |
| "A reviewer is demanding unrelated refactoring"         | Politely decline, create follow-up ticket, enforce scope                   | [ch07](chapters/ch07-constructive-code-reviews.md)                                                     |
| "We have no review process — where do we start?"        | Phase-based setup: align, setup tools, codify rules                        | [ch03](chapters/ch03-constructive-code-reviews.md)                                                     |
| "Our senior engineer is the bottleneck for all reviews" | Reviewer rotations, shadowing, distribute ownership                        | [ch08](chapters/ch08-constructive-code-reviews.md), [ch11](chapters/ch11-constructive-code-reviews.md) |
| "People approve without actually reading the code"      | Loophole audit, enforce 2-approver rule, automated checks                  | [ch09](chapters/ch09-constructive-code-reviews.md), [ch05](chapters/ch05-constructive-code-reviews.md) |
| "We have a production outage — can I skip review?"      | Follow the Emergency Playbook, not ad-hoc bypass                           | [ch10](chapters/ch10-constructive-code-reviews.md)                                                     |
| "Review comments are getting personal and harsh"        | Apply 5P process, focus on code not person, reset culture                  | [ch06](chapters/ch06-constructive-code-reviews.md), [ch07](chapters/ch07-constructive-code-reviews.md) |
| "Should we use AI to review our code?"                  | AI as first responder — nits and syntax; humans own logic and architecture | [ch13](chapters/ch13-constructive-code-reviews.md)                                                     |

---

## Core Mental Models & Frameworks

### 1. The 5P Comment Process

- **When to use:** Whenever a reviewer is about to leave a comment suggesting a code change.
- **The idea:** Prevents subjective debates and "review creep" by forcing self-reflection before commenting. It asks if a suggestion is truly necessary, justifiable with facts, and timely.
- **How to apply:**
  1. **Pause:** Stop and take a breath before writing a comment.
  2. **Ponder:** Walk through the rational justification. Is it necessary _now_? Is it objective?
  3. **Pass / Propose / Postpone:** Decide on one of these options:
     - **Pass:** If you cannot objectively justify it, do _not_ leave the comment.
     - **Propose:** If valid, write a polite comment explaining the _why_ and referencing objective guidelines.
     - **Postpone:** If useful but out of scope, take a note to discuss offline or in a future planning ticket.
- **Pitfall:** Reviewers skip the "Pause & Ponder" steps and write knee-jerk subjective opinions that destroy trust.

### 2. The Maintainable Middle Ground (MMG) Exchange

- **When to use:** When the author and reviewer have conflicting "objective" viewpoints on how code should be structured.
- **The idea:** A collaborative 5-step dispute resolution framework aimed at finding a maintainable compromise, rather than letting ego dictate the solution.
- **How to apply:**
  1. Keep the tone professional and respectful.
  2. Acknowledge the reviewer's concern and open a constructive discussion.
  3. Aim to understand each other's rationales.
  4. If small modifications fail, collaboratively search for a middle ground.
  5. If still stuck, escalate to the broader team for consensus.
- **Pitfall:** Treating the debate as a win/lose battle of egos rather than a search for a shared maintainable solution.

### 3. The Team Working Agreement (TWA) as a Living Document

- **When to use:** Defining a team's review culture, coding styles, response expectations, and PR sizing.
- **The idea:** Codifies code review norms and expectations in a shared document. Crucially, the agreement is itself code—stored in Git and updated via pull requests—making it a "living" representation of team alignment.
- **How to apply:** Draft a TWA covering PR sizing (e.g., max 300 lines), response SLAs (e.g., reviews within 24 hours), style rules, and template standards. Modify the TWA over time through team retrospectives.
- **Pitfall:** Leaving the document static and unreferenced, letting subjective debates creep back into PRs.

### 4. The Emergency Playbook Bypass

- **When to use:** Urgent production issues (e.g., severe outages or critical security vulnerabilities) that cannot wait for the standard code review pipeline.
- **The idea:** A formal, documented procedure for bypassing the standard review process. Bypassing is treated as an exceptional event that requires authorization, notification, and a mandatory post-merge review within 24 hours.
- **How to apply:** Trigger the playbook via authorized personnel, merge the emergency hotfix, and immediately start post-incident procedures including a retrospective and TWA updates to prevent future occurrences.
- **Pitfall:** Using the bypass path for non-emergencies due to poor planning or shipping pressure.

---

## Chapter Dependency Map

When you load a chapter, also consider loading its dependencies for complete context:

| If you load...                | Also load these for complementary guidance                               |
| ----------------------------- | ------------------------------------------------------------------------ |
| **Ch01** (Significance)       | — (foundational, few dependencies)                                       |
| **Ch02** (Dissecting Review)  | — (foundational)                                                         |
| **Ch03** (Building Process)   | Ch04 (TWA codifies process rules)                                        |
| **Ch04** (TWA)                | Ch05 (automate TWA rules), Ch08 (SLAs reduce delays)                     |
| **Ch05** (Automation)         | Ch04 (TWA provides rules to automate)                                    |
| **Ch06** (Comments)           | Ch07 (toxic patterns to avoid), Glossary (comment signals)               |
| **Ch07** (How Reviews Suck)   | Ch05 (automation eliminates nitpicking), Ch06 (5P prevents creep)        |
| **Ch08** (Reducing Delays)    | Ch04 (SLA baseline), Ch11, Ch12 (pair/mob reduce bottlenecks)            |
| **Ch09** (Loopholes)          | Ch10 (formal bypass path)                                                |
| **Ch10** (Emergency Playbook) | Ch09 (prevent abuse), Cheatsheet (checklist)                             |
| **Ch11** (Pair Programming)   | Ch08 (eliminates delays), Ch12 (mobbing for complex work)                |
| **Ch12** (Mob Programming)    | Ch05 (automation frees mob focus), Ch11 (pairing as lighter alternative) |
| **Ch13** (AI)                 | Ch05 (AI is advanced automation layer)                                   |

---

## Chapter Index

| Chapter   | Title                             | Key Topic                                                | Target File                                                                     | Est. Tokens |
| --------- | --------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------- | ----------- |
| **Ch 01** | The Significance of Code Reviews  | Benefits, collective ownership, psych safety             | [ch01-constructive-code-reviews.md](chapters/ch01-constructive-code-reviews.md) | ~1,000      |
| **Ch 02** | Dissecting the Code Review        | Review systems, workflow, PR parts, roles                | [ch02-constructive-code-reviews.md](chapters/ch02-constructive-code-reviews.md) | ~1,100      |
| **Ch 03** | Building Your First Process       | Phase-based setup, goals, workflows, rules               | [ch03-constructive-code-reviews.md](chapters/ch03-constructive-code-reviews.md) | ~1,100      |
| **Ch 04** | The Team Working Agreement        | Codifying rules, SLAs, styling, Git TWAs                 | [ch04-constructive-code-reviews.md](chapters/ch04-constructive-code-reviews.md) | ~1,200      |
| **Ch 05** | The Advantages of Automation      | Linting, formatters, automated CI checks, objectivity    | [ch05-constructive-code-reviews.md](chapters/ch05-constructive-code-reviews.md) | ~1,000      |
| **Ch 06** | Composing Effective Comments      | Empathetic comment writing, 5P, MMG Exchange             | [ch06-constructive-code-reviews.md](chapters/ch06-constructive-code-reviews.md) | ~1,200      |
| **Ch 07** | How Code Reviews Can Suck         | Nitpicking, review creep, delayed loops, friction        | [ch07-constructive-code-reviews.md](chapters/ch07-constructive-code-reviews.md) | ~1,000      |
| **Ch 08** | Decreasing Review Delays          | Review bottlenecks, taking chats offline, ticket sizing  | [ch08-constructive-code-reviews.md](chapters/ch08-constructive-code-reviews.md) | ~1,100      |
| **Ch 09** | Eliminating Process Loopholes     | Merging around reviews, rubber stamping, bypass auditing | [ch09-constructive-code-reviews.md](chapters/ch09-constructive-code-reviews.md) | ~1,100      |
| **Ch 10** | The Emergency Playbook            | Hotfixes, bypass authorization, post-incident reviews    | [ch10-constructive-code-reviews.md](chapters/ch10-constructive-code-reviews.md) | ~1,100      |
| **Ch 11** | Code Reviews and Pair Programming | Drivers, Navigators, pairing vs. reviewing, hybrid flows | [ch11-constructive-code-reviews.md](chapters/ch11-constructive-code-reviews.md) | ~1,000      |
| **Ch 12** | Code Reviews and Mob Programming  | Mobbing, knowledge sharing, "agree then split" approach  | [ch12-constructive-code-reviews.md](chapters/ch12-constructive-code-reviews.md) | ~1,000      |
| **Ch 13** | Code Reviews and AI               | AI benefits, limitations, tools, Human-AI pairing        | [ch13-constructive-code-reviews.md](chapters/ch13-constructive-code-reviews.md) | ~1,000      |

---

## Reference Files

- **[glossary.md](glossary.md):** Alphabetical guide to key terms (e.g., SLAs, review creep, MMG Exchange, runbooks). Load when the user asks "what is X?"
- **[patterns.md](patterns.md):** Structured techniques, principles, and anti-patterns. Load when the user asks about a specific technique or wants a catalog of what to do / what to avoid.
- **[cheatsheet.md](cheatsheet.md):** Decision tables, checklists, and quick references. Load when the user wants a decision guide, SLA matrix, or step-by-step checklist.
