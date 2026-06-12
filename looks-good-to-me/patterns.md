# Patterns & Anti-Patterns

A catalog of constructive techniques, software engineering principles, and process anti-patterns drawn from _Looks Good to Me: Constructive Code Reviews_.

---

## Positive Patterns & Techniques

### 1. The 5P Review Checklist

- **Type:** Technique
- **Context:** A reviewer is preparing to leave a change request comment on a pull request.
- **Solution:** Before typing the comment, pause and ponder:
  - _Pause:_ Wait a moment before writing.
  - _Ponder:_ Walk through your rational justification. Is it necessary? Is it objective?
  - _Pass:_ If subjective or personal preference, discard the comment.
  - _Propose:_ If valid, construct an objective, polite suggestion using comment signals.
  - _Postpone:_ If valuable but out of scope, save it for a separate issue.
- **Consequences:** Eliminates cosmetic arguments, saves developer time, and keeps review psychological safety high.
- **Chapter:** 6

### 2. Maintainable Middle Ground (MMG) Exchange

- **Type:** Technique
- **Context:** Author and reviewer are stuck in a subjective argument about variable naming, design, or formatting.
- **Solution:** Initiate an MMG Exchange:
  - Maintain a professional, respectful tone.
  - Acknowledge the other developer's concerns.
  - Seek to understand each other's technical justifications.
  - Proactively seek a middle ground compromise.
  - If still stuck, request a fast team review for consensus.
- **Consequences:** Resolves blockages quickly, prevents ego battles, and produces collaborative, highly maintainable code.
- **Chapter:** 6

### 3. Comment Signal Framework (MoSCoW Tags)

- **Type:** Technique
- **Context:** A reviewer wants to communicate the severity of a comment clearly.
- **Solution:** Prefix comments with standardized signals:
  - `[MUST]` — Critical blocker (logic flaw, security hole, TWA violation). Blocks merge.
  - `[SHOULD]` — Highly recommended (quality, readability, performance concern).
  - `[COULD]` — Optional improvement (nice-to-have suggestion).
  - `[NIT]` — Cosmetic or minor (typo, formatting). Does not block merge.
- **Consequences:** Authors immediately understand what is blocking vs. optional, reducing anxiety and speeding resolution.
- **Chapter:** 6

### 4. Three-Exchange Rule

- **Type:** Technique
- **Context:** A PR comment thread is going back and forth with no resolution in sight.
- **Solution:** After 3 exchanges on the same thread, take the discussion offline to a synchronous chat or call. Post the resolution back to the PR.
- **Consequences:** Prevents endless async debates, unblocks the PR, and resolves disagreements faster.
- **Chapter:** 8

### 5. Reviewer Rotation & Shadowing

- **Type:** Technique
- **Context:** Senior engineers are overloaded with reviews, while junior engineers do not feel empowered to approve pull requests.
- **Solution:** Rotate review assignments across all team members using automated round-robin selectors. Pair junior engineers with senior mentors to "shadow" reviews, giving them confidence to participate actively.
- **Consequences:** Eliminates lead developer bottlenecks, distributes system knowledge, and empowers less experienced team members.
- **Chapter:** 8

### 6. PR Labeling

- **Type:** Technique
- **Context:** Reviewers need to quickly triage incoming pull requests.
- **Solution:** Tag PRs with labels like `bug`, `feature`, `documentation`, `refactor`, or `blocked` so reviewers can prioritize their queue.
- **Consequences:** Reduces cognitive load on reviewers, speeds triage, and helps enforce SLAs by priority.
- **Chapter:** 2

### 7. The Living TWA (Team Working Agreement)

- **Type:** Principle
- **Context:** A team needs to codify review norms but wants them to stay current.
- **Solution:** Store the TWA as a markdown file in the Git repository. Modify it via pull requests (not stale wikis or docs). Review and update it during retrospectives.
- **Consequences:** The agreement evolves with the team, is discoverable in the codebase, and carries the same review rigor as production code.
- **Chapter:** 4

### 8. Phase-Based Process Setup

- **Type:** Principle
- **Context:** A team is adopting code reviews for the first time and feels overwhelmed.
- **Solution:** Roll out reviews in three phases:
  1. Alignment & Goals — agree on _why_ reviews matter.
  2. Workflow & Tools — set up branch protection, PR templates.
  3. Guidelines & Style — codify PR size limits, SLAs, conventions.
- **Consequences:** Gradual adoption reduces friction, builds buy-in, and produces a process the team actually follows.
- **Chapter:** 3

