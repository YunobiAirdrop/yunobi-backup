# Memory Store Triage

The auto-memory store at `~/.claude/projects/<repo-slug>/memory/` is a registry like any
other, written by sessions that never come back to read what they wrote. It decays in a way
skills do not: nothing prunes it, nothing verifies it, and the facts it holds were true on the
day they were written and never since.

`MEMORY.md` is the only part loaded into every session in that repo. The bodies cost nothing
until recalled. So the index is what you cut first, and the bodies are what you correct.

## Contents

- [The five outcomes](#the-five-outcomes)
- [Deciding which outcome applies](#deciding-which-outcome-applies)
- [Index rules](#index-rules)
- [Link repair](#link-repair)
- [Archiving, never deleting](#archiving-never-deleting)

## The five outcomes

Every memory file ends a pass in exactly one of these states.

| Outcome | Means | The file after |
| --- | --- | --- |
| **Keep** | One fact, still true, no other file owns it | Unchanged, or trimmed |
| **Fold** | A skill, rule or CLAUDE.md already owns the content | Deleted; the owning file gains what it was missing |
| **Promote** | It is a procedure or a durable agreement, not a fact | Becomes a skill, a rule, or a CLAUDE.md line; memory deleted |
| **Merge** | Two or three files circle one subject | One survivor holding the union; the rest archived |
| **Archive** | Resolved incident, shipped project, fact no longer true | Moved out of the store |

Promote and fold both end in deletion. That is the point: a memory is a holding pen for a fact
that has no home yet. Once it has one, the memory is a second copy, and a second copy is the
thing the SSOT rule exists to prevent.

## Deciding which outcome applies

Run these in order and stop at the first that fires.

0. **Has any session ever opened it?** `memory_cost.py <slug> --usage` lists the files no
   transcript has read. A memory nobody opens is not holding a fact for you, it is paying
   index rent, and it is the cheapest thing in the store to archive. Work that list first;
   the questions below only decide what happens to the ones that do get read.
1. **Is it still true?** Open what it names: the file path, the flag, the object ID, the URL,
   the port. Gone or changed means archive, or correct it and keep. Never carry a memory
   forward on the strength of its own confidence.
2. **Does another file already own it?** Grep the registry for the subject. A body that says
   "the full X now lives in the `y` skill" has already answered this: fold it. Anything the
   memory holds that the skill does not gets moved into the skill first.
3. **Is it a procedure?** Three or more ordered steps, a command sequence, a checklist. That is
   a skill wearing a memory's clothes. Promote it.
4. **Is it a standing agreement about how to work?** A `feedback` memory that has held for
   months belongs in the repo's CLAUDE.md or in a rule, where it binds every session rather
   than waiting to be recalled.
5. **Is it a resolved incident?** A description reading RESOLVED, FIXED or DONE describes
   something that already happened. Keep the transferable lesson as one short `feedback`
   memory if there is one, archive the narrative.
6. **Is it one fact?** Past 250 words it is a report. Cut to the fact, the why, and the how to
   apply. The evidence belongs in the repo, not in memory.
7. **Otherwise keep.**

`project` memories are the fastest-decaying type and usually the largest share of a store.
Weight the pass toward them.

## Index rules

- Every file has exactly one `MEMORY.md` line. A file with no line is never recalled, so it is
  either indexed or archived, never left.
- One line per fact, in the form `- [Title](file.md) — hook`. The hook is what makes recall
  fire; it is not a summary.
- Past about 60 lines the index is itself a context cost worth cutting. Group related memories
  onto one line (`- [a](a.md), [b](b.md) — shared hook`) rather than dropping facts.
- An index line pointing at a missing file is a hard violation. Fix or remove it.

## Link repair

`[[name]]` links between memories break silently and accumulate. Two causes account for nearly
all of them:

- **A naming convention that changed.** `[[project-foo]]` against a file named
  `project_foo.md`. Pick the convention the files on disk use, then repoint every link.
- **A `.md` suffix in the link.** `[[project_foo.md]]` resolves to nothing; the target is the
  `name:` slug, never the filename.

Repair after the archive and fold steps, not before, or you repoint links into files you are
about to remove. Links to a memory that no longer exists are removed with the sentence that
carried them, not left as bare text.

## Archiving, never deleting

`~/.claude/` is not a git repository, so a deleted memory has no recovery path. Archive
instead:

```bash
ARCHIVE=~/.claude/memory-archive/$(date +%F)/<repo-slug>
mkdir -p "$ARCHIVE" && mv <file>.md "$ARCHIVE/"
```

Report the archive path in the summary. Sweep archives older than a quarter only when the user
asks.
