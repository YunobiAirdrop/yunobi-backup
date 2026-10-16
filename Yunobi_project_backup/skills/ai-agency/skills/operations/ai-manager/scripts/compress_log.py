#!/usr/bin/env python3
"""Compress an overgrown learned-patterns log to the rules alone.

A log past about 25 entries has stopped being a log and become a second body:
`skool` reached 128 entries and 80 KB, which is 20k tokens paid by every session
that opens the skill, before it does any work. Almost all of that weight is the
story, the quote and the numbers behind a rule that takes one line to state.

The rule stays and the run goes, because git already holds the run: the entry as
it was written is in the history of this file, one `git log -p` away, and it
costs a reader nothing there. A second markdown file beside the first is a body
nobody opens and a standard that rots.

The rule line comes from the entry's own bold spans, because these logs are
written symptom-first and rule-last with both in bold, and from its first
sentence where it has none. That is half the job: a log written in long sentences
comes out of here as long lines, so rewrite each one as the law plus one
checkable anchor, under the 240 characters `heal.cjs log` enforces.

    python3 compress_log.py <skill-dir-or-log.md> [--min 25] [--dry]

Exits 0 and does nothing when the log is under `--min` entries, so it is safe to
run over a whole registry. Commit before running it: the discarded evidence is
recoverable only from the commit that held it.
"""

import argparse
import os
import re
import sys

ISO = re.compile(r"^-\s+\*{0,2}(\d{4}-\d{2}-\d{2})\s*(?:\([^)]*\))?\s*[,.:–—-]\s*(.+)$")
DATED = re.compile(
    r"^-\s+\*{0,2}(\d{1,2})\s+([A-Z][a-z]{2})[a-z]*\.?\s+(\d{4})\s*[,.:;—–-]*\s*(.+)$"
)
HEAD = re.compile(r"^(#{2,3})\s+(.+)$")
MONTHS = "jan feb mar apr may jun jul aug sep oct nov dec".split()


def date_of(text):
    """`26 Aug 2026` and `2026-08-26` both read back as an ISO date."""
    iso = re.match(r"^\*{0,2}(\d{4}-\d{2}-\d{2})", text)
    if iso:
        return iso.group(1)
    human = re.match(r"^\*{0,2}(\d{1,2})\s+([A-Z][a-z]{2})[a-z]*\.?\s+(\d{4})", text)
    if human:
        month = MONTHS.index(human.group(2).lower()) + 1
        return f"{human.group(3)}-{month:02d}-{int(human.group(1)):02d}"
    return None


def entries(lines):
    """[(date, body_lines)] for every entry, in file order.

    An entry is a dated bullet and everything indented under it, or a dated
    heading and everything down to the next one. A Contents list of the same
    entries sits above the headings in some logs; it is dropped, because the
    index this writes replaces it.
    """
    heads = [i for i, l in enumerate(lines) if HEAD.match(l) and date_of(HEAD.match(l).group(2))]
    if heads:
        found = []
        for k, i in enumerate(heads):
            end = heads[k + 1] if k + 1 < len(heads) else len(lines)
            found.append((date_of(HEAD.match(lines[i]).group(2)), lines[i:end]))
        return found, heads[0]

    starts = [i for i, l in enumerate(lines) if ISO.match(l.strip()) or DATED.match(l.strip())]
    if not starts:
        return [], 0
    found = []
    for k, i in enumerate(starts):
        end = starts[k + 1] if k + 1 < len(starts) else len(lines)
        found.append((date_of(lines[i].strip()[2:]), lines[i:end]))
    return found, starts[0]


