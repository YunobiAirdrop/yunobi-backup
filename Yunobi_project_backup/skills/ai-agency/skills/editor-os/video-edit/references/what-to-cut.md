# What to cut

Two passes. Pass 1 removes the wreckage of speaking. Pass 2 removes complete, well-formed sentences that carry nothing. `SKILL.md` states the rule; this is the method.

### Pass 1, the mechanical pass

Do not eyeball this one. `scripts/candidates.py` enumerates it from the block dump, and the cut
list is then auditable against that enumeration:

```bash
python3 candidates.py doc.json --comp "<name>"         # every candidate, off a doc dump
python3 candidates.py doc.json --check needles.json    # what the list does not cover
```

It reports two kinds. **Repeat runs**: any three-word run said twice within 400 characters. **Truncation marks**: `--`, `...` and one-to-three-letter hyphenated stumps, with the run-up.

### The last attempt is the keep, always

The author, 11 Sep 2026: **"it never takes the last retake ... always use the last retake."** A speaker
who says a sentence again has said it better, and the attempts before it are the wreckage. The
reported span runs from the first attempt to the START of the last one, and `keep` prints the words
that survive it. When the last attempt is itself a stump it is not an attempt: the span stops at
the last COMPLETE one, and the stump leaves with the truncation candidate that already names it.

**Never splice one attempt's head onto another's tail.** What survives has to be one unbroken run of
speech: the words either side of a seam were spoken minutes apart, so the cadence and the room jump
mid-sentence. FC38 shipped `Si vous démarrez sur ClickUp ou que vous voulez` from attempt 2 joined
to `utiliser plus de fonctionnalités` from attempt 4, attempts 1 and 3 cut around them - three
paragraphs cut and the sentence still wrong.

**The search runs over the JOINED script, never block by block.** Descript breaks a paragraph
exactly at the pause before a restart, so the restart lands in the paragraph AFTER the one it
abandons and a per-block search is blind to it. That opening returned zero candidates before
11 Sep 2026; the joined search returns it as one candidate spanning three paragraphs. Over FC38's
41k-character raw script it is 99 repeat runs against 40, and 37 of the 99 cross a paragraph break.

**A needle cannot cross a paragraph break, so a span over three paragraphs is three needles**, and
`--check` counts them: it subtracts every needle from each block slice and prints what is still
live. Covering the ends and leaving the middle is what the old head-match test passed.

**Every candidate is a needle or a dismissal.** `--check` comes back empty, or every survivor has a
one-word reason. On M0 L1 the shipped list left sixteen uncovered, ten of them real, including a
four-attempt opening sentence and a paragraph that said `This is not a sales pitch` six times.

Dismiss what deliberate speech looks like: anaphora (`You don't know how to deal with them. You
don't know how to deal with that influx of work.`), a list whose items share an opening, a phrase
repeated for emphasis. Leave small stutters whose only clean needle is ambiguous (`s- `, `add-- `):
they cost a fraction of a second and a wrong match costs a sentence.

### Pass 2, the meaning pass

Pass 1 cannot see these, because there is nothing wrong with them as sentences. Read the pass-1
result as prose and put one test to every sentence: **delete it, read its two neighbours together,
and name what the viewer lost.** Nothing lost is a cut.

**This one is read, not enumerated, and the read is dispatched**, on the exact brief below. A
digression is a well-formed sentence, so nothing mechanical sees it; item 2 below is the only one
of the five a score can reach.

`scripts/restate.py` is the backstop that runs after, not the pass: it pairs two sentences within
`WINDOW` of each other whose content words overlap by `OVERLAP` of the shorter, which is how *here
I've connected my Google Drive account* and *you could also give it the capacity to look into your
Gmail, into your Google Drive* come back as one pair. The author, 8 Sep 2026: **"Here I've repeated
myself twice."**

```bash
python3 restate.py doc.json --comp "<comp>"        # the backstop, by kind
python3 restate.py doc.json --check needles.json   # what the cut list does not cover
```

**A flag is a pointer to a paragraph, not a verdict on a sentence.** The same run flagged *So that
means each time it makes a mistake and you steer it by mentioning in a comment or just chatting with
the agent as if you're chatting with a human*, and the session dismissed it because the sentence
teaches the self-learning loop, which it does. The waste was the clause: one way of steering is the
teaching, two is padding, and the simile is the padding on the padding. The author cut it by hand. Read
every flag down to the clause before dismissing the sentence that holds it.

1. **Announcements.** A sentence naming what the next sentences are about to do: `If you see
   yourself in one of these bullet points, then it makes sense to explore the principles of Agency
   Master` - the bullets already say it. Not an announcement when it cues a visual: `This is an
   example of a week of work` earns its place.
2. **Second utterances of one idea.** Pass 1 catches the same *wording* twice; this catches the
   same *idea* twice in different wording, far more common and far more costly. Keep the
   strongest utterance, cut the others even though each is a clean sentence.
3. **Hedges and disclaimers.** `This is not a sales pitch`, `I don't want to promise you`, `I'm not
   gatekeeping anything`. Once is positioning. The second time is the speaker reassuring himself.
4. **Digressions.** Asides about how the product might change later, coffee-break jokes, telling
   the viewer to take a break. Anything that drops the pace without teaching. Rationale that
   justifies a choice is not a digression - keep it.
5. **The speaker.** Every sentence whose subject is the person on camera: the credential, the
   years, the process, the week he had, why he made the video. **Read the first-person sentence,
   write the viewer sentence carrying the same information; if there is not one, cut it.** Four
   survivors on one pass: a hedge on his own number ("I'm very conservative"), the DM ask, an
   assignment, and a line somebody else said that is the mechanism. `humanizer`'s "every I is a
   you" holds the measurement and the rewrite pairs.

