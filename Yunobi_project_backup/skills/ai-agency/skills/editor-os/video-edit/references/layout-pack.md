# Stamping a layout onto a cut

How a stamp works, which packs exist and the zoom ladder belong to [descript-projects.md](descript-projects.md). This is
what goes wrong when one lands on a script that is being cut. What a layout IS, its object model
and its sounds are in [`layout-object-model.md`](layout-object-model.md).

```bash
pnpm descript layout list                                   # every card, and which pack seeded each
pnpm descript layout apply <project> <comp> --use "Screen + Portrait Small" --at "the moment delivery" \
                                            --with "RAW IPAD.MP4"
pnpm descript layout pace  <project> <comp> --to 0:40 --ladder "cam-100,zoom-110,cam-100,zoom-130"
pnpm descript layout seed                                   # a new card in the pack, into the library
```

**Which of the two places a look comes from.** `pins.py --pins` clones a layout **already in the
composition**, so it can only ask for a look the video already uses, and it places media in the
same paste as the cut. `pnpm descript layout apply` stamps a look the video has **never** used, out
of the pack, and brings the stamp's own assets with it. Reach for the CLI when the look is new to
this video and for `pins.py` when it is not.

## Two name traps, both of which read as a missing layout

`layouts.json` keeps the name a card was **harvested under**, and renaming the card in the pack does
not follow. So `layout list` prints the pack's current name while `pick()` resolves the stored one:
`Cam 100` / `Cam 110` / `Cam 120` / `Cam 130` are seeded as `Camera/cam-100`, `zoom-110`, `zoom-120`,
`zoom-130`, and `Intro Zoom` is `Camera/woosh-zoom`. `--use "Cam 100"` answers *"No layout called
... is seeded"*, which reads like a card that needs applying once by hand and is not.

The second is the opposite: a name that exists in **two** packs refuses as ambiguous. `Screen +
Portrait Small`, `Screen + Square` and `Screen + Portrait Large` are all seeded twice. `pick()` matches a
`cardId` prefix, so pass the 8 characters `layout list` already prints - `b04ec873`, `5c57d7be`,
`cf302bc5`.

Both are one lookup away: read the id off `layout list` and pass that, rather than the name.

## Scope a pace to the register, never to the runtime

`pace` cycles one ladder, so pacing a whole video puts the camera over a screen tour and the screen
over a talking head. Time the section boundaries first with `beatclock.py`, then run it once per
register. EC49, 24:04, on 2026-08-31:

| stretch | ladder | beats |
|---|---|---|
| intro 0:00-3:30 | `cam-100,zoom-110,cam-100,zoom-130` | 20 |
| tour 3:30-21:05 | `b04ec873,cf302bc5,b04ec873,5c57d7be`, `--min 6` | 45 |
| outro 21:05-end | `cam-100,zoom-110,cam-100,zoom-120` | 10 |

75 beats took state changes from 16 to 76 and the median gap from 50.4s to 13.6s. `--min 6` on the
tour is what stops a short clause taking a card of its own; on a build-along the screen is already
the changing element, so ~23s between cards is right and the 7s gate is asking a different question.

## Snapshot before every layout write, because the snapshot IS the revert

`pnpm descript doc <project> --out doc.json` writes exactly `state.doc`, and `commit(id, head, doc,
…)` diffs whatever you hand it against the live head. So a saved document is a complete, provable
undo, and there is no other one: the CLI has no `revert` command and Descript's own history is a
click path.

```ts
// _revert.ts, run from inside CLIs/descript so the relative import resolves
import { head, commit } from "./client";
const state = await head(id);
await commit(id, state, JSON.parse(readFileSync("doc.json", "utf8")), { message: "revert" });
```

Verified 2026-08-31 on EC49: card boundaries 122 -> 78 -> 122, markers and scenes unmoved.

## `--with` binds from the LIBRARY, and on a paced document it deletes cards

