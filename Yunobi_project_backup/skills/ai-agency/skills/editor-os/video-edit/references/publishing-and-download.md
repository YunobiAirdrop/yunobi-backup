# Publishing and downloading a composition

Read this before rendering a master, and whenever somebody asks for 4K.

```
descript publish <project> [composition] --resolution 4K --download "~/Downloads/cut.mp4"
descript jobs                        # what is running; a second answers "A publish job is already running"
descript job <id> --download <path>  # pull a render that already finished
descript pull <project> <name>       # the ORIGINAL take, not a render (below)
```

## The ORIGINALS come off `pull`, and never off a render

A render is the cut; `descript pull` returns the camera and screen takes as recorded, to feed
any local edit
 without re-uploading anything.

```
descript assets <project> --kind video               # what is there, with sizes
descript pull <project> IMG_0015 --seconds 60        # the first 60s, ~70 MB of a 2.5 GB take
descript pull <project> IMG_0015                     # the whole file, 8 ranged connections
```

`--seconds` hands the signed URL to ffmpeg and stream-copies to that duration, so nothing is
re-encoded and the rest of the file never crosses the wire. It writes to `~/Downloads` unless
`--out` says otherwise, and the match is any part of the asset name.

**The name in `assets` is the ORIGINAL filename, not the name in the project's Files panel.** The
EP33 camera takes are `IMG_0015.mov` and `IMG_0016.mov` where the project calls them
`RAW CAM 1` and `RAW CAM 2`. Duration is what tells them apart: match the seconds in
`get_project` against `assets --probe`.

**A slow first connection reads like a hang.** These are iPhone QuickTime files with `mdat` first,
so ffmpeg range-seeks to the index at the end. One 180-second pull sat at 40 MB after seven
minutes; the same command a minute later did 60 seconds in 33. Re-run it before believing the
route is broken - `error: fetch failed` off `media_assets` is the same flakiness.

## 4K comes off a local export first, and the cloud publish second

**The lock is gone.** Until 10 September 2026 the 4K and 1440p rows drew a lock and a click
surfaced `Upgrade for higher than 1080p video resolution`. On `descript_creator_v3` both rows read
`aria-disabled="false"` with no lock and no upgrade text, so the app encodes 4K itself.

```
pnpm descript export local <project> [composition] --resolution 4K --quality high
pnpm descript export local <project> --resolution 2K --scope scene --dry    # set it up, click nothing
pnpm descript export local <project> --via orca --page <id>                 # drive HIS browser instead
pnpm descript export local <project> --keep                                 # leave the window up to look at it
```

**The local render is the better master on the two things that are decided rather than encoded:**
its colour tags read plain bt709 and its audio comes back at 48 kHz, where the cloud tags one
render `smpte170m` and the next `iec61966-2-1` over full-range `yuvj420p`, and resamples to
44.1 kHz every time. The cloud bitrate is unpredictable rather than low: it chose 7.8 Mbps on EC51
and 29.7 Mbps on C18.

**The cloud publish still has three jobs.** It renders without tying up the browser for the length
of the cut, it mints the share URL, and it is the fallback when a local export refuses a clip.

**A local export needs a click the page trusts, and the tab has to survive the encode.** A
synthetic `element.click()` flips the button to `Loading` and writes no file; the click has to go
through the browser's own input path. And the encode lives in that tab: close it, or let the
browser restart, and the export dies with no file, no toast and nothing in the log.

**So it runs in a Chrome of its own, and that is the default.** `--via chrome` launches
`/Applications/Google Chrome.app` on the profile `~/.cache/descript-cli/chrome`, with the DevTools
port 3348, signs it in by writing the `stytch_session` cookie the CLI already holds, opens one tab,
and drives it over CDP, touching nothing he is looking at. `--via orca` drives the browser he is
signed into: it works, but `orca click` acts on the FRONT tab, so it holds his browser for the whole
encode. On that route the confirm button and the editor's own button are both called `Export`, so
the command labels the confirm one first.

