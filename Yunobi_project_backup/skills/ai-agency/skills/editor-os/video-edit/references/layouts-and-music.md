# Layouts, the zoom ladder, the bed, and taking a clip back off

Read this before stamping a new look, pacing an intro, or when a stamped card renders as a flat colour.

## The closed library and review by exception

One layout library ships to every user, with no per-user config. The picker never invents a layout.

Every layout has a job: talking head full, face plus b-roll, quote card, list, chapter, closer,
insert. The picker matches the beat kind to the job, and only on an ambiguous beat does it say why.

`layout check` runs three rules as code over the finished plan:

- no layout change faster than 4 seconds (`MIN_LAYOUT_SECONDS`)
- no same layout more than 6 beats in a row (`MAX_SAME_LAYOUT_RUN`)
- no layout spent on exactly one beat (`MIN_LAYOUT_USES = 2`)

A beat breaking the first rule is restamped with its neighbor's layout; anything else is flagged.

Nothing is approved beat by beat. `layout sheet` builds one page with one frame per layout change,
and the human pass reads that sheet plus the flagged beats. Frames go in `--frames` as `<beat>.jpg`;
without them the tiles still name their beats.

## A stamp copies the ink in

Applying a layout copies the pack card's layers into your composition and leaves
`templateSource: {projectId, cardId}` as a record of where they came from. Nothing is read from the
pack at render time, so the CLI can't write a look it has never seen.

`layout seed [pack]` takes every card off a pack's own document: one call per pack learned 52 cards
across three packs, where hand-applying had seeded 6 in a month. A pack card carries **no
`templateSource`**: it IS the source, so `harvest`, keyed on that field, walks past it. `layout harvest
<project>` is still the road for a card no pack publishes any more, and a pack card outranks a
harvested copy in `merge`, because a copy may have been thinned.

**A stamp brings its own media.** The gradient behind a title, the CTA movie, the font a text layer
uses: each is copied in as a new mediaRef around the same `assetGuid`, filed under `_assets` or
`_fonts`, once however many cards ask for it.

**A `--with` slot is marked on the tau, never guessed from the name.** The pack writes
`visual: { type: "placeholder" }` on every empty picture box, the only honest test: `Title` and
`Subtitle` also draw no media, while `Gradient`, `Captions` and the CTA movies draw media nobody
replaces. Naming rules got `Camera/Subtext` asking for three files it has no use for.

**A picture layer needs a track as well as a composition.** Every camera card has a layer drawing
the speaker; the stamp has to point it at the composition it landed in AND at the `sequenceSceneId`
of the track that composition cuts from. Miss the second half and the layer draws nothing, so the
card renders as **a flat rectangle of its own background colour** - navy, on the cards carrying a
`solidColor`. `apply` writes the track id on every picture layer and refuses a camera card outright
when the composition has no sequence. A card with two picture layers (`Large Face + Screen`) gets
the same track on both and its second one still has to be set by hand.

## What every card is called

**A card's name IS its marker**, in Title Case, saying what is on the frame: `Cam 120`,
`Screen + Square`, `Text Behind Large`, `Speaker Bubble + Media`. `card rename` writes the picker
name, the script marker and the family in one go, and writes a marker where the card had none.

A **family** only where cards are variants of one thing (`camera`, `screen`, `text`, `clip`, `outro`),
because it collapses them under one tile. A card that stands alone takes `--type none` and gets its
own tile: the five Motion cards, the insert, the five Brand ones.

**Inside a card**: every text line is `Text 1`, `Text 2`... in reading order, an empty picture box
is `Media`, a transcript line is `Caption`. The pin's name is the slot `--say` fills, so two pins of
one name make the second unfillable.

`card space` lays one card per paragraph and carries each marker with its card. Run it after any
card is added or merged, then `layout publish` and `layout sync`.

## Which pack, and the ladder

**`Brand Layouts` is the pack. Read the manifest before choosing a card, never the library.**
`pnpm descript layout sync` re-reads every pack from scratch and writes
`CLIs/descript/layout-packs.json`: each card's group, its family, its media slots, the tracks it
draws and whether the picker still offers it. He edits the packs, and `layout seed` alone can't carry an edit through: it reports `alreadyHeld`
and keeps the old copy. Sync first, then
the pack script
 redraws the board and the renderer's numbers off
