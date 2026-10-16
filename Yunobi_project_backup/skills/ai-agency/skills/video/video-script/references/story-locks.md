# Story locks

Six sentence-level word swaps, not structures: walk a finished script once per lock and it comes
out tighter without a beat moving. The structure they sit inside belongs to `storytelling`; the
four-beat cycle they pace is its
[`references/addiction-loop.md`](~/Studio/vibe-kit/ai-doc/skills/content/writing/storytelling/references/addiction-loop.md).
They apply to a Short, a long-form body and a post equally, so `video-script` reads this file rather
than restating it.

**Contrast is the engine under the other five**, and it is number 6: a name contrasts with the
explanation expected, a certain sentence with a hedged one, your own thought out loud with a
stranger's, a warning with advice. If only one lock is affordable, use that one. Two collide with
rules this registry already enforces, and the registry wins: the hedge rule under lock 2, and the
banned phrase bank under lock 5.

## 1. Term branding: name the thing, then it cannot be left

Naming a concept makes it feel like a thing rather than a description (the labeling effect), and an
unfamiliar name opens a small question the viewer stays for. Hormozi's value equation and Kevin
Kelly's thousand true fans are ideas that would have been forgotten as explanations. This registry
already does it under other names: `shorts-script`, `shorts-structures.md` step 2 is "name the method", and
`video-script`'s ship list requires "one portable idea, named in the mechanism".

- A name is not a factual claim. Naming a method that does not exist, or that nobody has run, is.
- **Do not name everything.** A contrarian idea or a real framework earns a name; a step in a list
  does not. Three names per Short turns a script into a glossary.
- The name must be concrete enough to point at in the recap and carry the artefact CTA;
  `storytelling`'s motif rule is the long-form version, one object, returning changed.

## 2. Embedded truths: say it as true or do not say it

A hedge is a fork in the road. "If you try this" hands the viewer a decision about whether the
sentence applies to them, and the decision costs more attention than it returns. "When you try
this" removes the fork. Every `maybe`, `might`, `could`, `probably`, `some people` is an exit door.

| Hedged | Embedded |
| --- | --- |
| This might work because… | The reason this works is… |
| You might notice… | Once you see it, you cannot unsee it |
| Some agencies could be making this mistake | The mistake most agencies make is this |
| It could be worth trying | Do this first |

`humanizer` pattern 24 already bans over-qualifying and Ogilvy rule 9 already bans softening a
known answer, so this lock adds the mechanism rather than a new rule: the hedge does not merely
read weakly, it is where the viewer leaves.

**The collision resolves cleanly.** Ogilvy rule 9 permits honest uncertainty, and `storytelling`'s
caveat rule requires the objection to the strongest number to be said out loud. Neither is hedging.

> **Hedge the provenance of a claim. Never hedge the instruction.**

"This is one channel with no control band, so treat it as a hypothesis" is provenance, and it is
required. "This might help you a bit" is an instruction with the confidence removed: the exit door.
The caveat rule is provenance said once, at the point the number lands, after which the number
keeps being used at full strength.

## 3. Thought narration: say the thought they are having

Say out loud what the viewer is thinking at that moment, in their words, before they act on it. It
buys two things at once: they conclude you know the subject, because you knew what they were
thinking, and they now need your answer to their own question rather than to yours.

- "You are probably thinking this only works if you already have a team."
- "The question you are asking here is what happens when the client says no."
- "If you run a 4-person agency, the objection you have right now is the price."

This is the strongest form of `humanizer`'s "On camera, every I is a you": it points at the inside
of the viewer's head. It is also the general case of the objection sentence in
`shorts-script`'s [`shorts-structures.md`](shorts-structures.md) step 2b, used once, on a doubt, right after the
method is named.

**The thought is harvested, not invented.** `conversion` holds it verbatim from 367 recorded
calls, the difference between naming the doubt an agency founder actually has and the average
doubt. A guessed thought that misses reads worse than none. Cadence: after a major point, at a
transition, a few times per video. Every block turns it into a tic.

## 4. Negative frames: a warning outranks an offer

Loss aversion: people are about twice as motivated to avoid a loss as to seek an equivalent gain
(Kahneman and Tversky, 1979), so a viewer who thinks they may already be making the mistake stays
in a way one offered an improvement does not. **The negative flip** is the mechanical version: take
the point, invert it.

| Positive | Flipped |
| --- | --- |
| Here is how to grow on YouTube | This is what is killing your YouTube growth |
| Post more consistently | This posting habit is costing you subscribers |
| Use this hook format | Stop writing your hooks like this |

Softer frames work on the same instinct: "you are making this harder than it has to be" says
something is wrong without naming a fault. Two constraints: a negative frame is not a negation
pivot ([`video-hooks.md`](video-hooks.md) has the
cap, and this warns about a real cost rather than using the see-saw construction), and the mistake
has to cost something real
or say the small number, or the script becomes nothing but warnings, a fear register `humanizer`
rejects.

## 5. Loop openers: the transition is where they leave

