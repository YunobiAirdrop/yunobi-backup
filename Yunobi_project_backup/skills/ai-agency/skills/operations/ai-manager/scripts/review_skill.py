#!/usr/bin/env python3
"""
review_skill - the mechanical half of a skill review.

Everything here is checkable without reading the skill for meaning: frontmatter
constraints, body size, whether a linked file exists, whether a backticked path into
a sibling repo is still on disk, whether a script can be driven by an agent, and the
shapes references/skill-floor.md refuses. The half that needs judgement (does the description trigger
on the right prompts, is a fragile step prescriptive enough) is in
references/review-rubric.md and stays there.

Runs over one skill directory or a whole tree. No dependencies.

  python3 review_skill.py <path> [--json] [--quiet]

Exits 1 when any skill has an error, 0 otherwise.
"""

import json
import os
import re
import sys
from pathlib import Path

# Ceilings from the claude.ai upload and Skills API spec. Claude Code itself
# is looser, so treat these as the portable limit.
NAME_MAX = 64
DESCRIPTION_MAX = 1024

# A body past either of these stops being an overview. Roughly 4 chars a token.
BODY_MAX_LINES = 500
BODY_MAX_TOKENS = 5000

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^```.*?^```", re.M | re.DOTALL)
# `- [Title](file.md)` inside a backtick span is a format template, not a link.
CODESPAN_RE = re.compile(r"`[^`\n]+`")
# "I can help you", "you should run" - a description written at the reader
# instead of about the skill.
PERSON_RE = re.compile(r"\b(I can|I will|I'll|we can|we will|you should|you can|your skill)\b", re.I)
# Some form of "use when" is what tells the runtime when to pick the skill.
TRIGGER_RE = re.compile(r"\buse (this skill )?(when|whenever|for|before|after|on|the moment|as soon as|once|any time)\b", re.I)

# The mechanical half of references/skill-floor.md. Each one is a shape a reader
# can see without knowing what the skill is for.

# A pointer with no condition. The condition is the whole point of a pointer.
UNCONDITIONAL_RE = re.compile(
    r"(see (the )?`?references?/|refer to (the )?references?|for (more )?(details|information),? see)", re.I)
# Shouted absolutes where the reason would do the same work better.
SHOUT_RE = re.compile(r"(?<![A-Za-z])(ALWAYS|NEVER|MUST NOT|DO NOT|IMPORTANT|CRITICAL)(?![A-Za-z])")
# A claim stamped with a date ages into a lie that still reads as current.
DATED_RE = re.compile(
    r"\bas of (January|February|March|April|May|June|July|August|September|October|November|December|\d{4})", re.I)
# Headings an imported pack ships that carry nothing this workspace decided.
FILLER_HEADING_RE = re.compile(
    r"^#{2,4}\s*(Initial Assessment|Best Practices|Common Mistakes|Success Metrics|Key Benefits|"
    r"Core Responsibilities|Overview)\s*$", re.I | re.M)
# "You are **X**, an expert who..." is an agent persona, not a procedure.
PERSONA_RE = re.compile(r"^\s*You are (\*\*)?[A-Z]", re.M)
# A reference that says where it used to live is telling the reader about the
# registry's own history, which no session needs before doing the work.
NARRATION_RE = re.compile(
    r"((Moved|Split) out of `?SKILL\.md`?|to hold it under the \d+-line ceiling)", re.I)

# A reference past this has become a second body, whatever its headings say.
REFERENCE_MAX_LINES = 400
# Build output and editor droppings. Regenerable, so they are deleted, not read.
JUNK_RE = re.compile(r"(^|/)(__pycache__|\.DS_Store|node_modules|\.pytest_cache)(/|$)|\.pyc$")


def links_in(text):
    """Markdown links outside code. A link in a fence or a backtick span is a template."""
    return LINK_RE.findall(CODESPAN_RE.sub("", FENCE_RE.sub("", text)))


def is_file_link(target):
    """A link worth resolving: local, with an extension, no template placeholder."""
    if not target or "://" in target or target.startswith("mailto:"):
        return False
    if "{" in target or "}" in target or "$" in target:
        return False
    return bool(re.search(r"\.[A-Za-z0-9]{1,5}$", target))


