# Naming: clips, folders, sessions and batches, and getting footage in

Read this before an import, because the manifest key is the name and the folder both, and side-loading phone footage into Descript starts here too.

## `N [MM-SS] Description.ext`

- **One digit up to nine, two from ten.** A leading zero pads a number with nowhere to grow, so a
  lesson with six clips uses `1`. A long video does go past nine, and one-digit names then sort
  `1, 10, 11, 12, 2`. Pick the width once for the whole video and keep it.
- **A letter suffix means alternatives for one beat.** `2a`, `2b`, `2c` reads as three options for
  beat 2 and the editor picks one. A beat with a single option carries no letter.
- **`-` not `:`.** macOS renders `:` in a filename as `/` in Finder. `[04-19]` means 4:19.
- **Zero-pad the timecode** so `[00-09]` sorts above `[01-34]`.
- **When there is no take yet, drop the bracket rather than inventing one.** B-roll often arrives
  before the camera does, the composition reports 0, and a guessed `[01-20]` reads as measured.
- **Timecode against the cut whenever a composition exists.** `layout cards` or an SRT export of
  the composition gives the real clock.
- **A raw take is `RAW <CAM|MIC|SCREEN|IPAD> <Take>`, with no number and no timecode.** It isn't a
  beat. The author, 24 Sep 2026, dropping the old `00` prefix: "remove this concept."
- **A salvage take carries its salvage points instead**: `ALT 4K [salvage 1-05, 1-13, 3-41].MOV`.

## The three clip folders, and why they are apart

- **`Music`**: the bed, and only the bed. One file, no beat number and no timecode, because it is
  not a beat: it runs under the whole cut.
- **`Motion`**: everything built here, in both registers - flat motion (opaque, full frame or
  960x1080 beside him, `.mp4`) and alpha motion (keyed over him, QuickTime Animation `qtrle`
  `.mov`; an HEVC-alpha one keys as a black rectangle here, it is the public shelf's codec). The extension
  separates them, so the folder needs no further split. Ours outright.
- **`B-roll`**: real footage - a film beat, a meme, archive, a stock plate. Usually somebody
  else's picture, always muted.

They are apart for licensing, not tidiness. A borrowed shot **cannot ship in a paid lesson, a
client deliverable or an ad**, and a drawn one ships anywhere; mixed into one folder an unshippable
frame sits one drag away from a paid build and nothing on screen says which is which.
`broll` keeps the rights ledger and gates a build on it. `Music` sorts above the other
two, which is also the order the passes run in.

## The two folder shapes

One folder per video, holding that video's raw take and its three clip folders together:

```
second-brain/
  RAW CAM Second Brain.MOV
  Music/  Bed · Understated Drive.mp3
  Motion/ 1 [00-28] Notes App.mp4
  B-roll/ 1 [02-11] Printer Rage.mp4
```

A second video gets its own folder beside it, same shape - never `Raw/` plus `B-roll <Video>/`,
which opens two folders to cut one video. A single-video project keeps the three at its root:

```
clickup-terminology/
  RAW CAM ClickUp Terminology.MOV
  1 [00-00] Hierarchy Overview Diagram.jpg
  2a [00-09] Workspace.png
  2b [00-09] Workspace Sidebar.png
```

## A recording session, and a shorts batch

One folder per session, slug-cased. Raw files start `RAW`, so they sort together and apart from
the numbered clips:

```
you-only-need-five-spaces/
  RAW CAM  You Only Need Five Spaces.MOV     4K camera
  RAW IPAD You Only Need Five Spaces.MP4     iPad screen recording
  RAW MIC  You Only Need Five Spaces.wav     the web-recorder take
```

Sequences get `SEQ <code> · <Title>`, so the Sequences folder reads as the batch.

**A video code carries no `E`.** The codes are `C51`, `A19`, `P33`, `S02`, and the French channel's
`FC38`, `FA08`. The English channel dropped its `E` prefix when everything was renamed, so `EC51`
names nothing now: a folder or a ledger still carrying it (`ec51-agentic-crm`, its `RUN.json`) is
old, and the code you say and write is the one without it. The author, 22 Sep 2026: "we renamed
everything by removing the letter E everywhere."

A shorts batch project is `BATCH <week> - MM-YY`, in `60-Shorts`. The suffix is the month and year
of the **recording**, never of the publishing window: a batch publishes over three or four weeks
and often crosses a month, so a publishing month puts two batches on one name. The number is
inherited from the Apple Notes queue (`Projects › Shorts › Batch N`), which rolls when a batch is
folded into the one ahead of it, so it is not re-derived from the shot date and not renumbered to
close a gap. Only the suffix is computed.

Name it at creation - `pnpm descript project new "BATCH 5 - 09-26" --folder 60-Shorts` - because a
rename afterwards leaves every doc that quoted the old name stale. Re-importing to fix a name was
never the answer either: it duplicates the media and the original stays wired into any composition
using it.

## Getting footage off an iPhone and into a project

Side-loading phone footage into Descript, end to end.

### Read the phone

`afcclient` (libimobiledevice) lists and pulls without Photos or Image Capture.
`afcclient ls /DCIM/<NNNAPPLE>`, then `afcclient info <path>` for `st_size` / `st_mtime` /
`st_birthtime` in nanoseconds. **`birthtime -> mtime` is the recording span**, which is how you
match a file to "the 46 minute one" without pulling it first. Running bare `afcclient` opens an
interactive shell that hangs a tool call, so always pass a subcommand.

**Never trust mtime alone to pick "the latest".** A clip deleted in Photos still sits in `/DCIM`
until the phone purges it, so it reads as recent. Confirm the pick against duration before
transferring gigabytes.

Frames that refuse to come over are iCloud optimisation, not a transfer fault: Settings ▸ Photos ▸
Download and Keep Originals, then re-run. A pull script should be read-only and resumable.

### Upload

**That `{content_type, file_size}` object is the MCP's shape and never the CLI manifest's.** A
`descript import` manifest maps display path to a bare local path string, because the CLI hands each
value straight to `importEntry(path, key)`: an object there dies on `path.split is not a function`
with nothing said about which shape it wanted.

```json
{ "clickup-terminology/RAW CAM ClickUp Terminology.MOV": "/path/to/take.MOV" }
```

`import_media` with `content_type` and `file_size` returns a presigned `upload_url` per file,
valid 3 hours. Then `curl -T <file>` to it. **Use `-T`, never `--data-binary`** - `--data-binary`
buffers the whole file in RAM and dies with "out of memory" on anything multi-GB.

The import job is **atomic across all files in one call**. It sits at `waiting_for_uploads` and
every file shows in the UI as an unprocessed placeholder with an audio icon until the last byte
of the last file lands. That is not a failure, and re-uploading the finished file does nothing
but create a `-1` duplicate name.

A name already present in the project makes `import_media` refuse. Prefix the key with a folder
path (`"iPhone 19 Aug/IMG_7646.MOV"`) to route around a stale entry.
