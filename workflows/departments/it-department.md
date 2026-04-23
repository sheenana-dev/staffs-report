# IT Department Management

## Purpose
Keep B-Ticket's platform stable, shipping features, and technically healthy. The IT team builds and maintains everything users and merchants interact with — mobile apps, web platform, backend APIs, infrastructure, and UI/UX design. UI/UX sits within IT (not the Design department) so product decisions stay close to the people building them.

## When
- Daily standups (async via Telegram or 15-min call)
- Sprint planning every 2 weeks
- Sprint retrospective at end of each sprint
- Monthly technical review with you

## Steps: How to Manage IT

### Daily (5 minutes)
1. Check the Staff GC and Management GC for IT-related blockers or urgent issues
2. If something is down (app crash, server issue), ask: "What's the impact? When will it be fixed?"
3. Don't micromanage the how — focus on whether work is moving

### Every 2 Weeks: Sprint Planning
1. Meet with the IT lead 30 minutes before sprint planning to align priorities
2. Ask: "What are the top 3 things we need to ship this sprint?"
3. Ensure at least 1 item ties back to a business goal (merchant feature, user growth, etc.)
4. Leave 20% buffer for bugs and unplanned work — this is normal in IT
5. Document the sprint goals in the Management GC (leads) and Staff GC (whole team)

### Every 2 Weeks: Sprint Retrospective
1. Ask the team 3 questions:
   - What went well?
   - What didn't go well?
   - What should we change?
2. Pick ONE improvement to implement next sprint (not five)
3. Follow up on last sprint's improvement — did it actually help?

### Monthly: Technical Health Check
1. Review these with the IT lead:
   - Any recurring bugs or outages?
   - Is technical debt growing? What's the risk?
   - Are we using the right tools and services?
   - Any security concerns?
2. You don't need to understand the technical details — focus on risk and impact

## Templates

### Telegram: Daily Standup Prompt
```
Good morning IT team!

Quick check-in:
- What are you working on today?
- Any blockers?

Tag me if you need anything unblocked.
```

### Telegram: Sprint Goals Announcement
```
Sprint [number] Goals (Mar 1-14):

1. [Feature/task name] — [why it matters]
2. [Feature/task name] — [why it matters]
3. [Feature/task name] — [why it matters]

Buffer: Bug fixes + maintenance

Let's ship it!
```

### Telegram: After an Outage/Incident
```
Update on today's [issue]:

What happened: [brief description]
Impact: [who was affected]
Status: [resolved / being fixed]
Next steps: [what we're doing to prevent it]

Thanks to [person] for jumping on this.
```

## Key Metrics to Watch
- **Uptime** — App and API should be 99%+ available
- **Bug resolution time** — Critical bugs fixed within 24 hours
- **Sprint completion rate** — Are we finishing what we planned? (70-80% is healthy)
- **Deployment frequency** — How often we ship updates (weekly is good)
- **App store rating** — Below 4.0 needs attention
- **UX task turnaround** — UI/UX design to implementation cycle time

## Red Flags
- The same bug keeps coming back — indicates a deeper architectural problem
- Sprint completion rate below 50% — either scope is too ambitious or team is blocked
- No deployments in 2+ weeks — something is stuck
- Team avoids retrospectives — they've stopped believing things can improve
- One person is a bottleneck for everything — knowledge isn't shared
- Security issues being deprioritized — this can become a crisis fast

## What NOT to Do
- Don't assign specific tasks to developers — that's the IT lead's job
- Don't ask for daily progress reports on every ticket — trust the sprint process
- Don't push to skip testing to ship faster — it always backfires
- Don't compare IT velocity to Sales numbers — they measure different things
