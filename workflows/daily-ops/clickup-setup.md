# ClickUp Setup Across All Departments

## Purpose
Track all department work in one place. Give Sheena a single dashboard to see what's happening across IT, Design, Sales, and Marketing. Replace scattered Telegram task tracking with a structured system where nothing falls through the cracks.

## When
- **Setup:** Week 2-3 of your 30-day plan (after GC engagement and Monday sync are running)
- **Ongoing:** Teams use daily, you check dashboard before every Monday sync

## Prerequisites
- [ ] Create a ClickUp account at clickup.com (free plan)
- [ ] You become the workspace owner
- [ ] Collect everyone's email addresses for invitations

---

## Step 1: Create the Workspace

1. Go to **clickup.com** → Sign up
2. Workspace name: **B-Ticket**
3. You are the owner/admin

---

## Step 2: Create 4 Spaces (One Per Department)

Go to **+ Create Space** for each:

### Space 1: IT Department
```
Space Name: IT Department
Color: Blue
```

**Lists inside this Space:**
| List Name | Purpose |
|-----------|---------|
| Current Development | All active development work (features, design handoffs) |
| Bugs | Bug reports and fixes |

### Space 2: Design Department
```
Space Name: Design Department
Color: Purple
```

**Folders and Lists:**
| Folder | List Name | Purpose |
|--------|-----------|---------|
| B-Ticket | Design Requests | All incoming B-Ticket design work |
| B-Ticket | Merchant Materials | Posters, banners, menus for B-Ticket merchants |
| B-Ticket | Other (Daimasu, Midori, etc.) | Design work for other businesses |

### Space 3: Sales Department
```
Space Name: Sales Department
Color: Orange
```

**Lists inside this Space:**
| List Name | Purpose |
|-----------|---------|
| Merchant Leads | New merchant prospects being pitched |
| Onboarding | Merchants being set up (photos, HubSpot, app) |
| Account Management | Monthly coupon reviews, merchant health |

### Space 4: Marketing Department
```
Space Name: Marketing Department
Color: Green
```

**Folders and Lists:**
| Folder | List Name | Purpose |
|--------|-----------|---------|
| B-Ticket | Campaigns | Marketing campaigns (each campaign = 1 task with subtasks) |
| B-Ticket | Content Calendar | Individual content pieces (posts, videos, articles) |
| B-Ticket | Paid Ads | Ad campaigns with budget tracking |
| B-Ticket | Other (Daimasu, Midori, etc.) | All marketing work for other businesses |

---

## Step 3: Set Up Statuses (Same for All Spaces)

Apply the same 4 statuses to every Space:

```
● To Do (Gray)
● In Progress (Blue)
● Review (Yellow)
● Done (Green)
```

**How to set:** Space Settings → Statuses → Custom Statuses → Add the 4 above.

Do NOT add extra statuses in the first month. 4 is enough.

---

## Step 4: Create Tags for Cross-Department Requests

Tags are how you track when one department needs something from another.

Go to **Space Settings → Tags** and create these in every Space:

| Tag | Color | When to Use |
|-----|-------|-------------|
| `needs-IT` | Blue | Task requires IT help |
| `needs-design` | Purple | Task requires Design help |
| `needs-sales` | Orange | Task requires Sales help |
| `needs-marketing` | Green | Task requires Marketing help |
| `cross-dept` | Red | General cross-department task |
| `blocked` | Red | Task is stuck, needs attention |

---

## Step 5: Task Template Per Department

Teach leads to create tasks with these fields:

### Every Task Should Have:
| Field | Required? | Example |
|-------|-----------|---------|
| Task name | Yes | "Create banner for ABC Restaurant promo" |
| Assignee | Yes | @designer-name |
| Priority | Yes | Urgent / High / Normal / Low |
| Due date | Yes | March 15 |
| Description | Yes | What needs to be done, specs, context |
| Tags | If cross-dept | `needs-marketing` |

### Subtasks (Optional But Useful)
Break big tasks into steps:
```
Task: Onboard XYZ Café
  ├── Subtask: Collect photos from merchant
  ├── Subtask: Confirm operating hours
  ├── Subtask: Get contract signed
  ├── Subtask: Create HubSpot record
  ├── Subtask: Add merchant to B-Ticket app
  ├── Subtask: Set up coupons in app
  └── Subtask: Notify merchant they're live
```

---

## Step 6: Sample Tasks Per Department

