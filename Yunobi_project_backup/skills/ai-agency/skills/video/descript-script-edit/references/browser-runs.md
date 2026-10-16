# Driving the editor: tabs, parallel runs, and reading the result back

The browser path only. The clipboard path in [`pasteboard.md`](pasteboard.md) needs none of this -
no tab, no session, no viewport.

## The run, cold

The whole run, cold, with no thinking required. `$P` is the project UUID, `$S` the first 5 characters of the composition UUID.

```bash
PAGE=$(orca tab create --url "https://web.descript.com/$P/$S" --json | jq -r .result.browserPageId)
sleep 15                                                    # the editor loads slowly
orca exec --page "$PAGE" --command "set viewport 1600 20000" # AFTER the load, not before
orca eval --page "$PAGE" --expression "$(cat scripts/helpers.js)" --json
orca eval --page "$PAGE" --expression "JSON.stringify(window.__blocks().map(b=>window.__map(b).text))" --json
```

**Check the dump is real before you trust a word of it.** Descript virtualises the script pane:
a paragraph that is off screen renders as a skeleton (`data-block-skeleton="true"`) holding the
raw transcript as one flat text node, with no ignore styling on it. A dump taken before the
viewport has grown therefore reads the **uncut** take on every off-screen block, so a lesson that
was carefully edited looks untouched and the cut list is written against text that is already gone.
On 2026-08-19 that made a 27k-character edited script read as 36k of raw stutters.

```bash
orca eval --page "$PAGE" --expression "JSON.stringify(window.__blocks().filter(function(b){return b.getAttribute('data-block-skeleton');}).length)" --json
```

Zero, or the dump is fiction. Grow the viewport again and re-read.

Save those blocks as `blocks.json` and build `needles.json` against them - both passes, audited
with `candidates.py --check` (see **What to cut**). Dry-run every needle through
`window.__find(t, b)`, then:

```bash
DESCRIPT_PAGE=$PAGE python3 -u scripts/drive.py needles.json > run.log 2>&1   # run_in_background
```

Retry whatever reports `blocked`, then verify with `export_transcript` and `get_project`. Nothing else is required.

## Confirm the tab is on the composition you asked for

**A bad composition id does not error - it silently opens a different lesson.** Descript redirects to whatever it last had open, or to the project's first composition. An agent that trusts the URL it typed will cut the wrong video, and every guard in this skill will pass while it does. So the first read after any `navigate` is:

```bash
orca eval --page "$PAGE" --expression "JSON.stringify({url: location.href})" --json
```

If the URL does not still end in your `<short>`, stop. Do not cut.

The composition list is also live: the user renames, re-points and deletes compositions while you work. On 2026-08-15 a composition that `get_project` had listed minutes earlier was gone by the time its agent opened it - the footage had been unhooked and left as raw media. Re-read `get_project` before concluding anything about a composition that misbehaves, and never mint a new composition to "fix" a missing one. Which lesson raw footage belongs to is the user's call.

## Which compositions still need cutting

`get_project` answers this without opening anything. A composition whose `duration` **exactly equals** one of the `media_files` sequence durations has never been touched; one that is shorter has been cut. A duration of `1` (or `0`) is an empty placeholder with no media - there is nothing to edit, so do not open it.

Do not judge by the publish list. Every one of these lessons had been published from its raw take, so a share URL says nothing about whether the script was edited.

## One agent per composition

Lessons are independent, so fan out - one subagent per composition, each with its own tab. Two rules make it safe:

- **No agent may type with the OS-level commands.** `orca type` and `orca keypress` ignore `--page` and hit whatever tab is focused, so one agent's keystroke lands in another agent's lesson. `orca exec --command "key ..." --page "$PAGE"` goes through CDP, honours the page and is safe in parallel - use it for every keystroke. Anything that genuinely needs `orca type` has to run alone.
- **No agent touches a tab it did not create,** and none of them call `orca tab switch`.
- **Park OS focus on a blank tab before the fan-out starts.** Whatever the human types goes into whichever Descript tab holds focus - not into a text field, into the *script*. It has happened twice: a `#` into one lesson, and 800 characters of unrelated notes into a short, which also ate part of a closing line two paragraphs further down. Law 8 does not cover this; its `mouse up` and `removeAllRanges()` only guard against the driver's own selections, never against focus theft from outside the process. So create one throwaway tab on `about:blank`, `orca tab switch --page <blank> --focus`, and leave it there for the whole run. Tell the user their typing lands in the editor otherwise.

