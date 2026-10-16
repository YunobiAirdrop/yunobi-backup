---
name: descript-projects
description: "Creates, names, folders and reorders everything in a Descript project from the terminal: projects, imported media, folders in both panels, and compositions. Use when footage or b-roll needs to land in Descript, when a project or a drive is disorganised, when a composition has to be created, duplicated or filed, or when planning an import so the names come out right the first time."
tags: [drives, descript, video]
---

# Descript Projects

This skill covers the edit workspace: getting media into a Descript project, named and filed correctly. It does not cover encoding, scheduling or distribution.

- Cutting the script itself - false starts, retakes, filler - when `prompt_project_agent` cannot: `descript-script-edit`. That skill owns the browser-driven editing surface and its failure modes.
- Encode, ClickUp task, Drive upload, calendar: `shorts-production`. That skill starts where the camera stops; this one runs alongside it whenever the edit happens in Descript.
- Publishing the finished master to networks: `social-scheduling`.
- Writing the opening: `video-hooks`.

## The order of the edit

An edit is five passes, and they only work in this order. Each one needs the pass before it to have
settled, and doing them out of order is how a clip gets built for a beat that the next pass cuts.

1. **Cut** (`descript-script-edit`) — everything downstream is timed against it.
2. **Layouts** (`layout pace`, `layout apply`) — they decide what the frame holds, so motion built first fights them.
3. **Music** (`music set`) — the bed sets the pace the motion is cut to.
4. **Motion** (`motion-design`, then `import` into `Motion/`) — built to the clock the first three fixed.
5. **B-roll** (`broll-research` sourcing, then `import` into `B-roll/`) — borrowed picture last,
   because it fills what is left.

Read the clock once, at the top of pass 2, with `pnpm descript layout cards <project> <comp>`:
that is the shot list, and every `[mm-ss]` below comes from it.

The five passes as commands, `layout list/pace/apply/cards`, `music set` and `import` with the
flags each one takes: [`references/writing-the-document.md`](references/writing-the-document.md).

**A camera layout needs a SEQUENCE, and an imported file is not one.** A composition built from
`add_compositions` clips draws transcript scenes, `sequenceScenes` stays empty, and every camera
card is refused with "has no sequence for it to draw". Declare the sequence as its own `add_media`
entry, `tracks: [{media: "<the recording's key>"}]`, and point the clip at that. `tracks[]` is one
media per track, so **two takes of one video are joined before import** with `ffmpeg -c copy`.
And **a CLI-stamped composition does not publish** (2026-08-30, open): one `layout apply` turns a
working publish into "Job failed unexpectedly", and one copied `Title` pin is enough. Export from
the app, and never report an edit delivered on a publish never run.

**A layout is a stamp, not a link**, so the CLI holds the ink: `layout seed [pack]` reads a pack's
own cards and stamping one copies its gradients, CTA movies and fonts in with it. Re-seed rather than trusting a count: `layout list`
said 19 of 45 could not be stamped and told the reader to apply each one by hand, and a single
`layout seed` learned 18 of them (2026-08-30). The recent videos are on `YouTube - 2026` or
`ClickUp Master`, not the layout pack named in the picker's title. `apply` restamps the card the anchor falls inside;
`--split` cuts a new one. The bed is a fixed 0.211 with ducking on, never a per-video decision.

**The intro and the outro carry a zoom sequence, not one framing**, because a read held on one frame
marks nowhere that a thought ends. `layout pace` cuts one card per beat and cycles a ladder across
them, in the pack the video is already on, reaching the tightest step once a stretch on the hardest
line. It comes before motion: motion cannot rescue a flat open. Read the layers back afterwards,
never the card list - a card can carry a layout and still draw nothing. The ladders, and all of the
above, in [`references/writing-the-document.md`](references/writing-the-document.md).

## The rule that ranks above the rest

**Nothing in a Descript project is write-once, and neither the browser nor the published API is the
way to fix any of it. `pnpm descript` is.** His instruction, 30 Aug 2026, after the published API
broke an edit he then re-uploaded by hand: **"avoid using the descript API"**. So `import_media`,
`prompt_project_agent` and `publish` are the last resort, not the first: every organising verb, every
rename and every layout goes through the CLI, which writes `collab/commits`, one commit per edit,
exactly as the app does, which is why every organising verb below is one command (2026-08-24). A
**storyboard** project - every layout pack, and anything migrated - stores one JSON document per
revision instead, and the same verbs write those too (2026-08-25). The endpoint, the two credentials, the storyboard save and the
rule against route discovery in a live project:
[`references/writing-the-document.md`](references/writing-the-document.md):

