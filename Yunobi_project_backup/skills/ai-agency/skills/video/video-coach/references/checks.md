# The checks

Two families. Doctrine checks ask whether the take obeyed the rules the script was
written under. Strategy checks ask whether the video, as recorded, still competes.

Every check returns `pass`, `fail` or `n/a`, and every `fail` carries the file it
came from. A check that cannot name its source is an opinion and does not go in
the report.

---

## Doctrine checks

Source: the `video-script` and `video-hooks` skills, and a three-run control read off one
channel that shipped the same argument three ways.

### D1. One outbound ask, in the last twenty seconds

The strongest rule in the corpus and the one most often broken by talking. Count
every ask in the transcript that sends the viewer somewhere outside the video:
buy, book, download, go to the link, join. In-platform asks (subscribe, like,
comment) do not count and are allowed early.

- **fail** if there is more than one outbound ask.
- **fail** if the single one starts before the final 2% of runtime.
- **fail** if the close offers two actions (a purchase *and* a call). Two actions
  convert neither.

The losing run in the three-run control asked at 11% and lost by 3 to 5x. This is
checked before the word count, every time.

### D2. The failure told in full

The winner is the only run that tells the founder's own failure properly. Look
for it in the take: the specific agency, the specific number, the specific night.

- **fail** if the failure is one line, or is somebody else's failure only.
- **fail** if the viewer cannot see themselves inside it: a credential, a process or
  a good week is not a failure, it is the ego cut D9 removes.
- **n/a** if the script had no failure block, which is itself worth a line under
  "Also seen".

### D3. No arithmetic on camera

Ninety seconds of on-screen arithmetic appears only in the losing run. Show the
number and its artefact; never derive it.

- **fail** on any passage that computes a figure out loud from other figures.

### D4. Every build block ends on a visible state change

A block that ends on a sentence is a paragraph. Compare each delivered block
against its planned `endsOn`.

- **fail** for a build block that ends on a summary sentence with nothing changed
  on screen.

### D5. Camera language outside, mechanics inside

the doctrine, camera language section. The failure, the stakes and the ask stay in the words
a founder already uses. Named mechanics are allowed inside the teach blocks, once
the thing is on screen.

- **fail** if a mechanic is named in the cold open, the stakes or the ask.

### D6. Every number has an artefact

- **fail** for any figure spoken without the thing that proves it being named or
  shown. One invented figure costs the whole position.

### D7. Runtime and word budget

3,600 to 4,200 words, 190 to 200 wpm, which lands around 19 minutes. Nineteen
minutes beat twenty-nine in the control.

- **fail** over 4,500 words of *delivered* content, measured after the retakes are
  discounted, because a raw transcript double-counts every restart.
- Report the raw and the discounted number separately. Only the discounted one is
  judged.

### D8. The hook is the planned hook

The opening 30 seconds belong to `video-hooks` and its wording is load-bearing.
The script writes those lines out in full inside quotes for that reason.

- **fail** if the quoted cold-open lines were paraphrased on camera.
- **n/a** if the take opened on a different hook that was then kept - note it, do
  not judge it, and say which one shipped.

### D9. The first-person count

Count "I", "I'm", "I'll", "I've", "my", "mine", "me", "we", "our" across the whole
transcript, and count "you", "your", "yourself" beside it. The target is zero first
person. Four Shorts cut on 20 Aug 2026 measured 12 against 63, and two of them ran
literal zero. `take-stats.py` returns `firstPerson`, `secondPerson`, `firstPersonHits`
and `firstPersonInOpen`, each hit carrying the sentence to rewrite.

- **fail** on any first person outside four jobs: a hedge on his own number, the DM
  ask, an assignment, a line somebody else said, plus the failure block D2 allows.
- **fail** if the open carries any first person at all: the first 30 seconds of a
  long-form take, the first sentence of a Short. `firstPersonInOpen` in
  `take-stats.py` is that window. The open spends the only attention the video is
  guaranteed.
- Quote the worst offender and write the second-person sentence that replaces it.

Source: `humanizer`, "On camera, every I is a you", and the rule as it was set, 20 Aug 2026:
"People don't care about me. Every I should be a you."
### D10. The story gate

The only check in this file that is computed rather than read. `video-script`,
`scripts/story_metrics.py --grade` returns seven rules over the transcript, in two tiers, each
carrying the sentence that broke it and its percentile against 627 measured videos.

```bash
python3 .claude/skills/video-script/scripts/story_metrics.py transcript.txt \
  --duration <seconds> --grade
```

- **fail** for every row the script marks FAIL: a banned throat-clearing transition, a re-hook with
  no fact across the seam, more than three negation pivots, hedging above the corpus p90, a stretch
  past 831 seconds with no question reopened, or contrast below the corpus p10.
- A **WARN** row is not a fail. It is inside what the niche does and short of the house target, and
  it goes under "Also seen" unless it is the one thing.
- **n/a** on the sentence-shaped rows when the transcript has no punctuation, which the script
  detects and says. Descript exports are punctuated; a yt-dlp caption track often is not.

**Quote the sentence the script prints, never the count on its own.** The count is the finding and
the sentence is what gets rewritten.

Source: `video-script`, [`references/measuring.md`](../../video-script/references/measuring.md) for
the rules and their thresholds, and
a 627-video corpus for the percentiles they are read against.
 **None of these axes separated a winner from a control**, so a fail here is a retention
finding and never a reach one, and the report must say so where it lands.

---

## Strategy checks

Source: the competitor dossiers. These are the findings that replicated across channels.
Each one names its dossier.

### S1. The title names a specific product

Six channels agree, and it is the cheapest change available. A category word
("AI", "systems", "automation") behaves like naming nothing.

