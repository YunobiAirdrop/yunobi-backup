# Upload, and the calendar it drives

Both destinations every time: Drive is the library, ClickUp is the working record.
Every id, endpoint and failure mode behind that sentence is here, because each one
was learned by a upload that looked like it worked and did not.

Both destinations, every time. Drive is the library, ClickUp is the working record.

**Google Drive.** The `video` shared drive, `shorts/` folder.

| Thing | ID |
| --- | --- |
| Shared drive `video` | `0AIe50-YT-JzDUk9PVA` |
| `shorts/` folder | `1W91uGpPHsXdFkBSEUXCcd-rqVN84URaL` |

`gws drive +upload` cannot write to a shared drive: it does not send `supportsAllDrives` and returns `404 File not found` on a parent that plainly exists. Use the raw endpoint.

```bash
gws drive files create --upload OUT-master.mp4 --upload-content-type video/mp4 \
  --params '{"supportsAllDrives":true,"fields":"id,name,size,webViewLink"}' \
  --json '{"name":"OUT-master.mp4","parents":["1W91uGpPHsXdFkBSEUXCcd-rqVN84URaL"]}'
```

Upload the `.srt` alongside it. It costs nothing and it is what a re-cut or a translation starts from.

**ClickUp.** The Socials list in your own workspace.

**Attach the file, then call it out in a comment. Never a bare attachment.** This is the same rule
`social-scheduling` states as "an attachment arrives with what it is about, never bare" (set
26 Aug 2026) and that the deck host already implements for decks; it applies to a Short's
preview and `.srt` exactly the same way. Restated here 30 Aug 2026 after a run attached both bare.

```bash
cu task create --list 901507318162 --name "S01 - <title>" \
  --description-file desc.md --markdown --tag shorts --due-date YYYY-MM-DD
cu task attach <taskId> --file OUT-preview.mp4     # NOT the master
cu task attach <taskId> --file OUT.srt
```

The comment can sit beside the files, which is what `slides:host` does, or **carry them inside it**,
which reads better on a task somebody opens a month later. The embedded form is an `attachment`
segment in a v2 comment body, keyed by the id `cu task attachments <taskId>` prints **with its
extension** (`55423cfe-….mp4`), not the bare uuid:

```json
{"comment":[
  {"text":"Finished cut. Preview and captions.\n"},
  {"type":"attachment","attachment":{"id":"<attachmentId>.mp4"}},
  {"text":"\n"},
  {"type":"attachment","attachment":{"id":"<attachmentId>.srt"}},
  {"text":"\n"}
],"notify_all":false}
```

`cu comments list <taskId> --blocks` is the only view that shows a comment's files. **Do not go
looking for a comment-scoped upload endpoint**: `/v3/workspaces/{ws}/comment/{id}/attachments`
answers `Invalid path param for entityType: comment`, the plural 404s, and so does v2
`/comment/{id}/attachment`. The upload is always task-scoped; only the anchoring is a comment.

**ClickUp gets a preview, never the master.** A 155 MB master fails with
`ClickUp API error (500): context deadline exceeded` and no partial attachment, which reads as a
server fault rather than the size limit it is. Every short on the board carries a 9 to 12 MB preview.
Build it off the master and keep the master for Drive:

```bash
ffmpeg -i OUT-master.mp4 -map 0:v:0 -map 0:a:0 -vf scale=720:1280 \
  -c:v libx264 -crf 26 -preset veryfast -c:a aac -b:a 96k -movflags +faststart OUT-preview.mp4
```

This is not the no-re-encode rule being broken: the preview is a second
artefact for a human to glance at, and the master still ships untouched.

**Get the filename right before the upload, because ClickUp cannot fix it afterwards.** There is
no rename and no delete for an attachment on the public API: `DELETE /api/v2/attachment/<id>`
answers a bare `404 page not found`, and `cu` has no command for either. A file uploaded under the
wrong code stays on the task forever. Two were found on 24 Aug 2026: the C13 task carried
`C12-managing-wrong-4space-preview.mp4`, and the S01 task carried `T01-gsc-social-master.mp4` on a
prefix the taxonomy retired. Both were corrected in the Drive library, which does rename, and both
wrong names are still on their tasks.

