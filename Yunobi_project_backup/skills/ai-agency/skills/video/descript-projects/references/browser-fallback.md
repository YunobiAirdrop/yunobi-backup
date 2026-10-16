# Reorganising the media browser by hand

The fallback for when `pnpm descript` cannot authenticate. Everything here was learned the hard way before the CLI existed; `mv`, `rename`, `mkdir` and `rmdir` do all of it in one call each.

Everything here runs in the **Project** panel, not the Media panel. `sidebar-project-item` in the
left rail opens it; `sidebar-media-item` opens the stock/library pane, which lists nothing from the
project and is the wrong surface. Open the project on any composition, grow the viewport so the
whole file list fits (`set viewport 1600 1500` covers ~20 rows), and read the tree from
`[data-testid="sidebar-content"]`.

```bash
PAGE=$(orca tab create --url "https://web.descript.com/$P/$S" --json | jq -r .result.browserPageId)
sleep 25 && orca exec --page "$PAGE" --command "set viewport 1600 1500"
# click sidebar-project-item, then:
scripts/newfolder.sh   page.txt "Productizing"        # root-level folder, named
scripts/rename_folder.sh page.txt "Productizing" "Delivery"   # only to rename one later
scripts/movefile.py    page.txt "Speaker Name-9" "Productizing"
```

`sidebar-project-item` **toggles**. The panel is usually open already, so a first click closes it
and `sidebar-content` comes back null; click again and read the tree rather than concluding the
panel failed to open.

Eight things this cost to learn:

- **There is no move command.** A media file's context menu offers Rename, New composition from
  file, Create sequence, Insert into script, Add as new layer, Re-transcribe, Identify speakers,
  Detect filler words, Detach audio, Replace, Set A/V sync offset, Repair audio drift, Add to media
  library, Add to Underlord, Download, Delete, Change visual role - and no move. Drag is the route.
- **The drop needs a slow drag.** Mouse down, pause, a few waypoints, then hover the target row a
  second before mouse up. A fast drag reports `Dragging was cancelled.` and changes nothing.
- **The tree announces every drop.** The last line of the panel's text is a live region reading
  `Item "<name>" was dropped in Group "<folder>"`. That is the cheap verification; `get_project`
  confirms it server-side as a path change on the media key. **A stale announcement means the drop
  failed**, and it fails predictably: the drop that lands re-renders the tree - the target folder
  auto-expands and the live-region line is itself a row - so the *next* drag is the one that misses.
  Read the announcement after every move, and re-run the ones naming the previous file. Two of six
  moves needed exactly one retry each on 2026-08-15, and both landed on it.
- **"New folder" nests inside whatever is selected.** Right-clicking a folder and taking New folder
  puts the new folder *inside* it - which is how `Delivery Space/Productizing/` got created by
  accident - and with a file selected the menu has no New folder at all. Clear the selection by
  left-clicking the empty area below the list, then right-click there for the root menu. There is
  no drop target for the root, so a folder created in the wrong place cannot be dragged out: move
  its files into a correct folder and delete the empty one.
- **Renaming: type straight over the pre-selected text.** `Meta+a` closes the field instead of
  selecting it, and the rename then commits unchanged. Enter commits. `orca type` ignores `--page`,
  so `orca tab switch --page "$PAGE" --focus` first.
- **A new folder opens straight into that rename field, and its row never settles.** The row keeps
  reading `Group` for as long as the field is open, so a wait loop watching for `Untitled Folder`
  in the tree text times out on a folder that was created perfectly. The settle signal is
  `document.activeElement.value === "Untitled Folder"`. Name it there, in the same breath as
  creating it; the right-click Rename pass is only for renaming a folder later.
- **Assert `elementFromPoint` before every click.** A composition row sits under the sticky Files
  toolbar, so its rect is honest while the point belongs to the toolbar, and the right-click then
  opens nothing at all with no error anywhere. `el.scrollIntoView({block:'center'})`, re-read the
  rect, and check the point carries the row's own text.
- **Stray keys land in the Files search box and empty the tree.** `No results` under Files usually
  means a filter, not a missing file, so read the `search` input's value first. `press` needs
  `orca tab switch --page "$PG" --focus` like `orca type` does, and a click puts the caret mid-text,
  so clear it with the React native value setter plus an `input` event rather than backspaces.
- **Stay off "Edit sequence".** Taking it from a sequence's context menu killed the browser page:
  `browser_tab_not_found`, no tabs left. Nothing was lost, but the session restarts.

The `Add` button at the top of the panel (`add-composition-menu-trigger`) belongs to
**Compositions**, not Files. Its Folder item creates a composition group; one created that way has
to be deleted from the composition list.

## Pairing takes, and naming a sequence

Moved out of SKILL.md on 25 Aug 2026 to hold it under the 250-line ceiling.

## Reorganising the media browser, the browser fallback

`pnpm descript mv/rename/mkdir/rmdir` does all of this in one call each. The hand route - which panel, why a fast drag is cancelled, how the tree announces a drop, and the five other things it cost to learn - is in `references/browser-fallback.md`. Read it only when the CLI cannot authenticate.

### Pairing a camera take with its screen recording

Loose recording pairs carry no clue in their names (`Speaker Name-7`, `RPReplay_Final1786791996.MP4`).
Do not pair them by nearest duration - that is wrong as often as it is right. Pair them through the
**sequence** durations in `get_project`: a sequence's duration is its longer member, so a sequence
that matches a camera take exactly owns that take, and its screen partner is the longest screen file
still under that number. On 2026-08-15 this reversed a nearest-duration guess.

`RPReplay_Final<n>.MP4` names are unix timestamps of the **end** of the recording, not the start:
subtract the duration and the takes chain in order with no overlap. That gives the recording order
of a session, which orders the pairs but does not name them - only the person who recorded them
knows which lesson each one is. Ask rather than infer; a misfiled source take is worse than a loose one.

### Name a sequence from the course, never from the composition

A composition name is typed by a human and drifts. On `Agency Master Course 3.0`, 8 of 13 carried the wrong module and lesson number, so copying them onto the sequences would have burned the error into names the API cannot fix. Find the file that owns the naming scheme and join on something machine-generated: the course manifest stores each lesson's `share.descript.com` URL, which matches `publishes[].share_url` exactly, giving composition-to-lesson with no inference. Then check the repo for the same drift; two script files carried a lesson code that disagreed with their own filename.

Confirm the last hop, sequence to composition, with `export_transcript` and `include_speaker_labels: "every_paragraph"`. The paragraphs come back prefixed with the **source track name**, so the edit tells you which media it was cut from. It also answers the multi-take question durations cannot: a 400s take that looked like an abandoned first attempt turned out to supply 15 paragraphs of the published cut.
