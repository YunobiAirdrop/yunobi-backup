# Publishing and downloading a composition

Split out of `SKILL.md` on 2026-08-28 to hold the 250-line ceiling. Proven 26 Aug 2026, moving
the five ClickUp mini-course videos into Skool.

Proven 26 Aug 2026, moving the five ClickUp mini-course videos into Skool. **Publishing a
composition is what produces a downloadable file**, and the download URL comes back on the job
rather than on the project:

1. `publish_project` with `composition_id`, `access_level` and `resolution` returns a `job_id`.
   Publishing the same composition again **reuses its existing share URL** and overwrites the
   content, so it does not scatter new links.
2. `GET https://descriptapi.com/v1/jobs/{jobId}` on the **public** token carries
   `result.download_url`, a signed Google Storage URL valid 24 hours
   (`result.download_url_expires_at`).
3. `curl` it. A 3-minute 1080p cut is about 250MB and a 23-minute one about 730MB.

**Two traps, both of which cost a cycle.**

- **`GET /v1/jobs` omits `download_url`.** The list gives `status`, `composition_id`, `share_url`
  and `media_type` and stops there. A poller built on the list watches a finished job forever and
  downloads nothing; only the single-job GET has the URL.
- **One publish job per project at a time.** A second `publish_project` on the same project answers
  *"A publish job is already running"*, so a whole course is published in sequence, not in
  parallel. Poll the job list and fire the next one when the count of non-`stopped` jobs hits zero.

**Ask for the resolution the timeline actually is.** `resolution` accepts up to 4K and a 1080p
timeline published at 4K is an upscale that triples the file for nothing.

**Renders do not belong in a repo.** Five videos of this course are 2.1GB; they live in
`~/Movies/<course>/`. A `courses/<slug>/video/` folder inside a repo would be tracked,
because `business/.gitignore` ignores only `.impeccable/`.
