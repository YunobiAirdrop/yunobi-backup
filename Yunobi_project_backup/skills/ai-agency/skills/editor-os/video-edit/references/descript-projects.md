# Descript Projects

The edit workspace: media into a project, named and filed, and every organising verb over it.
This is pass 0 (organise), the music bed of pass 4, and the handoff of pass 7.

## The command surface

```bash
cd <the CLI directory>
pnpm descript projects --all                       # every project in the drive, with its folder
pnpm descript folders                              # the DRIVE folder tree
pnpm descript tree <project>                       # the Files panel: folders, names, ids
pnpm descript comps <project>                      # the Compositions panel, in sidebar order
pnpm descript usage <project>                      # which video each recording belongs to
pnpm descript assets <project> --probe             # camera or iPad, size, rate, duration

pnpm descript project new "BATCH 5 - 09-26" --folder 60-Shorts
pnpm descript import <project> <manifest.json>     # --dry sizes the files first; `adopt` when another project holds it
pnpm descript rename <project> "Speaker Name-9" "RAW CAM Second Brain.MOV"
pnpm descript mv <project> "RAW CAM Second Brain.MOV" second-brain --index 0
pnpm descript mkdir <project> second-brain
pnpm descript new <project> "M10 · Vertical" --folder Shorts   # empty, AUDIO and sizeless: see cli.md
pnpm descript dup <project> comp:"M09" "M09 (alt cut)"         # script, timeline and all
pnpm descript rm <project> comp:"M09 (alt cut)"                # refuses a live publish
pnpm descript assets prune <project> --kind audio              # uploads no media ref points at. Read only
pnpm descript card rename <pack> Camera b2a8a71f "Intro Zoom" --type camera  # picker name, marker AND family
pnpm descript card space <pack> Text                       # one card per paragraph, markers carried
pnpm descript realign <project> <comp>                     # the repair for "sortTiebreaker already used"
pnpm descript pin rename <pack> Text 909445ab 0 "Text 1"   # the slot name `--say` fills
pnpm descript text animate <p> Text 7c504674 "Text 1,Text 2" --direction right --by Character  # Animation in: slide, per letter
pnpm descript paragraph repeat <pack> Text "0:00"          # a placeholder paragraph for a new pack card
pnpm descript layout publish <pack>                            # push those names into the picker
pnpm descript clip <project> <comp> <pin> --gain 1 --media whoosh.wav
pnpm descript card merge <pack> Camera a7e28e4d          # delete a card: its span joins the one before
pnpm descript pin <p> <comp> --media shuffle.wav --at "<card>" --sound --tail 0.2   # on the text's OUT flicker
pnpm descript media swap <p> "3 [00-18] Best Month.mp4" "re-render.mp4"
pnpm descript export local <p> <comp> --resolution 4K --quality high   # its OWN Chrome encodes it, into ~/Downloads
pnpm descript batch <project> ops.json --dry       # any tidy-up bigger than two files
pnpm descript share ulisannnn@gmail.com <id>,<id>  # editor gets Can edit, no drive seat; `shares <p>` reads it back
pnpm descript comments <p> --todo                  # his open notes nobody has answered Done: yet
pnpm descript comment reply <p> <id> "..." --done  # say it is placed. Never `comment resolve`: he ticks after checking

pnpm descript tracks <project>                     # the tracks; `align <media>` reads the word clock, `--from`, `--refit` and `--resplit` repair it
pnpm descript track rename <project> "Speaker Name-5" CAM
pnpm descript track mute <project> SCREEN          # --off makes it the live one
pnpm descript track shift <project> "CAM GS" --to CAM   # the keyed twin onto CAM's clock, which the gate demands
pnpm descript track add <p> <seq> CAM --media IMG_0001.mov --offset 29.24  # a phone-shot camera
pnpm descript track add <p> <seq> CAM --segments pieces.json  # [{at, offset, seconds, media?}]: a piece's own media lets one track span the takes of a joined sequence
pnpm descript sequence new <p> "SEQ <code> · <Title>" --media <mic> --frame <screen>  # a take with no sequence left
pnpm descript track mv <project> SCREEN 0          # the order down the left of the timeline
pnpm descript studio <project> CAM --on --intensity 0.5

pnpm descript gaps <project> <comp>                # every pause, longest first; gaps close --over 1 closes them
pnpm descript speakers <project>                   # speaker set / speaker add / speaker labels rm
pnpm descript correct <project> <comp> "wrong word" --to "right word"
pnpm descript cue <project> <comp> <card> <layer> --at 0.5 --zoom 1.3   # the keyframe behind Smart Zoom
pnpm descript card copy <project> <comp> <card> --to all               # Copy layout / Paste, no library in between
pnpm descript layer copy <project> <comp> <card> <layer> --to all       # Paste special, one layer
pnpm descript layer paste <project> <comp>                               # Cmd+C a card in the app: its framing onto every screen share
```

