import { boards, pieces, resolve } from "#src/boards.ts";
import { broadcast, join, parseRoomLink } from "#src/room.ts";

// WHY: the room link carries the encryption key, so it lives in a gitignored
// .env rather than in the repo or in shell history.
try {
  process.loadEnvFile();
} catch {
  // No .env, so --room or an exported WHITEBOARD_ROOM has to supply it.
}

const [, , name, ...flags] = process.argv;
const names = name ? resolve(name) : [];
// WHY: indexOf returns -1 when the flag is absent, and flags[0] is the next
// flag rather than a room link, so the miss has to be handled explicitly.
const roomIndex = flags.indexOf("--room");
const link = (roomIndex === -1 ? undefined : flags[roomIndex + 1]) ?? process.env.WHITEBOARD_ROOM;

if (names.length === 0 || !link) {
  console.error("Usage: pnpm push <board | piece | all> [--room <excalidraw room link>]");
  console.error(`Pieces: ${Object.keys(pieces).join(", ")}`);
  console.error(`Boards: ${Object.keys(boards).join(", ")}`);
  process.exit(1);
}

const paceIndex = flags.indexOf("--pace");
const pace = paceIndex === -1 ? 250 : Number(flags[paceIndex + 1]);
const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

const room = parseRoomLink(link);
const { socket, peers } = await join(room);

// WHY: the relay stores nothing, so an empty room swallows the whole push and
// still looks like a success. Fail loudly instead of reporting a draw that
// nobody received.
if (peers === 0) {
  console.error(`Room ${room.id} has nobody in it, so this push would draw nothing.`);
  console.error("Open the room in ExcalidrawZ or excalidraw.com, then run this again.");
  socket.close();
  process.exit(1);
}

console.log(`joined room ${room.id}, ${peers} client${peers === 1 ? "" : "s"} present`);

// WHY: the scene is broadcast cumulatively and reconciled by element id on the
// other side, so collaborators keep whatever they drew themselves. Each board
// is broadcast on its own, since ids are unique across the whole registry.
for (const board of names) {
  const elements = boards[board];
  for (let count = 1; count <= elements.length; count += 1) {
    await broadcast(socket, room, elements.slice(0, count));
    if (pace) await sleep(pace);
  }
  console.log(`drew ${board}, ${elements.length} elements`);
}

await sleep(500);
socket.close();
