# The house glossary

**`--typos` is the house glossary, and it is what stops a caption saying the wrong product name.**
`scripts/typos.example.json` carries 41 entries: the tools a transcriber splits or lowercases
(`Hyper Frame` -> `HyperFrames`, `Make dot com` -> `Make.com`, `N8N` -> `n8n`, `De script` ->
`Descript`), the ones it hears as an ordinary word (`Cloud Code` -> `Claude Code`, `Entropic` ->
`Anthropic`), and your own house names, which a transcriber gets wrong every time. Add to it whenever a
run surfaces a new one - a caption is the part of a video most people read and never hear.


**A key that is an ordinary English word rewrites correct speech, so it is not allowed in.**
`"ski": "skill"` turns *I ski a lot* into *I skill a lot*; `"School": "Skool"` catches a sentence
that opens on the word. Both were written and both were pulled the same day. The pattern only
anchors `\b` where the key has a word edge, so test any new key against ordinary prose before it
ships.
