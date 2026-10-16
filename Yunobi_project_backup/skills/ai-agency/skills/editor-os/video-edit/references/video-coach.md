# Video Coach

The take is finished, nothing cut yet: the only moment the raw recording still
exists. Cut first and the evidence of how the speaker records is gone: the
restarts, the abandoned openings, the block he talked himself out of. So this
runs **before the script cut**, always, long-form only — a Short is one
argument, not a recording worth coaching against a plan.

Announce at start: "I'm using the video-coach skill."

## What it is for, and what it is not for

It answers one question: **what should be different in the next recording?**

It does not grade fidelity to the script. The speaker talks and finds the line on
camera, and the best takes in the corpus are the ones where they left the page.
Drift is only ever reported when the drift **cost something measurable** - a
promise opened and never paid, an ask that moved out of the last twenty seconds,
a number said with no artefact behind it, a block that ended on a sentence
instead of on the board looking different.

It is not a cut list either. `descript-script-edit.md` owns what leaves the video.
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

Each step, the exact commands, and the rule for it, including the two loads not to skip (never
`POST` the plan endpoint; no number in the report is estimated): [workflow.md](workflow.md).

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
`descript-script-edit.md` removes them completely. A take with 40 restarts and a
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
[checks.md](checks.md).

None of it is restated here. A rule that lives in two files drifts, and the
drift is silent - `video-script` and `script-contracts.ts` had already done it
once by 19 Aug 2026.

## Self-Healing

A check that turns out to be stale is corrected in [checks.md](checks.md) in the same session,
and in the file it came from if the rule itself moved.