### IT — Sample Tasks
```
Task: Fix login crash on Android
  Priority: Urgent
  Assignee: @dev-name
  Due: March 5
  List: Bugs

Task: Build merchant dashboard v2
  Priority: High
  Assignee: @dev-name
  Due: March 20
  List: Current Development
  Subtasks: API endpoint, frontend, testing, deployment

Task: Implement push notification for promos
  Priority: Normal
  Assignee: @dev-name
  Due: March 25
  List: Current Development
  Tags: needs-marketing (for notification copy)
```

### Design — Sample Tasks
```
Task: Create poster for Jollibee promo
  Priority: High
  Assignee: @designer-name
  Due: March 10
  List: Merchant Materials

Task: March payday campaign visuals (5 assets)
  Priority: High
  Assignee: @designer-name
  Due: March 14
  List: Design Requests
  Tags: needs-marketing (for campaign brief)
  Subtasks: Facebook banner, IG story, IG post, TikTok cover, App banner
```

### Sales — Sample Tasks
```
Task: Pitch ABC Restaurant — Makati
  Priority: High
  Assignee: @sales-name
  Due: March 8
  List: Merchant Leads

Task: Onboard XYZ Café
  Priority: High
  Assignee: @onboarding-ops
  Due: March 12
  List: Onboarding
  Subtasks: (use the 7-step checklist)

Task: Monthly review — 10 merchants
  Priority: Normal
  Assignee: @account-mgmt-ops
  Due: March 30
  List: Account Management
```

### Marketing — Sample Tasks
```
Task: March Payday Promo Campaign
  Priority: High
  Assignee: @marketing-lead
  Due: March 15-31
  List: Campaigns
  Tags: needs-design, needs-IT
  Subtasks: Campaign brief, social posts, paid ads, landing page, push notification

Task: TikTok video — How to redeem coupons
  Priority: Normal
  Assignee: @content-creator
  Due: March 10
  List: Content Calendar
```

---

## Step 7: Your Manager Dashboard

This is the most important step — your single view of everything.

### How to Create
1. Click **Dashboards** in the left sidebar
2. Click **+ New Dashboard**
3. Name it: **B-Ticket — All Departments**
4. Add these widgets:

### Dashboard Widgets

**Widget 1: Status Overview (Pie Chart)**
- Type: Status pie chart
- Filter: All Spaces
- Shows: How many tasks in each status across all departments

**Widget 2: Tasks by Space (Bar Chart)**
- Type: Bar chart by Space
- Filter: Status ≠ Done
- Shows: How much active work per department

**Widget 3: Overdue Tasks (Task List)**
- Type: Task list
- Filter: Due date < today, Status ≠ Done
- Sort: By due date (oldest first)
- Shows: Everything that's missed its deadline

**Widget 4: Cross-Department Requests (Task List)**
- Type: Task list
- Filter: Tags contains any of (needs-IT, needs-design, needs-sales, needs-marketing), Status ≠ Done
- Shows: All pending cross-team requests

**Widget 5: High Priority (Task List)**
- Type: Task list
- Filter: Priority = Urgent or High, Status ≠ Done
- Shows: What's most important right now

**Widget 6: Recently Completed (Task List)**
- Type: Task list
- Filter: Status = Done, Date completed = this week
- Shows: What got shipped this week (useful for Monday sync)

---

## Step 8: Views to Set Up

ClickUp free tier gives you multiple views. Set these up:

### Board View (Default — Every Space)
The kanban board everyone uses daily. Already set up by default.

### List View (For You)
Shows all tasks in a sortable list. Good for scanning quickly.

### Calendar View (For Marketing and Design)
Shows tasks on a calendar by due date. Helpful for content calendars and campaign planning.

**How to add views:** Open any Space → Click **+ View** → Select the view type.

---

## Step 9: Invite Team Members

### Permission Levels
| Person | Role | Access |
|--------|------|--------|
| Sheena | Owner | Everything |
| Department leads | Admin (their Space) | Full control of their Space, view other Spaces |
| Staff | Member | Their own Space only |

### Invite Order (Staggered)
| Day | Who | Why |
|-----|-----|-----|
| Day 1 (Monday) | Department leads only | Let them explore, create test tasks, ask questions |
| Day 3 (Wednesday) | All staff | Leads help their teams onboard |

### How to Invite
1. Click your workspace name → **Settings** → **People**
2. Click **Invite** → Enter email → Set role
3. Assign them to their Space

---

## Step 10: Rollout Plan (1 Week)

