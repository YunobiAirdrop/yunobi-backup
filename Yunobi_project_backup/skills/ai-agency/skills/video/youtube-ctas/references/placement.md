# Where an overlay sits, and what it says

Placement against YouTube's own clickable elements, and the words each overlay carries.

## Where an overlay sits, and what it says

**The kit ships as three shapes, all centred on `y = 826`.** One shape was wrong: a calendar
booking and a thumbs-up drawn at the same size says they are the same request. The hierarchy lives
in the geometry, which is the one place it cannot be argued with.

| shape | height | clips | what it is |
|---|---|---|---|
| `CtaSubscribeUnit` | 150 | Subscribe, Follow | avatar, handle, and a button that presses at frame 40 and turns into "Subscribed" / "Following" |
| `CtaHero` | 204 | Book a call, Build it yourself, Join the community | the asks that carry an address on a second line |
| `CtaPill` | 116 | Like, Comment, both handles | one line, one badge, no room for a second tier |
| `CtaProduct` | 204 pane | Agency Master, ClickUp Master | `CtaHero`'s pane with the product box standing in front of it |

**`CtaProduct` is the one shape whose subject is an object rather than an action**, so it lives in
`src/product-ctas/` and its box is CSS 3D geometry rather than the shipped packshot. A product signs
with its own mark there, never a stock glyph. It has three transform rules and a hard file-size
budget nothing else in the kit has: [references/product-ctas.md](product-ctas.md).

**Subscribe is a rehearsal, not a description.** "Subscribe" beside a bell icon *describes* the
action. An avatar, a handle and a button that presses and flips to "Subscribed" is the viewer
watching the outcome and then reproducing it. Remotion's own transparent-CTA prompt builds the same
thing. It has no tap ring: a ring has to sit outside the glass pane, which clips its own sweep,
and outside the pane it needs absolute coordinates that move with the handle string.

**A third party's logo on the disc keeps that party's colours.** `accent="platform"` on `CtaHero`
paints the disc the platform's own paper and leaves the slab indigo, because the pane is ours even
when the disc is not. The mark itself lives outside `icons.tsx` — `skool-mark.tsx` is the pattern:
it ignores `Icon`'s `color` prop, reads `size` as a width because it is wider than it is tall, and
carries its provenance in its header. Repainting somebody's logo in our palette is a forgery of the
logo, which is the same argument the subscribe slab already makes.

**The slab is the platform's, so its colour, its wording and its confirm glyph are props.** The
older rule here said the button stays cream because it is borrowing YouTube's affordance, and that
half was right: YouTube's is a solid light slab with dark type, and painting *that* one terra makes
it your button that happens to say Subscribe. What the rule got wrong was reading a constant into
a borrowing. TikTok's slab is a solid red one saying Follow, hollowing out to Following behind a
tick, so `accent="terra"` on `cta-follow-tiktok` is the same argument rather than an exception to
it — and the tick pops on `scale` rather than borrowing the bell's rotation, because a rotation on a
tick reads as an error. Terra is still off every ask we style ourselves except the discovery call.
`buttonWidth` is set per wording (372 for "Subscribed", 330 for "Following"): the faces cross-fade
at a fixed width so nothing reflows under the press, which means a short word left in a box sized
for a long one swims.

The corner geometry is not deleted, it is kept in the `youtube-ctas-corner` folder at
`left: 120, top: 798`. It is still the right answer for an overlay that runs under a sentence while
the edit continues, because the centre of frame is where the speaker and the screen capture live.
Reach for it when a CTA accompanies a line rather than owns the moment.

Either way, the frame is shared with YouTube's own furniture:

- **The bottom ~90px** is the progress bar and the controls whenever the viewer moves the mouse.
- **The top right** is where the cards teaser appears.

**Never centre an icon above the statement.** `impeccable` names it outright as the most templated
layout there is. The icon goes left of the type on the reading line and the group is what gets
centred, which is also why the type is left-aligned: it hangs off the icon rather than floating.

**A second line is an address, or it does not exist.** The old rule here said every CTA carries a
reason under the ask. It was right that mid-roll CTAs between 55% and 70% of a video measure far
better than end-screen ones, and wrong about what counts as a reason. Five of the seven labels were
invented to satisfy the rule: "New video every week" (three clips) is a promise the channel does not
keep, "It travels further" is false, and "I read every one" is true and about me rather than about
the viewer. All five are cut. Two survive, and both say *where to go*:
the booking URL and "Link in the description". Those clips are the two heroes; every
other ask is a pill, which has no second line to fill. Keep an indication under about 30 characters,
and never track it out or uppercase it, because it is a string the viewer reads and reproduces.

`shine` runs 54 frames, so any clip carrying it cannot be cut below about 80 without truncating its
own chord. Two of the seven carry it, which is what keeps it meaning something. On the subscribe
unit the chord lands on the *press* at frame 46, not on the entrance, so that clip needs 135 frames
rather than 120: the tail has to finish before the exit starts.

The end card is drawn to YouTube's element picker, which snaps to a grid and refuses to sit within
10% of any edge. Off that geometry, a placed element lands beside its own placeholder: two video
slots 560x315 at `left: 700` and `left: 1300`, `top: 383`; the subscribe circle 300px at
`left: 180, top: 390`; all centred on `y = 540`, everything 60px inside the frame. It gets no exit
animation, because fading it takes the clickable targets away while the viewer is reaching.

**The end card's subscribe disc carries the channel's avatar, on the same `avatar?` prop as
`CtaSubscribeUnit` and for the same reason.** YouTube's placed element paints the real channel
picture into that circle, so a bed showing the brand mark under a personal channel's face reads
as two channels for the seconds before the element settles. The default prop is the personal
avatar; omitting it falls back to the mark, which is right for a brand channel whose avatar
*is* the mark.
 The disc needs `overflow: hidden` for the photo to
take the 150px radius. The photo costs about 2.9MiB of qtrle (8.7 to 11.6MiB), all of it in the
20-frame entrance, which is the same bill the width rule describes.

The glass surface, its concentric radii, the icon set and the type ramp are in
[references/surface.md](surface.md).
