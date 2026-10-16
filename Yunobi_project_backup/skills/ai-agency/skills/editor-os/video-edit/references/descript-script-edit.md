# Descript Script Edit

Cutting the **script** of an existing composition, and placing the shots on the cut. This is
long-form passes 1 through 3: coach-then-cut, reorder, and rhythm.

## The CLI cuts, and it is the first thing to reach for

No AI credits, no clipboard, no browser.

```bash
cd <the CLI directory>
pnpm descript script <project> <comp>                 # the script, with cuts, speeds, cards, markers
pnpm descript cut <project> <comp> --from "<words>" [--to "<words>"] [--in "<paragraph>"] --dry
pnpm descript restore <project> <comp> "<cut words>"
pnpm descript speed <project> <comp> 1.1 --from "<words>"
pnpm descript verify <project>                        # open it and prove it still draws
pnpm descript undo <project> [steps]                  # the way back when verify refuses
pnpm descript doctor [project] [--fix]
```

It writes the app's own edit: the paragraph SPLITS and the removed half carries `isBlocked: true`, struck through and reversible, snapped to word boundaries off the transcript's alignment. `--dry` prints the seconds and the words before anything is written.

**`--in` names the paragraph, `--nth` names which one in it**, because `--in` narrows and stops. The needle matches case-insensitively as a SUBSTRING, so `--from "So"` can land inside `also` - the `text:` each step reports is the only proof. **A needle that repeats is refused**: `euh`, in fourteen paragraphs, needs `--in "<a phrase of that paragraph>"`. A needle cannot cross a paragraph break, and a phrase reading as one line in `--full` may need `\n` where a paragraph holds a newline.

**ANY editor tab open on the project merges its copy back over the CLI's writes**, and the reverted document reads as healthy: 42 cuts each read back correctly and were all live again on the next dump. **Ask for the project to be closed before a cut loop**, then prove it on a FRESH dump - `pnpm descript doc <project> --out after.json` then `python3 scripts/prove_cuts.py after.json needles.json`, which exits 1 while a needle is still live.

**When the CLI has no verb for what is wanted, the clipboard is the fallback**, not the browser: it carries the EDIT rather than the text, so one paste replaces forty guarded drags and ships cuts as reversible Ignores, run through `scripts/dscript.py`: [pasteboard.md](pasteboard.md).

A pass the CLI cannot do is a verb to write.

## What to cut

**Pass 1 is deterministic and Pass 2 is interpretative**, and that order is the method. The author, 8 Sep 2026: *"a 1st pass with a Python script that's deterministic and a 2nd pass with AI that's a little bit more interpretative. Kind of like the real editing workflow."* Pass 1 enumerates the wreckage of speaking; **pass 2 is a READ, dispatched** to oneSonnet subagent
 over the WHOLE live script, reporting 50 paragraphs at a time so each chunk is applied while it reads on, on the brief in [what-to-cut.md](what-to-cut.md) - no script finds a digression, since one is well-formed by definition.

```bash
python3 scripts/candidates.py doc.json --check needles.json     # pass 1, uncovered and the ratio
python3 scripts/restate.py doc.json --check needles.json        # pass 2 BACKSTOP, never the pass
```

**The last attempt is the keep, always, and it survives whole**: a sentence built from attempt 2's head and attempt 4's tail jumps mid-sentence however clean it reads. `candidates.py` searches the JOINED script for these, because a restart lands in the paragraph AFTER the one it abandons. `restate.py` only scores content-word overlap, and its hit is often a clause inside a sentence worth keeping. **Every sentence and every clause faces one test: delete it, read its two neighbours together, name what the viewer lost.** Nothing lost is a cut. 14-20% goes to pass 1, 22-30% to both. **A candidate isn't a cut.** It flags lists as well as retakes, so pass 1 is read by Claude and written as a `cutspec.py` spec, and `seams.py` checks every join: `python3 scripts/cutspec.py --help` has the method.

