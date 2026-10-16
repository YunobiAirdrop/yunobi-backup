# Cleaning a registry

Load this for the clean path: a cluttered folder, a runtime picking the wrong asset, a markdown
file past 200 lines, a log past 25 entries, a fresh import, or a quarter with no pass.

**The unit of waste is context, not files.** 250 assets at 400 chars each spend about 25k tokens
before the user asks anything; every run ends with the registry smaller or equal.

**A registry grows in two directions and only one shows in an asset count**: wider, which merging
and deleting fix, and deeper (a failure log nothing prunes, a copied paragraph, a table restating
the filesystem, prose the model knows), so nothing is added and the read cost still doubles. One
registry held 689 KB of failure logs against 1.4 MB of bodies, 59% log in its largest skill. Both
passes run every time; the second is [Simplification](#simplification-pass).

## Contents

[Session context](#session-context), [Target folders](#target-folders), [Budgets](#budgets),
[Execution flow](#execution-flow), [Simplification pass](#simplification-pass), [Memory stores](#memory-stores),
[Skill merging](#skill-merging), [Agent triage](#agent-triage), [Common issues](#common-issues),
[Verification](#verification).

## Session context

When the complaint is a full context window, measure the session before the registry: MCP
servers, claude.ai connectors, Claude in Chrome, plugins, projected agents and duplicated
instruction files outweigh every skill description. Method and levers:
[context-budget.md](context-budget.md#mcp-servers-connectors-and-the-rest-of-the-session).

## Target folders

| Folder      | Layout                     | Notes                                     |
| ----------- | -------------------------- | ----------------------------------------- |
| `.claude/`  | Flat                       | Runtime registry, projection of source    |
| `ai-doc/`   | Packaged (skills + agents) | Source of truth, projects into `.claude/` |
| `<plugin>/` | Plugin layout              | Has `.claude-plugin/plugin.json`          |
| `~/.claude/projects/*/memory/` | Flat `*.md` + `MEMORY.md` | Auto-memory store. See [Memory stores](#memory-stores) |

Auto-detect: `skills/<area>/<family>/<name>/SKILL.md` is the kit's own layout; anything shallower
is a stray to file into a family. Follow every symlink to its source, since a projection is a copy
the next sync overwrites. Naming and the agent-filename rule: [contract.md](contract.md).


## Budgets

Over budget makes the matching pass mandatory, not optional. A corpus is not a reference: a file
of measured evidence a skill reads from, such as a transcript set, keeps its size and trips the
warning; say so in the pointer.

| Scope | Budget | Over budget action |
| --- | --- | --- |
| `description` per asset | 500 chars (1024 hard cap) | Cut to what plus when. See [context-budget.md](context-budget.md) |
| Registry metadata total | About 100 tokens per asset, so 400 chars average | Descriptions pass, widest first |
| Any `.md` in a skill, or an agent body | 200 lines (gated) | Merge, cut what the model knows, split by reader |
| Markdown files per skill | 10 (gated) | Past that the body routes to nothing and the reader opens none. Merge or delete |
| Agents per category folder | 8 | Merge or delete down to budget |
| Agents total (`ai-doc/`) | 60 | Run the agent triage below |
| Skills per package | 12 | Merge near-duplicates, or sub-package |
| Learned Patterns log | 0 entries in the body, 25 in `references/` | See [Simplification](#simplification-pass), class 1 |
| A block repeated across sibling files | 3 copies | See [Simplification](#simplification-pass), class 2 |
| CLAUDE.md | ~500 lines | Extract reference material to skills |
| `MEMORY.md` index | 60 lines | Group related memories onto one line, archive the dead |
| Any one memory file | 250 words | Cut to the fact, the why, the how to apply |

## Execution flow

1. **Measure.** `python3 scripts/context_cost.py <folder>` prints asset counts, total
   always-loaded metadata, the widest descriptions, the longest bodies, and every violation.
   Every later step works from this list, not from reading files by eye.
2. **Fix hard violations**: missing frontmatter, duplicate registered names, broken links,
   illegal names. Then `python3 scripts/dead_pointers.py <folder>`, which resolves pointers
   prose makes by name ("belongs to `x`"); nothing else checks those, so a deleted asset leaves
   every route to it intact and silent.
3. **Descriptions pass, widest first**, the only edit that pays back in every session. Recipe in
   [context-budget.md](context-budget.md).
4. **Triage agents** per the rules below, and merge overlapping skills per
   [Skill merging](#skill-merging); commands are triaged the same way as skills.
5. **Simplification pass**, on every skill the measurement named, whether or not anything
   merged: the half that keeps a registry from growing while the asset count holds still.
6. **Bodies pass.** For each file still over 200 lines, delete what the base model already
   knows, then move whole sections out with `python3 scripts/split_section.py <SKILL.md>
   --sections "<heading>" --into references/<name>.md --title "<H1>" --pointer "<one line>"`.
   Judge the pass in bytes: a split or joined lines pass the gate and cut nothing (16 Sep 2026).
7. **Relocate**: docs that should be rules, hooks outside `settings.json`, agent files whose
   name has drifted from their `name:`.
8. **Propose one plan** as a table (file, action, chars or lines saved, reason), grouped so the
   user can approve per group or all at once, then **execute** with `git mv` and `git rm`.
9. Re-run the script, verify against the checklist, and report the metadata figure before and
   after.

## Simplification pass

Merging asks whether a skill should exist; this asks what is inside the ones that should, and
it's the pass that gets skipped because nothing about a bloated skill looks broken. The standard
being restored is [skill-floor.md](skill-floor.md): read it before rewriting a body, and run
`review_skill.py` over the target tree first, so this pass spends its attention on what a script
cannot see.

Five classes, in the order they pay back, all measured by `context_cost.py`:

1. **A failure log that has become a second body.** Never in `SKILL.md` (a body is read in full
   on every invocation, a log almost never): move with `split_section.py`. Past 25 entries,
   compress each to its rule with `python3 scripts/compress_log.py <skill-dir> --dry` (drop
   `--dry` to apply), after committing: the run goes, git keeps it. Fifteen second-log files once
   reached 5,296 lines holding 67 rules never folded anywhere.
2. **A block copied into its siblings.** Consolidate only into a file every reader already loads:
   27 transition references restated the same two notes (12 KB) while `SKILL.md` said both and
   is read first, so deleting all 54 copies cost nothing. The same shape across 12 `<area>-lead`
   agents is not the same finding, since an agent has no parent to hop to.
3. **A hand-maintained table restating what is on disk**: a skill list in a lead agent, a
   Contents list above a log. It goes stale silently (one drifted five entries behind). Generate
   it or delete it, never repair by hand.
4. **Prose the base model already knows**: imported-pack filler like "Initial Assessment", "Best
   Practices", "Common Mistakes". Keep only what this workspace decided.
5. **An entry that says the rule now lives above.** Delete the line rather than keep it as a
   signpost; same for a memory pointing at the skill that owns its fact.

The test that covers all five: would a session behave differently without this line? If not, it
is sediment.

## Memory stores

An auto-memory store is a registry nothing prunes: sessions write to it and never read back what
they wrote. Only `MEMORY.md` loads every session, so the index is what you cut and the bodies are
what you correct.

1. **Measure.** `python3 scripts/memory_cost.py [slug] [--usage]` profiles every store: index cost
   per session, four buckets (`archive`, `fold`, `trim`, `orphan`), and with `--usage` which files
   no session has ever opened, the cheapest thing to archive. Work that list first.
2. **Triage each flagged file** through the outcomes in [memory-triage.md](memory-triage.md), then
   **move the content before removing the file**: anything the memory holds that its owning skill,
   rule or CLAUDE.md does not gets written there first, the whole value of the pass.
3. **Repair links, then rebuild the index**, in that order (repairing first repoints into files
   about to be removed): [memory-triage.md](memory-triage.md).

## Skill merging

Two skills that read alike are one skill written twice, and merging is the default outcome for an
overlapping pair, not the last resort. Group candidates by topic across **all** packages, not
folder by folder, since topic trios accumulate across categories. Description overlap under 40% is
complementary, 40 to 70% is adjacent (merge unless a written reason survives), over 70% is
redundant, but read both bodies first: two skills can read 70% identical and take different
inputs, which is a disambiguation job, not a merge. Full method, and everything a deleted
directory breaks: [critique.md](critique.md#doing-the-merge).

## Agent triage

Agents are the most over-accumulated asset type. **Measure before scoring**, since the registry's
own usage is on disk (`grep -ho '"subagent_type": *"[^"]*"' ~/.claude/projects/*/*.jsonl | sort |
uniq -c | sort -rn`); counting name mentions instead is worthless, since the agent listing sits in
every session's system prompt and every agent scores in the hundreds. Then score each one:

1. **Distinct persona?** Near-identical system prompts (same domain, same deliverables) merge
   under the broader name, keeping the union of non-overlapping instructions.
2. **Cross-category duplicate?** Same registered `name:` or near-identical description in two
   categories: keep the canonical copy, delete the other. Compare basenames, not only registered
   names. Platform-sharded agents (one per social network) are one strategist with per-platform
   sections.
3. **Persona or just a skill?** A body that is a procedure (steps, checklists, no judgment or
   voice) is a skill wearing a costume: convert or fold in, delete the agent. The reverse also
   happens: a skill whose body is persona text duplicates the same-named agent, and there the
   agent owns the persona.
4. **Generic-model shadow?** An agent that adds nothing beyond what the base model does when
   asked directly is dead weight: would the same prompt to the base model produce the same
   output?
5. **Dormant?** No invocation you can find evidence for (`git log --follow` per file: created
   once, never touched). Flag as a prune candidate, delete on confirmation. An imported pack also
   carries agents for stacks and markets this workspace never touches; check each before keeping.

## Common issues

| Symptom | Fix |
| --- | --- |
| A log that reads as empty and is not | The counter matches one date format. Count `- 26 Aug 2026` and `## 2026-08-26` too |

## Verification

- [ ] `context_cost.py` reports zero hard violations (frontmatter, duplicate names)
- [ ] In `ai-doc/`, every agent filename equals its `name:`; references one level deep, a contents list past 100 lines
- [ ] `dead_pointers.py` reports none, and every deletion this run made was swept for routes into it
- [ ] Metadata total reported before and after, and it went down
- [ ] Every count at or under budget, or an approved exception noted in the report
- [ ] Hooks in `settings.json`; every other document under the skill that owns it, or in `ai-doc/references/` when several do. There is no `rules/`
- [ ] No banned words, no em-dashes (see `packages/lint/data/slop-words.js`)
- [ ] Every rewritten body answers the Verify list in [skill-floor.md](skill-floor.md), and `review_skill.py` reports no new findings against it
- [ ] No `SKILL.md` carries log entries in its body, and no log in `references/` is past 25 entries
- [ ] Every compressed log was committed first, and no `learned-patterns-archive.md` survives
- [ ] `duplicated blocks` in the report went down, or each survivor has a reader with no parent to hop to
- [ ] Registry smaller or equal to where the run started
- [ ] Consumers re-synced (`pnpm vibekit sync <dir>`) and no broken symlinks, pruning `*/worktrees/*`
- [ ] For memory stores: every file indexed once, no dead `[[link]]`, nothing deleted outside the archive, and each folded fact verified present in the file that now owns it
