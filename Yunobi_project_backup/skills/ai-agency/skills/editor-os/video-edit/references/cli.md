# The CLI: credentials, the write model, and what it refuses

Read this before any write bigger than a rename, and the moment the CLI says a credential is not set.

## The credentials, and the message that looks like a logged-out session

`pnpm descript` reads `DESCRIPT_STYTCH_SESSION` and `DESCRIPT_API_TOKEN` off the process
environment and loads no `.env` itself. Both live in `CLIs/.env` and both are valid, so
*"DESCRIPT_STYTCH_SESSION is not set"* reads exactly like a logged-out session and is not one. Run
the whoami before writing that anything is signed out.

```sh
export DESCRIPT_STYTCH_SESSION="$(grep '^DESCRIPT_STYTCH_SESSION=' CLIs/.env | cut -d= -f2-)"
export DESCRIPT_API_TOKEN="$(grep '^DESCRIPT_API_TOKEN=' CLIs/.env | cut -d= -f2-)"
npx tsx CLIs/descript/cli.ts            # whoami: the user and the drives
```

`STYTCH_SESSION` is the app's session and does everything inside a project. `API_TOKEN` is the
public API token and is needed only by `project new` and `import`, because creating a project and
uploading bytes are the two things the app's own API refuses (`POST /v2/projects` answers
`Classic project creation no longer supported`).

`auth capture` refreshes an expired cookie from a `web.descript.com` tab in Orca; pass `--page`
only when several are open. **Anyone else connects with `pnpm descript connect`**, which opens the
walkthrough page, takes both values on the prompt and verifies them with a real call, because a
cookie copied with a stray quote writes just as well as a good one and fails on the next command.
Never take either value as a flag: a flag lands in the shell history and in the process list.

## How the write works

The app does not use the published API. It writes `/v2/projects/{id}/collab/commits`, where a
project is a trimerge-sync document and every edit is one commit carrying a jsondiffpatch delta.
Media names live at `mediaLibrary.mediaRefs[].displayName`, the folder trees at
`rootMediaFileFolder` and `rootCompositionFolder`, the editor tabs at `compositions[]`.

**A storyboard project stores one JSON document per revision instead.** A layout pack, and anything
else with `is_storyboard_enabled`, is read and written that way. **The project record's
`is_storyboard_enabled` says which surface a project keeps, never an empty `collab/commits`**: a
pack can hold a commit chain as well, the app never reads it, and a CLI that routes on the commit
count writes every edit into a document only the CLI replays. `Brand Layouts` carried 102 such
commits under an editor that showed none of them, 9 Sep 2026. `tree` prints the surface it read as
`document: revision N` or `document: N commits`. Reading a storyboard document needs
`GET /v2/projects/{id}/asset_url?url=<the revision's unsigned content_url>`, which answers a
CloudFront URL signed for three hours; the revision's own `content_url` is unsigned and S3 answers
AccessDenied. Writing it is a presigned PUT of the whole document then
`POST /v2/projects/{id}/revisions?content_format_version=2`. `head` and `commit` route both kinds,
so every verb works on a pack unchanged. Two things to hold: `base_revision_id` is enforced with a
409 rather than merged, so an open browser tab on the same project beats you, and **publishing a
pack is a separate route**, `POST /v2/projects/{id}/templates/publish`, without which every rename
stays invisible to every other project.

**The live-editor guard counts the CLI's own last commit**, not only a person's, and it holds for
five minutes: a second verb run inside that window is refused quoting the first one back. It clears
on the cached tip ref, so anything that moves the tip in between - a transcription landing, `verify`
opening the tab - re-arms it. Pass `--anyway` rather than waiting it out, once the app is known shut.

**Never do route discovery inside a project that matters, and never press undo in someone's
editor.** `is_live_collab_enabled` is false on these projects, so two open sessions race and the
last save wins. Duplicate the project and drive the copy, check the collaborator avatars in the top
bar first, make the smallest edit, and delete exactly what you typed rather than undoing it.
`File > Version history` keeps every autosave, which is the only reason one bad restore was
recoverable.

## What a new composition is, and what `dup` copies

A project created through the public API arrives holding exactly one composition, and that is the
template `new` writes: two taus (five seconds whose text is a zero-width space, then a terminal
one), one card boundary anchored to the first tau, and the constant id `temp:vo-meta-track`. `dup`
regenerates every id the composition owns and keeps every `mediaRefId`, so the copy is a second cut
of the same footage with no dangling media.