def parse_frontmatter(text):
    """Return (dict, body). Flat scalars only, which is all a SKILL.md carries."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    fields, key = {}, None
    for line in match.group(1).split("\n"):
        top = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if top:
            key = top.group(1)
            fields[key] = top.group(2).strip()
        elif key and line.strip():
            # Folded (">") or block ("|") scalar, or a wrapped quoted string.
            fields[key] = (fields[key] + " " + line.strip()).strip()
    for key, value in fields.items():
        if value[:1] in {">", "|"}:
            value = value[1:].lstrip("-+ ")
        if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key] = value.strip()
    return fields, text[match.end():]


def check_frontmatter(fields, skill_dir, add):
    if fields is None:
        add("error", "No YAML frontmatter.")
        return
    name = fields.get("name")
    if not name:
        add("error", "Frontmatter has no 'name'.")
    else:
        if not NAME_RE.match(name):
            add("error", f"name '{name}' is not lowercase-hyphen-case.")
        if len(name) > NAME_MAX:
            add("error", f"name is {len(name)} chars, over the {NAME_MAX} ceiling.")
        if name != skill_dir.name:
            add("error", f"name '{name}' does not match its directory '{skill_dir.name}'.")
        # Reserved by the claude.ai upload and Skills API, not by Claude Code
        # itself, so a local-only skill named this way still loads.
        if re.search(r"claude|anthropic", name, re.I):
            add("warn", f"name '{name}' contains a reserved word; it cannot be uploaded to claude.ai.")

    description = fields.get("description")
    if not description:
        add("error", "Frontmatter has no 'description'.")
        return
    if len(description) > DESCRIPTION_MAX:
        add("error", f"description is {len(description)} chars, over the {DESCRIPTION_MAX} ceiling.")
    if "<" in description or ">" in description:
        add("error", "description contains an angle bracket, which breaks the loader.")
    if len(description) < 60:
        add("warn", f"description is {len(description)} chars, too thin to trigger reliably.")
    if not TRIGGER_RE.search(description):
        add("warn", "description says what the skill does but never when to use it.")
    person = PERSON_RE.search(description)
    if person:
        add("warn", f"description is written in first or second person ('{person.group(0)}').")


def check_body(body, add):
    lines = body.count("\n") + 1
    tokens = len(body) // 4
    if lines > BODY_MAX_LINES or tokens > BODY_MAX_TOKENS:
        add("warn", f"body is {lines} lines / ~{tokens} tokens; move detail to references/.")
    return lines, tokens


def check_links(body, skill_dir, add):
    """Every local link resolves, one level deep, no backslashes."""
    linked = set()
    for target in links_in(body):
        target = target.split("#")[0].strip()
        if not is_file_link(target):
            continue
        if "\\" in target:
            add("error", f"link '{target}' uses backslashes; paths are forward slashes.")
            continue
        path = (skill_dir / target).resolve()
        if not path.exists():
            add("error", f"link '{target}' points at a file that does not exist.")
            continue
        linked.add(path)
        # Siblings inside references/ may cross-link freely; a chain only hurts
        # when a link in it is dead, because the agent has already spent the read.
        if path.suffix == ".md":
            for onward in links_in(path.read_text(errors="replace")):
                onward = onward.split("#")[0].strip()
                if not is_file_link(onward):
                    continue
                if (path.parent / onward).exists():
                    continue
                # The commonest way a reference link breaks: written as if from
                # SKILL.md while the file already sits inside references/.
                if onward.startswith("references/") and (path.parent / onward[len("references/"):]).exists():
                    add("error", f"'{target}' links to '{onward}'; from inside references/ that path is '{onward[len('references/'):]}'.")
                else:
                    add("warn", f"'{target}' links on to '{onward}', which does not exist.")
    return linked


STUDIO = Path.home() / "Studio"
# A backtick span shaped like a path into a sibling repo: `<repo>/src/lib/x.ts`,
# `vibe-kit/CLIs/mercury/`. Only spans with an extension or a trailing slash
# are claims about a file; a bare `app` is a name.
REPO_PATH_RE = re.compile(r"^[A-Za-z0-9_.-]+/[^\s`]*(?:\.[A-Za-z0-9]{1,5}|/)$")
PLACEHOLDER_RE = re.compile(r"[{}$<>*?|]|\bYYYY\b|\.\.\.")


def check_repo_paths(body, add):
    """A path into a sibling repo names a file on this disk, so check the disk.

    A prompt audit on 2 Sep 2026 found twelve of these dead across 146 skills, every
    one left behind by a rename or a reorg the skill never heard about, and the model
    follows a literal path rather than noticing it is gone. Markdown links were
    already resolved; this closes the same gap for the backticked kind.
    """
    if not STUDIO.is_dir():
        return
    # `.claude/...` is a path inside whichever project the skill runs in, not a repo.
    repos = {p.name for p in STUDIO.iterdir() if p.is_dir() and not p.name.startswith(".")}
    prose = FENCE_RE.sub("", body)
    seen = set()
    for span in CODESPAN_RE.findall(prose):
        candidate = span.strip("`").strip()
        if candidate in seen or PLACEHOLDER_RE.search(candidate):
            continue
        if not REPO_PATH_RE.match(candidate) or candidate.split("/", 1)[0] not in repos:
            continue
        seen.add(candidate)
        if not (STUDIO / candidate).exists():
            add("warn", f"`{candidate}` names a file that is not on disk; a rename or reorg left it behind.")


def reachable(skill_dir, body):
    """Files an agent can arrive at from SKILL.md, following hubs like INDEX.md.

    A file counts as reached if a page already reached links to it or names it in
    prose, because either one tells the agent it exists. Anything left over is
    read by nobody.
    """
    found, frontier = set(), [body]
    while frontier:
        text = frontier.pop()
        for target in links_in(text):
            target = target.split("#")[0].strip()
            if not is_file_link(target):
                continue
            path = (skill_dir / target).resolve()
            if path.exists() and path not in found:
                found.add(path)
                if path.suffix == ".md":
                    frontier.append(path.read_text(errors="replace"))
        for path in skill_dir.rglob("*.md"):
            path = path.resolve()
            if path not in found and path.name in text:
                found.add(path)
                frontier.append(path.read_text(errors="replace"))
    return found


def vendored_paths(skill_dir):
    """Paths the skill declares this workspace does not shape.

    A file copied verbatim from a scrape or an upstream pack cannot be given
    headings that survive its next refresh, so the shape checks skip it. Dead
    links are still reported: a broken link costs the reader the same whoever
    wrote it.

    Prose alone cannot answer this, so the list is frontmatter in the skill's own
    `SKILL.md`. It used to live in a `VENDOR.md`, which went with the rest of the
    vendor files on 29 Aug 2026:

        ---
        vendored:
          - references/contemporary/huevaluechroma
        ---
    """
    note = skill_dir / "SKILL.md"
    if not note.exists():
        return set()
    text = note.read_text(errors="replace")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return set()
    paths, collecting = set(), False
    for line in match.group(1).split("\n"):
        if re.match(r"^vendored:", line):
            collecting = True
            continue
        if collecting:
            item = re.match(r"^\s+-\s*(.+?)\s*$", line)
            if item:
                paths.add(item.group(1).strip("\"'"))
                continue
            break
    return paths


def is_vendored(rel_path, vendored):
    """True when the path, or a directory above it, is declared vendored."""
    parts = Path(rel_path).parts
    return any("/".join(parts[:i]) in vendored for i in range(1, len(parts) + 1))


def check_bundled(skill_dir, linked, body, add):
    references = skill_dir / "references"
    vendored = vendored_paths(skill_dir)
    if references.is_dir():
        reached = reachable(skill_dir, body)
        for path in sorted(references.rglob("*.md")):
            rel = path.relative_to(references)
            if is_vendored(f"references/{rel}", vendored):
                continue
            if path.resolve() not in reached:
                add("warn", f"references/{rel} is not reachable from SKILL.md.")
            # The evidence behind a rule is in git, where it costs nothing to
            # carry. A second log beside the first is a body nobody reads.
            if path.name == "learned-patterns-archive.md":
                add("error", f"references/{rel}: the run belongs in git, not in a second log.")
                continue
            # Failure logs are append-only and dated, not documents. Their shape
            # and their ceiling belong to ai-manager.
            if path.stem.startswith("learned-patterns"):
                continue
            text = path.read_text(errors="replace")
            length = text.count("\n") + 1
            if length > REFERENCE_MAX_LINES:
                add("warn", f"references/{rel} is {length} lines; that is a second body, not a reference.")
            if text.count("\n") > 100:
                if not re.search(r"^#{2,3} ", text, re.M):
                    add("warn", f"references/{rel} is over 100 lines with no headings.")
            match = NARRATION_RE.search(text)
            if match:
                add("warn", f"references/{rel} narrates its own move ('{match.group(0)}'); cut it.")

    for path in sorted(skill_dir.rglob("*")):
        rel = path.relative_to(skill_dir)
        if JUNK_RE.search(str(rel)):
            add("error", f"{rel} is build output; delete it and ignore it.")
            break

    scripts = skill_dir / "scripts"
    if scripts.is_dir():
        for path in sorted(scripts.iterdir()):
            if not path.is_file() or path.suffix not in {".py", ".sh", ".mjs", ".cjs", ".js", ".ts"}:
                continue
            source = path.read_text(errors="replace")
            if re.search(r"^\s*(input\(|read -[pr])", source, re.M):
                add("error", f"scripts/{path.name} prompts on stdin; an agent cannot answer a TTY.")
            # A module nothing can invoke owes no usage text: it is imported, and the
            # agent reaches it through the script that does have one.
            runnable = re.search(r"sys\.argv|process\.argv|argparse|__main__|\$1|\$\{1", source)
            # Usage is written three ways here: a runner line, a comment naming the
            # script's own filename with its arguments, or an explicit Usage: block.
            invocation = (
                re.search(r"^\s*(#|//)?\s*(python3?|node|bash|sh) \S", source, re.M)
                or re.search(rf"^\s*(#|//)+\s*{re.escape(path.name)}\s+[<\[-]", source, re.M)
            )
            if runnable and not invocation and not re.search(r"--help|argparse|__doc__|[Uu]sage:|USAGE", source):
                add("warn", f"scripts/{path.name} has no usage line; an agent cannot tell what to pass it.")
            if source.startswith("#!") and not os.access(path, os.X_OK):
                add("warn", f"scripts/{path.name} has a shebang but is not executable.")


def check_floor(body, add):
    """The half of references/skill-floor.md a script can see."""
    prose = FENCE_RE.sub("", body)

    match = UNCONDITIONAL_RE.search(prose)
    if match:
        add("warn", f"pointer with no condition ('{match.group(0).strip()}'); say when to open the file.")

    shouts = SHOUT_RE.findall(prose)
    if len(shouts) > 4:
        add("warn", f"{len(shouts)} shouted absolutes; give the reason instead of raising the voice.")

    match = DATED_RE.search(prose)
    if match:
        add("warn", f"a claim stamped with a date ('{match.group(0)}'); it ages into a lie that reads as current.")

    for heading in FILLER_HEADING_RE.findall(prose):
        add("warn", f"'{heading}' is imported-pack filler; keep only what this workspace decided.")

    match = NARRATION_RE.search(prose)
    if match:
        add("warn", f"the body narrates its own edits ('{match.group(0)}'); write the rule, not the diff.")

    head = prose[:600]
    if PERSONA_RE.search(head):
        add("warn", "body opens as a persona ('You are ...'); a persona with no procedure is an agent.")


def review(skill_dir):
    skill_dir = Path(skill_dir).resolve()
    findings = []

    def add(level, message):
        finding = {"level": level, "message": message}
        if finding not in findings:
            findings.append(finding)

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add("error", "No SKILL.md.")
        return {"skill": skill_dir.name, "path": str(skill_dir), "findings": findings}

    text = skill_md.read_text(errors="replace")
    fields, body = parse_frontmatter(text)
    check_frontmatter(fields, skill_dir, add)
    lines, tokens = check_body(body, add)
    # A vendored SKILL.md is the author's prose; shaping it is lost on re-vendor.
    if "SKILL.md" not in vendored_paths(skill_dir):
        check_floor(body, add)
    linked = check_links(body, skill_dir, add)
    check_repo_paths(body, add)
    check_bundled(skill_dir, linked, body, add)

    return {
        "skill": skill_dir.name,
        "path": str(skill_dir),
        "lines": lines,
        "tokens": tokens,
        "description_chars": len((fields or {}).get("description", "")),
        "findings": findings,
    }


def discover(root):
    """Skill directories under root. Follows symlinks: a projected .claude/skills
    is a tree of links, and rglob walks straight past it."""
    root = Path(root)
    if (root / "SKILL.md").exists():
        return [root]
    found = set()
    for dirpath, _dirnames, filenames in os.walk(root, followlinks=True):
        if "SKILL.md" in filenames:
            found.add(Path(dirpath).resolve())
    return sorted(found)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if len(args) != 1:
        print(__doc__.strip())
        return 2

    skills = discover(args[0])
    if not skills:
        print(f"No SKILL.md found under {args[0]}")
        return 2

    results = [review(skill) for skill in skills]
    errors = sum(1 for r in results for f in r["findings"] if f["level"] == "error")
    warns = sum(1 for r in results for f in r["findings"] if f["level"] == "warn")

    if "--json" in flags:
        print(json.dumps({"results": results, "errors": errors, "warnings": warns}, indent=2))
        return 1 if errors else 0

    for result in results:
        if "--quiet" in flags and not result["findings"]:
            continue
        head = f"{result['skill']}  ({result.get('lines', 0)} lines, ~{result.get('tokens', 0)} tokens)"
        print(f"\n{head}")
        if not result["findings"]:
            print("  clean")
        for finding in result["findings"]:
            mark = "ERROR" if finding["level"] == "error" else " warn"
            print(f"  {mark}  {finding['message']}")

    print(f"\n{len(results)} skills, {errors} errors, {warns} warnings")
    print("Judgement (triggering, freedom calibration, placement, provenance): references/review-rubric.md")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
