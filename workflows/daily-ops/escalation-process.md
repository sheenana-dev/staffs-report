# Escalation Process

## Purpose
Define clear rules for when and how to escalate issues so problems get solved at the right level. Without this, small issues reach you unnecessarily while big issues get buried.

## When
- Reference this whenever an issue comes up that someone can't resolve on their own
- Review and update quarterly

## Steps: The Escalation Ladder

### Level 1: Within the Team (Department Lead handles)
**What:** Day-to-day issues that one department can solve alone
**Examples:**
- Task is taking longer than expected
- Team member needs help with their work
- Minor bug that doesn't affect users
- Design revision needed
- Missed a daily deadline

**Action:** Department lead resolves within 24 hours. No need to involve you.

### Level 2: Cross-Department (You coordinate)
**What:** Issues that require two or more departments to resolve
**Examples:**
- Design delivered specs but IT says they're not feasible
- Sales promised a merchant a feature that doesn't exist
- Marketing needs a landing page but IT is fully booked
- A merchant complained and it involves both Sales and IT

**Action:**
1. Department lead messages you on Telegram with the issue
2. You identify who else needs to be involved
3. Create a thread or quick call with the relevant people
4. Set a resolution deadline
5. Follow up until resolved

### Level 3: Business Impact (You decide + act immediately)
**What:** Issues that directly affect revenue, users, or company reputation
**Examples:**
- App is down and merchants/users are affected
- A merchant threatens to leave publicly
- Data breach or security incident
- Legal issue (complaint, copyright, etc.)
- Team member misconduct

**Action:**
1. Respond within 1 hour
2. Assess impact: How many users/merchants are affected?
3. Assign someone to fix it immediately
4. Communicate status to affected parties
5. Do a post-mortem after resolution

### Level 4: Executive / External (Escalate above you)
**What:** Issues beyond your authority or that need company leadership
**Examples:**
- Budget increase needed beyond your approval limit
- Partnership opportunity that changes company direction
- Legal threat requiring lawyer involvement
- HR issue you can't resolve (termination, harassment)
- Major pivot in strategy

**Action:**
1. Document the issue clearly
2. Present options (not just the problem)
3. Escalate to your manager/company leadership with a recommendation

## Templates

### Telegram: Escalation Report (Level 2+)
```
ESCALATION

Issue: [clear description]
Level: [2 / 3 / 4]
Departments involved: [which]
Impact: [who's affected and how]
Urgency: [needs resolution by when]

What's been tried: [what the team already did]
What's needed: [specific action or decision]

@[people who need to act]
```

### Telegram: Incident Alert (Level 3 — App Down / Major Issue)
```
INCIDENT ALERT

What: [the app is down / payment failing / data issue]
Since: [time it started]
Impact: [X users/merchants affected]
Severity: [Critical — revenue/users impacted]

IT lead @[name] is investigating.
I'll post updates every 30 minutes until resolved.

DO NOT post about this publicly until we have a fix timeline.
```

### Telegram: Incident Resolution
```
INCIDENT RESOLVED

Issue: [what happened]
Duration: [how long it lasted]
Root cause: [brief explanation]
Fix: [what was done]
Prevention: [what we'll do to stop it happening again]

Thanks to [team/people] for the quick response.

Post-mortem meeting: [date/time]
```

### Telegram: Merchant Complaint Escalation
```
MERCHANT ISSUE

Merchant: [name]
Account manager: @[salesperson]
Issue: [what they're unhappy about]
Risk: [might churn / public complaint / etc.]

Current status: [what's been done]
Needs: [specific help from IT/Design/etc.]

Let's resolve this by [date].
```

## Escalation Decision Tree

```
Is anyone in danger or is there a legal issue?
  → YES → Level 4 — Escalate to leadership immediately
  → NO ↓

Is the app down or merchants/users directly impacted?
  → YES → Level 3 — You handle immediately
  → NO ↓

Does it need another department to resolve?
  → YES → Level 2 — You coordinate
  → NO ↓

Can the department lead handle it?
  → YES → Level 1 — Let them handle it
```

## Red Flags
- Everything gets escalated to you — leads aren't empowered to make decisions
- Nothing gets escalated to you — leads might be hiding problems
- The same issue escalates multiple times — root cause isn't being fixed
- Escalations come with just the problem, never a proposed solution — train leads to bring options
- Merchant complaints take more than 48 hours to address — too slow for a B2C business
- Post-mortems are skipped — the team doesn't learn from incidents

## Rules for Your Team
Share these with all department leads:

1. **Don't sit on problems** — If you can't resolve it in 24 hours, escalate
2. **Escalate with context** — Use the template. "There's a problem" is not an escalation
3. **The person who spots the issue owns it until it's handed off** — Don't just throw it over the wall
4. **No blame** — We escalate to solve problems, not to point fingers
5. **Always include what you've already tried** — This saves everyone time
6. **After resolution, document what happened** — So we don't repeat it
