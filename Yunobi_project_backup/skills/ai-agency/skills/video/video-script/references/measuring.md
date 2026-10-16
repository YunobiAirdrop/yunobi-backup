# Measuring a script, and measuring somebody else's

Two scripts, one question each. `story_metrics.py` measures the story mechanics of a draft or a
take; `teardown.py` measures a reference video somebody has sent. Both exist so a review argues
with a number instead of with an impression.

## story_metrics.py

```bash
python3 .claude/skills/video-script/scripts/story_metrics.py <path> --duration <seconds> --grade
python3 .claude/skills/video-script/scripts/story_metrics.py <path> --json      # every count
```

It reads a transcript (`.txt`), a stored competitor transcript (`.json` with `fullText`), or a
script (`.json` with `blocks`), and counts seams, loop openers, throat-clearing, hedges, contrast,
thought narration, negative frames, term brands, negation pivots, the prediction beats and the
stakes triad. Pronouns are deliberately absent: `video-edit/scripts/take-stats.py` owns those.

### The seven rules, and where each threshold came from

| Rule | Warn | Fail | Source |
| --- | --- | --- | --- |
| `throatClearing` | > 0 | > 0 | house; the niche p75 is 0 |
| `emptyRehooks` | > 0 | > 1 | house |
| `negationPivots` | > 1 | > 3 | house; the niche p75 is 0.18 per 1k words |
| `hedgesOnInstructionPer1k` | > 3.23 | > 5.74 | corpus p75 / p90 |
| `longestGapSeconds` | > 300 | > 831 | house target / corpus p75 |
| `contrastSentencePct` | < 10.8 | < 8.8 | corpus p25 / p10 |
| `triadComplete` | false | never fails | house; the niche p90 is 0 |

**A house number is tighter than the niche on purpose.** The corpus measures reach, and none of
these axes separated a winner from its own channel's controls in it, so the niche median describes
what people do rather than what works. A corpus number is there to stop a house target firing on
everything: a single-tier gate anchored on the house target alone failed 90% of 627 videos, which
is an instrument that says nothing.

### Two limits it enforces on itself

**It will not grade an unpunctuated transcript on the sentence-shaped rules.** 288 of the 627
tracks in the corpus come back from yt-dlp with no sentence punctuation, and on those a "percentage
of sentences carrying a contrast" is a measurement of YouTube's ASR. Below one terminator per 100
words it prints `n/a` and says why.

**It is a fixed phrase list, so its recall is bounded.** It sees a loop opener written the way this
niche writes them and misses one phrased freshly, which makes every cadence number an upper bound
on the true gap. It also cannot tell a hedge from a hedge being quoted in order to be criticised.
Read a WARN as "look here", never as "this is wrong".

### The norms

`scripts/story-norms.json`, written by the corpus pass, carries p10 to p90 for every axis over
627 videos and 13 channels, plus how many channels each doctrinal direction held in. Regenerate it
by re-running that pass; the grader falls back to house thresholds when the file is absent.

## teardown.py

Somebody sends a video that works and asks for one shaped like it. Describing it produces
adjectives, and an adjective cannot be checked against a rule.

```bash
python3 .claude/skills/video-script/scripts/teardown.py <url>            # free, no download
python3 .claude/skills/video-script/scripts/teardown.py <url> --cuts     # also shot rhythm, 480p
python3 .claude/skills/video-script/scripts/teardown.py <url> --json
```

| It prints | Read it against |
| --- | --- |
| words, runtime, wpm | the runtime rules, and the density their read was written at |
| the first 30 seconds verbatim | `video-hooks`, which owns the cold open |
| where the first number lands | the measured finding that hits and flops reach it at the same moment |
| every ask, with its position | the ask rule: one ask, in the last twenty seconds |
| the author's published chapters | the eight-block table and its shares |
| cuts a minute, per quarter | how much the edit is doing to hold a viewer the script keeps with words |

**A reference tells you what somebody got away with, never what works.** One channel with no
control band: use it to find the specific move worth stealing, and take the number that governs it
from `SKILL.md`.

## Four audits on the draft

Four audits, run on the draft rather than on the analytics. `SKILL.md` names them; this is each one.

**Two usable things, early.** One non-obvious thing the viewer can go and change lands inside the
first block, a second before the average view duration. One hit and they may stay; two and they
stay, because the video has proved it holds more. A definition is not a hit: the test is whether
they can act on it today, rung 3 on `storytelling`'s literalness ladder.
**The eyes-closed test settles pacing, and nothing else does.** Play the cut with the picture off
and listen. Bored means the sentences are running long and the edit is not chopping; unable to keep
up means it is chopped past comprehension. The page has no tempo, so reading it finds neither. Run
it on the first assembly, and the note goes to the editor as a note about the audio.
**Reset your tolerance before you judge the cut.** After watching a take twenty times you are the
least qualified viewer it has: scroll a feed for five minutes, then watch it once through. What
reads as slow on the second pass is slow. Single source, no control test: Mino, Feb 2026,
`video-hooks` `references/hook-teardown.md`, who reports cutting roughly half a finished video
this way.
**One debatable question, written on purpose.** A block that leaves a genuinely contested question
open produces comment threads that argue with each other, and argument is what platforms pay for.
Not a bait question, which `social`'s `references/writing-posts.md` bans and X demotes: a real fork in the subject the
video declines to close, said once, in the teach.

## The seam between two blocks is where they leave

A body loses people where a block finishes, because that is the moment nothing is unresolved and
the viewer remembers they have work to do. The re-hook, its measured cadence and the
delete-the-transition test are [story-locks.md](story-locks.md) lock 5; what the block owes before
it (stakes with a clock, a big question specific enough to guess wrong at) is `storytelling`,
[`addiction-loop.md`](~/Studio/vibe-kit/ai-doc/skills/content/writing/storytelling/references/addiction-loop.md).
**A body with no point where the viewer can guess wrong is a correct list**, and a bullet outline is
the cheapest place to fix that. **When the body is a counted list the last seam is a demotion**,
paid for in the outline: rank the items by what carries the result, put that one last, and the line
before it ("none of the first two move anything without this") is then true.