def rule_of(body):
    """The one line that states what the entry taught.

    These logs open an entry with the lesson in bold and follow it with the run
    that produced it, so the bold span is the rule and everything after it is
    evidence. Where there is no bold span the first sentence has to do.
    """
    text = " ".join(l.strip() for l in body).strip()
    text = re.sub(r"^#{2,3}\s+", "", text)
    text = re.sub(r"^-\s+", "", text)
    # Drop the date prefix, in either shape.
    text = re.sub(r"^\*{0,2}\d{4}-\d{2}-\d{2}\s*(?:\([^)]*\))?\s*[,.:–—-]\s*", "", text)
    text = re.sub(
        r"^\*{0,2}\d{1,2}\s+[A-Z][a-z]{2}[a-z]*\.?\s+\d{4}\s*[,.:;—–-]*\s*", "", text
    )
    # These entries are written symptom-first and rule-last, both in bold: "**X
    # answered 200 and moved nothing.** ... **Re-run the write.**" Taking only
    # the opening span gives an index of symptoms with no instruction in it, so
    # a closing span is carried too where the entry has one.
    spans = [s for s in re.findall(r"\*\*(.+?)\*\*", text) if len(s.strip()) > 30]
    if spans:
        rule = spans[0].strip()
        if len(spans) > 1 and spans[-1].strip() != rule:
            rule = f"{rule.rstrip('.')}. {spans[-1].strip()}"
    else:
        rule = re.split(r"(?<=[.!?])\s", text.replace("**", ""), maxsplit=1)[0]
    rule = re.sub(r"\s+", " ", rule).strip().rstrip(".")
    if len(rule) > 300:
        rule = rule[:297].rsplit(" ", 1)[0] + "..."
    return rule


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="a skill directory, or the log file itself")
    ap.add_argument("--min", type=int, default=25, help="entries below which nothing happens")
    ap.add_argument(
        "--min-chars",
        type=int,
        default=10000,
        help="a log this large splits whatever its entry count, because a few long entries "
        "cost a reader as much as many short ones",
    )
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    log = args.target
    if os.path.isdir(log):
        log = os.path.join(log, "references", "learned-patterns.md")
    if not os.path.exists(log):
        sys.exit(f"no log at {log}")

    raw = open(log, encoding="utf-8").read()
    lines = raw.split("\n")
    found, first = entries(lines)
    # Size is the real ceiling: a 23-entry log whose entries each carry a
    # paragraph of evidence costs a reader more than a 128-entry index does.
    if len(found) < args.min and len(raw) < args.min_chars:
        print(f"{os.path.relpath(log)}: {len(found)} entries, under {args.min}, left alone")
        return
    if len(found) < 5:
        print(f"{os.path.relpath(log)}: only {len(found)} entries parsed, leaving it for a human")
        return

    # A hand-maintained Contents list sits above the entries in some logs, and
    # the index written below replaces it. Dropping only its heading left all 43
    # of its bullets in the preamble, so the index carried every entry twice, in
    # two date formats, and the counter read 97 for a 54-entry log.
    preamble = [
        l
        for l in lines[:first]
        if not l.startswith("## Contents")
        and not ISO.match(l.strip())
        and not DATED.match(l.strip())
    ]
    while preamble and preamble[-1].strip() == "":
        preamble.pop()

    title = next((l for l in preamble if l.startswith("# ")), "# Learned patterns")
    body = [l for l in preamble if not l.startswith("# ")]

    index = [
        title,
        "",
        "One line per entry, newest first: what the run taught, without the run.",
    ]
    if any(l.strip() for l in body):
        index += ["", *[l for l in body if l.strip()]]
    index += [""]
    for date, entry in found:
        index.append(f"- {date}: {rule_of(entry)}")
    index.append("")

    index_text = "\n".join(index)
    saved = len("\n".join(lines)) - len(index_text)
    print(
        f"{os.path.relpath(log)}: {len(found)} entries, "
        f"{len(lines)} -> {len(index_text.splitlines())} lines, {saved} chars out of the read path"
    )
    if args.dry:
        return
    open(log, "w", encoding="utf-8").write(index_text)


if __name__ == "__main__":
    main()
