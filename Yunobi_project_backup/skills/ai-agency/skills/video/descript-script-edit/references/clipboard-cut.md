# Cutting through the clipboard

`scripts/dscript.py` runs the whole loop. The user does the two ends - Cmd+A Cmd+C before `grab`,
Cmd+A Cmd+V after `apply` - and nothing in between needs credits or a browser.

```bash
D=scripts/dscript.py                    # ask: click into the script, Cmd+A, Cmd+C
python3 $D grab lesson-1                # decode + archive the clipboard, print the state
python3 $D words                        # indexed transcript, for writing the cut list against
# write phrases.json: [{"text": "<the words to cut>", "pass": 1, "reason": "...", "nth": 1}]
python3 scripts/resolve.py phrases.json cuts.json    # words -> token indices, audited
python3 $D apply cuts.json --typos scripts/typos.example.json --styles scripts/styles.example.json \
                           --markers markers.json
                                        # then tell them: Cmd+A, Cmd+V
python3 $D check                        # they copied it back? prove it matches what you built
```

**Write the cut list in words, never in indices.** `scripts/resolve.py` turns a phrase into the
token range `apply` wants, prints five words of context each side so the landing can be read back,
and refuses a phrase that matches nothing, matches twice with no `nth`, or overlaps another needle.

`apply` cuts as **Ignore**, keeps the Ignores already there, removes fillers, repairs glued
stutters, carries every scene boundary and marker onto the TAU that still holds its text, and
refuses a payload that does not round-trip, so a second pass is safe and an empty cut list is an
exact no-op. Every flag, the house glossary that stops a caption naming the wrong product, and the
partial-grab payload: [`references/pasteboard.md`](pasteboard.md) and
[`references/typos.md`](typos.md).
