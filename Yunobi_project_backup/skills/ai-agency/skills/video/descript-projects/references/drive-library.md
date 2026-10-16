# The drive media library, and the five verbs that write it

Split out of `SKILL.md`. Read it before reorganising "My media".

## The drive media library is a different surface, and it has its own commands

The "My media" panel is the **drive** library, shared by every project, and nothing in it lives in a
project's collab document. `pnpm descript library` reads it and five verbs write it (2026-08-29):

```bash
pnpm descript library                                  # the whole tree, with paths and ids
pnpm descript library mkdir "Backgrounds"              # --parent nests it
pnpm descript library rename "brand-grid-3840x2160.mov" "Brand Grid Dark.mov"
pnpm descript library mv "Brand Grid Dark.mov,Brand Grid Light.mov" Backgrounds
pnpm descript library rm "ZZ probe"                    # a folder takes its contents with it
pnpm descript library import sounds.json --folder "Sound Signature"   # local files onto the shelf
```

**`/v2/drives/{id}/assets` is the wrong place to read a name.** It reports
`metadata.default_display_name`, the original upload filename, which never changes; the library's
own name lives only on the `drive_media` record. A library renamed in the app therefore reads back
under its upload name there and looks untouched, which is what sent one session route-hunting for an
hour. Read it with `library`, never with `assets`.

**The panel has no New Folder button**, so a folder used to arrive only as the `Sound Signature/`
prefix on an upload. The standalone page at `web.descript.com/media-library` has one, and now so
does the CLI.

**`library import` is the shelf's own upload**, `POST /jobs/import/drive_media`, and it is the only
write path for bytes: `/v2/drive_media/{driveId}` answers 404 to a POST. It takes no `drive_id`
(`400 "drive_id" is not allowed`, because the drive is the token's) and it answers a bare **500** to
a manifest over three files, uploading none of them, so the command batches in threes. `--folder`
files the upload; without it a `Folder/Name.wav` key creates the folder, which is how
`Sound Signature/` arrived in the first place.

## The eight-folder standard, on any drive

**A shelf is eight top-level folders and no more** (2026-08-30). It is the same shape on a client
drive as on this one, it is what Editor OS teaches, and it is short on purpose: each folder
answers a question an editor asks mid-edit, and a ninth folder is almost always one of these eight
under a private name.

```
B-roll/            your own footage, in subfolders by subject (Desk/, Outdoors/)
Backgrounds/       the plates a title sits on
CTAs/              one movie per ask
Motion/            graphics you own outright
Overlays/          alpha clips that composite over the face
Placeholders/      the stand-ins a layout pins until real media arrives
Products/          one subfolder per product or vendor
Sound Signature/   every sound the layouts play, and nothing else
```

Four rules hold it together, and each one was learned by breaking it:

- **The shelf mirrors the layout project, folder for folder.** Same folder names, same file names,
  so an editor who has learned one panel has learned both.
- **Only what a layout actually plays.** Read that off the document, never off the folder: a sound
  a card plays sits on a `pinScenes[].timeline.superTau.taus[0].audioSegment.mediaRefId`, which is
  not a timeline and so never appears in `usage`. Eight generated `signature-v2` wavs sat on this
  shelf for two days and were on no card in any project.
- **The name states what the file is, not what the exporter called it.**
  `02_broll_run-park_4k.mov` and `03_broll_selfie-street_4k.mov` are both 2160x3840, so `_4k` read
  as landscape and the clip is vertical. Read a frame size off
  `assetJson.quality.original.video`, and rename at the source as well as on the shelf.
- **Nothing derived.** No sequences, no fonts, no `Roomtone - …`, which Descript writes one of per
  media file and which is per-project, not kit.

**Adding to the shelf is `library import` per folder, and the bytes really move.** An asset already
sitting in one of the drive's own projects still has to come down and go back up, because nothing
adopts an existing asset onto the shelf: `/v2/drive_media/{driveId}/folder/{id}/add` exists and
refused every payload shape tried. Learn it with `spy` before guessing at it again. Import from the
local originals where they exist.

One instance of the standard, as built on 2026-08-30: `Products/` holds a folder per product
this channel demonstrates;
 `B-roll/` holds the eight personal clips out of the `B-rolls` project in
`70 - Recordings & B-roll`, which is the only place they lived; and every other folder mirrors the
the layout pack's Files panel exactly.

## Teaching it to somebody else

`CLIs/descript/connect.html` is the Editor OS setup-day page, and `pnpm descript connect` opens
it. **It is a face over the terminal, not a manual** (2026-08-30): it names the three things only a
person can do - sign in, copy the session, make a token - and then shows a real screenshot of the
finished shelf, because nobody is going to type `library mkdir` forty times. As it was put: *"nobody
will do that by hand… explain them with actual screenshots what they need to do 1st to help you do it
a 100% agentic."*

It is **not a playground page**, and it was wrong to symlink it there. The playground is his own
store of boards to look at once; this ships with the product a student buys. The course deck
The course deck on connecting Descript carries the same split and the same
screenshot, so an edit here belongs there too.
