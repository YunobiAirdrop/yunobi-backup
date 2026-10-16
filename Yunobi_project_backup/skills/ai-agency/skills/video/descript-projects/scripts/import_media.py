#!/usr/bin/env python3
"""Import local media into a Descript project by direct upload.

WHY this is a script and not a curl in a session: the direct-upload flow has one shape that is easy
to read wrong and expensive to get wrong. `upload_urls` comes back as

    {"Folder/Display Name.mp4": {"upload_url": "...", "asset_id": "...", "artifact_id": "..."}}

and a run that treats the value as the URL dies after creating the job. The job then sits at
`waiting_for_uploads` forever, `GET /jobs/{id}` does not return the URLs a second time, and every
display name in the manifest is permanently taken on the project. `DELETE /v1/jobs/{id}` answers
204 and cancels the job but does NOT release the names: they stay in `media_files` as `type: other`
with a null duration, and a later POST reusing them hangs and then resets the connection. The only
way back is deleting those rows by hand in the app.

So this script writes the response to disk before touching it, uploads every file, and only then
polls. Run it twice and it is safe; run half of it and you have burned the names.

Usage:
    import_media.py <project_id> <manifest.json> [--dry-run]

manifest.json is {"Folder/Display Name.ext": "/abs/path/to/file.ext", ...}. The key IS the display
name and a "/" in it creates a folder. Names are write-once, so read the dry run before committing.

The token is read from DESCRIPT_API_TOKEN in the environment, or from --env-file.
"""
import json, mimetypes, os, pathlib, sys, time, urllib.error, urllib.request

BASE = "https://descriptapi.com/v1"


def token(env_file=None):
    tok = os.environ.get("DESCRIPT_API_TOKEN")
    if tok:
        return tok
    for path in filter(None, [env_file, "app/.env.local", ".env.local"]):
        p = pathlib.Path(path)
        if p.exists():
            for line in p.read_text().splitlines():
                if line.startswith("DESCRIPT_API_TOKEN"):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("no DESCRIPT_API_TOKEN")


def call(tok, method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": f"Bearer {tok}"}
    if data:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    raw = urllib.request.urlopen(req, timeout=180).read()
    return json.loads(raw) if raw else {}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    project, manifest_path = args[0], args[1]
    tok = token()
    manifest = json.loads(pathlib.Path(manifest_path).read_text())

    add_media = {}
    for key, path in manifest.items():
        p = pathlib.Path(path)
        if not p.exists():
            raise SystemExit(f"missing file for {key}: {p}")
        ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        add_media[key] = {"content_type": ctype, "file_size": p.stat().st_size}
        print(f"  {p.stat().st_size / 1e6:8.1f} MB  {ctype:18} {key}")
    print(f"  --- {len(add_media)} files, {sum(v['file_size'] for v in add_media.values()) / 1e6:.0f} MB")
    if dry:
        return

    res = call(tok, "POST", "/jobs/import/project_media", {"project_id": project, "add_media": add_media})
    # Written before anything else touches it: a bad parse after this point costs the names.
    pathlib.Path("descript-import-response.json").write_text(json.dumps(res, indent=2))
    job = res["job_id"]
    print("job", job, "(response saved to descript-import-response.json)", flush=True)

    for key, entry in res["upload_urls"].items():
        url = entry["upload_url"] if isinstance(entry, dict) else entry
        p = pathlib.Path(manifest[key])
        print(f"    PUT {p.stat().st_size / 1e6:6.1f} MB  {key}", flush=True)
        with open(p, "rb") as fh:
            req = urllib.request.Request(
                url, data=fh.read(), method="PUT",
                headers={"Content-Type": add_media[key]["content_type"],
                         "Content-Length": str(p.stat().st_size)})
            urllib.request.urlopen(req, timeout=1800)

    # The terminal field is `job_state`, and the terminal value is "stopped". There is no `status`
    # key at the top level; polling for one spins for the whole timeout on a job that already ended.
    for _ in range(360):
        j = call(tok, "GET", f"/jobs/{job}")
        if j.get("job_state") in ("stopped", "cancelled", "failed", "error"):
            result = j.get("result", {})
            print("job", j["job_state"], result.get("status"))
            for k, v in sorted(result.get("media_status", {}).items()):
                print(f"    {v.get('status'):8} {v.get('duration_seconds')}  {k}")
            return 0 if result.get("status") == "success" else 1
        time.sleep(5)
    print("job still running:", job)
    return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
