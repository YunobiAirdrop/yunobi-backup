import { boards } from "#src/boards.ts";
import { decrypt, join, parseRoomLink } from "#src/room.ts";

/**
 * Reports which boards are actually on the canvas in the room.
 *
 * WHY it exists: the relay stores nothing and `push` can only say what it sent,
 * so "drew 64 elements" and "the room holds 64 elements" were never the same
 * claim. A collaborator answers `new-user` by broadcasting its whole scene to
 * whoever just joined, so joining and listening is the one way to read the
 * canvas back. Element ids are deterministic and unique across the registry,
 * which is what turns that scene into a board list.
 */

try {
  process.loadEnvFile();
} catch {
  // No .env, so --room or an exported WHITEBOARD_ROOM has to supply it.
}

const flags = process.argv.slice(2);
const roomIndex = flags.indexOf("--room");
const link = (roomIndex === -1 ? undefined : flags[roomIndex + 1]) ?? process.env.WHITEBOARD_ROOM;
const waitIndex = flags.indexOf("--wait");
const wait = waitIndex === -1 ? 8000 : Number(flags[waitIndex + 1]);

if (!link) {
  console.error("Usage: pnpm inspect [--room <excalidraw room link>] [--wait <ms>]");
  process.exit(1);
}

/** Which board an element id belongs to, since ids are handed out per board. */
const owner = new Map<string, string>();
/** Where the build puts it, so a board sitting at a superseded band shows up. */
const placed = new Map<string, number>();
for (const [name, elements] of Object.entries(boards)) {
  for (const el of elements) {
    owner.set(el.id as string, name);
    placed.set(el.id as string, el.y as number);
  }
}

const room = parseRoomLink(link);
const { socket, peers } = await join(room);

if (peers === 0) {
  console.error(`Room ${room.id} has nobody in it, so there is no canvas to read.`);
  socket.close();
  process.exit(1);
}

console.log(`joined room ${room.id}, ${peers} client${peers === 1 ? "" : "s"} present`);

const seen = new Set<string>();
const stale = new Set<string>();
/** Every live element by id, so repeated broadcasts do not count one twice. */
const live = new Map<string, { y: number; height: number }>();

socket.on("client-broadcast", async (buffer: ArrayBuffer, iv: Uint8Array<ArrayBuffer>) => {
  const message = await decrypt(room.key, buffer, iv);
  const elements = message?.payload?.elements;
  if (!Array.isArray(elements)) return;
  for (const el of elements) {
    if (el.isDeleted) {
      live.delete(el.id);
      continue;
    }
    if (typeof el.y === "number") live.set(el.id, { y: el.y, height: el.height ?? 0 });
    const board = owner.get(el.id);
    if (!board) continue;
    seen.add(el.id);
    if (Math.round(el.y) !== Math.round(placed.get(el.id) as number)) stale.add(el.id);
    else stale.delete(el.id);
  }
});

await new Promise((resolve) => setTimeout(resolve, wait));
socket.close();

// WHY a count per board rather than a present/absent flag: a partial board is
// the interesting case, and it looks identical to a whole one from the room.
const rows = Object.entries(boards).map(([name, elements]) => ({
  name,
  on: elements.filter((el) => seen.has(el.id as string)).length,
  old: elements.filter((el) => stale.has(el.id as string)).length,
  of: elements.length,
}));

for (const row of rows.filter((r) => r.on)) {
  const state = row.on === row.of ? "complete" : "PARTIAL";
  const band = row.old ? `, ${row.old} at a superseded band` : "";
  console.log(`  ${row.name.padEnd(30)} ${String(row.on).padStart(3)}/${row.of}  ${state}${band}`);
}

const missing = rows.filter((r) => !r.on).map((r) => r.name);
if (missing.length) console.log(`\nnot on the canvas: ${missing.join(", ")}`);

// WHY the bands and not just a count: a push appends, so the question before sending one is
// "which band is free", and the room holds boards this repo has never heard of. A count of
// foreign elements says they exist; where they sit is what stops a push landing on them.
const occupied = [...live.values()].sort((a, b) => a.y - b.y);
if (occupied.length) {
  const bands: { from: number; to: number; count: number }[] = [];
  for (const el of occupied) {
    const last = bands.at(-1);
    // A gap of a thousand is wider than any board's internal spacing and narrower than
    // the smallest gap the band map leaves between two of them.
    if (last && el.y - last.to < 1000) {
      last.to = Math.max(last.to, el.y + el.height);
      last.count += 1;
    } else {
      bands.push({ from: el.y, to: el.y + el.height, count: 1 });
    }
  }
  console.log(
    `\n${occupied.length} elements on the canvas, in ${bands.length} band${bands.length === 1 ? "" : "s"}:`,
  );
  for (const band of bands) {
    console.log(`  y ${Math.round(band.from)} to ${Math.round(band.to)}  ${band.count} elements`);
  }
} else {
  console.log("\nthe peer sent no scene, so nothing could be read back");
}
