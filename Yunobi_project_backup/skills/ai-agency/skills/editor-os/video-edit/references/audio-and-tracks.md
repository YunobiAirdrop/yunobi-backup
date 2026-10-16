# The audio: which track transcribes, and the tracks inside a sequence

Read this before importing a multi-angle shoot, and before touching Studio Sound.

## Only one track gets transcribed, and it is the microphone

Descript transcribes what you import. On a multi-angle shoot the same words exist on three tracks -
the lav, the camera's built-in mic, the screen recording's room audio - and importing all three
produces three transcripts of one performance, costing transcription minutes and putting a worse
transcript in the browser beside the good one.

**`language` is not a switch.** The import API has no "do not transcribe" flag; `language` only
says which language to expect, and omitting it means auto-detect rather than skip. The only thing
under your control is what audio you upload.

- **An external mic track exists**: upload the camera and screen angles with their audio stripped,
  `ffmpeg -i in -c:v copy -an out`. Stream copy, so it costs seconds and no quality. Pass no
  `language` on the silent angles.
- **No external mic**: the camera track is the audio. Keep it and let it transcribe, or the project
  has no script at all.

Check before stripping: `tree` for an audio item whose duration matches the take. Sync is the other
check, because waveform alignment needs the camera audio - align first ([dji-sync.md](dji-sync.md)),
strip after,
and keep the un-stripped original on disk either way.

## CAM, SCREEN, MIC, and one live soundtrack

A sequence's tracks are neither media nor compositions, which is why `tree` and `comps` never show
them. They are `sequenceScenes`, one entry per track, reached from the sequence mediaRef through
`audio.trackSceneIds`.

```bash
pnpm descript tracks <project>                        # names, live, in script, clip start, Studio Sound
pnpm descript track rename <project> <track> "CAM"
pnpm descript track mute <project> <track> [--off]    # --off makes it the live one
pnpm descript track script <project> <track> --off    # take a track out of the script
pnpm descript studio <project> <track|media> --on --intensity 0.5
```

**The names are `CAM`, `CAM GS`, `MIC`, `SCREEN`**, in that order, because that is the order the
timeline draws them and the order an editor scans. `CAM GS` is the keyed twin of the camera, the
same take with the background removed, and it exists wherever the shoot was on green: eight of the
pack's cards draw it as the body over their text (`layouts-and-music.md`).

## Three gates, and `tracks` prints them

`tracks` ends on one line: `tracks clean`, or a fault per line. Pass 0 is not done until it reads
clean, and `run.py` takes that output as the evidence. The author, 8 Sep 2026, after doing both by hand
on EC51: *"The skill needs also to double-check that there is the green screen layer at the exact
same time in the sequence"* and *"only the active audio is in the script, the other one it should
remove from script."*

- **One live track.** Below.
- **Only the live track in the script.** `includeTranscript` on the scene is the app's "Include in
  script". A camera track left in it puts a second, worse transcript under every word, and every
  cut lands against the wrong one. `track script <track> --off` on every track that is not the mic.
- **The green twin on CAM's clock.** `at` is the second the track's media starts on the sequence,
  read off the silent lead-in tau before it. `CAM GS` has to match `CAM` within half a frame and
  play from the same media offset, or every Text card draws a body a frame off its own face. A
  missing twin is `track add <seq> "CAM GS" --media <the camera file>` with CAM's own offsets; the
  key is the card layer's `backgroundRemoval`, which `comp fill` stamps hidden.

**Exactly one track stays live and every other is muted** - the mic if it exists, otherwise the
camera. Two unmuted captures of one room is comb filtering: it passes every check that is not
listening and it is not visible in a waveform. `tracks` warns when it finds two live.

What the app draws as one track header is three fields on three objects:

| The app shows | The document holds |
| --- | --- |
| The track label | `sequenceScenes[].name` |
| The speaker icon | `sequenceScenes[].isMuted` |
| The Studio Sound toggle | `mediaRefs[].audio.speechEnhanceEnabled` |
| Its percentage | `mediaRefs[].audio.studioSoundIntensity`, 0 to 1 |

**A muted track keeps its gain at 1**, so reading gain to find the silent track finds nothing and
reports every track live.

**Studio Sound belongs to the media, not the track.** Turning it on for one track turns it on in
every track and every composition using that recording. `studio` takes a track name and resolves it
to the single media it was cut from, so the target reads like a track and behaves like a file.

**A track name and its media name are separate fields and drift apart.** Renaming the track to
`CAM` leaves the media on its web-recorder default and the browser still reads as a pile. Rename
both, and keep them the same word.

