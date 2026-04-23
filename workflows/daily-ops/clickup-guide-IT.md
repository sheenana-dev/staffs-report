# ClickUp Guide — IT Department

**Space:** IT Department (Blue)
**Lists:** Current Development, Bugs

This is your team's workspace for tracking all development work. Every feature and bug fix lives here.

---

## Your Lists

### Current Development
For **all planned development work** — features, improvements, design-to-dev handoffs, and any active work your team is building.

Examples:
- Build merchant dashboard v2
- Implement push notification for promos
- Add coupon expiration warning to app
- Implement new onboarding flow screens (from Design)

### Bugs
For **bug reports and fixes** — things that are broken and need to be fixed. Bugs are separate because they're often urgent and unplanned.

Examples:
- Fix login crash on Android
- Coupon redemption not updating count
- App freezes when loading large merchant list

---

## How to Create a Task

Every task must have these fields:

| Field | Required | How to Fill It |
|-------|----------|----------------|
| **Task name** | Yes | Be specific: "Fix login crash on Android" not just "Fix bug" |
| **Assignee** | Yes | Who's doing the work — assign one person |
| **Priority** | Yes | Urgent / High / Normal / Low |
| **Due date** | Yes | When it needs to be done |
| **Description** | Yes | What needs to happen, steps to reproduce (for bugs), specs, context |
| **List** | Yes | Current Development or Bugs |

### For Bugs — Also Include:
- **Severity** in the description: Critical (app unusable), High (feature broken), Low (cosmetic)
- **Steps to reproduce**: What the user did, what happened, what should have happened
- **Platform**: iOS, Android, Huawei, Web, API

### For Development Tasks — Also Include:
- **Subtasks** for big features: break into API, frontend, testing, deployment

---

## Statuses — What They Mean for IT

| Status | What It Means |
|--------|---------------|
| **TO DO** | Task is planned but no one has started coding yet |
| **IN PROGRESS** | Someone is actively working on it — code is being written |
| **REVIEW** | Code is done, waiting for code review or QA testing |
| **COMPLETE** | Merged, tested, and deployed (or ready for deployment) |

Move tasks across as work progresses. Don't wait until Friday to batch-update.

---

## Cross-Department Tags

Use these tags when your task needs something from another department:

| Tag | When to Use | Example |
|-----|-------------|---------|
| `needs-design` | You need UI mockups or design specs before you can build | "Need screens for new merchant onboarding flow" |
| `needs-marketing` | You need copy, campaign details, or notification text | "Need push notification copy for payday promo" |
| `needs-sales` | You need merchant info or business requirements | "Need list of merchant categories for dropdown" |
| `blocked` | Task is stuck and can't move forward | Waiting on external API, server issue, dependency |

When you add a tag, Sheena sees it on her dashboard. She'll help coordinate.

---

## Sample Tasks

```
Task: Fix login crash on Android
  List: Bugs
  Priority: Urgent
  Assignee: @dev-name
  Due: March 5
  Description:
    Severity: Critical
    Platform: Android (all versions)
    Steps to reproduce: Open app → tap Login → app crashes
    Expected: Login screen appears
    Actual: App force closes
```

```
Task: Build merchant dashboard v2
  List: Current Development
  Priority: High
  Assignee: @dev-name
  Due: March 20
  Description:
    Build the updated merchant dashboard with new KPI cards
  Subtasks:
    - API endpoint for merchant stats
    - Frontend dashboard components
    - Integration testing
    - Deployment to staging → production
```

```
Task: Implement push notification for promos
  List: Current Development
  Priority: Normal
  Assignee: @dev-name
  Due: March 25
  Tags: needs-marketing
  Description:
    Build push notification system for promotional campaigns.
    Need notification copy and schedule from Marketing team.
```

---

## Your Daily Routine (5 minutes)

1. **Open your IT Space** → Board View
2. **Scan the board** — anything stuck in IN PROGRESS for too long?
3. **Update task statuses** — move tasks that progressed since yesterday
4. **Check for new bugs** — anything urgent that came in overnight?
5. **Assign unassigned tasks** — nothing should sit in TO DO without an owner
6. **Tag blockers** — if something is stuck, add the `blocked` tag and note why

---

## Common Mistakes to Avoid

- **Tasks with no due date** — every task needs a deadline, even if it's an estimate
- **One giant task instead of subtasks** — if it takes more than a few days, break it down
- **Leaving tasks in IN PROGRESS for 2+ weeks** — either the task is too big or it's abandoned
- **Not using the Bugs list** — bugs go in Bugs, not Current Development, so you can track bug volume separately
