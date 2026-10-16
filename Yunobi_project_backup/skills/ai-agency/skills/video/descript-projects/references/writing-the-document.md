# Writing the document: batches, compositions, and naming a recording session

Split out of `SKILL.md`. The mechanics behind the commands: what a new composition actually is,
how a duplicate keeps its media, why a tidy-up is one batch rather than twenty-six commits, and
how a recording session gets its name. `learned-patterns.md` holds the dates.

**Compositions are creatable, and the shape is not invented** (2026-08-24). A project created through the public API arrives holding exactly one composition and nothing else, and that is the template `new` writes: two taus (five seconds of nothing whose text is a zero-width space, then a terminal one), one card boundary anchored to the first tau, and the constant id `temp:vo-meta-track` on the voiceover track. `dup` regenerates every id the composition owns and keeps every `mediaRefId`, so the copy is a second cut of the same footage; on a real 17KB timeline that was 50 of 51 ids new, zero dangling media, and Descript's own API then computed the copy's duration and returned the original's to the last decimal.

**Composition folders exist and behave like media folders** (`mkdir --comps`, `mv`, `rmdir --comps`). `rootCompositionFolder` is the same tree shape as `rootMediaFileFolder`. No project in the drive had one before 2026-08-24, so it is proven as far as the document round-tripping and Descript's own API still reading every composition; eyeball the sidebar the first time you use it on something that matters.

**A batch is one command, not one per file** (2026-08-24). `pnpm descript batch <project> ops.json` takes a JSON array of `rename` (`item`, `name`), `mv` (`item`, `folder`, optional `index`), `mkdir` (`name`, optional `parent`, `root`, `index`), `rmdir` (`folder`, optional `root`), `newcomp` (`name`, optional `folder`, `index`), `dup` (`item`, optional `name`) and `rm` (`item`) ops, resolves them all against the document as the ops before them left it, and writes **one** commit. The key is `item`, not `target`; a wrong key resolves to `undefined` and the run dies on op 1 with `No item matches "undefined"`. Every write replays the whole commit graph, so twenty-six renames one at a time is twenty-six replays. `--dry` prints the resolved plan first. A whole project reorganised - eleven media into three new folders, six compositions into two new composition folders, one duplicate, one new composition - was 21 ops and one commit. Use it for any tidy-up bigger than two files.

**Name a recording session from what uses it, never from the file names** (2026-08-20). Two commands answer what the media browser cannot:

- `pnpm descript usage <project>` gives composition -> sequence -> the takes inside it. A composition references only the **sequence**; the sequence is itself a mediaRef whose tracks are `audio.trackSceneIds` pointing into `sequenceScenes`. That two-hop link is the only thing that says which camera roll belongs to which short, and it is why a multicam batch lands as four folders called Untitled.
- `pnpm descript assets <project> --probe` reads the file itself through the signed read URL, so nothing downloads. The name never says the device: on BATCH 3 the camera takes were 3840x2160 at 30 and the screen recordings 1640x2360 at 60, which is the iPad Air 10.9 panel and no iPhone. `RPReplay_Final*.MP4` is an iOS **screen** recording; `IMG_*.MOV` is the camera roll; a Descript-recorded take carries `source: web-recorder` and is named after the speaker.

**A composition renames the same way** (2026-08-20). Its name is `compositions[].name`, so `pnpm descript comps` for the id and `pnpm descript rename <project> <id> "<name>"` for the change. The commit carries the app's own `EDITOR/DOCUMENT/SET_TRACK_NAME` and `trackId`. The app calls a composition a **track** in its action types, a **scene** in `published_projects.source_scene_id`, and a composition in the document; only the last name is the one in the document.

## How the write actually works, and what it refuses

Moved out of SKILL.md on 25 Aug 2026 to hold it under the 250-line ceiling.

The *published* API has no write path for names, and that is still true: the MCP's 14 tools, the spec's 12 paths carrying 13 operations, zero PATCH, zero PUT. What was wrong is the conclusion drawn from it. The app does not use that API. It writes `https://web.descript.com/v2/projects/{id}/collab/commits`, where a project is a trimerge-sync document and every edit is one commit carrying a jsondiffpatch delta. The media name lives in that document at `mediaLibrary.mediaRefs[].displayName`, the folder trees at `rootMediaFileFolder` and `rootCompositionFolder`, and the editor tabs at `compositions[]`.

