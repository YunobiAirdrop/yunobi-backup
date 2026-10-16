---
name: whiteboard
description: "Lays out hand-drawn concept boards as code and draws them onto the iPad live over Excalidraw's collaboration protocol, so a diagram arrives already composed and still editable on camera. Use when a video needs a board behind it, when an idea has to become circles, arrows and highlighter rings, when a board needs re-laying out or re-pushing, or when anything needs drawing into ExcalidrawZ from the Mac."
tags: [makes, video, design]
---

# Whiteboard

Boards live in `tool/` as TypeScript, not as drawings. A board is an array of elements built from
the helpers in `src/scene.ts` and registered in `src/boards.ts`. Run `pnpm install` in `tool/`
once, and run every command below from there.

```bash
pnpm build                      # every board to out/
pnpm build <board>              # just one
pnpm push <board> --room '<link>' --pace 700
```

`README.md` in that folder owns the protocol and the reasoning: why Excalidraw rather than Freeform
or Miro, how the collab socket works, and the iCloud route for boards that do not need to arrive
live. **Read it before changing anything in `src/`.** This file owns how a board gets composed,
checked and drawn.

## The vocabulary

`node(cx, cy, r, label)` is a circle plus its centred caption and is the workhorse. `circle`, `text`,
`arrow`, `underline` and `ring` are the rest. Coordinates are a plain top-left canvas, y grows
downward, and every position is absolute, so a board is a set of named x constants with items hung
off them.

Colours are two constants in `src/scene.ts`, `INK` for every stroke and label and `HIGHLIGHT` for
the marker pass. Derive both from your own brand tokens rather than picking them by eye. They are
hex copies because Excalidraw stores hex, so re-derive them if the palette moves rather than
eyeballing a replacement.

**The sketchy look is a switch, not the tool.** `LOOK` in `src/scene.ts` is `clean` since 16 August
2026: figures draw as straight strokes in Nunito, and only the terra ring and underline stay rough,
because those stand in for a marker pass over a finished diagram. `hand` restores rough.js and
Excalifont everywhere. Never set roughness or `fontFamily` on an element to work around the house
look; change `LOOK` and rebuild, or every board drifts apart.

## One hue per concept

A board that carries several parallel ideas gets a colour per idea, from `HUES` in `src/scene.ts`
(`indigo`, `amber`, `rose`, `green`, `teal`, `violet`). Each entry is a stroke, a pale tint for the
fill, and a darker label that survives sitting on that tint, so `node(cx, cy, r, name, size,
HUES.amber)` gives a filled circle whose caption stays readable.

**Colour the things that differ, leave everything else `INK`.** Four spaces, five stages, three
products: those are parallel concepts and a viewer sorts them by colour before reading a word. The
explanation around them is not a concept, it is prose, and prose in six colours is decoration.

**The hue is the concept's identity across the whole board, and across the set.** Give a caption the
same hue as the node it belongs to, and give an arrow leaving a node that node's hue, so a group
reads as a group. If a second board covers the same concepts, it keeps the same assignment: two
boards in one video that recolour the same four ideas cost more than they buy.

**One monochrome board is still the default.** Reach for `HUES` when the board is a taxonomy or a
comparison. A board that is one argument in three beats stays `INK` with `HIGHLIGHT` for emphasis.

## Composition

**One column per beat of the argument.** Declare the centres as constants (`const STACK = 380`) and
place everything relative to them. Two or three columns fill a frame; four is too wide to read on
camera.

**Captions sit beside a node, never on it.** Text is centred on its `(cx, cy)` and its width is
roughly `longest_line * fontSize * 0.52`, so a caption's half-width plus the circle radius decides
the offset. Getting this wrong is the most common defect and the layout gate below is what catches it.

**Rings and underlines are the emphasis budget.** One `ring` for the single number the board is
built around, `underline` for a title and for a total that has been ruled off. More than two rings
and none of them mean anything.

**Show arithmetic as a sum, never as a total.** A board is the one surface where the working can be
on screen: the parts, a rule across, then the result. Quoting the result alone throws away the
retention that the calculation buys.

