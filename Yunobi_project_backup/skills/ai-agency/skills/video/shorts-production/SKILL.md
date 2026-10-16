---
name: shorts-production
description: "Takes a finished short-form recording to a scheduled, coded, attached ClickUp task, with the export on Google Drive. Covers the SCALPM pillar codes, the rule that exports ship as they are and are never re-encoded, and the calendar write-back. Use when a Short has just been recorded, when a recording needs uploading, or when a Short needs coding and scheduling in the Socials calendar."
tags: [drives, video, clickup]
---

# Shorts Production

This skill starts where the camera stops. It does not write scripts and it does not write hooks.

- Hooks and script openings: `video-hooks`.
- Turning long-form into posts: `generate-social`.
- Getting the finished master out to the networks: `social-scheduling`. This skill ends at the ClickUp task; that one takes it from there.
- Strategy, cadence, pillar shares, CTA rules: your own marketing doctrine. Whatever holds it is the single source of truth and it wins over anything restated here.

## Know what a Short is worth before making more of them

Shorts are a distribution surface, not an engine: on the nearest positioning twin
they account for 7% of lifetime views, and volume did not rescue the ratio. A
Short is a clip that feeds the surfaces that do work (on our own numbers,
LinkedIn), so a batch of Shorts is not a growth plan by itself, and hours are
better spent on the long video and its title than on Short number twenty-five.
Full numbers in `vibe-kit/ai-doc/references/competitor-evidence.md`.

## Read what the feed rewards this month, before drafting

`social-engagement` derives it from competitor posts it collects itself, scored against each
account's own median so a 22,000-like account and a 21-like account contribute the same evidence:
`social-engagement`, `references/what-works.md`. It carries
its measurement date and a staleness ladder, because a feed re-ranks every month and a file does
not. Over 30 days old, collect the feed again before trusting the page.

It says what the feed rewards, never what is good. The bans in `@heyramzi/lint` and the voice in
`voice-dna` outrank every number on that page.

## The rule that ranks above the rest

**ClickUp is the calendar. The document follows it.**

The doctrine says so explicitly: when the doc and ClickUp disagree, ClickUp wins and the table gets rewritten to match, never the reverse. So schedule in ClickUp first, then write the doc back. Never the other way round, and never only one of the two.

## Read the recording before deciding anything about it

Do not ask what the video is about, and do not guess from the filename. Filenames are working titles and they carry codes that may not exist in the taxonomy.

**Captioned exports usually carry a subtitle track, which is a free transcript.**

```bash
ffprobe -v error -show_entries stream=index,codec_type,codec_name -of compact IN.mp4
ffmpeg -v error -i IN.mp4 -map 0:s:0 -c:s srt subs.srt   # if a subtitle stream exists
```

No subtitle track means transcribe, and **the transcriber on this machine is parakeet, not
whisper**. It is already installed as a uv tool, the model is already cached, and it needs no
download:

```bash
parakeet-mlx --output-format srt --output-dir . IN.mp4   # txt, srt, vtt, json, or all
```

**It reads the mp4 directly, so there is no ffmpeg step**, and the SRT comes back with timestamps.
It auto-detects the language and carries word-level timestamps with `--highlight-words`, so it
covers the caption and the matching cases both. Verified 28 Aug 2026: a 36-second clip in 6 seconds
on `parakeet-tdt-0.6b-v3`, French, straight from the mp4.

**Reaching for `whisper-cli` costs a 150 MB to 1.6 GB model download and gets the language wrong.**
An English `ggml-*.en.bin` on non-English audio does not fail, it hallucinates a fluent English loop
that looks like a transcript, which is a silent wrong answer rather than an error. The one place
whisper is still correct is `dji-sync`, whose solo path is tuned around it.

Then look at the picture, because the transcript cannot tell you whether it is a talking head, a split screen or a screen capture, and it cannot tell you whether captions are burned in. One contact sheet answers all of it, with the timecode burned into every cell:

```bash
python3 .claude/skills/motion-design/scripts/watch.py IN.mp4 --sheet -n 12
```

The same pass is the last check before the export leaves for Drive. Captions over his face, a caption running off the bottom, a burned-in caption on a clip that also ships an `.srt`, a black tail after the last word: all of them survive a clean export and none of them survive a look. Re-cutting is the fix, never a re-encode.

