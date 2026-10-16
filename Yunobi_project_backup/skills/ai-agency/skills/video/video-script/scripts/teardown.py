#!/usr/bin/env python3
"""Measure a reference video's edit, in the units this skill already argues in.

Somebody sends a video that works and asks for one like it. The instinct is to watch it and
describe it, which produces adjectives. This produces numbers, and every number it prints has a
rule already written against it somewhere in `video-hooks` or `video-script`:

  runtime, words, wpm      the runtime rules, and the density the read was written at
  the first 30 seconds     the cold open, which `video-hooks` owns
  the first number         video-hooks measured that hits and flops reach it at the same moment
  where the asks land      `video-script` puts one ask in the last 20 seconds; count theirs
  chapters                 the author's own block map, against the eight blocks in the table
  shots per minute         cut rhythm, with --cuts

It does not tell you what to do. It puts the reference on the same axes as the rules, so the two
can be compared instead of admired.

  python3 teardown.py https://youtube.com/watch?v=...        # transcript only, free, no download
  python3 teardown.py <url> --cuts                           # also fetch 360p and detect the cuts
  python3 teardown.py local.mp4 --cuts                       # a file already on disk
  python3 teardown.py <url> --json                           # machine-readable

WHY the video is not downloaded by default: everything except shot rhythm comes from the subtitle
track and the metadata, which yt-dlp fetches without touching a video stream. Asking for --cuts is
asking for a download, and it should be a decision rather than a surprise.
"""

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

# Phrases that mark an ask. Each one is something being requested of the viewer, which is the thing
# `video-script` allows exactly one of, in the last twenty seconds.
# An ask is the creator requesting something of the viewer. A tutorial saying "sign up with
# Google" is narrating a click on screen, not asking, so every pattern here has to name either the
# creator's own destination or an action that only makes sense pointed back at them. Getting this
# wrong inflates the count, and the count is the whole point: this skill allows one ask.
ASK_PATTERNS = [
    (r"\blink (?:is )?(?:in|below|down) the (?:description|comments)\b", "link"),
    (r"\b(?:in|check) the description\b|\bdescription below\b", "link"),
    (r"\bsubscribe\b", "subscribe"),
    (r"\bhit the bell\b|\bring the bell\b", "subscribe"),
    (r"\blike (?:this|the) video\b|\bsmash that like\b|\bleave a like\b", "like"),
    (r"\bcomment below\b|\blet me know in the comments\b|\bdrop a comment\b", "comment"),
    (r"\bbook a call\b|\bschedule a call\b|\bcall with me\b", "call"),
    (r"\bfree (?:training|course|template|guide|resource|community|trial|workshop)\b",
     "lead magnet"),
    (r"\bjoin (?:my|the|our) (?:community|school|skool|program|newsletter|discord)\b", "join"),
    (r"\bsign up (?:using|with|through|via) (?:my|the) link\b", "signup"),
]

# Only a quantity a viewer would register as a number. Bare "two" and "three" are grammar, not
# evidence, and counting them puts the first number in every video inside the first ten seconds.
NUMBER = re.compile(
    r"(?:\$\s?[\d,]+(?:\.\d+)?"
    r"|[\d,]+(?:\.\d+)?\s?(?:%|percent|k\b|x\b|hours?\b|days?\b|weeks?\b|months?\b"
    r"|years?\b|minutes?\b|dollars?\b|clients?\b|times\b)"
    r"|\b[\d,]{2,}(?:\.\d+)?\b"
    r"|\b(?:hundred|thousand|million|billion)\b)", re.I)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def need(tool):
    if not shutil.which(tool):
        sys.exit(f"{tool} not on PATH")


def hms(seconds):
    seconds = int(round(seconds))
    return f"{seconds // 60}:{seconds % 60:02d}"


def parse_vtt(path):
    """VTT cues as (start, end, text), with the rolling auto-caption repeats collapsed.

    YouTube's automatic track repeats the previous line at the top of every cue so the caption can
    scroll. Counting words off it raw roughly doubles them, which would double the wpm and make
    every reference look like it was read at 400 words a minute.
    """
    cues, start, end, buf = [], None, None, []

    def flush():
        if start is None:
            return
        text = " ".join(buf).strip()
        if text:
            cues.append((start, end, text))

    for raw in open(path, encoding="utf-8", errors="replace"):
        line = raw.rstrip("\n")
        m = re.match(r"(\d+:\d+:\d+\.\d+)\s+-->\s+(\d+:\d+:\d+\.\d+)", line)
        if m:
            flush()
            buf = []
            start, end = (secs(m.group(1)), secs(m.group(2)))
            continue
        if not line.strip() or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        buf.append(re.sub(r"<[^>]+>", "", line).strip())
    flush()

    out, seen_tail = [], ""
    for s, e, text in cues:
        # Drop the leading repeat of whatever the last cue ended with.
        if seen_tail and text.startswith(seen_tail):
            text = text[len(seen_tail):].strip()
        if text:
            out.append((s, e, text))
            seen_tail = text
    return out


