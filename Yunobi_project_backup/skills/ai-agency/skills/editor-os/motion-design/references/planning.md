# Registers, reading the cut, and planning a video's b-roll

How a set of clips is decided before any one of them is built. SKILL.md holds the value test; this
holds which register, the clock, how much, where, and the arithmetic that checks your own judgment
after the fact.

## Five registers in two families

**The first four are the motion design and the fifth is the b-roll.** Motion is drawn here in
Remotion and ships from the `Motion` folder; a borrowed shot is found, clipped, credited and ships
from `B-roll`. Keeping the word "b-roll" for both is what let a rights-gated borrowed frame sit one
drag from a paid build.

What to build is one of five, chosen by what the clip does to the picture rather than what it looks
like:

- **A clip that replaces the picture.** A full-frame graphic, cut in whole, standing on its own
  ground. Words stay to uppercase labels, per `type.ts`.
- **A clip that sits on the picture.** An overlay keyed over his face; he stays on screen and the
  words on top are the list he is reciting. Sentence case, brand type, read as text.
- **A figure.** Boxes and arrows for a structure, or a two-column bridge for an analogy. Worth
  building only when the arrangement says something the sentence did not.
- **A rendered object.** Real 3D, keyed over him, for a beat where the viewer has to believe it is
  an object rather than a diagram of one. Costs several times a flat frame; two or three per video.
- **A borrowed shot.** Footage that already exists, cut in whole and muted for three to six seconds.
  Its picture belongs to somebody else, so where it may ship is decided by the destination and
  recorded in a ledger.

All five are worked in **[figures.md](figures.md)** (the first three: replaces, overlay, figure,
plus the rendered object), and named registers (code-walk, introduction, hand-drawn, shorts-board)
in **[registers.md](registers.md)**, plus the two landscape registers with their own files,
[long-take.md](long-take.md) and the live screen inside it.

**Whatever the register, a landscape clip ships in two frames.** 1920x1080 to replace the picture
and 960x1080 to sit beside his face, opaque and alpha each, four files per clip. The narrow one is
the figure stood on end rather than the wide one shrunk. The frame constants and the hash check that
proves the wide render did not move are in [craft.md](craft.md).

## Read the cut, not the script

The clock comes from the edited video's transcript, never the written script. Export the SRT of the
cut, and compare the cut's duration against the raw take.


- Equal durations mean the take has not been cut and there is no clock yet. Build for the beats you
  can name, and say which ones are waiting.
- Different durations mean a cut exists. Its SRT is the only clock; the written script is a draft of
  what someone intended to say, and what got said is usually longer, differently ordered, and full
  of asides that want a face rather than a graphic.
- The editor may recut while clips render. Diff the line timings immediately before committing
  filenames, because those names are write-once.

**Unless there is no cut, because there is no read.** A product film has no transcript, so its clock
is the bar of the track: measure it once with `scripts/teardown.py tempo <track>` and build
`beats.ts` in multiples of it. [product-film.md](product-film.md) holds the rest of that genre, and
overrides this section, the type rules and the sound rules for as long as the film has no voice on
it.

Derive per beat: start timecode, end timecode and the sentence. The clip is as long as the sentence
it serves, minus any mid-beat aside that wants his face back.

## Search what exists before designing anything

Open every clip with a header comment that quotes the line it serves and argues its design. That
makes your own clip library searchable: grep it for the line you are about to build for before you
design anything from zero.

- Under about 40 percent on a talking-head explainer, look again for beats you were lazy about. If
  the second pass finds nothing, the number stands and you say why.
- Over about 60 percent, the person selling it has disappeared behind his own graphics. Cut the
  weakest, starting with any clip whose value-test answer needed more than one sentence.

**The band does not apply to every video.** A product tour where the presenter demonstrates on
screen is mostly screen by construction: in a 22-minute tour with 13 minutes of screen, the target
is stated against the other nine. State the band you
are working to, against the runtime it applies to.

Balance is separate from coverage and it is the one that gets missed:

- **No stretch over about 45 seconds with no b-roll.** That is where a viewer leaves.
- **No stretch over about 25 seconds with no face.** That is where they stop trusting it.
- **Never two clips back to back with no face between them**, unless the second is the payoff of the
  first.
- **Front-load nothing.** Six clips in the first two minutes and none in the last two is not a plan.

## The story checks

Checks the coverage arithmetic cannot see. The doctrine is in [storytelling.md](storytelling.md).

- **The three through-line lines are at the top of the plan.**
- **The motif returns, changed.** Name the beat it appears on and the beat it pays off on.
- **The open loop opens on a frame and closes on the same frame**, completed.
- **No structure is drawn twice.** Beats that rebuild an earlier figure inherit it instead.
- **The rungs are counted.** A median of 1 is a set of illustrations.
- **Repetition.** Six figures in a row is one idea applied six times, the sixth reads as wallpaper.
- **Borrowed shots.** One in a lesson is a punchline, four is a compilation, none may ship inside a
  paid product without a licence check.
- **Words on a background.** Past roughly a third of the plan, the video has stopped drawing and
  started subtitling itself.

Build in plan order. If only some beats are being built this session, say which in the plan and
leave the rest with their verdict written.

## One beat, one clip, three designs

- **One clip serves one sentence.** A payoff clause folded into the tail of the previous clip is a
  payoff nobody sees.
- **Ship three competing designs per beat**, at identical frame counts, so they drop into the
  timeline interchangeably.
- **A second design is a second reading, not a second layout.** Two designs on different rungs of
  the literalness ladder are a real choice; three arrangements of the same content are one design
  rendered three times.
- **Let them disagree.** A single "correct" option is a guess presented as an answer.

## Timing

Put the shared clock in one `beats.ts` per video, keyed by beat, derived from the SRT. Clips import
from it, so retiming the whole set is one edit, not fifteen.

- Every schedule constant is a named frame number at the top of the file, never inline.
- The resolve happens before the cut. Work out when the last element lands and leave hold frames
  after it.
- Phases that reference each other's final geometry must not overlap.

## Where a graphic lands against the word

The two arrival/exit laws off a measured nineteen-minute reference, the beat-frequency tiers and the
mechanisms that fill the clock between them are in [beat-devices.md](beat-devices.md), "Where a
graphic lands against the word".

## The line he pastes is not the line that is spoken

**He copies a scene out of the editor and the copy brings the ignored words with it**, struck
through in grey and absent from the export. On M0 L1 that cost one beat a sentence and another every
word of it. The paste points at a place in the cut; it is not the script. Check
`getComputedStyle(...).textDecorationLine` per text node before building anything.

