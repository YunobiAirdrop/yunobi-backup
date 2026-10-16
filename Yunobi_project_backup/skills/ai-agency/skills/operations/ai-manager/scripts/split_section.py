#!/usr/bin/env python3
"""Move named sections out of a SKILL.md into a reference, leaving a pointer.

The bodies pass does this same operation every time: lift whole `##` sections
verbatim, give the new file a Contents list, and put one link where the sections
used to sit. Doing it by hand re-derives the line offsets on every skill and gets
them wrong when a section heading repeats.

    python3 split_section.py <SKILL.md> \\
        --sections "The nine laws" "Undo is a button" \\
        --into references/laws.md \\
        --title "The nine laws of driving the editor" \\
        --pointer "One line of prose, then the link is appended." \\
        [--intro "A line under the Contents list."] [--dry]

Sections are matched on the start of the heading text, so a prefix is enough.
They must be contiguous or the pointer lands where the first one was and the
rest are lifted from where they sit. Exits 1 if a section is not found.
"""

import argparse
import os
import re
import sys


def sections(lines):
    """[(title, start, end)] for every `## ` heading, end exclusive."""
    heads = [i for i, l in enumerate(lines) if l.startswith("## ")]
    return [
        (lines[i][3:].strip(), i, heads[k + 1] if k + 1 < len(heads) else len(lines))
        for k, i in enumerate(heads)
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skill")
    ap.add_argument("--sections", nargs="+", required=True)
    ap.add_argument("--into", required=True, help="path relative to the skill directory")
    ap.add_argument("--title", required=True, help="H1 of the new reference")
    ap.add_argument("--pointer", required=True, help="prose that replaces the moved sections")
    ap.add_argument("--heading", help="heading for the pointer; defaults to the first moved section's")
    ap.add_argument("--intro", default="", help="a line under the Contents list")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    lines = open(args.skill, encoding="utf-8").read().split("\n")
    found = sections(lines)

    picked = []
    for want in args.sections:
        hit = [s for s in found if s[0].startswith(want)]
        if not hit:
            sys.exit(f"no section starting with {want!r} in {args.skill}")
        if len(hit) > 1:
            sys.exit(f"{want!r} matches {len(hit)} sections; give more of the heading")
        picked.append(hit[0])
    picked.sort(key=lambda s: s[1])

    moved = []
    for _, a, b in picked:
        moved.extend(lines[a:b])

    # Contents from the moved headings, so a partial read still sees the scope.
    # One section moving means its own heading would only repeat the new H1, so
    # it goes and the sub-headings become the contents.
    if len(picked) == 1:
        moved = moved[1:]
        heads = [h[4:].strip() for h in moved if h.startswith("### ")]
    else:
        heads = [h[3:].strip() for h in moved if h.startswith("## ")]
    body = "\n".join(moved).strip()
    ref = f"# {args.title}\n\n"
    # A Contents list earns its place only where a partial read is likely, which
    # is past 100 lines. Below that it is a second title.
    if heads and body.count("\n") > 100:
        ref += "## Contents\n\n" + "\n".join(f"- {h}" for h in heads) + "\n\n"
    if args.intro:
        ref += args.intro.strip() + "\n\n"
    ref += body + "\n"

    link = os.path.relpath(args.into, ".") if args.into.startswith("references") else args.into
    pointer = f"## {args.heading or picked[0][0]}\n\n{args.pointer.strip()} See [`{link}`]({link}).\n"

    out, cut = [], {i for _, a, b in picked for i in range(a, b)}
    for i, l in enumerate(lines):
        if i == picked[0][1]:
            out.extend(pointer.split("\n"))
        if i not in cut:
            out.append(l)

    # A link written from SKILL.md points at `references/x.md`; the same link one
    # level down inside references/ has to lose that prefix, and a link to a file
    # beside SKILL.md has to climb back out. Rewriting them here is the difference
    # between a split that reads and a split that leaves dead links behind.
    depth = args.into.count("/")
    if depth:
        prefix = "references/"
        ref = re.sub(r"\]\(" + re.escape(prefix) + r"([^)/]+\))", r"](\1", ref)
        ref = re.sub(r"\]\((?!https?:|#|\.\./|" + re.escape(prefix) + r")([^)]+\.[a-z]{1,4}\))",
                     r"](../\1", ref)

    dest = os.path.join(os.path.dirname(os.path.abspath(args.skill)), args.into)
    print(f"{len(lines)} -> {len(out)} lines; {args.into} gets {ref.count(chr(10)) + 1} lines")
    if args.dry:
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w", encoding="utf-8").write(ref)
    open(args.skill, "w", encoding="utf-8").write("\n".join(out))


if __name__ == "__main__":
    main()
