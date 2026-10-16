# Healing detail

## Contents

- Deciding which file owns a fact
- Retrofitting a registry
- What not to heal
- Worked examples
- Healing is not accretion
- The failure log scaffold
- Cadence

Loaded when a learning does not have an obvious home, or when retrofitting a
registry that was never written to heal.

## Deciding which file owns a fact

Specificity wins. The home is the narrowest file whose job already covers the
fact, because that is the file a reader consults when the fact matters.

| The learning is about | Home |
| --- | --- |
| How one task is performed | The skill that performs it |
| A constraint every skill in a domain hits | A rule scoped to that domain |
| The shape of the repo, its commands, its conventions | `CLAUDE.md` / `AGENTS.md` |
| An external system's behaviour | The skill that talks to that system |
| A one-off about this conversation | Nowhere. Let it go. |

Two failure modes when placing a fact:

**Writing it too high.** A detail about one API's pagination in a root
`CLAUDE.md` is read by every session that touches the repo and matters to almost
none of them. Cost is paid on every load, value is collected once.

**Writing it in two places.** The same fact in two files will drift, and the
reader cannot tell which copy is current. Second mentions become pointers to the
home, not restatements.

A file that intentionally reflects another opens by saying so and naming its
source. Update the source first, then the mirror.

## Retrofitting a registry

Opportunistic beats systematic. Adding the scaffold to 60 skills in one pass
produces 60 empty logs, and an empty log is worse than none: it looks like the
skill has nothing to teach when the truth is nobody has written it down.

The order that works:

1. `check --quiet` to see what is missing across the registry.
2. Retrofit the skills you actually use, when you next use them, seeding each
   log with the failure that made you open the file.
3. Leave the rest. A skill nobody runs has no failure modes to record, and it is
   the clean pass's problem rather than this one's.

The exception is a skill that has just cost you time. Retrofit that one now,
while you still remember precisely what it got wrong.

## What not to heal

**A failure that was the model's, not the file's.** If the instruction was
correct and clear and the run went wrong anyway, adding a caveat to the file
makes it longer without making the next run better. Not every failure has a
documentation fix.

**A preference stated once.** Wait for the second time. A rule written from a
single data point is usually a rule about that data point.

**Anything the code already says.** If a reader can learn it by reading the
source, the file restating it is one more thing to keep in sync. Document the
things the code cannot tell you: why this way, what was tried and abandoned,
which external system lies about its own behaviour.

## Worked examples

Weak, and why:

> - 2026-03-02: Be careful with the API rate limits.

Names no limit, no symptom, no action. The next session reads it, agrees, and
learns nothing it did not already assume.

> - 2026-03-02: Fixed a bug in the upload path.

Records that work happened. A changelog entry wearing a lesson's clothes.

Strong, and why:

> - 2026-03-02: The export endpoint returns 200 with an empty body while the job
>   is still running, so a naive read stores an empty file and reports success.
>   Poll `status` until it reads `complete` before reading the body.

Names the symptom, the false signal, and the action. A session that reads it
cannot make the mistake.

> - 2026-03-02: Assumed the folder-scoped delete would find a note created in
>   that same folder seconds earlier. It fails with -1728. Delete by full note id
>   rather than by walking a folder.

Records the assumption, not just the fix, so a reader recognises the situation
before repeating it.

## Healing is not accretion

- An edit should leave the file no longer than it found it, unless the learning is a really new
  case.
- A learning that repeats across three or more files becomes one rule, and the three copies become
  pointers to it.
- An entry that has hardened into how the body describes the work gets folded into the body and
  deleted from the log. `fold` lists the candidates; it does not rewrite prose, because which
  sentence absorbs the lesson is a judgment about the work.
- Past 25 entries a log still living in the `SKILL.md` has become a second body. That is the signal
  to fold, not to raise the number. Once it has moved to `references/`, the character count is the
  measure and not the entry count: 130 one-line rules are cheaper to read than 25 paragraphs.
- **There is no `learned-patterns-archive.md`.** A second log beside the first is a body nobody
  opens: fifteen of them reached 5,296 lines, and 67 rules inside them had never been folded into
  any log at all. `review_skill.py` errors on one.

