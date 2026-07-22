# Emergency Playbook — Template & Reference

*Based on Chapter 10 of "Looks Good to Me" by Adrienne Braganza*

## What Is an Emergency?

An emergency is a situation where the standard review process would cause unacceptable harm or delay. Examples:

- **Production outage** — Customers can't use the product
- **Security vulnerability** — Active exploit or critical CVE with a known fix
- **Regulatory deadline** — Compliance requirement with an immovable date
- **Revenue-blocking issue** — Feature delay directly costs money

## When to Use This Playbook

**Only** when all three conditions are met:
1. The situation meets the team's definition of emergency
2. The standard review process would take too long
3. The bypass is documented and time-boxed

## Decision Tree

```
Is this an emergency as defined by the team?
├── No → Follow standard review process
└── Yes →
    Does the fix require a bypass of standard process?
    ├── No → Follow standard review but mark as HIGH PRIORITY
    └── Yes →
        Is the author authorized to self-approve?
        ├── No → Request emergency approval from [lead/manager]
        └── Yes → Proceed with bypass (document everything)
```

## Emergency Review Process

### Step 1: Confirm Emergency Status
- Verify against team's emergency criteria
- If unclear, escalate to lead/manager for decision

### Step 2: Apply Bypass Mechanism
- Bypass type: [e.g., reduced reviewers, fast-track approval, pre-approved scope]
- Authorized by: [person who authorized the bypass]
- Duration: [how long this bypass is valid — e.g., "next 4 hours"]

### Step 3: Document Trade-offs
Record what was bypassed and why:

```
EMERGENCY BYPASS RECORD
Date/Time:
Incident:
Author:
Approver:
Bypassed controls:
- [ ] Standard review (skip/minimal review)
- [ ] Test coverage requirement (reduced)
- [ ] CI gate (ignored failure)
- [ ] Other:
Risk accepted:
Tracking issue for follow-up:
```

### Step 4: Post-Emergency Follow-up
- Create a tracking issue for each bypassed control
- Schedule review of the emergency change within [e.g., 5 business days]
- Retro: Did the emergency response work well? What could be improved?

## Bypass Gradients

Not all emergencies require full bypass. Use the minimum bypass needed:

| Situation | Bypass |
|---|---|
| Simple production fix (one-liner) | Single reviewer, no test requirement |
| Complex production fix (multiple files) | Two reviewers, reduced test requirement |
| Security patch | Two reviewers + security lead, expedited |
| Regulatory deadline | Lead approves, full review within 48 hours |
