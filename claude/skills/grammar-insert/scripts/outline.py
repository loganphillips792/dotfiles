#!/usr/bin/env python3
"""Print the heading tree of a markdown file with line ranges.

Usage: outline.py <file.md> [filter-substring]

Each line: <start>-<end>  <#'s> <heading>  (<n> top-level bullets)
`end` is the last line before the next heading of any level, so the range is
exactly the body that belongs to that heading. Headings inside fenced code
blocks are ignored.
"""
import re
import sys

path = sys.argv[1]
flt = sys.argv[2].lower() if len(sys.argv) > 2 else None

with open(path, encoding="utf-8") as f:
    lines = f.read().split("\n")

heads = []
in_fence = False
for i, line in enumerate(lines, 1):
    if line.lstrip().startswith("```"):
        in_fence = not in_fence
        continue
    if in_fence:
        continue
    m = re.match(r"^(#{1,6})\s+(.*)$", line)
    if m:
        heads.append([i, len(m.group(1)), m.group(2).strip()])

for idx, (start, level, text) in enumerate(heads):
    end = heads[idx + 1][0] - 1 if idx + 1 < len(heads) else len(lines)
    bullets = sum(1 for l in lines[start:end] if re.match(r"^[-*] ", l))
    if flt and flt not in text.lower():
        continue
    clean = text.replace("**", "")
    print(f"{start}-{end}\t{'#' * level} {clean}\t({bullets} top-level bullets)")
