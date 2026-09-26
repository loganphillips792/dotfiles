---
name: feature-doc
description: Write a FEATURE.md "how it all fits together" guide for a feature in any repo and language. On a feature branch it also explains every change to existing files and why. Use when asked to document a feature, explain a branch, or produce a feature guide for someone who has not read the code.
---

# Feature guide: $ARGUMENTS

Arguments, all optional, in any order:

- **A branch name** (an argument that `git rev-parse --verify` accepts as a branch). Else the
  current branch.
- **An output path** (an argument ending in `.md`, or a directory).
- **A feature scope**: anything else, such as a feature name ("announcements"), a page, route,
  class or file to start from. Required in default-branch mode (below); optional otherwise.

Resolve before doing anything else:

- **Diff base:** the repo's default branch. Detect it with
  `git symbolic-ref refs/remotes/origin/HEAD`, falling back to `main`, then `master`.
- **Mode:**
  - **Branch mode** when the branch is not the default branch and
    `git rev-list --count <base>..<branch>` is greater than 0. The feature is what the branch
    changes. Uncommitted changes in the working tree count too if the branch is checked out;
    say so in the header when they exist.
  - **Default-branch mode** when the branch *is* the default branch, or has no commits beyond
    it. There is no diff to describe, so the feature scope argument decides what to document.
    If none was given, ask the user which feature to document and stop.
- **Output path:** the argument, else whatever the repo's CLAUDE.md or memory says feature docs
  go, else an earlier feature doc's location if one exists, else
  `docs/features/<branch-or-feature-slug>/FEATURE.md` in the repo. If a FEATURE.md already
  exists there, read it first and update it rather than starting over. Say which rule chose the
  path in your final message.

## Who it is for

Someone who has not read the code yet and may not know the stack or the language. The code may
have been written with AI assistance, so the reader is often reviewing code nobody on the team
typed by hand. They must finish the document able to explain:

- which files make up the feature, why each one exists, and (in branch mode) what changed in
  each pre-existing file and why;
- how every public member of the feature's core components is used, and by whom;
- how one request, event or job travels through the files end to end;
- every mechanism that runs without a visible caller (timers, polling, framework lifecycle
  hooks, dependency injection, event wiring, property getters that do work).

Explain each convention the code relies on (framework lifecycle, partial or generated files,
DI registration, routing, ORM or migrations, project/build registration) the first time it
matters, in the section where it matters, not in a glossary.

**Stay on this feature.** Do not describe other features, even ones the code interacts with.
If the diff contains changes that belong to something else, list them only in the "Unrelated
changes" table (section 2) so the reader knows to ignore them, with one line each and no
explanation of that other feature.

## Research before writing (do all of it; do not write from the diff summary alone)

1. **Find the files.**
   - Branch mode: `git diff <base>...<branch> --stat`, `git log <base>..<branch>`, and
     `git status` for uncommitted work.
   - Default-branch mode: start from the scope argument and follow references (grep for the
     names, routes, table names, config keys) until you have every file the feature uses.
     Record how you found them.
2. **Read every file in full,** plus the files that form one unit with it (markup + code-behind
   + generated file, component + template + styles, model + migration, handler + route + test,
   project/build files that register them).
3. **Branch mode: read the base version of every pre-existing file the branch changes**
   (`git show <base>:<path>`) and the full diff for it. For each hunk, work out *why* it
   changed. For every removal, prove what it was: search for callers of removed functions,
   triggers of removed handlers, readers of removed fields and settings. Record the searches
   and their results ("nothing calls `PerformCallback(\"X\")`; searched the whole repo"). Note
   any bug or side effect the removal fixes, and any behaviour it changes.
4. **Read everything the feature calls that it did not add:** base classes, middleware,
   decorators, the auth or permission check, service or manager classes, shared helpers,
   framework entry points, anything in a lower layer.
5. **Find every caller of every public member** of the feature's own code (`grep` across the
   repo) and record file:line for each. "Called from exactly one place" is a fact worth
   recording; so is "public but nothing calls it".
6. **Find every mechanism that invokes feature code without a direct call:** timers,
   intervals, polling, scheduled jobs, queue consumers, webhooks, framework lifecycle methods
   wired by name, event handlers wired in markup or configuration, DI registrations, property
   getters or setters that run code. For each, find where it is started or registered and
   what triggers it.
7. **Find existing code that does the same thing** (an older page or endpoint with the same
   pattern, a duplicate copy, a key or flag already set elsewhere, a field added earlier and
   never used) and say how the feature relates to it, including side effects on that older code.
8. **Read every config source the feature touches** (config files, env vars, settings modules,
   feature flags). Note which entries are new, changed, removed or pre-existing.
