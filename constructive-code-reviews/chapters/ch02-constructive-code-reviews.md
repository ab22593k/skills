# Chapter 2: Dissecting the Code Review

## Core Concepts
* **Asynchronous Collaboration:** Reviewing pull requests asynchronously allows developers to remain in deep focus states, avoiding disruptive real-time interruptions.
* **Pull Requests (PRs):** The core mechanism of modern tool-facilitated reviews, representing a proposed change branch to be merged into a stable branch.
* **Clear PR Boundaries:** Defining who reviews, when to merge, and what states are required (Approved vs. Changes Requested).

## Frameworks Introduced
* **Review Systems Comparison:** Categorizing reviews into:
  - **Human-led:** Ad-hoc walkthroughs, meetings (best for small, co-located teams).
  - **Tool-facilitated:** PRs in GitHub/GitLab (best for async, distributed workflows).
  - **Hybrid:** Combining tools with synchronous sync-ups when complex changes arise.
* **Roles & Responsibilities:** Clarifying the distinct expectations of the **Author** and the **Reviewer**.

## Key Techniques
* **Writing a Great PR Description:** Providing the "why" and "how" of the changes, including testing steps and visual aids (screenshots/videos).
* **PR Labeling:** Using tags like `bug`, `feature`, `documentation`, or `blocked` to help reviewers prioritize.

## Connection to Other Chapters
* A clear breakdown of PR workflows provides the foundational blocks that will be formally codified in the **TWA (Chapter 4)** and automated using CI checks in **Chapter 5**.

## Technical Code Examples
### Recommended PR Markdown Template
```markdown
# 📝 Description
Provide a concise summary of the change and the problem it solves. Include the "why."

# 🛠️ Proposed Solution
Briefly explain the technical approach taken and why it was selected over alternatives.

# 🧪 How Has This Been Tested?
- [ ] Unit tests added/updated.
- [ ] Manual test: Verified invoice parse succeeds with multiple page layouts.

# 📸 Visuals (if applicable)
Add screenshots or screen recordings showing UI/output changes.
```

## Reference Tables
### Code Review Roles & Expectations
| Participant | Core Responsibility | Key Expectation |
|-------------|---------------------|-----------------|
| **Author** | Write clean, self-reviewed code | Be responsive to feedback, explain context, keep PRs small |
| **Reviewer** | Review logic, security, architecture | Be polite, objective, separate "nits" from "blockers", respond within SLA |