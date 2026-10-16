# When a run goes wrong, and when a drag will not land

Guards refuse bad cuts; these are the paths back when one lands anyway, and the escalation that makes a stubborn drag connect.

## Undo is a button, not a keystroke

When a run goes wrong, this is the way back. `Cmd+Z` does **not** work: `orca exec --command "key Meta+z"` reports `pressed` and changes nothing, and top-level `orca keypress --key Meta+z` goes to the **Orca app itself** rather than the page - forty of them opened the About Orca window and left the document untouched. The web app's own control is the only route that works:

```js
document.querySelector('[aria-label="Undo"]').click()
```

Click it in a loop with a check after each one, and stop the moment the damage is gone - each further click removes one good cut. 19 clicks unwound an accidental overwrite on 2026-08-15 and every cut before it survived. Verify with the non-ignored text, never with `innerText.length`: ignored words stay in the DOM, so the length never moves.

```js
// live script, ignored words dropped - the thing to diff against a known-good export
window.__blocks().map(function (b) {
  var w = document.createTreeWalker(b, NodeFilter.SHOW_TEXT), s = '', n;
  while ((n = w.nextNode())) s += (window.__ignored(n) ? '' : n.data);
  return s;
})
```

## When a drag collapses into a click

A one-jump `mouse move` sometimes selects only the needle's first word, and it does so **deterministically** - re-running the same cut reproduces the identical wrong selection, so a plain retry is wasted. `drive.py` now escalates on its own: one jump, then five waypoints, then five waypoints dragged end-to-start. Measured 2026-08-15 across two lessons, the slower drag cleared eight of nine such cuts and reversing direction cleared the last.

It escalates only when the selection came back **shorter** than the needle. A selection *longer* than the needle is the law 6 case - a stale coordinate - and dragging harder only selects more of the wrong thing.

Two things to know before you trust the escalation:

- **The reversed drag can over-select at a block boundary.** Starting from the end coordinate, the browser resolves the far end ambiguously and can run on - one produced a 1798-character selection where 135 were wanted. The law 6 guard refused it, as designed, so nothing was ignored. Treat reversal as a last resort and read the mismatch length rather than assuming the drag simply failed again.
- **Never anchor a needle on a paragraph's leading whitespace.** Descript floats UI furniture over it - the speaker avatar on one lesson, an "Add to Underlord" button on another - and it swallows the `mouse down`, so the drag never reaches the text and the cut reports `blocked` forever. Start the needle one word in. When a cut refuses to land for no visible reason, `document.elementFromPoint(sx, sy)` names whatever is sitting on top; if it is not editor content, move the anchor rather than dragging harder.
- **A long multi-line needle is more fragile than several short ones.** A 365-character three-line drag that would not connect landed first time once it was split into three needles.

## The toolbar mounts late

Even after a correct drag the button can take seconds to appear. A single check fails about half the time; a retry loop fixes it completely. Measured 2026-08-14: 10 of 13 cuts reported `toolbarMissing` on one attempt, and all 10 succeeded on retry with no other change.

```python
for _ in range(10):
    time.sleep(0.8)
    res = ignore_if(needle)
    if res.get("clicked") or res.get("mismatch"):
        break
```

Break on `mismatch` too - that is a real answer, not a timing problem.