`mediaId()` resolves against `doc.mediaLibrary.mediaRefs`, not the timeline, so `layout apply --with`
places a clip that was **never dragged in** - the exact case
[`pins.md`](pins.md) documents as unsolved and needing Descript's private frontdoor call. The bind
itself works: `bound: [{"slot":"Placeholder","media":"03 [00-14] Team On Nothing.mp4"}]`.

**It used to write no media onto the timeline, and that is now fixed.** Two bugs in `applyLayout`,
found 2026-08-31 after seven clips reported `bound` and every ref id occurred exactly as often after
as before: `bindPin` only *rewrote* an existing `mediaRefId`, and a pack card's placeholder segment
has none, so the walk bound nothing; and the slot-to-pin lookup was by array index, which put slot
`Placeholder` on a pin called `Title` whenever a template carries a pin that is not a media slot.
`bindPin` now sets the id on any segment (`offset`+`duration`+`speed` all numeric), the pin is
matched by name, a bind of zero segments throws instead of reporting success, and `bound[]` carries
a `segments` count.

**Verify a bind by counting the media ref id across the whole document anyway.** The `bound:` line
is the thing that lied. A placed clip goes from n to n+1; hold one clip back as a control and check
it did not move.

The first run of this also appeared to delete 44 of 122 card boundaries. It did not: the owner had the
composition open in the app, and the two writers were overwriting each other. Repeated with the tab
closed, cards held at 122 and `orphanedPins` fell from 4 to 1. **A card count that moves under a
`layout` command is a concurrency symptom, not the command.**

## What an "apply layout" click actually writes, captured

The app's own apply is one commit on `/collab/commits` with
`actionType: "EDITOR/COPY_PASTE/PASTE_AT_TARGET"` and `message: "apply layout"`, so the recipe is
readable without a browser: fetch the commit chain, find the ref your snapshot ended on, and decode
each `jdp1:` / `gzjdp1:` delta (base64 gzip, then jsondiffpatch). Two clicks on EC49, 2026-08-31,
gave the whole shape. Four things move, and only four:

1. **`pinScenes` gains the layout's own pin** - here `Whip Low Whoosh`, gain 0.4, a one-tau
   timeline. Its `mediaRefId` is the ref the project ALREADY holds: an asset already imported is
   reused by id, never copied twice. The pin's inner ids (`timeline.id`, the superTau, the four
   sub-tracks) are the pack's own, byte for byte, on both applies - only the scene id and the tau
   ids are fresh. Duplicate inner ids across pin scenes are legal.
2. **The composition's `timeline.pins.components` gains a `sceneComponent`** carrying the stamped
   card's `tauAnchor`, `sceneId` pointing at that new pin, and
   `endAnchor: { type: "cardBoundary", cardBoundaryId: <the NEXT card> }`. `sortTiebreaker` is the
   card's index plus a half, and a second pin over one card takes the next thousandth (2.5, then
   2.501). **This is the half `apply` and `pace` never wrote**, which is what put 46 unresolvable
   layers into EC49; `registerPins` in `layout.ts` writes it now.
3. **The card** gains `templateSource: { projectId, cardId }`, `name`, `layoutType`, the pack's
   `layers` (each with its effects, `sourceSceneId`, `sequenceSceneId`, and `templateState:
   "unedited"` plus `isHidden: true` on a slot nothing fills yet) and a `videoFades` pair of
   `com.descript.smartTransition`.
4. **The next card's `videoFades.tailTransitionEffect.id`** is rewritten, because the transition
   lives on the boundary between the two.

The old note that "the app prunes a sceneComponent it did not author" was wrong. A plain
`sceneComponent` is exactly what it writes; what does not survive is one with no
`endAnchor.cardBoundaryId`.

## A stamped CTA used to lock the project out, through its roomtone

