# Chapter 4: The Team Working Agreement (TWA)

## Core Concepts
* **The TWA as Code:** The Team Working Agreement should live inside the team's Git repository. Modifying the TWA requires a standard PR, ensuring collaborative alignment.
* **Style Guidelines:** Style rules (tabs vs. spaces, naming, imports) should be documented to remove subjective arguments from code reviews.
* **SLA (Service Level Agreements):** Clear time limits for reviews prevent pull requests from languishing in queue for days.

## Frameworks Introduced
* **The Living Agreement:** A framework for keeping team guidelines up-to-date. Instead of a forgotten wiki page, the TWA is a tracked file in the codebase.
* **Review SLAs:** Set clear turnaround expectations based on priority and size.

## Key Techniques
* **Defining "Nits" vs "Blockers":** Structuring comments so authors know what must be fixed before merging vs. what is a optional improvement.
* **Drafting a TWA:** Collaboratively writing the initial agreement using a standard template.

## Connection to Other Chapters
* Many styling and formatting guidelines in the TWA should be **automated in Chapter 5** to avoid human review friction. The TWA also provides the baseline SLAs that help **reduce delays in Chapter 8**.

## Technical Code Examples
### Markdown Example of a TWA's Code Review SLA Section
```markdown
## 🕒 Code Review SLAs
* **Standard PRs (< 300 LOC):** Initial review within **24 hours** of submission.
* **Urgent Hotfixes:** Reviewed immediately upon notification in the `#dev-emergency` Slack channel.
* **Large PRs (> 300 LOC):** Authors must schedule a synchronous walkthrough or pairing session to speed up review.
* **Review Window:** Code reviews are conducted twice daily: at 11:00 AM and 4:00 PM.
```

## Reference Tables
### Core Elements of a Team Working Agreement
| Section | Purpose | Example Rule |
|---------|---------|--------------|
| **PR Sizing & Slicing** | Prevent review fatigue | "Keep PRs under 300 lines of code" |
| **Review Turnaround SLA** | Avoid blockages and delays | "First review completed within 24 business hours" |
| **Nitpicking Definitions** | Distinguish critical logic from style preference | "Use MoSCoW tags (`[MUST]`, `[COULD]`) to label feedback" |
| **Style & Formatting** | Centralize style standards | "Format all code using standard configurations before opening a PR" |