## The script library lives in Apple Notes

Apple Notes is the script store; ClickUp is the production record, and they drift because a Short can
be shot without anyone opening the note. The folder contract (`Batch N`, `Unscripted pool`, `Shot`,
`Archive`), the triage procedure against ClickUp, the rebalance rules and the note shape are all in
[`references/script-library.md`](references/script-library.md). **Read it before moving any note**,
and re-triage whenever a batch is recorded.

## The pillar codes

`[Letter][NN]`. The letter is the pillar, the number is an ID inside it and **never a running order**.

| Code | Pillar | Sells |
| --- | --- | --- |
| **S** | **Skill**: a concrete tactic or tool the viewer can use today | Agency Master, top of funnel |
| **C** | ClickUp: workspace config, agency delivery | Agency Master |
| **A** | AI: Claude, agents, building software without being an engineer | Agency Master |
| **L** | Lifestyle: the founder's week, freelancers, getting out of delivery | Agency Brain, warm |
| **P** | **Product**: Seam and the other things built in public | Product downloads, and proof the software is real |
| **M** | Mindset: personal productivity, calendar, GTD, second brain | The community, and the school later |

S, C, A and M are the 70% core. L and P are the 30%.

**Long-form uses this same table.** As of 20 Aug 2026 the YouTube long-form codes are
`[Language][Pillar][NN]`, where the language is `E` for the English channel and `F`
for the French one, and the pillar letter and the
numbering rule are exactly the ones above. So `EA19` is an English AI video and `FC37`
is a French ClickUp video. A Short keeps the bare `[Letter][NN]`, because a Short has
no language split.

**Two traps from the migration that replaced it still bite**: read the title rather than the old
numeric family, because an AI video coded in a ClickUp family mis-files; and a number is an ID inside
its pillar, so it is **never renumbered to close a gap**, since the gap proves nothing was reused. The
family map, the S and P reassignment, and the open question about this weighting are in
[`references/pillar-codes-history.md`](references/pillar-codes-history.md); the doctrine owns the
pillar shares and wins over any note here.

Numbering: take the next free number inside the letter. Check the live list before assuming a number is free, because the doc lags.

## Two rules that reject work at this stage

Check both before scheduling, and say so out loud when one is breached.

1. **Dated content never goes to Shorts** (decision 10). Shorts is the evergreen home; TikTok and Instagram take the timely material. A video that says "a new update" or "a find of today" is dated even when the underlying feature is durable. This is a judgement call on news about a permanent feature, so flag it and let the owner decide rather than deciding silently.
2. **The congruence rule** (decision 3). Every video is the same subject as the thing sold, one level shallower. A tool tip with no product tie is allowed, but it is a connection-tax post and it should be named as one rather than counted as core content.

## Do not re-encode. Ship the export

**The file the editor exports is the file that ships.** Set 7 Aug 2026, and it replaces a re-encode
recipe that used to live here.

This file used to say the export runs at "roughly seven times what the picture needs" and to
transcode every master to CRF 19 with an SSIM gate at 0.99. The answer: the exports are already
right, and re-encoding them buys nothing, which the gate's own evidence bears out. Of
six masters run through it, four scored a literal `1.000000`, meaning the transcode was measurably
pointless, and the two that "failed" at 0.9810 and 0.9875 failed because the transcode had degraded
them. **The gate was catching damage the gate itself caused.** A step whose best case is no change
and whose worst case is loss is not a quality step.

So: upload the export. Keep the filename discipline (`S01-gsc-social-master.mp4`, code and topic,
never the working title) by copying or renaming, not by transcoding.

**What this costs downstream is now only disk.** Exports run 150 to 420 MB where a transcode landed
at 24 to 62 MB. The upload ceilings that used to bind (a Cloudflare cap at 100 MB, an application
error above ~250 MB, an origin `502` above ~450 MB) were all properties of the retired TryPost HTTP
upload path; media is written into the volume over `scp` now, which has no ceiling. See
`social-scheduling`'s `references/buffer-api.md`. **So re-encoding for size is no longer a permitted
workaround**, and the no-re-encode rule applies without exception.

## The cover is a separate deliverable, and it is where the shares are lost

A vertical cover is not a thumbnail and `youtube-thumbnail` says so in its non-goals: different
aspect, different rules, and it never plays in the feed. It is the still that represents the
video everywhere the video is not playing, and three of those places decide whether a Short does
anything at all.