def secs(stamp):
    h, m, s = stamp.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def fetch(url, workdir, want_video):
    """Metadata, subtitles, and the video stream only when the cuts were asked for.

    Three calls rather than one, because they fail independently. A video with no caption track
    still has a runtime and chapters worth reading, and folding the three together throws all of
    it away on the first error.

    WHY the sub languages are named rather than globbed: `--sub-langs "en.*"` matches every
    machine-translated variant YouTube publishes, which is dozens of separate requests for the same
    read, and YouTube answers the pile with HTTP 429. One English track is the whole job.

    WHY the video call names a player client: the default clients hand back 403 partway through and
    then offer only a 640x266 progressive file. `web_embedded` returns the real DASH ladder.
    """
    need("yt-dlp")
    base = os.path.join(workdir, "ref")
    out = ["-o", base + ".%(ext)s"]

    r = run(["yt-dlp", "--skip-download", "--write-info-json"] + out + [url])
    info = glob.glob(base + "*.info.json")
    if not info:
        sys.exit(f"yt-dlp returned no metadata:\n{(r.stderr or r.stdout)[-800:]}")
    meta = json.load(open(info[0], encoding="utf-8"))

    def pull(langs):
        run(["yt-dlp", "--skip-download", "--write-auto-subs", "--write-subs",
             "--sub-langs", langs, "--sub-format", "vtt",
             "--ignore-errors"] + out + [url])
        return sorted(glob.glob(base + "*.vtt"))

    lang, vtts = "en", pull("en-orig,en,en-US,en-GB")
    if not vtts:
        # A video spoken in another language has a full caption track and no English one. Reading
        # nothing off it reports 0 words and no asks, which is a wrong finding rather than a
        # missing one, so fall back to the language it was actually spoken in.
        native = meta.get("language")
        if not native:
            manual = [k for k in (meta.get("subtitles") or {}) if k != "live_chat"]
            native = manual[0] if manual else None
        if native:
            lang = native.split("-")[0]
            vtts = pull(f"{lang}-orig,{native},{lang}")
    if not vtts:
        print("no caption track in any language", file=sys.stderr)

    video = None
    if want_video:
        run(["yt-dlp", "--extractor-args", "youtube:player_client=web_embedded",
             "-f", "bv*[height<=480]+ba/b[height<=480]/worst"] + out + [url])
        video = next((p for p in glob.glob(base + ".*")
                      if os.path.splitext(p)[1] in (".mp4", ".webm", ".mkv")), None)
    return meta, (vtts[0] if vtts else None), video, lang


def detect_cuts(path, threshold):
    r = run(["ffmpeg", "-v", "info", "-i", path, "-filter:v",
             f"select='gt(scene,{threshold})',metadata=print:file=-", "-an", "-f", "null", "-"])
    return sorted(float(m) for m in re.findall(r"pts_time:([0-9.]+)", r.stdout + r.stderr))


