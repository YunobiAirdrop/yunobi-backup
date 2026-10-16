# The sequence: how often to cut, and what to cut to

Read this before writing a `pins.json` by hand, and whenever an edit is "done" but reads flat.
`scripts/sequence.py` implements every number here; the file is the reasoning, the script is the
answer.

## The two measured edits

Both read with `sequence.py audit`, on the speed-adjusted play clock. It takes the clipboard
payload `dscript grab` writes or a `pnpm descript doc` export: the taus, the cards and the pin
tracks are the same structures under two different keys.

| | ES02 · Ops Ceiling | EC51 · CRM Client Retention |
|---|---|---|
| runtime | 7:34 | 22:54 |
| jump cuts | 70, one every 6.5s | 123, one every 11.2s |
| state changes | 69, median gap 5.4s | 23, median gap 10.0s |
| full-frame overlays | 20, median 4.7s | 2, median 64.2s |
| coverage | 24% of runtime | 9% of runtime |
| stretches over 12s with a still frame | 6 | 4, one of them 18:47 long |

**ES02 is the standard and EC51 is what it replaced.** EC51 holds one screen recording for
nineteen unbroken minutes, a screen share with a voice over it; ES02 changes what is on screen
every 5.4 seconds and hides the speaker a quarter of the time.

## The gate

`sequence.py audit` exits 1 on any of three, and prints the stretches by timecode:

- **A state change every 7s or better**, median. A state change is a layout card or a clip
  arriving; a jump cut is not one, because the frame is the same frame two words later.
- **20% to 50% of runtime under a full-frame overlay.** Under 20% the video is a face talking.
  Over 50% the viewer stops believing anybody is there.
- **No stretch over 12s where nothing changes at all.** ES02 has six, the worst 29s: the six
  places the edit could still improve. Run it on the finished cut, before the b-roll pass, and
  again after.

## What fires a shot, and which one

`sequence.py plan` detects these off the surviving script. The trigger is the evidence; the layout
is the answer to what the sentence cannot say on its own.

| trigger | what fires it | the shot |
|---|---|---|
| `list` | three or more clauses in a row, each under 2.6s, each ending in a comma | one clip per clause, 1.0-1.5s each, full frame |
| `screen` | "this is what it looks like", "an example of", "let me show you" | the screen recording in the screen-beside-portrait look, and a zoom to 200% at the detail |
| `motion` | a quantity or a count in the line: "50 plus agencies", "three pillars", "tens of" | the motion clip full frame, camera in the corner at 0.10 wide |
| `cta` | "the link is down description", "book a call", "it's your decision" | the CTA card |
| `jumpcut` | a dead stretch holds an announcement of what the next sentence will say, under 3.5s | ignore it. The frame breaks AND the video shortens |
| `zoom` | a dead stretch with nothing worth cutting in it | the next step of the ladder, on a sentence start |
| `punch` | a contrastive word opening a sentence: "But", "Now", "Here's why", "Except" | a 1.0x to 1.22x crop as a hard cut, landing on the word's first consonant |

**A dead stretch prefers a jump cut to a zoom.** A zoom breaks the still frame; ignoring an
announcement breaks it and shortens the video at the same time. ES02's worst stretch is 29 seconds
from 6:31, and `plan` splits it by ignoring `And one last thing,` at 6:43, the same needle a person
writes by hand. Jump cuts land in a `.phrases.json` beside the pins, through `resolve.py` and
`dscript apply` rather than `--pins`.

**The zoom ladder returns to 100 between steps**: `110, 100, 120, 100, 130, 100`. A zoom pin has no
closing card, so two steps in a row read as a slow drift rather than a cut.

**A punch-in is the opposite move to the ladder.** The ladder drifts and comes back; a punch is a
hard cut with zero dead frames on either side, 1.0x to 1.22x, landing on the first consonant of the
word that turns the argument. Torn down 2026-08-29 off a nineteen-minute reference (the Tension
chapter, mechanism five): the cheapest tension
device in the whole file, no graphic, no clip, one crop, and the sentence that follows arrives
already marked as the important one. It belongs here rather than in `motion-design`, because
Remotion never sees the speaker's own frame.

**The speaker shrinking into a card is the other move from that teardown, and it replaces a cut.**
Full bleed scales down into a rounded glass window over a dark void, so the register changes while
spatial continuity survives - [`layout-pack.md`](layout-pack.md)'s `speaker bubble` applies it.

## The house name carries its own timecode

