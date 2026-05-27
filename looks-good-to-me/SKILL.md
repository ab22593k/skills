---
name: looks-good-to-me
description: "Applies Adrienne Braganza's Constructive Code Reviews framework to build healthy team practices, write empathetic comments, automate nits, eliminate bottlenecks, and pair reviews with pair/mob programming and AI."
effort: medium
---

# Constructive Code Reviews

Welcome to the **Constructive Code Reviews** skill. This skill is a structured, actionable knowledge base derived from Adrienne Braganza's book _Looks Good to Me: Constructive Code Reviews_ (Manning, 2025). It is designed to help software engineering teams transform their pull request processes from friction-filled gatekeeping into collaborative learning systems that promote psychological safety, high code quality, and shared ownership.

---

## 🧠 Core Mental Models & Frameworks

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

## 🚀 How to Use This Skill

This skill is designed for on-demand loading. You can read this index to locate a specific topic or load a single chapter file for deeper contextual knowledge.

- **Load Core Knowledge:** Type `/[slug]` to read this file and load the main mental models.
- **Topic-Based Queries:** Ask questions like `/[slug] how do I resolve a comment disagreement?` or `/[slug] emergency process`. Claude will map your query to the appropriate chapter or cheatsheet.
- **Direct Chapter Load:** Load individual chapters directly by typing `/[slug] ch01` or `/[slug] ch10`.

---

## 📖 Chapter Index

| Chapter   | Title                             | Key Topic                                                | Target File                                                                          | Est. Tokens |
| --------- | --------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------- |
| **Ch 01** | The Significance of Code Reviews  | Benefits, collective ownership, psych safety             | [ch01-constructive-code-reviews.md](file:chapters/ch01-constructive-code-reviews.md) | ~1,000      |
| **Ch 02** | Dissecting the Code Review        | Review systems, workflow, PR parts, roles                | [ch02-constructive-code-reviews.md](file:chapters/ch02-constructive-code-reviews.md) | ~1,100      |
| **Ch 03** | Building Your First Process       | Phase-based setup, goals, workflows, rules               | [ch03-constructive-code-reviews.md](file:chapters/ch03-constructive-code-reviews.md) | ~1,100      |
| **Ch 04** | The Team Working Agreement        | Codifying rules, SLAs, styling, Git TWAs                 | [ch04-constructive-code-reviews.md](file:chapters/ch04-constructive-code-reviews.md) | ~1,200      |
| **Ch 05** | The Advantages of Automation      | Linting, formatters, automated CI checks, objectivity    | [ch05-constructive-code-reviews.md](file:chapters/ch05-constructive-code-reviews.md) | ~1,000      |
| **Ch 06** | Composing Effective Comments      | Empathetic comment writing, 5P, MMG Exchange             | [ch06-constructive-code-reviews.md](file:chapters/ch06-constructive-code-reviews.md) | ~1,200      |
| **Ch 07** | How Code Reviews Can Suck         | Nitpicking, review creep, delayed loops, friction        | [ch07-constructive-code-reviews.md](file:chapters/ch07-constructive-code-reviews.md) | ~1,000      |
| **Ch 08** | Decreasing Review Delays          | Review bottlenecks, taking chats offline, ticket sizing  | [ch08-constructive-code-reviews.md](file:chapters/ch08-constructive-code-reviews.md) | ~1,100      |
| **Ch 09** | Eliminating Process Loopholes     | Merging around reviews, rubber stamping, bypass auditing | [ch09-constructive-code-reviews.md](file:chapters/ch09-constructive-code-reviews.md) | ~1,100      |
| **Ch 10** | The Emergency Playbook            | Hotfixes, bypass authorization, post-incident reviews    | [ch10-constructive-code-reviews.md](file:chapters/ch10-constructive-code-reviews.md) | ~1,100      |
| **Ch 11** | Code Reviews and Pair Programming | Drivers, Navigators, pairing vs. reviewing, hybrid flows | [ch11-constructive-code-reviews.md](file:chapters/ch11-constructive-code-reviews.md) | ~1,000      |
| **Ch 12** | Code Reviews and Mob Programming  | Mobbing, knowledge sharing, "agree then split" approach  | [ch12-constructive-code-reviews.md](file:chapters/ch12-constructive-code-reviews.md) | ~1,000      |
| **Ch 13** | Code Reviews and AI               | AI benefits, limitations, tools, Human-AI pairing        | [ch13-constructive-code-reviews.md](file:chapters/ch13-constructive-code-reviews.md) | ~1,000      |

---

## 📂 Reference Files

- **[glossary.md](glossary.md):** Alphabetical guide to key terms (e.g., SLAs, review creep, MMG Exchange, runbooks).
- **[patterns.md](patterns.md):** Structured techniques, principles, and anti-patterns for software engineers.
- **[cheatsheet.md](cheatsheet.md):** Decision tables, checklists, and quick references.