**The talking points ride along as their own board, at negative x.** Build them with `paragraph`,
which anchors at the top-left, and push them separately so they land in the same room without
touching the diagram. **Bullets, never prose**: the opening and closing lines are said as written and
the middle is spoken live, so a written-out middle gets read out on camera. `shorts-production`, "The
note shape", owns that split.

## The whole video is the board, walked

A board can decorate a talking head, or it can **be** the video. The second is its own
format and it is the one this skill is best at, so it gets named rather than rediscovered.

Measured 24 Aug 2026 on Matis Clouet's `09a_B8KZURM` (19:22, 5,011 words, 29k views on a
channel under 4k subscribers). The whole runtime is one canvas on a shared screen, walked
node by node. He never opens the tool the system is built in, never clicks, never builds.
The board carries the argument and the build is what he sells.

What transfers:

- **One canvas, several bands, walked in order.** Not one board per idea with cuts between.
  The viewer keeps their bearings because the picture never resets, and `pieces` in
  `src/boards.ts` already models exactly this.
- **The diagram is the *what*, the tool is the *how*.** Teaching the shape and selling the
  build is the split that makes a screen-share video sell without turning into a demo. If a
  beat can only be shown by clicking something, it belongs in a different video.
- **Screenshots are proof, not navigation.** A framed still that proves a claim the board
  just made, cut in and back out. The moment the recording goes live in the product, the
  format has collapsed into a tutorial.

What does not transfer: he asks five or more times across the runtime. `video-script`'s ask
rule is measured against a three-run control and his is not, so the count stays at one
outbound ask in the last twenty seconds, with in-platform asks free and mid-roll.

**Board 1 carries the idea every later board restates.** `video-script`'s teach-block
finding is that one portable idea named once and pointed at six times holds longer than six
ideas listed once. On a walked canvas that means the opening board is the vocabulary, and
every board after it ends by naming the same thing again.

## One video, one document

**A video gets exactly one diagram.** Never split its visuals across several files, even when they
band down one shared canvas. His words, 24 Aug 2026: *"I don't want nine diagrams. You should never
ever create multiple diagrams for one video."* One video was built as nine `.excalidraw` boards
banded down a canvas: on the canvas it read as one picture, and in Finder it was nine things to
open, move and keep in sync. He deleted all of them and rebuilt it as a single board.

So the beats are **zones inside one document**, laid out in the order they are spoken, not separate
files. The `pieces` map below models a piece as a list of boards, which is the shape this rule
rejects for a video: keep it to one entry per video and put the beats inside that board.

**In Whimsical, shapes are never fully coloured.** Pass `deco: "outline"` with the hue, which
renders a coloured stroke over a light tint, and leave notes light (white or smoke) rather than
carrying a saturated fill. His words, same day: *"I never use fully colored, I use outline and light
color in designs in whimsical."* A saturated fill puts white text on a strong ground and turns a
diagram into a set of buttons; the outline keeps the hue as identity and leaves the words as the
thing being read. `color` alone defaults to `deco: fill`, so pass `deco` explicitly on create. On an
existing board, one `edit` call of `{op: "update", id, deco: "outline"}` per shape converts the lot.

## A piece of content, not a board

Boards are the unit of layout; a video is the unit of work. `pieces` in `src/boards.ts` maps one
name to the boards behind one piece of content, and every command takes a piece name, a board name,
or `all`:

```bash
pnpm push intro            # every board behind that video, into the room
pnpm copy skool            # the same set onto the clipboard
```

Add a board to a piece in the same edit that registers it, or the piece silently stops being the
whole video.

`copy` writes Excalidraw's own `excalidraw/clipboard` payload and normalises the set back to the
origin first, since boards are authored in bands of one tall shared canvas. It is the route into a
canvas that is not the pushed room: a local file, a different room, somebody else's screen.

## Draft the set by talking, then edit it down

The fastest way into a piece's board set is not a written brief. Dictate for ten minutes: the
argument, the beats, roughly how many boards it wants, and what each one is trying to show. Speech
carries the argument's real order, which is the part a written outline flattens, and dictating is
where the number of boards settles honestly rather than being padded to a round figure.

**Expect the first pass at about 80% and budget half an hour to edit it.** That is the deal, and it
is a good one against composing from a blank canvas. What comes back is the layout skeleton; the
captions, the hue assignment and the offsets in `Composition` above are hand work and stay hand
work. Do not push a dictated set without that pass.

