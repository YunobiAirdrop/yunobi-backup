## Sound

Every CTA carries its own audio track, generated rather than sampled. `scripts/build-sfx.py`
synthesises the kit into `public/sfx/`, `src/youtube-ctas/sfx.tsx` pairs a voice with a frame, and
`<Sfx name="tap" from={8} />` sits directly above the `interpolate(frame, [8, 24], ...)` it lands
on, so the two move together.

Four rules are what make it read as 2026 rather than 2015:

- **No noise in any voice.** Filtered noise with a moving cutoff is the whoosh, and the whoosh is
  what dates a kit. Every voice is sine oscillators only. Noise appears once, inside the reverb
  impulse, where it is what a room is made of and is never heard alone.
- **A tail is most of what "cinematic" means.** A dry blip reads as a web app, a tail reads as a
  film. It costs one FFT convolution against a synthesised impulse, lowpassed to about 2.2kHz
  because a bright tail sounds like a plugin preset and a dark one sounds like a space.
- **One chord, and the middle left empty.** A major, A2 to A5. Everything sits below 250Hz or above
  550Hz, so a voiceover keeps its range and no CTA has to be ducked in the edit.
- **The width is in the room, not the note.** The dry sine is centred and the two channels are wet
  into impulses built from different seeds, so a clip folds down to mono for about 1dB.

Six voices: `enter` and `exit` (a pill arriving and leaving, written as a rising and falling
interval rather than as air), `tap` (an icon), `shine` (the hero, the chord arpeggiated over 75ms
then left to ring for 1.7s), `sub` (a landing, with an octave up so a phone speaker hears it),
`dot` (a comment dot, a link line, a handle).

Generated rather than bought because a library whoosh is cut to somebody else's clock, while a
generated file is exactly as long as the beat under it. If a pack is ever wanted anyway: Epidemic
Sound paid and cleared for YouTube, Pixabay free, `romainsimon/uisfx` for CC0 cues. Skip the sfxr
family, it makes arcade blips.

## The signature

Three more voices, and they are not effects. Every voice above plays because something on screen
happened and is named after the event. The mark plays because the channel is speaking. It is the one
sound whose job is to be recognised on its own, in a car, three seconds into a video nobody chose to
watch.

**The no-noise rule does not survive contact with this job, and it took building the wrong thing to
find out.** The first pass obeyed the rule: sines only, A major, arpeggio into an octave landing,
peak -9 dBFS. It measured beautifully — 22 discrete partials, spectral flatness 0.001 — and the
verdict on 2026-08-27 was **"They sound like UI sounds. We need a little bit more YouTube sounds."**
That was right, and the measurement is why:
 22 partials is a thin sound, and 0.001 flatness is the
number for a sound with no noise in it, which is the number for a settings toggle.

So the mark has its own file, `scripts/build-signature.py`, which imports nothing from
`build-sfx.py` and is imported by nothing there. **Two jobs, two rule sets, two files**, so neither
can quietly infect the other. The CTA kit keeps sine-only because it is right for a sound that plays
under a read; the mark drops it because it is wrong for a sound that plays instead of one.

Five things separate a channel mark from a UI sound, in the order they matter:

1. **Harmonic density.** A sine has one partial. Everything an ear calls produced has dozens: a
   detuned saw stack, a two-operator FM bell, a saturated 808. The stack is what does most of the
   work — the beating between seven voices at ±16 cents *is* the sound, and one saw is not it.
2. **Noise is the anticipation.** The sine version's 165ms gap was silence, measured at -27.5 dBFS.
   Silence before a hit only works in a room that is already quiet, and a YouTube viewer's is not. A
   riser fills it and a riser is filtered noise: bandpass, resonant, cutoff climbing 260Hz to 9.5kHz
   while its amplitude climbs with it, so it arrives rather than fades in. There is no sine
   substitute. This is the rule that had to go and the reason it had to.
