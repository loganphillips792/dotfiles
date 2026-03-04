#!/usr/bin/env python3
"""
Dependency Mapper: Analyzes how files and components interact with each other.
Supports: Python, JavaScript, TypeScript, Go, Rust, Ruby, PHP, Java, C/C++
"""

import json
import re
import sys
import webbrowser
from pathlib import Path
from collections import defaultdict

IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv',
               'dist', 'build', '.next', 'coverage', '.cache', 'vendor'}

PARSERS = {
    # Python
    '.py': [
        r'^\s*import\s+([\w.]+)',
        r'^\s*from\s+([\w.]+)\s+import',
    ],
    # JavaScript / TypeScript / JSX / TSX
    '.js':   [r"""(?:import|require)\s*(?:[\w*{},\s]+\s+from\s+)?['"]([^'"]+)['"]"""],
    '.ts':   [r"""(?:import|require)\s*(?:[\w*{},\s]+\s+from\s+)?['"]([^'"]+)['"]"""],
    '.jsx':  [r"""(?:import|require)\s*(?:[\w*{},\s]+\s+from\s+)?['"]([^'"]+)['"]"""],
    '.tsx':  [r"""(?:import|require)\s*(?:[\w*{},\s]+\s+from\s+)?['"]([^'"]+)['"]"""],
    '.mjs':  [r"""(?:import|require)\s*(?:[\w*{},\s]+\s+from\s+)?['"]([^'"]+)['"]"""],
    # Go
    '.go': [r'"([^"]+)"'],
    # Rust
    '.rs': [
        r'use\s+([\w:]+)',
        r'extern\s+crate\s+(\w+)',
    ],
    # Ruby
    '.rb': [
        r"require(?:_relative)?\s+['\"]([^'\"]+)['\"]",
    ],
    # PHP
    '.php': [
        r"(?:require|include)(?:_once)?\s+['\"]([^'\"]+)['\"]",
        r'use\s+([\w\\]+)',
    ],
    # Java / Kotlin
    '.java': [r'import\s+([\w.]+)'],
    '.kt':   [r'import\s+([\w.]+)'],
    # C / C++
    '.c':    [r'#include\s+[<"]([^>"]+)[>"]'],
    '.cpp':  [r'#include\s+[<"]([^>"]+)[>"]'],
    '.h':    [r'#include\s+[<"]([^>"]+)[>"]'],
    '.hpp':  [r'#include\s+[<"]([^>"]+)[>"]'],
    # CSS / SCSS
    '.css':  [r"""@import\s+['"]([^'"]+)['"]"""],
    '.scss': [r"""@(?:import|use|forward)\s+['"]([^'"]+)['"]"""],
    # Vue
    '.vue':  [r"""(?:import|require)\s*(?:[\w*{},\s]+\s+from\s+)?['"]([^'"]+)['"]"""],
    # Svelte
    '.svelte': [r"""(?:import|require)\s*(?:[\w*{},\s]+\s+from\s+)?['"]([^'"]+)['"]"""],
}

COLORS = {
    '.py': '#3776ab', '.js': '#f7df1e', '.ts': '#3178c6',
    '.jsx': '#61dafb', '.tsx': '#3178c6', '.vue': '#42b883',
    '.svelte': '#ff3e00', '.go': '#00add8', '.rs': '#dea584',
    '.rb': '#cc342d', '.php': '#777bb4', '.java': '#007396',
    '.kt': '#7f52ff', '.c': '#a8b9cc', '.cpp': '#00599c',
    '.h': '#a8b9cc', '.hpp': '#00599c', '.css': '#264de4',
    '.scss': '#c6538c', '.html': '#e34c26', '.md': '#083fa1',
    '.json': '#6b7280', '.yaml': '#cb171e', '.yml': '#cb171e',
}

def is_local(imp: str) -> bool:
    """Check if an import references a local file (not a package)."""
    return imp.startswith('.') or imp.startswith('/')

def resolve_import(source_file: Path, imp: str, all_files: set) -> str | None:
    """Try to resolve a relative import to an actual file path."""
    if not is_local(imp):
        return None

    base = source_file.parent
    candidates = [
        base / imp,
        base / (imp + '.py'),
        base / (imp + '.js'),
        base / (imp + '.ts'),
        base / (imp + '.jsx'),
        base / (imp + '.tsx'),
        base / (imp + '.vue'),
        base / (imp + '.svelte'),
        base / imp / '__init__.py',
        base / imp / 'index.js',
        base / imp / 'index.ts',
        base / imp / 'index.tsx',
    ]
    for c in candidates:
        resolved = str(c.resolve())
        if resolved in all_files:
            return resolved
    return None

