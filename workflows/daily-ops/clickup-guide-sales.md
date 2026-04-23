# ClickUp Guide — Sales Department

**Space:** Sales Department (Orange)
**Lists:** Merchant Leads, Onboarding, Account Management

This is your team's workspace for tracking the full merchant lifecycle — from first pitch to ongoing account health. Every merchant prospect, onboarding process, and account review lives here.

---

## Your Lists

### Merchant Leads
For **new merchant prospects** — anyone your sales team is pitching or in talks with. A merchant stays here until they sign a contract.

Examples:
- Pitch ABC Restaurant — Makati
- Follow up with XYZ Cafe — Quezon City
- Schedule demo for 123 Grill — BGC

### Onboarding
For **merchants who signed but aren't live yet** — the setup process from contract to going live on the B-Ticket app. Once a lead signs, move them from Merchant Leads to Onboarding.

Examples:
- Onboard XYZ Cafe (signed March 5)
- Onboard 123 Grill (signed March 8)

### Account Management
For **active merchants already on the platform** — monthly coupon reviews, merchant health checks, and relationship management.

Examples:
- Monthly review — Jollibee Makati (March)
- Coupon swap request — ABC Restaurant
- Follow up on low redemptions — DEF Bakery

### The Merchant Lifecycle

```
Merchant Leads → Onboarding → Account Management
(pitching)        (setting up)   (live on app)
```

When a merchant moves to the next stage, create a new task in the right list (or move the task).

---

## How to Create a Task

Every task must have these fields:

| Field | Required | How to Fill It |
|-------|----------|----------------|
| **Task name** | Yes | Include merchant name and location: "Pitch ABC Restaurant — Makati" |
| **Assignee** | Yes | Who owns this merchant relationship |
| **Priority** | Yes | Urgent / High / Normal / Low |
| **Due date** | Yes | Next action date (pitch meeting, follow-up call, onboarding deadline) |
| **Description** | Yes | Merchant details, contact info, what stage they're in |
| **List** | Yes | Merchant Leads, Onboarding, or Account Management |

### For Merchant Leads — Also Include:
- **Location**: City / area
- **Category**: Restaurant, Cafe, Fast Food, Bakery, etc.
- **Pipeline stage**: Contacted / Pitched / Negotiating / Contract Sent

### For Onboarding — Use the 7-Step Subtask Checklist:
Every onboarding task should have these subtasks:
```
Task: Onboard XYZ Cafe
  ├── Collect photos from merchant
  ├── Confirm operating hours
  ├── Get contract signed
  ├── Create HubSpot record
  ├── Add merchant to B-Ticket app
  ├── Set up coupons in app
  └── Notify merchant they're live
```
Check off each subtask as you complete it. This is how you track onboarding progress.

### For Account Management — Also Include:
- **Coupons active**: How many and what kind
- **Redemptions this month**: Current count
- **Action needed**: None / Swap coupon / Follow up / At risk

---

## Statuses — What They Mean for Sales

| Status | What It Means |
|--------|---------------|
| **TO DO** | Identified but not contacted yet (leads), or assigned but not started (onboarding/accounts) |
| **IN PROGRESS** | Actively working — in talks with merchant, collecting info, doing review |
| **REVIEW** | Needs approval or a decision — contract needs sign-off, coupon swap needs confirmation |
| **COMPLETE** | Deal closed (leads), merchant is live (onboarding), monthly review done (accounts) |

---

## Cross-Department Tags

Use these tags when your task needs something from another department:

| Tag | When to Use | Example |
|-----|-------------|---------|
| `needs-design` | You need marketing materials for a merchant | "Need poster and table tent for ABC Restaurant's launch promo" |
| `needs-IT` | You need the merchant added to the app or technical setup | "XYZ Cafe signed — needs to be added to B-Ticket app and coupons set up" |
| `needs-marketing` | You need promotional support for a merchant launch | "ABC Restaurant going live next week — need social media push" |
| `blocked` | Task is stuck | Waiting for merchant to send photos, contract not returned, app issue |

When you add a tag, Sheena sees it on her dashboard. She'll help coordinate.

---

## Sample Tasks

```
Task: Pitch ABC Restaurant — Makati
  List: Merchant Leads
  Priority: High
  Assignee: @sales-name
  Due: March 8
  Description:
    Location: Makati Ave, Makati City
    Category: Restaurant (Filipino cuisine)
    Contact: Juan dela Cruz, 0917-XXX-XXXX
    Pipeline stage: Contacted — meeting scheduled March 8
    Notes: Interested in 3-month trial. Has 2 branches.
```

```
Task: Onboard XYZ Cafe
  List: Onboarding
  Priority: High
  Assignee: @onboarding-ops
  Due: March 12
  Tags: needs-IT, needs-design
  Description:
    Signed: March 5
    Location: Quezon City
    Category: Cafe
    Need IT to add to app. Need Design for launch poster.
  Subtasks:
    - [x] Get contract signed
    - [ ] Collect photos from merchant
    - [ ] Confirm operating hours
    - [ ] Create HubSpot record
    - [ ] Add merchant to B-Ticket app (needs-IT)
    - [ ] Set up coupons in app (needs-IT)
    - [ ] Notify merchant they're live
```

```
Task: Monthly review — 10 merchants
  List: Account Management
  Priority: Normal
  Assignee: @account-mgmt-ops
  Due: March 30
  Description:
    Review coupon performance for these 10 merchants:
    1. Jollibee Makati — 45 redemptions
    2. ABC Restaurant — 12 redemptions (low — needs follow up)
    3. ...
    Flag any merchant with <15 redemptions for coupon swap discussion.
```

---

## Your Daily Routine (5 minutes)

1. **Open your Sales Space** → Board View
2. **Check Merchant Leads** — any follow-ups due today? Update statuses after calls/meetings
3. **Check Onboarding** — any merchants stuck? Which subtasks are incomplete?
4. **Check Account Management** — any reviews due this week?
5. **Tag cross-department needs** — if a merchant needs design materials or IT setup, tag it now
6. **Update pipeline stages** in task descriptions after each interaction

---

## Common Mistakes to Avoid

- **Not using the onboarding checklist** — always create the 7 subtasks when a merchant moves to Onboarding. This is how Sheena tracks onboarding bottlenecks
- **Leaving merchants in Onboarding for 2+ weeks** — if onboarding is stuck, add the `blocked` tag and say why
- **Not moving merchants between lists** — when a lead signs, create their onboarding task. When they go live, create their account management task
- **Missing merchant details** — always include merchant name, location, and category. "Follow up with merchant" is not a useful task name
