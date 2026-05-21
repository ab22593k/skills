# Patterns & Anti-Patterns

A catalog of constructive techniques, software engineering principles, and process anti-patterns.

---

## 🟢 Positive Patterns & Techniques

### 1. The 5P Review Checklist
* **Type:** Technique
* **Context:** A reviewer is preparing to leave a change request comment on a pull request.
* **Solution:** Before typing the comment, pause and ponder:
  - *Pause:* Wait a moment before writing.
  - *Ponder:* Walk through your rational justification. Is it necessary? Is it objective?
  - *Pass:* If subjective or personal preference, discard the comment.
  - *Propose:* If valid, construct an objective, polite suggestion using comment signals.
  - *Postpone:* If valuable but out of scope, save it for a separate issue.
* **Consequences:** Eliminates cosmetic arguments, saves developer time, and keeps review psychological safety high.

### 2. Maintainable Middle Ground (MMG) Exchange
* **Type:** Technique
* **Context:** Author and reviewer are stuck in a subjective argument about variable naming, design, or formatting.
* **Solution:** Initiate an MMG Exchange:
  - Maintain a professional, respectful tone.
  - Acknowledge the other developer's concerns.
  - Seek to understand each other's technical justifications.
  - Proactively seek a middle ground compromise.
  - If still stuck, request a fast team review for consensus.
* **Consequences:** Resolves blockages quickly, prevents ego battles, and produces collaborative, highly maintainable code.

### 3. Reviewer Rotation & Shadowing
* **Type:** Technique
* **Context:** Senior engineers are overloaded with reviews, while junior engineers do not feel empowered to approve pull requests.
* **Solution:** Rotate review assignments across all team members using automated round-robin selectors. Pair junior engineers with senior mentors to "shadow" reviews, giving them confidence to participate actively.
* **Consequences:** Eliminates lead developer bottlenecks, distributes system knowledge, and empowers less experienced team members.

---

## 🔴 Anti-Patterns (What NOT to Do)

### 1. LGTM Rubber-Stamping
* **Type:** Anti-Pattern
* **Context:** Developers are under high pressure to meet a deadline, or are suffering from review fatigue.
* **Solution (Bust it):** Developers quickly type "Looks Good To Me" (LGTM) and approve the PR without reading the diffs or testing.
* **Bust it with:** Require automated status checks, configure the repository to require 2 approvals, and rotate reviewers to reduce fatigue.

### 2. Review Creep
* **Type:** Anti-Pattern
* **Context:** A reviewer notices old technical debt in a file that the author modified, and wants it fixed in this PR.
* **Solution (Bust it):** The reviewer blocks merge approval until the author refactors unrelated modules.
* **Bust it with:** Formally define scope boundaries in the TWA. Direct out-of-scope refactor suggestions into the team's product backlog as separate tasks.

### 3. The Single Reviewer Bottleneck
* **Type:** Anti-Pattern
* **Context:** The tech lead or senior architect insists on personally reviewing and approving every pull request.
* **Solution (Bust it):** Code reviews stall for days when the lead is in meetings, blocking the delivery pipe.
* **Bust it with:** Distribute ownership. Update repository settings to allow approvals from any two team members, and implement reviewer rotations.