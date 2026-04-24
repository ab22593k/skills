---
name: Effective Testing
description: "A comprehensive methodology for highly effective, human-centered software testing, based on 'Taking Testing Seriously' (Bach & Bolton, 2026). Use this skill to escape the echo chamber of 'best practices' and learn to think critically about risk. MANDATORY for: (1) Designing context-driven test strategies, (2) Performing exploratory testing (SBTM), (3) Identifying bugs with oracle heuristics (FEW HICCUPS), (4) Reporting bugs with high business significance (PROOF), (5) Prospective testing on requirements, or (6) Supervizing AI output through transpection. If the user asks 'Is this code good?' or 'How should I test this?', YOU MUST provide a professional investigation that justifies its methods based on context, not rote standards."
---

# Rapid Software Testing (RST)

## Overview: Testing as the Headlights

Testing is the "headlights" of the project—it doesn't slow the car down; it allows it to move safely at speed by revealing the road ahead. RST treats testing as an empirical investigation, a search for truth grounded in evidence rather than a ritual of "checking" against fixed scripts.

## Part I: Escaping the Echo Chamber

To think critically, a tester must recognize the **Five Schools of Testing** and identify which "echo chamber" is currently influencing the project:

1.  **Factory School**: Focuses on artifacts and rote test cases; treats testers as replaceable robots.
2.  **Quality School**: Claims "quality is everyone's job," often leading to social loafing and the marginalization of deep testing.
3.  **Agile/DevOps School**: Prioritizes delivery speed and automation; often believes full-time testers shouldn't exist.
4.  **Analytical School**: Treats testing as an algorithmic/mathematical branch of computer science.
5.  **Context-Driven School (RST)**: Believes there are **no best practices**—only good practices in context. Testing is a social, psychological, and heuristic process.

### The Core Mindset

- **The Product is a Mystery**: Do not assume it works; probe it to discover its true nature.
- **Testing vs. Checking**: Testing is the human process of exploration and learning. Checking is the algorithmic verification of propositions. Tools can _check_, but only humans can _test_.
- **The Responsible Tester**: You are an independent agent accountable for the quality of your investigation. You must justify your work based on risk, not templates.
- **Critical Distance**: Maintain the ability to think differently from the developers. Avoid becoming a "cheerleader" for the product.

## Part II: Methodology & Process

1.  **Model the Product**: Use the [HTSM](references/htsm.md) to brainstorm coverage.
2.  **Define Strategy**: Use [Test Strategy](references/strategy.md) to prioritize risks. Move between **Deep vs. Shallow** and **Narrow vs. Broad** testing based on "Enoughness."
3.  **Progressive Formalization**: Do not formalize procedures before you understand the product. "Don't follow a procedure that didn't follow you first."
4.  **Execute Sessions**: Use Session-Based Test Management (SBTM) to manage agency.
5.  **Apply Oracles**: Use [Oracle Heuristics](references/oracles.md) (FEW HICCUPS) to recognize "bugs that matter."
6.  **Report & Storytell**: Use the [Reporting Guide](references/reporting.md). A test report is a story of the product's status and the testing's quality.

## Part III: Critical Application & AI

- **[Prospective Testing](references/prospective_testing.md)**: Testing ideas _before_ code exists. Use the [Prospective Checklist](assets/prospective_testing_checklist.txt).
- **[AI and Testing](references/ai_testing.md)**: Perform **Transpection**—the process of explaining and justifying the "magic box" output of AI. Beware of **Automation Bias** and the productivity paradox.
- **[Signals-Based Testing](references/signals_based_testing.md)**: Leveraging system signals while maintaining a critical human eye on failure patterns.

## Part IV: Context, Culture & "Parnism"

- **[Context & Culture](references/context_and_culture.md)**: Understanding why management might prefer "fake testing" (ceremony over result).
- **Beware of Parnism**: The trap of "faking" a rational process retrospectively to satisfy auditors while ignoring real risks.
- **[The Horizon Scandal](references/horizon_scandal.md)**: Learning from systemic failures where management discouraged critical thinking.

## Resources (Assets)

### Templates & Checklists

- **[SBTM Session Template](assets/sbtm_session_template.txt)**: For focused exploratory sessions.
- **[Bug Report Template](assets/bug_report_template.txt)**: Focuses on the PROOF heuristic.
- **[Prospective Checklist](assets/prospective_testing_checklist.txt)**: For requirements/design analysis.

### Examples

- **[Risk Analysis Example](assets/risk_analysis_example.md)**: Four-part risk stories.
- **[Coverage Outline Example](assets/coverage_outline_example.md)**: Mapping the product mystery.

## Critical Thinking Examples

### Challenging a "Best Practice"

_User: "We must have 100% test case documentation before we start. How do I do that?"_

1.  Identify this as a **Factory School** requirement.
2.  Advise on **Progressive Formalization**: Explain that documentation without exploration is hollow and likely to miss elusive bugs.
3.  Suggest a **Coverage Outline** or **Mind Map** as a leaner, more critical alternative.

### Identifying "Fake Testing"

_User: "The automation is green, so we're good to go, right?"_

1.  Refer to **Automation Bias**.
2.  Ask: "What _didn't_ the automation check?" and "How do we know the checks are powerful enough to find bugs that matter?"
3.  Suggest a brief **Exploratory Session** to probe for side effects the automation can't see.
