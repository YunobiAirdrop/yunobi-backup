# Balance: where the dressing sits, and whether anybody heard it

`audit` reads a video as one number. This reads its distribution. Run both; they catch different
failures, and the second one is the failure a viewer actually meets.

```bash
pnpm descript doc <project> --out doc.json     # balance needs the real document, not the clipboard
python3 scripts/sequence.py balance doc.json
```

## Why an average is not a rhythm

EC49, an 18:50 ClickUp build, measured on 2026-09-07:

| | `audit` says | `balance` says |
|---|---|---|
| state changes | 122, median gap **7.1s** against a gate of 7 | 4 minutes with nothing on screen at all |
| coverage | 20% full-frame, inside the 20-50% band | the thinnest fifth holds **7%** of the dressing |
| sound | not measured | **74% of the runtime carries no sound**, longest silence 2:50 |

Nothing in the first column is wrong. The edit really does change state every seven seconds on
average, and the average is made of seventeen state changes in minute one and three in minute
sixteen. **An edit whose median passes and whose middle four minutes are bare is not an edit with
a rhythm; it is two edits joined.**

## The baseline: three finished edits, measured 8 Sep 2026

| | ES02 7:39 | EC49 19:00 | EA20 20:02 |
|---|---|---|---|
| cards | 95 | 154 | 86 |
| state change, median gap | **4.6s** | 7.1s | 7.8s |
| full-frame coverage | **28%** | 22% | 15% |
| stretches over 12s with nothing changing | 6 | 19 | 23 |
| naked minutes | **0** | 2 | 10 |
| arrivals carrying a sound | 10% | 27% | 27% |
| longest silence | 110s | 163s | **789s** |

The seven-minute lesson is the only one that passes the rhythm gates, and none of the three
passes the sound gate. The ten naked minutes on EA20 are its demo, 4:00 to 16:00: every one of its
eleven rendered clips sits before 3:30 or after 18:00. The fix is the demo lane below, not more
graphics at the ends.

## The four gates

- **No naked minute.** A minute carrying under 6s of clip, graphic or title AND at most one sound.
- **No silent stretch over 45s.** The density law it comes from is the sound section below. The
  **median** gap is deliberately not the gate: EC49's median is 7.1s and passes while three
  quarters of the video is silent, because its 44 sounds arrive in two bursts.
- **80% of arrivals carry a sound within 0.6s.** A graphic that lands in silence is a graphic the
  viewer notices a beat late. EC49 runs 23%.
- **No fifth of the runtime under 8% of the dressing.** An even spread is 20% each, so 8% still
  allows one section to carry two and a half times another. EC49's middle fifth holds 7%.

A gate is a question, not a verdict: a build-along is legitimately 60% screen, and the answer to
"why is this one different" can be a good one. What it may not be is "nobody looked".

## The three lanes, and the chrome that is not one of them

`balance` classifies each pinned scene off the document rather than off its name:

| lane | how it is known | EC49 |
|---|---|---|
| `sound` | its media has audio and no picture | 44 |
| `title` | its scene carries no media at all: text is drawn on the card | 44s, 4% |
| `graphic` | a clip whose house name carries the `[mm-ss]` bracket it was rendered for | 210s, 19% |
| `footage` | any other clip or still | 91s, 8% |

**`chrome` is the fifth lane and it is what makes the count honest.** A background plate and a
progress bar are pinned scenes like any other, and the first run of this counted them: EC49 came
back at **199% title and 83% footage**, because a grid plate ran under all eighteen minutes and a
progress HUD sat on 129 cards. So a scene earns a lane only where it sits **above the camera** on
some card and draws wider than `CHROME_W` (0.15 frame widths).

## The mix, and the lane that goes missing

EC49's 91 seconds of footage sit in minutes 0-2 and 14-18. **The twelve minutes of demonstration
between them contain no footage at all** - every dressed second there is a rendered graphic. That
is the shape a graphics pipeline produces when it is the only pipeline anybody reaches for:
`motion-design` renders to a script, so it fires where the script argues, and the demo body does
not argue, it shows.

So a naked minute inside a demo is a `broll` brief, not a `motion-design` one, and the
sound lane is usually the cheaper half of the fix, below.