Pass 2 changes what the speaker said, not only how cleanly he said it, so list every pass-2 cut in the run report.

### The pass-2 brief, verbatim

A brief rewritten from memory each run is a different brief each run, so paste the block below
exactly. Write the live paragraphs to a text file, one per line, each prefixed with `[<index>] `
and newlines inside a paragraph shown as ` ⏎ ` (`scripts/restate.py` shares that loader). One
Sonnet subagent
 reads the WHOLE script, since a callback over a split is invisible to
both readers, **then reports 50 paragraphs at a time**, and the session applies each chunk while it
writes the next. The author, 23 Sep 2026, after 18 minutes of silence on 308 paragraphs: *"its job
should be recursive."* Put this line above the block:

> Read the whole file first, then for each 50 paragraphs append ONE line holding that chunk's JSON
> array to `<dir>/proposal.jsonl` and print `CHUNK <n>`. Print `DONE` after the last.

---

Read `<path to the half>`. It is the surviving script of a finished video, one paragraph per line,
each prefixed with its paragraph index in square brackets. ` ⏎ ` marks a newline inside a paragraph.

Your job is the CLAUSE-level digression pass. A previous pass already removed stutters, restarts,
filler, and whole restated sentences. What is left is clean prose with dead weight still inside
individual sentences. Find it.

THE TEST, applied to every clause, not only every sentence: delete the clause, read what remains,
and name what the viewer lost. Nothing lost is a cut.

Cut these:

1. **A second example of one idea.** "by mentioning in a comment or just chatting with the agent as
   if you're chatting with a human" - one way of steering it is the teaching, two is padding, and
   the simile is the padding on the padding. This is the archetype; find every sibling.
2. **A simile or restatement tacked onto a clause that was already complete**: "as if you're
   chatting with a human", "exactly like your company members", "think of it as...".
3. **Trailing vagueness**: "and stuff", "or whatever", "or something", "blah blah blah", "and you
   name it", "and so on".
4. **A hedge inside a sentence**: "obviously", "pretty much", "basically", "literally", "kind of",
   "like" as a filler, "I think", "maybe", "a little bit" - ONLY where removing it changes nothing.
   Some of these carry real meaning ("a little bit better organized" after a comparison does).
5. **A doubled adjective or a doubled clause** inside one sentence: two words where the sentence
   used one idea.
6. **A self-justifying aside** the sentence does not need: "for reference", "just as a reminder",
   "FYI", "by the way", "don't worry", "if I wanted".

Do NOT cut:

- anything that cues what is on screen ("here we're in the Delivery space", "if I open my Gmail") -
  the footage needs its narration
- a concrete number, product name, or a named client
- rationale that justifies a choice
- the one commercial ask, or the community ask
- a clause whose removal leaves the sentence ungrammatical or leaves a full stop followed by a
  lowercase word

OUTPUT. A JSON array, nothing else, no prose around it. Each element is
`[<paragraph index as a string>, "<the exact text to remove>"]`. Rules that make it usable:

- the text must be a VERBATIM substring of that one paragraph, copied character for character
  including its leading and trailing spaces and any comma that belongs to the cut - check it
  against the line before you write it
- include the trailing space when the cut sits between two words, so the remaining words do not
  glue together
- never write ` ⏎ ` in the needle; if a cut would cross the newline, split it into two entries
- do not propose a needle whose text appears more than once in that paragraph
- 15 to 30 entries per 200 paragraphs. Be strict: a marginal cut is a wrong cut.

Return only the JSON array (one per chunk, per the chunk rule).

---

**Judging what comes back.** The union is a proposal, not a cut list. Resolve every needle against
the live document before driving it, and drop, never repair by guessing, one that resolves to zero
or two live paragraphs. Then read each one against the "do NOT cut" list yourself: an agent reading
half a script cannot see that a clause cues a shot three paragraphs later.

**Strip a leading `, ` off every needle before driving it**: the CLI snaps the cut back over the
word before, and the gate refuses the batch ("holds 1 word(s) its seconds do not"). Each chunk is one
`pnpm descript edits` batch, back to front, `--dry` first.

### The ratio says whether the list is long enough

Measure the list before driving it: characters removed over characters in the block dump.

| | first-take lesson | tight short |
|---|---|---|
| pass 1 | 14-20% | 20-35% |
| pass 1 and pass 2 | 22-30% | 30-45% |

Below those numbers means under-listed, not a clean take.

**Pass 2 item 5 runs far past the table, and that's correct**: four Shorts on 20 Aug 2026 kept
25-43% of the raw take, the extra all the speaker. `scripts/needles.example.json` is a finished list.

## Reading the finished transcript for what you never listed

A run reporting every needle landed says nothing about the needles you failed to write. Glued words
mean a needle took both boundary spaces, and `[a-z][.,][A-Za-z]` finds those; a surviving restart
means the cut list was short, and only a prose read finds that. Run `candidates.py` on the finished
export too: anything beyond the dismissals you already named is a needle that never landed. A
missed needle is a one-line `fix.json` through the same driver, never a hand-back.

## The house glossary

`--typos` is the house glossary that stops a caption saying the wrong product name (`Hyper Frame` -> `HyperFrames`, `Cloud Code` -> `Claude Code`): `scripts/typos.example.json`, internal names in `typos.internal.json`. **A key that is an ordinary English word rewrites correct speech.** `"ski": "skill"` turned *I ski a lot* into *I skill a lot*; `"School": "Skool"` caught a sentence opening on the word. Both were pulled the day they were written; test any new key against ordinary prose.