3. **A transient that is not a note.** A kick is a 4ms broadband click at the skin plus a pitch
   falling into the floor. The sine kit could write the second and not the first, which is exactly
   why its landing had weight and no contact.
4. **Loudness as density, not as peak.** The sine version peaked at -9 dBFS and measured **-22.7
   LUFS** — correct for a CTA under a read, and half the volume of everything else on the platform.
   Saturation adds the harmonics that make a sound feel loud at the same meter reading; the limiter
   is what lets it actually be loud. The marks land at **-8.8 to -11 LUFS**.
5. **Rhythm.** Three notes on a clock is a melody. Three notes with a hat between them is music.

**Ceiling is -1.5 dBTP, measured on a 4x-upsampled copy.** YouTube re-encodes to AAC and an AAC
encoder overshoots a waveform that already touches full scale. A file trimmed to -1.5 at 48k still
reads -0.7 on a true-peak meter, and that clips after upload.

What is kept, so the mark and the kit still belong to one brand: **A major, the same climb resolving
to the octave, and the mark still asks before it answers.**

Four candidates, all built from the same figure:

| voice | length | instrument | for |
| --- | --- | --- | --- |
| `hype` | 60f | riser, FM pickups, supersaw drop, kick + 808 | the standard intro |
| `slam` | 36f | the run-up cut to 280ms, clap, hats | a Short, a hard cut |
| `braam` | 69f | distorted low cluster first, FM bells climbing out | an end card, a trailer beat |
| `chop` | 54f | three "ah" stabs, the last landing with the kick | vocal-led, the loudest of the four |

`chop`'s vowel is a saw through three bandpass resonances at 730/1090/2440Hz, not a sample and not
additive weighting. The first attempt weighted harmonics by their distance to a formant, which is
the right maths and the wrong instrument: it produces a *static* vowel. Fixed formants with the
pitch moving under them is what the ear reads as a person rather than an organ.

## The clean kit

**The produced four are not the default.** The verdict on them, 27 Aug 2026: *"They are a bit
too different from usual. You need to go for clean modern YouTube audio."* They are what a hard cut
or an end card wants. They are not what the top of a video wants, and the reason is measurable.

Three Kallaway openers were pulled at full bandwidth and read in 10ms frames (`yt-dlp -f bestaudio`,
first 20s, 48k stereo). **There is no musical logo anywhere in them**, and the design that is there
behaves in three ways the produced four do not:

- **Transitions are air and nothing else.** The frames at 1.10s, 1.30s, 2.90s, 3.30s and 4.60s carry
  **84-94% of their energy above 4kHz** and 0-2% below 160Hz.
- **Weight arrives on its own, after the air.** The low hits at 2.60-2.70s are 52-59% in 60-160Hz,
  17% sub, centroid **920Hz**, and they are separate events from the transitions.
- **Nothing is dense.** Peaks run -12 to -20 dBFS with the gaps at -30, and the opener is mono to
  about 4s (side/mid 0.00-0.08).

`scripts/build-clean-kit.py` is that third rule set. It execs the engine out of
`build-signature.py` and none of its candidates, and writes `out/clean-kit/` plus a `kit.html`
audition page with real waveforms.

### Five of its voices were then cut, and that is the lesson

Two Uppbeat files went in beside the kit on 27 Aug 2026 and out went `mark`, `open`, `cut`,
`whoosh` and `whoosh-long`: *"the sound designs of the cyberwhoosh and the futuristic UI are
better."*

**Be precise about what lost.** The whoosh had been rebuilt twice by then, and the second rebuild was
right on every measurement: a doppler tracing 1800 -> 3433 -> 2583Hz, a wind body at more than twice
the level of its resonant band, an envelope peaking at the pass rather than the middle, and
`add_moving()` panning it across the head (-2.7 to +1.5 dB). It still sounded synthesised, **because
a whoosh is a recording of an object in a room, and the room is the part no oscillator writes.**

