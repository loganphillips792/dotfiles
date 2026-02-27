---
name: documenting-flow
description: Traces a feature's execution flow across the codebase and produces structured documentation. Use when the user wants to document, trace, or understand how a feature works end-to-end.
---

# Document Feature Flow

1. Search the codebase for all files involved in the feature
2. Read relevant sections of each file
3. Trace the execution flow in order
4. Write documentation covering: overview, step-by-step flow with real file paths and line numbers, error/failure paths, data flow (types and shapes between steps), and a mermaid sequence diagram if 3+ components are involved

## Rules
- Use REAL file paths and line numbers — never fabricate
- If uncertain about a connection in the flow, say so
- Output as a single markdown code block so the user can copy it

## Feature to document
$ARGUMENTS