## The music bed

One sound per channel, not per episode: the brand's music style is the answer, and a track a
sibling project already uses wins a tie, because a different sound each time reads as a different
channel. Level, ducking and the loop are not per-video decisions either. `music set` writes **0.211 with
ducking on and `fillBehavior: loop`**, because a 121-second bed under a 22-minute cut goes silent at
2:01 otherwise (EC51, 8 Sep 2026, looped by hand in the app), which is where Descript put a real
one, and the scene's own gain stays at 1 so the slider an editor drags next still tells the truth.
The bed is Descript stock: `stock music search` finds it and `stock music pull` puts it in the
project's `Music/` folder. Pass 4 pulls three of them as options and `place` lays the one he keeps
(`descript-projects.md`).

A guard checking only `media &&` counts an empty `Placeholder` pin or a bare PNG as a bed. Never
clear one with `music rm`: it lifts the card's own pin.

## The evidence behind DJI sync, and why not the obvious ways

Three signals were measured against a confirmed true/false take pair. Two of them fail:

| Signal | True take | False take | Verdict |
| --- | --- | --- | --- |
| Envelope correlation | r ≈ 0.00 | r ≈ 0.00 | **Useless.** A chest lav and a room mic have unrelated envelopes on identical speech. |
| Correlation peak height (PSR) | median 15.1 | median 7.1 (max 23.1) | **Overlaps.** Cannot separate on its own. |
| **Offset agreement across windows** | **0.15 ms spread** | **5.9 ms spread** | **This is the discriminator.** |

So the pipeline aligns once globally with GCC-PHAT, then re-measures the offset independently
in every 2-second window. A genuine match holds the same offset everywhere because it is the
same physical event hitting two mics. A false one wanders.

### Precision

Alignment is sub-sample. GCC-PHAT with parabolic peak interpolation resolves well under one
sample at 48 kHz (20.8 µs), the agreeing windows are averaged to sharpen it further, and the
fractional part is applied as an exact FFT phase ramp rather than rounded away. Verified on
the burned file: every window read 0.000 ms with 0.0000 ms spread.

**Clock drift is the real enemy on long takes, not the initial offset.** Measured −13.9 ppm on
this transmitter: 0.5 ms across a 36 s reel, which is nothing, but ≈ 8 ms across ten minutes,
which is visible. The per-window offsets already exist, so a slope is fitted for free and the
take is resampled only when projected drift exceeds 10 ms. Below that a single offset is
applied, because resampling a clean signal for a sub-millisecond gain is a bad trade.

### Why silence is cut before whisper sees a solo take

Cutting silence looks like a file-size trick. It is not. It is the only reason the transcript
has any content at all. Measured on the first real take, 20m17s recorded on a walk, 233.7 MB:
the whole file gave 249 words and **none** of the real content, while the same take VAD-cut to
1m00s gave 130 words and all of it.

Given twenty minutes of near-silence, whisper locks into a repeat loop: 38 of the 42 lines it
returned were the same sentence, and the actual thinking on the take, an all-in-one assistant,
the ClickUp to Sheets user base in D1, a video about a skill cleaner, **did not appear once**.
The transcript looked plausible and was worthless. Feed it only the spoken parts and all of it
comes back. Size is the free side effect: 233.7 MB to 168 KB, **1393x**, at 24 kbps mono Opus.

### VAD decides, an amplitude gate cannot

A fixed dB threshold is not a usable discriminator. On that same take, `silenceremove` at
−50/−45/−40/−35 dB kept 488/230/113/50 s: a ten-fold swing across 15 dB, so the number would
need retuning for every recording depending on how loud he was and where he was standing.
Silero VAD reports 49.8 s independently, which agrees with the −35 dB reading, and it needs no
tuning. The gate is worth running only as a cross-check when a result looks wrong.

### What it runs on

Both paths need `ffmpeg`, `ffprobe` and numpy. The solo path also needs `whisper-cli` and
`whisper-vad-speech-segments` (`brew install whisper-cpp`), plus two models already on this
machine because VoiceInk downloaded them:

- `~/Library/Application Support/com.prakashjoshipax.VoiceInk/WhisperModels/ggml-large-v3-turbo-q5_0.bin`
- `/Applications/VoiceInk.app/Contents/Resources/ggml-silero-v5.1.2.bin`

Nothing is downloaded or sent anywhere: it is local and free. **This borrows VoiceInk's files**;
if VoiceInk is ever removed, copy both models somewhere stable and point `--model` and
`--vad-model` at them. A 20-minute take costs about 26 seconds end to end on the M4 Pro.
