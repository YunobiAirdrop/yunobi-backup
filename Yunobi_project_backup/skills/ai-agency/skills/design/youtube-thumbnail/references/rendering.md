# Rendering a thumbnail programmatically

Step 7, execution route B. The build order from step 6 is the input; nothing here re-decides the concept.

## Do not draw his face

**A face variant is composited, not generated.** `--photo` takes the face plate, conforms it to
1280x720, sets the words in Manrope 800 and passes them behind the real subject. No model is
called, and the likeness is perfect because it is not a likeness.

```bash
# composite the plate rather than calling a model at all
```

`cutSubject` lifts the subject off the RENDERED plate, so a generated frame contains zero photographed pixels of him: the plate
was only ever a reference. The verdict, 26 Aug 2026, on a frame built from `deadpan-wide-left-02`:
"it doesn't look like me at all. It looks AI generated way too much." No model choice fixes it.

Generate only for what does not exist to be photographed: an object, a figure, a room we do not
have. Never to obtain him. When the background must be a **real artifact** (a screenshot, a board,
a dashboard), composite his real cut-out face onto it: [`composites.md`](composites.md).

## Which model

**The model, the tier, the price and the ban live in** `vibe-kit/ai-doc/references/image-generation.md`. Ask `@heyramzi/ai` for a tier, never type an id, and `large` (Nano Banana Pro) is banned outright, so `--model=pro` throws. `render-thumbnail.ts` draws on the `medium` tier and takes `--model=<id>` for a test only. Ideogram's type accuracy and FLUX.2's photorealism do not reach here: the words are set in real Manrope, and neither carries the face compositing that keeps one person identical across a wall.

**OpenAI re-rendered the person; Gemini keeps the photograph.** Tested twice with `gpt-image-1` and `gpt-image-2`. Editing a finished frame, `gpt-image-2` returned a lookalike (narrower jaw, different beard) and `gpt-image-1` cropped the type off. Building from the source plate it did far better (convincing likeness, excellent tile lighting, correct card) but still not the photograph: beard filled in, brow heavied, face idealised. Gemini returns the photographed face unchanged in both cases, because it composites where OpenAI resampled the canvas. On a channel where the same face appears weekly, a per-frame re-render drifts.

**That ban is this skill's, it is about the face, and it holds.** A thumbnail carrying him goes to `gemini-3.1-flash-image`, always. A workspace-wide ban sat on top for one morning (1 Sep 2026) and was lifted the same day, so objects and illustration with nobody in frame may go to `gpt-image-2` where a call site names it. **Seeds do not work**: `generationConfig.seed` is accepted and ignored by `gemini-3.1-flash-image`, the same seed twice returns two images (verified 19 Aug 2026, same prompt, hashes differ); the substitute is the edit pass. No Gemini image model returns alpha, so key the backdrop off with `logo3d/key.ts`.

## Changing one thing in a frame you already like

The most common request after a good render is "this one, but ___". Do not re-render the brief:
you will get a different face, card and crop, because there is no seed. **Hand the finished PNG
back as the first attached image and edit it.**

**The same pass builds a cinematic frame from a flat plate, and this is the route to reach for.**
Hand the model a flatly-lit `--photo` plate, tell it to keep his face, hair, beard, expression,
hand and pose pixel-for-pixel, and transform everything else: a near-black defocused studio, a warm
rim light, glowing panels. Gemini keeps the photographed face and generates the world, which the
flat composite in [`composites.md`](composites.md) cannot reach. Verified 26 Aug 2026 on the
"hiring won't fix it" base at `tier: large`: four samples, the face held in all four. Call
`generateImage(router, { references: [{bytes, mediaType}], tier: "large" })` and set the type
afterward. Say "keep his facial detail, do not plasticise the skin."

```
Edit the FIRST attached image. It is a finished YouTube thumbnail and it is already correct.
Make exactly ONE change: <the change, with its geometry and its light>
Everything else is unchanged and reproduced pixel for pixel: his face, hair, beard, expression,
skin, clothing and hand; <every other element, with position and content>; the framing and crop.
Do not redraw the face. Do not restyle. Do not re-typeset the text. Do not change the crop.
```

**Naming what must not change is the whole job.** A model asked only to enlarge a logo will cheerfully re-typeset the overlay and re-crop the frame. List the survivors explicitly, then take three samples. The edit pass is the one case still on Pro, because nobody has re-run it on Nano Banana 2 since 25 Aug.

## The template is what a render is built from

A concept carrying a `templateId` is rendered from [`templates.md`](templates.md), not from its prose fields: `buildPrompt` hands off to `compileTemplatePrompt`, and the three paragraphs are only there for the wall and for a designer handoff. The template names the provider, so `--provider=` is for a deliberate comparison and nothing else.

## The client, and the key order

Put every image caller behind **one module**. Import
`googleImageClient()` and `NANO_BANANA_MODEL` from it; do not build a provider by hand and do not
add a new key anywhere. It walks three lanes in order and only changes lane when the lane itself
failed: a quota answer (429, or a 403 naming `RESOURCE_EXHAUSTED`) or a rejected key (401, or a 400
naming the key). A malformed request is returned as is, because retrying it on the next key just
spends the next key.

1. `GOOGLE_GENERATIVE_AI_API_KEY`: direct to Google AI Studio. The priority lane.
2. `GOOGLE_GENERATIVE_AI_API_KEY_BACKUP`: direct, a second key. Leave it unset rather than setting
   a dead one.
