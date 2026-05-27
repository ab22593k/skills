# Chapter 11: Code Reviews and Pair Programming

## Core Concepts
* **Real-time vs. Async Review:** Pair programming is real-time code review. Two developers review every line of code as it is typed, catching logical nits immediately.
* **Driver vs. Navigator Roles:** Clarifying the distinct cognitive loads in pairing:
  - **Driver:** Focuses on typing, syntax, and short-term implementation.
  - **Navigator:** Focuses on architecture, edge cases, security, and alignment with the ticket goals.
* **Asynchronous Fresh Eyes:** Even if code was paired, it still requires a lightweight asynchronous review from a third developer to check readability, documentation, and maintainability.

## Frameworks Introduced
* **Driver & Navigator Workflow:** Standard pairing roles.
* **Hybrid Review Loop:** Pair programming on complex blocks followed by a lightweight PR review.

## Key Techniques
* **Convincing Teams to Try Pairing:** Overcoming the objection that pairing "wastes resources" (two developers on one task) by proving that it yields higher code quality and eliminates down-stream debugging.
* **Remote Pair Programming Practices:** Utilizing video calls, shared collaborative IDE tools (e.g., Live Share), and clear workspaces.

## Connection to Other Chapters
* Pairing is an excellent tool for **onboarding new devs (Chapter 1)** and **eliminating reviewer bottleneck delays (Chapter 8)**.

## Technical Code Examples
### Pair Programming Git Co-Authoring Commits
```markdown
# To ensure both developers get credit for paired work:
# Add Co-authored-by trailers to the commit message footer

Feat: Implement parametrized customer invoice parsing module

We refactored the parsing mechanism to support dynamic PDF templates, 
resolving the incorrect fee calculation bug identified during demos.

Co-authored-by: Erica Dev <erica@team.com>
Co-authored-by: Justin Coder <justin@team.com>
```

## Reference Tables
### Asynchronous Reviews vs. Pair Programming
| Feature / Characteristic | Asynchronous Code Review (PR) | Pair Programming (Real-Time) |
|--------------------------|--------------------------------|------------------------------|
| **Feedback Loop** | Delayed (hours/days) | Instant (seconds) |
| **Developer Cost** | Low upfront, high downstream when rework occurs | High upfront, low downstream due to fewer bugs |
| **Knowledge Sharing** | Broad but shallow (reviewing diffs) | Deep but localized (pairing partners) |
| **Primary Focus** | Readability, documentation, compliance | Complex logic, architecture, design decisions |