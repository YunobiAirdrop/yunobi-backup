# The agent path: credits, its two faults, and the API dead end

Moved out of SKILL.md on 31 Aug 2026 to hold it under the 250-line ceiling. That the agent path
is tried first, and that a top-up is the user's call, stay in the skill.

It is metered on Descript AI credits. When they are gone it fails clean, project untouched:
`{"status":"error","error_message":"Insufficient AI credits"}`.

**Two things it always gets wrong, so put both in the first prompt.** It **ignores words and leaves
the silence**, so a cut that reads right runs at 114s where the words are 60s - ask for the gaps
closed in the same breath as the cut (0.35s between sentences, 0.2s inside one, total under 5%).
And it **cuts the head off a kept sentence**, twice on one video even with each passage quoted whole,
while reporting that passage as kept. So **read the transcript back and check every sentence starts
where a sentence starts**; the repair is one prompt naming the missing words and the attempt they
belong to.

**A top-up is the user's call, never yours.** Give them the `upgrade_url` and stop. Only when they
decline, or want the edit now, does the clipboard path apply - and the browser only after that.

**It is also the only API write path, so do not go looking for a cheaper one.** Descript's public
REST API (`https://descriptapi.com/v1`) exposes seven endpoints and only `/jobs/agent` mutates a
script: no transcript-patch endpoint, no documented `.descript` format, and `export_timeline` has
no matching import. At zero credits the tree has two branches, a top-up or the clipboard.
