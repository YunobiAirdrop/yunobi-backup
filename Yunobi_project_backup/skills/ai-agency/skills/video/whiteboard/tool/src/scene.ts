/**
 * Minimal builder for Excalidraw scene files (.excalidraw).
 *
 * The output opens in ExcalidrawZ on iPad/Mac and on excalidraw.com, with every
 * element still editable: drag a circle, retype a number, draw over it with the
 * Pencil.
 */

export type El = Record<string, unknown>;

/**
 * The two colours every board is drawn in. INK is the explanatory stroke and
 * every label; HIGHLIGHT is the marker pass, the ring and the underline.
 *
 * Put your own brand here, as plain hex: Excalidraw stores hex and nothing
 * else, so a token in a stylesheet has to be converted rather than referenced,
 * and these are the only two lines to change when the palette moves.
 */
export const INK = "#414fd2";
export const HIGHLIGHT = "#f0503d";

/**
 * One hue per concept, for boards that carry several parallel ideas the viewer
 * has to tell apart at a glance rather than by reading. INK stays the default
 * for everything explanatory and HIGHLIGHT stays the highlighter, so a coloured
 * group reads as a group instead of as decoration.
 *
 * Each entry is the stroke, a pale tint to fill with, and a darker label that
 * survives sitting on that tint.
 */
export const HUES = {
  indigo: { color: "#4c6ef5", fill: "#dbe4ff", labelColor: "#3b5bdb" },
  amber: { color: "#f08c00", fill: "#ffec99", labelColor: "#e8590c" },
  rose: { color: "#e64980", fill: "#fcc2d7", labelColor: "#c2255c" },
  green: { color: "#40c057", fill: "#b2f2bb", labelColor: "#2f9e44" },
  teal: { color: "#20c997", fill: "#c3fae8", labelColor: "#0ca678" },
  violet: { color: "#7950f2", fill: "#e5dbff", labelColor: "#6741d9" },
} as const;

/**
 * The house look, one switch for every board.
 *
 * WHY it is a switch and not a constant: the sketchy stroke and the handwriting
 * face are Excalidraw's defaults, not a decision this repo ever made on the
 * merits, and they are the whole of what "looks like Excalidraw" means. Both are
 * per-element properties in the JSON, so the look is ours to set. Nothing else
 * about the pipeline changes with it.
 *
 * - `clean`: straight strokes and Nunito for the figures, with the terra
 *   highlighter left rough. The diagram reads as drawn rather than doodled, and
 *   the only hand-drawn marks left are the ones standing in for a marker pass.
 * - `hand`: the original, rough.js everywhere and Excalifont throughout.
 */
export type Look = "clean" | "hand";

/**
 * Excalidraw font family ids.
 *
 * WHY the legacy numbers: current Excalidraw numbers its faces 5 Excalifont,
 * 6 Nunito, 7 Lilita One, 8 Comic Shanns, while 1, 2 and 3 are the original
 * Virgil, Helvetica and Cascadia. Every build still understands the legacy
 * three, and an older renderer handed a 7 falls back to its default, which is
 * the handwriting face and therefore the exact look we are leaving. So the two
 * ids in use stay legacy, and the modern ones are listed for trying by hand.
 */
const FONTS = {
  /** Excalifont on current builds, Virgil on old ones. Both handwriting. */
  hand: 1,
  /** Nunito on current builds, Helvetica on old ones. Clean sans either way. */
  sans: 2,
  /** Lilita One, a heavy display face. Current builds only. */
  display: 7,
} as const;

/**
 * `figureRoughness` is rough.js sketchiness on circles, boxes, arrows and
 * connectors, where 0 is a straight stroke.
 */
const LOOKS: Record<Look, { figureRoughness: number; font: number }> = {
  clean: { figureRoughness: 0, font: FONTS.sans },
  hand: { figureRoughness: 1, font: FONTS.hand },
};

/** Change this one line to reskin every board, then `pnpm build`. */
export const LOOK: Look = "clean";

const FIGURE_ROUGHNESS = LOOKS[LOOK].figureRoughness;
const FONT = LOOKS[LOOK].font;

/**
 * Sketchiness for the emphasis marks, the highlighter ring and the underline.
 * Stays rough in both looks: a straight terra bar reads as a UI rule, and the
 * mark is meant to read as something a person drew on top afterwards.
 */
const EMPHASIS_ROUGHNESS = 2;

let seq = 0;