**A take with pass 1 done is not part-done; the expensive half has not started.** The retake rule, the method and the ratio table are in [what-to-cut.md](what-to-cut.md). Run both scripts on the finished export too, and repair with a one-line `fix.json`, never one you never wrote.

## Place the b-roll and the layout from the script

**One `edits` pass does the whole dressing, and it is one commit.** `layout apply --split` cuts a
card at a sentence and stamps a look on it; `pin` puts a clip on the timeline at a phrase. Mixed in
one file they dress a cut end to end - 18 splits and 7 clips on one video, where the clipboard
would have been five pastes.

```bash
pnpm descript pin <project> <comp> --media "<clip>" --at "<phrase>" [--to "<phrase>" | --cards 2] --dry
pnpm descript edits <project> <comp> pass.json --dry     # the whole pass, then drop --dry
pnpm descript layer place <project> <comp> <card|all> <layer> --width 0.4 --anchor bottom-right
```

**`--dry` is the verification loop, and `holds` is the number to read**: the seconds the last frame
sits there - a second or two reads as intentional, ten does not, negative means the clip overruns
its slot. **Splits first, then the pins in reverse timeline order.** Two rules are automatic: `pin`
hides the cameras under a FULL-FRAME clip and clears the two transitions bracketing it; the filler
pass cuts sentence-opening `now` / `so`.

**A pin is three coupled objects, so an insert is a state change, not an object drop**: a card at
the in-point carrying the layer and a second at the out-point that does not, and a missed closing
card runs the clip to the end of the video. The object model, `--keep-cameras`, the b-roll clock
and every refusal are in [pins.md](pins.md); what goes wrong when a stamp lands on a script being
cut - name traps, the snapshot that IS the revert, the CTA lockout - is in [layout-pack.md](layout-pack.md), and the layout object model, sounds and text in
[layout-object-model.md](layout-object-model.md).

## Where the shots go: the rhythm decides, not the eye

```bash
python3 scripts/sequence.py audit ~/.descript-clip/current.json   # the grab payload, or a doc.json
python3 scripts/sequence.py plan  ~/.descript-clip/current.json --out pins.json
```

`audit` exits 1 and names the timecodes when the edit misses any of three: a state change every 7s
median, 20-50% of runtime under a full-frame overlay, and no stretch over 12s where nothing changes.
`plan` reads six triggers off the surviving script and comes out as pins with the zoom ladder filled
in, the jump cuts beside them, and every unbound slot printed as `OPEN`. **`plan` is pass 1 of the
shots and has pass 1's blind spot**: a well-formed sentence naming a STRUCTURE with no digit fires
nothing and falls to `zoom`, dead air's default (EA20 came out 29 zooms to 13 graphic slots). The
measurements and the shot read that catches what a pattern cannot are in
[sequencing.md](sequencing.md).

**An OPEN slot is a brief to dispatch, never a line in the summary.** `plan` returns the trigger and
the sentence, which is a written brief. Hand each one to the agent that owns that lane, in the same
turn:

| the slot says | dispatch |
|---|---|
| `motion` on a count, a list or an argument with steps | `motion-design` - Remotion, local, no marginal cost |
| `screen` where the recording exists | place it here; no agent needed |
| a beat that wants a photograph or a material | `broll` for the still |
| a film beat, a meme, a shot that already exists | `broll` |

```bash
python3 scripts/visuals.py brief doc.json --out visuals.txt        # the reader's input
python3 scripts/visuals.py check doc.json briefs.json --plan pins.json
```

`check` resolves each brief verbatim and prints `covered`, `zoom only` or `nothing` against pass 1,
exiting 1 over a 45% zoom share. **`zoom only` is the finding**, and every surviving brief is
dispatched on the table above in the same turn.

## Balance: an average is not a rhythm, and every arrival needs a sound

```bash
pnpm descript doc <project> --out doc.json
python3 scripts/sequence.py balance doc.json      # the dressing minute by minute, and the sound
```

