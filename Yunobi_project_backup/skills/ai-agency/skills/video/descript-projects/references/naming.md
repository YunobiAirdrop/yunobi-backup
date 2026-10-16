# The clip naming rules

`N [MM-SS] Description.ext`. Moved out of SKILL.md on 25 Aug 2026 to hold it under the
250-line ceiling. The pattern and the example tree stay in the skill; these are the seven
rules that make it work.

Rules that make it work:

- **One digit up to nine, two from ten.** A leading zero pads a number that has nowhere to grow, so a lesson with six clips uses `1`, not `01`. A long video does go past nine: the Glance demo has twelve, and one-digit names sort `1, 10, 11, 12, 2` in the media browser, which is worse than the padding the rule was avoiding. Pick the width once for the whole video and keep it.
- **A letter suffix means alternatives for the same beat.** `2a`, `2b`, `2c` reads as "three options for beat 2", and the editor picks one. A beat with a single option carries no letter.
- **`-` not `:`.** macOS renders `:` in a filename as `/` in Finder. `[04-19]` means 4:19.
- **Zero-pad the timecode to mm-ss** so `[00-09]` sorts above `[01-34]`. That padding is about sorting two-part numbers and is untouched by the rule above.
- **Timecode against the cut, not the raw, whenever a composition already exists.** `export_transcript` with `format: "srt"` on the composition gives the real clock. A raw timecode on a cut take is not merely offset, it is meaningless: the line may have been cut entirely.
- `00 RAW` keeps its two digits and carries no timecode. It is the marker for a raw take, not a beat number, which is why it does not follow the one-digit rule and must not be "fixed" to match.
- On a salvage take kept only for a few lines, put the salvage points in the name instead: `00b ALT 4K [salvage 1-05, 1-13, 3-41].MOV`.


## The three clip folders, and why they are apart

Moved out of SKILL.md on 25 Aug 2026 to hold it under the 250-line ceiling.

**Inside the video's folder there are exactly three clip folders, and the split is by where the picture came from.**

- **`Music`** — the bed, and only the bed. One file. It carries no beat number and no timecode, because it is not a beat: it runs under the whole cut. Keep one house library and record what each track is licensed for.
- **`Motion`** — everything built here, in both of its registers: **flat motion** (opaque, full frame or 960x1080 beside him, `.mp4`) and **alpha motion** (keyed over him, `qtrle` `.mov`). The extension is what separates the two, so the folder needs no further split. Ours outright.
- **`B-roll`** — real video footage: a film beat, a meme, archive, a stock plate, a shot of the actual thing. Usually somebody else's picture, always muted.

Flat motion, alpha motion and B-roll are the three registers, and the playbook that defines them with a worked example of each is the app's `/design/playbooks/b-roll`.

`Music` sorts above the other two, which is also the order the passes run in.

They are apart for a reason that has nothing to do with tidiness. A borrowed shot **cannot ship in a paid lesson, a client deliverable or an ad**, and a drawn one ships anywhere. Mixed into one folder, an unshippable frame sits one drag away from a paid build and nothing on screen says which is which. The `broll-research` skill keeps the rights ledger (`sources.json`) and gates a build on it; this folder is the same rule made visible in the media browser. Where the borrowed lane comes from, how a window is pulled and what the licence rules are: the `broll-research` skill.

A single-video project has no per-video folder to nest in, so `Motion` and `B-roll` sit at its root next to the raw takes.


## Naming a recording session's raw takes

Moved out of SKILL.md on 25 Aug 2026 to hold it under the 250-line ceiling.

The naming that came out of it, one folder per session, slug-cased like the folders already there:

```
you-only-need-five-spaces/
  00 RAW CAM  You Only Need Five Spaces.MOV     4K camera
  00 RAW IPAD You Only Need Five Spaces.MP4     iPad screen recording
  00 RAW MIC  You Only Need Five Spaces.wav     the web-recorder take
```

Everything raw is `00`, which leaves `01` upward to the b-roll convention, and the three sort camera, iPad, mic. Sequences get `SEQ <code> · <Title>` so the Sequences folder reads as the batch.

Getting the name right at import is still worth doing, because one call beats two. But a wrong name is now a one-line fix, not a manual pass, and re-importing to fix a name was never the answer anyway: it duplicates the media and the original stays wired into any composition using it.

## The two shapes, drawn out

One folder per video, holding that video's raw take and its three clip folders together. `Music`
carries the bed and takes no beat number; `Motion` is built here and is ours outright; `B-roll` is
borrowed picture, kept apart because a borrowed shot cannot ship in a paid lesson.

```
second-brain/
  00 RAW Second Brain.MOV
  Music/
    Bed · Understated Drive.mp3
  Motion/
    1 [00-28] Notes App.mp4
    2 [01-04] Typing A To-Do List.mp4
  B-roll/
    1 [02-11] Printer Rage.mp4
```

A single-video project keeps the three at its root, and the beat number with its letter suffix sorts
the browser into edit order, so the media browser is the shot list:

```
clickup-terminology/
  00 RAW ClickUp Terminology.MOV
  1 [00-00] Hierarchy Overview Diagram.jpg
  2a [00-09] Workspace.png
  2b [00-09] Workspace Sidebar.png
  4 [01-34] Folders.png
```


## A shorts batch project is named for the week it was shot

`BATCH <week> - MM-YY`, in `60-Shorts`. The number is the week of the month, the suffix is
the month and the two-digit year of the **recording**, never of the publishing window: a batch
publishes over three or four weeks and often crosses a month boundary, so a publishing month
puts two batches on the same name. Set 31 Aug 2026, when five projects carried three
distinct names between them and two of them read `BATCH 2`.

The number is inherited from the Apple Notes queue (`Projects › Shorts › Batch N`), which rolls
when a batch is folded into the one ahead of it, so it is **not** re-derived from the shot date
and it is not renumbered to close a gap. Only the suffix is computed. The five that exist:
`BATCH 2 - 07-26`, `BATCH 2 - 08-26`, `BATCH 3 - 08-26`, `BATCH 4 - 08-26`, `BATCH 1 - 08-26`.

Name it at creation, `pnpm descript project new "BATCH 5 - 09-26" --folder 60-Shorts`, because a
rename after the fact leaves every doc that quoted the old name stale.