**Two credentials, not one.** `DESCRIPT_STYTCH_SESSION` is the app's session and does everything inside a project. `DESCRIPT_API_TOKEN` is the public API token and is needed only by `project new` and `import`, because creating a project and uploading a file are the two things the app's own API refuses (`POST /v2/projects` answers `Classic project creation no longer supported`).

**Never do route discovery inside a project that matters, and never press undo in someone's editor** (2026-08-20). Learning the storyboard save route cost an incident: three stray characters typed into a live scene title, two `cmd+z` presses whose stack was not mine, and a version restore fired on a misread.The composition that looked deleted was being deleted by **a second session of the owner's own**, open at the same time in another browser, and the restore fought it.
 `is_live_collab_enabled` is false on these projects, so two open sessions race and the last save wins.

So: duplicate the project first and drive the copy, check the collaborator avatars in the top bar before touching anything, make the smallest possible edit, and never use undo to clean up - delete exactly what you typed instead. `File > Version history` keeps every autosave and its restore dialog names the version number, which is the only reason this was recoverable.

**A storyboard project writes differently, and every verb still works on it** (2026-08-25). A layout pack, and anything else with `is_storyboard_enabled`, keeps no collab document
: `collab/commits` and `collab/sparse_graph` are both empty, and the real document is one JSON file on S3 per revision. Reading it needs `GET /v2/projects/{id}/asset_url?url=<the revision's unsigned content_url>`, which answers a CloudFront URL signed for three hours - the revision's own `content_url` is unsigned and S3 answers AccessDenied, which is what made this look impossible for a week. Writing it is three calls: `GET /upload_file?content_type=application/json&extension=.json&filename=document-<32 hex>` for a presigned PUT, the **whole document** PUT to it, then `POST /v2/projects/{id}/revisions?content_format_version=2` with `{id, message, bundle_version, contents: {content_url, content, assets, json}, default_scene_analysis, base_revision_id, force_save, composition_summaries, is_late_revision}`. `head` and `commit` route both kinds, so `rename`, `mv`, `batch`, `tracks`, `card rename` and the rest need no special casing. Two things to hold: `base_revision_id` is enforced with a 409 rather than merged, so an open browser tab on the same project will beat you; and **publishing a pack is a separate route**, `POST /v2/projects/{id}/templates/publish` with `version_id`, without which every rename stays invisible to every other project. Ego lite is signed into Descript and is where the wire was watched; Orca is not.

**None of which blocks using the layouts**, which was the assumption for weeks and was wrong. A card
applied to a composition does not read the pack at render time: the app COPIES the layout's layers
into your document and leaves `templateSource: {projectId, cardId}` as a record of where they came
from. So the stamp is readable from any project that has used it, `layout harvest` collects them,
and `layout apply` writes them - all without the pack's bundle and without a signed-in browser.
The pack itself is readable and writable too since `asset_url` opened storyboard documents:
`layout seed` reads its cards, `card rename` edits them, `layout publish` pushes the names out.

**The app is not the API.** A composition's right-click menu in the Compositions list ends in **Delete**, and it goes through with no confirmation. So `New composition from file` → `export_transcript` → Delete reads the transcript of media that has no cut and leaves the project as it was.

## The five passes, as commands

```bash
# 1. cut - descript-script-edit owns this

# 2. layouts. Pace the intro and the outro; stamp the middle one call at a time
pnpm descript layout list                                    # the 52 cards, and which pack each is from
pnpm descript layout pace <p> <comp> --to 0:40 --ladder "Agency Master,Zoom S (110%),Zoom M (130%)"
pnpm descript layout apply <p> <comp> --use "Zoom 115%" --at 2:15
pnpm descript layout apply <p> <comp> --use "Screen + Portrait S" --at "the moment delivery" \
  --with "00 RAW IPAD Ops Ceiling.MP4"
pnpm descript layout cards <p> <comp>                        # read it back

# 3. music. The house bed is Descript stock, so it is adopted from a project that already
# holds it (its mediaRef, new id and assetKey, committed with `adopted`), not imported
pnpm descript music set <p> <comp> --use "Lofi Background Vlog Hip Hop"   # 0.211 gain, ducking on
pnpm descript music <p>                                      # read it back

# 4 and 5. motion and b-roll, named off the clock from pass 2
pnpm descript import <p> <manifest.json>
```

