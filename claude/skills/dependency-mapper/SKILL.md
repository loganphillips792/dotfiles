---
name: dependency-mapper
description: Generate an interactive force-directed graph showing how files and components import and depend on each other. Use when exploring a codebase's architecture, understanding component relationships, debugging circular dependencies, or planning refactors.
allowed-tools: Bash(python *)
---

# Dependency Mapper

Generates an interactive force-directed graph that visualizes how your project's files import and depend on one another — so you can see the full architecture at a glance.

## Usage

Run from your project root (or point at any directory):

```bash
python ~/.claude/skills/dependency-mapper/scripts/map_dependencies.py .
```

Or target a specific subfolder:

```bash
python ~/.claude/skills/dependency-mapper/scripts/map_dependencies.py ./src
```

This creates `dependency-map.html` and opens it in your browser.

## What it shows

- **Force-directed graph**: Files are nodes, imports are directed edges (arrows)
- **Node size**: Bigger = imported by more files (high-value shared modules)
- **Node color**: Color-coded by file type (.py, .ts, .go, etc.)
- **Sidebar file list**: Browse and search all files, grouped by extension
- **External packages**: See which third-party packages are used most
- **Click a node**: Highlights all direct connections and shows import/used-by details

## Supported languages

Python, JavaScript, TypeScript, JSX, TSX, Vue, Svelte, Go, Rust, Ruby, PHP, Java, Kotlin, C, C++, CSS, SCSS

## Tips

- **Large codebases**: The graph may be dense — use the search box to filter files and click nodes to isolate connections
- **Fit view**: Click "⊡ Fit" if the graph is off-screen after load
- **Labels**: Toggle file name labels on/off with "🏷 Labels"
- Ignored automatically: `node_modules`, `.git`, `__pycache__`, `venv`, `dist`, `build`, `.next`