- **fail** if the title names a category rather than a product.
- Source: `jordan-ross.html` (1.93x vs 1.22x), `liam-ottley.html` (1.61x vs
  0.90x, n=264), `chase-ai.html` (0.61x penalty for naming none).

### S2. The artefact is the subject of the frame

Not the face, and not a revenue figure. A face beside the tool is fine; a face
instead of the tool is not.

- **fail** if the thumbnail concept on the video has no artefact in it.
- Source: `ross-harkness.html` (24-video family, zero overlap between the face and
  no-face bands), corrected in `liam-ottley.html` - the rule is positive.

### S3. It teaches a build

The largest and best-replicated effect in the series, and the one that separates
a 7.7x asset from a long video. Teach the tool, not the business.

- **fail** if the video explains how to run an agency rather than how to build the
  thing on screen.
- Source: `liam-ottley.html` (10 instructional at 938 views/day vs 3 non-
  instructional at 82, 53, 241), `michele-torti.html` (tool courses 1,487
  views/day vs agency-business 83, same creator, same year).

### S4. Money-claim framing stays out

Category-dependent: 0.90x on Ottley, 1.29x on Ali Abdaal, who sells an
aspirational life to a general audience. Ours is not that category.

- **fail** if the title or the thumbnail leads on a revenue figure.

### S5. The promise is one the viewer can picture reaching next quarter

$20,000 beat $100,000 by roughly 2x age-adjusted. Matt Gray found it
independently at 11x on an age framing.

- **fail** if the promise addresses the arrived rather than the aspirant.
- Source: the three-run control dossier, and one more channel that replicated it.

### S6. Length is not the variable

Do not recommend "make it longer" or "make it shorter" on its own. The 60-minute
cliff on Ottley is real and belongs to the annual flagship, not to a weekly
upload; everything from 10 to 60 minutes sits within 15% of his median.

- This check never fails a video. It exists to stop the report inventing a length
  recommendation, which is the easiest wrong note to write.

---

## What is deliberately not checked

**Hook craft.** Five channels, a 232x range on identical openings. The hook
governs whether people stay, never how many arrive, so a "your hook was weak"
note has no evidence behind it and does not go in the report.

**Cadence.** A floor, not a strategy. Ross Harkness published every Sunday
without a miss and his rolling median fell by two thirds.

**Shorts.** Settled elsewhere and nothing to do with a long-form take.

---

## The writing score, out of 10

One number, on the front of the report, next to the one thing. It exists so the
ledger can show a line moving across recordings; a report of pass/fail rows cannot
be compared to last month's.

**It scores the writing, never the delivery.** Restarts, truncations, filler
density and pace are all excluded on purpose. The edit removes every one of them,
so counting them here would punish the same fault twice and would move the number
for reasons that have nothing to do with what was written.

Ten lines, one point each. Each scores **1, 0.5 or 0**, and every line names its
evidence: the sentence that earned it, the sentence that lost it, or - for W7, W8
and W9 - the measurement, or the absence itself. W8 and W9 are scored on absence by
design; "nothing to quote" is their whole finding.

A line you cannot evidence either way is left **unscored**, not scored zero, and
the total is printed over the number of lines that were scored.

| # | Line | 1 point | 0.5 | 0 |
| --- | --- | --- | --- | --- |
| W1 | Your own failure, told in full (D2) | The specific agency, the specific number, the specific night, and the viewer is living it | Told, but in one line | Absent, or somebody else's |
| W1b | First person at zero (D9) | Zero, or every survivor does one of the four jobs | One stray outside the four | An opener, a credential or a process about the speaker |
| W2 | One outbound ask, last twenty seconds (D1) | Exactly one, inside the window, one action | One action, drifted early | Two asks, or two actions in the close |
| W3 | Every number has an artefact (D6) | Every figure names the thing that proves it | One figure floats | The only figures are vague quantifiers |
| W4 | No arithmetic on camera (D3) | Nothing derived out loud | One aside | A sustained calculation |
| W5 | Build blocks end on a visible state change (D4) | Every one | More than half | Blocks end on sentences |
| W6 | Camera language outside, mechanics inside (D5) | Clean split | One leak | Mechanics in the stakes or the ask |
| W7 | Word budget (D7) | 3,600-4,200 delivered words | Within 15% of the band | Outside that |
| W8 | The proof block exists | The artefact doing the thing, two configurations from one input | A screenshot | Nothing |
| W9 | The honest limit exists | Who this does not fit, said plainly | Hedged | Nothing |
| W10 | The story gate (D10) | Zero FAIL rows | One FAIL row, or three or more WARNs | Two or more FAIL rows |

W1 to W7 read their verdict straight off the doctrine checks above, so the score
cannot disagree with the table underneath it. W1b shares W1's point: half of it is
the failure, half is the count, so a take that tells the failure well and still opens
on the speaker scores 0.5 rather than 1. W8 and W9 are structural and are the
two most often missing.

**W10 used to be the one judged line and is now computed.** It read "register: short declaratives,
real nouns, contrast pairs", which is what `voice-dna` and `humanizer` already own and what two
reviewers scored two ways. It now reads off D10, which measures the same thing in seven axes with
the sentence attached. The denominator stays 10, so the ledger's `writingScore` column is still
comparable across recordings; what changed is that the last line can no longer be argued into a
different number. Register itself did not stop mattering: it is audited by `humanizer` on the
finished script, where it belongs, rather than scored twice.

**Do not round the total.** 3.0 and 3.5 are different recordings. Print it as
`x.x / 10` and put the ten lines in the report so the number can be argued with.

**The score is not a verdict on the video.** A tour that teaches well can score 3
because it has no proof block and no honest limit, and those are exactly the two
things that would take it to 5 without changing a word of what is already there.
Say that in the report when it applies.
