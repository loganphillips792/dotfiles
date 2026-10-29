---
name: repo-overview
description: Write or refresh REPO_OVERVIEW.md, an onboarding guide to a whole repository for a developer who is new to it (summary, architecture, directory guide, ranked end-to-end flows, data models, APIs, config, testing, gotchas). If REPO_OVERVIEW.md already exists, audits it against the current code and fixes anything stale. Use when asked to document a repo, onboard someone to a codebase, explain how a project is structured, or update/refresh an existing repo overview.
---

# Repo overview: $ARGUMENTS

You are documenting this repository for a developer who is new to it. Your goal is to help them understand what the system does, how it's structured, how the main flows work end to end, and how data is modeled.

## Pick a mode first

Look for `REPO_OVERVIEW.md` at the repo root (or at the path given in `$ARGUMENTS`, if any).

- **No file** → **Create mode**: follow every section below from "How to work" on.
- **File exists and has the defined structure** (headings for sections 1–10 as listed under "Document structure", in order, give or take wording) → **Update mode**: follow "Update mode" at the end.
- **File exists but does not follow the structure** → stop and ask whether to rewrite it in this structure or leave it alone. Don't overwrite it without an answer.

## How to work
- Explore before writing. Start with the README, package/dependency manifests (package.json, pyproject.toml, go.mod, Gemfile, pom.xml, etc.), config files, entry points, and the top-level directory structure.
- Trace real code paths. Don't infer behavior from file or function names alone. When you describe a flow, you should have read the code that implements it.
- Cite file paths (and function/class names) for every significant claim so the reader can jump to the source.
- If something is unclear, ambiguous, or appears unused/dead, say so explicitly rather than guessing.
- Prefer accuracy over completeness. Skip trivial files; focus on what matters for understanding the system.

## Document structure

Produce a single Markdown document (`REPO_OVERVIEW.md`) with these sections.

### 1. Summary
- What this project is and what problem it solves (2–4 sentences)
- Tech stack: languages, frameworks, major libraries, databases, external services
- How to run it locally (from what you can find in scripts/config/docs)

### 2. Architecture
- High-level components/layers and how they interact (e.g., API, workers, frontend, DB, queues, third-party services)
- Include a Mermaid diagram of the architecture
- Key design patterns or conventions used in the codebase

### 3. Directory & File Guide
- Annotated tree of important directories and files (not every file)
- For each: its responsibility in one line
- Identify entry points (main files, server startup, CLI commands, cron/job definitions)

### 4. Core Functionality
- List the main features/capabilities of the system
- For each: what it does, where it lives (files/modules), and key functions/classes

### 5. Main Flows

#### 5a. Flow Inventory
Systematically enumerate every end-to-end flow by scanning all entry points, not just the obvious ones. Check for:
- HTTP routes/controllers/handlers (REST, GraphQL resolvers, RPC)
- UI actions that trigger backend work (forms, buttons, page loads)
- Background jobs, workers, queue consumers
- Scheduled tasks / cron jobs
- Webhook and event handlers (incoming from third parties or internal event buses)
- CLI commands, scripts, and management tasks
- Database triggers, model lifecycle hooks/callbacks, and signals
- Startup/initialization and shutdown logic

Group closely related entry points into a single flow where they form one user or system journey (e.g., "request password reset" + "confirm reset" = one password reset flow).

Present the inventory as a table with columns:
| Flow | Trigger type | Entry point (file:function) | Models touched | External services | Rank score |

#### 5b. Ranking
Score each flow 1–3 on these criteria and show the scores so I can see your reasoning:
- **Centrality**: Is it part of the product's core purpose, or peripheral/admin?
- **Data impact**: Does it create, modify, or delete important records (especially money, user accounts, permissions)?
- **Reach**: How much of the codebase does it touch (number of modules, models, services)?
- **Frequency**: How often is it likely to run (every request, per user action, rare admin task)? Base this on evidence in the code (e.g., middleware, cron schedule), not assumption.
- **Risk**: Does it involve auth, payments, external integrations, concurrency, or irreversible actions?

Sort the table by total score. Note any flow where you were uncertain about a score and why.

#### 5c. Detailed Walkthroughs
For the top-ranked flows (at least the top 7, more if the scores are close), document:
- Trigger (HTTP route, event, job schedule, UI action)
- Step-by-step path through the code, with file/function references
- Data read or written along the way
- Error handling and notable edge cases
- A Mermaid sequence diagram

