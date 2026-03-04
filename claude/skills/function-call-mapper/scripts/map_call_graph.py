#!/usr/bin/env python3
"""
Function-Level Call Graph Mapper
Analyzes function definitions and call relationships across Go and Python codebases.
Generates an interactive D3 force-directed graph visualization.
"""

import json
import re
import sys
import webbrowser
from pathlib import Path
from collections import defaultdict

IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv',
               'dist', 'build', '.next', 'coverage', '.cache', 'vendor',
               'testdata', '.idea', '.vscode'}

GO_STDLIB = {
    'fmt', 'os', 'io', 'log', 'net', 'time', 'sync', 'math', 'sort',
    'strings', 'strconv', 'bytes', 'bufio', 'errors', 'context', 'reflect',
    'regexp', 'path', 'filepath', 'encoding', 'crypto', 'hash', 'compress',
    'archive', 'database', 'html', 'image', 'index', 'mime', 'plugin',
    'runtime', 'syscall', 'testing', 'text', 'unicode', 'unsafe', 'embed',
    'debug', 'go', 'internal', 'slog',
}

PY_EXTERNAL = {
    'os', 'sys', 'json', 'time', 'logging', 'pathlib', 're', 'typing',
    'collections', 'functools', 'itertools', 'dataclasses', 'abc', 'io',
    'math', 'random', 'datetime', 'copy', 'enum', 'hashlib', 'base64',
    'uuid', 'asyncio', 'threading', 'multiprocessing', 'subprocess',
    'socket', 'http', 'urllib', 'email', 'html', 'xml', 'csv', 'sqlite3',
    'contextlib', 'warnings', 'traceback', 'inspect', 'importlib',
    'redis', 'ujson', 'opentelemetry', 'flask', 'requests', 'pytest',
    'celery', 'pydantic', 'fastapi', 'sqlalchemy',
}

PALETTE = [
    '#a78bfa', '#f472b6', '#34d399', '#fbbf24', '#60a5fa',
    '#f87171', '#2dd4bf', '#fb923c', '#a3e635', '#c084fc',
    '#38bdf8', '#e879f9', '#4ade80', '#facc15', '#818cf8',
]

# ── File Discovery ────────────────────────────────────────────────


def discover_files(root: Path) -> list[Path]:
    """Find all .go and .py files under root, skipping ignored dirs and test files."""
    files = []
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix not in ('.go', '.py'):
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.name.endswith('_test.go'):
            continue
        files.append(path)
    return files


# ── Go Parsing ────────────────────────────────────────────────────


def extract_go_package(content: str) -> str:
    """Extract package name from Go source."""
    m = re.search(r'^package\s+(\w+)', content, re.MULTILINE)
    return m.group(1) if m else 'unknown'


def extract_go_imports(content: str) -> dict[str, str]:
    """Parse Go imports into {alias: import_path} map."""
    imports = {}
    # Single import
    for m in re.finditer(r'^import\s+(?:(\w+)\s+)?"([^"]+)"', content, re.MULTILINE):
        alias, path = m.group(1), m.group(2)
        if not alias:
            alias = _go_pkg_name(path)
        imports[alias] = path
    # Grouped import block
    for block in re.finditer(r'import\s*\((.*?)\)', content, re.DOTALL):
        for line in block.group(1).splitlines():
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            m = re.match(r'(?:(\w+)\s+)?"([^"]+)"', line)
            if m:
                alias, path = m.group(1), m.group(2)
                if not alias:
                    alias = _go_pkg_name(path)
                imports[alias] = path
    return imports


def _go_pkg_name(import_path: str) -> str:
    """Derive Go package name from import path (handles /vN suffixes)."""
    base = import_path.rsplit('/', 1)[-1]
    if re.match(r'^v\d+$', base):
        parts = import_path.rsplit('/', 2)
        return parts[-2] if len(parts) >= 2 else base
    return base


def _is_go_external(import_path: str) -> bool:
    """Check if a Go import is stdlib or third-party (not local project)."""
    top = import_path.split('/')[0]
    if top in GO_STDLIB:
        return True
    if '.' in top:  # domain-based = third-party (github.com, golang.org, etc.)
        return True
    return False


