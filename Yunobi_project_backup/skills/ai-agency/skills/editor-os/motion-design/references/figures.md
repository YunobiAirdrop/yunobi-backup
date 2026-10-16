# Figures: diagrams, analogies, overlays and rendered objects

The three registers that are not a full-frame cutaway on its own ground, plus the rendered object.
Each earns its place by *arrangement* rather than by illustration, which is why each fails in its own
distinct way when it does not.

## Diagrams: boxes, arrows, and four ways they go wrong

A box-and-arrow figure is the third of the four things a graphic can add - a structure that has no
name yet - because speech is serial and a frame holds five parts at once.

**Mermaid slop.** Default rounded boxes, a drop shadow, six colours, a font nobody chose. Nothing in
this kit renders a diagram from a text description; `diagram.tsx` is the vocabulary and a clip
composes it by hand.

**Density.** Everything the read mentions gets a node, so eleven arrive and the viewer reads none of
them. **Four to six.** The box you are reluctant to cut is usually the one the read already explained
in words.

**No focal point.** Every node styled the same is a map with no "you are here". Exactly one node
carries the accent - two accents is zero accents.

**Arriving whole.** A finished diagram dropped on screen is a slide the viewer parses alone while he
keeps talking. Nodes land in the order he names them; edges draw after both boxes they join exist.

**The vocabulary**, in `src/diagram.tsx` and nothing else: `Node` (a `Plate` with an uppercase title,
an optional sentence-case sub, `kind="focal"` fills terra, everything else is night with a veil edge);
`Edge` (an orthogonal polyline; `dashed` means a return or a loop closing, and that is the only
semantic difference a line style may carry); `Edges` (the one SVG layer they all sit on - see
`SvgLayer` in `primitives.tsx` for why a bare `<svg>` in an `AbsoluteFill` silently never paints).
Routes are `straight`, `hv`, `vh`, `hvh`, `vhv` - right angles, never curves, which read as a circuit
rather than decoration. A return path takes its own road rather than retracing the forward one.

A node label is **recognised**, not read: uppercase gives every label the same silhouette height. One
trap only a still catches: on a terra focal node the `muted` token equals the fill, so a sub
disappears - check contrast against what is behind the text, never against the palette's idea of
"secondary".

From `cathrynlavery/diagram-design`, three judgments worth keeping and nothing else (its output is a
web page and its paper-and-ink skin is the opposite of a dark motion ground): one accent reserved for
what the reader should look at first, density around 4/10, no generic rounded boxes by default.

**Landscape is not portrait rotated.** A landscape frame gives roughly a third of the
vertical budget and twice the horizontal. Widen the subject to carry the vertical budget rather than
leaving empty side gutters, and check the outer eighth: `SAFE_X` is 200, `SAFE_Y` is 140.

**Verify at the resolve frame of every phase.** The failures here are silent by construction: an
arrowhead drawn past its endpoint and hidden under the node, a line clipped by a portrait-sized SVG
layer, a stroke that runs out before the end of its path. Every one renders clean and typechecks clean.

## Analogies

An analogy is a claim that two structures are the same shape, not a picture of the familiar thing. The
restaurant-as-API illustration shows a waiter; what it does not show is the mapping - that the waiter
*is* the API - so the mapping stays in the voiceover, which is decoration. `AnalogyBridge` in
`src/analogy.tsx` puts familiar on the left, real on the right, one line per pair, landing as he names
them, so the viewer watches "recipe" become "template" rather than hearing it. The line arrives before
the word it buys; the accent is an edge on a whole column, never a fill (three solid terra slabs read
as a colour scheme, not "this one").

**Four tests, and failing any one costs more attention than it saves.** The familiar side has to be
genuinely familiar - kitchens, keys, rent, hiring, traffic. The structures match on at least three
points, or it is a simile that collapses. It has to break somewhere, and the header comment names
where. It cannot already be his own words - if he says "it is like a recipe", drawing a recipe is
decoration.

**Reuse the one you already have.** Pick one familiar world for the whole video (a kitchen, say: recipes,
the pass, the rack) and extend it before opening a new domain. Every analogy breaks somewhere, so name
where: a restaurant's customers order off a fixed menu, while an agency's client asks for what is not
on it.

**When not to use one at all.** An analogy buys understanding of a *structure*, nothing for a
quantity, a consequence or a recognition. If the beat is "twenty percent drives eighty", draw the
twenty percent.

## The listicle re-engineered: four motion architectures

A vertical bullet list is the death of retention: speech reads the items while the viewer's eye jumps
ahead, parses the words, and leaves before the explanation arrives. Four architectures that replace
vertical lists with spatial progression, measured off a creator's long-form systems:

1. **The horizontal spectrum / continuum listicle ("Ranked by Effort / Impact").** A central continuous
   horizontal gradient axis (Lowest Effort -> Highest Effort) with numbered tick marks. Cards alternate
   systematically ABOVE and BELOW the line in a staggered zig-zag layout, doubling readable space. Each
   node is a rich asset card: real smartphone frame thumbnail, bold label, 2-line explanation, creator
   attribution, and view count metric chip. Handles 10-15 items without visual crowding, allowing the
   viewer to scan a continuum of options instead of reading a vertical shopping list.
2. **The multi-phase sliding calendar / sprints.** Multi-month processes or timelines laid out as physical
   monthly calendar grids in 3D perspective side-by-side. The camera glides horizontally across the sprint
   sequence; the active month lights up while questions and milestone badges pop inside the active
   container.
