#!/usr/bin/env python3
"""Find routing pointers that name a skill or agent which does not exist.

A registry routes by name in prose: "belongs to `clickup-ops`", "invoke `board-spec`".
Nothing resolves those, so a merged or deleted asset leaves every pointer at it intact and
silent. Found 9 Sep 2026: `project-manager` listed twelve skills and four of them had been
gone long enough that nobody could say when, `discovery-system` routed the build phase to a
skill that never shipped, and `hyperframes-lane` promised a migration skill that does not exist.

    python3 scripts/dead_pointers.py [ai-doc-root] [--extra name,name]

Exits 1 when anything is dead. Names outside `ai-doc/` (a consumer's own skills, a CLI, a
reference filename) are the false-positive class: pass them with `--extra`, and prefer that
over widening the regex, because a pointer this misses is a pointer nothing checks.
"""

import pathlib
import re
import sys

argv = [a for a in sys.argv[1:] if not a.startswith("-")]
root = pathlib.Path(argv[0] if argv else pathlib.Path(__file__).resolve().parents[5])
extra = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--extra=")), "")

# Assets that exist here, plus the ones that live in a consumer repo or the harness and are
# still legitimate targets. Keep this list short; a name that stops being real has to show up.
KNOWN_ELSEWHERE = {
    "board-spec", "board-start", "board-ship", "board-move", "clickup-cli", "clickup-browser",
    "clickup-data-manager", "batch-workload", "impeccable", "ship", "release", "verify",
    "claude-api", "dataviz", "artifact-design", "update-config", "code-review", "run",
    "security-review", "voice-dna", "heyramzi-slop", "pass-cli",
    "claude-in-chrome", "chrome-devtools", "yt-dlp", "gws-workspace", "dokploy-network",
}

real = {f.parent.name for f in root.glob("skills/**/SKILL.md")}
real |= {f.stem for f in root.glob("agents/*/*.md") if f.name.lower() != "readme.md"}
real |= KNOWN_ELSEWHERE | {n for n in extra.split(",") if n}

# Only prose that hands work to a named asset. The verb has to sit next to the token, because a
# weak trigger ("is the", "owns") matches ordinary sentences and buries the real hits: a first
# cut on those reported 13 CSS classes, folder slugs and CLI names against one true positive.
NEAR = r"(?:[^`\n]{0,40})"
VERB = r"(?:invoke|invoked|route|routes|routed|belongs? to|dispatch(?:es|ed)? to|hand(?:s|ed)? (?:it |the |work )?(?:to|off to))"
ROUTING = re.compile(rf"(?:{VERB}{NEAR}`TOK`|`TOK`{NEAR}{VERB})", re.I)
SKILL_WORD = re.compile(r"`TOK`(?:\s+(?:skill|agent))|(?:the\s+)`TOK`\s+(?:skill|agent)", re.I)
TOKEN = re.compile(r"`([a-z][a-z0-9]+(?:-[a-z0-9]+){1,3})`")

dead = []
files = list(root.glob("skills/**/SKILL.md"))
files += [p for p in root.glob("agents/*/*.md") if p.name.lower() != "readme.md"]
for f in sorted(files):
    text = f.read_text(errors="ignore")
    for m in TOKEN.finditer(text):
        name = m.group(1)
        if name in real:
            continue
        line = text[text.rfind("\n", 0, m.start()) + 1 : text.find("\n", m.end())]
        tok = re.escape(f"`{name}`")
        routes = re.search(ROUTING.pattern.replace("`TOK`", tok), line, re.I)
        named = re.search(SKILL_WORD.pattern.replace("`TOK`", tok), line, re.I)
        if routes or named:
            n = text.count("\n", 0, m.start()) + 1
            dead.append((f.relative_to(root), n, name, line.strip()[:90]))

for path, n, name, line in dead:
    print(f"{path}:{n} routes to `{name}`, which does not exist")
    print(f"    {line}")
print(f"dead pointers: {len(dead)}" if dead else "dead pointers: none")
sys.exit(1 if dead else 0)
