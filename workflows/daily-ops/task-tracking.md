# Task Tracking System

## Purpose
Know what every department is working on, what's on track, and what's at risk — without micromanaging. You need visibility, not control over every task.

## When
- Set up once, then maintain continuously
- Review task boards during weekly syncs
- Deep review monthly to clean up stale items

## Steps: Setting Up Task Tracking

### Step 1: Choose Your Tool
Since the team uses Telegram, keep it simple. Pick ONE:

**Option A: Google Sheets (Recommended for starting out)**
- Free, everyone can access it, works on mobile
- One sheet per department, shared with leads
- You get a dashboard view across all departments

**Option B: Trello (Free tier)**
- Visual board with cards (To Do → In Progress → Done)
- Good for Design and IT who think visually
- Free for up to 10 boards

**Option C: Notion (Free for small teams)**
- Combines docs + task tracking
- More powerful but steeper learning curve
- Good if the team will actually adopt it

### Step 2: Set Up the Structure (Per Department)
Each department gets columns/stages:

```
Backlog → This Week → In Progress → Review → Done
```

Each task should have:
- **Title** — What is it? (clear, specific)
- **Owner** — Who's responsible?
- **Priority** — High / Medium / Low
- **Due date** — When is it expected?
- **Status** — Which column is it in?
- **Dependencies** — Waiting on another team? Tag it

### Step 3: Establish the Rhythm
- **Monday:** Leads update their task boards before the weekly sync
- **Daily:** Team members move their tasks as they progress
- **Friday:** Mark completed tasks as Done, move incomplete to next week
- **Monthly:** Archive completed tasks, review backlog for relevance

### Step 4: Your Dashboard View
Create a simple summary you check weekly:

| Department | Total Tasks | On Track | At Risk | Blocked |
|------------|-------------|----------|---------|---------|
| IT | | | | |
| Design | | | | |
| Sales | | | | |
| Marketing | | | | |

## Templates

### Google Sheet: Task Tracker (Per Department)
```
Columns:
A: Task Name
B: Owner
C: Priority (High/Medium/Low)
D: Status (Backlog/This Week/In Progress/Review/Done)
E: Due Date
F: Dependencies (blank or "Waiting on [team/person]")
G: Notes

Color coding:
- Red row = Blocked or overdue
- Yellow row = At risk (due this week, not in progress)
- Green row = On track
- Gray row = Done (move to archive sheet monthly)
```

### Telegram: Weekly Task Board Reminder
```
Reminder to all leads:

Please update your department task board before tomorrow's sync.

For each task:
- Move completed items to Done
- Flag anything blocked or at risk
- Add new tasks for this week

Links:
- IT: [sheet link]
- Design: [sheet link]
- Sales: [sheet link]
- Marketing: [sheet link]
```

### Telegram: When a Task is Blocked
```
BLOCKED: [Task name]

Department: [which]
Owner: [who]
Blocked by: [what's in the way]
Impact: [what happens if this stays blocked]
Need: [specific request to unblock]

@[person who can help] — can you look at this today?
```

## Prioritization Framework

When everything feels urgent, use this quick filter:

```
1. Is the app down or a merchant can't operate?     → Do it NOW
2. Does it directly affect revenue this week?         → High priority
3. Is another team blocked waiting for this?          → High priority
4. Does it support a quarterly goal?                  → Medium priority
5. Is it nice to have but nothing breaks without it?  → Low priority / Backlog
```

Share this framework with your department leads so they prioritize consistently.

## Red Flags
- Task board hasn't been updated in 2+ weeks — the team abandoned it
- Everything is "High priority" — nothing is actually prioritized
- Tasks sit "In Progress" for weeks — they're either too big (break them down) or stuck
- No one uses the tool — it's too complex or wasn't adopted properly
- You're the only one updating the board — leads need to own their department's tracking
- Backlog grows but nothing gets archived — creates overwhelm and noise

## Tips
- Start with Google Sheets — you can always upgrade later
- Don't track everything — only track work that matters for weekly/monthly goals
- Make updating the board a habit, not a chore — tie it to the Monday sync
- If a task is bigger than 1 week, break it into subtasks
- Review the backlog monthly — delete anything that's been there 2+ months and no one misses it