the same file.

**Editor OS ships a neutral copy of the pack.** No brand cards, every colour a grey, and the
previews draw it when `EDITOR_OS_PACK` isn't set. A camera box with no footage is drawn the way
Descript draws it: near-black, the card's own corner radius, a small layout icon and the card's
picker name ("Cam 130"), all through one function in the review package.

**`CAM-green` is three layers, and whether it draws decides everything.** The author, 7 Sep 2026: *"The
purpose of having a green screen overlay is to be able to display stuff like text or an image behind
my face while making sure that the text is also there in the background. So there is three layers:
the background, the image or text, and then my body."* The keyed body sits ON TOP, which is why the
pack stacks it above the text.

**It is the same camera twice.** `CAM-green` is a second track cut from the SAME take with the key
applied, which is why EC49's sequence reads CAM, CAM GS, MIC, SCREEN. It exists only where the take
was shot against green: EA20 was shot in the room, so it has three tracks and no keyed one, a
recording decision and not a forgotten setup. Check the take before concluding a track is missing:
`pnpm descript pull <project> IMG_ --seconds 4` and pull a frame.

So the same track name means two different things. On 22 of the pack's 30 cards the `CAM-green`
layer is HIDDEN - a spare the card carries and never draws. On a take with no key, `apply` drops
that spare. It used to point it at CAM instead, which put two CAM layers on every card: that's the
doubled camera the author saw on the CRM cut (22 Sep 2026). The pack's `CAM-green` matches a recording's
`CAM GS` too. Reading the missing track as a refusal once sent a whole 26-minute video onto a second
pack. On the other 8 it is VISIBLE and IS the effect: `Text Behind Large`, `Text Behind 2 Lines`,
`Text 4 Lines`, `Text Left 2 Lines`, `Text + Card`, `Image Behind + Logo`, `Shorts Bottom`,
`Shorts Green Screen`. Falling back there fills the frame with the un-keyed camera and hides the
card's own text, so `apply` refuses those outright on a project with no keyed track.

**Every keyed layer lines up with the camera under it to 0.05px**, and it has to: a body drawn twice
at two offsets reads as a ghost edge. `contentPosition` is the centre of the footage inside the box,
not a share of the overflow, so frame x = box left + cp.x × box width − footage width / 2.
`Shorts Bottom` was 8px out until 22 Sep 2026. The screen cards sit on whole pixels: 120px margins
and gaps on `Portrait Small` and `Portrait Large`, 60px on `Square` with its cam 40px off both edges. After
any pack edit, run `layout publish` then `layout sync`. A re-read now replaces the held geometry.

A drive holds other packs, usually stale: `layout sync` names any deleted pack.

A zoom is one layer: `contentScale`, with a `contentPosition` that walks down to hold the face as
the frame tightens.

| Card | Scale | Content y |
| --- | --- | --- |
| `Camera/Zoom 100%` | 1.00 | 0.500 |
| `Camera/Zoom 115%` | 1.15 | 0.575 |
| `Camera/Zoom 130%` | 1.30 | 0.650 |
| `Camera/Zoom 145%` | 1.45 | 0.664 |
| `Zoom S (110%)` | 1.10 | 0.500 |
| `Zoom M (130%)` | 1.30 | 0.547 |
| `Agency Master` | 1.00 | 0.431, on a branded background |

Cycle a ladder of four to eight steps so it breathes in and back out rather than jumping wide to
tightest, and **let it reach 145% once a stretch**, on the claim, not the setup. A ladder that never
leaves 100-130 is as flat as none, only busier.

## The house grammar, measured off three finished edits

Read on 8 Sep 2026 with `layout cards` off EC49 (19:00, 154 cards), EA20 MCP (20:02, 86 cards) and
ES02 (7:39, 95 cards), all cut by hand in the app. Which card goes on which stretch is what the
finished edits do, not taste:

