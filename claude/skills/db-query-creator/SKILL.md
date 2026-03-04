---
name: db-query
description: Generate SQL queries from natural language descriptions for any project. Use this skill whenever the user asks to write, build, create, or generate a SQL query, wants to fetch or filter data from the database, asks "how do I get X from the database", mentions any model or table name, or asks for reports, aggregations, joins, or data lookups. Trigger even if the user is vague — e.g. "give me all users from last month" or "how many events happened today". Also use when the user wants to understand table structure or relationships between models.
---

# SQL Query Generator (Universal)

Generate accurate, schema-aware SQL queries by first detecting the project's stack and database, then using its schema definitions as the source of truth.

## Step 1 — Detect the Stack and Database

Before anything else, identify:

**Database engine** — determines SQL dialect:
- Look for config files: `database.yml`, `config/database.go`, `.env`, `docker-compose.yml`, `config.py`, `appsettings.json`, `knexfile.js`, `prisma/schema.prisma`, `ormconfig.*`, etc.
- Common indicators: `postgres://`, `mysql://`, `sqlite:`, `sqlserver://`, `mongodb://`
- If ambiguous, check the project's dependency files (see below) for database driver packages.

**Language/framework** — determines where schema and model definitions live:

| Stack | Dependency file | Schema/model locations |
|---|---|---|
| Ruby on Rails | `Gemfile` | `db/schema.rb`, `app/models/` |
| Go (GORM, sqlc, etc.) | `go.mod` | `*.go` structs with `gorm:` or `db:` tags, `sqlc.yaml` + `*.sql` files, migration files |
| Python (Django) | `requirements.txt` / `pyproject.toml` | `models.py` files, migration files |
| Python (SQLAlchemy) | `requirements.txt` / `pyproject.toml` | `models.py`, `Base` subclasses |
| Node.js (Prisma) | `package.json` | `prisma/schema.prisma` |
| Node.js (Sequelize) | `package.json` | `models/` directory |
| Node.js (TypeORM) | `package.json` | `entities/` or `*.entity.ts` files |
| Java/Kotlin (JPA/Hibernate) | `pom.xml` / `build.gradle` | `@Entity` annotated classes |
| PHP (Laravel) | `composer.json` | `database/migrations/`, `app/Models/` |
| .NET (EF Core) | `*.csproj` | `DbContext` subclasses, `[Table]` annotated classes |

If the stack is unclear, search for migration files in common locations (`migrations/`, `db/migrate/`, `database/migrations/`) — these are the most universal source of truth.

## Step 2 — Find the Schema Source of Truth

Use the detected stack to locate schema definitions. Priority order:

1. **Compiled/generated schema file** (most reliable) — `db/schema.rb`, `prisma/schema.prisma`, `*.dbml`, generated `schema.sql`
2. **ORM model/entity files** — read struct tags, annotations, or class definitions to infer table names, column names, and types
3. **Migration files** — read in order to reconstruct the current schema; look for the latest migrations if the set is large
4. **Database introspection** — if a live connection is available (`db`, `psql`, `sqlite3` CLI), running `\d tablename` or `PRAGMA table_info` is a valid fallback

For large schemas, search or grep for specific table/model names rather than reading everything.

## Step 3 — Infer Relationships

Relationships define join paths. Find them in:
- Rails: `belongs_to`, `has_many`, `has_many :through` in model files
- GORM: struct fields with foreign key tags or `gorm:"foreignKey:..."` 
- Prisma: `@relation` fields in `schema.prisma`
- Django: `ForeignKey`, `ManyToManyField`, `OneToOneField`
- TypeORM/JPA: `@ManyToOne`, `@OneToMany`, `@JoinColumn` annotations
- Laravel: `belongsTo()`, `hasMany()`, `belongsToMany()` in Model classes
- Sequelize: `belongsTo`, `hasMany`, `belongsToMany` in model association files
- Migrations: explicit `FOREIGN KEY` constraints are the fallback for any stack

## Step 4 — Clarify if Ambiguous

Before writing the query, clarify anything that would meaningfully change the output:
- Date/time range and timezone expectations
- Whether to include soft-deleted records (check for `deleted_at`, `discarded_at`, `is_deleted`, `archived_at` columns)
- Pagination expectations (`LIMIT` / `OFFSET` needed?)
- Aggregation level (per user? per day? total?)

Skip clarification for straightforward requests.

## Step 5 — Write the Query

### Adapt SQL dialect to the detected engine:

| Feature | PostgreSQL | MySQL | SQLite | SQL Server |
|---|---|---|---|---|
| Quoting identifiers | `"table"."col"` | `` `table`.`col` `` | `"table"."col"` | `[table].[col]` |
| String concat | `\|\|` | `CONCAT()` | `\|\|` | `+` |
| Current timestamp | `NOW()` | `NOW()` | `datetime('now')` | `GETDATE()` |
| Limit/offset | `LIMIT n OFFSET m` | `LIMIT n OFFSET m` | `LIMIT n OFFSET m` | `OFFSET m ROWS FETCH NEXT n ROWS ONLY` |
| Regex match | `~ 'pattern'` | `REGEXP 'pattern'` | (not supported natively) | `LIKE` only |
| JSON access | `col->>'key'` | `JSON_EXTRACT(col, '$.key')` | `json_extract(col, '$.key')` | `JSON_VALUE(col, '$.key')` |

### Universal conventions:
- Use explicit `INNER JOIN` / `LEFT JOIN` — never implicit comma joins
- Use CTEs (`WITH`) for multi-step logic rather than deeply nested subqueries
- Always alias tables with short meaningful names
- Add `LIMIT 100` by default unless the user specifies or it's a pure aggregation
- Use `IS NULL` / `IS NOT NULL`, never `= NULL`
- Format with one clause per line

### Common ORM/framework patterns to account for:

| Concept | What to look for | SQL implication |
|---|---|---|
| Soft deletes | `deleted_at`, `discarded_at`, `is_deleted` column | Add `AND deleted_at IS NULL` unless user wants deleted rows |
| Timestamps | `created_at` / `updated_at` auto-managed by ORM | Always present; stored in UTC |
| Enums | Stored as integers (Rails, GORM) or strings (Prisma, Django) | Check model definition for mapping |
| Polymorphic associations | `*_type` + `*_id` column pair | Filter on both columns |
| STI / single-table inheritance | `type` or `kind` discriminator column | Filter by subclass name |
| UUID primary keys | `id` is `uuid` / `char(36)` not integer | Adjust any hardcoded ID examples |
| Join tables (M2M) | Intermediate table, often with no model file | Join through it explicitly |
| Composite primary keys | Multiple PK columns | Match all PK columns in joins |

### Timestamps and timezones:
- ORMs typically store timestamps in UTC — advise the user if timezone conversion is needed
- PostgreSQL: use `AT TIME ZONE`; MySQL: use `CONVERT_TZ()`; SQLite: use `datetime(col, 'localtime')`

## Step 6 — Output Format

Return:
1. The detected **database engine** and **framework** (one line, e.g. "PostgreSQL · Django")
2. The SQL query in a ` ```sql ` code block using the correct dialect
3. A 2–3 sentence plain-English explanation of what the query does
4. Any caveats: missing indexes, soft-delete assumptions, timezone considerations, enum mappings, performance risks