def extract_imports(file_path: Path) -> list[str]:
    """Extract all import strings from a file."""
    ext = file_path.suffix.lower()
    patterns = PARSERS.get(ext, [])
    if not patterns:
        return []
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return []

    imports = []
    for pattern in patterns:
        imports.extend(re.findall(pattern, content, re.MULTILINE))
    return imports

def scan_project(root: Path) -> tuple[dict, dict]:
    """Scan all files and build dependency graph."""
    all_files = set()
    file_imports = defaultdict(list)

    # First pass: collect all files
    for path in root.rglob('*'):
        if path.is_file() and path.suffix.lower() in PARSERS:
            skip = any(part in IGNORE_DIRS or part.startswith('.') for part in path.parts)
            if not skip:
                all_files.add(str(path.resolve()))

    # Second pass: extract imports
    for filepath_str in all_files:
        path = Path(filepath_str)
        imports = extract_imports(path)
        file_imports[filepath_str] = imports

    return file_imports, all_files

def build_graph(root: Path, file_imports: dict, all_files: set) -> dict:
    """Build node/edge graph data."""
    root_str = str(root.resolve())
    nodes = {}
    edges = []
    external_deps = defaultdict(int)

    def rel(p: str) -> str:
        try:
            return str(Path(p).relative_to(root))
        except ValueError:
            return p

    for filepath_str, imports in file_imports.items():
        path = Path(filepath_str)
        ext = path.suffix.lower()
        node_id = rel(filepath_str)

        if node_id not in nodes:
            nodes[node_id] = {
                'id': node_id,
                'label': path.name,
                'ext': ext,
                'color': COLORS.get(ext, '#6b7280'),
                'size': path.stat().st_size,
                'imports': len(imports),
                'imported_by': 0,
            }

        for imp in imports:
            resolved = resolve_import(path, imp, all_files)
            if resolved:
                target_id = rel(resolved)
                if target_id not in nodes:
                    tp = Path(resolved)
                    te = tp.suffix.lower()
                    nodes[target_id] = {
                        'id': target_id,
                        'label': tp.name,
                        'ext': te,
                        'color': COLORS.get(te, '#6b7280'),
                        'size': tp.stat().st_size if tp.exists() else 0,
                        'imports': 0,
                        'imported_by': 0,
                    }
                nodes[target_id]['imported_by'] += 1
                edges.append({'source': node_id, 'target': target_id})
            else:
                # Track external/package deps
                package = imp.split('/')[0].split('.')[0]
                if package and not package.startswith('_'):
                    external_deps[package] += 1

    # Sort external deps
    top_external = sorted(external_deps.items(), key=lambda x: -x[1])[:20]

    return {
        'nodes': list(nodes.values()),
        'edges': edges,
        'external': top_external,
        'root': root.name,
    }