For all remaining flows, give a 2–3 sentence summary with entry point references so nothing is left undocumented.

### 6. Data Models
- Every database model/table/collection/schema: name, purpose, key fields and types, constraints, indexes if defined
- Relationships between models (one-to-many, many-to-many, foreign keys)
- A Mermaid ER diagram
- Where migrations live and how schema changes are made
- Any non-DB persistent state (caches, file storage, queues)

### 7. APIs & Interfaces
- Public endpoints/routes (method, path, purpose, handler location)
- Authentication/authorization approach
- External integrations and where they're called

### 8. Configuration & Environment
- Environment variables and config files, what each controls
- Differences between environments (dev/staging/prod) if visible

### 9. Testing
- Test framework(s), where tests live, how to run them
- Rough sense of what is well-tested vs. not

### 10. Gotchas & Open Questions
- Confusing, surprising, or fragile areas of the code
- Tech debt, TODOs, dead code, or inconsistencies you noticed
- Questions a new developer should ask the team

End the document with a footer line: `_Last verified against commit <short SHA> on <YYYY-MM-DD>._` (from `git rev-parse --short HEAD`). Update mode uses it as the baseline.

## Checkpoint before writing
Before writing the detailed walkthroughs (5c) and the rest of the document, stop and show me:
1. The full flow inventory and ranking table (5a and 5b)
2. The list of data models you've identified

Wait for me to adjust scores, add or remove flows, or pick which flows to go deep on before continuing.

## Update mode

The document already exists. Your job is to make it true of the code as it is now, changing only what is stale, wrong, or missing. Don't rewrite accurate prose for style.

### 1. Find what changed
- Baseline commit: the SHA in the "Last verified" footer. If there is no footer, use the last commit that touched the doc: `git log -1 --format=%H -- REPO_OVERVIEW.md`.
- Run `git diff --stat <baseline>..HEAD` and `git log --oneline <baseline>..HEAD` to see which areas moved. Use this to prioritize, not to limit: uncommitted edits and changes made before the doc's last commit can also leave it stale.

### 2. Audit every section against the code
Check each claim, not just the ones near changed files:
- **Citations**: every cited file path, function, class, route, and model still exists under that name and still does what the doc says. Fix renamed or moved references; remove ones that are gone.
- **Summary/stack/run steps**: compare against current manifests, lockfiles, scripts, and docs (new or dropped dependencies, changed run commands).
- **Architecture & directory guide**: new, removed, or restructured top-level directories, components, services, or entry points. Update the Mermaid diagram if components or their connections changed.
- **Core functionality**: features added or removed.
- **Flows**: rerun the 5a entry-point scan. Find flows that are new, removed, or whose path changed (different steps, models, services, error handling). Re-check each walkthrough step by step against the code, and update its sequence diagram when the steps change.
- **Ranking**: keep existing scores unless the code now gives a reason to change them. The user may have tuned them by hand. Score new flows with the same criteria. If a re-sort pushes a flow into or out of the top tier, flag it.
- **Data models**: compare against current models, schemas, and migrations: new or dropped models, fields, types, constraints, indexes, relationships. Update the ER diagram to match.
- **APIs, config/env vars, testing**: new or removed endpoints, auth changes, env vars, config files, test frameworks, test locations, coverage shifts.
- **Gotchas**: drop items that have been fixed (resolved TODOs, deleted dead code). Add new ones you notice.

### 3. Checkpoint on structural changes
If the audit finds flows added or removed, rank changes that alter which flows get detailed walkthroughs, or models added or removed, stop and show me:
1. The updated inventory and ranking table, with new/removed/changed rows marked
2. The updated model list, with changes marked

Wait for my input before writing new walkthroughs or deleting old ones. If nothing structural changed, skip the checkpoint and go straight to editing.

### 4. Edit in place
- Edit the existing file section by section. Keep section order, headings, and any content you verified as still accurate.
- Follow the same rules as create mode: trace real code, cite paths, flag uncertainty.
- Update the "Last verified" footer to the current commit and date.

### 5. Report
Reply with a short changelog grouped by section: what was stale and what you changed, plus anything you couldn't verify. If everything was already accurate, say so, and update only the footer.
