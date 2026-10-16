# The template library

Step 5c, and it is the step that decides whether a wall of frames looks like one
channel or like one model's mood on six different days.

**A template holds everything that is not about this video.** The camera, the
ground, the light, the palette, the depth rules, where the type sits and what is
banned. A concept fills the slots. Same template plus same slots gives the same
prompt, every time.

Stated 26 Aug 2026: *"we need some sort of thumbnail system or thumbnail template
because otherwise we will never get consistently great results and we need the
skill to learn its template."*

Keep the library, the schema and the compiler in one file, locked by a test. Read it, do not
paraphrase it. A template lists its slots, its negatives and the frames it has shipped, and the
compiler turns template plus slots into the prompt text you hand the renderer.

## Why the prose fields were not enough

The concept generator returned `subject`, `background` and `foreground` as three
paragraphs. Three paragraphs cannot be reused, so every run re-decided the camera,
the ground, the light and the depth, and the good frames taught the next run
nothing. That is the whole diagnosis. A frame that shipped and a frame that was
rejected were written by the same instructions on the same day.

The fix is not a better paragraph. It is moving every decision that is not about
this video out of the paragraph and into a named object, and leaving the concept
holding only what changes: the claim, the payoff, the words, and the slots.

## The five

| id | variant | route | carries |
| --- | --- | --- | --- |
| `cinematic-world` | face | edit-pass, google | a position or a change of mind |
| `real-artifact-hold` | face | edit-pass, google | here is the thing, and I vouch for it |
| `artifact-fills-frame` | faceless | composite, no model | the thing itself is the argument |
| `object-in-daylight` | faceless | generate, google | one concrete thing stands for the idea |
| `held-object` | face | photo, no model | I made this, and here it is in my hand |

Three have shipped a frame. Two are proposals, and the difference matters: **a
template with an empty `shipped` list is a proposal, not a template.** Never bet
all three concepts of a set on proposals.

**Every template runs on the Gemini lane.** The OpenAI request shape exists in
`@heyramzi/ai` and `provider: "openai"` would reach it, but this workspace holds no
`OPENAI_API_KEY`: the key pasted on 26 Aug 2026 came back 401 `invalid_api_key`, and the
call was to drop it rather than replace it. `object-in-daylight` was written for
OpenAI and moved to google the same day, which cost nothing because nobody is in its
frame either way.

Two tests hold the line: no `face` template may name `openai`, because that model
resamples the canvas and returns a lookalike where Gemini keeps the photograph; and **no
template may name a provider this workspace has no key for**, because a template pointed
at a dead lane fails at render time with the assets already built.

## The route is the render-mode gate, made mechanical

`photo` and `composite` call no model at all. `edit-pass` hands the model a real
plate and asks it to keep the face and rebuild the world. `generate` draws from
nothing real and never carries a person. The gate the SKILL used to state in prose
is now a field, and the test that no `face` template sits on `openai` is that gate
with teeth.

## The slots can overrule the template, and nothing warns

Verified 26 Aug 2026 on `object-in-daylight`, whose negatives ban a second object: a slot
reading "a notebook **beside a cold cup of coffee**" returned a notebook and a mug, correctly,
because a specific instruction beats a general ban and the compiler cannot tell the two apart.
That precedence is right, and it is the author's job to notice. **Read a template's `negatives`
while you fill its slots, not after the render comes back.**

## How the library learns

**A template is promoted, never invented.** The sequence is fixed:

1. A frame ships. It is kept.
2. Write down what actually produced it: the route, the camera, the ground, the
   light, the depth, and which decisions were made by hand rather than by prompt.
3. If an existing template produced it, append to that template's `shipped` list:
   the date, the frame, and **the one thing this run taught that the template did
   not already say**. That last field is the point. "Rendered fine" teaches
   nothing; "keep a zone clear in the edit pass and composite the real capture
   into it afterwards" is why the template exists.
4. If no existing template produced it, add a sixth, with `shipped` holding that
   one frame.

**A rejected frame edits a template, it does not add one.** When a frame is crossed
frame off, the fault belongs in the template's `negatives`, or in
`STANDING_NEGATIVES` when it is a fault any composition could make. A fault
recorded only in `learned-patterns.md` is a fault the next generation will make
again, because the generator reads the templates and not that file.

Both writes go to `thumbnail-templates.ts` **before the turn ends**. A learning
that stays in the conversation is lost when the conversation ends.

## What the generator sees

`thumbnail-concepts.ts` prints the whole library into its prompt, with every
slot's `asks` and its `example`, and its schema **requires** `templateId` and
`templateSlots` on a fresh set. A concept may not decline to pick one. The three
concepts use three different templates wherever three fit, because two concepts on
one template are two draws of one frame.

The stored shape keeps both fields optional, because every set written before
26 Aug 2026 predates the library and `parseThumbnailConceptSet` treats a set that
fails the schema as absent.

**Change the library and change the generator's reading of it in the same
session.** They are one system, and the drift is silent: a generated concept looks
finished whatever it was built from.
