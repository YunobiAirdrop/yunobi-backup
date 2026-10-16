---
name: ai-manager
description: "Manages every skill and agent: writes, repairs, reviews and cleans them, critiques the shelf for bad names and overlap, and gates broken agent-to-skill links. Use when writing or editing a skill or agent, when one fires wrong, before it ships, or when the shelf feels messy."
author: "Anthropic"
license: Complete terms in LICENSE.txt
argument-hint: "[critique · audit · new|agent · trigger|improve · heal|log · clean · review|package] [target]"
tags: [makes, agents]
lane: judgment
---

# AI Manager

Every skill, every agent and every link between them is written, repaired and cut back through
this file. It replaced `skill-manager` on 30 Sep 2026, after 12 of 22 agents were found naming
skills they could never load, and took its name, `ai-manager`, on 4 Oct. A skill is a slot every session pays for before the user asks
anything, so the bar is "does this earn its place against everything already here".

## The architecture, and the gate that holds it

A skill is found by its description. Every session sees all of them, and there's no router agent.

An agent inherits no skills. Its `skills:` line is the only way one reaches it, preloaded whole.
Every agent declares at least one, and every skill its body names in backticks is on that line.
An agent with nothing to declare is a persona: give it a skill or delete it.

The `audit` command parses every frontmatter block with a real YAML parser and fails an agent
whose `skills:` names a missing skill or skips one its body names. Run it in a pre-commit hook.

Four principles carry the rest: **extraction, not design** (a skill or a learning comes from work
already done twice or a failure that cost real time, never a planning session); **enforcement, not
description** (a skill that sets a bar ships the eval that holds it, not prose describing one);
**the floor is shared** ([references/skill-floor.md](references/skill-floor.md) holds the quality
bar for every path here, so a standard is never restated); and **verified by outcome in a cleared
session**, never by reading the file back.

## The three paths

**Write** when nothing covers the request. **Repair** when something does and it is wrong, stale,
or silent about what it just cost you. **Clean** when the shelf itself is the problem: overlap,
duplicate names, a registry over budget, a body that has doubled. Repair is the common one, and
reaching for a new file when an existing one was wrong is how a registry doubles without getting
better.

| Command | Path | Does | Reference |
|---|---|---|---|
| `critique` | Judge | Hold every skill and agent to the philosophy, one verdict each, then execute them | [critique.md](references/critique.md) |
| `audit` | Judge | Run the gate, fix every failure at its source, re-run until it passes | above |
| `new [name]` | Write | A skill out of a run already done twice | [creation-process.md](references/creation-process.md) |
| `agent [name]` | Write | An agent, or the finding that it should be a skill | [creation-process.md](references/creation-process.md), Writing an agent |
| `heal [target]` | Repair | The five-step loop below, on the file that should have known | [healing.md](references/healing.md) |
| `log [skill]` | Repair | Append one dated failure mode to a skill's own log | below |
| `trigger [skill]` | Repair | A description that fires on the wrong prompts or not at all | [skill-floor.md](references/skill-floor.md), Triggering |
| `improve [skill]` | Repair | Run it, judge the output, correct the file, retest cleared | [review-rubric.md](references/review-rubric.md), Improving by outcome |
| `clean [folder]` | Clean | Measure the registry and the session context (MCP, connectors, plugins), merge, delete, simplify what stays | [cleaning.md](references/cleaning.md) |
| `review [target]` | Judge | The mechanical script, then the eight-dimension rubric | [review-rubric.md](references/review-rubric.md) |
| `package [skill]` | Ship | Validate and zip for distribution outside this workspace | `scripts/package_skill.py` |

`cleaning.md` opens [context-budget.md](references/context-budget.md) for the descriptions pass
and [memory-triage.md](references/memory-triage.md) for an auto-memory store; merges follow
[critique.md](references/critique.md).

With no argument, pick from the conversation: a correction is `heal`, something missing is `new`,
bad names or overlap is `critique`, size is `clean`, a broken agent-to-skill link is `audit`.
Heal continuously; critique and clean as a pass over the whole tree, never a reflex.

## Setup, before writing anything

1. **Search first.** Read [references/contract.md](references/contract.md), then grep skill and
   agent descriptions for the topic (a 70% match means strengthen that instead of writing new),
   and `scripts/` too, since a shipped capability reads as a missing skill.
2. **Load the one reference that owns the request** from the table above, and nothing else.
3. **Load [references/skill-floor.md](references/skill-floor.md) right before writing a body**,
   for the quality bar and the reflexes no script catches.

## Writing a file

Procedure, Judgment, Interface or Context: the kind names what the reader of the finished file is
doing when they open it, and decides what the body contains. Definitions, how each fails, and
picking by reader rather than topic:
[references/creation-process.md](references/creation-process.md).

A skill is also the third-best fix. Work down the ladder in
[references/contract.md](references/contract.md) (architecture, a lint or CI gate, then a skill
or rule) and name in one line why levels 1 and 2 cannot hold it.

