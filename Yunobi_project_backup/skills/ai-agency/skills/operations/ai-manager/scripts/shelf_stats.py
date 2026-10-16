#!/usr/bin/env python3
"""Size a skill shelf against a reference one: `shelf_stats.py <ours> [<reference>]`.

Prints medians and the worst skills, so a critique starts from numbers.
The reference is a shallow clone, e.g. `git clone --depth 1 https://github.com/mattpocock/skills`.
"""
import os
import re
import statistics
import sys


def measure(root):
    rows = []
    for dirpath, _, names in os.walk(root):
        if "SKILL.md" not in names or "/.claude/" in dirpath:
            continue
        files = [os.path.join(a, f) for a, _, fs in os.walk(dirpath) for f in fs if not f.endswith(".pyc") and f != ".DS_Store"]
        md_lines = sum(open(f, errors="ignore").read().count("\n") for f in files if f.endswith(".md"))
        body = open(os.path.join(dirpath, "SKILL.md"), errors="ignore").read()
        front = body.split("---")[1] if body.startswith("---") else ""
        desc = re.search(r"^description:\s*(.*)$", front, re.M)
        rows.append({
            "name": os.path.basename(dirpath),
            "body": body.count("\n"),
            "md": md_lines,
            "files": len(files),
            "desc": len(desc.group(1).strip('"')) if desc else 0,
            "manual": "disable-model-invocation: true" in front,
        })
    return rows


def report(label, rows):
    med = lambda k: int(statistics.median(r[k] for r in rows))
    manual = sum(r["manual"] for r in rows)
    print(f"{label}: {len(rows)} skills | SKILL.md {med('body')} lines | whole skill {med('md')} md lines | "
          f"{med('files')} files | description {med('desc')} chars | manual-only {manual} ({manual * 100 // len(rows)}%)")


ours = measure(sys.argv[1])
report("ours", ours)
if len(sys.argv) > 2:
    report("reference", measure(sys.argv[2]))
print("\nheaviest, whole skill in md lines:")
for r in sorted(ours, key=lambda r: -r["md"])[:12]:
    print(f"  {r['md']:>6}  {r['files']:>3} files  {r['name']}")