9. **Databases, queues, workers, scheduled jobs, external services:** if involved, read their
   code too and say whether it changed. Note what format values are stored in (time zones,
   units, encodings) and where that convention is enforced.
10. **Data-dependent decisions** (uniqueness of a column, how many rows share a value, how often
    a job runs): query the local environment if one is available and record the number with the
    date. Otherwise say the decision assumes it and mark it "(unverified)".
11. **Line numbers:** record the line of every member and every quoted line you describe.
    Verify each against the current file, not from memory.
12. **Companion docs** next to the output (changelog, test script, design notes, an earlier
    version of this guide): read them, link to them in the intro, and note anything in them the
    code has since made stale.

## Document structure

Number the sections sequentially, with a Contents list up front linking to each. Keep this
order. Section 3 exists only in branch mode; renumber the rest when it is absent.

1. **What the feature does.** The user's (or caller's) steps, numbered, in plain language, with
   real labels and example values. Then one paragraph on what they see when something goes wrong.

2. **The files, grouped by layer.** One table per layer the repo actually has (for example
   Database, Data/ORM, Domain/Business, API, UI, Scripts/Styles, Build/Solution, Workers), with
   columns File | What it does. In branch mode mark new files "(new)" and point pre-existing ones
   to section 3. End with an **Unrelated changes** table (File | One-line description | Action:
   revert or keep) for diff entries that are not part of the feature, if any. Call out anything
   a builder must do that the diff does not show (regenerate code, run a migration, install a
   package, register a file in a project or build file).

3. **What changed in existing files, and why.** *(Branch mode only.)* Start with a short
   paragraph on what existed before the branch. Then one subsection per pre-existing file the
   branch changes, titled with the file path and a few words on its role (for example
   "`MasterPages/MainLayout.Master` (the layout used by 174 pages)"). In each subsection:
   - number each change;
   - show **before** and **after** as code blocks, trimmed with `…` to the lines that matter,
     with the new line numbers;
   - follow each with an italic ***Why:*** that gives the actual reason: duplication removed,
     moved to a shared place (say where), dead code (cite the search that proves it), bug fixed
     (describe the symptom), convention matched, required by the new feature;
   - for removed code, say where its job is done now, or that nothing needed it;
   - for project, build, solution or registration files, explain what each added entry does and
     what breaks without it.
   Unrelated changes are not described here; they are only listed in section 2.

4. **How the framework pieces relate.** The stack conventions the feature depends on, using the
   feature's own files as examples: how split or generated files form one unit, how handlers are
   wired (by name, by decorator, by registration, by configuration), the request or component
   lifecycle as the feature uses it (what runs in which phase and why the feature's code sits
   where it does), what the base class or middleware does and why the feature overrides or
   bypasses it, and any language feature a newcomer would misread (property getters that do
   work, static vs. instance members, async, generated members). If an earlier feature doc in
   the same repo already explains a convention, link to it instead of repeating it.

5. **The core components: what they offer and who calls them.** For each central class, module,
   service or component the feature adds (the one most other files talk to):
   - **Its relationship to its callers:** a table of what each side knows about, does, and never
     touches (for example UI code-behind vs. business/service class), and how callers obtain it
     (constructor injection, a property on a shared object, a static call, an import).
   - **Every use from each caller:** a table Line | Code | Purpose.
   - **One subsection per public member,** titled with its signature and a few words on its job:
     the code (or its essential lines), every caller as file:line, the **exact calling line
     quoted**, with each argument mapped to the parameter it becomes, what the member does as
     numbered steps, what happens on failure, and how its result reaches the user or the next
     system. Include a worked example with realistic values for anything that transforms data
     (input → output).
   - Unused public members and unused injected dependencies, stated as such.

6. **The end-to-end flow.** One **Mermaid `sequenceDiagram`** per leg of the flow (the main
   request, and each separate leg such as an async callback, a poll, an email link, a retry, a
   scheduled job). Requirements:
   - `autonumber` on, so the text can refer to "step 12";
   - one `participant` per real actor (browser or client, each handler or page, each service,
     the database, each worker or external system), aliased to the real file or class name;
   - messages use real function names, real arguments and real field assignments;
   - `Note over` to label phases ("First visit", "Admin clicks Publish"), `loop` for anything
     repeated (a timer, a retry, a per-row loop), `alt`/`else` for real branches;
   - dashed arrows (`-->>`) for returns, solid (`->>`) for calls.

   Mermaid syntax rules (a wrong character silently breaks rendering):
   - no `;` inside a line (it ends the statement), no `#` (entity codes), no `<` or `>` in
     message text: write `≤`, `≥`, "less than", or rephrase;
   - one message per line; keep each under about 90 characters;
   - put the diagram in a fenced block tagged `mermaid`.

   If a way to run Mermaid is available (mermaid-cli, Node with the `mermaid` package, or a
   browser tool that can import it), parse every diagram and fix any error before finishing.
   Otherwise re-read each diagram against the rules above.

