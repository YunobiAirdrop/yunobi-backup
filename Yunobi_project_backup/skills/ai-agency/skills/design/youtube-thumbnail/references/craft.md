# The craft layer: depth, light and the floating object

Step 5 of the workflow: [`niche-evidence.md`](niche-evidence.md) answers **what goes in the
frame**, never **why two frames holding the same things look one professional and one
homemade**. That gap is where most rejected drafts die.

The read behind this file: **Higgsfield AI** (`@HiggsfieldAI`, 133 uploads), banded top
24 against bottom 24 on the same channel and period, 19 August 2026. A different niche
from ours, deliberately (below).

## 0. Evidence transfers by layer, never wholesale

The rule that governs every other line in this file. A thumbnail carries two independent
layers, and they generalise differently:

| Layer | What it holds | Does it transfer between niches? |
| --- | --- | --- |
| **Claim** | subject, expression, words, what is promised | **No.** Audience-specific. |
| **Craft** | depth, light, lens, type placement, how objects sit in space | **Yes.** Physics and perception. |

Higgsfield's winners run shocked faces, `$1280/day` on the frame and `INSANE` in the copy:
every one a **measured control marker in our niche**, importing them makes the frame
worse. Their *lighting and layering* is the same lighting and layering that makes any
photograph read as made rather than assembled, and it costs nothing to take.

So: **borrow craft from the best-produced channel you can find, in any niche. Borrow
claim only from your own banded evidence.** Reading a foreign channel for its claims is
how a skill talks itself out of its own 270 frames.

## 1. Clean means depth, not fewer things

The instinct, when a frame looks cluttered, is to delete an element. Usually wrong.

Counted on the Higgsfield bands: winners carry **more** objects than controls, not
fewer. What separates them is that the winners' objects sit on **three distinct depth
planes** and the controls' objects all sit on **one**.

The stack, and every winner has all three:

1. **Far** — the ground. A real place or a simple gradient, pushed dark and thrown well
   out of focus. Never a flat fill.
2. **Mid** — the subject. The only genuinely sharp thing in the frame.
3. **Near / behind** — one floating object, crossing the subject's silhouette.

A control puts a person and a logo side by side, both sharp, both on the wall: two elements,
and it reads busier than a winner holding four, because the eye has no order to read them
in. **Depth is what "well balanced" actually means when someone says it about a thumbnail.**
Flatness is the fault, element count is usually innocent. This does not loosen the
one-thing rule in step 2: one **subject**, three **planes**.

## 2. Separation is light, never a cutout

Every Higgsfield winner puts a rim light on the subject: a bright edge down the shoulder
and jaw, usually cool, usually from behind. Not one control does.

A cut-out figure dropped on a background has a hard, even, unlit edge, and the eye reads
it as pasted in about 200 milliseconds even at 320 pixels wide. The rim is what buys the
figure a place in the room. It is one instruction and it is the highest return per word
in the whole prompt.

Three lights, and that is the whole recipe:

- **Key**, soft, from the side the face is turned toward.
- **Rim**, harder and cooler, from behind the opposite shoulder.
- **Spill**, from whatever is floating nearby, landing on the near shoulder.

The dark background is not a black fill either. It carries one soft bloom so the subject
is not sitting on nothing.

The corollary about skin:
The note on the frame that was kept: *"the quality of my face and skin looks enhanced
without feeling too much like AI."* Nothing touched the face. What produced that read
was the dark defocused ground plus the rim, which is exactly what a portrait
photographer does to a real person.

So the instruction is **grade, never regenerate**: re-light the photograph and colour it, do
not let the model resample the face. The moment it redraws skin it goes plastic, and skin is
the feature a viewer checks first.

## 3. A floating object has four properties, and needs all four

This is the single most common failure in our own drafts, and it has a name: the object
is *placed* rather than *lit*. A 3D app tile in a neat panel beside the head is a
sticker. The same tile, bigger and one step back, is a scene.

An object floats when, and only when, it:

1. **Occludes, or is occluded.** Some part of it goes behind the shoulder, the hair or
   the hand. An object that touches nothing is a badge.
2. **Tilts.** 10 to 20 degrees off-axis, in perspective. Square-on to camera is a UI
   element; tilted is a thing in a room.
3. **Glows onto its neighbours.** Its colour lands on the near shoulder and blooms on
   the wall. Light that stops at the object's own edge is a sticker's light.
4. **Casts.** A real soft shadow on the surface behind it.

Miss one and it reads pasted. Miss all four and you have built the control frame.

Size it at **30 to 60% of frame height**: below 25% it is decoration the eye never goes to, the timid version is what looks cheap, not the bold one. At the top of the range, let it run off the top of the frame: cropped reads as being in the room, fully contained reads as placed on the picture.

