# DJI Sync

Starts when the recording stops, owns the card until it is empty. Does not edit, trim,
colour-grade or re-encode video: swaps one audio track and gets out.

## Two paths off the same card

A take is either **half of a reel** or **a thought recorded alone**. They share the card
detection and the archive-and-wipe contract and nothing else.

| | Reel take | Solo take |
| --- | --- | --- |
| Script | `dji_sync.py` | `dji_note.py` |
| Needs | an iPhone clip to pair with | nothing but the take |
| Output | `NAME-dji.MOV`, video bit-identical | speech-only `.opus` + a vault voicenote |
| Ranking rule | the video is the timeline | the transcript is the deliverable |

**Ask which one it is. Do not infer it silently.** The author says it in plain language ("that's a
voice memo", "pair this with the reel") and that wins. A wrong guess burns 20 minutes of
thinking or destroys a reel's audio half. Without it: no clip in `~/Downloads` near the take's
timestamp means solo; a long take VAD reports as mostly silence means solo, a walk with pauses;
a take within seconds of a clip's length means reel. Run `dji_note.py --dry-run` when unsure: it
decides and reports without writing.

## The rule that ranks above the rest

**The video is the timeline.** The clip's duration, frame timing and metadata are the truth.
The DJI take is a raw ingredient: it gets trimmed, shifted and padded to fit the video, never
the other way round. Output duration always equals input duration. If that is not true, the
run failed.

Usually the mic starts first and stops last, so both ends get trimmed off. Not guaranteed;
see "When the take runs short".

## Never match on timestamps

The transmitter's clock and the phone's clock do not agree, and the drift is not constant.
On the first real pair the DJI filename stamped `190732` while the clip stamped `19:07:49`,
implying 17 s, and the true measured offset was 16.004 s. A second take on the same card was
stamped 90 s away from where its audio actually sat.

Filename stamps are worth using to *order* takes and nothing else. The waveform decides.

## How the match is decided

The pipeline aligns once globally with GCC-PHAT, then re-measures the offset independently in
every 2-second window: a genuine match holds the same offset everywhere, a false one wanders.
Alignment is sub-sample and drift is corrected when it matters. The measured evidence behind
the method (why envelope correlation and peak height fail, the drift numbers) is in
[How the match is decided](audio-and-tracks.md#the-evidence-behind-dji-sync-and-why-not-the-obvious-ways).

Accept requires **all** of: ≥ 80 % of windows within 1.0 ms of the median, each with
peak-to-sidelobe ≥ 5; a ≥ 15 percentage-point margin over the runner-up take; at least 2 usable
windows. Miss any and it refuses, writing nothing rather than risk a wrong take. Do not loosen
these to force a match; pass the take explicitly instead:
`dji_sync.py clip.MOV --take /path/to/TX00_MIC005.wav`.

## When the take runs short

The first real pair covered **20.29 s of a 35.84 s clip**: the transmitter stopped before the
phone did. Expect it again. Uncovered stretches fill from the phone's own audio, RMS-matched to
the lav so the level does not jump, with a 40 ms crossfade at the seam. The run prints a loud
`WARNING` with the head and tail gap. `--silence-gaps` leaves them silent instead: obvious in an
edit, at the cost of usable audio.

**Always read the coverage line.** A file at 57 % coverage is a usable rescue, not a clean take.

## What "no loss" means here

- **Video is never re-encoded.** `-c:v copy`, and the burn is rejected unless the output's video
  stream MD5 equals the source's. Bit-identical or it does not ship.
- **Audio is lossless.** ALAC `s32p` in the `.MOV`. Measured round-trip residual −143.3 dBFS,
  max 1.19e-7, which is float32's own epsilon rather than any codec loss.
- The only intentional changes to the lav samples are the sub-sample shift and the seam crossfade.

`--codec pcm` for older NLEs, `--codec aac` for a small upload copy. Both a step down for no
gain in an edit.

## Metadata and what survives

`-map_metadata 0 -movflags use_metadata_tags`, then `exiftool` restores the Apple keys ffmpeg
drops, then the file's mtime and creation date are reset to the original's. Verified preserved:
rotation (90°, both as the tag and the display matrix), `CreationDate` with its timezone, GPS,
`Make`/`Model`/`Software`, and the four `mebx` Core Media Metadata tracks with their handler
names. macOS parses the result natively.

**Known cosmetic wart:** ffprobe reports the data tracks' `codec_tag_string` as `stts`, not
`mebx`, after the remux. Handlers and payloads still survive; drop those tracks if a tool
ever chokes on them.

## The solo path: silence goes before whisper sees it

Silence stripping is a correctness requirement, not a size optimisation: fed a mostly-silent
take, whisper loops on one sentence and the real content never appears. **Silero VAD decides**
what is speech; a fixed dB gate needs per-recording tuning and works only as a cross-check.
Evidence for both claims: [How the match is decided](audio-and-tracks.md#the-evidence-behind-dji-sync-and-why-not-the-obvious-ways).

Everything else is defaults with a reason: 0.25 s of padding either side so words are not
clipped, joins de-clicked with a 10 ms fade, and silences shorter than 400 ms left in.

### The loop guard, which is the real safety net

The transcript is checked before anything is written or deleted. If one normalised sentence
accounts for 6 or more lines and 40% of the transcript, it is whisper looping, not the speaker
repeating himself. The run refuses: no note, no wipe, card untouched, and it says to try a
lower `--vad-threshold`. Verified against both transcripts above: the trap trips at 38 of 42
lines, the real one passes at 1 of 11.

### Where the note lands

`📥 Raw/Voicenotes/YYYY-MM-DD <Title>.md` in the vault, with the take id, both durations and
the audio path in frontmatter.

**Raw is immutable and the wiki is a separate act.** The script files the transcript and stops.
Turning it into `🧠 Wiki/Coaching/2026 North Star.md`, the project pages, `index.md` and
`log.md` is the vault's ingest, which its own `CLAUDE.md` says runs one source at a time with
the speaker in the loop. Summarise the take back and ask what to emphasise before writing a
single wiki page. Never quietly rewrite the North Star from a walk.

Pass `--title` once the transcript has been read. Without it the note is filed under a
provisional `DJI note HHMM` and has to be renamed during the ingest.

### What the wipe destroys here

The reel path archives every take in full. **The solo path does not:** it archives the
speech-only Opus and deletes the source wav, irreversibly, the 95% that was silence and the
untouched 5% that was not. The transcript must pass the loop guard first, so the ordering still
holds. When the raw take matters, `--keep-original` archives the full wav through the same
checksummed path the reel side uses.

## Running it

```bash
D=<skill-dir>/scripts
python3 "$D/dji_sync.py"                     # newest clip in ~/Downloads, detect card, burn, wipe
python3 "$D/dji_sync.py" --dry-run           # decide and report, touch nothing
python3 "$D/dji_sync.py" clip1.MOV clip2.MOV # several clips, each take used at most once
python3 "$D/dji_note.py" --dry-run --no-note # cut, transcribe, print, write nothing
python3 "$D/dji_note.py" --title "..."       # file the note, then wipe the card
```

`--no-clean` keeps the card as it is on either path.

Reel flags: `--take` to force the pairing, `--keep-scratch` to retain the phone audio as a
second track, `--silence-gaps`, `--codec`, `--archive DIR`, `--card PATH`, `--output PATH`.
Note flags: `--title`, `--vad-threshold` (0.5), `--min-silence-ms` (400), `--pad` (0.25),
`--bitrate` (24k), `--lang` (auto, so French and English both work), `--keep-original`,
`--no-note`, `--vault DIR`.

Reel output lands beside the source as `NAME-dji.MOV`. **The original is never modified**, so a
bad run costs nothing but disk. Note output lands in the day's archive folder and the vault.

Dependencies, the borrowed whisper models and their paths, and measured run time are in
[What it runs on](audio-and-tracks.md#what-it-runs-on).

## The card wipe, and the trap in it

Order is fixed: **burn, verify, archive, checksum, delete.** Every take on the card is copied to
`~/Movies/dji-archive/YYYY-MM-DD/` and each copy's SHA-256 is compared against the original
*before* anything is removed. A take whose checksum mismatches stays on the card. If any clip in
the run fails to verify, the card is left completely alone.

**Dragging takes to the Trash on a removable volume never frees the space.** They move to a
hidden `.Trashes` folder on the card and sit there. The first run found **31.5 MB** of takes
"deleted" that way. The wipe clears `.Trashes` explicitly, which is most of the point of
automating this.
