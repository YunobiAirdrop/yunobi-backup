#!/usr/bin/env python3
"""Profile the Claude auto-memory stores under ~/.claude/projects/*/memory/.

Prints, per store: the index cost every session in that repo pays, and the
triage buckets (archive, fold, trim, orphan). Read-only. Never writes.

  python3 memory_cost.py                 # every store
  python3 memory_cost.py <repo-slug>     # one store, with the per-file table
  python3 memory_cost.py --fix-links     # repoint dead [[links]], report the rest
  python3 memory_cost.py <repo-slug> --usage   # write-to-read ratio from the transcripts
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path.home() / ".claude" / "projects"
WORD = re.compile(r"\S+")
LINK = re.compile(r"\[\[([^\]]+)\]\]")
INDEX_LINK = re.compile(r"\(([^)]+\.md)\)")
DESC = re.compile(r"^description:\s*(.*)$", re.M)
TYPE = re.compile(r"^\s*type:\s*(\w+)", re.M)
DEAD = re.compile(r"\b(RESOLVED|FIXED|DONE|SHIPPED|superseded|deprecated|no longer|obsolete)\b", re.I)
SKILL_REDIRECT = re.compile(r"(lives? in|now in|moved to|see|read|full .{0,20}in) the [`/]?[a-z0-9-]+[`]? skill", re.I)

BODY_WORDS_BUDGET = 250      # one fact, not an essay
INDEX_LINES_BUDGET = 60      # every session in the repo pays for these

WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
READ_TOOLS = {"Read", "Bash", "Grep", "Glob"}


def words(text):
    return len(WORD.findall(text))


def profile(store):
    files = sorted(p for p in store.glob("*.md") if p.name != "MEMORY.md")
    index = store / "MEMORY.md"
    index_text = index.read_text() if index.exists() else ""
    named = {p.stem for p in files}

    rows, linked = [], set()
    for p in files:
        text = p.read_text()
        head = text.split("---", 2)
        body = head[2] if len(head) > 2 else text
        desc = (DESC.search(text) or [None, ""])[1]
        linked |= set(LINK.findall(text))
        rows.append({
            "path": p,
            "name": p.stem,
            "words": words(body),
            "type": (TYPE.search(text) or [None, "?"])[1],
            "dead": bool(DEAD.search(desc)),
            "redirect": bool(SKILL_REDIRECT.search(body)),
            "indexed": p.name in index_text,
        })

    return {
        "store": store,
        "rows": rows,
        "index_lines": index_text.count("\n"),
        "index_words": words(index_text),
        "index_missing": sorted(
            t for t in INDEX_LINK.findall(index_text)
            if t != "MEMORY.md" and not (store / t).exists()
        ),
        "broken_links": sorted({l for l in linked if l not in named}),
    }


def buckets(r):
    out = []
    if r["dead"]:
        out.append("archive")
    if r["redirect"]:
        out.append("fold")
    if r["words"] > BODY_WORDS_BUDGET:
        out.append("trim")
    if not r["indexed"]:
        out.append("orphan")
    return out


def usage(store):
    """Count how often the store is written against how often it is opened.

    A memory earns its slot by being read. The session transcripts sit next to the
    store as `<session-id>.jsonl`, so the ratio is measurable: every explicit open
    (`Read`, a `cat` in `Bash`, a `Grep` over the folder) against every write.

    The recall injection does not appear in the transcript, so the read count is a
    floor on explicit opens, not a count of every time a memory reached the context.
    That is the number that matters anyway: a memory nothing ever opens is paying
    index rent for a fact no session used. Maintenance passes read the store too, so
    read the never-opened list before the ratio; it is the harder number to inflate.
    """
    names = {p.name for p in store.glob("*.md")}
    sessions = sorted(store.parent.glob("*.jsonl"))
    wrote, read = set(), set()
    per_file = {n: 0 for n in names}

    for path in sessions:
        sid = path.stem
        for line in path.open(errors="ignore"):
            if "/memory/" not in line:
                continue
            try:
                blocks = (json.loads(line).get("message") or {}).get("content")
            except (json.JSONDecodeError, AttributeError):
                continue
            if not isinstance(blocks, list):
                continue
            for b in blocks:
                if not isinstance(b, dict) or b.get("type") != "tool_use":
                    continue
                tool = b.get("name")
                blob = json.dumps(b.get("input", {}))
                if f"{store}" not in blob:
                    continue
                if tool in WRITE_TOOLS:
                    wrote.add(sid)
                elif tool in READ_TOOLS:
                    read.add(sid)
                    for n in names:
                        if n in blob:
                            per_file[n] += 1

    return {
        "sessions": len(sessions),
        "wrote": len(wrote),
        "read": len(read),
        "never_read": sorted(n for n, c in per_file.items() if not c and n != "MEMORY.md"),
    }


def fix_links(store):
    """Repoint links broken by a changed naming convention or a .md suffix.

    Only rewrites a link when exactly one file on disk matches after normalising
    hyphens, underscores and the suffix. Ambiguous or genuinely absent targets are
    left alone and reported, because guessing loses the fact.
    """
    names = {p.stem for p in store.glob("*.md") if p.name != "MEMORY.md"}
    canon = {}
    for n in names:
        canon.setdefault(n.replace("-", "_").lower().removesuffix(".md"), []).append(n)

    fixed, unresolved = [], set()
    for p in store.glob("*.md"):
        text = original = p.read_text()
        for raw in set(LINK.findall(text)):
            if raw in names:
                continue
            hit = canon.get(raw.replace("-", "_").lower().removesuffix(".md"), [])
            if len(hit) == 1:
                text = text.replace(f"[[{raw}]]", f"[[{hit[0]}]]")
                fixed.append((p.name, raw, hit[0]))
            else:
                unresolved.add(raw)
        if text != original:
            p.write_text(text)
    return fixed, unresolved


def main():
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--fix-links" in sys.argv:
        for store in sorted(p for p in ROOT.glob("*/memory") if any(p.glob("*.md"))):
            if argv and not any(a in store.parent.name for a in argv):
                continue
            fixed, unresolved = fix_links(store)
            if fixed or unresolved:
                print(f"{store.parent.name}: {len(fixed)} repointed, "
                      f"{len(unresolved)} unresolved")
                for u in sorted(unresolved):
                    print(f"  no target for [[{u}]] - remove the sentence or write the memory")
        return

    target = argv[0] if argv else None
    stores = sorted(p for p in ROOT.glob("*/memory") if any(p.glob("*.md")))
    if target:
        stores = [s for s in stores if target in s.parent.name]
        if not stores:
            sys.exit(f"no memory store matching {target!r}")

    total_files = total_index = 0
    print(f"{'files':>6} {'idx-lines':>10} {'idx-tok':>8} {'archive':>8} {'fold':>5} "
          f"{'trim':>5} {'orphan':>7}  store")
    print("-" * 86)
    reports = []
    for store in stores:
        rep = profile(store)
        reports.append(rep)
        tally = {k: 0 for k in ("archive", "fold", "trim", "orphan")}
        for r in rep["rows"]:
            for b in buckets(r):
                tally[b] += 1
        idx_tok = rep["index_words"] * 4 // 3
        total_files += len(rep["rows"])
        total_index += idx_tok
        flag = "!" if rep["index_lines"] > INDEX_LINES_BUDGET else " "
        print(f"{len(rep['rows']):>6} {rep['index_lines']:>9}{flag} {idx_tok:>8} "
              f"{tally['archive']:>8} {tally['fold']:>5} {tally['trim']:>5} "
              f"{tally['orphan']:>7}  {store.parent.name}")

    print("-" * 86)
    print(f"{total_files:>6} {'':>10} {total_index:>8}  "
          f"tokens of index loaded per session, summed across stores")

    for rep in reports:
        issues = rep["index_missing"] or rep["broken_links"]
        if issues:
            print(f"\n{rep['store'].parent.name}")
            for t in rep["index_missing"]:
                print(f"  index points at a missing file: {t}")
            for l in rep["broken_links"]:
                print(f"  [[{l}]] resolves to nothing")

    if target:
        rep = reports[0]
        print(f"\nper-file triage for {rep['store'].parent.name}\n" + "-" * 86)
        for r in sorted(rep["rows"], key=lambda r: -r["words"]):
            b = buckets(r)
            if b:
                print(f"{r['words']:>5}w  {r['type']:<9} {','.join(b):<24} {r['name']}")

        if "--usage" in sys.argv:
            u = usage(rep["store"])
            ratio = f"{u['wrote'] / u['read']:.1f}:1" if u["read"] else "no reads"
            print(f"\nusage across {u['sessions']} transcripts\n" + "-" * 86)
            print(f"  sessions that wrote a memory: {u['wrote']}")
            print(f"  sessions that opened one:     {u['read']}")
            print(f"  write-to-read ratio:          {ratio}")
            if u["never_read"]:
                print(f"  never opened by any session ({len(u['never_read'])}):")
                for n in u["never_read"]:
                    print(f"    {n}")


if __name__ == "__main__":
    main()
