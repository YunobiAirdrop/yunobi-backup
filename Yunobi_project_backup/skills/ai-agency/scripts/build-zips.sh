#!/usr/bin/env bash
# Regenerates zips/<skill>.zip, one zip per skill folder, and rewrites the
# `skills` array in .claude-plugin/plugin.json.
#
# Skills live one folder per area, `skills/<area>/<skill>/`, and a nested folder
# is not discovered on its own: the plugin manifest has to name every one. A
# hand-kept list of forty is a list that goes stale in silence, which is the exact
# failure this repo exists to make visible, so it is generated here instead.
#
# Claude Code installs skills from this repo as a plugin and never needs the zips.
# Claude Cowork and claude.ai take one file per skill through Settings > Skills >
# Add > Upload a skill, so a non-technical member needs a file they can download
# and upload as-is. The uploader accepts .zip and .skill (both must contain a
# SKILL.md) and a bare .md whose YAML frontmatter carries name and description.
# The zip is flat inside, `<skill>/SKILL.md`, because the area is a fact about
# this repo and not about the skill.
#
# Run this after any change under skills/ and commit the result.

set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

rm -rf zips
mkdir -p zips

paths=()
for dir in skills/*/*/; do
  [[ -f "$dir/SKILL.md" ]] || continue
  name="$(basename "$dir")"
  area="$(basename "$(dirname "$dir")")"
  paths+=("./skills/$area/$name")
  # node_modules and build output belong to the repo, not to the uploaded skill.
  (cd "skills/$area" && zip -qr "../../zips/$name.zip" "$name" \
    -x "$name/*/node_modules/*" "$name/node_modules/*" "$name/*/out/*" \
    "$name/dist/*" "$name/test/*" "*/.DS_Store")
  printf '%-32s %-12s %s\n' "$name.zip" "$area" "$(du -h "zips/$name.zip" | cut -f1)"
done

python3 - "${paths[@]}" <<'PY'
import json, re, sys

paths = sys.argv[1:]

path = ".claude-plugin/plugin.json"
m = json.load(open(path))
m["skills"] = paths
json.dump(m, open(path, "w"), indent=2, ensure_ascii=False)
open(path, "a").write("\n")
print(f"\n{len(paths)} skills declared in {path}")

# index.json is the agent's entry point: one fetch answers "what is here, what
# does each one do, and what URL do I read to run it". An agent with no terminal
# cannot list a directory tree over HTTP, and guessing raw URLs from a README
# table is where a run goes wrong, so the URLs are written out rather than
# implied.
RAW = "https://raw.githubusercontent.com/heyramzi/ai-agency/main"
TREE = "https://github.com/heyramzi/ai-agency/tree/main"

def frontmatter(file):
    text = open(file, encoding="utf-8").read()
    if not text.startswith("---"):
        return {}
    block = text.split("---", 2)[1]
    out, key = {}, None
    for line in block.splitlines():
        hit = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", line)
        if hit:
            key, value = hit.group(1), hit.group(2).strip()
            out[key] = value.strip('"').strip("'")
        elif key and line.startswith(" "):
            out[key] = (out[key] + " " + line.strip()).strip()
    return out

skills = []
for rel in paths:
    rel = rel.lstrip("./")
    area, name = rel.split("/")[1], rel.split("/")[2]
    fm = frontmatter(f"{rel}/SKILL.md")
    skills.append({
        "name": fm.get("name", name),
        "area": area,
        "description": fm.get("description", ""),
        "skill_md": f"{RAW}/{rel}/SKILL.md",
        "folder": f"{TREE}/{rel}",
        "zip": f"{RAW}/zips/{name}.zip",
    })

commands = sorted(f[:-3] for f in __import__("os").listdir("commands") if f.endswith(".md"))
index = {
    "repository": "https://github.com/heyramzi/ai-agency",
    "marketplace": "heyramzi/ai-agency",
    "install": ["/plugin marketplace add heyramzi/ai-agency", "/plugin install ai-agency@ai-agency"],
    "read_this_first": f"{RAW}/AGENTS.md",
    # Where the skills came from. An agent asked "what is this" over HTTP gets the
    # repo; the room is the half that explains why any of it is shaped this way.
    # Always the tracked short link, never the raw skool.com URL: only the short
    # one records the click.
    "courses": "https://go.upsys-consulting.com/skool",
    "commands": [{"name": c, "markdown": f"{RAW}/commands/{c}.md"} for c in commands],
    "agents": [{"name": "project-manager", "markdown": f"{RAW}/agents/delivery/project-manager.md"}],
    "skills": skills,
}
json.dump(index, open("index.json", "w"), indent=2, ensure_ascii=False)
open("index.json", "a").write("\n")
print(f"{len(skills)} skills and {len(commands)} commands written to index.json")
PY