- **In a direct message.** This is the one nobody designs for and it is where virality actually
  comes from: a Short spreads because people send it to each other, and in a DM it sits as a
  static frame that is not looping. The cover is the only thing that earns the tap. A recipient
  sent five clips opens two, and picks them off the covers.
- **On the profile grid.** Somebody who liked one piece goes to the grid to find more. A grid of
  frames that all say nothing gives them nothing to choose, and the session ends at one.
- **On the Shorts shelf and in search**, where it sits beside a title.

So the cover ships with the master, chosen or built rather than left to whatever frame the
platform grabs. It carries the same words the piece is about, legible at grid size, and it is
different enough from the last five that the grid reads as a set of distinct things rather than
one thing posted repeatedly. `slide-deck` holds the surfaces and the type rules a still like this
is built on.

**A numbered series is the cheapest bingeability there is.** "3 of 10" on the cover makes the
grid a puzzle with pieces missing, and a viewer who liked number three goes looking for one and
two. It works because the pieces are visibly countable, which is also its cost: a series
announced and abandoned is a promise broken in public. **Shoot the whole series before the first
one publishes**, which is the same rule the batch already runs on, and never start one from a
cadence you are currently maintaining rather than one you have already banked.

## Upload

Both destinations, every time. Drive is the library, ClickUp is the working record. **Drive takes
the master** (`gws drive files create` with `supportsAllDrives`, because `gws drive +upload` 404s
on a shared drive) plus the `.srt`. **ClickUp takes a 9-12 MB preview and never the master**, which
fails at 155 MB with a 500 that reads like a server fault. Get the filename right first: ClickUp
has no rename and no delete for an attachment.

The Socials calendar is driven by a `Publishing` date custom field, not by the due date, and where
that field and Buffer disagree Buffer wins — `social-scheduling`'s `reconcile.py` corrects it, and
a date is never corrected by hand. Posting days are Mon, Tue, Thu, Fri, Sat, Sun; Wednesday belongs
to the long-form, and the two weekend slots take unscripted material only.

Every id, endpoint, token path and recovery route: **[references/upload.md](references/upload.md)**.

## What goes in the task description

The task is the production record. Someone opening it three weeks later should not need the video to know what it is.

Topic line with pillar, format, length and record date. Status, plainly: what is shot, what is left. The hook, verbatim. A beat table with seconds. The full transcript as a blockquote. An asset list with the Drive links and where the untouched source sits. Any rule breach, named, with the decision left open if it is the owner's to make. Any follow-up the video promises on camera, because a promised part two is a scheduled post.

## Write the calendar back

Only after ClickUp is correct: update the short-form calendar to match, and add the code to the pillar table if the taxonomy moved. A Short that was recorded without a written script does not need one invented after the fact, but the code and date belong in the calendar either way.

## Verification checklist

- [ ] Content was read from the subtitle track or a transcript, not inferred from the filename
- [ ] A `watch.py --sheet` pass was read: the format is known, captions sit clear of his face and inside the frame, and there is no black tail
- [ ] The pillar letter matches the current table, and the number was checked free against the live list
- [ ] The dated-content rule and the congruence rule were both checked, and any breach was named out loud
- [ ] A cover was chosen or built, reads at grid size, and is distinguishable from the last five
- [ ] Any series number on the cover belongs to a series already shot in full
- [ ] The uploaded file is the export itself, not a transcode of it
- [ ] The master and the `.srt` are both on the Drive `shorts/` folder
- [ ] The ClickUp task exists with the `shorts` tag, a due date on a posting day, and the preview and the `.srt` attached
- [ ] Every attached filename opens with this short's own code, checked before the upload
- [ ] `reconcile.py` was run and reports 0 corrected, so the board matches Buffer
- [ ] the calendar was updated to match ClickUp, after ClickUp
- [ ] Any new failure mode was appended to Learned Patterns

## Learned Patterns


This skill appends new failure modes to its own pattern list after each run.
The pattern list lives in [references/learned-patterns.md](references/learned-patterns.md).
Read it before a run. If this run surfaced a failure mode not already listed, append it
there with today's date before finishing.

The run each line came from, with its quotes and numbers, is in [`references/learned-patterns-archive.md`](references/learned-patterns-archive.md).