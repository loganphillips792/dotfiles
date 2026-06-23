# Performance checklist

Static analysis can't see the real query plan or data distribution, so frame
performance findings in terms of *patterns that scale badly*, and be honest
about what depends on cardinality you can't observe.

## Index-defeating predicates
A predicate that wraps an indexed column in a function or expression usually
can't use the index — the engine must compute the expression per row.
- `WHERE YEAR(created_at) = 2024` → can't use an index on `created_at`. Rewrite
  as a range: `created_at >= '2024-01-01' AND created_at < '2025-01-01'`.
- `WHERE UPPER(email) = 'X'` → defeats the index on `email` unless a functional
  index exists. Prefer storing/normalizing case, or a case-insensitive collation.
- Leading wildcard `LIKE '%foo'` → can't use a B-tree index; only a trailing
  wildcard `'foo%'` is sargable.
- Implicit type coercion: comparing an indexed `VARCHAR` column to a number, or
  vice versa, can force a full scan.

## Joins
- **Full scans from missing join indexes** — every join column should be
  indexed on at least one side. Flag join keys that look unindexed (provisional
  without a schema).
- **Join order / explosion** — joining before filtering can blow up
  intermediate row counts; pushing selective `WHERE`s earlier (or into
  subqueries/CTEs) shrinks the working set.
- **Wrong join type for intent** — a `LEFT JOIN` whose `WHERE` clause filters on
  the right table's columns silently behaves like an `INNER JOIN` (and is slower
  + misleading). See correctness.md.

## Subqueries & correlated subqueries
- **Correlated subquery in SELECT/WHERE** runs once per outer row — O(n·m).
  Usually rewritable as a join or a window function. Flag and rewrite.
- `IN (SELECT ...)` vs `EXISTS` vs `JOIN` — for existence checks, `EXISTS` or a
  semi-join often optimizes better than `IN` on large subqueries; `IN` with a
  huge list materializes it.
- **Repeated subquery** — the same subquery computed multiple times should be a
  CTE (or derived table) computed once.

## Reading more than needed
- `SELECT *` pulls every column including large TEXT/BLOB fields, inflates row
  width, defeats covering indexes, and breaks if columns change. Select only
  what's used.
- Missing `LIMIT` on queries that feed a UI / only need a sample.
- `ORDER BY` on an unindexed column forces a sort of the full result; `ORDER BY`
  + `LIMIT` (top-N) is much cheaper with a matching index.
- `DISTINCT` used to paper over a join that produces duplicates — fix the join
  instead; `DISTINCT` forces a sort/hash over the whole result.

## Aggregation
- `GROUP BY` on unindexed/high-cardinality columns is expensive; note it.
- `HAVING` filtering rows that could be filtered in `WHERE` before aggregation
  wastes work — only post-aggregate conditions belong in `HAVING`.
- `COUNT(DISTINCT ...)` is far costlier than `COUNT(*)`; flag if distinctness
  isn't actually required.

## Pagination
- `OFFSET 100000 LIMIT 20` still scans and discards 100k rows. For deep
  pagination, suggest keyset/seek pagination (`WHERE id > :last_id`).