`importAssets` copies the pack's mediaRef into the target project. Twelve pack cards - every CTA
among them - carry `audio.roomtoneRefId` pointing at a companion ref that does NOT travel with the
stamp, and one dangling reference refuses the whole document: "Oh no! Something's not working", with
no repair possible from the app because the app will not open it. The copy now drops a roomtone the
target does not already hold. Nothing is lost: that roomtone matches the pack's room, not the room
the video was recorded in.

**Prove any layout change offline before it is written.** Pull `doc <project> --out now.json`, run
`applyLayout` against the parsed file, and put the result through `inspectDocument` from
`client.ts`. It reads every `*Id` in the document, so a dangling reference is caught on the desk
rather than on a project that will no longer open.

## A Screen layout with no `--screen` shows the camera twice

A pack card's empty frame is marked `templateState: "unedited"` and names no sequence track: it is
the frame an editor drops footage on. `apply` used to point EVERY picture layer at the one track the
composition already drew, which is the camera, so `Screen + Portrait Small` came out with the same face
in the big frame and in the pill. Forty-five cards of the EC49 tour shipped that way on 2026-08-31
and it read as "the screen recording is missing".

`--screen SCREEN` (on `layout apply` and on `layout pace`) points the waiting frames at that track
and leaves every other layer on the camera. It resolves by name or id and names the tracks the
project does cut when the one asked for is not there, rather than drawing the wrong one.

Repairing a tour already stamped is one pass over `doc --out`: for every card whose `name` starts
`Screen`, set the visible `templateState` layer's `sequenceSceneId` to the SCREEN scene, run
`inspectDocument`, then `commit`. **Clone `state.doc` before touching it** - `commit` diffs what you
hand it against `state.doc`, so mutating that object in place reports "nothing changed" and writes
nothing.

## `pace` leaves a beat behind wherever a tau carries two card boundaries

`applyLayout` resolves `--at` and `--tauId` to a TAU, then takes the last card at or before it. A
glitch card or a mid-sentence cut puts **two** boundaries on one tau, so the walk restamps one and
the other keeps whatever it was on. Seven beats of EC49 sat on the app's own `Zoom 100%` that way -
110 seconds of a 24 minute cut, five of them inside the screen tour, where the video dropped from a
pack Screen look back to a bare camera. Nothing reported it: `pace` counted them as done.

`--card <id>` (first 8 characters are enough) restamps exactly one card and skips the tau walk. Read
the ids off `layout cards`; a card printing `(none)` and carrying no pin is a beat the pace missed.

**Never restamp a card that draws a pinned scene.** A restamp replaces what the card draws, so a
glitch, a clip or a title goes with it, and `sweepPins` then deletes the scene. `applied.orphanedPins`
is the number that says it happened - read it. Before a batch, skip any target whose layers name a
`pinScenes` id.

## Never re-sort a track you did not write

Sorting the whole pins track on `clock()` positions is how a track that was already in order comes
out of it: `clock` skips a blocked tau, so every component anchored to a cut word sorts to the
front, and Descript answers `Components are in incorrect order` and refuses the write. Splice the
new component into place instead - every existing one stays exactly where the app left it - and
build the order map over **every** tau, blocked ones included.

## A commit into an open project is reverted, silently

**This is the most expensive trap in this file.** The collab document is not last-write-wins. An
open tab holds its own copy and replays it, so a commit that lands while somebody is in the editor
is discarded a minute later - by the app's next merge, with no error anywhere. On EC49, 2026-08-31,
two clean writes (45 screen frames re-pointed, then 6 beats stamped) were both reverted by a
`DIARIZATION/ADD_DIARIZATION_RESULT` merge. Every check passed: the POST returned a ref,
`inspectDocument` was clean, and the read-back one minute later was correct. The overwrite came
afterwards.

`commit()` now refuses when the newest commit is one the app authored inside the last five minutes,
naming what it was and how long ago. The CLI's own writes carry `EDITOR/DOCUMENT/SET_TRACK_NAME`,
which is how it tells them apart. Pass `anyway: true` only for a project you know is shut.

**A read-back is not proof.** The only proof a layout write survived is a read after the editor is
closed.