**The set then frames the recording, not the other way round.** Once the boards exist, the video is
the boards said out loud in order, which is why `Element order is the talk track` below matters. A
board added after the recording usually means a beat the argument did not have.


## Deliver it, by whichever route is open

Building a board is not delivering one, and there are three routes that deliver. **Take one of them
as the last step of every board, without being asked**, then say what landed and where.

| Route | Command | When |
| --- | --- | --- |
| Push into the room | `pnpm push <board>` | Somebody is in the collaboration room. Fastest, and the board arrives already composed. |
| The clipboard | `pnpm copy <piece>` | Any canvas that is already open, including a local file. Normalises the set back to the origin. |
| The files | `pnpm build <board>` | `out/<board>.excalidraw` is a real file. Drag it onto Excalidraw, or open it in ExcalidrawZ. |

**The push is not required, and it never was.** Stated 24 Aug 2026: *"the skill does not need to push
to the room. It can create locally and then I can copy paste or drag and drop into Excalidraw."* The
relay stores nothing, so a push only works while a peer is connected, and building the delivery
around that made an empty room look like a failure when the files were sitting in `out/` the whole
time. Pick the route that fits, and name the `out/` path when the answer is the files.

**A shared canvas is append-only.** The room holds work no repo knows about: another product's
screenshots, a morning of Pencil annotation. Read it first with `pnpm inspect`, which reports every
occupied band, then take a **free** band. Never clear, erase or reset a band to make room, and never
write a command that does. Clearing a band to "replace" a board took Wavenote's screenshots off the
room on its first run, because the band held two boards and only one was being replaced. No command
can know what somebody else put there. This holds for every shared surface, not just this one.

The room, the band allocation, `push-file` for a board another tool wrote, and `pnpm inspect` for
reading the canvas back are in [`references/delivery.md`](references/delivery.md). **Two boards
pushed into one room need different coordinates**, and `pnpm build` fails on an overlap, so a band
clash never reaches the canvas.

## Element order is the talk track

`push` broadcasts the scene cumulatively, one element at a time, so the array order is the order the
board draws itself. Write the elements in the order they are spoken and the push becomes the
animation. Set `--pace` so that `elements * pace` lands just under the length of the script: 53
elements at 700ms is about 37 seconds.

Reconciliation on the far side merges by element id, and ids are deterministic across builds, so
anything drawn with the Pencil during a push survives, and re-pushing a rebuilt board replaces its
own elements rather than duplicating them.

## Verify before pushing

The file is valid JSON whether or not a caption is sitting on a circle, and the mistake only shows
up once it is on the iPad in front of a camera.

```bash
pnpm typecheck && pnpm build <board>
node <skill>/scripts/check-layout.mjs out/<board>.excalidraw
```

The gate reports text over text, text over an off-centre shape, and text over an underline, then
prints the element count and the bounds. Concentric overlaps are skipped, because a label inside a
node and a ring around a figure are both concentric by construction. Fix the coordinates, rebuild,
run it again. **A board is not pushed until this prints `layout clean`.**

## The words on a board are first-party copy

A board goes on camera under the author's name, so the voice profile and the copy rules apply to every label:
no slop vocabulary, no engagement-bait close, no em dashes. **Internal mechanics vocabulary is
banned on camera**, which is a separate and easier rule to break: points, slippage and the
three-space model never appear in transcripts of him talking, and a number on a board invites the
question it stands for. Write what the mechanism does for the viewer and keep the machinery out of
the frame.

## Verification checklist

- [ ] `pnpm typecheck` clean and the board rebuilt after the last source edit
- [ ] `check-layout.mjs` prints `layout clean`
- [ ] Delivered by one of the three routes, and said which; a push verified with `pnpm inspect`
- [ ] Element order matches the spoken order, and `elements * pace` fits the script
- [ ] One ring, and it is around the number the board exists for
- [ ] Every label read against `voice-dna`, with no internal mechanics vocabulary
- [ ] The room link was not written into any summary or committed file
- [ ] Any new failure mode appended to Learned Patterns

## Learned Patterns

They live in [`references/learned-patterns.md`](references/learned-patterns.md), newest first.
**Read that file before a run**, and append to it after one whenever a run surfaces something not
already there.
