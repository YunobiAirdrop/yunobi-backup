# The nine-step workflow

### 1. Find the concept

The take names its video by title and nothing else, so start from the title.

```bash
KEY=$(grep '^UPSYS_APP_API_KEY=' app/.env.local | cut -d= -f2-)
curl -s -H "Authorization: Bearer $KEY" http://localhost:3160/api/youtube/concepts \
  | jq '.data.concepts[] | select(.title | test("Agency Master"; "i"))'
```

The dev server talks to the production database, so this reads the real concept.
It has to be up; never start or stop it, ask. If no concept matches the Descript
project name, **stop and ask which one it is.** Reviewing a take against the
wrong plan produces confident nonsense.

### 2. Read the plan

```bash
curl -s -H "Authorization: Bearer $KEY" \
  "http://localhost:3160/api/youtube/concepts/<id>/script" | jq .data
```

`GET` reads, `POST` regenerates. **Never POST here.** The plan is the thing being
measured against, and a review that rewrites its own baseline measures nothing.
A concept with no script yet answers 404: that is a finding in its own right
("recorded with nothing written"), not an error to work around.

The script arrives as the eight blocks from `video-script`: `name`, `startsAt`,
`onScreen`, `spoken`, `endsOn`, plus `ask` and `claimsToVerify`.

### 3. Read the raw take

Descript, raw, before anything is ignored:

```
pnpm descript comps <project>                -> composition id and duration
pnpm descript script <project> <comp> --full -> the raw transcript, cuts included
```

If the composition has already been cut, say so in the report and measure what
survives. The recording-habit numbers are then a floor, not a measurement.

### 4. Measure it

```bash
python3 scripts/take-stats.py transcript.txt --duration 1767 > stats.json
python3 ../video-script/scripts/story_metrics.py transcript.txt --duration 1767 --grade
```

`take-stats.py` returns words, pace, runtime against the 3,600-4,200 word budget, the retake and
truncation count with the seconds they cost, filler density, and the five paragraphs where
restarts cluster. `story_metrics.py --grade` returns the seven story rules behind check D10 and
score W10, detailed in `doctrine-checks.md`. Every number in the report comes from one of those
two scripts or the API. **No number in the report is estimated.**

### 5. Align plan to take

Walk the planned blocks in order and mark each one against the transcript:
`delivered`, `dropped`, `added`, `reordered`, `thinned`. Match on the beats in
`spoken`, not on wording, the wording is expected to change.

An added block is not a fault. A dropped one is only a fault if something else in
the video depended on it, which the checks decide.

**Count the verdicts before you write any of them down.** If more than half the
planned blocks come back dropped or reordered, the plan and the take are not the
same video and per-block faults stop meaning anything, nine rows saying "dropped"
is one finding wearing nine hats. Say the divergence once, at the top, and keep the
block table as a record rather than as a charge sheet. Then check the plan itself:
a script under the 3,600-word floor is why the take had to improvise, and that is a
fault in the plan, not in the delivery.

### 6. Run the checks

[`checks.md`](checks.md) holds them, in two families: doctrine checks from `video-script` and
`video-script`, and strategy checks from the competitor dossiers, plus the pass/fail/n/a and
source-required contract both share.

### 7. Score the writing

Ten lines, one point each, scored straight off the checks just run so the total can never
disagree with the table under it. The rubric, the evidence-per-line rule, and what is excluded
because the edit removes it (restarts, truncations, filler, pace) are in
[`checks.md`](checks.md), "The writing score, out of 10".

### 8. Write the ledger row

One ledger file outside the skill, one row per recording, appended:

```json
{"date":"2026-08-19","title":"...","conceptId":"...","compositionId":"...",
 "writingScore":3.0,"priorWritingScore":null,
 "oneThing":"...","priorOneThing":"...","priorFixed":true,"stats":{...}}
```

The `priorFixed` field is the whole point of keeping a ledger. Before writing the
row, read the previous one and test its `oneThing` against **this** take's stats.
The report opens with that verdict, because "the thing I told you last time" is
the only claim in the document that has already been tested.

### 9. Render and open

```bash
python3 scripts/report.py findings.json -o ~/Desktop/reviews/video-coach-<slug>.html
open "file://$HOME/Desktop/reviews/video-coach-<slug>.html"
```

Self-contained HTML on disk, opened in a browser. Never an Artifact, never a terminal
dump, the block-by-block table is unreadable in a terminal and this is meant to
be looked at.
