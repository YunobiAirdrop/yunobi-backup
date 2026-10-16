# The sequence: how often to cut, and what to cut to

Read this before writing a `pins.json` by hand, and whenever an edit is "done" but reads flat.
`scripts/sequence.py` implements every number here; the file is the reasoning, the script is the
answer.

## The two measured edits

Both read with `sequence.py audit`, on the speed-adjusted play clock. It takes the clipboard
payload `dscript grab` writes or a `pnpm descript doc` export: the taus, the cards and the pin
tracks are the same structures under two different keys.

| | ES02 · Ops Ceiling | EC51 · Goes Quiet After 45 Days |
|---|---|---|
| runtime | 7:34 | 22:54 |
| jump cuts | 70, one every 6.5s | 123, one every 11.2s |
| state changes | 69, median gap 5.4s | 23, median gap 10.0s |
| full-frame overlays | 20, median 4.7s | 2, median 64.2s |
| coverage | 24% of runtime | 9% of runtime |
| stretches over 12s with a still frame | 6 | 4, one of them 18:47 long |

**ES02 is the standard and EC51 is what it replaced.** The difference is not taste: EC51 holds one
screen recording for nineteen unbroken minutes, which is a screen share with a voice over it. ES02
changes what is on screen every 5.4 seconds and hides the speaker a quarter of the time.

## The gate

`sequence.py audit` exits 1 on any of three, and prints the stretches by timecode:

- **A state change every 7s or better**, median. A state change is a layout card or a clip
  arriving; a jump cut is not one, because the frame is the same frame two words later.
- **20% to 50% of runtime under a full-frame overlay.** Under 20% the video is a face talking.
  Over 50% the viewer stops believing anybody is there.
- **No stretch over 12s where nothing changes at all.** ES02 has six, the worst 29s, and they are
  the six places the edit could still improve. A gate the reference video passes clean is a gate
  measuring nothing.

Run it on the finished cut, before the b-roll pass, and again after.

## What fires a shot, and which one

`sequence.py plan` detects these off the surviving script. The trigger is the evidence; the layout
is the answer to what the sentence cannot say on its own.

| trigger | what fires it | the shot |
|---|---|---|
| `list` | three or more clauses in a row, each under 2.6s, each ending in a comma | one clip per clause, 1.0-1.5s each, full frame. ES02 spends 3:58-4:02 on four: get clients / ship / be happy / more projects |
| `screen` | "this is what it looks like", "an example of", "let me show you" | the screen recording in the screen-beside-portrait look, and a zoom to 200% at the detail |
| `motion` | a quantity or a count in the line: "50 plus agencies", "three pillars", "tens of" | the motion clip full frame, camera in the corner at 0.10 wide |
| `cta` | "the link is down description", "book a call", "it's your decision" | the CTA card |
| `jumpcut` | a dead stretch holds an announcement of what the next sentence will say, under 3.5s | ignore it. The frame breaks AND the video shortens |
| `zoom` | a dead stretch with nothing worth cutting in it | the next step of the ladder, on a sentence start |
| `punch` | a contrastive word opening a sentence: "But", "Now", "Here's why", "Except" | a 1.0x to 1.22x crop as a hard cut, landing on the word's first consonant |

**A dead stretch prefers a jump cut to a zoom.** A zoom breaks the still frame; ignoring an
announcement breaks it and takes the words out at the same time. ES02's worst stretch is 29
seconds from 6:31, and `plan` splits it by ignoring `And one last thing,` at 6:43, which is the
same needle a person writes by hand. Jump cuts land in a `.phrases.json` beside the pins, because
they go through `resolve.py` and `dscript apply` rather than through `--pins`.

**The zoom ladder returns to 100 between steps**: `110, 100, 120, 100, 130, 100`. A zoom pin has no
closing card, so it holds until the next one, and two steps in a row read as a slow drift rather
than as a cut.

**A punch-in is the opposite move to the ladder, and the two must not be confused.** The ladder
drifts and comes back; a punch is a hard cut with zero dead frames on either side, 1.0x to 1.22x,
and it lands on the first consonant of the word that turns the argument. Torn down on 2026-08-29 off
a nineteen-minute reference, mechanism five in that teardown, where it is the cheapest tension
device in the whole file: no graphic, no clip, one crop, and
the sentence that follows arrives already marked as the important one. It is an edit move and it
belongs here rather than in `motion-design`, because Remotion never sees the speaker's own frame.