def extract_go_definitions(filepath: Path, content: str, package: str, root: Path) -> list[dict]:
    """Extract Go function and method definitions."""
    defs = []
    lines = content.splitlines()
    for i, line in enumerate(lines):
        # Method: func (r *Type) Name(
        m = re.match(r'^func\s+\(\s*\w+\s+\*?(\w+)\)\s+(\w+)\s*\(', line)
        if m:
            receiver, name = m.group(1), m.group(2)
            defs.append({
                'id': f'{package}.{receiver}.{name}',
                'name': name,
                'package': package,
                'receiver': receiver,
                'file': str(filepath.relative_to(root)),
                'line': i + 1,
                'lang': 'go',
            })
            continue
        # Function: func Name(
        m = re.match(r'^func\s+(\w+)\s*\(', line)
        if m:
            name = m.group(1)
            defs.append({
                'id': f'{package}.{name}',
                'name': name,
                'package': package,
                'receiver': None,
                'file': str(filepath.relative_to(root)),
                'line': i + 1,
                'lang': 'go',
            })
    return defs


def extract_go_body(lines: list[str], start_line: int) -> str:
    """Extract Go function body using brace counting. start_line is 0-indexed."""
    body_lines = []
    brace_count = 0
    started = False
    for i in range(start_line, len(lines)):
        line = lines[i]
        for ch in line:
            if ch == '{':
                brace_count += 1
                started = True
            elif ch == '}':
                brace_count -= 1
        if started:
            body_lines.append(line)
        if started and brace_count <= 0:
            break
    return '\n'.join(body_lines)


# ── Python Parsing ────────────────────────────────────────────────


def extract_py_imports(content: str, local_modules: set) -> dict[str, str]:
    """Parse Python imports into {local_name: module.name} map for local modules only."""
    imports = {}
    for m in re.finditer(
        r'^from\s+([\w.]+)\s+import\s+(.+)$', content, re.MULTILINE
    ):
        module = m.group(1)
        names_str = m.group(2).strip()
        if module.split('.')[0] in PY_EXTERNAL:
            continue
        if module not in local_modules:
            continue
        for part in names_str.split(','):
            part = part.strip()
            if not part or part.startswith('#'):
                break
            as_match = re.match(r'(\w+)\s+as\s+(\w+)', part)
            if as_match:
                name, alias = as_match.group(1), as_match.group(2)
                imports[alias] = f'{module}.{name}'
            else:
                name = part.strip()
                if name.isidentifier():
                    imports[name] = f'{module}.{name}'
    return imports


def extract_py_definitions(filepath: Path, content: str, module: str, root: Path) -> list[dict]:
    """Extract Python function and class method definitions."""
    defs = []
    lines = content.splitlines()
    current_class = None
    class_indent = 0

    for i, line in enumerate(lines):
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        # Track class scope
        cm = re.match(r'^class\s+(\w+)', stripped)
        if cm and indent == 0:
            current_class = cm.group(1)
            class_indent = indent
            continue

        # Reset class scope at module level (non-empty, non-decorator, non-class, non-def)
        if current_class and indent == 0 and stripped and not stripped.startswith(('#', '@', 'class ', 'def ')):
            current_class = None

        # Detect function/method
        dm = re.match(r'^(\s*)def\s+(\w+)\s*\(', line)
        if dm:
            func_indent = len(dm.group(1))
            name = dm.group(2)
            if current_class and func_indent > class_indent:
                defs.append({
                    'id': f'{module}.{current_class}.{name}',
                    'name': name,
                    'package': module,
                    'receiver': current_class,
                    'file': str(filepath.relative_to(root)),
                    'line': i + 1,
                    'lang': 'py',
                })
            else:
                if func_indent == 0:
                    current_class = None
                defs.append({
                    'id': f'{module}.{name}',
                    'name': name,
                    'package': module,
                    'receiver': None,
                    'file': str(filepath.relative_to(root)),
                    'line': i + 1,
                    'lang': 'py',
                })
    return defs


def extract_py_body(lines: list[str], start_line: int) -> str:
    """Extract Python function body using indentation. start_line is 0-indexed."""
    if start_line >= len(lines):
        return ''
    def_line = lines[start_line]
    def_indent = len(def_line) - len(def_line.lstrip())
    body_lines = []
    for i in range(start_line + 1, len(lines)):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            body_lines.append(line)
            continue
        indent = len(line) - len(stripped)
        if indent <= def_indent:
            break
        body_lines.append(line)
    return '\n'.join(body_lines)


# ── Call Extraction & Resolution ──────────────────────────────────