`audit` reads the whole video as one number and passes an edit that is dressed at both ends and
bare in the middle. `balance` reads the distribution and gates on four: **no naked minute** (under
6s of clip, graphic or title and at most one sound), **no silent stretch over 45s**, **80% of
visual arrivals carrying a sound within 0.6s**, and **no fifth of the runtime under 8% of the
dressing**. EC49 passed `audit` within a tenth of a second on the median and failed all four: four
naked minutes, 74% of its runtime with no sound at all, 23% of arrivals heard.

**A naked minute is a brief to dispatch in the same turn**, on the same rule as an `OPEN` slot, and
inside a demo it is a `broll` brief rather than a `motion-design` one: a graphics pipeline
fires where the script argues, and a demo does not argue, it shows. The lane classification, the
chrome trap, and which sound plays on which arrival: [balance.md](balance.md).

**Run `pins.py catalogue` before placing a zoom through the clipboard**: a zoom clones the
prevailing stack, and where no card carries a pin layer every zoom lands as an empty card, which
shipped fourteen blank frames into a finished cut. `pnpm descript layout pace` is both the
placement and the repair then.

## Lint the document before every commit. This is a gate, not a check.

```bash
pnpm descript lint <project>     # every invariant the commit gate runs, without writing
```

**One dangling id makes the whole project unopenable**, and the repair cannot be done from the app
either, because the app will not open it. The gate lives in `CLIs/descript/gate.ts` and runs inside
`commit()`, so an invalid document cannot leave the machine whoever is driving. **A count is not a
validation**: cards, markers, pin scenes and words all matched the known-good state on the document
that would not load. The three invariants and the lockout they came from:
[document-lint.md](document-lint.md).

## Reordering, and closing the breathing room

`descript move <p> <comp> "<first>" --to "<last>" --before "<phrase>"` lifts one block in one
commit, splitting the paragraphs at both edges so only the named words travel; `scripts/arrange.py`
rewrites a whole order on the clipboard when every block moves. Look first for a second pain
recorded after the promise (40:11 to 29:48 on a CRM build), then a block the speaker forgot and
delivered after the sign-off.

**A cut is not finished until the air between the words is out.** The closer is the app's own
`shorten word gap`, never a third Ignore sweep, and it is the LAST step of the cut pass. **`--edges`
closes the long ones**: without it a pause that `borders a cut` is skipped, which is where the
longest holes are, and it still reports success.

```bash
pnpm descript gaps close <project> <comp> --over 0.81 --keep 0.4 --edges   # every gap over 0.8s ends at 0.8s
pnpm descript gaps <project> <comp> --over 0.81                      # the proof: nothing left
python3 scripts/silences.py deadair <export.mp4> doc.json "<comp>" --keep 0.35   # on the render
python3 scripts/beatclock.py doc.json --beat "first words" "last words"   # start, end, duration
```

**The gate is 5% of runtime**, and ours came in at 9.9% and 7.5% against a competitor's 2.2% and
2.6%. A beat's clock comes off the document, never off a subtitle export or the in-page readout:
reading one off an SRT is how a video's clips were timed 203.8s wrong. The reorder mechanics, the
silence gate and the b-roll clock are in [finishing.md](finishing.md) and [pins.md](pins.md).

## Verification

- [ ] `prove_cuts.py` and `seams.py` pass on a FRESH dump (every flag read), and `descript lint` before the commit
- [ ] The cut ratio was measured, and pass 2 ran, not just pass 1
- [ ] `gaps close --over 0.81 --keep 0.4 --edges` ran after the LAST cut, and `gaps --over 0.81` reads back empty
- [ ] Every `OPEN` slot was dispatched in the same turn, never reported as a hole
- [ ] `visuals.py check` ran, and the zoom share came in under 45%
- [ ] `sequence.py balance` ran on the finished document, and every naked minute was dressed
- [ ] Every arrival carries a sound, and no stretch over 45s is silent
- [ ] `descript settings <project>` reads clean: the audio and the look, checked once at the end, on [finishing.md](finishing.md)