/**
 * Version stamped on every element this run, seconds since the epoch.
 *
 * WHY it is not a constant: a receiving client keeps whichever copy of an id
 * carries the higher `version`, and bumps its own copy every time it touches
 * one. With a hardcoded `version: 1` a re-push tied or lost against the copy
 * already in the room, so a rebuilt board silently failed to replace itself and
 * the fix never appeared on screen. Ids stay deterministic, which is what makes
 * a re-push replace rather than duplicate; only the version moves.
 */
const VERSION = Math.floor(Date.now() / 1000);

function base(type: string, x: number, y: number, width: number, height: number, extra: El): El {
  seq += 1;
  return {
    id: `w${seq.toString(36).padStart(4, "0")}`,
    type,
    x,
    y,
    width,
    height,
    angle: 0,
    strokeColor: INK,
    backgroundColor: "transparent",
    fillStyle: "solid",
    strokeWidth: 2,
    strokeStyle: "solid",
    roughness: FIGURE_ROUGHNESS,
    opacity: 100,
    groupIds: [],
    frameId: null,
    index: `a${seq.toString(36).padStart(3, "0")}`,
    roundness: null,
    seed: 1 + ((seq * 2654435761) % 2147483647),
    version: VERSION,
    versionNonce: 1 + ((seq * 40503) % 2147483647),
    isDeleted: false,
    boundElements: [],
    updated: VERSION,
    link: null,
    locked: false,
    ...extra,
  };
}

/**
 * Advance width of one glyph, as a fraction of the font size, for Excalifont.
 *
 * WHY per character rather than one average: a flat factor is set by lowercase
 * prose and then clips every uppercase label, because Excalifont's caps run
 * about a third wider than its lowercase. `MARKETING` in a node came back
 * rendered as `ARKETINC`, cut off at both ends of a box too narrow to hold it.
 */
function glyphWidth(ch: string): number {
  if (ch === " ") return 0.3;
  if ("iljtfrI.,;:!|'`".includes(ch)) return 0.34;
  if ("mwMW@%".includes(ch)) return 0.92;
  if (ch >= "A" && ch <= "Z") return 0.72;
  if (ch >= "0" && ch <= "9") return 0.62;
  return 0.56;
}

/**
 * Width of a hand-drawn glyph run, used to size and centre text boxes.
 *
 * Excalidraw only re-measures a text element when it is edited, so a box that
 * ships too narrow stays clipped until someone double-clicks it. This runs
 * deliberately generous: a box wider than its glyphs is invisible, since the
 * text is centred inside it, and a box narrower than them loses characters.
 */
function textWidth(text: string, fontSize: number): number {
  const longest = text.split("\n").reduce(
    (max, line) =>
      Math.max(
        max,
        [...line].reduce((sum, ch) => sum + glyphWidth(ch), 0),
      ),
    0,
  );
  return Math.max(longest * fontSize * 1.06, fontSize);
}

type TextOpts = { size?: number; color?: string; align?: "left" | "center" | "right" };

function textBox(x: number, y: number, value: string, opts: TextOpts, centred: boolean): El {
  const fontSize = opts.size ?? 20;
  const lineHeight = 1.25;
  const width = textWidth(value, fontSize);
  const height = value.split("\n").length * fontSize * lineHeight;
  return base("text", centred ? x - width / 2 : x, centred ? y - height / 2 : y, width, height, {
    strokeColor: opts.color ?? INK,
    text: value,
    originalText: value,
    fontSize,
    fontFamily: FONT,
    textAlign: opts.align ?? (centred ? "center" : "left"),
    verticalAlign: "top",
    containerId: null,
    autoResize: true,
    lineHeight,
  });
}

/** Text centred on (cx, cy). Multi-line via \n. */
export function text(cx: number, cy: number, value: string, opts: TextOpts = {}): El {
  return textBox(cx, cy, value, opts, true);
}

/** Text block anchored at its top-left, for a column of script lines. */
export function paragraph(x: number, y: number, value: string, opts: TextOpts = {}): El {
  return textBox(x, y, value, opts, false);
}

/** Grey, for marks that address whoever is recording rather than the viewer. */
export const MARGIN = "#adb5bd";

/**
 * Names the video a group of boards belongs to, and rules a line under it.
 *
 * WHY it exists: the canvas is one column of diagrams and a recording session
 * runs down it, so without a marker between groups there is nothing that says
 * which video a board is spoken over.
 *
 * WHY grey, left-anchored and set well above the first board: it has to be
 * unmissable while scrolling and out of the shot once a board fills the frame.
 */