SKIP_NAMES = {
    # Go keywords & builtins
    'if', 'for', 'switch', 'select', 'return', 'range', 'case', 'go', 'defer',
    'make', 'len', 'cap', 'append', 'copy', 'delete', 'close',
    'new', 'panic', 'recover', 'print', 'println',
    'int', 'int32', 'int64', 'uint', 'uint32', 'uint64',
    'float32', 'float64', 'string', 'bool', 'byte', 'rune',
    'error', 'nil', 'true', 'false', 'iota',
    # Python keywords & builtins
    'isinstance', 'type', 'super', 'str', 'dict', 'list',
    'tuple', 'set', 'frozenset', 'enumerate', 'zip', 'map',
    'filter', 'sorted', 'reversed', 'any', 'all', 'min', 'max',
    'sum', 'abs', 'round', 'pow', 'chr', 'ord', 'repr', 'format',
    'getattr', 'setattr', 'hasattr', 'delattr', 'property',
    'staticmethod', 'classmethod', 'vars', 'dir', 'id', 'hash',
    'input', 'open', 'iter', 'next', 'slice', 'range', 'object',
    'while', 'else', 'elif', 'except', 'finally', 'with', 'as',
    'assert', 'raise', 'try', 'yield', 'lambda', 'def', 'class',
    'not', 'and', 'or', 'in', 'is', 'pass', 'break', 'continue',
    'from', 'import', 'global', 'nonlocal', 'del',
}


def extract_calls(body: str) -> list[str]:
    """Extract function/method call patterns from a body of code."""
    calls = []
    for m in re.finditer(r'(?<![.\w])([a-zA-Z_][\w]*(?:\.[a-zA-Z_][\w]*)*)\s*\(', body):
        call = m.group(1)
        head = call.split('.')[0]
        if head in SKIP_NAMES:
            continue
        calls.append(call)
    return calls


def resolve_go_call(call: str, caller_pkg: str, imports: dict,
                    defs_by_name: dict, defs_by_id: dict) -> str | None:
    """Resolve a Go call expression to a definition ID."""
    parts = call.split('.')

    if len(parts) == 1:
        name = parts[0]
        # Same package: try package.Name
        candidate = f'{caller_pkg}.{name}'
        if candidate in defs_by_id:
            return candidate
        # Same package method: try package.*.Name
        if name in defs_by_name:
            for did in defs_by_name[name]:
                if defs_by_id[did]['package'] == caller_pkg:
                    return did
        return None

    if len(parts) == 2:
        alias, name = parts
        if alias in imports:
            import_path = imports[alias]
            if _is_go_external(import_path):
                return None
            real_pkg = _go_pkg_name(import_path)
            # Try package.Name
            candidate = f'{real_pkg}.{name}'
            if candidate in defs_by_id:
                return candidate
            # Try package.*.Name (method on a type in that package)
            if name in defs_by_name:
                for did in defs_by_name[name]:
                    if defs_by_id[did]['package'] == real_pkg:
                        return did
            return None
        else:
            # Field access like s.InitiateScan — resolve by method name
            name = parts[-1]
            if name in defs_by_name:
                candidates = defs_by_name[name]
                if len(candidates) == 1:
                    return candidates[0]
            return None

    if len(parts) >= 3:
        # Chain like h.service.InitiateScan — extract terminal method name
        name = parts[-1]
        if name in defs_by_name:
            candidates = defs_by_name[name]
            if len(candidates) == 1:
                return candidates[0]
            # Narrow by matching intermediate part to receiver type
            for did in candidates:
                d = defs_by_id[did]
                if d.get('receiver'):
                    for p in parts[:-1]:
                        if p.lower() in d['receiver'].lower():
                            return did
        return None

    return None


def resolve_py_call(call: str, caller_module: str, imports: dict,
                    defs_by_name: dict, defs_by_id: dict) -> str | None:
    """Resolve a Python call expression to a definition ID."""
    parts = call.split('.')
    head = parts[0]

    # Check if the call head is an imported name
    if head in imports:
        resolved = imports[head]
        if len(parts) > 1:
            candidate = f'{resolved}.{".".join(parts[1:])}'
            if candidate in defs_by_id:
                return candidate
        if resolved in defs_by_id:
            return resolved
        return None

    if len(parts) == 1:
        name = parts[0]
        # Same module
        candidate = f'{caller_module}.{name}'
        if candidate in defs_by_id:
            return candidate
        # Fallback: unique name match
        if name in defs_by_name and len(defs_by_name[name]) == 1:
            return defs_by_name[name][0]
        return None

    if len(parts) == 2:
        obj, method = parts
        if obj == 'self':
            # Match class method in same module
            if method in defs_by_name:
                for did in defs_by_name[method]:
                    d = defs_by_id[did]
                    if d['package'] == caller_module and d.get('receiver'):
                        return did
            return None
        # ClassName.method in same module
        candidate = f'{caller_module}.{obj}.{method}'
        if candidate in defs_by_id:
            return candidate

    return None


# ── Graph Building ────────────────────────────────────────────────


