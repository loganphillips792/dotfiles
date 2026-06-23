# Correctness checklist

These are the bugs that make a query *return the wrong answer while looking
fine*. They are the highest-value findings — a slow query annoys, a wrong query
corrupts decisions. Most warrant CRITICAL or HIGH severity.

## Cartesian products / fan-out
- A `JOIN` with no `ON` (or a `,` join with no join condition in `WHERE`)
  produces every combination — usually a bug. CRITICAL.
- Joining on a non-unique key multiplies rows ("fan-out"). If the query then
  does `SUM`/`COUNT`, the aggregate is inflated. Classic example: joining
  `orders` to `order_items` and summing `orders.total` — the total is counted
  once per item. Flag any aggregate computed after a one-to-many join.

## LEFT JOIN turned into INNER JOIN
A `LEFT JOIN` followed by a `WHERE` condition on the right table's column
(other than `IS NULL`) silently drops the unmatched rows — defeating the point
of the outer join. The condition belongs in the `ON` clause instead.
```sql
-- BUG: rows with no matching payment are dropped
SELECT u.* FROM users u
LEFT JOIN payments p ON p.user_id = u.id
WHERE p.status = 'paid';
-- FIX: move the predicate into ON, or use INNER JOIN if that was the intent
```

## NULL handling
- **`NOT IN` with a nullable subquery/column** — if the subquery returns even
  one NULL, `NOT IN` yields no rows at all (three-valued logic). Use `NOT EXISTS`
  instead. HIGH/CRITICAL.
- `= NULL` / `!= NULL` never match — must use `IS NULL` / `IS NOT NULL`.
- `<>`/`!=`/`>` comparisons exclude NULL rows; if NULLs should be included the
  query needs `OR col IS NULL`.
- Aggregates ignore NULLs: `COUNT(col)` skips NULLs while `COUNT(*)` doesn't;
  `AVG(col)` divides by the non-NULL count. Flag if that's likely unintended.
- `NULL` in arithmetic/concatenation propagates — `col + NULL` is NULL.

## GROUP BY / aggregation grain
- Selecting a non-aggregated column that isn't in `GROUP BY` — ANSI-illegal, and
  in lenient dialects (older MySQL) returns an arbitrary row's value. Flag it.
- Aggregating at the wrong grain (see fan-out above).
- `HAVING` vs `WHERE` confusion changes results when NULLs/filtering interact.

## Set operations
- `UNION` deduplicates (sorts the whole result); `UNION ALL` doesn't. Using
  `UNION` when duplicates are impossible is a perf bug; using `UNION ALL` when
  duplicates should be removed is a correctness bug. Determine intent.

## Logic & precedence
- Mixed `AND`/`OR` without parentheses — `a AND b OR c` parses as
  `(a AND b) OR c`, often not what's meant. Flag missing parens.
- `BETWEEN` is inclusive on both ends — off-by-one risk on date ranges
  (`BETWEEN '2024-01-01' AND '2024-01-31'` misses Jan 31's timestamps).
- Date/timestamp boundary bugs: comparing a `DATE` to a `TIMESTAMP` truncates;
  half-open ranges (`>= start AND < next_day`) are safer than `BETWEEN`.

## Duplicates & DISTINCT misuse
- `DISTINCT` hiding a join fan-out masks the real bug and is slow. Find why the
  duplicates appear.
