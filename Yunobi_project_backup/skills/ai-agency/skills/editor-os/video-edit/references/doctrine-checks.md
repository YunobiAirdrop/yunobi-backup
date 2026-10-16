# Doctrine checks

Ask whether the take obeyed the rules the script was written under. Strategy checks, and the
`pass`/`fail`/`n/a` contract both families share, are in [checks.md](checks.md).

Source: the `video-script` skill, and a three-run control read off one
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

In `video-script`, [`references/writing-the-script.md`](~/Studio/vibe-kit/ai-doc/skills/video/scripting/video-script/references/writing-the-script.md)
section "Camera language on the outside, mechanics on the inside," the rule and the block-split.

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

The opening 30 seconds belong to `video-script`'s hook branch and its wording is load-bearing.
The script writes those lines out in full inside quotes for that reason.

- **fail** if the quoted cold-open lines were paraphrased on camera.
- **n/a** if the take opened on a different hook that was then kept, note it, do
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

Source: `video-script`, [`references/measuring.md`](~/Studio/vibe-kit/ai-doc/skills/video/scripting/video-script/references/measuring.md) for
the rules and their thresholds, and
a 627-video corpus for the percentiles they are read against.
 **None of these axes separated a winner from a control**, so a fail here is a retention
finding and never a reach one, and the report must say so where it lands.
