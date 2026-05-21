# Automated Testing and Quality Assurance

## Core concepts

- AI testing tools generate test scripts from plain English prompts — no need to learn testing syntax. This makes testing accessible to nontechnical stakeholders.
- **Self-healing tests** automatically update when the application UI changes, solving the biggest maintenance burden in QA.
- Choose tools by team maturity: Katalon (enterprise, complex workflows, rate 9/10) vs testRigor (startups, rapid iteration, rate 7/10).

## Frameworks introduced

**Functional vs Nonfunctional AI testing** — Functional tools verify behavior (unit, integration, visual, regression). Nonfunctional tools assess performance, compatibility, security, reliability. Many tools combine both.

**Self-healing capability** — When application code or UI changes break existing tests, AI automatically detects and fixes the test scripts. This eliminates the common pattern of tests becoming deprecated and being commented out under deadline pressure.

## Key techniques

**Natural language test generation:** Describe test steps in plain English — "Open browser to URL, click Make Appointment, enter username and password, verify appointment div exists" — and get executable test scripts in correct syntax (Groovy for Katalon, plain English for testRigor).

**Behavior-Driven Test Creation (testRigor):** Define tests based on how users interact with the application, not technical implementation details. Fully cloud-based, no installation needed.

## Code examples

Katalon's StudioAssist generated a full Groovy test script from a natural language prompt in seconds — WebUI.openBrowser(), WebUI.click(), WebUI.setText(), WebUI.verifyElementPresent() — all in correct syntax.

## Connection to other chapters

Continues the Chapter 3 quality theme, moving from code review (pre-merge) to QA (post-merge, pre-production). The AI + Human principle applies: humans define test scope, AI executes the grunt work.
