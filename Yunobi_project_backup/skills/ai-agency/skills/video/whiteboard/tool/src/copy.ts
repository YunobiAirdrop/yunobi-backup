import { spawnSync } from "node:child_process";
import { boards, pieces, resolve } from "#src/boards.ts";
import type { El } from "#src/scene.ts";

/**
 * Puts a board, or a whole piece of content, on the clipboard in Excalidraw's
 * own clipboard format, so it can be pasted into any canvas rather than only
 * into the room `push` draws on.
 *
 * Positions are normalised to the origin first. Boards are authored in their
 * own band of one shared canvas, which puts the later ones thousands of pixels
 * down, and Excalidraw pastes what it is given.
 */

const [, , name] = process.argv;
const names = name ? resolve(name) : [];

if (names.length === 0) {
  console.error("Usage: pnpm copy <board | piece | all>");
  console.error(`Pieces: ${Object.keys(pieces).join(", ")}`);
  console.error(`Boards: ${Object.keys(boards).join(", ")}`);
  process.exit(1);
}

const elements: El[] = names.flatMap((board) => boards[board]);
const top = Math.min(...elements.map((el) => el.y as number));
const left = Math.min(...elements.map((el) => el.x as number));
const placed = elements.map((el) => ({
  ...el,
  x: (el.x as number) - left,
  y: (el.y as number) - top,
}));

const payload = JSON.stringify({ type: "excalidraw/clipboard", elements: placed, files: {} });
const copied = spawnSync("pbcopy", { input: payload });

if (copied.error || copied.status !== 0) {
  console.error(
    `Could not reach the clipboard: ${copied.error?.message ?? `pbcopy exited ${copied.status}`}`,
  );
  process.exit(1);
}

const size = `${Math.round(payload.length / 1024)} KB`;
console.log(`copied ${names.join(", ")}: ${placed.length} elements, ${size}`);
console.log("paste into any Excalidraw canvas with cmd V");