```bash
cd <the CLI directory>
pnpm descript projects --all                       # every project in the drive, with its folder
pnpm descript folders                              # the DRIVE folder tree
pnpm descript tree <project>                       # the Files panel: folders, names, ids
pnpm descript comps <project>                      # the Compositions panel, in sidebar order
pnpm descript usage <project>                      # which short each recording belongs to
pnpm descript assets <project> --probe             # camera or iPad, size, rate, duration

pnpm descript project new "Batch 5" --folder 60-Shorts
pnpm descript import <project> ~/clip.MOV --as "second-brain/01 Notes App.MOV"
pnpm descript rename <project> "Speaker Name-9" "00 RAW Second Brain.MOV"
pnpm descript mv <project> "00 RAW Second Brain.MOV" second-brain --index 0
pnpm descript mkdir <project> second-brain
pnpm descript new <project> "M10 · Vertical" --folder Shorts   # an empty composition
pnpm descript dup <project> comp:"M09" "M09 (alt cut)"          # script and timeline and all
pnpm descript rm <project> comp:"M09 (alt cut)"                 # or media:<name>; refuses a live publish, refuses media still on a timeline
pnpm descript media swap <p> "3 [00-18] Best Month.mp4" "re-render.mp4"   # a re-render onto the card the old one is stamped on
pnpm descript project mv <project> 60-Shorts

pnpm descript tracks <project>                                  # the tracks inside its sequences
pnpm descript track rename <project> "Speaker Name-5" CAM
pnpm descript track mute <project> SCREEN                        # --off to make it the live one
pnpm descript studio <project> CAM --on --intensity 0.5          # Studio Sound, on the media
```

The layout and music verbs are in [`references/writing-the-document.md`](references/writing-the-document.md); `vibe-kit/CLIs/descript/README.md` holds how the write works and what it refuses.

**`comp:` and `media:` say which panel** (2026-08-24). Descript names a sequence after the composition built from it, so `T1 webm over magenta` is a composition AND a mediaRef, and a full path does not separate them: the composition's path IS the bare name, which is exactly the sequence's name. Unprefixed that pair is refused rather than guessed, and the prefix is the only way to address either one by name.

One folder per session, slug-cased, raw takes at `00 RAW CAM|IPAD|MIC`, sequences at
`SEQ <code> · <Title>`. Getting the name right at import still beats fixing it, but a wrong name
is one command now. The example tree is in [`references/naming.md`](references/naming.md).

**The mechanics behind these commands** - what `new` writes, why `dup` never dangles, how composition
folders work, why a tidy-up is one `batch`, and how a recording session gets its name from what uses
it - are in **[`references/writing-the-document.md`](references/writing-the-document.md)**. Read it
before any reorganisation bigger than two files.

### "Can you reorganize this project" is one batch

Write the ops file, `--dry` it, run it. **`prompt_project_agent` is not the route** for media or
composition names: it is metered on AI credits and it substitutes. And **the API only controls names
for media it imports**, so most of the mess it cannot reach: do not sell a tidy-up as a fix, hand
over four underscore-prefixed bucket folders instead. Full procedure in the reference.

## A layout pack is a project too

A pack is a storyboard project, so every verb above works on it. `card list` and `card rename`
read and write the three names a card carries, `resize` sets the frame its cards are offered at,
and `layout publish` is the only thing that shows any of it to another project, because saving
does not. All four, and the storyboard save, in
[`references/writing-the-document.md`](references/writing-the-document.md).

**`pnpm descript import` puts a file into one** (2026-08-28), through the app's own upload route
(`via: app upload`). The *published* API still refuses template projects, so the MCP
`import_drive_media` fallback in [`references/import-mechanics.md`](references/import-mechanics.md)
is only needed when the CLI's session credential is dead.

## The drive media library is a different surface, and it has its own commands

The "My media" panel is the **drive** library, shared by every project, and nothing in it lives in a
project's collab document. `pnpm descript library` reads it; `mkdir`, `rename`, `mv`, `rm` and
`import` write it. **The shelf is eight folders on any drive** - `B-roll`, `Backgrounds`, `CTAs`,
`Motion`, `Overlays`, `Placeholders`, `Products`, `Sound Signature` - mirroring the layout project
folder for folder, holding only what a layout plays, carrying nothing derived. Read a name with
`library`, never with `/v2/drives/{id}/assets`, which reports the upload filename and shows a
renamed file as untouched: **[`references/drive-library.md`](references/drive-library.md)**.

## Reorganising the media browser, the browser fallback

`pnpm descript mv/rename/mkdir/rmdir` does all of this in one call each. The hand route - pairing
takes through **sequence** durations, `RPReplay_Final<n>.MP4` as the recording's end timestamp,
naming a sequence from the course - is in
[`references/browser-fallback.md`](references/browser-fallback.md). Ask which lesson a take
belongs to rather than inferring it: a misfiled source take is worse than a loose one.

## Folder by video, never by asset type

`pnpm descript import <project> <manifest.json>` does the whole flow (job, uploads, poll); `--dry` sizes the files first. The import key **is** the display path, and a `/` in it creates a folder:

```json
{ "clickup-terminology/00 RAW ClickUp Terminology.MOV": { "content_type": "video/quicktime", "file_size": 401830273, "language": "en" } }
```

