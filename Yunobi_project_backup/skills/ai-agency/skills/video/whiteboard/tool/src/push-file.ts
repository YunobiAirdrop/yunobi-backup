import { readFileSync } from "node:fs";
import { broadcast, join, parseRoomLink } from "#src/room.ts";
import { encodeFile, fetchFile, uploadFile, type SceneFile } from "#src/files.ts";

/**
 * Draws an existing `.excalidraw` file into a room, images included.
 *
 * `push` composes boards from the TypeScript registry. This one takes a file
 * another tool wrote (Seam's `make snapshots` board, an export off the iPad)
 * and puts it on the same canvas, uploading every embedded image first so the
 * frames arrive with something in them.
 *
 *     pnpm push-file <path.excalidraw> [--room <link>]
 */

try {
  process.loadEnvFile();
} catch {
  // No .env, so --room or an exported WHITEBOARD_ROOM has to supply it.
}

const [, , path, ...flags] = process.argv;
const roomIndex = flags.indexOf("--room");
const link = (roomIndex === -1 ? undefined : flags[roomIndex + 1]) ?? process.env.WHITEBOARD_ROOM;

if (!path || !link) {
  console.error("Usage: pnpm push-file <path.excalidraw> [--room <excalidraw room link>]");
  process.exit(1);
}

const scene = JSON.parse(readFileSync(path, "utf8")) as {
  elements: { type: string; fileId?: string; version?: number }[];
  files?: Record<string, { id?: string; dataURL: string; mimeType: string }>;
};

// WHY the version is raised: a peer reconciles by id and keeps whichever copy claims the
// higher one. A generated board writes version 1 into every element, so re-pushing a board
// the room has already seen was dropped in silence and read as a failed upload. A wall clock
// is monotonic across runs, and it only ever competes with an element of the same id, which
// is this board's own. Everything else in the room is untouched: a push appends, and the
// README says why there is no command here that does anything else.
const version = Math.floor(Date.now() / 1000);
const elements = (scene.elements ?? []).map((el) => ({ ...el, version }));
const files: SceneFile[] = Object.entries(scene.files ?? {}).map(([id, file]) => ({
  id,
  dataURL: file.dataURL,
  mimeType: file.mimeType,
}));

const room = parseRoomLink(link);
const { socket, peers } = await join(room);

// WHY: the relay stores nothing, so an empty room swallows the whole push and
// still looks like a success.
if (peers === 0) {
  console.error(`Room ${room.id} has nobody in it, so this push would draw nothing.`);
  console.error("Open the room in ExcalidrawZ or excalidraw.com, then run this again.");
  socket.close();
  process.exit(1);
}

console.log(`joined room ${room.id}, ${peers} client${peers === 1 ? "" : "s"} present`);

// WHY files first: a peer that meets an image element whose file it cannot find
// gives up on that fileId, and re-broadcasting the same element later does not
// make it look again.
for (const file of files) {
  const body = await encodeFile(file, room.key);
  await uploadFile(room.id, file.id, body);
  const stored = await fetchFile(room.id, file.id);
  if (stored.byteLength !== body.byteLength) {
    throw new Error(`${file.id} read back ${stored.byteLength}B, sent ${body.byteLength}B`);
  }
}
if (files.length) console.log(`uploaded ${files.length} file${files.length === 1 ? "" : "s"}`);

await broadcast(socket, room, elements);
console.log(`drew ${path}, ${elements.length} elements`);

await new Promise((resolve) => setTimeout(resolve, 500));
socket.close();