export function banner(x: number, y: number, title: string, width = 3300): El[] {
  return [
    paragraph(x, y, title.toUpperCase(), { size: 40, color: MARGIN }),
    line(x, y + 70, x + width, y + 70, { color: MARGIN, strokeWidth: 3 }),
  ];
}

type ShapeOpts = {
  color?: string;
  fill?: string;
  fillStyle?: "solid" | "hachure" | "cross-hatch";
  strokeWidth?: number;
  roughness?: number;
  opacity?: number;
};

/** Circle centred on (cx, cy). */
export function circle(cx: number, cy: number, r: number, opts: ShapeOpts = {}): El {
  return base("ellipse", cx - r, cy - r, r * 2, r * 2, {
    strokeColor: opts.color ?? INK,
    backgroundColor: opts.fill ?? "transparent",
    fillStyle: opts.fillStyle ?? "solid",
    strokeWidth: opts.strokeWidth ?? 2,
    roughness: opts.roughness ?? FIGURE_ROUGHNESS,
    opacity: opts.opacity ?? 100,
  });
}

/** Wide oval, for highlighter rings around a percentage or a title. */
export function ring(cx: number, cy: number, rx: number, ry: number): El {
  return base("ellipse", cx - rx, cy - ry, rx * 2, ry * 2, {
    strokeColor: HIGHLIGHT,
    strokeWidth: 4,
    roughness: EMPHASIS_ROUGHNESS,
    opacity: 60,
  });
}

/** Rectangle centred on (cx, cy). */
export function box(cx: number, cy: number, w: number, h: number, opts: ShapeOpts = {}): El {
  return base("rectangle", cx - w / 2, cy - h / 2, w, h, {
    strokeColor: opts.color ?? INK,
    backgroundColor: opts.fill ?? "transparent",
    fillStyle: opts.fillStyle ?? "solid",
    strokeWidth: opts.strokeWidth ?? 2,
    roughness: opts.roughness ?? FIGURE_ROUGHNESS,
    opacity: opts.opacity ?? 100,
    roundness: { type: 3 },
  });
}

/** Plain stroke from (x1, y1) to (x2, y2), for figures rather than emphasis. */
export function line(x1: number, y1: number, x2: number, y2: number, opts: ShapeOpts = {}): El {
  return base("line", x1, y1, Math.abs(x2 - x1), Math.abs(y2 - y1), {
    strokeColor: opts.color ?? INK,
    strokeWidth: opts.strokeWidth ?? 2,
    points: [
      [0, 0],
      [x2 - x1, y2 - y1],
    ],
    lastCommittedPoint: null,
    roundness: { type: 2 },
  });
}

/** Straight arrow from (x1, y1) to (x2, y2). */
export function arrow(x1: number, y1: number, x2: number, y2: number, opts: ShapeOpts = {}): El {
  const dx = x2 - x1;
  const dy = y2 - y1;
  return base("arrow", x1, y1, Math.abs(dx), Math.abs(dy), {
    strokeColor: opts.color ?? INK,
    strokeWidth: opts.strokeWidth ?? 2,
    points: [
      [0, 0],
      [dx, dy],
    ],
    lastCommittedPoint: null,
    startBinding: null,
    endBinding: null,
    startArrowhead: null,
    endArrowhead: "arrow",
    elbowed: false,
    roundness: { type: 2 },
  });
}

/** Underline stroke, the pink swipe under a heading. */
export function underline(x1: number, y: number, x2: number): El {
  return base("line", x1, y, x2 - x1, 0, {
    strokeColor: HIGHLIGHT,
    strokeWidth: 4,
    opacity: 60,
    roughness: EMPHASIS_ROUGHNESS,
    points: [
      [0, 0],
      [x2 - x1, 0],
    ],
    lastCommittedPoint: null,
    roundness: { type: 2 },
  });
}

/**
 * Labelled circle: the shape plus its centred caption.
 *
 * WHY: `labelColor` is separate from `color` because a filled node needs its
 * label darker than its own stroke to stay readable on the tint.
 */
export function node(
  cx: number,
  cy: number,
  r: number,
  label: string,
  size = 24,
  opts: ShapeOpts & { labelColor?: string } = {},
): El[] {
  return [
    circle(cx, cy, r, opts),
    text(cx, cy, label, { size, color: opts.labelColor ?? opts.color }),
  ];
}

export function scene(elements: El[]): string {
  return `${JSON.stringify(
    {
      type: "excalidraw",
      version: 2,
      source: "https://github.com/heyramzi/ai-agency",
      elements,
      appState: { gridSize: null, viewBackgroundColor: "#ffffff" },
      files: {},
    },
    null,
    2,
  )}\n`;
}
