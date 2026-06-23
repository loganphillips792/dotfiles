---
name: sql-query-analyzer
description: >-
  Analyze SQL queries for performance, correctness, security, and style issues,
  then return a severity-ranked findings report plus an optimized rewrite. Use
  this skill whenever the user shares a SQL query or .sql file and wants a
  review, optimization, debugging help, or a second opinion — including casual
  phrasings like "why is this query slow", "is this query right", "what's wrong
  with this SQL", "clean this up", or "can this be faster". Trigger on query
  tuning, EXPLAIN-style questions, and "review my query" requests even when the
  user never says the word "analyze".
---

# SQL Query Analyzer

Review a SQL query statically (no database connection) across four lenses —
performance, correctness, security, and style — and hand back a ranked findings
report together with a corrected/optimized rewrite.

The goal is to be the careful senior reviewer the user wishes they had: catch
the bug that returns wrong data, the missing index pattern that makes it crawl,
the injection hole, and the sloppiness — and explain *why* each one matters so
the user learns, not just complies.

## Workflow

1. **Gather context.** You need the query itself. Two things are *optional but
   valuable* — ask for them only if they're cheap to get and would change your
   findings, otherwise proceed and state your assumptions:
   - **Dialect** — default to generic ANSI SQL. If the query uses obviously
     dialect-specific syntax (e.g. `LIMIT`, `ILIKE`, backticks, `::` casts),
     note which dialect you're assuming.
   - **Schema / DDL** — if the user provides table definitions, use them to
     reason about indexes, column types, nullability, and cardinality. Without
     a schema, you can still flag patterns; just be explicit that index advice
     is provisional.

   Don't block the analysis waiting for these. A useful review of the query
   alone beats no review.

2. **Analyze across all four lenses.** Read the matching reference file for the
   detailed checklist and the reasoning behind each check. Run every applicable
   check, not just the obvious one — a query can be fast but wrong, or correct
   but injectable.
   - `references/performance.md` — scans, joins, subqueries, index usage, `SELECT *`
   - `references/correctness.md` — join logic, NULLs, GROUP BY, aggregates, cartesian products
   - `references/security.md` — injection surface, parameterization, privilege scope
   - `references/style.md` — readability, naming, portability, maintainability

3. **Produce the report** in the exact structure below.

## Severity scale

Rank every finding so the user knows what to fix first. Judge by *impact if
left as-is*, not by which lens it came from.

- **CRITICAL** — returns wrong results, or is exploitable (e.g. injection,
  silent cartesian product, an aggregate over the wrong grain).
- **HIGH** — works today but will perform badly at scale, or is fragile in a
  way that's likely to break (e.g. full scan on a large table, `NOT IN` with a
  nullable column).
- **MEDIUM** — real improvement but not urgent (e.g. a subquery that reads
  better as a join, missing an index hint worth suggesting).
- **LOW** — style and polish (e.g. `SELECT *`, inconsistent casing, implicit
  join syntax).

## Report structure

Use this template exactly. Lead with the verdict so a busy reader gets the
headline first.

```markdown
# SQL Query Analysis

## Summary
One or two sentences: is the query correct? fast enough? safe? Then a count,
e.g. "3 findings: 1 critical, 1 high, 1 low."

## Findings
For each finding, in severity order (critical first):

### [SEVERITY] Short title
- **Where:** the offending clause/line (quote the snippet)
- **Why it matters:** the concrete consequence — wrong data, slow at N rows, exploitable
- **Fix:** what to change and why that resolves it

## Optimized query
```sql
-- the corrected / optimized version
```
A short note on what changed and the expected effect.

## Assumptions & caveats
Dialect assumed, schema assumed/unknown, anything you couldn't verify statically
(e.g. "index advice assumes `orders.user_id` is unindexed — confirm against your
schema").
```

## Guidance on judgment

- **No findings is a valid result.** If the query is genuinely fine, say so
  plainly and skip the rewrite rather than inventing nitpicks. A trustworthy
  reviewer doesn't manufacture problems.
- **Preserve intent in the rewrite.** The optimized query must return the same
  logical result as the original (unless the original is *buggy*, in which case
  fix the bug and call out that the results will now differ — that's the point).
- **Explain, don't decree.** "Avoid `SELECT *`" is weak. "`SELECT *` here pulls
  the 2KB `description` blob you never use, inflating row size and preventing a
  covering index — list the four columns you actually read" teaches the why.
- **Static limits are real.** You can't see the data distribution or the actual
  plan. When a finding depends on cardinality you don't know, frame it as
  conditional ("if `status` has few distinct values, this index won't help")
  rather than asserting it.
