# Document Feature Flow

I want to describe a feature. Produce full documentation of its execution flow.

## Process

1. Search the codebase to find ALL files involved in this feature
2. Read each relevant file completely — do not skim
3. Trace the execution flow in order
4. Write the documentation below

## Output Format

### Overview
2-3 sentences on what the feature does.

### Flow

For each step in execution order:

#### Step N: [What happens]
**File:** `path/to/file.ext` (Lines X–Y)

[1-2 sentence explanation]
```
// Lines X-Y
<actual code from the file>
```

Note error handling, edge cases, or branching logic at each step.

### Error & Failure Paths
Document non-happy-path flows separately.

### Data Flow
Types, schemas, request/response shapes passed between steps.

### Sequence Diagram
Mermaid diagram if 3+ components are involved.

## Rules
- Use REAL file paths and line numbers — never fabricate
- Include every meaningful step
- Keep explanations concise and technically precise
- If you're uncertain about a connection in the flow, say so
- Output the entire document as a single markdown code block (```markdown ... ```) so the user can copy it directly

## Feature to document
$ARGUMENTS
