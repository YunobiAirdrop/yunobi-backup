---
name: video-coach
description: "Reviews a recorded long-form take against the plan it was recorded from, before a single cut is made. Reads the concept and its script from the app, the raw transcript from Descript, measures what the take actually did, and returns one habit to change on the next recording. Use after a recording lands in Descript and before descript-script-edit, when a take felt off and the reason is not obvious, or on 'coach me on this video', 'how did that take go', '/video-coach'."
tags: [audits, video]
---

# Video Coach

The take is finished, nothing is cut yet, and this is the only moment the raw
recording still exists. Cut first and the evidence about how the speaker records is
gone: the restarts, the abandoned openings, the block he talked himself out of.
So this runs **before `descript-script-edit`**, always.

Announce at start: "I'm using the video-coach skill."

## What it is for, and what it is not for

It answers one question: **what should be different in the next recording?**

It does not grade fidelity to the script. The speaker talks and finds the line on
camera, and the best takes in the corpus are the ones where they left the page.
Drift is only ever reported when the drift **cost something measurable** - a
promise opened and never paid, an ask that moved out of the last twenty seconds,
a number said with no artefact behind it, a block that ended on a sentence
instead of on the board looking different.

It is not a cut list either. `descript-script-edit` owns what leaves the video.
This skill owns what changes about the way the next one is recorded.

## The one-thing rule

**The report leads with exactly one habit.** Not a ranked list of eight, not
"here are some observations". One, named, with the seconds it cost in this take
and the recording where it last appeared.

The reason is mechanical: a coaching note that lists eight things gets read once
and changes nothing, and the ledger cannot tell whether any of them landed. One
habit per video is checkable on the next video, which is what makes this a loop
instead of a report.

Everything else goes below the fold, under "Also seen", unranked and unargued.

## Listen to the take with the picture off

One pass, before anything else, and it is the only instrument that reads pacing honestly. Play the
raw audio and do not watch it.

- **Bored** means the sentences are running long and the delivery is flat. The note is about the
  take, not about the edit: the next recording gets shorter sentences and more energy on the verbs.
- **Cannot keep up** means he is compressing past comprehension. The note is to leave air after each
  number and each new term.

Watching hides both, because the picture supplies interest the audio has not earned and the eye
forgives a rhythm the ear will not. On the finished cut the same test belongs to `video-script`,
where it becomes a note to the editor. Here it belongs to the take, and it is one of the few
things this skill can see that a script review cannot.

## The workflow

```
find the concept  ->  read the plan  ->  read the raw take  ->  measure it
   ->  align plan to take  ->  run the checks  ->  score the writing
   ->  write the ledger row  ->  render the page  ->  open it
```

### 1. Find the concept

The take names its video by title and nothing else, so start from the title.

```bash
KEY=$(grep '^UPSYS_APP_API_KEY=' app/.env.local | cut -d= -f2-)
curl -s -H "Authorization: Bearer $KEY" http://localhost:3160/api/youtube/concepts \
  | jq '.data.concepts[] | select(.title | test("Agency Master"; "i"))'
```

The dev server talks to the production database, so this reads the real concept.
It has to be up; never start or stop it, ask. If no concept matches the Descript
project name, **stop and ask which one it is.** Reviewing a take against the
wrong plan produces confident nonsense.

### 2. Read the plan

```bash
curl -s -H "Authorization: Bearer $KEY" \
  "http://localhost:3160/api/youtube/concepts/<id>/script" | jq .data
```

`GET` reads, `POST` regenerates. **Never POST here.** The plan is the thing being
measured against, and a review that rewrites its own baseline measures nothing.
A concept with no script yet answers 404: that is a finding in its own right
("recorded with nothing written"), not an error to work around.

The script arrives as the eight blocks from `video-script`: `name`, `startsAt`,
`onScreen`, `spoken`, `endsOn`, plus `ask` and `claimsToVerify`.

### 3. Read the raw take

Descript, raw, before anything is ignored:

```
mcp__claude_ai_Descript__get_project        -> composition id and duration
mcp__claude_ai_Descript__export_transcript  -> format txt, speaker labels off
```

If the composition has already been cut, say so in the report and measure what
survives. The recording-habit numbers are then a floor, not a measurement.

### 4. Measure it

```bash
python3 scripts/take-stats.py transcript.txt --duration 1767 > stats.json
python3 ../video-script/scripts/story_metrics.py transcript.txt --duration 1767 --grade
```

`take-stats.py` returns words, pace, runtime against the 3,600-4,200 word budget,
the retake and truncation count with the seconds they cost, filler density, and the
five paragraphs where restarts cluster. `story_metrics.py --grade` returns the seven
story rules, each with the sentence that broke it and its percentile against 627
measured videos: it is check D10 and it scores W10. Every number in the report comes
from one of those two or from the API. **No number in the report is estimated.**

### 5. Align plan to take

Walk the planned blocks in order and mark each one against the transcript:
`delivered`, `dropped`, `added`, `reordered`, `thinned`. Match on the beats in
`spoken`, not on wording - the wording is expected to change.