**That template carries no `videoMetadata` and `isVideo` false, so the composition is an AUDIO one
until it is told otherwise**: it renders audio-only and the layout picker, which gates a card on the
frame size, offers it nothing. Dropping video into it implies neither, so `resize <comp> 2160x3840`
and `comp type <comp> video` both have to follow (A19, 18 Sep 2026).

Composition folders are the same tree shape as media folders: `mkdir --comps`, `mv`, `rmdir --comps`.

The app calls a composition a **track** in its action types and a **scene** in
`published_projects.source_scene_id`. Only the document's name is the one to write.

## A tidy-up is one batch

`pnpm descript batch <project> ops.json` takes an array of `rename` (`item`, `name`), `mv` (`item`,
`folder`, optional `index`), `mkdir`, `rmdir`, `newcomp`, `dup` and `rm` ops, resolves each against
the document as the ops before it left it, and writes **one** commit. Eleven media into three
folders, six compositions into two, one duplicate and one new composition was 21 ops and one
commit. `--dry` prints the resolved plan.

**Most of the mess is not the imports.** The API only controls names for media it imports;
everything Descript generates itself lands at the project root with a machine name and no folder -
fonts, AI voice clips, pasted images, screen recordings, Stock Media pulls. On one project 70 of
109 media items were loose at root while all seven video folders were clean. So do not sell a
tidy-up as a fix: hand over four underscore-prefixed bucket folders (`_fonts`, `_ai-audio`,
`_stills`, `_recordings`) so they sort above the video folders, say that sorting the browser by
Type makes each bucket one contiguous run and the job four shift-click drags, and say plainly that
it recurs - the cheap moment to sweep is when a batch closes.

## Importing bytes

`pnpm descript import <project> <manifest.json>` runs the whole flow: job, uploads, poll. The
declared `file_size` must match the file exactly and signed URLs last three hours.

- **Three media per call through the MCP, not through the API.** The MCP answers `Query count
  exceeded limit of 100` above three; a direct `POST /jobs/import/project_media` took nine
  direct-upload items in one call. The CLI batches for you.
- **One job at a time per project.** A second import while one runs is rejected outright, not
  queued.
- **Direct upload beats URL import**, which validates server-side and rejects anything answering
  with HTML, including CDNs that serve the file perfectly to `curl`.
- **Timeline export to EDL, AAF, FCPXML or Resolve XML is MCP-only.** `export_timeline`,
  `list_folders`, `get_drive_info` and `import_drive_media` answer to no endpoint in the public
  spec, so losing the connector loses those whatever the token can do.
- A failed import leaves an asset record with `artifacts: []`, and enough of them make `publish`
  refuse: `GET .../media_assets?include_artifacts=true` finds them, `DELETE .../{guid}` removes them.

## `have not finished uploading` is an unregistered asset

A publish precheck resolves every `mediaLibrary.mediaRefs[].assetGuid` against the project's own
`GET /v2/projects/{id}/media_assets`. A clip adopted into the cut but never shared into the project
fails that lookup, and the render refuses with a sentence about uploads that names nothing. EA20
carried three (`Glitch.mov` and two stock whooshes) and refused six renders across 4K, 1080p and
720p, through `publish` and the MCP alike.

Diagnose it as a set difference against a project that DOES render, never off the assets alone:
EC49 renders carrying 172 artifacts at `status: failed`, so a failed artifact is not the signal.
The repair is `descript adopt <media> --from <the project that holds it>`, which answers
`assetShared: true`; the render runs on the next attempt. A local export is not the answer: it hides
the broken reference and can refuse the same clip.

## If an agent has to do it after all

`prompt_project_agent` will do *something* adjacent when it cannot do what was asked and report
success: on 2026-08-01 it renamed tracks inside a live published composition instead of the media
it was asked about. Every mutating prompt ends with a refusal clause - *"If you really cannot do X,
do not do anything else as a substitute. State plainly which tool or capability is missing"* - and
the run is verified with `get_project`, never with `agent_response`. It is metered on AI credits,
and **a top-up is the user's call, never yours**.

Compositions with an entry in `publishes` are live URLs. Renaming one changes what viewers see.