3. **The paired-container anticipation reveal.** For 2-part concepts or dual bottlenecks ("The hard parts
   are [A] and [B]"), render two side-by-side rounded pill containers at the same time. Fill Container 1
   with text immediately while Container 2 remains an empty wireframe container. The empty slot creates
   an instant visual open loop that forces the viewer to anticipate the second answer before it resolves.
4. **The formula equation bar.** Mathematical synthesis: `[topic] + [format] + [visual layout] = Formula`.
   Rendered as luminous interactive pill badges summing into a framework container, mapped directly to real
   persona cards above.

## Overlays: words over his face

Every other clip is full-frame, replacing the picture. An overlay keys over him instead: he stays on
screen, the graphic sits on top of the shot.

**Which register a beat wants.** His face plus a list he is reciting: an overlay - he is the proof and
the words are the index. A structure, a quantity, a mechanism: a full-frame clip, which needs the
whole frame. A screen he is demonstrating: neither - a graphic over real evidence argues with it. An
overlay is the cheaper of the two to be wrong about: a miss costs a few words nobody needed, not four
seconds of video.

**Three registers, in `caption.tsx`.** `GlassCaption` puts words on a frosted pane - reach for it when
the list is long, when it is a set rather than a statement, or the plate behind it is bright or busy.
`PlainCaption` puts words on nothing - one statement, two or three lines, harder to land and better
when it does. `DefocusedCamOverlay` blurs his talking head plate (~20-30px gaussian blur + dark vignette)
rather than cutting away to a full graphic - it keeps vocal presence and speaker cadence alive while
forcing 100% of visual focus onto a foreground conceptual dichotomy, decision fork, or formula. None
is the default; a video that only uses one has a lower third or subtitles.

**Sentence case here, uppercase everywhere else**, decided by what the clip replaces, never by
preference:

| The clip | The type |
|---|---|
| **is** the picture | `type.ts`. Uppercase, tracked out, labels only. |
| **sits on** the picture | `caption.tsx`. Sentence case, brand font, read as text. |

Mixing the two inside one video is what makes a set look like two hands.

**Rows land one at a time, on his words.** Cut the stagger from the read: frames between the first and
last named item, divided by row count. The exception is a list whose rows *compete* rather than
accumulate - every row on screen from frame one, only the spoken one lit, because anticipating which
row lights next beats the surprise of arrival. [planning.md](planning.md) has the measured opacities.

**Three things that only fail over footage**, and all render clean, typecheck clean, exit zero:

- Cream text on a bright wall disappears; a soft shadow does not save it, because a wide blur darkens
  the field, never the glyph's edge. `legible()` is three shadows - a tight zero-offset outline, a
  contact shadow, and the field - the outline is load-bearing.
- The alpha key light behind bare type reads as a grey disc on his wall. Pass `lightStrength={0}` on
  any overlay whose whole content is type.
- `backdrop-filter` cannot make the glass: it samples what is painted behind the element in the same
  document, and an alpha render has nothing there. build the blurred pane out of parts that survive an alpha channel
  (a layered gradient and a faked blur), not a CSS filter.

**The file it ships as.** Descript, like most editors, only keys MOVs: register the alpha composition with
`defaultProps={{ alpha: true }}`, render ProRes 4444, convert to `qtrle`. A Studio export otherwise
inherits h264 and arrives as a black rectangle where the transparency should be.

**Verify against a bright card, not the ground**: a transparent still tells you nothing about whether
type survives. Composite it over `#d8d3c8`, about the value of the wall and sofa behind him - if it
reads there, it reads anywhere in that room.

## 3D

The fourth register: a real rendered object, keyed over him. `src/three.tsx`, on `@remotion/three`.

**When it earns its cost.** A WebGL frame is several times a DOM frame. Reach for it only when the
object is the point - a hierarchy, a volume, a physical thing the viewer has to believe is an object
rather than a diagram of one. The tell is reflection: light genuinely travelling across a curved
surface, which only a renderer does. Two or three per video; a video where every graphic is rendered
has stopped being his video.

**The environment, not the geometry, decides whether it looks bought or made.** A `meshPhysicalMaterial`
with no environment renders as flat plastic however many lights are added - more lights only make it
brighter. Three lights, then stop: a key that models the form, a rim that separates it from what it is
keyed over, a low fill so the underside is not black. `RoomEnvironment` ships inside `three` and is
generated in memory, no file to vendor. The material is two layers, a coloured metal body under a
clear coat - one layer gives a mirror or plastic, and the reference is neither.

**Two wiring bugs that both look like a taste failure**, neither errors, both survive a clean
typecheck: a module-level handle on the renderer is not reactive (stash nothing from `onCreated`; use
`useThree`), and an effect that assigns `scene.environment` inside `useEffect` misses Remotion's frame
capture, so the render comes back byte-identical to one with no environment. `PMREMGenerator.fromScene`
is synchronous - assign during the render pass and skip `delayRender`. Anything genuinely async (a
loaded model, an HDRI, a texture) does need it.

**Alpha**: `gl={{ alpha: true }}` and no `scene.background`, composited into the same ProRes-to-qtrle
MOV as every overlay. Do not add the brand grain; a rendered surface carries its own specular detail.
Verify the way every overlay is verified: a WebGL edge clean on ink can carry a dark fringe over a
light wall.

**The camera**: long glass, not wide. The default 75-degree field of view gives a small object
aggressive perspective; a phone at that distance is nearer 25 degrees, which is what `Stage` defaults
to.
