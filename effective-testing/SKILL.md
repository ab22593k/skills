---
name: effective-testing
description: "A comprehensive methodology for highly effective, human-centered software testing. Use this skill when you need to: (1) Design a test strategy for a complex product, (2) Perform exploratory testing using Session-Based Test Management (SBTM), (3) Identify potential bugs using advanced oracle heuristics (FEW HICCUPS), (4) Report bugs with high business significance, (5) Perform prospective testing on requirements/designs, or (6) Supervise AI-generated work. Trigger this skill whenever 'testing', 'quality assurance', 'bug hunting', 'test strategy', 'automation traps', or 'risk analysis' are mentioned."
---

# Rapid Software Testing (RST)

## Overview

Rapid Software Testing is a human-centered, context-driven methodology that treats the product as a mystery to be investigated. It focuses on people, heuristics, skills, and ethics to find the "bugs that matter" as efficiently as possible.

## Core Mindset

- **The Product is a Mystery**: Do not assume it works; probe it to discover its true nature.
- **Testing is Learning**: Every test is an episode of learning about the product's status.
- **The Responsible Tester**: You are an independent agent accountable for the quality of your investigation.
- **Tactical Pessimism**: Cultivate faith in the existence of trouble.
- **Vital Qualities**: Professional testing requires five vital qualities: Empirical, Skilled, Different, Motivated, and Available. See [Tester Qualities](references/tester_qualities.md).

## Workflow: The Testing Cycle

1. **Prospective Testing**: Test ideas and requirements _before_ code exists. Use the [Prospective Checklist](assets/prospective_testing_checklist.txt) and see [Prospective Testing](references/prospective_testing.md).
2. **Model the Product**: Use the [HTSM](references/htsm.md) to brainstorm what to test.
3. **Define Charters**: Create specific missions for testing sessions.
4. **Execute Sessions**: Use SBTM to perform focused exploration. Use the [Session Template](assets/sbtm_session_template.txt).
5. **Apply Oracles**: Use [Oracle Heuristics](references/oracles.md) (FEW HICCUPS) to recognize problematic behavior.
6. **Apply Tools**: Use tools for _checking facts_, but avoid the [13 Automation Traps](references/automation_traps.md).
7. **Report & Storytell**: Use the [Reporting Guide](references/reporting.md) and [Bug Template](assets/bug_report_template.txt) (PROOF heuristic).

## Detailed Guides

- **[Heuristic Test Strategy Model (HTSM)](references/htsm.md)**: A complete taxonomy for strategy brainstorming.
- **[Test Oracles](references/oracles.md)**: How to identify bugs (FEW HICCUPS, Blink Oracle, Safety Language).
- **[Workflows & Management](references/workflows.md)**: Testing vs. Checking, Deep vs. Shallow, SBTM/TBTM.
- **[Automation Traps](references/automation_traps.md)**: 13 classic pitfalls when using tools in testing.
- **[Prospective Testing](references/prospective_testing.md)**: Testing before implementation (The 11-Question Cheat Sheet).
- **[AI and Testing](references/ai_testing.md)**: How to supervise AI, transpection, and the productivity paradox.
- **[Reporting & Storytelling](references/reporting.md)**: PROOF heuristic and Telescoping reports.

## Resources (Assets)

- **[SBTM Session Template](assets/sbtm_session_template.txt)**: For focused exploratory sessions.
- **[Bug Report Template](assets/bug_report_template.txt)**: For professional and actionable bug reporting.
- **[Prospective Checklist](assets/prospective_testing_checklist.txt)**: For meetings and requirements analysis.

## Examples

### Prospective Testing in a Meeting

_User: "We're planning a new feature for multi-currency support. Any thoughts?"_

1. Refer to [Prospective Testing](references/prospective_testing.md).
2. Ask: _"What other features will be affected?"_ or _"How will it recover from currency API failures?"_
3. Use the [Checklist](assets/prospective_testing_checklist.txt) to capture risks.

### Avoiding Automation Pitfalls

_User: "I want to automate 100% of our UI tests to save time."_

1. Refer to [Automation Traps](references/automation_traps.md).
2. Warn about the **Maintenance Trap** and the **Classic GUI Trap**.
3. Suggest the **Golden Rule of Tool Adoption** to evaluate the true value vs. cost.

### Supervizing AI Output

_User: "The AI generated these 50 test cases for me. Are they good?"_

1. Refer to [AI and Testing](references/ai_testing.md).
2. Perform **Transpection**: Ask _"How do I know these are valid?"_ and _"Are they shallow?"_
3. Identify where the AI might be "hallucinating" or providing tautological checks.