**Parking focus is not protection, only a head start.** It held for about twenty minutes on 2026-08-15 and then the user clicked into one of the editor tabs to publish, at which point focus was theirs again and two of three lessons took an injection. What actually decides whether that costs anything is how long a live selection is standing when it happens: a cut between drags is exposed for a second, and a cut stuck in the escalation loop is exposed for as long as it retries - 25 minutes on that run, which is how 165 characters of the user's own typed instruction came to *replace* a stutter. So bound the exposure rather than trusting the parking: any cut that has retried past a couple of minutes gets `mouse up` and `removeAllRanges()` before the next attempt, and a run that is going to take an hour is told to the user up front, because they will use the app in that hour.

When damage does land, diff **every** block, not the one showing the garbage - a single foreign edit spans paragraph boundaries and deletes content well past where the typed text appears. Undo in a checked loop, and check for two things after each click: the bad text gone *and* the eaten text back. They flip at different click counts.

Give each agent its target UUID, its editor URL, its own scratch prefix, and the instruction to read this skill first.

## Use Orca's browser, not Claude in Chrome

Both can drive the page. Orca wins on every axis that matters here, measured 2026-08-14 on a 19:41 composition, 29 cuts:

| | Claude in Chrome | Orca (`orca exec` → agent-browser) |
|---|---|---|
| Session | fresh profile, hits the Descript login wall | cookies imported, already authenticated |
| Coordinates | screenshot is **scaled** vs DOM | 1:1 CSS pixels, no conversion |
| Cost per cut | ~2 MCP round trips, seconds each | one shell loop for all of them |
| Batching | `browser_batch` only | full Python/bash driver |

The Claude in Chrome scaling trap, if you are ever stuck with it: `getBoundingClientRect()` returns DOM pixels but `computer` clicks in **screenshot** pixels. Multiply by `screenshotWidth / window.innerWidth` (measured 1568/1920 = 0.817). Skipping this clicks two lines off target.

Orca setup is already done on this machine: CLI at `/usr/local/bin/orca`, cookies imported. Open a tab, note `browserPageId`, and pass `--page` on every call.

The `<short>` in the editor URL is simply the **first 5 characters of the composition UUID** - `fff8f317-623e-...` opens at `/fff8f`. `get_project` hands you the full UUIDs, so no lookup is needed.

```bash
orca tab create --url "https://web.descript.com/<project>/<short>" --json
orca eval --page "$PAGE" --expression "$(cat helpers.js)" --json
orca exec --page "$PAGE" --command "mouse move 100 200" --json
```

## Run the lessons in parallel, one tab each

`orca tab create` gives every composition its own `browserPageId`, and mouse commands are addressed per page, so three lessons cut at once without interfering. Open a tab, grow its viewport, install helpers, dump its blocks - then start `drive.py` on it while you write the next lesson's cut list.

Two things to respect. Run each `drive.py` with `run_in_background`, because a Bash call is capped at 10 minutes and 30 cuts take longer than that; a run killed mid-drag can leave a selection standing, so clear it before doing anything else. And size the viewport to the script: roughly 0.8 px per character of transcript, so a 27 000-character lesson needs `set viewport 1600 34000`. Anything that does not fit reports `offscreen` instead of cutting.

Budget the time. Every `orca` round trip costs about 4-5 seconds once the document is large, and a cut spends a dozen of them between the block dump, the drag and the toolbar retries. A 30-cut lesson runs 20 to 30 minutes; a 60-cut, 100-block lesson runs closer to an hour. A driver that stops writing lines is not necessarily stuck - measure one `mouse move` before killing it. When you do kill one, the restart is free: `python3 drive.py needles.json $(seq 40 60)` picks up where it stopped, and anything already ignored reports `not-found-or-done`.

## The exported transcript is not a faithful renderer

`export_transcript` sometimes runs two adjacent paragraphs together with no space - `conservative.Two hours a week` - where the live DOM has them correctly separated. Do not chase that as a stitching bug. When the transcript shows two words glued, check the block texts in the DOM before repairing anything: a real glue-up (the both-boundary-spaces mistake) shows up *inside* one block, a rendering artifact shows up only across a block break.

## The loop

```
dump blocks  →  both passes  →  --check clean, ratio in range  →  install helpers
   →  grow viewport  →  per needle: find → drag → guarded ignore (with retry)
   →  restore viewport  →  read the export as prose  →  verify via get_project
```

`scripts/helpers.js` and `scripts/drive.py` in this skill are the working implementation. Verified end to end 2026-08-14 on `M0 L1 - Why agencies hit the ops ceiling`: 29 cuts, **1181.54s → 999.35s**, 182.2 seconds of false starts removed, zero bad cuts, confirmed server-side by `get_project`.

Zero bad cuts is not a finished script. That list audited sixteen candidates short on 2026-08-18
with the whole of pass 2 missing, and the corrected `scripts/needles.example.json` runs to 40
needles and 22.8% of the characters. The driver is trustworthy; `40 of 40 landed` still says
nothing about the needles nobody wrote.
