# Style & maintainability checklist

These are LOW severity by default — real but not urgent. Keep this section
short in the report; don't let polish drown out a correctness or perf finding.
Only raise a style point if it genuinely aids readability, portability, or
future correctness.

## Explicitness
- **Implicit (comma) joins** — `FROM a, b WHERE a.id = b.a_id` — hide the join
  condition and make accidental cartesian products easy. Prefer explicit
  `JOIN ... ON`.
- **`SELECT *`** in anything beyond ad-hoc exploration — column list documents
  intent, survives schema changes, and enables covering indexes. (Also a perf
  and security point; mention once, in the most relevant lens.)
- **Unqualified columns in a multi-table query** — prefix with table aliases so
  the source is unambiguous and the query survives a new same-named column.

## Naming & aliases
- Cryptic aliases (`a`, `b`, `t1`) hurt readability — short *meaningful*
  aliases (`u` for users, `o` for orders) are fine; one-letter-per-table is a
  reasonable convention. Flag only genuinely confusing ones.
- Consistent keyword casing (uppercase keywords / lowercase identifiers is the
  common convention) — flag only if inconsistency hurts readability.

## Structure
- Deeply nested subqueries that would read more clearly as CTEs (`WITH`).
- Repeated expressions that should be a CTE or computed once.
- Magic numbers/strings without comment (`status = 3`) — a brief comment or a
  named reference aids the next reader.

## Portability (relevant since the default target is ANSI SQL)
- Dialect-specific syntax when portability matters: backtick quoting (MySQL),
  `LIMIT`/`OFFSET` vs `FETCH FIRST`, `ISNULL`/`IFNULL`/`NVL` vs `COALESCE`,
  `TOP` (SQL Server) vs `LIMIT`. Suggest the ANSI form (`COALESCE`, `FETCH
  FIRST ... ROWS ONLY`) when the user cares about portability, but don't force
  it if they've told you the dialect.

## Formatting
- One major clause per line, consistent indentation for joins/conditions —
  helps review but isn't worth a finding on its own unless the query is a
  genuine wall of text. If you rewrite, format it cleanly as a free upgrade.