def report(meta, cues, cuts, runtime, args, lang="en"):
    words = sum(len(c[2].split()) for c in cues)
    wpm = words / (runtime / 60) if runtime else 0
    open30 = [c for c in cues if c[0] < 30]
    open_text = " ".join(c[2] for c in open30)

    first_number = next(((c[0], c[2]) for c in cues if NUMBER.search(c[2])), None)

    # One ask spoken across four consecutive cues is one ask. Collapsing a repeat of the same kind
    # inside a window is what separates "he asked three times" from "he asked once, slowly".
    # The patterns are English. On a foreign-language read they match nothing, and "0 asks" would
    # read as a channel that never asks, so the count is withheld instead of reported as zero.
    asks, last_seen = ([] if lang.startswith("en") else None), {}
    for s, _, text in (cues if asks is not None else []):
        low = text.lower()
        for pat, label in ASK_PATTERNS:
            if re.search(pat, low):
                if s - last_seen.get(label, -1e9) < args.ask_window:
                    last_seen[label] = s
                    break
                last_seen[label] = s
                asks.append({"t": s, "pct": (s / runtime * 100) if runtime else 0,
                             "kind": label, "line": text})
                break

    chapters = [{"t": c.get("start_time", 0), "title": c.get("title", "")}
                for c in (meta.get("chapters") or [])]

    shots = None
    if cuts is not None:
        lens = [b - a for a, b in zip([0.0] + cuts, cuts + [runtime]) if b > a]
        lens.sort()
        quarters = []
        for q in range(4):
            lo, hi = runtime * q / 4, runtime * (q + 1) / 4
            n = sum(1 for t in cuts if lo <= t < hi)
            quarters.append(round(n / ((hi - lo) / 60), 1) if hi > lo else 0)
        shots = {
            "cuts": len(cuts),
            "per_minute": round(len(cuts) / (runtime / 60), 1) if runtime else 0,
            "median_shot": round(lens[len(lens) // 2], 2) if lens else 0,
            "longest_shot": round(lens[-1], 1) if lens else 0,
            "per_minute_by_quarter": quarters,
        }

    return {
        "title": meta.get("title"), "channel": meta.get("uploader"),
        "url": meta.get("webpage_url"), "uploaded": meta.get("upload_date"),
        "views": meta.get("view_count"), "runtime_s": round(runtime, 1),
        "words": words, "wpm": round(wpm), "cold_open_30s": open_text,
        "first_number": ({"t": round(first_number[0], 1), "line": first_number[1]}
                         if first_number else None),
        "asks": asks, "chapters": chapters, "shots": shots, "caption_lang": lang,
    }


def render(r):
    L = []
    a = L.append
    a(f"# {r['title']}")
    a("")
    a(f"{r['channel']} · {hms(r['runtime_s'])} · "
      f"{r['views']:,} views · {r['uploaded']}" if r["views"] else
      f"{r['channel']} · {hms(r['runtime_s'])}")
    a(f"<{r['url']}>" if r["url"] else "")
    a("")
    a("## Density")
    a("")
    if r.get("caption_lang", "en") != "en":
        a(f"_Read off the `{r['caption_lang']}` caption track; there is no English one._")
        a("")
    a(f"- **{r['words']:,} words over {hms(r['runtime_s'])}, {r['wpm']} wpm.**")
    a(f"- A body budgeted at 7s a beat would be **~{int(r['runtime_s'] / 7)} beats**. "
      "Compare with the 158-185 the beat budget puts on a winning nineteen minutes.")
    a("")
    a("## The cold open, which video-hooks owns")
    a("")
    if r["cold_open_30s"]:
        a("> " + r["cold_open_30s"])
    else:
        a("_No subtitle cue inside the first 30 seconds._")
    a("")
    if r["first_number"]:
        a(f"First number at **{hms(r['first_number']['t'])}**: "
          f"\"{r['first_number']['line']}\"")
    else:
        a("**No number anywhere in the read.**")
    a("")
    a("## The asks")
    a("")
    if r["asks"] is None:
        a(f"_Not measured: the read is in `{r['caption_lang']}` and the ask patterns are English. "
          "Read the closing minute by hand._")
    elif r["asks"]:
        a("| At | % in | Kind | Line |")
        a("| --- | --- | --- | --- |")
        for k in r["asks"]:
            a(f"| {hms(k['t'])} | {k['pct']:.0f}% | {k['kind']} | {k['line'][:90]} |")
        a("")
        a(f"**{len(r['asks'])} asks.** This skill allows one, in the last twenty seconds.")
    else:
        a("None detected.")
    a("")
    a("## The author's own block map")
    a("")
    if r["chapters"]:
        a("| At | % in | Chapter |")
        a("| --- | --- | --- |")
        for c in r["chapters"]:
            pct = c["t"] / r["runtime_s"] * 100 if r["runtime_s"] else 0
            a(f"| {hms(c['t'])} | {pct:.0f}% | {c['title']} |")
        a("")
        a("Read the shares against the eight-block table before borrowing the shape.")
    else:
        a("_No chapters published._")
    a("")
    a("## Cut rhythm")
    a("")
    s = r["shots"]
    if s:
        a(f"- **{s['cuts']} cuts, {s['per_minute']} a minute.** "
          f"Median shot {s['median_shot']}s, longest {s['longest_shot']}s.")
        a(f"- By quarter, cuts a minute: {', '.join(str(q) for q in s['per_minute_by_quarter'])}. "
          "A rising curve means the edit gets denser as retention gets harder.")
    else:
        a("_Not measured. Pass `--cuts` to fetch 360p and detect them._")
    a("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="a video URL, or a local file")
    ap.add_argument("--cuts", action="store_true",
                    help="also measure shot rhythm (downloads the video at 360p)")
    ap.add_argument("--subs", help="a .vtt already on disk, for a local file")
    ap.add_argument("--scene", type=float, default=0.30, help="cut threshold (default 0.30)")
    ap.add_argument("--ask-window", type=float, default=45.0,
                    help="seconds within which a repeat of the same ask counts once (default 45)")
    ap.add_argument("--out", help="write the report here as well as to stdout")
    ap.add_argument("--json", action="store_true", help="machine-readable")
    args = ap.parse_args()

    need("ffmpeg")
    with tempfile.TemporaryDirectory() as work:
        if os.path.exists(args.source):
            meta = {"title": os.path.basename(args.source), "uploader": "(local file)"}
            vtt, video, lang = args.subs, args.source, "en"
            probe = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                         "-of", "csv=p=0", video])
            meta["duration"] = float(probe.stdout.strip() or 0)
        else:
            meta, vtt, video, lang = fetch(args.source, work, args.cuts)

        runtime = float(meta.get("duration") or 0)
        cues = parse_vtt(vtt) if vtt and os.path.exists(vtt) else []
        if not cues:
            print("no subtitle track found; density and the asks cannot be measured",
                  file=sys.stderr)
        if not runtime and cues:
            runtime = cues[-1][1]

        cuts = None
        if args.cuts:
            if not video or not os.path.exists(video):
                print("--cuts asked for but no video stream was fetched", file=sys.stderr)
            else:
                cuts = detect_cuts(video, args.scene)

        r = report(meta, cues, cuts, runtime, args, lang)

    if args.json:
        print(json.dumps(r, indent=2))
        return
    text = render(r)
    print(text)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        open(args.out, "w", encoding="utf-8").write(text)
        print(f"\nwritten to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
