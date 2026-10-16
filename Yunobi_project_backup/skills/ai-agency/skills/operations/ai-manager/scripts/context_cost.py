#!/usr/bin/env python3
"""Measure what a Claude extension registry costs in context.

Metadata (name + description) of every asset is preloaded into every session,
so it is paid for whether or not the asset is ever used. Bodies are paid for
once loaded. References are free until read. This reports all three against
the budgets in SKILL.md.

It also measures the two shapes that make a registry grow without any asset
being added: a failure log that has become a second body, and a block of prose
copied across files. Neither shows up in an asset count and both are paid for on
every read.

Usage:
    python3 context_cost.py <folder> [--json] [--top N] [--dupes N]

Exit 1 on a hard violation (missing frontmatter, description over 1024 chars,
duplicate registered name), else 0.
"""

import argparse
import json
import os
import re
import sys

DESC_TARGET = 500  # chars; soft budget, one sentence of what + one of when
DESC_HARD = 1024  # chars; platform maximum
BODY_MAX = 200  # lines; every skill .md and agent bodies, as scripts/check-skill-length.mjs
REF_TOC = 100  # lines; reference files past this need a table of contents
CHARS_PER_TOKEN = 4
LOG_ENTRIES_MAX = 25  # entries; past this a failure log has become a second body
DUP_MIN_CHARS = 120  # a shorter repeated block is a turn of phrase, not a copy
DUP_MIN_COPIES = 3  # two copies is a pair to read, three is a pattern to fix

FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LOG_ENTRY = re.compile(
    r"^\s*(?:[-*]\s+|#{2,3}\s+)\*{0,2}(?:\d{4}-\d{2}-\d{2}|\d{1,2}\s+[A-Z][a-z]{2}[a-z]*\.?\s+\d{4})",
    re.M,
)
FIELD = re.compile(r"^(\w[\w-]*):\s*(.*(?:\n[ \t]+.*)*)", re.M)
LINK = re.compile(r"\[[^\]]*\]\(([^)#]+\.md)[^)]*\)")
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
TOC = re.compile(r"^#{1,3}\s*(contents|table of contents)\b", re.M | re.I)
RESERVED = ("anthropic", "claude")


