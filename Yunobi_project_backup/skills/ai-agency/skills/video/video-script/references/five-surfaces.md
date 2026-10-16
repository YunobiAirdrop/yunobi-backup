# One video, five surfaces

## Contents

- The run, end to end
- Three things that go wrong here

A long-form video is not finished when the script is. It is finished when a person who has never
read this conversation can open the board, find the video, read the brief, open the script and open
the Descript project. Five surfaces, and every one of them is written in the same session as the
script.

| Surface | What it holds | How it is written |
| --- | --- | --- |
| The concept, in the app | The brief, the keyword evidence, the packaging, **and the script** | `POST /api/youtube/concepts`, then `PUT .../script` |
| The ClickUp task | Production state, dates, who holds it, the batch | `POST /api/youtube/concepts/<id>/production-task` |
| The board fields | Publishing, Format, Socials, BATCH, Points, Descript | `cu task field set` |
| The Descript project | The take, once it exists | `pnpm descript project new` |
| The calendar | The calendar row, so the schedule reads true | edited by hand |

**The script's home is the concept**, at `/youtube/concepts`, as `metadata.script`. That is the copy
that gets rewritten, reviewed, teleprompted and recorded from. A script that lives in a repo file or
in a chat window does not exist.

**A hand-written script gets there with `PUT`, not by being regenerated.** `POST` spends a model call
and returns a plan, so a script drafted anywhere else could never reach its own home and lived twice.
`PUT` on the same route stores a finished script, validated against `videoScriptSchema` and nothing
else. Two fields it needs: `beatCount` drives the runtime the recording page shows, so it is the real
bullet count including the cold open and the ask, and `startsAt` on each block is cumulative beats
times `BEAT_SECONDS` rather than a guess.

**A concept born outside the SEO flow passes `source`.** `reportId`, `seed` and `keyword` are
nullable, but a zod `.nullable().default(null)` still refuses an absent key on this route, so send
`"reportId": null` and `"seed": null` explicitly rather than omitting them. Pass `source` so the SEO
flow stays distinguishable from a competitor teardown.

### The run, end to end

```bash
KEY=$(grep -E '^UPSYS_APP_API_KEY=' app/.env.local | cut -d= -f2- | tr -d '"')
API=http://localhost:3160          # prod refuses anything the last deploy does not carry

# 1. the concept, which is the brief and the keyword evidence
curl -sS -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' \
  -X POST "$API/api/youtube/concepts" --data-binary @concept.json      # -> id

# 2. the script, already written, never regenerated
curl -sS -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' \
  -X PUT "$API/api/youtube/concepts/<id>/script" --data-binary @script.json

# 3. the board task, which also writes the concept URL into `Link`
curl -sS -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' \
  -X POST "$API/api/youtube/concepts/<id>/production-task" -d '{}'     # -> taskId

# 4. the name carries the code, and the fields carry the schedule
cu task update <taskId> --name "EC52 - <title>" --description "$(cat brief.md)" --markdown \
  --due-date 2026-12-09
cu task field set <taskId> --field 663d0445-3420-4152-bacb-e11a8145d859 --value 2026-12-09 --all-day
cu task field set <taskId> --field d508e762-2df9-4d4d-9640-4e260b602a18 --value 6      # Format: Video
cu task field set <taskId> --field af2f2fb5-cc3f-4918-b4ca-9f5e31c16acc --value 3      # BATCH: Later
cu task field set <taskId> --field 43369afa-4a38-4c40-ba5a-9392fb5ea25f --value 1      # Points: 2
cu task field set <taskId> --field d8574a56-d8c0-4ab0-bb47-8343cc9dbf78 \
  --value '["bd92c09f-45eb-4d69-a6e7-8b6b0fe9b6a2"]' --json-value                      # Socials: YouTube

# 5. the Descript project, before the shoot, so the field is never empty
cd ../vibe-kit/CLIs
pnpm descript project new "EC52 - <title>"
pnpm descript project mv <projectId> "01 - Youtube HeyRamzi/00 - In Production"
pnpm descript rename <projectId> <compId> "<title>"      # the composition is the title ALONE
cd -
cu task field set <taskId> --field 632095f8-6949-40f7-88dc-7737203ab5c0 \
  --value "https://web.descript.com/<projectId>"

# 6. relink, so `productionTask.name` matches the renamed board task rather than the old title
curl -sS -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' \
  -X POST "$API/api/youtube/concepts/<id>/production-task" -d '{"taskId":"<taskId>"}'
```

**Then the calendar row**, plus one short note saying why the video earned its slot and what
moved to make room.
 ClickUp wins whenever the two
disagree, so the row is written after the board, never before it.

**`cu task field set` on a `labels` field needs a JSON array of option ids**, and the ids are not in
`cu fields list`. Read them from `GET /list/<id>/field` on the ClickUp API with the token in
`~/.config/clickup/`. Passing the plain label answers `Value must be an array`.

### Three things that go wrong here

**The dev server is the writer, not prod.** `localhost:3160` runs the working tree and talks to the
**prod** database, so a route added this week works there and 400s against the deployed app
until the next deploy. Check it with `curl -o /dev/null -w '%{http_code}' http://localhost:3160/`
and ask the owner to start it if it is down. Never start it yourself.

**One name across all five surfaces.** The ClickUp task is `CODE - Title`. The Descript project is
`CODE - Title`. The Descript composition is the title **alone**. The concept is the title alone. A
project left holding the name Descript generated at import is the failure this prevents, and it hit
all seven videos in flight on 26 Aug 2026.

**The code is assigned off the whole registry, never by eye.** `[Language][Pillar][NN]`, pillar
letters SCALPM. Enumerate every existing code including closed tasks
(`cu tasks --list 901507318169 --closed --json`) and take the next free number in that pillar. `NN`
is an id, not a running order, and a gap is never closed by renumbering. Three live collisions were
made without this step.

The doctrine that governs how a script is written lives here, in this skill. A generator in the
app is a runtime copy of it and says so in its header:
**change one and change the other in the same session.** On 19 Aug 2026 they had already drifted,
`script-contracts.ts` requiring prose ("Not bullet points") while this skill required bullets.

The course lesson files are the
**curriculum record**, not a second script: module, surface, status, runtime, takeaways, recording
notes. A lesson that is also a YouTube video keeps its spoken beats in one of the two places and the
other one links to it. Never both.
