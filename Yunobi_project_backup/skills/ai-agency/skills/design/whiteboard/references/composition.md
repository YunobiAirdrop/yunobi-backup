# Colour and layout rules

## One hue per concept

A board with several parallel ideas gets a colour per idea, from `HUES` in `src/scene.ts`
(`indigo`, `amber`, `rose`, `green`, `teal`, `violet`). Each entry is a stroke, a pale fill tint,
and a label dark enough to read on that tint: `node(cx, cy, r, name, size, HUES.amber)` gives a
filled circle with a readable caption.

**Colour what differs; leave everything else `INK`.** Four spaces, five stages, three products
are parallel concepts, sorted by colour before a word is read. Prose in six colours is
decoration, not a concept.

**The hue is the concept's identity, across the whole board and the set.** Give a caption the
same hue as its node, and an arrow leaving a node that node's hue, so a group reads as a group. A
second board covering the same concepts keeps the same assignment: recolouring the same four
ideas across one video costs more than it buys.

**One monochrome board is still the default.** Reach for `HUES` when the board is a taxonomy or a
comparison. A board that is one argument in three beats stays `INK` with `HIGHLIGHT` for emphasis.

## Composition

**One column per beat of the argument.** Declare the centres as constants (`const STACK = 380`) and
place everything relative to them. Two or three columns fill a frame; four is too wide to read on
camera.

**Captions sit beside a node, never on it.** Text is centred on its `(cx, cy)` and its width is
roughly `longest_line * fontSize * 0.52`, so a caption's half-width plus the circle radius decides
the offset. Getting this wrong is the most common defect and the layout gate in `SKILL.md` catches
it.

**An analogy always carries the real name under it, smaller.** "The stockroom" gets "Supabase", then
"a database, with logins", in a smaller, darker line. A table of analogies gets a "Means" column
beside "Picture it". The author, 23 Sep 2026: *"I love the analogies, but also make sure that you put
what it actually is."* The mapping rules are the Analogies section of `motion-design`'s
`references/figures.md`.

**Rings and underlines are the emphasis budget.** One `ring` for the single number the board is
built around, `underline` for a title and for a total that has been ruled off. More than two rings
and none of them mean anything.

**Show arithmetic as a sum, never as a total.** A board is the one surface where the working can be
on screen: the parts, a rule across, then the result. Quoting the result alone throws away the
retention that the calculation buys.

**The talking points ride along as their own board, at negative x.** Build them with `paragraph`,
which anchors at the top-left, and push them separately so they land in the same room without
touching the diagram. **Bullets, never prose**: the opening and closing lines are said as written and
the middle is spoken live, so a written-out middle gets read out on camera. `video-script`,
`references/note-shape.md`, owns that split.
