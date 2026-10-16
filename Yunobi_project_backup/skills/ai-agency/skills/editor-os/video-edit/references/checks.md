# The checks

Two families. Doctrine checks, in [doctrine-checks.md](doctrine-checks.md), ask whether the take
obeyed the rules the script was written under. Strategy checks, below, ask whether the video, as
recorded, still competes.

Every check returns `pass`, `fail` or `n/a`, and every `fail` carries the file it
came from. A check that cannot name its source is an opinion and does not go in
the report.

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

**Cadence.** In `video-script`, [`references/shorts-structures.md`](~/Studio/vibe-kit/ai-doc/skills/video/scripting/video-script/references/shorts-structures.md),
why cadence is a floor, not a strategy.

**Shorts.** Settled elsewhere and nothing to do with a long-form take.

---

## The writing score, out of 10

One number, on the front of the report, next to the one thing: it lets the ledger show a line
moving across recordings, which pass/fail rows cannot.

**It scores the writing, never the delivery.** Restarts, truncations, filler density and pace
are excluded on purpose: the edit removes all of them, so counting them here would punish the
same fault twice and move the number for reasons that have nothing to do with what was written.

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

W1 to W7 read their verdict straight off the doctrine checks in
[doctrine-checks.md](doctrine-checks.md), so the score cannot disagree with the table underneath
it. W1b shares W1's point: half is the failure, half is the count, so a take that tells the
failure well but still opens on the speaker scores 0.5, not 1. W8 and W9 are structural, and the
two most often missing.

**W10 used to be the judged line and is now computed.** It read "register: short declaratives,
real nouns, contrast pairs," which `humanizer` already owns and which two reviewers scored two
ways. It now reads off D10, measuring the same thing in seven axes with the sentence attached. The
denominator stays 10, so `writingScore` stays comparable across recordings; what changed is that
the last line can no longer be argued into a different number. Register still matters:
`humanizer` audits it on the finished script, not scored twice here.

**Do not round the total.** 3.0 and 3.5 are different recordings. Print it as
`x.x / 10` and put the ten lines in the report so the number can be argued with.

**The score is not a verdict on the video.** A tour that teaches well can score 3
because it has no proof block and no honest limit, and those are exactly the two
things that would take it to 5 without changing a word of what is already there.
Say that in the report when it applies.
