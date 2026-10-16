# Review in Editor OS

The project page is the review board. Its rail lists the passes and how many choices each has left. A pass is done when nothing in it is open, so there are no steps to close and no Finish button. The editor reads the cut, then keeps, skips or requests a change on each beat. Nothing is placed by a review click.

## Prepare the page

`editor-os transcript <project>` pulls the cut, its words and its chapters from Descript into `edit.json`. Run it after a cut changes. `editor-os plan <project>` reads `beats.json`, `pins.json` and the music offer into `edit.json` and keeps earlier decisions by beat.

`beats.json` is optional proposal input. Its `layouts`, `motion`, `broll` and `sfx` rows use `[code, "m:ss", "spoken line"]`; layout rows add an array of pack names. Put motion files under `motion/`, footage under `broll/<worker>/`, and sound effects under `sfx/`. Name each option with its beat code first, such as `M1 [01-16] Tools.mp4`. The project page finds new files on refresh. A beat with no file says what it is waiting for.

## The passes

The rail shows the eight passes of the ledger. The ones with something to decide open a view:

1. **Cut and Reorder:** the transcript, with what the pass removed or moved marked on its lines. A note on a line asks for a cut fix.
2. **Rhythm:** the layouts, one card per layout change, and any zoom. Keep the AI's pick or choose another option.
3. **Music:** the three tracks, then keep one, skip, or ask for more.
4. **Motion and B-roll:** each insert in playing order. Preview each option, keep one or skip the beat. An unrendered beat cannot be kept.
5. **Review:** the whole transcript, for notes.

Every decision lives in `edit.json` and every note in `edit.notes.json`, both beside `RUN.json`. The folder's transcript, beats, media and music offer describe what is available; they do not own the editor's decisions. The page saves a click immediately and shows its result. `editor-os feedback <project>` and `editor-os wait` read the same files; answer a note with `editor-os reply <project> <id> "<what changed>"`. A note on a beat reopens that beat until the answer is accepted.

`editor-os place <project>` refuses until every beat and the music are decided. It applies kept layouts, pins kept media and sound effects, then lays the selected music bed. Unkept files stay in the folder.

Notes and choices from before `edit.json` (`plan.json`, `plan.notes.json`) are imported once, when the project is first opened. The old files stay on disk and are not written again. For new work, use only the project page.