A viewer's attention runs on a timer. The hook flips it once; every section boundary is where it
runs out. A loop opener closes the block and opens the next question in the same breath, the
re-hook beat in `storytelling`,
[`references/addiction-loop.md`](~/Studio/vibe-kit/ai-doc/skills/content/writing/storytelling/references/addiction-loop.md), at sentence scale.

**Cadence, and the source's number did not survive contact with the corpus.** He teaches one loop
opener every 20 to 30 seconds on a Short and every 60 to 90 seconds on long-form. Measured 29 Aug
2026 across 339 punctuated long-form transcripts, the niche's median gap between loop openers is
**230 seconds** (p10 85, p75 377): about 3x looser than his figure. So the house target is **no
stretch past 300 seconds**, still tighter than 90% of the corpus, and `video-script`,
`scripts/story_metrics.py` fails a script only past 831 seconds, the niche's own p75. On a Short the
~25-second flip in `shorts-script`, `shorts-structures.md` stands unchanged, unmeasured but a different claim at
19 minutes with twelve turns than at 60 seconds with one.

**The collision, and it is the important part of this file.** The source's own phrase bank is
mostly banned here: `here's the thing`, `it turns out`, `here's the problem` and `the truth is` are
in `vibe-kit/packages/lint/data/slop-words.js` as throat-clearing openers, and "here is what nobody
talks about" is the `the-part-nobody` rule. The ban does not weaken the re-hook: it catches exactly
the version of the move that carries no information.

> **The test: delete the transition. If a question or a fact is still standing, it was a re-hook.
> If the sentence disappears, it was throat-clearing.**

"And this is where it gets crazy" fails: nothing is left. "That fixes the reporting, and it is also
what broke the invoicing two weeks later" passes: the new question is in the clause. House-legal
openers name the next question rather than advertising it: "Which would have worked, except the
client had already signed." "So the reporting is solved. The invoicing is not, and this is why."
Each closes and opens on one clause and carries a fact across the boundary, which is also what
stops a loop opener becoming bait: the question opened here gets answered in the block that
follows, not in the next video.

## 6. Contrast words: split the haymaker

Curiosity is a gap between what somebody expects and what is true, and a contrast word builds the
gap inside a single sentence: `but` is the strongest, `actually` says the first belief was wrong,
`instead` redirects, `except` carves out the case that breaks the rule, `yet` holds two things that
should not both be true.

The tactic runs on the finished draft. **Go to the sentences that make the piece's main points, and
split each one in half: lean the viewer one way, then turn them.** Not "the tool saves four hours a
week", but "the tool saves four hours a week, and the agency that installed it lost six to the
training".

Three limits:

- **Not every sentence.** Overused, `but` reads as friction and the piece feels like it is arguing
  with itself. The main points only.
- **`it turns out` is banned here** by the slop list, along with the rest of lock 5's collision. The
  other five contrast words are ordinary English and are not on it.
- **A contrast word is not a licence to pivot.** "Not X, but Y" is still the negation pivot from
  [`video-hooks.md`](video-hooks.md), and this lock
  is the most common way a draft grows a second one.

## What happened when the six were measured

One script put all six over 627 videos
on 13 channels, winner band against control band inside each channel, on 29 Aug 2026. Ten of 13 is
the threshold a sign test clears at that n.

| Lock | Axis | Held in | The niche's own p25 / p50 / p75 |
| --- | --- | --- | --- |
| Term branding | term brands per 10 min | 7 of 13 | 0 / 0 / 0 |
| Embedded truths | hedged instructions per 1k | 9 of 13 | 0 / 0.66 / 3.23 |
| Thought narration | per 10 min | 6 of 13 | 0 / 0 / 0 |
| Negative frames | per 10 min | 5 of 12 | 0 / 0 / 0 |
| Loop openers | per 10 min | 7 of 13 | 0.34 / 0.84 / 1.91 |
| Contrast words | contrast sentences | 6 of 10 | 10.8% / 13.9% / 17.1% |

**Not one of them is a lever on reach**, the fifth replication of the finding `SKILL.md` opens on
and the first that covers craft rather than construction. Embedded truths comes closest, and it
points at *less* hedging in winners rather than more technique. Still worth having: four of the six
are unused in this niche, the median video carrying zero term brands, zero thought narration and
zero negative frames, and it puts numbers under two house rules that were taste, the
one-negation-pivot cap landing on the niche's p75 to p90 (0.18 per 1k words) and 75% of the niche
never using a banned throat-clearing transition at all.

**The instrument has bounded recall**: a fixed phrase list misses a fresh loop opener and cannot
tell a hedge from a hedge being quoted to be criticised, so every count is a floor.

## Provenance

Kallaway (@kallawaymarketing), "Say This in Your Videos, It'll Improve Your Storytelling by 10x",
`https://www.youtube.com/watch?v=pcnrzBwoVUk`. Keep the full transcript in your own corpus.
Same source as `shorts-script`'s [`shorts-structures.md`](shorts-structures.md): one practitioner, no control band,
and his register is rejected on sight by `humanizer` even where the mechanic is kept.
