# Reading the SERP

The measurement that says whether a subject is worth a recording day. It runs before the hook, and
`idea-mining` has already chosen what the piece is about. One read, and it is free.

## The two passes

`yt-dlp` on the exact phrase a buyer types, then a second pass for the counts, because
`--flat-playlist` returns `NA` for them:

```bash
yt-dlp --flat-playlist --skip-download "ytsearch20:<phrase>" --print "%(id)s" > ids.txt
yt-dlp --skip-download --no-warnings -a ids.txt \
  --print "%(view_count)s|%(duration)s|%(upload_date)s|%(channel)s|%(title)s"
```

**Pull the date and the runtime with the count, and read all four.** The count alone answers the
wrong question. What decides the lane is who holds it, how old they are, and how the last twelve
months did against them.

## Two conditions open a lane, not one

- **The unserved query.** A first page of 2-to-5-minute clips under 150 views each. Nobody has
  answered it and the SERP says so.
- **The stale head.** The commoner case on a commercial phrase, and the one the original rule
  missed: two or three videos well clear of the rest, all of them a year or more old, and every
  entrant since under a thousand. A stale head is a lane a current video can take, and the tail is
  the proof that nobody has tried properly.

Measured 9 Sep 2026 on `airtable to google sheets`: 28,804 views on a 2:37 clip from October 2025
and 27,757 on a 12:06 tutorial from December 2022, then a tail of 927, 768, 740, 612, 542, 444,
364, 354, 278, 238, 178, 152, 101, 31, 26.

## Never take the runtime off the SERP

The thin clips crowding a commercial phrase are the ones losing, so matching their length copies
the loser. The band in [`three-run-control.md`](three-run-control.md) governs whatever the SERP
looks like. Satisfy the searcher's intent inside the first two minutes, then earn the rest. On the
read above, the 12-minute video outranks nine 2-minute ones published after it.

## A product demo reads two SERPs

The YouTube one decides the video. The product's own Search Console rows decide whether the video
is worth a recording day at all, because a video that ranks is off-site presence on a phrase the
site already competes for. Pull them with the `seo` skill, and say which page owns the
phrase before writing a title that fights it.

## Demand is not measurable, so do not fake it

`yt-dlp` returns no search volume and no competition score, and the app's
`POST /api/youtube/keyword-research` is quarantined by the fabrication finding below. Decide on the
SERP, and say in one line that volume was not measured.

Worked example, 28 Aug 2026, EC52. `clickup pricing` measured as a middling keyword on the volume
instrument of the day, and the SERP returned 11, 7, 27, 118 and 16 views on its top five. **The
SERP read is what made it a video, and the volume row would not have stopped it either way**, which
is the reason losing the volume instrument costs less here than it looks.

**A fallback that invents its own data is worse than an outage.** The app's keyword report answered
four different seeds with an identical estimated volume of 140 and seven templated ideas while
looking exactly like a measurement, and a title was chosen off it on 26 Aug 2026. Any keyword row
repeating across unrelated seeds is a fallback, not a reading.
