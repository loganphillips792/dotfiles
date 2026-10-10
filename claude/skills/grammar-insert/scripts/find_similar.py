#!/usr/bin/env python3
"""Find lines in a notes file that resemble a new sentence.

Usage: find_similar.py <file.md> "<sentence>" [max_results]

Comparison ignores case, accents, punctuation, and the English half of
"Spanish - English" lines. Each content word (3+ letters, not a stopword)
shared with the new sentence scores a point. Prints the best matches as
"<line>: <score>/<words>  <text>". A score close to the word count means a
near-duplicate.
"""
import re, sys, unicodedata

STOP = set("que los las del una uno unos unas por para con sin pero como mas muy the and you are was this that".split())

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-zñ]+", s)

def words(s):
    return {w for w in norm(s) if len(w) >= 3 and w not in STOP}

path, sentence = sys.argv[1], sys.argv[2]
k = int(sys.argv[3]) if len(sys.argv) > 3 else 8
spanish = re.split(r"\s[-–—]\s", sentence)[0]
target = words(spanish)
if not target:
    sys.exit("no content words in sentence")

hits = []
with open(path, encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        es = re.split(r"\s[-–—]\s", line.strip().lstrip("-*\t "), maxsplit=1)[0]
        score = len(target & words(es))
        if score >= max(2, len(target) // 2):
            hits.append((score, i, line.rstrip()))
hits.sort(key=lambda h: (-h[0], h[1]))
for score, i, line in hits[:k]:
    print(f"{i}: {score}/{len(target)}  {line.strip()[:160]}")
