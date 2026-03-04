# Function Call Graph Mapper

Generates an interactive D3 force-directed graph showing how **functions** call each other across Go and Python codebases. Goes deeper than file-level dependency mapping by extracting function/method definitions and resolving call sites to known definitions.

## Usage

```bash
python3 ~/.claude/skills/function-call-mapper/scripts/map_call_graph.py <directory>
```

Example:
```bash
python3 ~/.claude/skills/function-call-mapper/scripts/map_call_graph.py /path/to/backend/services/
```

Opens `call-graph.html` in the browser with an interactive visualization.

## What It Does

1. **Discovers** `.go` and `.py` files (skips node_modules, .git, vendor, test files, etc.)
2. **Extracts** function/method definitions with file, line, package/module, and receiver info
3. **Parses** import blocks (Go grouped imports, Python from/import statements)
4. **Extracts** function bodies (brace-counting for Go, indentation for Python)
5. **Resolves** call sites to known definitions using import context and name matching
6. **Generates** an interactive D3 force-directed graph

## Supported Patterns

### Go
- Package-qualified calls: `redispkg.NewProducer()` → resolves via import alias
- Same-package calls: `persistWorkerEvent()` → resolves within current package
- Method calls on fields: `h.service.InitiateScan()` → extracts terminal method name
- Methods with receivers: `func (h *Handler) InitiateScan(...)` → `scan.Handler.InitiateScan`

### Python
- Imported names: `run_scan()` from `from scan_events import run_scan`
- Aliased imports: `sql_injection_scan()` from `import scan as sql_injection_scan`
- Self method calls: `self.helper()` → resolves to same-class method
- Module-level and class methods distinguished by indentation

## Visualization Features

- **Nodes** = functions, colored by package/module, sized by how many callers they have
- **Sidebar** groups functions by package with search
- **Packages tab** shows package overview with function counts
- **Click** a node to see its calls/called-by lists and file:line location
- **Drag** nodes to rearrange, **zoom** with scroll, **Fit/Reset** controls