Start with the reusable parts (`scripts/`, `references/`, `assets/`): they decide what the body
has to say, and a body written first ends up describing work the reference already carries. A
Judgment skill writes its eval before the body. Initialise with
`scripts/init_skill.py <name> --path <dir>`, delete unused example files, and write the body last,
as a router, in the directory that names the slash command. Placement and naming:
[references/contract.md](references/contract.md).

## Repairing a file

Five steps, in order. Step 2 is the one that gets skipped, and skipping it is what turns
instruction files into archives nobody trusts.

1. **Find the owning file.** Grep for where the fact already lives before writing it anywhere; if
   nowhere, [references/healing.md](references/healing.md) names which file should own it. Follow
   symlinks to their source, since a projection is a copy the next sync overwrites.
2. **Delete what the learning contradicts.** A wrong sentence left standing outranks a right one
   appended after it: instructions are read top to bottom and trusted equally.
3. **Write the smallest edit that prevents a repeat**, patched into an existing file. "Check dates
   carefully" teaches nothing; "Buffer accepts a 600-character tweet and lets it die at send"
   prevents a repeat.
4. **Read it back**: frontmatter parses, links resolve, and nothing else contradicts the edit,
   including any gate the skill ships (the Coherence check in [skill-floor.md](references/skill-floor.md)).
5. **Retest in a cleared session.** Reading the edit back proves the file says the right thing, not
   that it *changes what happens*, since this session already knows the lesson and complies
   regardless. Loop and stop rule: [review-rubric.md](references/review-rubric.md), Improving by
   outcome.

**What counts as a learning:** a correction from the user, a stale instruction, an approach that
beat the documented one, or a failure that cost real time, not a one-off. An edit leaves the file
no longer than it found it, and over the ceiling you restructure rather than shave the new fact.
What not to heal, and worked entries: [references/healing.md](references/healing.md).

## Cleaning a registry

Measure first, decided by the script rather than by eye:

```bash
python3 scripts/context_cost.py <folder>    # counts, metadata cost, every violation
python3 scripts/dead_pointers.py <folder>   # routes into assets that no longer exist
```

Then a descriptions pass widest first, an agent triage, a merge of every overlapping pair, and a
simplification pass on the bodies that stay. Every run ends with the registry smaller or equal,
metadata reported before and after. Budgets, the five waste classes, memory stores, the checklist:
[references/cleaning.md](references/cleaning.md).

## The failure log, and how to run it

Every skill keeps an append-only log about itself. A skill that repeats a mistake is a bug, and
the log fixes it because the next run reads it as instructions.

Four parts, all required: the stated promise in the body, the closing step of the flow, a
verification item, and `## Learned Patterns` last in the file, seeded with real entries.
`heal.cjs retrofit` adds what is missing. Entry format, the 240-character law, the `[ask:` field
and why each exists: [references/healing.md](references/healing.md). Node 20+ and Python 3,
nothing installed:

```bash
node scripts/heal.cjs check [paths...]         # which skills carry the scaffold
node scripts/heal.cjs retrofit <skill> --apply # add the missing parts to one
node scripts/heal.cjs log <skill> "<entry>" --apply
node scripts/heal.cjs fold <skill>             # entries that belong in the body now
```

`retrofit` and `log` are dry runs without `--apply`, and `log` refuses an entry it already holds.
`check` exits 1 on a missing scaffold; the ask and length findings are only warnings.

## Before it ships

Two passes, in order, and the first is free. **Mechanical:** `review_skill.py` checks frontmatter
against the published ceilings, name against directory, description length and person, body size,
dead links, unreachable references and scripts an agent cannot drive; exits 1 on any error, whole
tree, `--json`/`--quiet`. **Judgment:** [references/review-rubric.md](references/review-rubric.md)
scores the eight dimensions a script cannot; read it when a skill is about to ship, keeps getting
picked for the wrong prompt, or its output changes between sessions.

Neither replaces the cleared-session retest: one cold Sonnet session on the rewritten `humanizer`
broke it on four points that a reread had passed.


## Closing a run

If this run surfaced a failure mode not already listed, log it against this skill before
finishing: `node scripts/heal.cjs log . "what was assumed, what to do instead" --apply`. A
learning that stays in the conversation is lost when the conversation ends.

## Verification

- [ ] Nothing existing covered 70% of it, and the search that established that was run
- [ ] For a repair: what the learning contradicts was deleted, not left below the new text
- [ ] For a clean: the metadata figure went down, and `dead_pointers.py` reports none
- [ ] The floor was loaded before the body was written, and every check answers
- [ ] A skill that sets a standard ships the eval that holds it, not prose describing one
- [ ] `review_skill.py` reports no errors
- [ ] Retested in a cleared session, rather than read back
- [ ] `audit` passes, and the sync ran after it
- [ ] New failure modes from this run appended to Learned Patterns

## Learned Patterns

What runs of this skill have taught it, newest first:
[references/learned-patterns.md](references/learned-patterns.md).

---

*Originates in Anthropic's skill-creator, Apache License 2.0.*