**The speaker shrinking into a card is the other move from that teardown, and it replaces a cut.**
Full bleed scales down into a rounded glass window over a dark void, so the register changes while
spatial continuity survives, which is what a cut to the same layout throws away.
[`layout-pack.md`](layout-pack.md)'s `speaker bubble` is the applyable form of it. What is not built
is the shrink itself as a recording-background variant, and until it is, applying the layout on a
cut is the available half of the mechanism, not the mechanism.

## The house name carries its own timecode

A motion clip is named `13b [06-41] Each Video Builds A Space Portal.mp4`, and the bracket is the
timecode it was rendered for. `plan` binds a clip to a slot within 25 seconds of its own bracket
and prints the binding, so a set rendered against a script lands on that script without anybody
retyping a time. On EP33 that bound `10 [19-02] Less Than Five Minutes.mov` to 19:02 exactly.

The bracket is a seed, never the anchor. The pin resolves on the **phrase**, because the cut moved
everything after it: ES02's `[01-28]` clip sits at 1:33 in the finished edit and is correct there.

## The run

```bash
C=~/.descript-clip/current.json                     # what `dscript grab` already wrote
python3 scripts/sequence.py audit $C                # what rhythm this cut has
python3 scripts/sequence.py plan $C --out pins.json
# read the table: every OPEN slot is a clip that does not exist yet
python3 scripts/pins.py resolve pins.json           # dry run, refuses on anything it cannot land
python3 scripts/dscript.py apply cuts.json --pins pins.json
python3 scripts/sequence.py audit $C                # grab again first: the gate should pass
```

An `OPEN` slot is the brief for `broll-research` or `motion-design`, with the trigger and the line
already written. Do not fill one with a clip that argues something else to keep a number green.

## What it will not do

- **Invent geometry.** `layout` names a look the video already uses, which `plan` reads back off
  the document. A project where no clip has ever been placed has no look to clone, and the plan
  says so rather than proposing one: drag one clip in, copy again, re-run.
- **Bind a clip that is not on the timeline.** `pins.py` refuses those, and the refusal prints what
  is placeable. `plan` proposes only from the media the payload carries, which is the same set.
- **Decide the coverage number for you on a demo.** A build-along is legitimately 60% screen. Take
  the gate as the question "why is this one different", not as a rule the video has broken.

## What `plan` reads, and how a clip binds to a slot

Moved out of SKILL.md on 31 Aug 2026 to hold it under the 250-line ceiling.

`plan` reads six triggers off the surviving script - a run of short clauses, "this is what it
looks like", a count, the CTA, and a frame that has sat still, which prefers a **jump cut** over a
zoom whenever the stretch holds an announcement worth ignoring. Pins come out with the zoom ladder
filled in and the jump cuts in a `.phrases.json` beside them. A clip whose house name carries its own timecode (`13b [06-41] ...`) binds to the
slot within 25s of that bracket; the rest print as `OPEN`, which is a brief for `broll-research` or
`motion-design`, not a hole to fill with whatever is nearest.

## The two ways a still becomes a clip

Moved out of SKILL.md on 31 Aug 2026 to hold it under the 250-line ceiling.

**A still becomes a clip two ways and both are cheap enough to ship side by side**, which is how a
choice gets made by looking rather than by arguing: `pnpm broll:loop <image>` is DepthFlow parallax,
local, free, 270fps on this machine; a hosted image-to-video model redraws every frame and is the
one to reach for when the beat needs material physics the depth map cannot fake. Generate the
comparison at 480p, because the question at that stage is whether the motion reads.

## The three rhythm thresholds `audit` enforces

Moved out of SKILL.md on 31 Aug 2026 to hold it under the 250-line ceiling.

`audit` exits 1 and names the timecodes when the edit misses any of three: **a state change every
7s** median, **20-50% of runtime under a full-frame overlay**, **no stretch over 12s where nothing
changes**. Measured on ES02 - on screen changes every 5.4s, speaker hidden 24% of the time -
against EC51, which held one screen recording for nineteen unbroken minutes.

`plan` reads six triggers off the surviving script and comes out as pins with the zoom ladder
filled in, the jump cuts in a `.phrases.json` beside them, and every unbound slot printed as `OPEN`.

**Read [`references/sequencing.md`](sequencing.md) before writing a `pins.json` by
hand**, and whenever an edit is finished but reads flat.
[`references/layout-pack.md`](layout-pack.md) is for when the look a beat needs is one
this video has never used, because `pins.py` can only clone a look already in it.
