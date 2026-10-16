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
