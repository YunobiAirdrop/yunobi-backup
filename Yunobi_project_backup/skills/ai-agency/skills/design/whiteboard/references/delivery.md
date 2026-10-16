# Delivering a board

The three delivery routes and the rule that one of them runs on every board are in `SKILL.md`. This
file holds the mechanics behind the room route.

## The room link is a secret

It carries the AES key in its fragment, so anyone who reads it off the screen can join the board.
Keep it out of frame while recording, take it from the user each session rather than storing it, and
never print it back into a summary.

## The room, the bands and reading the canvas back

`WHITEBOARD_ROOM` in `tool/.env` is the room, quoted. If it is missing, ask for the link
once and pass it as `--room` for that run rather than writing it to disk.

**Two boards pushed into one room need different coordinates.** Pushes carry absolute positions, so a
second board authored from the same origin lands on top of the first. Give each one its own band of
the canvas (`const TOP = 1750`, mapped over the elements on export). `pnpm build` checks every
board's bounding box against every other and exits non-zero on an overlap, whichever board was
built, so a band clash is a build failure rather than a mess on the canvas.

**A group of boards opens with a `banner` naming the video.** A recording session runs down the
canvas and the boards do not say which take they belong to, so each group carries a grey title and a
rule 300px above its first board: quiet, out of frame once a board is zoomed into, and unmissable
while scrolling. The banner is authored in the group's first board so its bounding box stays honest.

**Take the band next to the boards it ships with.** The allocation is mapped at the top of
`src/boards.ts`, and the sets that share a room are packed one after another rather than spread over
round numbers. A band reserved for a board that belongs on a different canvas is a hole in this one,
and a hole reads as a push that half arrived.

**A board another tool wrote goes up with `pnpm push-file <path.excalidraw>`.** Screenshots, an
export off the iPad, anything with an embedded `files` map: it uploads the images first, then
broadcasts the elements. `push` alone would draw empty frames, because the socket carries elements
and an image element only names a `fileId`. Image uploads cannot be taken back, so check the file
before sending it.

**`pnpm inspect` reads the canvas back.** `push` can only report what it sent. A collaborator answers
a new joiner by broadcasting its whole scene, so `inspect` joins, decrypts it and prints which boards
are actually there, complete or partial, and whether any element still sits at a superseded band. Run
it after a push, and run it first when somebody says a board is missing: a board can be on the canvas
and off the screen.

## The canvas is append-only

The room holds work no repo knows about: another product's screenshots, a morning of Pencil
annotation. Never clear, erase or reset a band to make room, and never write a command that does.
Clearing a band to "replace" a board took Wavenote's screenshots off the room on its first run,
because the band held two boards and only one was being replaced. No command can know what somebody
else put there.

## Element order is the talk track

`push` broadcasts the scene cumulatively, one element at a time, so the array order is the order the
board draws itself. Write the elements in the order they are spoken and the push becomes the
animation. Set `--pace` so that `elements * pace` lands just under the length of the script: 53
elements at 700ms is about 37 seconds.

Reconciliation on the far side merges by element id, and ids are deterministic across builds, so
anything drawn with the Pencil during a push survives, and re-pushing a rebuilt board replaces its
own elements rather than duplicating them.

## The contact sheet

`src/gallery.ts` reads the registry, takes the PNG `pnpm render all --scale 1` left for each board,
and writes them all into
one local `.html` page
 as inlined WebP, grouped by video. A tile crops to the top of the board, where
its title is; the whole board is one click away. Built 10 Sep 2026, when finding the ClickUp pricing
board meant opening files in `out/` by name.

Two traps. WebP holds 16,383 pixels an edge, so a spoken column, twelve times taller than it is
wide, blows the limit the moment a thumbnail pipeline fixes the width alone: cap both edges and
never enlarge. And the page carries the pictures inlined rather than pointing at `out/png/`, because
a page that points at a tool's output draws empty frames the day that folder is cleaned.

## A figure to PNG, for an email or a page

`pnpm render <figure>` exports through Excalidraw's own `exportToBlob` in headless Chromium, so
the PNG is what Excalidraw would export, fonts included, cropped to the elements plus
`--padding` (default 32) at `--scale` (default 2). Output: `out/png/<name>.png`. Figures are
registered in `src/figures.ts`, sit at the origin of their own canvas and take no band; they are
reskinned with `handLook()` once, per figure, so a letter reads as drawn and the boards stay clean.

Then `pnpm cli storage upload --file out/png/<name>.png --path email/lessons/<name>-v1.png
--bucket brand-assets` from `app/cli`, and the file serves at
`https://<your-app>/api/brand-assets/email/lessons/<name>-v1.png`
, immutable, so a
change is a new `-v2` path. The 8 email figures: `src/figures/email-lessons.ts`.

Two traps. `tsx` compiles every function with an esbuild `__name` helper, so a function passed to
`page.evaluate` dies with `__name is not defined`: define the exporter inside the page and call it
by a string expression. And `textWidth()` underestimates Excalifont by about a fifth, so leave
more room right of a long hand-look label than the estimate says.