3. `CF_AIG_*`: the Cloudflare AI Gateway, which holds its own Google key.

**Known state, 26 Aug 2026: the direct Google key is not in `app/.env.local` either.** Every image
call lands on lane 3, the Cloudflare AI Gateway, which holds its own Google key: the fallback
doing its job, and the lane every verified render here was drawn on. **OpenAI has no gateway lane,
and that is separate from whether it is allowed.** It is a direct `fetch` on `OPENAI_API_KEY`,
because `/v1/images/generations` and `/v1/images/edits` are their own endpoints. It bills by
returned tokens ($30 per 1M image output tokens, off platform.openai.com/docs/pricing on 26 Aug
2026), so a frame at 1536x1024 costs about $0.008 low, $0.032 medium and $0.125 high. No thumbnail
carrying his face goes there whatever it costs.

Lock the lane order with a test and keep it identical in any second caller. Put callers behind the
same module.

## Filing the result, and generating options

**A rendered thumbnail is filed on its concept**, never handed over as a loose file or a standalone
HTML sheet: the Concepts page at `/youtube/concepts` is the wall the frames are judged on.

The frame is filed against the video's concept record, with the build orders merged into its
metadata; a stored set that fails the schema disappears silently, so read it back before calling it
done.

In the browser the same two writes are `POST /api/youtube/thumbnails` (multipart: `file`, `name`,
`conceptId`, `type`). The mood board's generator is the fastest route to a rendered option: it
reads the concept, resolves the owned assets and writes to the board.

```bash
node scripts/render.mjs --prompt prompt.txt --ref face.webp --ref box.png --out out/a.png
```

It hands the model the owned assets as image parts, so identity is photographic and free. PNGs land
in the **private** `app-assets` bucket, so board nodes point at
`/api/storage/serve-url?bucket=app-assets&path=…&mode=redirect`, never a storage public URL.

## Set the type yourself, and put it behind the subject

**This is wired in since 20 Aug 2026 and is no longer a manual four-step.** Give the concept a
`type` block and the script does all of it:

```json
"type": {
  "lines": ["ClickUp was", "layer one"],
  "placement": "top-left",     // top-left | top-right | left-center | bottom-left
  "shape": "tab",              // tab hugs each line; band bleeds off the left edge
  "plate": "#414FD2",          // brand indigo
  "ink": "#FBF3EF",            // brand cream
  "behindSubject": true
}
```

Its presence forces `No text anywhere in the image` into the prompt, so there is nothing to paint
out, and the size is fitted in the page. `scripts/thumbnail-compose.ts` owns it. For a frame
rendered elsewhere: cut the subject out
with a `cutout <in.png> <out.png>` helper (Apple's
`VNGenerateForegroundInstanceMaskRequest` on the Neural Engine, free, no key, no upload); set real
Manrope 800 through headless Chrome; stack plate, type, subject. The type then lands **behind** the
person: a band that bleeds off the edge and dies behind his head reads as a thing in the room,
where the same band on top reads as a label on a picture. **Occlude the plate, never a glyph**: the
first composite hid the full stop after "it." behind the card, which reads as a typo rather than
depth. The brand face is Manrope 800.

## Prompt in pictures, and what must stay real

**When a reference image exists, stop describing and start pointing.** Hand the model the winner
tile whose composition you are borrowing ("this layout, this subject") and a second image for the
type treatment. The house style is the last ten thumbnails, so consistency comes from those files,
not a written style guide.

**Text inside the frame obeys the same law, and it is the one people try to prompt.** Not the
overlay, which the model sets reliably at four words, but writing on an object: a card, a screen, a
label, a list of names. Prose cannot pin it: the same card described four ways came back with the
wrong row count and different colours. Build the artwork as HTML, screenshot it transparent, attach
it as a reference image, then point: *"the THIRD attached image is the printed card artwork.
Reproduce it exactly: same words, order and colours, correctly spelled. Do not invent, translate,
reorder or add text."* A supplied 3D tile is the same, and degrades the same way (angle and size
limits in [`composites.md`](composites.md)): **say "reproduce that exact object at almost exactly
the angle it is presented in, do not rotate the mark, do not merge the shapes", then crop the mark
at full resolution and look.**

**Grade, never regenerate, and that is what makes skin look expensive.** Ask for re-lighting and
colour, never resampled skin: the full recipe and the corollary about skin is in [`craft.md`](craft.md).

**Do not copy a composition closely enough to be recognisably another creator's.** Change the
subject, the type and the palette; keep the structure. **The `Avoid` line is not boilerplate**:
every item is a measured control marker (see [`niche-evidence.md`](niche-evidence.md)): a second
person, a shocked expression, a readable screenshot, a chart, more than two working colours, a
centred symmetric composition, more than four words of text, a flat cut-out pasted look, an object
square-on to camera, fused or extra fingers.

## When the render comes back wrong

| Symptom | Fix |
| --- | --- |
| Text misspelled | Shorten the string. Four words is the practical ceiling for reliable glyphs. |
| Face distorted | You asked it to change an expression. Go back to a composite. |
| Five things in frame | The prompt described a scene. Name one subject and one accent. |
| Washed out at 320px | Two working colours, and the type on a solid plate, not an outline. |
| Looks like the reference | Change subject, type and palette. Keep only the structure. |
| Quota error on every lane | All three lanes are rate limited. Wait, or add a second direct key. |
