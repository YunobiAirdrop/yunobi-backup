---
name: whiteboard
description: "Builds the whiteboard a video talks over: a compiled document, or hand-drawn Excalidraw elements drawn live on the iPad. Use when a video needs a board, a diagram from the terminal, or an .excalidraw file to write, change or read."
tags: [makes, video, design]
lane: visual
---

# Whiteboard

The wall a viewer reads while you talk over it, built one of 2 ways depending on how it reaches
the screen. Pick the branch by that, ahead of which tool you know better.

| Reaches the screen by | Branch |
| --- | --- |
| Drawn live on the iPad, on camera, over Excalidraw's collaboration protocol | [Live iPad board](references/excalidraw-board.md) |

A still image with no live camera on it belongs to a different pipeline. Excalidraw's job here is
the board drawn live, on camera.

## Shared judgment, either branch

**One element per concept, every time.** Walk the script or argument concept by concept and ask what shape it is; one
shape for everything is the tell that nobody thought about the idea. Each branch's own vocabulary
table is in its reference file.

**One canvas, walked in the video's order, never several documents.** A board per idea with cuts
between resets the viewer's bearings; a video gets exactly one diagram, its chapters or bands laid
out top to bottom (or left to right) in the video's own order, with air between them so nothing
reads as cramped.
**The words on a board are first-party copy.** Every label runs the `humanizer` loop before it
ships, whichever branch built it. Internal mechanics vocabulary (points, slippage, IDs, production
notes) never goes on a board a viewer sees.

**Look at it, or push it, before calling it done.** A board you have not rendered and looked at is
a board you have not finished. Each branch's own verification loop and checklist is in its
reference file.

## Live iPad board

Hand-drawn Excalidraw elements, laid out as TypeScript, and pushed live to the iPad over
Excalidraw's collaboration protocol, so a diagram arrives already composed and editable on camera.
The vocabulary (`node`, `circle`, `arrow`, `underline`, `ring`), the hand-drawn `LOOK` switch,
colour and layout, the 3 delivery routes, and the layout-overlap gate:
[references/excalidraw-board.md](references/excalidraw-board.md).

## Learned Patterns

The live-iPad branch's own failure modes, newest first, in
[references/learned-patterns.md](references/learned-patterns.md): read it before a run, append
after one.