### 9. Automated Quality Gates

- **Type:** Technique
- **Context:** The team wants to eliminate subjective formatting debates from human reviews.
- **Solution:** Run linters, formatters, and security scanners in CI. Block merges if quality checks fail. Let machines enforce what machines can judge objectively.
- **Consequences:** Human reviewers focus on architecture and logic instead of whitespace. Removes a major source of nitpicking friction.
- **Chapter:** 5

### 10. Driver & Navigator Workflow

- **Type:** Technique
- **Context:** Two developers are pair programming to produce higher-quality code.
- **Solution:** Split roles clearly:
  - **Driver:** Types, focuses on syntax and short-term implementation.
  - **Navigator:** Reviews architecture, edge cases, security, and alignment with goals.
  - Rotate roles periodically to keep both engaged.
- **Consequences:** Real-time code review catches issues as they are typed, reducing downstream rework.
- **Chapter:** 11

### 11. Hybrid Review Loop

- **Type:** Technique
- **Context:** Complex or high-risk code needs thorough review without slowing the team.
- **Solution:** Pair program on the complex structural parts, then submit a lightweight PR for a third developer to review documentation, readability, and maintainability.
- **Consequences:** Catches deep structural issues in real-time while still getting fresh eyes on the final output.
- **Chapter:** 11

### 12. "Agree Then Split" Mob Programming

- **Type:** Technique
- **Context:** A large refactor or migration requires team-wide alignment on approach.
- **Solution:** The full team mobs on the architecture, interfaces, and core patterns together. Then developers split off to implement routine details individually, submitting standard PRs.
- **Consequences:** Everyone agrees on the hard structural decisions upfront; routine work flows through normal lightweight reviews.
- **Chapter:** 12

### 13. Loophole Audit Framework

- **Type:** Technique
- **Context:** The team suspects code is entering the main branch without proper review.
- **Solution:** Systematically audit all ways code can bypass review: self-approvals, admin merges, stale approvals, skipped status checks. Close each gap with branch protection rules and logging.
- **Consequences:** Eliminates false confidence in the review process. Every path to production is known and governed.
- **Chapter:** 9

### 14. Emergency Playbook Procedure

- **Type:** Technique
- **Context:** A production outage or critical CVE requires an immediate hotfix that cannot wait for standard review.
- **Solution:** Follow a formal, documented bypass path:
  1. Authorize via Tech Lead or EM.
  2. Merge hotfix using admin credentials.
  3. Notify team in public channel immediately.
  4. Conduct retroactive review and postmortem within 24 hours.
- **Consequences:** Urgency is handled without compromising accountability. The bypass is audited, not hidden.
- **Chapter:** 10

### 15. AI as First Responder

- **Type:** Principle
- **Context:** The team wants to use AI tools in the review process.
- **Solution:** Assign AI to handle the first pass: syntax checks, docstring verification, basic edge cases, and PR description generation. Reserve human reviewers for domain logic, architectural alignment, and team safety.
- **Consequences:** AI handles mechanical checks at scale; humans focus on what requires judgment and empathy.
- **Chapter:** 13

### 16. PR Stacking

- **Type:** Technique
- **Context:** A feature is too large to fit in a single reviewable PR.
- **Solution:** Break the feature into small, dependent increments. Merge each increment into an active feature branch. Each PR stays under 300 LOC and is independently reviewable.
- **Consequences:** Prevents gargantuan PRs that reviewers dread. Keeps the review queue flowing.
- **Chapter:** 8

### 17. Active Listening in PRs

- **Type:** Technique
- **Context:** An author has put significant effort into a PR and the reviewer needs to give critical feedback.
- **Solution:** Start the review by acknowledging what the author did well before diving into change requests. Frame suggestions as questions rather than demands.
- **Consequences:** Authors are more receptive to feedback. Psychological safety stays intact.
- **Chapter:** 1

---

## Anti-Patterns (What NOT to Do)

### 1. LGTM Rubber-Stamping

- **Type:** Anti-Pattern
- **Context:** Developers are under high pressure to meet a deadline, or are suffering from review fatigue.
- **Behavior:** Developers quickly type "Looks Good To Me" (LGTM) and approve the PR without reading the diffs or testing.
- **Bust it with:** Require automated status checks, configure the repository to require 2 approvals, and rotate reviewers to reduce fatigue.
- **Chapter:** 9

### 2. Review Creep

