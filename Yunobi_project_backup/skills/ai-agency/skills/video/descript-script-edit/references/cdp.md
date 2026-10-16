## Typed text has no Ignore, and keystrokes go through CDP

Text that arrived by keyboard rather than by recording has no media behind it, so Descript mounts
no selection toolbar for it. The drag lands, the selection is exactly right, and the driver reports
`toolbarMissing` with a correct `len`. **A right-sized selection plus a missing toolbar is the
signature of no-media text** - the span has to be deleted, never ignored, and retrying for the
toolbar cannot succeed.

Send the key through CDP, which needs no window and no focus:

```bash
orca exec --command "key Delete" --page "$PAGE"
```

The OS-level commands are the trap. With no on-screen Orca window,
`orca computer press-key --app Orca` returns `window_not_found`, and `orca keypress --key Delete`
reports `{"pressed":"Delete"}` while doing nothing - so a delete loop reports `still-present`
forever with no clue why. Check with `orca computer list-windows --app Orca --json`; an empty
`windows` array means no OS keystroke will land, and `orca open` does not create one. Never raise
the window to deliver a key: doing that on 2026-08-15 left Orca frontmost and four batches of the
user's dictation landed in the script, each replacing whatever span was selected at the time.

Guard a delete exactly like an Ignore (law 6), then re-read to confirm. A **one-character** span
cannot be dragged at all - use a guarded caret instead: click the character's left rect, verify
`getSelection()` is collapsed *and* its anchor sits inside the intended block, press forward
`Delete`, then verify the neighbouring blocks are byte-identical. Backspace is wrong there, because
the caret lands at offset 0 and merges the paragraph into the one above.

`scripts/delcdp.py` is the working implementation.
