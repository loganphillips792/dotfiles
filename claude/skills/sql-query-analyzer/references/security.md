# Security checklist

Static SQL review can't see the application, but it can spot the patterns that
make a query injectable or over-privileged. Be precise about *what makes it
unsafe* and *what makes it safe* — vague "use prepared statements" advice
doesn't help someone who thinks they already are.

## SQL injection surface
The core question: is any part of this query built from untrusted input via
string concatenation rather than a bound parameter?

- **String-concatenated values** — `... WHERE name = '" + userInput + "'"` or
  f-strings/`%`-formatting/`${}` interpolation that splice a value into the SQL
  text. CRITICAL. The fix is a **bound parameter** (`?`, `:name`, `%s` with a
  params tuple — dialect/driver dependent), which sends the value separately
  from the SQL so it can never be parsed as SQL.
- **Identifiers can't be parameterized.** Table/column names and `ORDER BY`
  columns interpolated from input are still injectable even if values are bound.
  These must be validated against an allowlist, not parameterized.
- **`LIKE` with user input** — still needs binding; also escape `%`/`_` if the
  user shouldn't control wildcards.
- **`IN (...)` lists** — building the list by concatenation is injectable; bind
  each element or use an array parameter.
- **Dynamic SQL / `EXEC`/`sp_executesql`** built from input — high risk; flag
  and recommend parameterization within the dynamic statement.

If the query is a plain static string with no interpolation, say it has no
injection surface — don't cry wolf.

## Quoting/escaping anti-patterns
- Manual quote-escaping (doubling `'`) instead of binding — brittle and
  bypassable (e.g. via encoding tricks). Treat as injectable; recommend binding.
- Comments (`--`, `/* */`) or stacked queries (`;`) appearing in a value
  position is a red flag for an active injection or a test thereof.

## Privilege & exposure
- `SELECT *` on tables holding sensitive columns (password hashes, tokens, PII,
  full card numbers) exposes data the caller may not need — list columns and
  exclude secrets.
- `DELETE`/`UPDATE` with **no `WHERE`** (or a `WHERE` that's always true) — wipes
  or rewrites the whole table. CRITICAL. Confirm intent and recommend a guard.
- `GRANT`/broad permissions, `DROP`, or DDL mixed into what should be a read
  path — flag privilege scope.
- Returning password hashes, API keys, or tokens in a result set that feeds a
  client/UI.

## Defense-in-depth notes (mention when relevant, don't overload)
- Least-privilege DB account for the query's purpose (read-only where possible).
- Row-level security / tenant scoping: a multi-tenant query missing its
  `tenant_id` filter is both a correctness and a security bug.