So the rule the file carries now: **write what an oscillator can be, source what a microphone
heard.** What survived is exactly the sounds whose object is simple enough to model - a struck bell,
a plastic switch, a mouse - and the transitions are bought.

| voice | length | source | measured |
| --- | --- | --- | --- |
| `whoosh` | 43f | Uppbeat, Brukowskij, **ding trimmed** | peak at 0.31s, no transient after it, -4 dBTP |
| `ui` | 7f | Uppbeat, Davies Aguirre, as downloaded | -5 dBTP |
| `chime` | 48f | written: `fm_bell` ratio 3.5, A5 then E6 | 4777Hz, nothing below 400Hz |
| `click` | 3f | written: a leaf in a hollow shell | dry, no reverb |
| `type-2s`, `type-4s` | 60f, 120f | written: `keypress()` scattered by `type_run()` | 2235Hz, 45% presence, 17% air |

**The ding came off at 1.46s.** It is a separate event starting at 1.50s - a spectral-flux spike of
51.8 against a floor of 0.3 - on a whoosh tail already down at -75 dBFS, so the cut costs nothing.
`write_sourced()` trims, fades and sets the ceiling and **does not saturate**, unlike `write_at()`:
a file somebody already mastered does not need a second tanh stage.

**The build is the publish step.** `build-clean-kit.py` ends by copying the six files into
the design shelf's sound folder and writing a waveform SVG per voice beside it,
which puts them on the **Sound** room of the design library at `/design/sound` (and `/assets/sound`
for the shared one). The app lists that folder straight off disk in dev, so there is no upload and no
manifest to edit; the tile plays instead of opening a lightbox, because a lightbox has nothing to
show for a wave file.

Provenance and licence live in the licence ledger. Both files are Uppbeat free-plan, which
covers YouTube and social **only with the Uppbeat credit in the description**; premium (~$7/mo)
removes it and Business is what would cover client work.

### What the written voices kept

**A set needs one of each instrument, not one of each length.** The first `chime` was two mallets in
A major with a long dark tail, which is what `mark` was, and they were heard as one sound twice:
*"The mark and the chime are too similar."* The chime is now the metal one - `fm_bell` at ratio 3.5
rather than `mallet` at 2.0, struck twice 70ms apart, in a bright 1.5s room.

**The levels are baked in rather than set in the edit**: transition -4 dBTP, chime -3, mouse -5, the
runs -7. Drop the kit in at unity.

**Keystrokes are written, not downloaded.** `kamillobinski/thock` (MIT, 900 stars) and
`hainguyents13/mechvibes` (MIT, 2.3k) are the two best-kept, and **neither ships its audio in the
repository**: both pull packs recorded and traded by the keyboard community, so the MIT licence on
the code covers none of the sound, and a good share of it is lifted from switch-test videos.

**And a key is measurable, so it does not have to be guessed at.** Two models were wrong before the
third was right. A click at 3kHz over a 195Hz sine read as a laptop. Four case modes at
104/178/306/623Hz measured a 373Hz centroid, which is a cardboard box. Then 195 isolated strokes were
measured off a six-board sound test (53s, 48k mono, peaks with 60ms of silence in front of them) and
said plainly what a keyboard is: **a presence-band event, not a bass one.** Median centroid 2640Hz;
median split sub 3%, bass 3%, low-mid 1%, mid 14%, **presence 62%**, air 15%; median fall to -20dB
**3-4ms**. All six boards agreed, and the thockiest (centroid 1995Hz) differed from the clackiest
(4762Hz) **by how much air it had, not how much bass**.

