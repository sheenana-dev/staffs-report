# CLAUDE.md — WAT Framework Project

## Architecture: WAT (Workflows, Agents, Tools)

This project uses the WAT architecture to separate concerns:

- **Workflows** (markdown SOPs in `workflows/`) — define objectives, inputs, tool sequences, expected outputs, and edge cases
- **Agent** (Claude) — reads workflows, orchestrates tools, handles failures, asks clarifying questions
- **Tools** (Python scripts in `tools/`) — deterministic execution: API calls, data transforms, file ops, DB queries

**Core principle:** AI handles reasoning and coordination. Deterministic scripts handle execution. This separation keeps accuracy high across multi-step tasks.

## Operating Rules

### 1. Tools-First Approach
- Always check `tools/` for existing scripts before building anything new
- Only create new tools when no existing script covers the task
- Credentials and API keys live in `.env` — never store secrets elsewhere

### 2. Failure Recovery Loop
When something breaks:
1. Read the full error message and trace
2. Fix the script and retest (**if it uses paid APIs or credits, ask before re-running**)
3. Document what you learned in the relevant workflow
4. Verify the fix works before moving on

### 3. Workflow Maintenance
- Workflows evolve as we learn — update them when you find better methods or discover constraints
- **Do not create or overwrite workflows without asking** unless explicitly told to
- Workflows are persistent instructions, not disposable notes

## Directory Structure

```
.tmp/           # Temporary/intermediate files (disposable, regenerated as needed)
tools/          # Python scripts for deterministic execution
workflows/      # Markdown SOPs defining what to do and how
.env            # API keys and environment variables (NEVER commit)
credentials.json, token.json  # Google OAuth (gitignored)
```

## File Placement Rules

- **Deliverables** → cloud services (Google Sheets, Slides, etc.) where the user can access them directly
- **Intermediates** → `.tmp/` directory (disposable, can be regenerated)
- Everything in `.tmp/` is temporary — never treat it as a permanent store

## Key Conventions

- Before executing a multi-step task, find and read the relevant workflow in `workflows/`
- Run tools in the sequence the workflow specifies
- When a workflow doesn't exist for a task, ask before creating one
- Keep workflows updated with lessons learned (rate limits, timing quirks, API changes)
- Local files are for processing only — final outputs go to cloud services