**A naked minute is a brief to dispatch in the same turn, never a line in the summary**, on the
same rule as an `OPEN` slot in [`sequencing.md`](sequencing.md).

## The one gate a screen demonstration cannot pass, and should not

`the thinnest fifth holds N% of the dressing` asks for clip, graphic or title spread across the
runtime. A video that is one continuous demonstration has none in its middle three fifths by
construction, and buying that number costs the thing the video is. EA20, 7 Sep 2026, closed every
other gate - 0 naked minutes, no silent stretch, 88% of arrivals heard, 121 sounds - and left this
one failing on purpose, with 3:33 to 22:03 dressed by **sound and card rhythm alone**.

That is the trade to make: pace the demo so a framing never holds past ~10 seconds, put a whoosh on
every arrival, and let the coverage number stay low.

## Sound on the cut: which sound, how many, and where the silence is

A sound effect is a pin no layer draws, at gain 0.4; [`layout-pack.md`](layout-pack.md) owns that
object and the `--sound` flag that writes it. The levels, the -14 LUFS master and the density law
are measured in `editor-os/motion-design/references/sound-layout.md`. This is the grammar:
what plays on what, and how a cut is checked for the sound it never got.

**Sound is the third hook, and it is the one that gets skipped.** A creator teaching this on
TikTok, `@kienobimedia`, 2026: *"Everyone obsesses over the words and the visuals, but sound is
the third hook most creators skip. A reveal, a cut, a transition all hit harder when audio carries
the motion."* That is checkable, so it became the 80%-of-arrivals gate above rather than a
paragraph.

### What plays on what

Read off EC49's finished 18:50 cut, 2026-09-07, where the pairing is consistent enough to be a
rule. The right column is the clean kit's own voice for the same event:

| the edit does this | Descript stock, as used | the clean kit |
|---|---|---|
| a cutaway or a graphic arrives | `Whip Low Whoosh` - 12 of 16 graphics, 5 of 5 cutaways | `whoosh` |
| a title or a line of text arrives | `Text Readout Digital` - 20 of them | `ui` |
| a line **replaces** the line before it | `Designed Transitions Shuffle …Flicker 01` | `ui`, lower gain |
| a section ends and another starts | `Deep Low Whoosh` | `impact`, or `riser` into the cut |
| the video opens | `Fast Hi-Tech Whoosh 3` | `riser` + `impact` |
| a wide shot is held | `Atmospheric Swish Wind Swoosh`, gain 0.30 | `swell` |
| a mouse is clicked on a screen recording | *never used* | `click` |
| typing on a screen recording | *never used* | `type-2s` / `type-4s` |

**The last two rows are the finding.** EC49 carries twelve unbroken minutes of screen
demonstration, and not one click or keystroke is voiced in it - those twelve minutes are also
where all four of its naked minutes are. The kit has held both voices since 2026-08-27.

### How many, and the gate that is not the average

ES02 places **three a minute** (`layout-pack.md` counts its 22). EC49's finished cut places 2.3 a
minute, which reads fine as an average and is not what it does:

```
sounds 44, median gap 7.1s, 74% of the runtime carries none
  no sound at all (over 45s):
    4:12 -> 7:02  (170s)
    7:32 -> 10:09  (157s)
```

Forty-four sounds arriving in two bursts is a designed opener, a designed close, and a silent
middle. So the gate is **no stretch over 45 seconds with no sound at all**, and the median is
printed beside it as the number that lied.

### Placing them

One `edits` pass, sounds mixed in beside the splits and the clips - a sound written in a separate
pass is a sound written last and therefore not at all.

```bash
pnpm descript pin <project> <comp> --media "Whip Low Whoosh" --at "<phrase>" --sound --gain 0.4
python3 scripts/sequence.py balance doc.json      # before, to find the silence; after, to prove it
```

Two rules from `sound-layout.md` that a Descript pass breaks most often: **on the frame, never one
frame early**, and **never two cuts in a row** - if two consecutive cuts both got a whoosh, delete
one. A third belongs here: **a sound is not a fix for a naked minute on its own.** It raises a
NAKED row to `thin`, and the minute still needs something to look at.