**The fit is on the median board, and it went the long way round.** Asked for the clack - *"I need
the clack sound for the keyboard. The more mechanical clack keyboard"* - `keypress()` was refitted to
the 4762Hz board and measured 4611Hz, 40% presence, 42% air: correct against its reference, and
wrong in the edit. *"Regarding the typing I actually preferred the previous one."* So it is back on
the median of all 195 strokes: a 1.3kHz burst for the body, 2.2kHz over it for the edge, 600Hz for
the plate, a nearly-inaudible 116Hz sine, lowpassed at 5.5kHz. **2235Hz, 45% presence, 17% air.**

The clacky fit is one line each way and is written into the docstring, so it does not have to be
re-derived: the two bursts to 2.2k and 4.2kHz, the plate to 900Hz at 0.35, the air layer to 7.2kHz
at 0.52, the low sine to 0.03, the lowpass to 13kHz.

`type_run()` scatters strokes on a lognormal around 135ms, because straight spacing sounds like a
printer, and the single-key files are gone: what an edit places is a run.

## When a sound has to be recorded rather than written

Two routes, and neither needs an account.

**A local model, and it is Stable Audio 3.** Released May 2026, three of the four variants ship as
open weights: `small-sfx` (433M, sound effects only, CPU-capable) and `medium` (1.4B) are the two
that matter here. The repo's own MLX path is Apple-Silicon-native with no PyTorch at runtime, and
**`stabilityai/stable-audio-3-optimized` carries the MLX bundles ungated**, so nothing needs a token:

```bash
git clone --depth 1 https://github.com/Stability-AI/stable-audio-3
cd stable-audio-3/optimized/mlx && ./install.sh -y
./sa3 --prompt "a fast clean whoosh transition, airy swish passing by" \
      --negative-prompt "hiss, white noise, music, speech" --cfg 3.5 \
      --dit medium --decoder same-l --seconds 3 --out whoosh.wav
```

`medium` runs about **1.1x realtime on this Mac at 4GB peak RAM**, so a 5s take costs 4.5s. It also
does audio-to-audio restyling and inpainting of a region, which is the interesting part: an existing
sound can be pushed rather than replaced. Community License, free commercially below $1M revenue,
outputs are ours. `stable-audio-open-1.0` is the previous generation and is superseded; the only
reason to keep it is that its ungated mirror needs no repo clone.

**What it is actually good for, measured.** Against the same band analysis used on everything else:
`medium` produced a usable chime (centroid 1982Hz, 40% presence, 14% air) and a usable whoosh
(1775Hz), and both models failed on the short dry ones - the generated mouse click came out 64-78%
air, which is a hiss, and the generated keyboard measured a 5682Hz centroid against a real board's
2640Hz. Every take also arrives peak-normalised to 0.0 dBFS and needs trimming. **So: generate
texture and atmosphere, write anything that has to land on a frame.**

**A library, when one is bought.** The music shelf already picked Artlist Pro for beds, and
SFX come in the same subscription; Epidemic Sound is the safer answer for a channel that is only a
channel. Neither is bought yet, and neither is needed for the kit above.

The sine-only versions are kept at `out/sound-signature/` as the counter-example, and
in the kit as `signature`, `stamp` and `bloom`. **Do not reach for them for an intro.** They are
useful where a mark has to play under a voice without ducking it, which is the one thing the
produced versions cannot do.

**Which of the three files to open.** The top of a video, a transition, a screen recording: the
clean kit. A hard cut in a Short, an end card, anything that has to compete with a music bed: the
produced four. A cue that plays under a read and must not duck it: the sine kit.

Levels land at -9 to -19 dBFS and nothing needs a compressor in the edit. Check every tail fits
before the clip ends: `shine` runs 54 frames, and a truncated reverb is more obviously wrong than
no reverb at all.

Verify by measuring, not by listening once:

```bash
ffmpeg -v error -i out.mov -f s16le -ac 2 -ar 48000 -y /tmp/a.raw
# Peak per frame: 1600 samples is one frame at 30fps. Onsets must land on the frames the component
# names, and the last frame must read silent, which is how you know no tail was truncated.
```
