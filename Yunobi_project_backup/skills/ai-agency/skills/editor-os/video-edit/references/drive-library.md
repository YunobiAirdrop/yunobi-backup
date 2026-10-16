# The drive media library, and the eight-folder shelf

Read this before reorganising "My media", which is the drive's library and not a project's.

## The five verbs

```bash
pnpm descript library                                  # the whole tree, with paths and ids
pnpm descript library mkdir "Backgrounds"              # --parent nests it
pnpm descript library rename "brand-grid-3840x2160.mov" "Brand Grid Dark.mov"
pnpm descript library mv "Brand Grid Dark.mov,Brand Grid Light.mov" Backgrounds
pnpm descript library rm "ZZ probe"                    # a folder takes its contents with it
pnpm descript library import sounds.json --folder "Sound Signature"
```

**`/v2/drives/{id}/assets` is the wrong place to read a name.** It reports
`metadata.default_display_name`, the original upload filename, which never changes; the library's
own name lives only on the `drive_media` record. A file renamed in the app therefore reads back
under its upload name and looks untouched. Read it with `library`.

**`library import` is the shelf's own upload**, `POST /jobs/import/drive_media`, and it is the only
write path for bytes. It takes no `drive_id` (the drive is the token's) and answers a bare 500 to a
manifest over three files while uploading none of them, so the command batches in threes.
`--folder` files the upload; without it a `Folder/Name.wav` key creates the folder.

An asset already sitting in one of the drive's own projects still has to come down and go back up:
nothing adopts an existing asset onto the shelf. Import from the local originals where they exist.

## The shelf is eight folders on any drive

Short on purpose: each folder answers a question an editor asks mid-edit, and a ninth is almost
always one of these eight under a private name.

```
B-roll/            your own footage, in subfolders by subject (Desk/, Outdoors/)
Backgrounds/       the plates a title sits on
CTAs/              one movie per ask
Motion/            graphics you own outright
Overlays/          alpha clips that composite over the face
Placeholders/      the stand-ins a layout pins until real media arrives
Products/          one subfolder per product or vendor
Sounds/            every sound the layouts play, and nothing else, under the kit's names
```

- **The shelf mirrors the layout project, folder for folder**, so an editor who has learned one
  panel has learned both.
- **Only what a layout actually plays**, read off the document rather than the folder: a sound a
  card plays sits on `pinScenes[].timeline.superTau.taus[0].audioSegment.mediaRefId`, which is not
  a timeline and never appears in `usage`. Eight generated wavs sat on this shelf for two days on
  no card in any project.
- **The name states what the file is, not what the exporter called it.**
  `02_broll_run-park_4k.mov` is 2160x3840, so `_4k` read as landscape and the clip is vertical.
  Read a frame size off `assetJson.quality.original.video`, and rename at the source too.
- **Nothing derived.** No sequences, no fonts, no `Roomtone - …`, which Descript writes one of per
  media file and which is per-project, not kit.
- **`Sounds/` is the kit's own vocabulary, not the stock browser's.** `whoosh`,
  `whoosh-hi`, `whoosh-mid`, `whoosh-deep`, `swish`, `zoom`, `riser`, `readout`, `shuffle`, `ui`,
  `chime`, `chime-soft`, and `mouse` for the one voice only the layout pack plays. **The pack itself
  carries eleven of these**, not thirteen (no `zoom`, no `chime`): the shelf is every sound we own, the pack is the set its own
  cards play. See [layout-pack.md](layout-pack.md). Those names are
the sound library's JSON
, which is also the app library's Descript kit shelf, so a sound has one
  name from the census through to the timeline. It held `Chime Light` and `Whip Low Whoosh` until
  8 Sep 2026, which is the same file under the name whoever sold it chose. The folder was called
  `Sound Signature` on the drive and `Sounds` in the layout project until 9 Sep 2026; the shelf
  mirrors the project, so the project's name won.

## A file at the root of the Files panel is a fault, and `lint` says so

`pnpm descript lint <project>` warns on **media at the root of the Files panel, in no folder** and on
**media in the library the folder tree never files**. The author, 9 Sep 2026, looking at four takes
sitting above every folder: *"files at root, which is a bug that the cli should lint."* It breaks
nothing, which is why it warns rather than blocks - and is exactly why it survives, because every
other invariant in that gate asks whether an id RESOLVES and none of them asks where a file sits.
`Internal` reports seven; `Brand Layouts` reports none.

**A panel showing upload names in a flat list is not a messy project, it is a client that could not
load the document.**`brand-testimonials-highlight.mp4`
 where the document says
`Products/Brand/Testimonials Highlight.mp4` is `metadata.default_display_name` - the upload filename
that never changes - which is what the panel falls back to when the drive's media endpoint fails. On
9 Sep 2026 that endpoint was answering **503** and the console carried `suppressing local load
failure`; the document was clean the whole time. **Read the tree with `pnpm descript tree` before
concluding a project is disorganised**, because the panel and the document can disagree and only one
of them is the project.

## Deleting an asset breaks every project that adopted it, and the repair needs no timeline surgery

**An asset is not owned by the project that uploaded it.** `Extra Fast Multimedia Whoosh 3` was
uploaded into `Brand Layouts` - its own `lookup_key` still names `projectId=9765b037` - and the
video `ClickUp Super Agents Just Got MCP` adopted it. Deleting it from the pack on 8 Sep 2026 left
the video with a media reference whose `assetGuid` resolved to nothing: a row that spins for ever in
the Files panel. Nothing in the pack showed it, because the pack was clean.

The repair, and it touches no card:

```bash
pnpm descript pull <video> "Multimedia Whoosh" --out /tmp     # the artifact usually survives
pnpm descript import <video> fix.json                          # a fresh copy, under a temp name
pnpm descript media swap <video> "Extra Fast Multimedia Whoosh 3" "whoosh-fix-donor.wav"
```

**`media swap` is the whole answer, not delete-and-re-add.** It puts the new asset under the id the
cards already hold, so every pin keeps its place and its gain, and it consumes the donor. Deleting
the reference first would mean taking it off the sequence and restamping every card that drew it.

A reference with no `assetJson` is NOT proof of breakage: an asset adopted from the drive library
carries none, which is why both CTA movs in that video read as missing and are fine. The test is
whether its `assetGuid` appears in `assets <project>`.

## Teaching it to somebody else

`CLIs/descript/connect.html` is the setup-day page and `pnpm descript connect` opens it. **It is a
face over the terminal, not a manual**: it names the three things only a person can do - sign in,
copy the session, make a token - then shows a real screenshot of the finished shelf, because nobody
is going to type `library mkdir` forty times. His words: *"nobody will do that by hand… explain
them with actual screenshots what they need to do 1st to help you do it a 100% agentic."*

It ships with the product a student buys, so it is not a playground page.
The course deck on connecting Descript carries the same split and the same screenshot, so an edit
here belongs there too.
