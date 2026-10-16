import { arrow, node, ring, text, underline, type El } from "../scene.ts";

/**
 * The one board that ships with this skill, and the template for your own.
 *
 * It argues one thing: the old agency stacks four departments and keeps 35% of
 * the revenue, the new one runs on attention plus systems and keeps 88%. Two
 * columns, arrows between them, and a highlighter ring on the number each
 * column exists for.
 *
 * Read it for the four moves every board makes: named x constants rather than
 * scattered coordinates, `node()` for a labelled circle, one `ring` on the
 * number that matters, and a `BAND` offset applied last so the board owns its
 * own stretch of the shared canvas.
 */

const OLD_X = 300;
const NEW_X = 880;
const R = 105;

/**
 * This board's band of the tall shared canvas. Every board is authored from the
 * origin and moved into its band on the way out, because a push carries
 * absolute positions and a second board authored at the origin lands on top of
 * the first. `pnpm build` fails on an overlap, so a clash is a build error
 * rather than a mess in the room.
 */
const BAND = 0;

const oldStack = [
  { label: "Marketing", pct: "10%", cy: 300 },
  { label: "Ads", pct: "25%", cy: 540 },
  { label: "Sales", pct: "20%", cy: 780 },
  { label: "Client\nSuccess", pct: "10%", cy: 1020 },
];

// The array order is the order the board draws itself under `pnpm push`, so
// this is the talk track: write each element where it is spoken.
const beats: El[] = [
  // The old way, top to bottom.
  text(OLD_X, 70, "The Old Way", { size: 48 }),
  text(OLD_X, 130, "6 to 7 figures", { size: 20 }),
  underline(235, 148, 370),
  text(OLD_X, 168, "funnels", { size: 22 }),
  ...oldStack.flatMap(({ label, pct, cy }) => [
    ...node(OLD_X, cy, R, label, 26),
    ring(120, cy, 52, 38),
    text(120, cy, pct, { size: 22 }),
  ]),
  text(OLD_X, 1230, "35% margin", { size: 24 }),
  text(OLD_X, 1285, "$100,000 revenue", { size: 24 }),
  text(OLD_X, 1340, "$65,000 variable expenses", { size: 24 }),
  text(OLD_X, 1395, "$35,000 profit", { size: 24 }),
  underline(215, 1415, 390),

  // The new way, two circles instead of four.
  text(NEW_X, 210, "The New Way", { size: 48 }),
  text(NEW_X, 270, "6 to 7 figures", { size: 20 }),
  underline(815, 288, 950),
  text(NEW_X, 330, "flywheel", { size: 22 }),
  ...node(NEW_X, 460, R, "Attention", 26),
  ...node(NEW_X, 800, R, "AI +\nSystems", 26),

  // Old collapsing into new. Drawn after both columns exist, because an arrow
  // landing on a circle nobody has seen yet reads as a mistake on camera.
  arrow(415, 340, 760, 430),
  arrow(415, 540, 765, 480),
  arrow(415, 780, 765, 795),
  arrow(415, 1000, 760, 870),

  // What the new column costs, which is the whole argument.
  text(1050, 460, "7%", { size: 22 }),
  text(1290, 400, "Instagram - $2,000", { size: 24 }),
  text(1290, 455, "YouTube - $2,000", { size: 24 }),
  text(1290, 510, "Flywheel Ads = $3,000", { size: 24 }),
  underline(1330, 528, 1420),
  text(1075, 800, "5%", { size: 22 }),
  text(1320, 800, "Systems Operator = $5,000", { size: 24 }),
  underline(1385, 818, 1475),

  text(NEW_X, 990, "88% margin", { size: 24 }),
  text(NEW_X, 1045, "$100,000 revenue", { size: 24 }),
  text(NEW_X, 1100, "$12,000 fixed expenses", { size: 24 }),
  text(NEW_X, 1155, "$88,000 profit", { size: 24 }),
  underline(795, 1175, 970),
];

export const oldWayNewWay: El[] = beats.map((el) => ({ ...el, y: (el.y as number) + BAND }));