Moved out of SKILL.md on 31 Aug 2026 to hold it under the 250-line ceiling. The order of the
passes, and why it cannot change, stays in the skill.

## Layouts and the music bed, in detail

Moved out of SKILL.md on 25 Aug 2026 to hold it under the 250-line ceiling.

**A layout is a stamp, not a link.** Applying one copies the pack card's layers into your
composition; `templateSource` only records where they came from. So the CLI cannot write a layout it
has never seen.

**A pack seeds itself, and hand-applying each card is over** (2026-08-25). `layout seed [pack]` reads
the pack's own document and takes every card straight off it. What made this look impossible is that
a pack card carries **no `templateSource`** - it IS the source - so `harvest`, which keys on that
field, walked past all 22 of them. The id the app writes into `templateSource.cardId` when it stamps
a card is simply **the card's own id**, which is what makes the pack readable as a library. One call
per pack now seeds **52 cards over the three packs**, where hand-applying had seeded 6 in a month.
`layout harvest <project>` is still the road for a card no pack publishes any more, and a pack card
outranks a harvested copy in `merge`, because a copy is a print an editor may have thinned.

**A `--with` slot is marked on the tau, never guessed from the name.** The pack writes
`visual: { type: "placeholder" }` on the tau of every empty picture box, and that is the only honest
test: `Title` and `Subtitle` also draw no media, while `Gradient`, `Captions` and the CTA movies draw
media nobody is meant to replace. Naming rules were tried first and got `Camera/Subtext` asking for
three files it has no use for.

**A stamp brings its own media with it.** The gradient behind a title, the CTA movie, the font a text
layer is set in: a pack owns those and the project being stamped does not. The app copies each one in
as a **new mediaRef around the same `assetGuid`**, filed under `_assets`, or `_fonts` for a font -
which is exactly what the two projects already stamped from these packs were found carrying, with no
ref id in common and the guids matching. `apply` now does the same, and imports an asset once however
many cards ask for it.

**There can be more than one layout pack in a drive.** The oldest (22 cards) is
the one in the picker's title, but the recent videos are stamped from **`YouTube - 2026`**
(`078da627`, 25 cards) and a few from `ClickUp Master` (`1849eca1`, 4 cards). Check which pack a
video actually uses before assuming the house one: stamping a plain `Camera/Zoom 130%` into a video
built on `ClickUp Master/Agency Master` drops the branded background mid-sentence.

**The zoom ladder, measured off the cards.** A zoom is one layer, `contentScale` with a
`contentPosition` that walks down to hold the face as the frame tightens:

| Pack | Cards | Scale | Content y |
| --- | --- | --- | --- |
| The oldest pack | `Camera/Zoom 100%` | 1.00 | 0.500 |
| | `Camera/Zoom 115%` | 1.15 | 0.575 |
| | `Camera/Zoom 130%` | 1.30 | 0.650 |
| | `Camera/Zoom 145%` | 1.45 | 0.664 |
| `YouTube - 2026` | `Zoom S (110%)` | 1.10 | 0.500 |
| | `Zoom M (130%)` | 1.30 | 0.547 |
| `ClickUp Master` | `Agency Master` | 1.00 | 0.431, on a branded background |

Cycle a ladder of four to eight steps so it steps in and breathes back out rather than jumping wide
to tightest, and **let it reach 145% once a stretch**, on the hardest line in it - the claim, not the
setup. A ladder that never leaves 100-130 is as flat as no ladder, only busier.

**`apply` restamps the card the anchor falls inside.** Descript already cut the composition into
cards; choosing a layout changes the one you are standing on. `--split` cuts a new card instead, and
is the rarer verb.

**A picture layer needs a track as well as a composition, and a pack card names neither.** Every card
has one layer drawing the speaker; a stamp has to point it at the composition it landed in AND at the
`sequenceSceneId` of the track that composition cuts from. Miss the second half and the layer draws
nothing, so the card renders as **a flat rectangle of its own background colour** - navy, on the
`Zoom 115%` and `Zoom 145%` cards, which carry a `solidColor` the others do not. Harvested stamps
already held a track id and hid this for a week; a seeded pack card holds none, so `apply` now writes
one on every picture layer and refuses a camera card outright when the composition has no sequence.
A card with two picture layers (`Large Face + Screen`) gets the same track on both and its second one
still has to be set by hand.