def build_graph(definitions: list[dict], edges: list[dict]) -> dict:
    """Build graph data structure for D3 visualization."""
    packages = sorted(set(d['package'] for d in definitions))
    pkg_colors = {pkg: PALETTE[i % len(PALETTE)] for i, pkg in enumerate(packages)}

    called_by_count = defaultdict(int)
    calls_count = defaultdict(int)
    for edge in edges:
        called_by_count[edge['target']] += 1
        calls_count[edge['source']] += 1

    nodes = []
    for d in definitions:
        nodes.append({
            'id': d['id'],
            'label': d['name'],
            'package': d['package'],
            'receiver': d.get('receiver'),
            'file': d['file'],
            'line': d['line'],
            'lang': d['lang'],
            'color': pkg_colors[d['package']],
            'called_by': called_by_count.get(d['id'], 0),
            'calls': calls_count.get(d['id'], 0),
        })

    pkg_summary = []
    for pkg in packages:
        count = sum(1 for d in definitions if d['package'] == pkg)
        pkg_summary.append({'name': pkg, 'count': count, 'color': pkg_colors[pkg]})
    pkg_summary.sort(key=lambda x: -x['count'])

    return {
        'nodes': nodes,
        'edges': edges,
        'packages': pkg_summary,
        'root': 'Call Graph',
    }


# ── HTML Generation ──────────────────────────────────────────────