| The stretch | The card | Count on EC49 / EA20 |
| --- | --- | --- |
| 0:00, the first sentence | `Camera/Intro Zoom` | 1 / 1 |
| him talking, full frame | `Camera/Cam 100 · 110 · 120 · 130`, one card per beat, 3-6s each | 55 / 32 |
| the demo, default | `Screen/Screen + Portrait Small` | 38 / 30 |
| the demo, a tall interface | `Screen/Screen + Portrait Large` | 13 / 1 |
| the demo, a wide interface | `Screen/Screen + Square` | 9 / 3 |
| a list he recites | `Text/Text Left 2 Lines`, `Text 4 Lines`, `Text Behind Large`, `Text Small Right`, `Text Left + Right`, `Text + Card`, `Speaker Top`, `Speaker + Text` | 19 / 14 |
| a real product named | `Inserts/Image Behind + Logo` | 0 / 2 |
| the close, the two asks | `CTAs/CTA - Call`, then `CTAs/CTA - Skool` | 0 / 2 |
| a lesson sold under a brand | `ClickUp Master/Agency Master` (ES02: 47 of 95 cards) | - |

Two things the count says. **The demo is one card family and the camera is a ladder**: a screen
stretch changes card only when the interface changes shape, a camera stretch on every beat. **A text
card is the list, not the sentence**: every `Text/*` stamp sits on a line that enumerates. What none of the three did is put a sound on more than 27% of their arrivals, which is
the lane `sequence.py balance` was written to catch.

### Four cards added 25 Sep 2026, before any edit used them

No finished edit has counted these yet. What each is for, and the `--say` order `layout lines` prints:

| The stretch | The card | `--say` |
| --- | --- | --- |
| a guest or him introduced by name | `Text/Lower Third` | `name\|role` |
| a section starts | `Text/Chapter Card` | `number\|title`, e.g. `03\|Where the margin goes` |
| a list he builds step by step | `Text/Checklist Build` | four lines, each `✓ ...`; three hides the fourth |
| a makeover shown side by side | `Screen/Before + After` | `AFTER\|BEFORE`, **after first** |

- **Before + After's text order follows the layer stack, not the frame.** The first `--say` line is
  the right-hand label. Its left frame is the `SCREEN` track, and the right one is an empty frame he
  drops the result into.
- **Checklist Build draws `CAM-green` visibly**, like `Text 4 Lines` it was cut from, so `apply`
  refuses it on a take with no keyed track.
- **Its lines slide in from the left, letter by letter**, 0.5s apart.
  `text animate <p> <comp> <card> "Text 1,Text 2" --direction right --by Character` sets that on any
  text layer. `--out` sets the Animation out, and `--effect flicker` swaps the slide for a flicker.
  It writes the pinned scene's `headTransition` or `tailTransition`, where the app keeps them: 0° is
  the → arrow, 270° is ↑. `descript effects` lists the five transition names, and the Editing OS
  board prints every layer's in and out in those same names.
- **Chapter Card frosts the whole frame** with its glass layer, so the title reads over the face.
  Lower Third keeps the camera clear and sits in the bottom-left 96px from both edges.

## Pacing beats stamping

`layout pace <p> <comp> --ladder a,b,c --from --to` puts one card on every beat of a stretch and
cycles the ladder across them, restamping the card already standing on a beat and cutting one where
none stands. A beat is a **tau**, which in these scripts is a paragraph rather than a word, so it
lands one card per thought; `--min` (2s default) skips a beat too short to read as emphasis rather
than flashing a frame. It is the cheapest cut in the edit, and it was missing from a video where 29 of 37 cards
carried one identical framing for eleven minutes.

`apply` restamps the card the anchor falls inside, since Descript has already cut the composition
into cards. `--split` cuts a new card instead, the rarer verb.

Read the result back from the **layers**, never from the card list: a card can carry a layout and
still draw nothing.

## The bed

Level, ducking, loop and the false-positive guard: [audio-and-tracks.md](audio-and-tracks.md), "The
music bed". Pass 4 picks the track from the brand's music style ([descript-projects.md](descript-projects.md)).

## Taking a clip back off a card: the transparent plate

Nothing removes a pin outright (`media swap` repoints, `rm` deletes media). The transparent-plate
workaround, its ffmpeg command and the swap-by-id trap are in [pins.md](pins.md), "The transparent plate".