| Day | Action |
|-----|--------|
| **Monday** | Create workspace, all 4 Spaces, lists, statuses, tags |
| **Tuesday** | Build your dashboard, set up views, create sample tasks |
| **Wednesday** | Invite leads, send walkthrough message, DM each lead |
| **Thursday** | Leads explore, create real tasks, ask questions. You answer in 1-on-1 or DM |
| **Friday** | Invite all staff. Leads help their teams. Post announcement in Staff GC |
| **Next Monday** | Everyone uses ClickUp for real. Review dashboard in Monday sync |

---

## Day-to-Day Usage After Rollout

### For Staff (2 minutes/day)
1. Open ClickUp → Go to your Space
2. Check your assigned tasks
3. Move tasks to the right column as you work
4. Create new tasks when you get new work

### For Leads (5 minutes/day)
1. Review their team's board — anything stuck?
2. Assign new tasks, set priorities and due dates
3. Tag cross-department requests
4. Move completed tasks to Done

### For You — Sheena (5 minutes/day, 10 minutes on Monday)
1. **Daily:** Open dashboard → check overdue + cross-dept requests
2. **Monday:** Full dashboard review before Monday sync. Bring findings to the meeting
3. **Friday:** Check "Recently Completed" widget for the weekly wrap-up

---

## Integration with Your Other Workflows

| Workflow | How ClickUp Connects |
|----------|---------------------|
| **Daily GC reports** | GC = quick updates and communication. ClickUp = task status. Don't duplicate. |
| **Monday sync** | Pull from dashboard: overdue tasks, cross-dept requests, completed work |
| **Weekly reports** | Leads can reference ClickUp data when filling the Google Sheets report |
| **1-on-1s** | Review the lead's board together — what's stuck, what's the backlog |
| **Monthly review** | Pull completion stats from ClickUp for each department |

---

## Telegram Messages

### Management GC: Announce ClickUp to Leads
```
Hey leads!

We're going to start using ClickUp to track work across all departments.

Why: Right now it's hard to see what's in progress, what's blocked, and what teams need from each other. ClickUp gives us one place to track everything — and I get a dashboard to see all 4 departments at a glance.

Your boards will be simple. Just 4 columns: To Do → In Progress → Review → Done. You drag tasks across as you work.

I'll set up everything this week and invite you first so you can explore before your team joins.

Free plan — no cost to the company.

Questions? Ask away!
```

### DM to Each Lead: Personal Walkthrough
```
Hey [name]!

I'm setting up ClickUp for all departments. I've created a Space for [Department] with these lists:

- [List 1]
- [List 2]
- [List 3]

You'll get an invite tomorrow. Take 10 minutes to explore, create a few test tasks, and let me know if anything is confusing.

On [day], I'll invite your team. I'd like you to walk them through it — just show them how to create a task, assign it, and move it across columns.

Quick start:
1. Create a task → give it a name, assignee, due date, and priority
2. Drag it from To Do → In Progress when you start
3. Drag to Review when it needs approval
4. Drag to Done when it's finished

If you need something from another department, add a tag like "needs-IT" or "needs-design" and I'll see it on my dashboard.

That's it! Simple as that.
```

### Staff GC: Announce ClickUp to Everyone
```
Hey team!

Starting this week, we're using ClickUp to track our work across all departments. Your lead will walk you through it — it's simple.

What this means for you:
- Your tasks go into ClickUp
- Drag them across columns as you work: To Do → In Progress → Review → Done
- If you need something from another department, your lead will tag it

This doesn't replace our daily GC updates — you still post in the GC. ClickUp is for tracking WHAT we're working on. The GC is for quick communication.

Your lead will show you how it works. It takes about 5 minutes to learn.

Let's go team!
```

---

## Red Flags After Launch

- **Tasks have no due dates** — people aren't planning, just dumping tasks
- **Same task in "In Progress" for 2+ weeks** — too big or abandoned, needs to be broken down
- **Cross-dept tags pile up** — departments are ignoring requests from other teams
- **One person has 15+ tasks assigned** — overloaded, needs help
- **A department stops using ClickUp** — fix immediately, talk to the lead
- **Tasks only move to Done on Fridays** — people batch-update instead of using it daily

## What NOT to Do
- Don't add custom statuses, automations, or extra fields in the first month
- Don't make ClickUp replace the daily GC — they serve different purposes
- Don't check the dashboard hourly — once a day is enough
- Don't create tasks for your leads — they manage their own boards
- Don't skip the staggered rollout — leads first, then staff