**The Chrome driver always closes its own tab, and a leaked one breaks the next run.** Three tabs
left open on one project made Descript refuse a fourth session with `Project is taking longer than
expected to initialize`, for eleven minutes, on a three-second scene. `openChrome` now clears any
tab already on that project's URL before opening its own, and `close` takes its tab with it even
when it leaves the browser running. `--keep` is the one exception, for looking at what it saw.

**It is not headless, and must not be.** The render is a WebCodecs encode inside the tab, and
headless Chrome on macOS falls back to a software encoder.

**The cookie is the whole sign-in.** A fresh profile with `stytch_session` written to
`web.descript.com` loads the editor as him, project and all. When it has expired the page is a
sign-in screen instead, and the command prints what the page reads rather than guessing; the repair
is `pnpm descript auth capture`. The first run on a fresh profile downloads the app bundle and can
take two minutes to show the editor, where a warm one takes four seconds.

**The file sits at 0 bytes for the whole encode, then fills in one step.** The browser opens it in
`~/Downloads` the moment the click lands and writes nothing into it until the encode is done: a
1:05 cut at 4K held 0 bytes for five minutes, then went to 221 MB. So an empty file is progress,
`export local` prints `encoding into <name>` while it is empty, and a `--timeout` shorter than the
encode reports a failure over a run that was fine. Never answer that by clicking Export again: a
second export in the same tab never gets its own file and both runs then watch the same name. The
command now refuses the second click.

**Never run a local export and a cloud `publish --download` of one composition at the same time.**
Both write that composition's name into `~/Downloads`, and on 11 September the local watcher claimed
the cloud download as its own render. The browser's file is always empty when it first appears, so
the watcher now ignores anything that already carries bytes; run them in sequence anyway, because
only one of the two can own the name.

**It can refuse a clip, and it says so in a toast.** FC38's full composition stopped after about
two minutes with `Couldn't process "00 RAW CAM Tarifs ClickUp.mov" during export. Try removing or
replacing that clip.` - a 43-minute HEVC 4K camera take, whose two-second scene exported fine at 4K
from the same project. The command reads that toast and fails on it; publish that cut in the cloud.

**Every row goes to the top of its list, and the audio one needs the Advanced panel opened.** His
ruling, 11 September 2026: maximum bitrate, maximum quality. The video rows already default to the
top, 4K and High, but the app ships audio at 128 kbps and nothing in the main dialog says so.
`export local` now opens Advanced, opens the audio settings, and takes stereo, 48 kHz and the
highest bitrate the menu offers, which is 256 kbps. It reads that last row rather than naming the
number, so a new one is taken on its own. The command prints what it set.

**The quality rows are bitrates, and they scale with the resolution.** At 4K they read High
30 Mbps, Recommended 20, Low 10; at 1080p, 21, 14 and 7. `--quality` defaults to `high`, because
YouTube re-encodes the master anyway and the bits cost nothing but disk.

**4K is often real detail, but never assume it.** Where the takes are 3840x2160 and the composition
is cut at 3840x2160, a 1080p export is what throws pixels away. It is not the whole shelf: EP33's
camera takes are **1920x1080** where its screen recordings are 3840x2160, measured 4 September 2026,
so a 4K render of that one upscales the face and keeps the screen. Check before choosing:
`assets --probe` for the sources, `videoMetadata` in `descript doc` for the composition. When the
timeline really is 1080p, `pnpm youtube:master` does the Lanczos upscale locally in three minutes.

**YouTube needs 2160p either way.** It picks its encoding ladder off the resolution it is handed
and never builds a rung above it: uploaded at 1080p it serves one rung, 1920x1080 h264 at
**1.35 Mbps**, no VP9; at 2160p it serves rungs to 3840x2160 VP9 at **3.0-5.4 Mbps**.
`youtube` refuses an upload under 2160p.

## What each route actually hands you

`ffprobe`, 10 September 2026. The local column is FC38's opening scene at 4K/Recommended; the cloud
column is C18's 2:21 cut at 4K, and EC51's 8 September publish is the second cloud reading.

