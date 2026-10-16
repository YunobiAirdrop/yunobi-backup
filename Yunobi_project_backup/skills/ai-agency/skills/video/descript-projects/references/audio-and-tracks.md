# The audio of a project: which track transcribes, and the tracks inside a sequence

Split out of `SKILL.md` so the skill stays readable. Everything here is proven on real projects;
the dates are in `learned-patterns.md`.

## Only one track gets transcribed, and it is the microphone

Descript transcribes what you import. On a multi-angle shoot the same words exist on three tracks
(the lav, the camera's built-in mic, the screen recording's room audio), and importing all three
produces three transcripts of one performance. The script should be driven by the best capture,
which is the external mic, and the other two are duplicates that cost transcription minutes and put
a worse transcript in the browser next to the good one.

**`language` is not a switch.** The import API has no "do not transcribe" flag; `language` only
tells it which language to expect, and omitting it means auto-detect rather than skip. The only
thing actually under your control is what audio you upload.

So the rule is about the file, not the API call:

- **An external mic track exists** (a lav, a recorder, a separate speaker-named audio item):
  upload the camera and screen angles with their audio stripped, `ffmpeg -i in -c:v copy -an out`.
  Stream copy, so it costs seconds and no quality. The mic stays the only thing that can drive a
  script. Pass no `language` on the silent angles.
- **No external mic** (phone or camera audio is the only capture): the camera track is the audio.
  Keep it, import it normally, and let it transcribe. Stripping it here would leave the project
  with no script at all.

Check before stripping rather than assuming: `get_project` and look for an audio item whose
duration matches the take. Sync is the other thing to check, because waveform alignment needs the
camera audio; if the angles are not aligned yet, align first (`dji-sync`) and strip after. Keep the
un-stripped original on disk either way.

## Inside a sequence: CAM, SCREEN, MIC, and one live soundtrack

A sequence's tracks are neither media nor compositions, so `tree` and `comps` never showed them and
for a long time this skill implied they were unreachable. They are `sequenceScenes`, one entry per
track, reached from the sequence mediaRef through `audio.trackSceneIds`. Every verb is a command
(2026-08-25):

```bash
pnpm descript tracks <project>                        # names, which one is live, its Studio Sound
pnpm descript track rename <project> <track> "CAM"
pnpm descript track mute <project> <track> [--off]    # --off makes it the live one
pnpm descript studio <project> <track|media> --on --intensity 0.5
```

**The names are `CAM`, `SCREEN`, and `MIC` when the mic was recorded apart from the camera.** In
that order, because that is the order the timeline draws them and the order an editor scans.

**Exactly one track stays live and every other one is muted.** The mic if it exists, otherwise the
camera. Two unmuted captures of one room is comb filtering: it passes every check that is not
listening, and it is not visible in a waveform. `tracks` prints a warning when it finds two live.

What the app draws as one track header is three fields on three different objects, which is why
guessing at any one of them fails:

| The app shows | The document holds |
| --- | --- |
| The track label | `sequenceScenes[].name` |
| The speaker icon | `sequenceScenes[].isMuted` |
| The Studio Sound toggle | `mediaLibrary.mediaRefs[].audio.speechEnhanceEnabled` |
| Its percentage | `mediaLibrary.mediaRefs[].audio.studioSoundIntensity`, 0 to 1 |

**A muted track keeps its gain at 1.** Mute is `isMuted` alone, so reading gain to find the silent
track finds nothing and reports every track live.

**Studio Sound belongs to the media, not to the track.** Turning it on for one track turns it on
in every track and every composition that uses that recording. `studio` takes a track name and
resolves it to the single media the track was cut from, so the target reads like a track and
behaves like a file. Media carrying no audio is refused rather than silently given the field.

**A track name and its media name are separate fields and drift apart on purpose.** Renaming the
track to `CAM` leaves the media called `Speaker Name-5`, and the media browser still reads as a pile
of web-recorder defaults. Rename both, and keep them the same word: the media browser and the
timeline are read by the same person a week later.
