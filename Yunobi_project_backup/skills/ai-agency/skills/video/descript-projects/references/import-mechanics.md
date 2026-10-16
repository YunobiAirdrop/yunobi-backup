# Import mechanics: the REST fallback, the caps, and direct upload

Split out of `SKILL.md`. Read it before an import session, together with `learned-patterns.md`.

## Import mechanics

**When there is no Descript connector on the session, go straight to the REST API.** The personal token is `DESCRIPT_API_TOKEN` in your own env file, the base is
 `https://descriptapi.com/v1`, and `https://docs.descriptapi.com/openapi.yaml` is the live endpoint list. `GET /projects`, `GET /projects/{id}` and `POST /jobs/import/project_media` cover everything an import needs, and `GET /jobs/{job_id}` is the wait. Nothing below changes for an import. **The MCP is not a pure wrapper, so the fallback is not equal.** Four of its tools answer to no endpoint in the spec at all - `export_timeline`, `list_folders`, `get_drive_info`, `import_drive_media` - and a fifth, `report_upload_status`, only serves the direct-upload flow. Timeline export to EDL, AAF, FCPXML or Resolve XML is MCP-only; there is no REST route to it. Lose the connector and you lose those, whatever the token can do. Drive it with `scripts/import_media.py <project_id> <manifest.json>`, dry run first: `upload_urls` maps each display name to an *object* holding the URL, and a run that reads it as a string creates the job, uploads nothing, and burns every name in the manifest - cancelling the job does not give them back (`references/learned-patterns.md`, 2026-08-19).

**Cap: 3 media per call through the MCP, not through the API.** The MCP returned `Failed to create project media import job: Query count exceeded limit of 100` above three on 2026-08-01 (18 failed, 5 failed, 3 succeeded). A direct `POST /jobs/import/project_media` took **nine** direct-upload items in one call on 2026-08-18 and reported all nine `success`. Batch in threes when going through the MCP; through the API, send the set.

**One job at a time per project.** A second import while one is running returns `A job is already running for this project`. Call `wait_for_job` between batches. Not optional; the whole batch is rejected, not queued.

**Prefer direct upload to URL import.** URL import validates server-side and rejects anything that answers with HTML, including CDNs that serve the file perfectly to `curl`. Direct upload is two steps and never has this problem:

```bash
# 1. import_media with content_type + file_size returns upload_urls
# 2. PUT the bytes
curl -sS -X PUT -H "Content-Type: application/octet-stream" \
  --upload-file FILE "$UPLOAD_URL" -w "HTTP %{http_code}\n"
```

The declared `file_size` must match the file exactly. Signed URLs last 3 hours.

Pass `language` on takes with speech so the transcript comes back usable.