def generate_html(graph: dict, output: Path) -> None:
    """Generate interactive D3 force-directed graph HTML."""
    graph_json = json.dumps(graph)

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Function Call Graph</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font: 13px/1.5 system-ui, sans-serif; background: #0f0f1a; color: #e0e0f0; overflow: hidden; }
  #app { display: flex; height: 100vh; }

  #sidebar { width: 300px; flex-shrink: 0; background: #16162a; border-right: 1px solid #2a2a44;
             display: flex; flex-direction: column; overflow: hidden; z-index: 10; }
  #sidebar-header { padding: 16px; border-bottom: 1px solid #2a2a44; }
  #sidebar-header h1 { font-size: 16px; color: #a78bfa; margin-bottom: 4px; }
  #sidebar-header p { color: #888; font-size: 12px; }
  #search { width: 100%; background: #0f0f1a; border: 1px solid #2a2a44; color: #e0e0f0;
            padding: 8px 10px; border-radius: 6px; margin-top: 10px; font-size: 13px; }
  #search:focus { outline: none; border-color: #a78bfa; }

  #tabs { display: flex; border-bottom: 1px solid #2a2a44; }
  .tab { flex: 1; padding: 8px; text-align: center; cursor: pointer; font-size: 12px;
          color: #666; transition: all 0.2s; }
  .tab.active { color: #a78bfa; border-bottom: 2px solid #a78bfa; }
  .tab:hover:not(.active) { color: #aaa; }

  #panel { flex: 1; overflow-y: auto; padding: 10px; }
  #panel::-webkit-scrollbar { width: 4px; }
  #panel::-webkit-scrollbar-track { background: #0f0f1a; }
  #panel::-webkit-scrollbar-thumb { background: #2a2a44; border-radius: 2px; }

  .fn-item { display: flex; align-items: center; gap: 8px; padding: 6px 8px; border-radius: 6px;
               cursor: pointer; transition: background 0.15s; }
  .fn-item:hover { background: #1e1e38; }
  .fn-item.selected { background: #252548; border: 1px solid #a78bfa44; }
  .dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
  .fn-name { flex: 1; font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .fn-meta { font-size: 11px; color: #555; flex-shrink: 0; }

  .pkg-group { margin-bottom: 4px; }
  .pkg-label { font-size: 11px; color: #555; padding: 6px 8px 2px; text-transform: uppercase; letter-spacing: 0.05em; }
  .badge { display: inline-block; padding: 1px 6px; border-radius: 10px; font-size: 11px;
           background: #252548; color: #a78bfa; }

  #info-panel { position: absolute; right: 20px; bottom: 20px; width: 300px;
                background: #16162a; border: 1px solid #2a2a44; border-radius: 10px;
                padding: 16px; display: none; z-index: 20; max-height: 60vh; overflow-y: auto; }
  #info-panel h3 { color: #a78bfa; margin-bottom: 8px; font-size: 14px;
                   white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .info-row { display: flex; justify-content: space-between; padding: 4px 0;
              border-bottom: 1px solid #1e1e38; font-size: 12px; }
  .info-label { color: #777; }
  #close-info { position: absolute; top: 10px; right: 12px; cursor: pointer; color: #555;
                font-size: 18px; line-height: 1; }
  #close-info:hover { color: #aaa; }
  #info-deps { margin-top: 10px; }
  #info-deps h4 { font-size: 11px; color: #555; text-transform: uppercase; margin-bottom: 6px; }
  .dep-item { font-size: 12px; padding: 2px 0; color: #a0a0c0; white-space: nowrap;
              overflow: hidden; text-overflow: ellipsis; cursor: pointer; }
  .dep-item:hover { color: #a78bfa; }

  #canvas { flex: 1; position: relative; }
  svg { width: 100%; height: 100%; }

  #controls { position: absolute; top: 16px; right: 16px; display: flex; flex-direction: column;
              gap: 6px; z-index: 10; }
  .ctrl-btn { background: #16162a; border: 1px solid #2a2a44; color: #aaa; padding: 6px 10px;
              border-radius: 6px; cursor: pointer; font-size: 12px; transition: all 0.2s; }
  .ctrl-btn:hover { background: #1e1e38; color: #fff; border-color: #a78bfa; }

  #stats { position: absolute; top: 16px; left: 16px; display: flex; gap: 12px; z-index: 10; }
  .stat-pill { background: #16162a; border: 1px solid #2a2a44; border-radius: 20px;
               padding: 4px 12px; font-size: 12px; color: #888; }
  .stat-pill strong { color: #a78bfa; }

  #legend { position: absolute; bottom: 16px; left: 16px; background: #16162a;
            border: 1px solid #2a2a44; border-radius: 8px; padding: 10px; z-index: 10; max-width: 200px; }
  #legend h4 { font-size: 11px; color: #555; text-transform: uppercase; margin-bottom: 8px; }
  .legend-item { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; font-size: 12px; color: #888; }

  .link { stroke: #2a2a55; stroke-opacity: 0.6; fill: none; }
  .link.highlighted { stroke: #a78bfa; stroke-opacity: 0.9; stroke-width: 2px; }
  .link.faded { stroke-opacity: 0.1; }

  .node circle { stroke-width: 2; transition: r 0.2s; cursor: pointer; }
  .node.faded circle { opacity: 0.15; }
  .node.faded text { opacity: 0.1; }
  .node text { font-size: 11px; fill: #ccc; pointer-events: none; }

  #tooltip { position: absolute; background: #16162a; border: 1px solid #2a2a44; border-radius: 6px;
             padding: 8px 12px; font-size: 12px; pointer-events: none; display: none; z-index: 30;
             white-space: nowrap; }

  .pkg-overview { display: flex; align-items: center; justify-content: space-between;
                  padding: 5px 8px; border-radius: 6px; }
  .pkg-overview:hover { background: #1e1e38; }
  .pkg-bar { height: 4px; border-radius: 2px; margin-top: 3px; }
</style>
</head>
<body>
<div id="app">
  <div id="sidebar">
    <div id="sidebar-header">
      <h1>Function Call Graph</h1>
      <p id="root-label"></p>
      <input id="search" type="text" placeholder="Search functions...">
    </div>
    <div id="tabs">
      <div class="tab active" data-tab="functions">Functions</div>
      <div class="tab" data-tab="packages">Packages</div>
    </div>
    <div id="panel"></div>
  </div>

  <div id="canvas">
    <div id="stats">
      <div class="stat-pill"><strong id="s-nodes">0</strong> functions</div>
      <div class="stat-pill"><strong id="s-edges">0</strong> calls</div>
      <div class="stat-pill"><strong id="s-pkg">0</strong> packages</div>
    </div>
    <svg id="svg"></svg>
    <div id="controls">
      <button class="ctrl-btn" id="btn-fit">Fit</button>
      <button class="ctrl-btn" id="btn-reset">Reset</button>
      <button class="ctrl-btn" id="btn-labels" data-on="true">Labels</button>
    </div>
    <div id="legend">
      <h4>Node size = called by</h4>
      <div class="legend-item"><svg width="14" height="14"><circle cx="7" cy="7" r="5" fill="#a78bfa"></circle></svg> Highly called</div>
      <div class="legend-item"><svg width="14" height="14"><circle cx="7" cy="7" r="3" fill="#6b7280"></circle></svg> Rarely called</div>
    </div>
    <div id="tooltip"></div>
    <div id="info-panel">
      <span id="close-info">&times;</span>
      <h3 id="info-name"></h3>
      <div id="info-rows"></div>
      <div id="info-deps"></div>
    </div>
  </div>
</div>

<script>
const GRAPH = ''' + graph_json + ''';

let selectedNode = null;
let showLabels = true;
let currentTab = 'functions';
let searchQuery = '';

document.getElementById('root-label').textContent = GRAPH.root;
document.getElementById('s-nodes').textContent = GRAPH.nodes.length;
document.getElementById('s-edges').textContent = GRAPH.edges.length;
document.getElementById('s-pkg').textContent = GRAPH.packages.length;

const svg = d3.select('#svg');
const g = svg.append('g');

const zoomBehavior = d3.zoom()
  .scaleExtent([0.05, 4])
  .on('zoom', e => g.attr('transform', e.transform));
svg.call(zoomBehavior);

const W = () => document.getElementById('canvas').offsetWidth;
const H = () => document.getElementById('canvas').offsetHeight;

const nodeMap = Object.fromEntries(GRAPH.nodes.map(n => [n.id, n]));
const validEdges = GRAPH.edges.filter(e => nodeMap[e.source] && nodeMap[e.target]);

const simulation = d3.forceSimulation(GRAPH.nodes)
  .force('link', d3.forceLink(validEdges).id(d => d.id).distance(100).strength(0.3))
  .force('charge', d3.forceManyBody().strength(-300))
  .force('center', d3.forceCenter(W() / 2, H() / 2))
  .force('collision', d3.forceCollide().radius(d => nodeRadius(d) + 8));

function nodeRadius(d) {
  const base = 5;
  const scale = Math.sqrt(d.called_by || 0) * 3;
  return Math.min(base + scale, 28);
}

// Arrow marker
svg.append('defs').append('marker')
  .attr('id', 'arrow')
  .attr('viewBox', '0 -4 8 8')
  .attr('refX', 14)
  .attr('refY', 0)
  .attr('markerWidth', 6)
  .attr('markerHeight', 6)
  .attr('orient', 'auto')
  .append('path')
  .attr('d', 'M0,-4L8,0L0,4')
  .attr('fill', '#2a2a55');

const link = g.append('g')
  .selectAll('line')
  .data(validEdges)
  .join('line')
  .attr('class', 'link')
  .attr('marker-end', 'url(#arrow)');

const node = g.append('g')
  .selectAll('g')
  .data(GRAPH.nodes)
  .join('g')
  .attr('class', 'node')
  .call(d3.drag()
    .on('start', (e, d) => { if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
    .on('drag', (e, d) => { d.fx = e.x; d.fy = e.y; })
    .on('end', (e, d) => { if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }))
  .on('click', (e, d) => { e.stopPropagation(); selectNode(d); })
  .on('mouseover', showTooltip)
  .on('mouseout', hideTooltip);

node.append('circle')
  .attr('r', nodeRadius)
  .attr('fill', d => d.color)
  .attr('stroke', d => d3.color(d.color)?.brighter(1) || '#fff')
  .attr('fill-opacity', 0.85);

const labels = node.append('text')
  .attr('dx', d => nodeRadius(d) + 4)
  .attr('dy', '0.35em')
  .text(d => d.receiver ? d.receiver + '.' + d.label : d.label);

svg.on('click', () => clearSelection());

simulation.on('tick', () => {
  link
    .attr('x1', d => d.source.x)
    .attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x)
    .attr('y2', d => d.target.y);
  node.attr('transform', d => `translate(${d.x},${d.y})`);
});

// ── Selection ───────────────────────────────────────────────────
function selectNode(d) {
  selectedNode = d;
  const connected = new Set();
  const connectedEdges = new Set();
  validEdges.forEach((e, i) => {
    const src = typeof e.source === 'object' ? e.source.id : e.source;
    const tgt = typeof e.target === 'object' ? e.target.id : e.target;
    if (src === d.id || tgt === d.id) {
      connected.add(src);
      connected.add(tgt);
      connectedEdges.add(i);
    }
  });
  node.classed('faded', n => !connected.has(n.id) && n.id !== d.id);
  link.classed('highlighted', (_, i) => connectedEdges.has(i));
  link.classed('faded', (_, i) => !connectedEdges.has(i));
  showInfoPanel(d);
  highlightSidebar(d.id);
}

function clearSelection() {
  selectedNode = null;
  node.classed('faded', false);
  link.classed('highlighted', false).classed('faded', false);
  document.getElementById('info-panel').style.display = 'none';
  document.querySelectorAll('.fn-item').forEach(el => el.classList.remove('selected'));
}

// ── Info Panel ──────────────────────────────────────────────────
function showInfoPanel(d) {
  const panel = document.getElementById('info-panel');
  panel.style.display = 'block';
  document.getElementById('info-name').textContent = d.id;
  document.getElementById('info-name').title = d.id;

  const rows = [
    ['File', d.file + ':' + d.line],
    ['Package', d.package],
    ['Language', d.lang === 'go' ? 'Go' : 'Python'],
  ];
  if (d.receiver) rows.push(['Receiver', d.receiver]);
  rows.push(['Calls', d.calls]);
  rows.push(['Called by', d.called_by]);

  document.getElementById('info-rows').innerHTML = rows.map(([k,v]) =>
    `<div class="info-row"><span class="info-label">${k}</span><span>${v}</span></div>`
  ).join('');

  const callsOut = validEdges.filter(e => {
    const src = typeof e.source === 'object' ? e.source.id : e.source;
    return src === d.id;
  }).map(e => typeof e.target === 'object' ? e.target.id : e.target);

  const calledBy = validEdges.filter(e => {
    const tgt = typeof e.target === 'object' ? e.target.id : e.target;
    return tgt === d.id;
  }).map(e => typeof e.source === 'object' ? e.source.id : e.source);

  let depsHtml = '';
  if (callsOut.length) {
    depsHtml += '<h4>Calls (' + callsOut.length + ')</h4>' + callsOut.map(p =>
      '<div class="dep-item" onclick="focusNode(\\''+p+'\\')" title="'+p+'">'+p+'</div>'
    ).join('');
  }
  if (calledBy.length) {
    depsHtml += '<h4 style="margin-top:8px">Called by (' + calledBy.length + ')</h4>' + calledBy.map(p =>
      '<div class="dep-item" onclick="focusNode(\\''+p+'\\')" title="'+p+'">'+p+'</div>'
    ).join('');
  }
  document.getElementById('info-deps').innerHTML = depsHtml;
}

function focusNode(id) {
  const d = GRAPH.nodes.find(n => n.id === id);
  if (d) selectNode(d);
}

document.getElementById('close-info').onclick = clearSelection;

// ── Tooltip ─────────────────────────────────────────────────────
const tooltip = document.getElementById('tooltip');
function showTooltip(e, d) {
  tooltip.style.display = 'block';
  tooltip.innerHTML = '<strong>' + d.id + '</strong><br>' +
    '<span style="color:#888">' + d.file + ':' + d.line + '</span><br>' +
    '<span style="color:#888">calls ' + d.calls + ' | called by ' + d.called_by + '</span>';
  tooltip.style.left = (e.pageX + 12) + 'px';
  tooltip.style.top = (e.pageY - 10) + 'px';
}
function hideTooltip() { tooltip.style.display = 'none'; }

// ── Controls ────────────────────────────────────────────────────
document.getElementById('btn-fit').onclick = fitView;
document.getElementById('btn-reset').onclick = () => {
  GRAPH.nodes.forEach(d => { d.fx = null; d.fy = null; });
  simulation.alpha(0.5).restart();
  fitView();
};
document.getElementById('btn-labels').onclick = function() {
  showLabels = !showLabels;
  labels.style('display', showLabels ? null : 'none');
  this.textContent = showLabels ? 'Labels' : 'Labels (off)';
};

function fitView() {
  const bounds = g.node().getBBox();
  if (!bounds.width || !bounds.height) return;
  const fullW = W(), fullH = H();
  const scale = Math.min(fullW / bounds.width, fullH / bounds.height) * 0.85;
  const tx = (fullW - bounds.width * scale) / 2 - bounds.x * scale;
  const ty = (fullH - bounds.height * scale) / 2 - bounds.y * scale;
  svg.transition().duration(500).call(zoomBehavior.transform, d3.zoomIdentity.translate(tx, ty).scale(scale));
}
setTimeout(fitView, 2000);

// ── Sidebar: Functions tab ──────────────────────────────────────
function renderFunctionsTab() {
  const panel = document.getElementById('panel');
  const q = searchQuery.toLowerCase();
  const filtered = GRAPH.nodes.filter(n => !q || n.id.toLowerCase().includes(q) || n.label.toLowerCase().includes(q));

  const groups = {};
  filtered.forEach(n => {
    const pkg = n.package || 'unknown';
    if (!groups[pkg]) groups[pkg] = [];
    groups[pkg].push(n);
  });

  const sorted = Object.entries(groups).sort((a, b) => b[1].length - a[1].length);

  panel.innerHTML = sorted.map(([pkg, nodes]) => {
    const items = nodes.sort((a, b) => b.called_by - a.called_by).map(n => {
      const display = n.receiver ? n.receiver + '.' + n.label : n.label;
      return '<div class="fn-item' + (selectedNode?.id === n.id ? ' selected' : '') + '"' +
        ' data-id="' + n.id + '" onclick="focusNode(\\'' + n.id + '\\')">' +
        '<div class="dot" style="background:' + n.color + '"></div>' +
        '<span class="fn-name" title="' + n.id + '">' + display + '</span>' +
        '<span class="fn-meta">' + (n.called_by > 0 ? '\\u2190' + n.called_by : '') + '</span>' +
        '</div>';
    }).join('');
    return '<div class="pkg-group">' +
      '<div class="pkg-label">' + pkg + ' <span class="badge">' + nodes.length + '</span></div>' +
      items + '</div>';
  }).join('');
}

// ── Sidebar: Packages tab ───────────────────────────────────────
function renderPackagesTab() {
  const panel = document.getElementById('panel');
  const max = GRAPH.packages[0]?.count || 1;
  panel.innerHTML = '<div style="padding:8px 4px">' + GRAPH.packages.map(pkg =>
    '<div class="pkg-overview">' +
      '<div style="flex:1">' +
        '<div style="font-size:13px;color:#ccc">' +
          '<span class="dot" style="display:inline-block;background:' + pkg.color + ';width:8px;height:8px;vertical-align:middle;margin-right:6px"></span>' +
          pkg.name +
        '</div>' +
        '<div class="pkg-bar" style="width:' + (pkg.count/max)*100 + '%;background:' + pkg.color + '"></div>' +
      '</div>' +
      '<span class="fn-meta" style="margin-left:12px">' + pkg.count + '</span>' +
    '</div>'
  ).join('') + '</div>';
}

function renderPanel() {
  if (currentTab === 'functions') renderFunctionsTab();
  else renderPackagesTab();
}

function highlightSidebar(id) {
  document.querySelectorAll('.fn-item').forEach(el => {
    el.classList.toggle('selected', el.dataset.id === id);
  });
}

// ── Tabs ────────────────────────────────────────────────────────
document.querySelectorAll('.tab').forEach(tab => {
  tab.onclick = () => {
    currentTab = tab.dataset.tab;
    document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t === tab));
    renderPanel();
  };
});

document.getElementById('search').oninput = e => {
  searchQuery = e.target.value;
  renderPanel();
};

renderPanel();

window.onresize = () => simulation.force('center', d3.forceCenter(W()/2, H()/2)).alpha(0.1).restart();
</script>
</body>
</html>'''

    output.write_text(html, encoding='utf-8')


# ── Main ─────────────────────────────────────────────────────────


def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    print(f'Scanning {target}...')

    # 1. Discover files
    files = discover_files(target)
    print(f'Found {len(files)} files (.go + .py)')

    # 2. Extract definitions and imports per file
    all_definitions = []
    file_data = {}

    # Build set of local Python module names for import resolution
    py_modules = set()
    for f in files:
        if f.suffix == '.py':
            py_modules.add(f.stem)

    for filepath in files:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        lines = content.splitlines()

        if filepath.suffix == '.go':
            package = extract_go_package(content)
            imports = extract_go_imports(content)
            defs = extract_go_definitions(filepath, content, package, target)
        else:
            module = filepath.stem
            imports = extract_py_imports(content, py_modules)
            defs = extract_py_definitions(filepath, content, module, target)
            package = module

        file_data[filepath] = {
            'content': content,
            'lines': lines,
            'package': package,
            'imports': imports,
            'defs': defs,
            'lang': 'go' if filepath.suffix == '.go' else 'py',
        }
        all_definitions.extend(defs)

    print(f'Extracted {len(all_definitions)} function definitions')

    # 3. Build lookup indices
    defs_by_id = {d['id']: d for d in all_definitions}
    defs_by_name = defaultdict(list)
    for d in all_definitions:
        defs_by_name[d['name']].append(d['id'])

    # 4. Extract calls and resolve edges
    edges = []
    seen_edges = set()

    for filepath, data in file_data.items():
        for defn in data['defs']:
            start = defn['line'] - 1  # 0-indexed
            if data['lang'] == 'go':
                body = extract_go_body(data['lines'], start)
            else:
                body = extract_py_body(data['lines'], start)

            calls = extract_calls(body)

            for call in calls:
                if data['lang'] == 'go':
                    resolved = resolve_go_call(
                        call, data['package'], data['imports'],
                        defs_by_name, defs_by_id
                    )
                else:
                    resolved = resolve_py_call(
                        call, data['package'], data['imports'],
                        defs_by_name, defs_by_id
                    )

                if resolved and resolved != defn['id']:
                    edge_key = (defn['id'], resolved)
                    if edge_key not in seen_edges:
                        seen_edges.add(edge_key)
                        edges.append({'source': defn['id'], 'target': resolved})

    print(f'Resolved {len(edges)} call edges')

    # 5. Build graph and generate HTML
    graph = build_graph(all_definitions, edges)
    out = Path('call-graph.html')
    generate_html(graph, out)
    print(f'Generated {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')


if __name__ == '__main__':
    main()