7. **Deep dives,** one section each, titled "Deep dive: how X reaches Y" (or "how X works").
   Write one for **every** item in these categories that the feature contains; drop a category
   only if the feature has nothing in it:
   - **each data hand-off** (a value crossing a boundary: form → server, server → script,
     page → page, service → service, app → database → another process);
   - **each trigger mechanism** (timer, polling, scheduled job, queue consumer, webhook,
     lifecycle hook, event subscription): start where it is registered or started, and walk
     step by step to what it changes on screen or in data, quoting the code at each step;
   - **each transformation that is easy to get wrong** (time zones and daylight saving, money
     and rounding, encoding and escaping, units, identifiers that change format).

   In each deep dive, walk the value as numbered steps from where it is created to where it is
   consumed, quoting the exact line of code at each hop. Cover: what the value looks like (a
   real example), what encodes or escapes it, what happens on re-entry (postback, retry,
   refresh, re-render), why the chosen mechanism was picked over the alternatives, and what
   someone tampering with it would achieve. Where both an interactive path and a background path
   produce the same output (for example a preview and the real thing), show both paths and the
   shared code that keeps them identical.

8. **Security decisions baked into the design.** Bulleted. Each bullet: bold the decision, then
   the reason and the code that enforces it. Include endpoints reachable without login, checks
   done only in the UI, and what is *not* done (no throttling, no audit row, no idempotency key)
   and where it would go if wanted.

9. **Configuration and deployment.** Table Key / constant | Where | Used for, marking which are
   real settings and which are constants in code. Then numbered deploy steps in order: migration
   scripts, code generation, build, data already in production that the change affects, caches
   (browsers, CDNs) that may serve old code, and "no change needed" for systems that are
   involved but untouched.

10. **File-by-file trace.** Start with N.0: a numbered table of every request, event, or job
    invocation in one successful run and the code that runs for each, in call order, so every
    member in the feature appears at least once. When the trace shows a call that is not
    visible at the call site (a property getter, a framework hook, an injected dependency),
    say so in the row. Then one subsection per main file: a paragraph on how the file's entry
    point is reached and what causes re-entry, then a table Member (line N) | When it runs |
    What it does. "When it runs" must be precise about the lifecycle (every request / first
    render only / only on this event / after validation / every 60 s from the timer / on the
    worker's next poll) and name the caller. "What it does" is a numbered list of steps for
    anything longer than one action, and includes what happens on failure.

End with a **Known open issues** subsection if any are known, each marked "(unverified)" where
the cause has not been established.

## Style

- Plain declarative sentences. No marketing, no "robust", no "seamless".
- Facts, not paraphrase: real identifiers, real values, real line numbers, real counts.
- **No bare labels.** A step titled "Compare" or "Validate" must say what is compared or checked
  against what, in which code, why, and what goes wrong otherwise, with an example value.
- **Quote calls, don't summarise them.** When describing a call, quote the calling line and map
  each argument to the parameter it becomes, especially when an argument is computed inline.
- **Explain indirection.** The first time the document relies on a call that does not appear at
  the call site (property getter, lifecycle method, event wiring, DI, a timer), explain where it
  comes from.
- **Every change has a why.** In section 3 and anywhere else a change is mentioned, give the
  reason. "Removed" alone is not an explanation.
- When two things could be confused (a field added earlier vs. now; client-side vs. server-side
  validation; a preview vs. the real output; a file vs. the class it inherits), say which is which.
- When something is redundant on purpose (a check done twice), say so and why it exists anyway.
- Mark anything you could not verify with "(unverified)" rather than guessing.
- Tables for parallel facts, code blocks for anything the reader might copy or grep for, prose
  for explanation, Mermaid for flows. Wrap prose at about 95 columns.
- Header: title, then a line with Branch (or "Default-branch mode: feature as of commit
  `<sha>`"), diff base, absolute repo root, and "Last updated: <date>". Then an intro paragraph
  naming the companion docs, if any, and what each is for, and a short "How to read this guide"
  paragraph saying which sections answer which questions.

## Before finishing

Re-read the whole file against the code and fix what is wrong:

1. Every line number and every "called from" claim, checked against the current files.
2. Every cross-reference ("section 7") points at the right section after numbering.
3. Grep the document for identifiers the branch renamed or removed; only mention them as
   history ("before this change…").
4. Every Mermaid diagram parses (or has been checked against the syntax rules).
5. Nothing describes an unrelated feature.
6. In branch mode, every pre-existing file in the diff appears in section 3 or in the Unrelated
   changes table, and every new file appears in section 2.

Then report: the output path and which rule chose it, the mode, and anything you marked
"(unverified)".