def generate_html(graph: dict, output: Path) -> None:
    graph_json = json.dumps(graph)

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Dependency Map</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font: 13px/1.5 system-ui, sans-serif; background: #0f0f1a; color: #e0e0f0; overflow: hidden; }
  #app { display: flex; height: 100vh; }

  /* Sidebar */
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

  .file-item { display: flex; align-items: center; gap: 8px; padding: 6px 8px; border-radius: 6px;
               cursor: pointer; transition: background 0.15s; }
  .file-item:hover { background: #1e1e38; }
  .file-item.selected { background: #252548; border: 1px solid #a78bfa44; }
  .dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
  .file-name { flex: 1; font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .file-meta { font-size: 11px; color: #555; flex-shrink: 0; }

  .ext-group { margin-bottom: 4px; }
  .ext-label { font-size: 11px; color: #555; padding: 6px 8px 2px; text-transform: uppercase; letter-spacing: 0.05em; }

  .badge { display: inline-block; padding: 1px 6px; border-radius: 10px; font-size: 11px;
           background: #252548; color: #a78bfa; }

  /* Info panel */
  #info-panel { position: absolute; right: 20px; bottom: 20px; width: 280px;
                background: #16162a; border: 1px solid #2a2a44; border-radius: 10px;
                padding: 16px; display: none; z-index: 20; }
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

  /* Canvas */
  #canvas { flex: 1; position: relative; }
  svg { width: 100%; height: 100%; }

  /* Controls */
  #controls { position: absolute; top: 16px; right: 16px; display: flex; flex-direction: column;
              gap: 6px; z-index: 10; }
  .ctrl-btn { background: #16162a; border: 1px solid #2a2a44; color: #aaa; padding: 6px 10px;
              border-radius: 6px; cursor: pointer; font-size: 12px; transition: all 0.2s; }
  .ctrl-btn:hover { background: #1e1e38; color: #fff; border-color: #a78bfa; }

  /* Stats bar */
  #stats { position: absolute; top: 16px; left: 16px; display: flex; gap: 12px; z-index: 10; }
  .stat-pill { background: #16162a; border: 1px solid #2a2a44; border-radius: 20px;
               padding: 4px 12px; font-size: 12px; color: #888; }
  .stat-pill strong { color: #a78bfa; }

  /* Legend */
  #legend { position: absolute; bottom: 16px; left: 16px; background: #16162a;
            border: 1px solid #2a2a44; border-radius: 8px; padding: 10px; z-index: 10; max-width: 200px; }
  #legend h4 { font-size: 11px; color: #555; text-transform: uppercase; margin-bottom: 8px; }
  .legend-item { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; font-size: 12px; color: #888; }

  /* Links */
  .link { stroke: #2a2a55; stroke-opacity: 0.6; fill: none; }
  .link.highlighted { stroke: #a78bfa; stroke-opacity: 0.9; stroke-width: 2px; }
  .link.faded { stroke-opacity: 0.1; }

  /* Nodes */
  .node circle { stroke-width: 2; transition: r 0.2s; cursor: pointer; }
  .node.faded circle { opacity: 0.15; }
  .node.faded text { opacity: 0.1; }
  .node text { font-size: 11px; fill: #ccc; pointer-events: none; }

  /* Tooltip */
  #tooltip { position: absolute; background: #16162a; border: 1px solid #2a2a44; border-radius: 6px;
             padding: 8px 12px; font-size: 12px; pointer-events: none; display: none; z-index: 30;
             white-space: nowrap; }

  /* External panel */
  .ext-dep { display: flex; align-items: center; justify-content: space-between;
             padding: 5px 8px; border-radius: 6px; }
  .ext-dep:hover { background: #1e1e38; }
  .ext-bar { height: 4px; border-radius: 2px; background: #a78bfa; margin-top: 3px; }
</style>
</head>
<body>
<div id="app">
  <div id="sidebar">
    <div id="sidebar-header">
      <h1>🕸️ Dependency Map</h1>
      <p id="root-label"></p>
      <input id="search" type="text" placeholder="Search files…">
    </div>
    <div id="tabs">
      <div class="tab active" data-tab="files">Files</div>
      <div class="tab" data-tab="external">External</div>
    </div>
    <div id="panel"></div>
  </div>

  <div id="canvas">
    <div id="stats">
      <div class="stat-pill"><strong id="s-nodes">0</strong> files</div>
      <div class="stat-pill"><strong id="s-edges">0</strong> links</div>
      <div class="stat-pill"><strong id="s-ext">0</strong> packages</div>
    </div>
    <svg id="svg"></svg>
    <div id="controls">
      <button class="ctrl-btn" id="btn-fit">⊡ Fit</button>
      <button class="ctrl-btn" id="btn-reset">↺ Reset</button>
      <button class="ctrl-btn" id="btn-labels" data-on="true">🏷 Labels</button>
    </div>
    <div id="legend">
      <h4>Node size = imported by</h4>
      <div class="legend-item"><svg width="14" height="14"><circle cx="7" cy="7" r="5" fill="#a78bfa"></circle></svg> Highly used</div>
      <div class="legend-item"><svg width="14" height="14"><circle cx="7" cy="7" r="3" fill="#6b7280"></circle></svg> Rarely used</div>
    </div>
    <div id="tooltip"></div>
    <div id="info-panel">
      <span id="close-info">×</span>
      <h3 id="info-name"></h3>
      <div id="info-rows"></div>
      <div id="info-deps"></div>
    </div>
  </div>
</div>

<script>
const GRAPH = ''' + graph_json + ''';

// ── State ───────────────────────────────────────────────────────
let selectedNode = null;
let showLabels = true;
let currentTab = 'files';
let searchQuery = '';

// ── Stats ───────────────────────────────────────────────────────
document.getElementById('root-label').textContent = GRAPH.root;
document.getElementById('s-nodes').textContent = GRAPH.nodes.length;
document.getElementById('s-edges').textContent = GRAPH.edges.length;
document.getElementById('s-ext').textContent = GRAPH.external.length;

// ── D3 Setup ────────────────────────────────────────────────────
const svg = d3.select('#svg');
const g = svg.append('g');

const zoom = d3.zoom()
  .scaleExtent([0.05, 4])
  .on('zoom', e => g.attr('transform', e.transform));
svg.call(zoom);

const W = () => document.getElementById('canvas').offsetWidth;
const H = () => document.getElementById('canvas').offsetHeight;

// Build node map for edge resolution
const nodeMap = Object.fromEntries(GRAPH.nodes.map(n => [n.id, n]));

// Filter to only edges where both nodes exist
const validEdges = GRAPH.edges.filter(e => nodeMap[e.source] && nodeMap[e.target]);

// ── Force Simulation ─────────────────────────────────────────────
const simulation = d3.forceSimulation(GRAPH.nodes)
  .force('link', d3.forceLink(validEdges).id(d => d.id).distance(80).strength(0.3))
  .force('charge', d3.forceManyBody().strength(-200))
  .force('center', d3.forceCenter(W() / 2, H() / 2))
  .force('collision', d3.forceCollide().radius(d => nodeRadius(d) + 6));

function nodeRadius(d) {
  const base = 6;
  const scale = Math.sqrt(d.imported_by || 0) * 3;
  return Math.min(base + scale, 30);
}

// ── Render links ─────────────────────────────────────────────────
const link = g.append('g')
  .selectAll('line')
  .data(validEdges)
  .join('line')
  .attr('class', 'link')
  .attr('marker-end', 'url(#arrow)');

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

// ── Render nodes ─────────────────────────────────────────────────
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
  .text(d => d.label);

svg.on('click', () => clearSelection());

simulation.on('tick', () => {
  link
    .attr('x1', d => d.source.x)
    .attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x)
    .attr('y2', d => d.target.y);
  node.attr('transform', d => `translate(${d.x},${d.y})`);
});

// ── Selection ─────────────────────────────────────────────────────
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

  showInfoPanel(d, connected, validEdges);
  highlightSidebar(d.id);
}

function clearSelection() {
  selectedNode = null;
  node.classed('faded', false);
  link.classed('highlighted', false).classed('faded', false);
  document.getElementById('info-panel').style.display = 'none';
  document.querySelectorAll('.file-item').forEach(el => el.classList.remove('selected'));
}

// ── Info Panel ─────────────────────────────────────────────────────
function showInfoPanel(d, connected, edges) {
  const panel = document.getElementById('info-panel');
  panel.style.display = 'block';
  document.getElementById('info-name').textContent = d.label;
  document.getElementById('info-name').title = d.id;

  const fmt = b => b < 1024 ? b + ' B' : b < 1048576 ? (b/1024).toFixed(1) + ' KB' : (b/1048576).toFixed(1) + ' MB';

  const rows = [
    ['Path', d.id],
    ['Type', d.ext || 'unknown'],
    ['Size', fmt(d.size)],
    ['Imports', d.imports],
    ['Imported by', d.imported_by],
  ];
  document.getElementById('info-rows').innerHTML = rows.map(([k,v]) =>
    `<div class="info-row"><span class="info-label">${k}</span><span>${v}</span></div>`
  ).join('');

  // Dependencies
  const deps = edges.filter(e => {
    const src = typeof e.source === 'object' ? e.source.id : e.source;
    return src === d.id;
  }).map(e => typeof e.target === 'object' ? e.target.id : e.target);

  const usedBy = edges.filter(e => {
    const tgt = typeof e.target === 'object' ? e.target.id : e.target;
    return tgt === d.id;
  }).map(e => typeof e.source === 'object' ? e.source.id : e.source);

  let depsHtml = '';
  if (deps.length) {
    depsHtml += `<h4>Imports (${deps.length})</h4>` + deps.map(p =>
      `<div class="dep-item" onclick="focusNode('${p}')" title="${p}">${p.split('/').pop()}</div>`
    ).join('');
  }
  if (usedBy.length) {
    depsHtml += `<h4 style="margin-top:8px">Used by (${usedBy.length})</h4>` + usedBy.map(p =>
      `<div class="dep-item" onclick="focusNode('${p}')" title="${p}">${p.split('/').pop()}</div>`
    ).join('');
  }
  document.getElementById('info-deps').innerHTML = depsHtml;
}

function focusNode(id) {
  const d = GRAPH.nodes.find(n => n.id === id);
  if (d) selectNode(d);
}

document.getElementById('close-info').onclick = clearSelection;

// ── Tooltip ────────────────────────────────────────────────────────
const tooltip = document.getElementById('tooltip');
function showTooltip(e, d) {
  tooltip.style.display = 'block';
  tooltip.innerHTML = `<strong>${d.label}</strong> &nbsp;<span style="color:#555">${d.ext}</span><br>
    <span style="color:#888">↑ imports ${d.imports} &nbsp; ↓ imported by ${d.imported_by}</span>`;
  tooltip.style.left = (e.pageX + 12) + 'px';
  tooltip.style.top = (e.pageY - 10) + 'px';
}
function hideTooltip() { tooltip.style.display = 'none'; }

// ── Controls ────────────────────────────────────────────────────────
document.getElementById('btn-fit').onclick = fitView;
document.getElementById('btn-reset').onclick = () => {
  GRAPH.nodes.forEach(d => { d.fx = null; d.fy = null; });
  simulation.alpha(0.5).restart();
  fitView();
};
document.getElementById('btn-labels').onclick = function() {
  showLabels = !showLabels;
  labels.style('display', showLabels ? null : 'none');
  this.textContent = showLabels ? '🏷 Labels' : '🔵 Labels';
};

function fitView() {
  const bounds = g.node().getBBox();
  if (!bounds.width || !bounds.height) return;
  const fullW = W(), fullH = H();
  const scale = Math.min(fullW / bounds.width, fullH / bounds.height) * 0.85;
  const tx = (fullW - bounds.width * scale) / 2 - bounds.x * scale;
  const ty = (fullH - bounds.height * scale) / 2 - bounds.y * scale;
  svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(scale));
}

setTimeout(fitView, 2000);

// ── Sidebar: Files tab ────────────────────────────────────────────
function renderFilesTab() {
  const panel = document.getElementById('panel');
  const q = searchQuery.toLowerCase();
  const filtered = GRAPH.nodes.filter(n => !q || n.id.toLowerCase().includes(q));

  // Group by extension
  const groups = {};
  filtered.forEach(n => {
    const ext = n.ext || 'other';
    if (!groups[ext]) groups[ext] = [];
    groups[ext].push(n);
  });

  const sorted = Object.entries(groups).sort((a, b) => b[1].length - a[1].length);

  panel.innerHTML = sorted.map(([ext, nodes]) => {
    const items = nodes.sort((a, b) => b.imported_by - a.imported_by).map(n =>
      `<div class="file-item${selectedNode?.id === n.id ? ' selected' : ''}"
            data-id="${n.id}" onclick="focusNode('${n.id}')">
        <div class="dot" style="background:${n.color}"></div>
        <span class="file-name" title="${n.id}">${n.label}</span>
        <span class="file-meta">${n.imported_by > 0 ? '↓'+n.imported_by : ''}</span>
      </div>`
    ).join('');
    return `<div class="ext-group">
      <div class="ext-label">${ext} <span class="badge">${nodes.length}</span></div>
      ${items}
    </div>`;
  }).join('');
}

// ── Sidebar: External tab ─────────────────────────────────────────
function renderExternalTab() {
  const panel = document.getElementById('panel');
  const max = GRAPH.external[0]?.[1] || 1;
  panel.innerHTML = '<div style="padding:8px 4px">' + GRAPH.external.map(([pkg, count]) =>
    `<div class="ext-dep">
      <div style="flex:1">
        <div style="font-size:13px;color:#ccc">${pkg}</div>
        <div class="ext-bar" style="width:${(count/max)*100}%"></div>
      </div>
      <span class="file-meta" style="margin-left:12px">${count}</span>
    </div>`
  ).join('') + '</div>';
}

function renderPanel() {
  if (currentTab === 'files') renderFilesTab();
  else renderExternalTab();
}

function highlightSidebar(id) {
  document.querySelectorAll('.file-item').forEach(el => {
    el.classList.toggle('selected', el.dataset.id === id);
  });
}

// ── Tabs ──────────────────────────────────────────────────────────
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

// ── Window resize ─────────────────────────────────────────────────
window.onresize = () => simulation.force('center', d3.forceCenter(W()/2, H()/2)).alpha(0.1).restart();
</script>
</body>
</html>'''

    output.write_text(html, encoding='utf-8')


if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    print(f'Scanning {target}…')

    file_imports, all_files = scan_project(target)
    print(f'Found {len(all_files)} files')

    graph = build_graph(target, file_imports, all_files)
    print(f'Built graph: {len(graph["nodes"])} nodes, {len(graph["edges"])} edges')

    out = Path('dependency-map.html')
    generate_html(graph, out)
    print(f'Generated {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')
