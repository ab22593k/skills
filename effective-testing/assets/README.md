# Effective Testing Assets

This directory contains practical templates and examples for implementing Rapid Software Testing (RST) methodology.

## Templates

Use these templates to structure your testing work:

### 1. SBTM Session Template (`sbtm_session_template.txt`)

**Purpose**: Plan and document focused exploratory testing sessions  
**When to use**: Before starting any testing session (typically 60-120 minutes)  
**Key sections**:

- Charter (one-sentence mission)
- Areas to explore
- Bugs found
- Chronological test notes
- New ideas for future testing
- Outlook (what's left to test)

### 2. Bug Report Template (`bug_report_template.txt`)

**Purpose**: Communicate bugs with clarity and business significance  
**When to use**: When reporting any defect to developers or stakeholders  
**Key sections**:

- Title (concise description)
- Summary (why it matters)
- Steps to reproduce
- Expected vs. actual results
- Significance (impact, likelihood, workarounds)
- Environment details

### 3. Prospective Testing Checklist (`prospective_testing_checklist.txt`)

**Purpose**: Guide requirements/design reviews before implementation  
**When to use**: In meetings with BAs, developers, or product owners  
**Key sections**:

- 11 critical questions to ask
- Testability requirements identification
- Risks identified
- Next steps

## Examples

Study these examples to understand RST in practice:

### 1. Coverage Outline Example (`coverage_outline_example.md`)

**What it shows**:

- How to use HTSM to model a product (URL shortener)
- Coverage tracking with checkboxes
- Quality characteristics assessment
- Risk identification and prioritization
- Testing status summary

**Key takeaways**:

- Coverage is multi-dimensional (structure, function, data, platform)
- Use checkmarks to show what's been tested
- Always identify what's NOT yet tested
- Include professional confidence assessment

### 2. Session Report Example (`session_report_example.md`)

**What it shows**:

- Complete SBTM session documentation
- Chronological thinking process
- Bug reports with oracle references
- New test ideas that emerged during testing
- Professional assessment and recommendations

**Key takeaways**:

- Testing is a learning process (notes show evolving understanding)
- Bugs are discovered through systematic exploration
- Oracles are explicitly referenced (FEW HICCUPS)
- Session ends with clear next steps

### 3. Risk Analysis Example (`risk_analysis_example.md`)

**What it shows**:

- Four-part risk story format
- Collaborative risk brainstorming process
- Risk prioritization matrix
- Testing strategy derived from risks
- Mitigation ideas for each risk

**Key takeaways**:

- Risks are stories, not just items on a list
- Impact × Likelihood = Priority Score
- Testing strategy should be risk-driven
- Include stakeholders in risk sessions

## How to Use These Assets

### For New Testers

1. Start with the **SBTM Session Template** for every testing session
2. Use the **Bug Report Template** to communicate findings professionally
3. Study the **Session Report Example** to understand the thinking process
4. Reference the **Coverage Outline Example** when planning test strategy

### For Experienced Testers

1. Use the **Prospective Checklist** in requirements meetings
2. Adapt the **Risk Analysis Example** for your team's risk sessions
3. Customize templates to fit your team's workflow
4. Share examples with developers to improve bug communication

### For Team Leads

1. Introduce these templates gradually (don't overwhelm the team)
2. Use examples in training sessions
3. Encourage team members to create their own examples
4. Review session reports in debrief meetings

## Integration with RST Methodology

These assets support the core RST workflow:

```
1. Model Product → Use Coverage Outline Example (HTSM)
       ↓
2. Define Strategy → Use Risk Analysis Example
       ↓
3. Execute Sessions → Use SBTM Session Template
       ↓
4. Apply Oracles → Reference FEW HICCUPS in bug reports
       ↓
5. Report Findings → Use Bug Report Template + PROOF heuristic
```

## Best Practices

### Do's

- ✅ Keep session notes chronological and detailed
- ✅ Reference specific oracles when reporting bugs
- ✅ Update coverage outlines as testing progresses
- ✅ Include professional assessment in reports
- ✅ Debrief sessions with stakeholders

### Don'ts

- ❌ Don't treat templates as bureaucracy (they're thinking tools)
- ❌ Don't write bug reports without significance assessment
- ❌ Don't skip the "new ideas" section in session reports
- ❌ Don't use coverage outlines as metrics (they're for learning)
- ❌ Don't do prospective testing alone (it's collaborative)

## Further Reading

- [HTSM Reference](../references/htsm.md) - Heuristic Test Strategy Model
- [Oracles Reference](../references/oracles.md) - FEW HICCUPS heuristic
- [Reporting Guide](../references/reporting.md) - PROOF heuristic and storytelling
- [Prospective Testing Guide](../references/prospective_testing.md) - Testing before code
- [Automation Traps](../references/automation_traps.md) - Avoiding tool pitfalls

---

**Remember**: These are thinking tools, not documentation burdens. Use them to improve your testing, not to create paperwork. The goal is better testing, not better templates.
