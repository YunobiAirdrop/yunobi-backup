# Live iPad board

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

## The `.excalidraw` file is build output

**Never hand-edit one, never script over its JSON, and never go looking for a library.** A 175-line
board source builds to 47KB of elements carrying seeds, versions and nonces, so a hand edit and the
next `pnpm build` disagree and the iPad shows whichever ran last. `@excalidraw/excalidraw` is a React
component that needs react and react-dom in the page and `@excalidraw/utils` never left prerelease,
so neither reaches a file from a terminal. This tool is the utility: change `src/boards/<board>.ts`
and rebuild. A file another tool wrote has one route, `pnpm push-file <path>`, which draws it as it
stands; nothing here reads a drawing back into board source.

## The vocabulary

`node(cx, cy, r, label)` is a circle plus its centred caption and is the workhorse. `circle`, `text`,
`arrow`, `underline` and `ring` are the rest, and `shift(elements, dx, dy)` moves a whole group,
which is how a board drops into its band on export. Coordinates are a plain top-left canvas, y grows
downward, and every position is absolute, so a board is a set of named x constants with items hung
off them.

Colours are two constants in `src/scene.ts`, `INK` for every stroke and label and `HIGHLIGHT` for
the marker pass. Derive both from your own brand tokens rather than picking them by eye. They are
hex copies because Excalidraw stores hex, so re-derive them if the palette moves rather than
eyeballing a replacement.

**The look is hand-drawn, and it is a switch rather than the tool.** `LOOK` in `src/scene.ts` is
`hand` since 10 September 2026: rough.js strokes and Excalifont on every figure. The author's ruling, on
a board built the other way: *"instead of choosing drawing based designs and circles you chose very
sharp shapes, I want to always in Excalidraw use this type of shape, that's more like drawing."*
`clean` held the house from 16 August 2026 until then and is kept only for a figure that sits inside
a page. Never set roughness or `fontFamily` on an element to work around it; change `LOOK` and
rebuild, or every board drifts apart.

**Draw with circles and open strokes, not filled rounded rectangles.** Same ruling. A transparent
circle with its caption beside it, an arrow with a word on it, and the terra ring for the one number
that matters. A saturated fill behind a rounded box reads as a UI component, which is the look he
rejected; the Whimsical rule below says the same thing in the other tool.

## Colour and layout

One hue per concept from `HUES` in `src/scene.ts`, never for prose; one column per beat of the
argument; captions beside a node, never on it; rings and underlines as a tight emphasis budget;
arithmetic shown as a sum. The exact rules, the caption-offset formula and where talking points ride
along the board: [composition.md](composition.md).

## One canvas, walked in order, never several documents

A board can decorate a talking head, or it can be the video. Measured 24 Aug 2026 on Matis Clouet's
`09a_B8KZURM`: 19:22 and 5,011 words, 29k views on a channel under 4k subscribers, the whole runtime
one canvas on a shared screen, walked node by node, never opening the tool it was built in.

- **One canvas, several bands, walked in order**, not one board per idea with cuts between: the
  viewer keeps their bearings because the picture never resets. `pieces` in `src/boards.ts` models
  this. **A video gets exactly one diagram**, beats as zones in the spoken order, never separate
  files (24 Aug 2026: *"You should never ever create multiple diagrams for one video"*).
- **The diagram is the *what*, the tool is the *how*.** If a beat can only be shown by clicking
  something, it belongs in a different video.
- **Screenshots are proof, not navigation.** A framed still that proves a claim the board just made,
  cut in and back out. A recording that goes live in the product has collapsed into a tutorial.
- **Board 1 carries the idea every later board restates.** The opening board is the vocabulary and
  every board after it ends by naming the same thing again, `video-script`'s teach-block finding
  applied to a canvas.

What does not transfer: he asks five or more times across a runtime this long. The count stays at
one outbound ask in the last twenty seconds, with in-platform asks free and mid-roll.

**In Whimsical, shapes are never fully coloured.** Pass `deco: "outline"` with the hue; leave notes
light (white or smoke) rather than saturated fill (24 Aug 2026: *"I use outline and light color in
designs in whimsical"*). Saturated fill puts white text on strong ground; outline keeps hue as
identity.

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

Dictate the argument for ten minutes, expect the first pass at about 80%, and budget half an hour
to edit it. Why, and what stays hand work: [drafting.md](drafting.md).

## Deliver it, by whichever route is open

Building a board is not delivering one, and there are three routes that deliver. **Take one of them
as the last step of every board, without being asked**, then say what landed and where.

| Route | Command | When |
| --- | --- | --- |
| Push into the room | `pnpm push <board>` | Somebody is in the room. Fastest; arrives already composed. |
| The clipboard | `pnpm copy <piece>` | Any open canvas, including a local file. Normalises the set back to origin. |
| The files | `pnpm build <board>` | `out/<board>.excalidraw` is a real file. Drag it onto Excalidraw, or open it in ExcalidrawZ. |
| The contact sheet | `pnpm render all --scale 1 && pnpm gallery` | Every board on one page, for finding one without knowing its name. **Rebuild it in the session that adds or changes a board.** [delivery.md](delivery.md), "The contact sheet". |

A still image belongs to a different, app-based pipeline, not this tool.
 The `pnpm render` figures in `src/figures/` stay only as the source of PNGs
already out, like the immutable email URLs.

**The push is not required.** Stated 24 Aug 2026: *"the skill does not need to push to the room. It
can create locally and then I can copy paste or drag and drop into Excalidraw."* Pick the route
that fits, and name the `out/` path when the answer is the files. The room, why the canvas is
append-only, band allocation and coordinates, `push-file`, and element order as the talk track
(why the array order is the spoken order, and how `--pace` is set) are in
[delivery.md](delivery.md).

## Verify before pushing

The file is valid JSON whether or not a caption is sitting on a circle, and the mistake only shows
up once it is on the iPad in front of a camera.

```bash
pnpm typecheck && pnpm build <board>
node ../scripts/check-layout.mjs out/<board>.excalidraw
```

The gate reports text over text, text over an off-centre shape, and text over an underline, then
prints the element count and the bounds. Concentric overlaps are skipped, because a label inside a
node and a ring around a figure are both concentric by construction. Fix the coordinates, rebuild,
run it again. **A board is not pushed until this prints `layout clean`.**

## The words on a board are first-party copy

A board goes on camera under the author's name, so every label follows the voice profile.
 **Internal mechanics vocabulary is banned on camera**, which is a separate and
easier rule to break: points, slippage and the three-space model never appear in transcripts of him
talking, and a number on a board invites the question it stands for. Write what the mechanism does
for the viewer and keep the machinery out of the frame.

## Verification checklist

- [ ] `pnpm typecheck` clean and the board rebuilt after the last source edit
- [ ] `check-layout.mjs` prints `layout clean`
- [ ] Delivered by one of the three routes, and said which; a push verified with `pnpm inspect`
- [ ] Element order matches the spoken order, and `elements * pace` fits the script
- [ ] One ring, and it is around the number the board exists for
- [ ] Every label read against `humanizer`, with no internal mechanics vocabulary
- [ ] The room link was not written into any summary or committed file
- [ ] Any new failure mode appended to Learned Patterns

## Learned Patterns

They live in [learned-patterns.md](learned-patterns.md), newest first.
**Read that file before a run**, and append to it after one whenever a run surfaces something not
already there.