**Size is not what breaks it, contact is.** A tile level with the head and touching nothing is a logo bug at 20% and at 60%; a tile whose edge disappears behind the head, lit and casting, is an object at both. Check occlusion, not percentage.

**Mirror it when its perspective fights the subject.** A 3D asset is rendered at one fixed three-quarter angle; behind a head turned the other way, two vanishing points disagree and the frame reads wrong before anyone can say why. `magick <tile> -flop`, kept in the run's scratchpad rather than over the owned asset.

Where it goes: behind the shoulder, or behind the head. **Not** beside the head at the same scale as
the head, which is the arrangement that reads as a logo bug, and not centred behind the
head symmetrically, which reads as a halo.

## 4. Type sits in the plane too

The winners' type is one of two things and never in between:

- **Bare heavy sans**, white, with only a soft shadow, laid over a dark defocused region
  of the ground.
- **A solid tab**, square corners, when there is no quiet region to sit on.

The control shape is small, thin, centred type in the middle of the frame with a logo
lockup above it. Nine of twenty-four controls; zero winners.

Placement is the opposite third from the subject, vertically centred or high. One
accent colour touches one word at most.

## 5. Consistency is in the treatment, not the layout

The Higgsfield wall reads as one channel at a glance because the palette, the rim light
and the type system repeat on every frame. The **compositions** do not repeat: hands,
laptops, astronaut suits, side profiles.

This qualifies the anti-pattern about template reuse. Reusing a *layout* decays CTR
through pattern fatigue. Reusing a *treatment* is what builds the recognisable wall that
makes a subscriber stop. Hold the light recipe and the two working colours constant;
change what is in the frame every time.

## 6. The prompt block

Craft translates into roughly six lines. Paste them under the subject description in the
[`rendering.md`](rendering.md) template; they are the part that does not change between
concepts.

```
Depth: three separate planes. The room sits far behind, pushed dark and well out of
  focus. He is the only sharp thing in the frame. The <object> floats in the middle
  distance, in front of the wall and behind his shoulder, with his shoulder and hair
  overlapping its lower edge so it sits in the room rather than on top of the picture.
Light: soft key from the left on his face; one cool rim light down his right shoulder
  and jaw that separates him from the wall; the <object> emits its own <colour> light,
  which lands on his shoulder and blooms softly on the wall behind it, and it casts a
  real soft shadow onto that wall.
```

Add to the `Avoid` line, alongside the claim-level bans:

```
a flat cut-out pasted look, an object square-on to camera, a logo bug beside the head
```

## 7. Checking it

Three checks, all at full resolution, all cheap:

- **Trace the edge.** Follow the subject's outline. If the brightness on the inside of
  the line is the same everywhere, there is no rim and the figure is pasted.
- **Find the shadow.** Every floating object owns one. No shadow, no object.
- **Squint at the planes.** Blur hard. Three tonal groups at three sharpnesses means the
  stack is there. One flat group means it is not, and no amount of element deletion
  will fix it.

## The orbit treatment, approved 26 Aug 2026

Translucent panels caught mid-turn around the subject, tumbling at different angles and
depths, each spilling a soft prismatic bloom onto him. Near-black ground, one key, rim light
down the jaw. The verdict: "I do like this concept. It could be used in the future, just not this
time, but I like the rotating things around me. It looks cool."

It is a **treatment**, so it is the thing worth reusing across a wall; the composition under it must still change per video (the anti-patterns list in [`production.md`](production.md)). Two conditions it only works under: the panels carry no glyphs at all, which keeps them a texture rather than a document, and there are three or four of them, because the two-element law counts the orbit as one element while it reads as one motion. It is a generated treatment and the subject is still his photograph, so it is a background job: generate the orbit and the room, composite him in.

## Setting the plate: contrast, type, safe area

- Canvas 1280x720. Judge everything at 320x180, because that is the render that matters.
- One label block, one weight. Heavy condensed sans. White on a dark plate, black on a
  light plate, or a solid colour tab behind the words. Winners in this niche use a
  solid tab far more than an outline.
- Two colours doing work, not five. A third only as a single accent.
- Keep the bottom-right ~15% clear of the timestamp overlay, and the bottom-left ~10%
  clear of the watched-progress bar.
- **The 50% test, for TV.** On the TV app's home and suggested rows only the **top portion** of
  a frame is on screen until the viewer presses down on the remote. Cover the bottom half: is
  there still enough to say what the video is about and to earn that press? If not, move the
  subject and the type up, or put a line in the top third. Check the channel's own exposure at
  Analytics -> Audience -> Device type; at 10% TV or more this outranks a composition you prefer.
  It bears on `placement` directly: `bottom-left` type is invisible to those viewers.
- **Squint test.** Blur it until the words are gone. If the one thing from step 2 still
  reads, it passes.