The short form is in `SKILL.md`.

## The failure log scaffold

Moved out of the body 11 Sep 2026; `SKILL.md` states the four parts and points here.

1. **A stated promise** in the body that the skill appends new failure modes after each run. Not in
   the description: every description is preloaded into every session, and this sentence tells the
   runtime nothing about when to pick the skill.
2. **The closing step of the flow** reads: if this run surfaced a failure mode not already listed,
   append it to Learned Patterns with today's date.
3. **A verification item** confirming new patterns were appended.
4. **`## Learned Patterns`** last in the file, seeded with real entries. Never ship it empty; an
   empty log teaches the reader to skip the section. Past a handful it moves to
   `references/learned-patterns.md`, because a body is read in full on every invocation and a log
   is read on almost none.

Entry format, newest first:

```
- YYYY-MM-DD: <what went wrong or was assumed> <what to do instead>. [ask: <the ask that caused it>]
```

**One line, 240 characters, opening with the law.** A log is paid for in context on every run, so
the entry carries the rule and one checkable anchor (the error string, the threshold, the flag) and
nothing else. The story belongs in git. `heal.cjs log` refuses a longer entry; `--long` overrides.

**Keep the ask when a prompt caused the failure**, and `check` counts them, because this field died
once already: on 5 Sep 2026 it was absent from all 758 entries in all 34 logs, written as optional
and enforced by nothing. The wording that broke the skill is the only input that proves the edit
worked, so a log of 5 or more entries with no ask now warns. Ship the scaffold only when the run
that motivated the skill already produced real failures to seed it with.

## Cadence

Healing is per-session and reactive: it fires when something is learned.
Cleaning is scheduled and subtractive: it fires on a calendar.

Running them on the same cadence collapses the difference and produces a weekly
pass that both adds and removes, where the two halves fight. Heal continuously,
clean on a schedule, and let the clean pass fold the hardened entries the heal
passes accumulated.

## Over the ceiling: restructure, do not shave

The body rule is in `SKILL.md`. This is what to look for and what it is worth.

The author, 14 Sep 2026, watching a session shave sentences off `skool` to fit a new command under the
250-line cap: *"instead of trimming things just to refactor so that you just keep the essence and
key value"*, and *"sometimes it's better to rework than to cut off, because you might lose value and
in what you keep there might be fluff"*. Shaving is the reflex because the new text is the only part
the session feels it owns. It is also the part that was just proven to matter, so it is the wrong
thing to pay with.

Read the whole body before cutting a word of it, and look for three shapes. All three were in
`skool` and none had been noticed in a month of edits.

- **The same claim, twice.** It said "reading the room is a CLI job, not a browser job", then said
  it again three lines later in different words. Two sentences, one fact, and the duplicate had
  survived because each edit only read its own paragraph.
- **Several paragraphs on one subject, each closing with its own pointer to the same reference.**
  Five of them on pushing a course, each ending "see classroom.md". They became one section with the
  rules kept and one pointer, and the section reads better because the three rules that can destroy
  something now sit together instead of being spread across four screens.
- **A rule whose evidence has outgrown it.** The incident belongs in the reference; only the rule
  belongs in the body. A body paragraph that spends four lines on what happened and one on what to
  do has its ratio backwards.

That pass added a command, a script and a corrected fact, and the file came out 17 lines shorter.
A restructure that does not end shorter than it started has not found the fluff yet.

## Why writing, healing, reorganising and cleaning are one skill

Three separate skills until 11 Sep 2026. All three wrote against the same floor, each opened by
routing to another, and the cleaner's closing step was a command that lived in the creator. Both
merges were the author's call: 5 Sep 2026, *"merge skill healer and skill creator into one. This is the
easiest and most DRY solution."* Then 11 Sep 2026, *"the skill manager should take care of skill
cleaning as well, so that we are more DRY and we don't have another skill cleaner."* Reorganising
joined them on 14 Sep 2026, as the rule above: *"the skill manager should take care of reorganizing,
not just adding or trimming."*