A motion clip is named `13b [06-41] Each Video Builds A Space Portal.mp4`, the bracket its render
timecode. `plan` binds a clip to a slot within 25 seconds of its own bracket and prints the
binding, so a set rendered against a script lands on that script without anybody retyping a time.
On EP33 that bound `10 [19-02] Less Than Five Minutes.mov` to 19:02 exactly. The bracket is a seed,
never the anchor: the pin resolves on the **phrase**, because the cut moved everything after it
(ES02's `[01-28]` clip sits at 1:33 in the finished edit and is correct there).

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

An `OPEN` slot is the brief for `broll` or `motion-design`, trigger and line already
written. Do not fill one with a clip that argues something else to keep a number green.

## What it will not do

- **Invent geometry.** `layout` names a look the video already uses. A project where no clip has
  ever been placed has no look to clone: drag one clip in, copy again, re-run.
- **Bind a clip that is not on the timeline.** `pins.py` refuses those and prints what is
  placeable; `plan` proposes only from the media the payload carries.
- **Decide the coverage number for you on a demo.** A build-along is legitimately 60% screen. Take
  the gate as "why is this one different", not as a rule the video has broken.

## The two ways a still becomes a clip

A still becomes a clip two ways, cheap enough to ship side by side so a choice gets made by
looking rather than arguing: `pnpm broll:loop <image>` is DepthFlow parallax, local, free, 270fps
on this machine; a hosted image-to-video model redraws every frame for material physics the depth
map cannot fake. Generate the comparison at 480p to check whether the motion reads.

## What a pattern cannot see, and the shot read that follows

`plan` is pass 1 of the shots, and it has pass 1 of the cuts' blind spot: all six triggers above
are surface patterns, so a well-formed sentence naming a STRUCTURE with no digit fires nothing and
falls to `zoom`, what dead air gets. EA20 came out 29 zooms to 13 graphic slots. This runs after
`plan`, never instead of it: the pattern finds what the read below cannot, and the read finds what
no pattern can see.

```bash
python3 scripts/visuals.py brief doc.json --out visuals.txt        # the reader's input
python3 scripts/visuals.py check doc.json briefs.json --plan pins.json
```

**One agent, on Sonnet, over the WHOLE script, never split**: the second time a video draws the
same structure it should inherit the first frame rather than open a new one, invisible to a reader
holding half the script. Hand the reader the plan's own table too, so it can say `covered`. Paste
the block below exactly, substituting the file path.

---

Read `<path to visuals.txt>`. It is the surviving script of a cut video, one paragraph per line,
each prefixed with its index in square brackets and the timecode it plays at.

Your job is to find the beats that should be SHOWN and are currently only being said. A previous,
deterministic pass already found every line carrying a number, a demonstrative ("this is what it
looks like"), a contrastive opener, and every stretch of dead air. Do not report those. Find the
rest.

THE TEST, and a beat has to pass it whole: **what would a viewer know after this clip that the
sentence did not tell them?** There are exactly four answers, and a beat that gives none of them
stays on his face, because his face is more interesting than any rectangle.

1. **A quantity made comparable.** The read states arithmetic the listener has to do.
2. **A consequence the read leaves implicit.** He says do the thing; he does not say what it costs
   or returns.
3. **A structure that has no name yet.** Two things joined, a loop that closes, three layers, a
   hand-off. Speech is serial and a structure is not, so the frame holds at once what the sentence
   can only spell out in order.
4. **A recognition.** A real product, a real screen, a real word. The moment a viewer sees a tool
   they have open in another tab, the video stops being about the topic and starts being about them.

Report a beat ONLY when:

- the sentence would still make sense with the clip muted, and the clip would still say something
  with the sentence muted - if the graphic is the sentence in shapes, that is Mayer's redundancy
  and it is worse than no clip
- the thing to draw is CONCRETE. "Automation saves time" is a topic; "your project tool talking to
  your documentation tool" is a drawing
- it is not a screen the recording already shows. A graphic over real evidence argues with it

Do NOT report:

- a beat inside a live demonstration, where the screen IS the proof
- a line whose visual is a film beat, a meme or archive footage - that is a different lane
- more than one beat per 30 seconds of script. A set of clips is a rhythm, not a coverage number

OUTPUT. A JSON array, nothing else, no prose around it. Each element is an object:

```json
{"i": 115,
 "line": "So that ClickUp, your project tool, could talk to Notion, your documentation tool.",
 "adds": "structure",
 "shows": "The two real marks with the link drawn between them, and the thing that travels it."}
```

- `i` is the paragraph index in square brackets
- `line` is a VERBATIM substring of that one paragraph, copied character for character
- `adds` is exactly one of `quantity`, `consequence`, `structure`, `recognition`
- `shows` is one sentence naming what is in the frame. Not a style, not a template id: the picker
  is the motion agent's job and it owns the roster
- 8 to 20 entries for a twenty-minute video. Be strict: a marginal beat is a clip nobody needed

Return only the JSON array.

---

**Judging what comes back.** `visuals.py check` resolves every brief against the live script and
drops, never repairs, one that does not land verbatim, then says per brief whether pass 1 already
put a graphic there (`covered`), put a zoom step there (`zoom only`), or proposed nothing.

**`zoom only` is the finding this whole pass exists for.** A zoom is what `plan` emits for dead
air, so a beat that deserved a graphic and got a ladder step is the failure being measured, not a
near miss; the check exits 1 when zoom steps are over 45% of the plan.

Then dispatch every resolved brief to a lane in the same turn, on the table in `SKILL.md`:
`motion-design` owns anything drawn, `broll` anything found, a screen the recording
already holds needs no agent.