def parse(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    m = FM.match(text)
    if not m:
        return None, text, text.count("\n") + 1
    fields = {k: v.strip().strip("\"'") for k, v in FIELD.findall(m.group(1))}
    body = text[m.end() :]
    return fields, body, body.count("\n") + 1


def lines(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return sum(1 for _ in fh)


def collect(root):
    """Return (assets, reference_files). Assets are skills and agents."""
    assets, refs = [], []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
        for name in filenames:
            if not name.endswith(".md") or name in ("README.md", "LICENSE.md"):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root)
            parts = rel.split(os.sep)
            if name == "SKILL.md":
                assets.append(("skill", path, rel))
            elif "agents" in parts or "commands" in parts:
                assets.append(("agent" if "agents" in parts else "command", path, rel))
            elif ("references" in parts or "reference" in parts) and owning_skill(dirpath):
                # Only files a SKILL.md can reach. A top-level corpus of vendored
                # documents is not a skill reference and is not held to the rules.
                refs.append((path, rel))
    return assets, refs


def owning_skill(dirpath):
    """True when some ancestor directory holds a SKILL.md."""
    d = dirpath
    while True:
        if os.path.exists(os.path.join(d, "SKILL.md")):
            return True
        parent = os.path.dirname(d)
        if parent == d:
            return False
        d = parent


def vendored(path, root):
    """True when this file sits under a pack that tracks an upstream repo.

    A pack copied verbatim from upstream has internal repeats that are upstream's
    business: editing them is discarded on the next refresh, and reporting them
    buries the findings that can be acted on. The marker is a `version:` in the
    skill's frontmatter, which is how an upstream pack pins the release it was
    taken from. The `VENDOR.md` marker went with the vendor files on
    29 Aug 2026.
    """
    d = os.path.dirname(os.path.abspath(path))
    stop = os.path.abspath(root)
    while d.startswith(stop):
        skill = os.path.join(d, "SKILL.md")
        if os.path.exists(skill):
            fields, _, _ = parse(skill)
            if fields and "version" in fields:
                return True
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return False


def failure_logs(root):
    """Every learned-patterns file, with the entries and the bytes it holds.

    A log is the one part of a registry with no ceiling on it: every run may add
    to it and nothing ever takes anything out, so it outgrows the skill it
    belongs to without a single asset being added. Counting it is what makes the
    25-entry rule fire.
    """
    found = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
        for name in filenames:
            if not name.startswith("learned-patterns") or not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            text = open(path, encoding="utf-8", errors="replace").read()
            found.append(
                {
                    "path": os.path.relpath(path, root),
                    "entries": len(LOG_ENTRY.findall(text)),
                    "chars": len(text),
                    "archive": "archive" in name,
                }
            )
    return sorted(found, key=lambda f: -f["chars"])


def duplicate_blocks(root):
    """Paragraphs of real length that appear in more than one file.

    The waste figure is what the copies cost beyond the first, which is the
    number that decides whether consolidating is worth the hop it adds.
    """
    blocks = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            if vendored(path, root):
                continue
            text = open(path, encoding="utf-8", errors="replace").read()
            m = FM.match(text)
            if m:
                text = text[m.end() :]
            for para in re.split(r"\n\s*\n", text):
                norm = " ".join(para.split())
                if len(norm) < DUP_MIN_CHARS:
                    continue
                blocks.setdefault(norm, set()).add(os.path.relpath(path, root))
    dupes = [
        {
            "copies": len(files),
            "chars": len(norm),
            "waste": len(norm) * (len(files) - 1),
            "text": norm[:120],
            "files": sorted(files),
        }
        for norm, files in blocks.items()
        if len(files) >= DUP_MIN_COPIES
    ]
    return sorted(dupes, key=lambda d: -d["waste"])


def audit(root, top, dupes_top=10):
    assets, refs = collect(root)
    logs = failure_logs(root)
    dupes = duplicate_blocks(root)
    rows, hard, soft = [], [], []
    seen = {}

    for kind, path, rel in assets:
        fields, body, body_lines = parse(path)
        # Commands take their name from the filename, so only description is required there.
        required = ("description",) if kind == "command" else ("name", "description")
        if fields is None or any(f not in fields for f in required):
            hard.append(f"{rel}: missing frontmatter {'/'.join(required)}")
            continue
        name = fields.get("name") or os.path.splitext(os.path.basename(rel))[0]
        desc = " ".join(fields["description"].split())
        rows.append({"kind": kind, "name": name, "path": rel, "desc": len(desc), "body": body_lines})

        if name in seen:
            hard.append(f"{rel}: registered name '{name}' also used by {seen[name]}")
        seen[name] = rel
        if len(desc) > DESC_HARD:
            hard.append(f"{rel}: description {len(desc)} chars, over the {DESC_HARD} maximum")
        elif len(desc) > DESC_TARGET:
            soft.append(f"{rel}: description {len(desc)} chars, over the {DESC_TARGET} budget")
        if body_lines > BODY_MAX:
            soft.append(f"{rel}: body {body_lines} lines, over the {BODY_MAX} budget, split to references")
        if kind == "skill":
            if len(name) > 64 or not re.fullmatch(r"[a-z0-9-]+", name):
                hard.append(f"{rel}: name '{name}' must be lowercase kebab-case, 64 chars maximum")
            if any(w in name.lower() for w in RESERVED):
                hard.append(f"{rel}: name '{name}' uses a reserved word")

        # Nested references: a bundled file linked from SKILL.md must not link onward
        # to a third file. A link to another skill's SKILL.md is a route, not a reference.
        if kind == "skill":
            # Normalised, because normpath strips a leading "./" from the child
            # and an un-normalised base then never prefix-matches it.
            base = os.path.normpath(os.path.dirname(path))
            # A file SKILL.md already links is reachable in one hop, so a sibling
            # pointing at it as well is a cross-reference, not a nested chain.
            # An absolute URL is not a bundled reference, so it is never resolved
            # as a local path. Without this every external link ending in .md read
            # as a broken file: four of the eight hard findings on 2026-08-25 were
            # links to remotion.dev.
            def local(l):
                return not l.startswith(("http://", "https://", "mailto:", "#"))

            # A link inside a fenced block is sample markdown, not a reference.
            # The Make migration reference shows a batch-tracker line as a template, and it read
            # as a broken file on every run.
            body = FENCE.sub("", body)

            direct = {os.path.normpath(os.path.join(base, l)) for l in LINK.findall(body) if local(l)}
            for link in dict.fromkeys(l for l in LINK.findall(body) if local(l)):
                child = os.path.normpath(os.path.join(base, link))
                if not os.path.exists(child):
                    hard.append(f"{rel}: broken link to {link}")
                    continue
                if not child.startswith(base + os.sep) or os.path.basename(child) == "SKILL.md":
                    continue
                _, child_body, _ = parse(child)
                for grandchild in dict.fromkeys(LINK.findall(child_body)):
                    target = os.path.normpath(os.path.join(os.path.dirname(child), grandchild))
                    if os.path.exists(target) and os.path.basename(target) != "SKILL.md" and target not in direct:
                        soft.append(f"{rel}: {link} links onward to {grandchild}, keep references one level deep")

    for path, rel in refs:
        n = lines(path)
        if n <= REF_TOC:
            continue
        text = open(path, encoding="utf-8", errors="replace").read()
        # A flat file (a dated log, a glossary, a list of entries) has no sections
        # to index, so a Contents list there would name nothing.
        if len(re.findall(r"^##\s+\S", text, re.M)) < 3:
            continue
        if not TOC.search(text):
            soft.append(f"{rel}: {n} lines with no Contents heading, add one so partial reads see the scope")

    for log in logs:
        if not log["archive"] and log["entries"] > LOG_ENTRIES_MAX:
            soft.append(
                f"{log['path']}: {log['entries']} entries, over the {LOG_ENTRIES_MAX} budget, "
                f"compress each entry to its rule with compress_log.py"
            )
    for d in dupes:
        soft.append(
            f"{d['files'][0]}: a {d['chars']}-char block is copied into "
            f"{d['copies'] - 1} other file(s), {d['waste']} chars of waste"
        )

    meta = sum(r["desc"] + len(r["name"]) for r in rows)
    report = {
        "assets": len(rows),
        "metadata_chars": meta,
        "metadata_tokens": meta // CHARS_PER_TOKEN,
        "references": len(refs),
        "hard": hard,
        "soft": soft,
        "worst_descriptions": sorted(rows, key=lambda r: -r["desc"])[:top],
        "worst_bodies": sorted(rows, key=lambda r: -r["body"])[:top],
        "log_chars": sum(l["chars"] for l in logs),
        "worst_logs": [l for l in logs if not l["archive"]][:top],
        "duplicate_waste": sum(d["waste"] for d in dupes),
        "worst_duplicates": dupes[:dupes_top],
    }
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--dupes", type=int, default=10, help="how many duplicated blocks to name")
    args = ap.parse_args()

    r = audit(args.folder, args.top, args.dupes)
    if args.json:
        print(json.dumps(r, indent=2))
        return 1 if r["hard"] else 0

    print(f"{r['assets']} assets, {r['references']} reference files")
    print(f"always-loaded metadata: {r['metadata_chars']} chars, about {r['metadata_tokens']} tokens\n")
    print(f"widest descriptions (budget {DESC_TARGET}):")
    for x in r["worst_descriptions"]:
        print(f"  {x['desc']:5d}  {x['name']}")
    print(f"\nlongest bodies (budget {BODY_MAX} lines):")
    for x in r["worst_bodies"]:
        print(f"  {x['body']:5d}  {x['name']}")
    print(f"\nfailure logs: {r['log_chars']} chars total (budget {LOG_ENTRIES_MAX} entries each):")
    for x in r["worst_logs"][:5]:
        print(f"  {x['entries']:5d} entries {x['chars']:7d} chars  {x['path']}")
    print(f"\nduplicated blocks: {r['duplicate_waste']} chars of copies beyond the first")
    for x in r["worst_duplicates"][:5]:
        print(f"  {x['copies']:3d}x {x['waste']:6d}  {x['text'][:80]}")
    if r["hard"]:
        print(f"\nHARD ({len(r['hard'])}):")
        for m in r["hard"]:
            print(f"  {m}")
    if r["soft"]:
        print(f"\nSOFT ({len(r['soft'])}):")
        for m in r["soft"]:
            print(f"  {m}")
    return 1 if r["hard"] else 0


if __name__ == "__main__":
    sys.exit(main())