One folder per video, holding that video's raw take and its three clip folders together: `Music`
(the bed, one file, no beat number), `Motion` (built here, ours outright) and `B-roll` (borrowed
picture). They are apart for licensing rather than tidiness: a borrowed shot cannot ship in a paid
lesson. A second video gets its own folder beside it, same shape, never `Raw/` plus
`B-roll <Video>/`, which opens two folders to cut one video. A single-video project keeps the three
at its root.

## Every name carries its number and its timecode

`N [MM-SS] Description.ext`

The number is the **beat**, not the clip, with a letter suffix (`2a`, `2b`) for alternatives, and it
sorts the browser into edit order, so the media browser *is* the shot list. The timecode says where
the beat sits, taken against the cut rather than the raw whenever a composition exists. Both folder
shapes drawn out, and the seven rules behind the pattern:
[`references/naming.md`](references/naming.md).

**When there is no take yet, drop the bracket rather than inventing one** (2026-08-21). B-roll often
arrives before the camera does, so the project holds no raw take, the composition reports 0 and there
is no clock at all. A guessed `[01-20]` then reads as measured. Import as `N Description.ext`, keep
the number so the browser still sorts into edit order, and add the bracket after the cut.

## The audio, and the tracks inside a sequence

Which track gets transcribed (only the microphone, and how to strip the others), and the
`sequenceScenes` that the timeline draws as track headers - `tracks`, `track rename`, `track mute`,
`studio`, the CAM/SCREEN/MIC naming and the one-live-track rule:
**[`references/audio-and-tracks.md`](references/audio-and-tracks.md)**.

Two things are load-bearing enough to repeat: **exactly one track stays live per sequence**, because
two open captures of one room is comb filtering that nothing but listening catches, and **Studio
Sound belongs to the media**, so turning it on for one track turns it on everywhere.

## The CLI is authenticated; load its env before believing otherwise

`pnpm descript` reads `DESCRIPT_STYTCH_SESSION` and `DESCRIPT_API_TOKEN` off the process environment
and loads no `.env` itself. Both live in `vibe-kit/CLIs/.env` and both are valid, so the "is not set"
message reads exactly like a logged-out session and is not one. Export them and run the whoami before
writing that anything is signed out. **Anyone else connects with `pnpm descript connect`**, which
opens the walkthrough page, takes both values on the prompt and verifies them with a real call:
**[`references/cli-auth.md`](references/cli-auth.md)**.

## Lifting a pin off the timeline: the transparent plate

Nothing removes a pin. A fully transparent qtrle plate cut to the card's exact length, swapped in
for the unwanted clip, hands that card back to the face underneath. Swap by media id, never by name:
**[`references/removing-a-pin.md`](references/removing-a-pin.md)**.

## Import mechanics

The REST fallback when there is no connector, the 3-per-call MCP cap, one-job-at-a-time, and why
direct upload beats URL import: **[`references/import-mechanics.md`](references/import-mechanics.md)**.

## Never let the agent substitute

`prompt_project_agent` will do *something* adjacent when it cannot do what was asked, and report
success - on 2026-08-01 it renamed tracks inside a live published composition instead of the media
it was asked about. Every mutating prompt ends with an explicit refusal clause, and the run is
verified with `get_project`, never `agent_response`. The clause and what to check:
[`references/writing-the-document.md`](references/writing-the-document.md).

## Pulling a finished composition to disk, without opening Descript

Publishing a composition is what produces a downloadable file; the signed URL is on the **single-job** GET, one publish job runs per project, publish at the timeline's own resolution, and renders
live in `~/Movies/<course>/`, never in a repo. The full flow and its traps:
[`references/publishing-and-download.md`](references/publishing-and-download.md).

## Verification checklist

- [ ] The five passes ran in order: cut, layouts, music, motion, b-roll
- [ ] Every `[mm-ss]` came from `layout cards`, never from the raw take
- [ ] Every import key carries its folder path, its sort prefix and its `[mm-ss]` timecode
- [ ] Raw take, bed, motion and b-roll for one video sit in the same folder
- [ ] The composition has exactly one bed, and `music <project>` reports it ducking
- [ ] No import call carries more than 3 media entries, and `wait_for_job` ran between batches
- [ ] Any composition created carries the orientation the take was actually shot in
- [ ] `get_project` confirms every file landed, with the intended name
- [ ] Any composition touched was checked against `publishes` first
- [ ] The sequence's tracks are named CAM / SCREEN / MIC, and exactly one of them is live

## Self-Healing

New failure modes go to `references/learned-patterns.md`, newest first, with today's date. **Read
it before any import session**: most entries are a call that reported success while doing something
else. A limit stated in *this* file gets re-verified before it is repeated - "a storyboard project
cannot be written" stood for a week and was one unread route (2026-08-25).

The run each line came from, with its quotes and numbers, is in [`references/learned-patterns-archive.md`](references/learned-patterns-archive.md).