**Every editor move the app's history holds now has a verb**, measured off 84 action types on
2026-09-08, except the cloud tasks (Correct, Regenerate, Overdub, filler detection, room tone,
Underlord). Takes recorded as separate sequences become one with `sequence join`, and an empty
composition plays it with `comp fill`. `pnpm descript --help` is the list.

**The reads are not exempt either.** `get_project` is `comps` plus `assets`, and
`export_transcript` is the export's own subtitle track, pulled with `ffmpeg -map 0:s:0`, which is
the source the description block already demands.

**`comp:` and `media:` say which panel.** Descript names a sequence after the composition built
from it, so one name is a composition AND a mediaRef. Unprefixed, that pair is refused rather than
guessed.

**Every write replays the whole commit graph**, so twenty-six renames one at a time is twenty-six
replays: a reorganisation is one `batch`. The ops key is `item`, and a wrong key resolves to
`undefined` and dies on op 1. Credentials, the write model, the storyboard variant, importing bytes
and handing the CLI to somebody else: [cli.md](cli.md), before any write bigger than a rename.

## Pass 0's own detail

**The pack's camera cards bind to a track named `CAM`**, so a sequence whose tracks still carry
their recorder names refuses every `layout pace` and `layout apply` (EC51, 8 Sep 2026: "has no
CAM track for that layer"). That is why organise is a pass and not a tidy-up afterwards, and why
it reads the ASSETS and the ALIGNMENT too: FC38's camera was uploaded and never joined to its
sequence, its transcript carried right words over wrong times, and `tracks` printed clean through
both.

Read the clock once, at the top of pass 3, with `pnpm descript layout cards <project> <comp>`:
that is the shot list, and every `[mm-ss]` comes from it. A timecode taken from the raw take is
not offset, it is meaningless, because the line may have been cut.

## Layouts and the bed

```bash
pnpm descript layout sync                          # re-read every pack, rewrite the manifest
pnpm descript layout pace <p> <comp> --to 0:40 --ladder "Camera/Cam 110,Camera/Cam 130"
pnpm descript layout apply <p> <comp> --use "Camera/Cam 120" --at 2:15  # --split cuts a new card
pnpm descript layout cards <p> <comp>
pnpm descript stock music search "<query>" [--limit N] [--json]   # Descript Stock music
pnpm descript stock music pull <p> <id-or-title> [--as "Music/<name>"]   # into the project's Music folder
pnpm descript music set <p> <comp> --use "<name>"
```

`stock music search` prints id, title and length, and that is all the shelf returns: no tags, mood or genre, so the query does the filtering. `stock music pull` accepts the id or the exact title (a title two tracks share is refused, pass the id), files the WAV under `Music/<title>` unless `--as "folder/name"` says otherwise, and puts nothing on a card: `music set --use "<title>"` does that. Pulling a track the project already holds is a no-op. It fetches a 25 MB file server side, so allow up to 30 seconds. `--dry` prints the name it would file.

**Pass 4 offers three options and moves on.** It never lays a bed and never blocks on him (29 Sep
2026, the author: *"Editor OS should be capable of giving me a few options instead of being stuck."*).
The person answered "what should your videos sound like?" once, on the setup page, and
`editor-os music` prints the answer and its search terms. Style `none` means no card: mark the
pass done with that as the evidence. No answer yet, don't ask: offer one track from each of three
styles that fit the video, and never save a style he didn't say. Then:

1. `stock music search "<term>" --json --full` each term, best first, until a few candidates come
   back. `--full` keeps the `preview` link the page plays.
2. Choose three by what the results show. Each has to run at least 20 seconds (the loop covers the
   rest), sound like the mood by its title and not like a vocal or a jingle, and differ from the
   other two. A track already in a sibling project's `Music/` wins a tie, so a channel keeps a sound.
3. `stock music pull` each into `Music/`, then `editor-os music offer <project> '<json>'` with
   `[{"id","title","seconds","mood","preview"}]`, one word or two of `mood` each. The studio saves
   the previews beside the project and shows the Music card. Mark pass 4 done with the three titles
   as the evidence, and go on to pass 5.
4. Don't run `music set`. `place` lays the one he keeps (0.211, ducking, loop) and lays nothing on a
   skip, and it refuses until he has decided. If `editor-os wait` returns `music.more`, he wants
   others: run the search again on the next terms and offer a new set. `asked` says how many times.

**Run `layout sync` before choosing a card, every time**: he edits the packs, `layout seed` reports
`alreadyHeld` and keeps the stale copy, and the manifest it rewrites is what says what a card is
FOR, where the library only holds its ink. **A layout is a stamp, not a link**, and a ladder splits
on commas, so a card whose NAME holds one goes in by id. **A camera layout needs a SEQUENCE**,
declared as its own `add_media` entry, `tracks: [{media: "<key>"}]`, or every camera card is
refused. **Read the layers back after any screen stamp**, and take a layer off with `layer rm`: a
`sceneId` naming a scene nothing draws locks the project out of its own editor. A CLI-stamped
composition publishes (EC51, 8 Sep 2026: 48 stamped cards, 21 pins, 4K in 14 minutes), and a
finished job is pulled again with `descript job <id> --download`, never re-rendered. The pack list,
the zoom ladder and its numbers, the `--with` placeholder rule, the fixed 0.211 bed, and lifting a
placed clip back off a card: [layouts-and-music.md](layouts-and-music.md).

**The screen's size is set per video, never taken from the pack.** Each recording crops differently,
so the SCREEN box in the PiP layout and in the big-head layout (camera large on the right) changes
from one video to the next. The author frames one card of each layout in the app and copies it (Cmd+C).
Then `layer paste <p> <comp>` puts that framing on every card in the same layout. Run it once per
layout, and read the sizes back after (P33, 25 Sep 2026: PiP 0.90×0.53, big head 0.72×0.39 at x 0.39).

## Every name carries its number and its timecode

One folder per video holding that video's raw take and its three clip folders; the number is the
beat and a letter suffix marks alternatives. The import key IS the display path, the value is the
local path as a bare string, and the MCP's `add_media` object is the wrong shape here. Raw takes
at `RAW CAM|IPAD|MIC`, sequences at `SEQ <code> · <Title>`, batches at `BATCH <week> - MM-YY` off
the recording month. The naming rules, both folder shapes, the batch numbering and the manifest
shape: [naming.md](naming.md).

## One project, one sequence, four layers

However many takes, a project holds one sequence and one composition filled from it: `sequence
join` the takes in order, then `comp fill`. Every take carries `CAM`, `CAM GS`, `MIC` and `SCREEN`.
Sync each camera from the audio, head and tail, never by eye. On the Claude Code tutorial, two
cameras dropped at 0 by hand sat 1.04s and 6.5s off. An intro recorded with the camera inside the
web recorder has no separate mic, so that one file is `MIC`, and `CAM` and `CAM GS` play an
untranscribed copy of its mediaRef. The same transcribed file on a muted track makes the app drop
its words.
A take whose sequence got deleted, or one `adopt`ed from another project, gets a new one with
`sequence new`. A series too heavy for one project is one project per part:
`<Title> - Part N · <Topic>` for the project and its composition, `SEQ <same>` for the sequence,
raw files `RAW CAM|MIC|SCREEN <Take>`.

## The two gates: the tracks at the start, every setting at the end

`descript tracks` ends on `tracks clean` or a fault per line, and pass 0 ends when it reads clean:
one track live, only that track in the script, `CAM GS` on CAM's clock to half a frame
([audio-and-tracks.md](audio-and-tracks.md)). `descript settings` is the last pass, every audio
and look setting against its standard: [finishing.md](finishing.md).

## The drive media library is a different surface

The "My media" panel is the drive library, not a project's: eight folders on any drive, read with
`pnpm descript library`, never with `/v2/drives/{id}/assets`. [drive-library.md](drive-library.md).

## Pulling a finished composition to disk

Only when he asks for it, after his own pass. Both routes land in `~/Downloads/`. `export local`
is the better master since 4K and 2K were ungated on 10 September 2026; `publish` when the browser
must stay free, for the share URL, or when a local export refuses a clip.
[publishing-and-download.md](publishing-and-download.md).

## Verification checklist

- [ ] Every `[mm-ss]` came from `layout cards`, never from the raw take
- [ ] Every import key carries its folder path, its sort prefix and its timecode
- [ ] Raw take, bed, motion and b-roll for one video sit in the same folder
- [ ] The composition has exactly one bed, and `music <project>` reports it ducking
- [ ] Any composition created carries the orientation the take was shot in
- [ ] `tree` confirms every file landed with the intended name
- [ ] Any composition touched was checked against `publishes` first
- [ ] `tracks` and `settings` both read clean before the render