- **Type:** Anti-Pattern
- **Context:** A reviewer notices old technical debt in a file that the author modified, and wants it fixed in this PR.
- **Behavior:** The reviewer blocks merge approval until the author refactors unrelated modules.
- **Bust it with:** Formally define scope boundaries in the TWA. Direct out-of-scope refactor suggestions into the team's product backlog as separate tasks.
- **Chapter:** 7

### 3. The Single Reviewer Bottleneck (Reviewer King/Queen)

- **Type:** Anti-Pattern
- **Context:** The tech lead or senior architect insists on personally reviewing and approving every pull request.
- **Behavior:** Code reviews stall for days when the lead is in meetings, blocking the delivery pipe.
- **Bust it with:** Distribute ownership. Update repository settings to allow approvals from any two team members, and implement reviewer rotations.
- **Chapter:** 8

### 4. Self-Approval

- **Type:** Anti-Pattern
- **Context:** A developer has admin permissions and uses them to approve and merge their own PRs.
- **Behavior:** Code enters the main branch with zero external review, bypassing the entire process.
- **Bust it with:** Disable self-approval in repository branch protection settings. Audit admin merge activity.
- **Chapter:** 9

### 5. Admin Bypass Abuse

- **Type:** Anti-Pattern
- **Context:** Administrators routinely use their override permissions to skip reviews for non-emergency features to meet shipping deadlines.
- **Behavior:** Standard PRs are bypassed using admin credentials, eroding the review culture.
- **Bust it with:** Restrict admin bypass to documented emergencies only. Mandate automated logging and public notification of all bypass actions.
- **Chapter:** 9

### 6. Nitpicking

- **Type:** Anti-Pattern
- **Context:** A reviewer leaves dozens of comments on formatting, variable naming, or style preferences.
- **Behavior:** The PR becomes cluttered with cosmetic feedback that could have been automated or ignored.
- **Bust it with:** Set up automated formatters and linters in CI. Define "nit" vs "blocker" in the TWA. Use `[NIT]` tags for cosmetic feedback.
- **Chapter:** 7

### 7. Ego Clashes

- **Type:** Anti-Pattern
- **Context:** Two developers disagree on an implementation and the discussion becomes personal.
- **Behavior:** Comments shift from technical justification to proving who is "smarter," blocking the PR and damaging team relationships.
- **Bust it with:** Enforce the MMG Exchange. Escalate to team consensus if needed. Remind both parties that the goal is maintainable code, not winning.
- **Chapter:** 7

### 8. Async Ping-Pong

- **Type:** Anti-Pattern
- **Context:** A PR comment thread goes on for 10+ cycles with no resolution.
- **Behavior:** Both developers continue making the same points asynchronously, wasting time and delaying the PR.
- **Bust it with:** Enforce the Three-Exchange Rule. After 3 exchanges, take it to a synchronous call.
- **Chapter:** 8

### 9. PR Ghosting

- **Type:** Anti-Pattern
- **Context:** A reviewer starts a review but never completes it or responds to follow-up comments.
- **Behavior:** PRs remain open for days or weeks waiting for reviewer response.
- **Bust it with:** Establish review SLAs in the TWA. Set up automated reminders. Define escalation paths for non-responsive reviewers.
- **Chapter:** 7

### 10. Blind Trust in AI

- **Type:** Anti-Pattern
- **Context:** A team adopts AI code review tools and begins accepting all AI suggestions without scrutiny.
- **Behavior:** AI-generated review comments are applied automatically, creating a new form of rubber-stamping — now with an algorithm.
- **Bust it with:** Treat AI as a first-pass filter, not a final authority. Always have a human review AI suggestions, especially for business logic.
- **Chapter:** 13

### 11. Gargantuan PRs

- **Type:** Anti-Pattern
- **Context:** A developer submits a single PR with 1000+ lines of changes across multiple unrelated concerns.
- **Behavior:** Reviewers procrastinate or skim due to fatigue, missing critical issues.
- **Bust it with:** Enforce PR size limits in the TWA. Break work into smaller PRs using PR Stacking. Slice tickets upstream using the DICE rule.
- **Chapter:** 8

### 12. The Forgotten TWA

- **Type:** Anti-Pattern
- **Context:** A team wrote a Team Working Agreement months ago but nobody references it during reviews.
- **Behavior:** Subjective debates return because there is no shared reference point. The TWA becomes a dead document.
- **Bust it with:** Link the TWA in the PR template. Review and update it during every retrospective. Treat it as living code, not a one-time artifact.
- **Chapter:** 4
