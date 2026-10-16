import { oldWayNewWay } from "#src/boards/old-way-new-way.ts";
import type { El } from "#src/scene.ts";

/**
 * Every board, by name.
 *
 * One tall canvas holds the whole registry, and each board owns a band of it in
 * `y`, because a push carries absolute positions and a room can hold every
 * board at once. Keep the map of taken bands here as the registry grows, so a
 * new board is given a free band rather than one that looks free:
 *
 *   old-way-new-way    0
 *
 * `pnpm build` checks every board's bounding box against every other one and
 * exits non-zero on an overlap, whichever board was built, so a band clash is a
 * build failure rather than a mess on the canvas.
 */
export const boards: Record<string, El[]> = {
  "old-way-new-way": oldWayNewWay,
};

/**
 * Ids, keyed to the board and to the element's place in it.
 *
 * WHY not the counter the scene helpers hand out: that counts up in module
 * execution order, so adding one element to one board renumbered every board
 * imported after it, and the next push wrote a second copy of each instead of
 * replacing the one already in the room. It also made import order load
 * bearing, which is a rule nobody remembers. An id built from the board name
 * keeps an edit inside the board that made it.
 */
for (const [name, elements] of Object.entries(boards)) {
  elements.forEach((el, i) => {
    el.id = `${name}-${i}`;
  });
}

/**
 * The boards that belong to one piece of content, so a whole video can be
 * pushed or copied in one go rather than board by board.
 *
 * A piece name is accepted anywhere a board name is, and `all` is every board
 * in registration order. Add a board to its piece in the same edit that
 * registers it, or the piece silently stops being the whole video.
 */
export const pieces: Record<string, string[]> = {
  // The example video: one board, spoken in the order the array is written.
  example: ["old-way-new-way"],
};

/** Board names for a piece, a single board, or `all`. Empty when unknown. */
export function resolve(name: string): string[] {
  if (name === "all") return Object.keys(boards);
  if (pieces[name]) return pieces[name];
  return boards[name] ? [name] : [];
}