**A missing attachment is recoverable, because Buffer keeps the video.** Every Short posted through
Buffer carries its file on the post: read `items.assets.source` off `posts list` and download it,
then build the preview from that. Prefer the `buffer-updates-media-backfill-bucket.s3.amazonaws.com`
copy over your own self-hosted one: that volume is purged periodically and a
purged path answers **`200` with an HTML "Not Found" page**, so `curl` writes a 6.9 KB file named
`.mp4` and reports success. Check the size before trusting a download. Nine published Shorts were
recovered this way on 24 Aug 2026; only the three published outside Buffer (L07, L09, M10) have no
file anywhere.

Tag is exactly `shorts`, lowercase, on every short. The MARKETING space also carries `to-optimize`, `youtube`, `📛 urgent`, `🇺🇸 en` and `🇫🇷 fr`; no short uses the language tags today, so adding one breaks the convention rather than improving it.

**The calendar is driven by a `Publishing` date custom field, not by the due date.** This file said "the due date is the publish date" until 7 Aug 2026 and that was wrong: the Socials calendar view reads `Publishing` (`663d0445-3420-4152-bacb-e11a8145d859`), so a task whose due date moved and whose `Publishing` field did not stays exactly where it was on the board. Set both, and set them to the same day.

`cu` cannot write custom fields. Use the REST endpoint, and stamp noon UTC so no timezone rolls the date back a day. **The token is not exported**: `$CLICKUP_API_TOKEN_UPSYS` is empty in a fresh shell. It lives in `app/.env.local`, and the same value is `apiToken` in `~/.config/clickup/config.json`, which is where `cu` itself reads it and the shorter path from any directory.

```bash
CU=$(python3 -c "import json;print(json.load(open('$HOME/.config/clickup/config.json'))['apiToken'])")
curl -X POST -H "Authorization: $CU" -H "Content-Type: application/json" \
  -d '{"value":'"$(python3 -c 'import datetime;print(int(datetime.datetime(2026,8,8,12,tzinfo=datetime.timezone.utc).timestamp()*1000))')"'}' \
  https://api.clickup.com/api/v2/task/<taskId>/field/663d0445-3420-4152-bacb-e11a8145d859
```

The other fields on the list, read 7 Aug 2026: `📦 BATCH` `af2f2fb5-...` (Previous / This Week / Next Week / Later / Maybe), `Format` `d508e762-...` (Short 📹 is `367afda7-fb68-4e86-b9fe-eab1e4412f01`), `Socials` `d8574a56-...` (a labels field, set with `{"add":[...]}`), `🔢 Points` `43369afa-...`. A new short needs all of them or it renders blank on the board.

**Where `Publishing` and Buffer disagree, Buffer wins and the field gets corrected. One command
does it, so never correct a date by hand:**

```bash
python3 .claude/skills/social-scheduling/references/reconcile.py --dry-run   # what would change
python3 .claude/skills/social-scheduling/references/reconcile.py            # correct ClickUp
```

Its `publishing` stage reads Buffer, then writes the `Publishing` field, the due date and a
published status back onto the coded task. The true date is the earliest **video** post for the
code (TikTok, Instagram, YouTube) in Lisbon time: the LinkedIn and X posts carrying the same topic
are repurposes that trail it by days and must never move the Shorts calendar.

Nothing read this back until 24 Aug 2026 and the board had drifted by up to twenty days. A05
published on 11 Aug still sat on the calendar as open work for 31 Aug, A07 published on 18 Aug read
7 Sep, and S02 published on 19 Aug carried no `Publishing` date at all. The date came from whatever
the batch plan said the day it was written, and no reschedule made in Buffer ever came home. This
is the same fault found on 7 Aug 2026 in M05, fixed by hand then and back within two weeks, which is
why reading the queue is no longer good enough: the walk has to write.

Run it after any scheduling session, and before writing the calendar back.

Posting days are Monday, Tuesday, Thursday, Friday, **Saturday and Sunday** (set 7 Aug 2026); Wednesday belongs to the long-form. The two weekend slots take unscripted, clip-harvest and personal material only, so the scripted batch stays at four a week. Weekend register is `L` and `M`. Off-batch posts take the next free posting day, and news takes the earliest one available because it decays. Your own calendar doctrine wins over this paragraph.