| | Local export | Cloud publish |
|---|---|---|
| Video | h264 High, 3840x2160, **18.4 Mbps** at Recommended | h264 High, **29.7 Mbps** on C18, **7.8 Mbps** on EC51 |
| Bitrate control | High / Recommended / Low, printed in Mbps beside each row | none; the encoder picks, and the two readings above are the spread |
| Colour | `bt709` for primaries, transfer and matrix | `smpte170m` on EC51; `bt709` primaries with an `iec61966-2-1` transfer over full-range `yuvj420p` on C18 |
| Audio | AAC **48 kHz**, 128 kbps | AAC **44.1 kHz**, 160 kbps |
| Extras | a `mov_text` subtitle track unless Advanced turns it off | none |
| Cost | the tab is busy for the whole encode | 15 min for a 2:21 cut, nothing local held |

**The cloud's colour tags are two different wrong tags, not one.** Whatever it writes,
`pnpm youtube:master` restamps bt709, so a master built through that step is right either way.

**The colour tag is not decidable from the render alone.** If Descript converted with 709 and
mistagged, retagging is lossless; if it genuinely converted with 601, the file is self-consistent
and retagging breaks it. Check first: `descript pull` the original take, sample the same frame from
both, compare saturation. Only if they diverge is this the fix, and it re-encodes nothing:

```
ffmpeg -i master.mp4 -c copy -color_primaries bt709 -color_trc bt709 -colorspace bt709 out.mp4
```

**A dark, plain background is a bitrate decision as well as a lighting one.** At 7.8 Mbps for
3840x2160 the encoder is rationing, and a brightly lit wall of high-contrast posters behind a
talking head takes those bits off the face. Measured on EC51: the background sat 1.33 stops
*brighter* than the subject.
## Timings

| at 4K | 442-second cut | 1367-second cut | 1834-second cut |
|---|---|---|---|
| render | **22 min**, 18.8 Mbps, 1.05 GB | **~22 min**, 29.0 Mbps, 5.0 GB | **17 min**, 8.6 Mbps, 2.01 GB |
| download, 8 ranged connections | **135 s** at 7.8 MB/s | ~11 min | **298 s** at 6.7 MB/s |
| download, one stream | ~45 min at ~400 KB/s | hours | - |

All three came back 3840x2160 h264 at 30, decoding clean to the last frame, each duration matching
its composition to the millisecond.

**Render time tracks runtime; bytes do not.** The 1834s cut came back at 8.6 Mbps where the shorter
1367s one took 29.0, because the encoder rates the picture: a talking head over a static screen
recording compresses far below a cut full of motion. Estimating a size off the table was wrong by a
factor of three, so quote no GB figure before the render lands.

The signed Google Storage URL throttles per connection, not per file, and signs `host` only, so
`Range` is free. `--download` takes eight connections by default and streams each range to its
offset rather than buffering it, because eight buffered chunks of a 5 GB render is 5 GB of RSS;
`--connections 1` is the old single stream. The streamed and buffered files hash identically.

## Traps

- **`GET /v1/jobs` answers `{ data: [...] }`, not an array**, and omits `download_url`. Only the
  single-job GET carries the URL.
- **`progress.percent` sits at 15 for the whole render.** `job_state: stopped` is the terminal
  value; never poll on the percentage.
- **A publish replaces the composition's existing share URL** rather than minting a new one, so
  naming the wrong composition overwrites the wrong link.

## Where renders land

**`--download` writes to `~/Downloads/`, always.** His ruling, 4 September 2026: *"always download
in downloads folder"*. One flat folder, the composition's own name as the filename, and he files it
from there. Never into a repo: five videos of one course are 2.1 GB, and a `video/` folder inside a
repo is tracked.

**Pass the folder, not a filename.** `--download ~/Downloads` names the file after the
composition and takes the extension from what the server serves. Before 2026-09-10 a folder target
took the URL's basename, which for a publish is the remux proxy's endpoint, so FC38's 4K master
landed as an extensionless `remux`.
