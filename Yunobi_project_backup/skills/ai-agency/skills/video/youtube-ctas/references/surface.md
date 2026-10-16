## The glass surface

`glass/surface.tsx` draws it, and every shape stands on it. Seven layers, because the one that
would do it in a browser is unavailable: `backdrop-filter` samples what is painted behind the
element *in the same document*, and an alpha overlay has nothing behind it, so it returns the blur
of nothing.

1. A gradient rim, 1.5px, bright top-left to dim bottom-right. A flat border draws a box; a
   gradient rim draws a curved surface catching a light. This is the layer that reads most as glass.
2. A hairline ring, indigo at 0.16, outside the rim.
3. Two shadows: 3px contact so it sits *on* the footage, 92px ambient so it floats above it. One
   alone gives a sticker or a cloud, never a pane.
4. A body gradient, lighter at the top, so the fill has a direction rather than a value.
5. An inset top highlight and an inset bottom darkening. This pair is the pane's *thickness*.
6. Frost: `feTurbulence` grain at **3.5%**, plus a soft cream bloom in the top-left. Frosted glass
   is not a flat tint, it is a surface with particles that scatter light unevenly. Grain is the one
   layer with no upper bound that looks obviously wrong, so it creeps; above about 6% the pane stops
   reading as glass and starts reading as a noise texture with a CTA on it.
7. A specular sweep crossing once over 30 frames. The light moves, so the surface reads as something
   with a curve. It never loops, for the same reason the tap ring does not.

The frost is an SVG painted as a **background image**, never a CSS `filter`: `filter` applies to the
whole subtree, so frosting the pane frosts the type inside it. Same lesson as the `boxShadow`-not-
`glow()` rule below.

### The concentric radius rule

**Every curve that wraps a curve shares its centre.** `Glass` takes the *pane's* radius and gives
the rim `radius + 1.5`; each call site sets the pane's radius to the radius of the round thing
inside it **plus the padding around it**. A 53px avatar in 22px of padding gives a 75px pane, not a
62px one. Two curves that do not share a centre read as a mistake even when nobody can name it,
and it is the first thing anybody spots on a finished render.

It falls out that all three shapes are stadiums, because the concentric radius and half the pane
height agree once the round element is the tallest child. When they disagree, the round element is
not the tallest child, and the fix is to grow it rather than to pick a radius between the two.

| shape | round child | padding | pane radius |
|---|---|---|---|
| `CtaSubscribeUnit` | 106 avatar and button (r 53) | 22 | 75 |
| `CtaHero` | 124 disc (r 62) | 40 | 102 |
| `CtaPill` | 82 disc (r 41) | 17 | 58 |

The far padding is larger than the near one on the two shapes that hold type, because at a stadium
end the curve reaches `radius` px inward and the last letter has to clear it.

## Iconography

**Phosphor, at duotone, from `@phosphor-icons/react`.** The kit used to carry six hand-drawn glyphs
traced to look like everybody else's, which made it the only surface here not on the house icon
library.
 Duotone rather than regular or fill: regular disappears at distance on a phone and fill is
heavy enough to fight the type beside it.

**The ghost layer has to be lifted, and there is no prop for it.** Phosphor writes `opacity="0.2"`
into the duotone path as a literal, and `duotoneOpacity` is not in `IconProps` on 2.1.10. At 0.2 on
a saturated disc the ghost is invisible and the icon reads as the regular weight with extra steps.
`glass/icons.tsx` injects one rule matching that literal and lifts it to 0.38.

The brand mark stays hand-drawn. It is the mark, not an icon, and Phosphor does not have it.

**A glyph on terra is ink, never cream.** Cream on terra measures 3.24:1 and fails at any size;
DESIGN.md records this. On indigo, cream is 8.4:1.

## Type

The kit is set in **Space Grotesk**, which the design system assigns the Code / Label role, and a
CTA pill word is a label: short, uppercase, tracked out. It was previously the system stack, which
made these the only surface here not carrying house type.
 Not Manrope: that is the
heading face and nothing here is a heading, the 38px end card title included.

The face shows in the lowercase, so the payoff is concentrated on the channel handle (46px,
tracking -0.9) and the call CTA's sub-label.
 At 42px caps with +4.2 tracking a pill word is
nearly face-agnostic, worth knowing before anybody expects a transformation across all eight.

`font.ts` copies the woff2 out of the app's font folder into `public/fonts/` and holds the render with
`delayRender` until `document.fonts.load` resolves for every weight. Do not swap it for a Google
Fonts URL: a render is a hundred-odd headless frames, and a slow request means the first few come
out in the fallback, which exits zero and looks like a mistake nobody made.
