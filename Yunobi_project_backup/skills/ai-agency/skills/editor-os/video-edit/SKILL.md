---
name: video-edit
description: "Runs a take from card to composition. In Descript: DJI lav sync, project setup, pre-cut coaching, the script cut, long-form or the tighter 5-pass Short. Use when a reel used a lav, footage needs to land in Descript, a take needs coaching before cutting, or a raw take or Short needs cutting."
tags: [drives, descript, video]
lane: general
---

# Video Edit

The path from a recorded take to a rendered Descript composition runs in nine passes, 0 to 8,
each timed against the one before it. Work out of order and you build motion for a frame that is about to
move, or lay a bed before the cut ends in its final place.

## Before any of the nine

**Everything Descript goes through `pnpm descript`.** The browser, the published API and
Underlord write outside the CLI's commit gate and get reverted or corrupted.
The API once broke an edit that had to be re-uploaded by hand, and Underlord once littered a
project with test sequences.
Where no verb exists, write the verb in `CLIs/descript/` instead of reaching past
it.

**A production gets a ledger before the first pass.** `scripts/run.py` writes `RUN.md`/`RUN.json`
beside the video's `plan.md` and mirrors the same rows to its ClickUp task as a checklist.
`next` names the one pass to do now and what proves it; `start` refuses a pass whose predecessor
is neither done nor blocked; `done` needs the pass's proof command named in `--evidence` and
either `--file` (its saved output) or `--run` (run.py runs it and keeps the output in `proof/`).

```bash
R=.claude/skills/video-edit/scripts/run.py; D=tools/motion/src/<video-code>
python3 $R init $D --code EC51 --project <id> --comp <id>
python3 $R board $D --task <ClickUp task id>
python3 $R next $D
python3 $R done $D <n> --evidence "<what the command's output said>" --file <its saved output>   # or --run "<command>"
```

**A name always carries its number and timecode**: `N [MM-SS] Description.ext`. Any `[mm-ss]`
quoted anywhere downstream comes from `layout cards`, never from the raw take. A cut has already
moved every second. Full naming rules: [references/naming.md](references/naming.md).

**Never publish or export on your own.**
The editor always does a human pass before anything is exported.
 The state gets read back from outside the tool
that wrote it at the end of every one: a tool reporting success is not evidence. The project
stays his, for him to watch.

Sibling skills, not covered here: `social`'s `references/shorts-production.md` (encoding, Drive, ClickUp, calendar),
`video-script` (writing the script), `social` (captions), `broll`
(finding a shot that exists), `motion-design` (building a clip).

## The order the passes run in

Long-form is 9 passes, timed against each other. `schemas/passes.json`, which `run.py` reads, is
the one home of the order; this table says what owns each one and where its detail lives.

| # | Pass | Owner | Done when |
|---|---|---|---|
| pre | feeds pass 0 | [dji-sync.md](references/dji-sync.md) runs before any footage lands, when a reel used a DJI lav | card burned, verified, archived |
| 0 | organise | [descript-projects.md](references/descript-projects.md) | `descript tracks` prints clean |
| 1 | coach, then cut | [video-coach.md](references/video-coach.md) runs first, then [descript-script-edit.md](references/descript-script-edit.md) | script reads with no retake or false start left standing |
| 2 | reorder, chapters | `descript-script-edit.md` (`arrange.py`, then a marker per section) | markers land, chapters read right |
| 3 | rhythm, layouts | `descript-script-edit.md` (`sequence.py`, then `layout pace`/`layout apply`) | `layout cards` shows a card per beat |
| 4 | music | `descript-projects.md` (the brand's music style, searched in Descript Stock; three options offered, he keeps one) | `music offer` answered, no bed laid yet |
| 5 | motion | `motion-design` (a sibling skill, outside video-edit) | every clip rendered, watched, in Editor OS review |
| 6 | broll | `broll` (a sibling skill, outside video-edit) | sourced, imported, in Editor OS review |
| 7 | review | [review-board.md](references/review-board.md) (`editor-os transcript`, `editor-os plan`, `editor-os wait`) | he decides the open beats and the music in the project page; `edit.json` holds his choices |
| 8 | handoff | `descript-projects.md` (`descript settings` clean) | settings clean, project left for his pass |

A Short earns five of these passes and never reorders or chapters; it runs its own tighter cut,
dress and bed in place of passes 1 through 4, and hands off to encoding and scheduling instead of
pass 7.

## Learned Patterns

One log for all nine passes: [references/learned-patterns.md](references/learned-patterns.md).
Read it before a run: most entries are a call that reported success while doing something else.
Append any new failure mode there, newest last, dated, as the rule alone: git holds the story.
