import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { boards, resolve } from "#src/boards.ts";
import { scene, type El } from "#src/scene.ts";

const only = process.argv[2];

// WHY resolve() rather than a lookup in `boards`: push and copy both take a
// piece name, and a build that did not left `pnpm build intro` failing with
// "Unknown board" on the exact name the other two commands accept.
const names = only ? resolve(only) : Object.keys(boards);

if (only && !names.length) {
  console.error(`Unknown board or piece "${only}". Available: ${Object.keys(boards).join(", ")}`);
  process.exit(1);
}

const outDir = new URL("../out/", import.meta.url).pathname;
await mkdir(outDir, { recursive: true });

for (const name of names) {
  const elements = boards[name];
  if (!elements) continue;
  const file = join(outDir, `${name}.excalidraw`);
  await writeFile(file, scene(elements));
  console.log(`${file}  (${elements.length} elements)`);
}

// WHY: every board is authored into its own band of one tall shared canvas, and
// nothing enforced that. Two boards given the same band land on top of each
// other in the room, which reads as a broken push rather than as a coordinate
// bug. The whole registry is checked whatever was built, since a band is a
// property of the set.
function bounds(elements: El[]) {
  return {
    x1: Math.min(...elements.map((el) => el.x as number)),
    x2: Math.max(...elements.map((el) => (el.x as number) + ((el.width as number) ?? 0))),
    y1: Math.min(...elements.map((el) => el.y as number)),
    y2: Math.max(...elements.map((el) => (el.y as number) + ((el.height as number) ?? 0))),
  };
}

const boxes = Object.entries(boards).map(([name, elements]) => ({ name, ...bounds(elements) }));
const clashes = boxes.flatMap((a, i) =>
  boxes
    .slice(i + 1)
    .filter((b) => a.x1 < b.x2 && b.x1 < a.x2 && a.y1 < b.y2 && b.y1 < a.y2)
    .map(
      (b) =>
        `${a.name} (y ${Math.round(a.y1)}..${Math.round(a.y2)}) overlaps ${b.name} (y ${Math.round(b.y1)}..${Math.round(b.y2)})`,
    ),
);

if (clashes.length) {
  console.error(`\n${clashes.length} band collision${clashes.length === 1 ? "" : "s"}:`);
  for (const clash of clashes) console.error(`  ${clash}`);
  console.error("Move one of each pair to a free band before pushing.");
  process.exit(1);
}
