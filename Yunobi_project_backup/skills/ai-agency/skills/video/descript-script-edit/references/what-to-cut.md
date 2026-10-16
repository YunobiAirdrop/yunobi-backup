# What to cut

Two passes. Pass 1 removes the wreckage of speaking. Pass 2 removes complete, well-formed sentences
that carry nothing. `SKILL.md` states the rule; this is the method.

### Pass 1, the mechanical pass

Do not eyeball this one. `scripts/candidates.py` enumerates it from the block dump, and the cut
list is then auditable against that enumeration:

```bash
python3 candidates.py blocks.json                       # every candidate
python3 candidates.py blocks.json --check needles.json  # what the list does not cover
```

It reports two kinds. **Repeat runs**: any three-word run said twice within 400 characters, where
the span from the first attempt to the last is the cut and three attempts at one sentence merge
into one needle. Keep whichever version is complete - usually the last, but take the first when the
retake is the broken one. **Truncation marks**: `--`, `...` and one-to-three-letter hyphenated
stumps, with the run-up that leads into them.

**Every candidate is a needle or a dismissal.** `--check` comes back empty, or every survivor has a
one-word reason. On M0 L1 the shipped list left sixteen uncovered, ten of them real - including the
lesson's two largest wastes, a four-attempt opening sentence and a paragraph that said `This is not
a sales pitch` six times. Nothing in that run reported a problem, because nothing was checking.

Dismiss what deliberate speech looks like: anaphora (`You don't know how to deal with them. You
don't know how to deal with that influx of work.`), a list whose items share an opening, a phrase
repeated for emphasis across a paragraph break. Leave small stutters whose only clean needle is
ambiguous (`s- `, `add-- `) - they cost a fraction of a second and a wrong match costs a sentence.

### Pass 2, the meaning pass

Pass 1 cannot see these, because there is nothing wrong with them as sentences. Read the pass-1
result as prose and put one test to every sentence: **delete it, read its two neighbours together,
and name what the viewer lost.** Nothing lost is a cut.

1. **Announcements.** A sentence that says what the next sentences are about to do. `If you see
   yourself in one of these bullet points, then it makes sense to explore the principles of Agency
   Master` - the bullets say that, and they say it next. Pointing at a visual is not an
   announcement: `This is an example of a week of work` earns its place, because it cues the
   screen.
2. **Second utterances of one idea.** Pass 1 catches the same *wording* twice. This catches the
   same *idea* twice in different wording, which is far more common and costs far more time. One
   utterance per idea: keep the strongest, cut the others even though each is a clean sentence.
3. **Hedges and disclaimers.** `This is not a sales pitch`, `I don't want to promise you`, `I'm not
   gatekeeping anything`. Once is positioning. The second time is the speaker reassuring himself.
4. **Digressions.** Asides about how the product might change later, coffee-break jokes, telling
   the viewer to take a break. Anything that drops the pace without teaching. Rationale that
   justifies a choice is not a digression - keep it.
5. **The speaker.** Every sentence whose subject is the person on camera: the credential, the
   ten years, the process, the week he had, the reason he made the video, the warm-up before the
   idea. **Read the first-person sentence, write the sentence about the viewer that carries the
   same information, and if there is not one, cut it.** Four survivors and no fifth: a hedge on
   his own number ("I'm very conservative"), the DM ask ("I'll send you the playbook"), an
   assignment ("So now I want you to..."), and a line somebody else said that is the mechanism
   of the piece. A failure story survives only where the viewer is living the same failure.
   `humanizer`, "On camera, every I is a you", holds the measurement and the rewrite pairs.

Pass 2 changes what the speaker said, not only how cleanly he said it, so list every pass-2 cut in
the run report. That is the part the user will want to read back.

### The ratio says whether the list is long enough

Measure the list before driving it: characters removed over characters in the block dump.

| | first-take lesson | tight short |
|---|---|---|
| pass 1 | 14-20% | 20-35% |
| pass 1 and pass 2 | 22-30% | 30-45% |

Below those numbers means under-listed, not a clean take.

**Pass 2 item 5 runs far past the table and that is correct.** Four Shorts cut on 20 Aug 2026 kept
25%, 33%, 39% and 43% of the raw take, so 57 to 75% of the seconds left, and the extra over the
band above was one category: the speaker. A take that rambles into the idea gives up more than half
of itself, and the survivor is a short that opens on the viewer in its first sentence. M0 L1 measured 14.5% at 29 needles and
22.8% at 40, and the eleven added needles are the difference between a script with no stutters and
a script with nothing spare in it. `scripts/needles.example.json` is that finished list, both
passes, every needle resolving exactly once.

## Reading the finished transcript for what you never listed

Moved out of SKILL.md on 31 Aug 2026 to hold it under the 250-line ceiling.

A run reporting every needle landed says nothing about the needles you failed to write. Two faults,
and only one is about seams: glued words mean a needle took both boundary spaces, and
`[a-z][.,][A-Za-z]` finds those; a surviving restart means the cut list was short, and only the
transcript read as prose finds that. Run `candidates.py` on the finished export as well, where
anything beyond the dismissals you already named is a needle that never landed. A missed needle is a
one-line `fix.json` through the same driver, so never hand one back.
