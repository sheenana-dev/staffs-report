# ClickUp Guide — Design Department

**Space:** Design Department (Purple)
**Folder:** B-Ticket
**Lists:** Design Requests, Merchant Materials, Other (Daimasu, Midori, etc.)

This is your team's workspace for tracking all design work. Everything lives inside one B-Ticket folder.

---

## Your Lists

### Design Requests
For **all incoming B-Ticket design work** — campaign visuals, app mockups, brand materials.

Examples:
- March payday campaign visuals (5 assets)
- New app onboarding screen mockups
- Updated B-Ticket brand guidelines document

### Merchant Materials
For **merchant-specific collateral** — posters, banners, menus for B-Ticket merchants.

Examples:
- Create poster for Jollibee promo
- Design table tent for ABC Restaurant
- Update menu layout for XYZ Cafe

**Rule of thumb:** If it's for a specific merchant's physical or digital promotion → Merchant Materials. Everything else → Design Requests.

### Other (Daimasu, Midori, etc.)
For **all design work for the company's other businesses** — Daimasu, Midori, and any non-B-Ticket brands.

Examples:
- Daimasu menu update — new seasonal items
- Midori promotional poster — March promo
- Social media assets for Daimasu Instagram

---

## How to Create a Task

Every task must have these fields:

| Field | Required | How to Fill It |
|-------|----------|----------------|
| **Task name** | Yes | Be specific: "Create poster for Jollibee March promo" not just "Design poster" |
| **Assignee** | Yes | Which designer is doing the work |
| **Priority** | Yes | Urgent / High / Normal / Low |
| **Due date** | Yes | When the requester needs it delivered |
| **Description** | Yes | What's needed, dimensions/format, brand guidelines, reference images |
| **List** | Yes | Design Requests, Merchant Materials, or Other (Daimasu, Midori, etc.) |

### Also Include in the Description:
- **Requested by**: Which department or person asked for this (e.g., "Requested by: Marketing — for March payday campaign")
- **Type**: Merchant / Campaign / Brand / Other
- **Deliverable format**: PNG, PDF, Figma link, etc.
- **Dimensions**: Social media size, print size, app banner size, etc.

### For Multi-Asset Requests — Use Subtasks:
```
Task: March payday campaign visuals (5 assets)
  ├── Facebook banner (1200x628)
  ├── IG story (1080x1920)
  ├── IG post (1080x1080)
  ├── TikTok cover (1080x1920)
  └── App banner (750x400)
```

---

## Statuses — What They Mean for Design

| Status | What It Means |
|--------|---------------|
| **TO DO** | Request received, not started yet — sitting in the queue |
| **IN PROGRESS** | A designer is actively working on it |
| **REVIEW** | Design is done, waiting for the requester's feedback or approval |
| **COMPLETE** | Approved and delivered — files sent/uploaded |

Move tasks to REVIEW as soon as you send the draft for feedback. Don't wait for approval to move it — that's what REVIEW means.

---

## Cross-Department Tags

Use these tags when your task needs something from another department:

| Tag | When to Use | Example |
|-----|-------------|---------|
| `needs-marketing` | You need campaign details, copy, or a brief before you can start designing | "Need campaign brief for payday promo before I can create visuals" |
| `needs-IT` | The design needs to be implemented by developers | "Onboarding screens done, needs dev to implement" |
| `needs-sales` | You need merchant info, photos, or details | "Need ABC Restaurant's logo and menu photos to create poster" |
| `blocked` | Task is stuck and can't move forward | Waiting for feedback, missing assets, unclear brief |

When you add a tag, Sheena sees it on her dashboard. She'll help coordinate.

---

## Sample Tasks

```
Task: Create poster for Jollibee promo
  List: Merchant Materials
  Priority: High
  Assignee: @designer-name
  Due: March 10
  Description:
    Requested by: Sales — for Jollibee Makati branch
    Type: Merchant
    Deliverable: Print poster (A3) + digital version (1080x1080 for IG)
    Details: March 15-31 promo, 20% off with B-Ticket coupon
    Assets needed: Jollibee logo (on file), promo details from Sales
```

```
Task: March payday campaign visuals (5 assets)
  List: Design Requests
  Priority: High
  Assignee: @designer-name
  Due: March 14
  Tags: needs-marketing
  Description:
    Requested by: Marketing — for March Payday Promo campaign
    Type: Campaign
    Need campaign brief from Marketing before starting.
  Subtasks:
    - Facebook banner (1200x628)
    - IG story (1080x1920)
    - IG post (1080x1080)
    - TikTok cover (1080x1920)
    - App banner (750x400)
```

```
Task: New onboarding flow mockups
  List: Design Requests
  Priority: Normal
  Assignee: @designer-name
  Due: March 20
  Tags: needs-IT
  Description:
    Requested by: IT — redesign the app onboarding experience
    Type: Brand
    Deliverable: Figma file with 5 screens + interaction notes
    When done, hand off to IT for implementation.
```

---

## Your Daily Routine (5 minutes)

1. **Open your Design Space** → Board View
2. **Check TO DO column** — any new requests that came in? Do they have enough detail to start?
3. **Update statuses** — move tasks that progressed (sent draft → REVIEW, got approval → COMPLETE)
4. **Check REVIEW column** — anything waiting for feedback for more than 2 days? Follow up with the requester
5. **Prioritize the backlog** — sort TO DO by due date. What's due soonest?
6. **Tag missing info** — if a request doesn't have enough detail, add `blocked` and comment what's missing

---

## Common Mistakes to Avoid

- **Requests without a requester name** — always note who asked for it and which department, so you can follow up
- **No due date** — every request needs a deadline, even if the requester didn't give one (ask them)
- **Skipping REVIEW status** — don't jump from IN PROGRESS to COMPLETE. REVIEW is where feedback happens
- **Not using Merchant Materials list** — keep B-Ticket merchant-specific work separate so you can track how many merchants you serve each week (this feeds into your weekly report)
- **Mixing lists** — B-Ticket design work goes in Design Requests, merchant stuff in Merchant Materials, and Daimasu/Midori work in the Other list. Don't mix them