An added block is not a fault. A dropped one is only a fault if something else in
the video depended on it, which the checks decide.

**Count the verdicts before you write any of them down.** If more than half the
planned blocks come back dropped or reordered, the plan and the take are not the
same video and per-block faults stop meaning anything - nine rows saying "dropped"
is one finding wearing nine hats. Say the divergence once, at the top, and keep the
block table as a record rather than as a charge sheet. Then check the plan itself:
a script under the 3,600-word floor is why the take had to improvise, and that is a
fault in the plan, not in the delivery.

### 6. Run the checks

[`references/checks.md`](references/checks.md) holds them, in two families: the
doctrine checks that come from `video-script` and `video-hooks`, and the strategy
checks that come from the competitor dossiers. Each check returns pass, fail, or
not-applicable, and every fail carries its source file. **A check with no source
does not go in the report.**

### 7. Score the writing

Ten lines, one point each, 1 / 0.5 / 0, totalling a number out of 10. The rubric is
the last section of [`references/checks.md`](references/checks.md) and seven of the
ten lines read their verdict straight off the checks you have just run, so the score
can never disagree with the table printed under it.

**Every line quotes the sentence that earned or lost it.** A line with nothing to
quote is unscored and the total says so, rather than being scored at zero.

The score is about the writing. Restarts, truncations, filler and pace are excluded
because the edit removes all of them, and a number that moves when the cut moves is
not measuring what was written.

### 8. Write the ledger row

One ledger file outside the skill, one row per recording, appended:

```json
{"date":"2026-08-19","title":"...","conceptId":"...","compositionId":"...",
 "writingScore":3.0,"priorWritingScore":null,
 "oneThing":"...","priorOneThing":"...","priorFixed":true,"stats":{...}}
```

The `priorFixed` field is the whole point of keeping a ledger. Before writing the
row, read the previous one and test its `oneThing` against **this** take's stats.
The report opens with that verdict, because "the thing I told you last time" is
the only claim in the document that has already been tested.

### 9. Render and open

```bash
python3 scripts/report.py findings.json -o ~/Desktop/reviews/video-coach-<slug>.html
open "file://$HOME/Desktop/reviews/video-coach-<slug>.html"
```

Self-contained HTML on disk, opened in a browser. Never an Artifact, never a terminal
dump - the block-by-block table is unreadable in a terminal and this is meant to
be looked at.

## What the page says, in order

1. **Last time I said X.** Fixed, or not, with the number that decides it.
2. **Writing, x.x out of 10**, with the previous score beside it and the ten lines
   that produced it, each carrying its quote.
3. **The one thing.** The habit, the seconds it cost here, what to do instead.
4. **The take in numbers.** Words, pace, runtime, retakes, filler density, each
   against its target.
5. **Plan against take.** One row per planned block: planned, delivered, verdict.
6. **What the drift cost.** Only the drift that cost something. Empty is a
   legitimate and good result, and is printed as "nothing".
7. **Against the strategy.** The dossier checks, each with its source file.
8. **Also seen.** Everything that did not win. Unranked, one line each.

## The things this skill keeps getting wrong

**Confusing a dropped block with a fault.** Half the dropped blocks in the corpus
were dropped because the take found a better route. Ask what depended on it
before calling it a loss.

**Counting restarts as a quality signal.** They are a cost, in seconds, and
`descript-script-edit` removes them completely. A take with 40 restarts and a
clean argument is a better take than one with 4 and a muddled one. Restarts only
become the one thing when they cluster on the same block across two recordings -
that is a preparation problem, not a delivery one.

**When they do win the slot, prescribe a recovery move, never "prepare more".** A block
recorded from a bullet with no claim in it has nothing to return to, so the next one opens on
the one-sentence line `video-script` now asks for and comes back to it. Lost anyway, he says
"what was I just saying" out loud and carries on: the edit removes that the way it removes a
restart, where a restart costs the whole sentence twice. First run here: 74 spans, 19:46 of
56:38, 34.9%, off a plan 1,100 words under its floor. One unmeasured source for the move,
31 Aug 2026, Joseph Tsar, `How To Never Ramble When You Speak`.

**Letting the score drift from the table.** Seven of the ten lines are the doctrine
checks. If W2 says half a point and D1 says fail, one of them was written by feel.
Score the lines from the verdicts, never alongside them.

**Reporting the word count without the ask placement.** The word budget is the
famous rule and the weakest one. The ask rule beat it 3 to 5x in the same
control. Check the ask first.

## Sources this reads

Every check names its own source, and they are collected at the head of
[`references/checks.md`](references/checks.md).

None of it is restated here. A rule that lives in two files drifts, and the
drift is silent - `video-script` and `script-contracts.ts` had already done it
once by 19 Aug 2026.

## Self-Healing

Append every new failure mode to
[`references/learned-patterns.md`](references/learned-patterns.md), newest last,
dated. A check that turns out to be stale is corrected in `references/checks.md`
in the same session, and in the file it came from if the rule itself moved.
