# The nine laws of driving the Descript editor

Every law was paid for by a repair. `scripts/drive.py` implements all nine.

**1. Only trusted input works.** Descript ignores synthetic events completely. A `new KeyboardEvent('keydown',{key:'Delete'})` dispatched at the editor does nothing, even with `keyCode` patched on. Setting a DOM Range and calling `getSelection().addRange()` sets the browser selection but Descript never registers it - the selection toolbar does not mount. Every selection must come from real mouse input.

**2. A drag is the only gesture that mounts the toolbar.** This is the single hardest-won fact. `click` then `shift+click` produces a *visually correct, correctly measured* selection - right words, right word count, right duration on the timeline - and the toolbar still never appears, so there is nothing to click. `left_click_drag` / `mouse down → move → up` produces the same selection **and** mounts the toolbar. Always drag.

**3. Ignore is not Delete.** They are different operations with different reversibility:
- **Ignore** (`[data-testid="selection-toolbar-ignore-button"]`, the S in the toolbar) leaves the words in the script struck through, excluded from the render, restorable later via *Restore ignored text*. This is the default for anything you did not record yourself.
- **Delete** (the Delete key) removes the words outright. Recoverable only by ⌘Z in the same session.

Both shorten the composition identically. Prefer Ignore. There is no keyboard shortcut for it and no entry in the right-click menu; the toolbar button is the only route.

**4. Ignored text stays in the DOM.** Struck-through words remain in `textContent`, so naive `indexOf` keeps matching text that is already cut, and offsets drift. Filter by computed style:

```js
getComputedStyle(el).textDecorationLine.includes('line-through')
```

A needle whose match is inside ignored text should report *not found*, which conveniently makes the whole run idempotent - re-running skips completed cuts.

**5. Never trust the exported transcript for exact needles.** `export_transcript` and the live DOM disagree in small ways. Measured 2026-08-14: the export read `Maybe you know better about how to deal with it` where the DOM had `Maybe you know better how to deal with it`. Build the cut list from the export to decide *what* to cut, then match against `__map(block).text` from the live DOM. Every mismatch is a silently skipped cut.

**6. Guard every click with a selection equality check.** This is what makes the method safe. Never click Ignore because a drag happened; click it because the selection **is** what you meant:

```js
if (norm(getSelection().toString()) !== norm(expected)) return {mismatch:true};
```

Without this guard a stale coordinate ignored 984 characters and 49 seconds of good content in one action (2026-08-14). With it, a drifted coordinate is a no-op you retry. Whitespace-normalise both sides.

**7. Do not scroll. Grow the viewport.** Descript's script pane refuses to be scrolled programmatically - `scrollTop = 1200` snaps straight back to its previous value - and mouse wheel events do not move it either. Instead make the whole document fit:

```bash
orca exec --page "$PAGE" --command "set viewport 1600 11500"
```

The pane grows to roughly 0.69 × viewport height. When the content fits, every target is on screen at once and scrolling never enters the problem. Restore a normal viewport before screenshotting for the user. Re-apply `set viewport` **after** any `navigate`: the override does not survive a page load.

Then check the timeline is not sitting on top of the text. The timeline panel takes a share of whatever height is left over, so a viewport that is tall but not tall enough leaves it overlapping the bottom of the editor pane. Coordinates there are geometrically right and still land on the timeline, so the selection comes back empty every time and no amount of retrying helps:

```js
window.__ed.getBoundingClientRect().bottom < document
  .querySelector('[data-testid="timeline-container"]').getBoundingClientRect().top - 60
```

If that is false, grow the viewport again - generously, since the timeline eats a fraction of every pixel you add - and re-check. `document.elementFromPoint(x, y)` at a failing drag coordinate tells you which panel you actually hit, and separates this from a drag that simply failed.

**8. Release the mouse before every drag, and drop the selection after every cut.** A `mouse up` that does not register leaves the button held down, and the next cut's `mouse move` extends a single selection across every paragraph in between. The guard in law 6 refuses to fire on it, so the cut merely reports blocked - but any keystroke that reaches the page then *replaces* that whole span. This is how 3.5 minutes of good content disappeared on 2026-08-15, when a chat message the user typed landed in the editor. `drive.py` now opens each cut with an unconditional `mouse up` and closes it with `removeAllRanges()`. Never leave a live selection standing between cuts.

**9. Block indices are a hint, not an address.** An Ignore sometimes splits one paragraph into two, so every index recorded when the cut list was written shifts by one from that point on. Measured 2026-08-15: 34 blocks became 35 mid-run and the remaining 18 cuts all reported not-found. `drive.py` re-reads the blocks before each cut and takes the candidate nearest the recorded index. Scope a needle to a block whenever a second paragraph could contain the same text - `"So"` on its own line will otherwise match the `So` that opens some paragraph far above.