**An intro and an outro are paced, not stamped once.** `layout pace <p> <comp> --ladder a,b,c
--from --to` puts one card on every beat of a stretch and cycles the ladder across them, restamping
the card already standing on a beat and cutting one where none stands. A beat is a **tau**, which in
these scripts is a paragraph and not a word, so it lands one card per thought; `--min` (2s default)
skips a beat too short to read as emphasis rather than flashing a frame. This is the cheapest cut in
the edit - no clip to build, no graphic to design - and it is what was missing from `ES02`, where
29 of 37 cards carried one identical framing for eleven minutes.

**The bed goes down before the motion, and there is one of it.** A different track per episode reads
as a different channel. Level and ducking are not decisions to make per video either: `music set`
writes 0.211 with ducking on, which is where Descript put a real one, and the scene's own gain stays
at 1 so the slider an editor drags next still tells the truth.


## A tidy-up is one batch, and what it cannot reach

Moved out of SKILL.md on 25 Aug 2026 to hold it under the 250-line ceiling.

### "Can you reorganize this project" is one batch

Write the ops file, `--dry` it, run it. The browser drag route below is the fallback for when the CLI's session has expired and nobody is at the keyboard to sign in again.

`prompt_project_agent` is not the route, for media names or for composition names: it is metered on AI credits and returns `Insufficient AI credits` when they run out, and on a project with entries in `publishes` it is worse than no, having renamed a live composition once already (`references/learned-patterns.md`, 2026-08-01). `pnpm descript rename` renames exactly what it is given and nothing else.

Most of the mess is not the imports. **The API only controls names for media it imports. Everything Descript generates itself lands at the project root with a machine name and no folder**: fonts, AI voice clips, pasted images, screen recordings, Stock Media pulls. On `BATCH 2`, 70 of 109 media items were loose at root while all seven video folders were clean. **An import session also tends to leave loose root items, sometimes one per file** - 23 files once added 23 bare UUIDs, a single file added none - so the only honest number is a `get_project` diff around your own call. The named entry is what shows in the folder and what an editor drags; the UUID is the underlying asset.

So do not sell a tidy-up as a fix. Hand over instead: **four bucket folders, underscore-prefixed** so they sort above the video folders (`_fonts`, `_ai-audio`, `_stills`, `_recordings`, and a wrong bucket name costs nothing since folders stay renamable); **sort the media browser by Type first**, which makes each bucket one contiguous run and the job four shift-click drags rather than seventy; and **say plainly that it recurs**, the cheap moment to sweep being when a batch closes, not when it has grown to seventy.


## Why the five passes cannot be reordered

Moved out of SKILL.md on 25 Aug 2026 to hold it under the 250-line ceiling.

| # | Pass | What runs | Why it cannot move |
| --- | --- | --- | --- |
| 1 | **Cut** | `descript-script-edit` | Everything downstream is timed against the cut. A timecode taken from the raw take is not offset, it is meaningless. |
| 2 | **Layouts** | `pnpm descript layout apply` | Layouts decide what the frame holds - camera, screen, both, a title. Until the frame is decided, nobody knows which beats still need a picture. |
| 3 | **Music** | `pnpm descript music set` | The bed sets the pace the motion is cut to. Building motion first means timing it against silence and re-timing it after. |
| 4 | **Motion** | `motion-design`, then `import` into `Motion/` | Built to the clock the first three passes fixed. |
| 5 | **B-roll** | `broll-research` sourcing, then `import` into `B-roll/` | Borrowed picture, last, because it fills what motion did not earn. |


## The refusal clause, and verifying an agent run

Moved out of SKILL.md on 25 Aug 2026 to hold it under the 250-line ceiling.

Every agent prompt that mutates anything must end with an explicit refusal clause:

> If you really cannot do X, do not do anything else as a substitute. State plainly which tool or capability is missing.

Then verify with `get_project` rather than trusting `agent_response`. Check the `compositions` array against what it claimed.

Compositions with an entry in `publishes` are live URLs. Renaming one changes what viewers see. Leave them alone unless asked.
