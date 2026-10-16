#!/usr/bin/env python3
"""
Write the direction board: two or three ways a video could look, side by side, as a local page.

WHY this exists: a twenty-clip set was designed, built, rendered and imported before the owner saw a
frame of it, and the verdict was that all twenty were too complex and looked amateur. By then the
only honest thing left to say was that it was too late. The gate has to cost a minute or it will be
skipped again, so this takes a small manifest and writes the page.

    python3 directions.py board.json out/directions.html

board.json:
{
  "video": "Why Your Agency Hits the Ops Ceiling",
  "beat": "\"Your best month is the one where your delivery breaks.\"",
  "now": {"still": "out/dir/today.png", "note": "What the set looks like today, and why it is here."},
  "directions": [
    {"name": "Two marks",
     "still": "out/dir/two-marks.png",
     "clip": "out/dir/two-marks.mp4",
     "commits": "One shape and one line. The whole video is a count against a limit.",
     "gives_up": "Cannot show structure. Every beat about arrangement goes to his face."}
  ]
}

`clip` is optional and is the same beat moving: an mp4 the panel plays in place of the still, with
the still as its poster. Add it whenever the direction is about motion rather than about a frame -
an overlay judged on a still is judged on the one thing it is not. Both are embedded as data URIs,
so the page is self-contained and can be moved anywhere.
"""
import base64
import html
import json
import mimetypes
import os
import sys

# Fallback look, used when no house sheet sits beside the page. A `_playground.css` next to the
# board, if there is one, loads after this and wins.
DEFAULTS = """
:root { --void:#0b0d12; --surface:#141821; --line:#262b38; --text:#e8eaf0; --text-dim:#8b93a7;
  --accent:#7c6cf0; --radius-lg:12px; color-scheme:dark; }
body { margin:0; background:var(--void); color:var(--text);
  font:16px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
"""

CSS = """
/* The page's own grid and nothing else.
 *
 * WHY the grid rules carry no colour of their own: colour and type come from `:root` variables,
 * so a house stylesheet linked after the defaults below can restyle the whole board without
 * touching this file. A page sizes its own grid; colour and type belong to the sheet. */
* { box-sizing: border-box; }
header { padding:56px 48px 28px; border-bottom:1px solid var(--line); }
h1 { margin:0 0 6px; font-size:26px; font-weight:600; letter-spacing:-0.01em; }
.beat { color:var(--text-dim); font-size:15px; }
.note { max-width:70ch; margin:22px 48px 0; color:var(--text-dim); font-size:14px; }
main { display:grid; gap:28px; padding:32px 48px 72px;
  grid-template-columns:repeat(auto-fit,minmax(420px,1fr)); }
figure { margin:0; background:var(--surface); border:1px solid var(--line);
  border-radius:var(--radius-lg); overflow:hidden; }
/* The clip is the one place a board is allowed a hard black: it is the letterbox behind a 16:9
   render, not a surface, and any token here would tint the frame it sits behind. */
figure img, figure video { display:block; width:100%; height:auto; background:var(--void); }
figcaption { padding:18px 20px 20px; }
.name { font-size:17px; font-weight:600; margin-bottom:10px; }
.name span { color:var(--accent); font-variant-numeric:tabular-nums; margin-right:8px; }
/* The panel for what ships today. It is full width and it is not numbered, because a board that
   numbers it alongside the options reads as a four-way choice and one of the four is the thing
   being replaced. Seeing it is the point: the gate got skipped on an earlier video because nobody put the
   current look beside anything. */
.now { margin:32px 48px 0; max-width:760px; border:1px solid var(--line);
  border-radius:var(--radius-lg); overflow:hidden; background:var(--surface); }
.now img { display:block; width:100%; height:auto; background:var(--void); }
.now figcaption { padding:18px 20px 20px; }
.now .name { color:var(--text-dim); }
dl { margin:0; display:grid; grid-template-columns:auto 1fr; gap:4px 12px; font-size:14px; }
dt { color:var(--text-dim); white-space:nowrap; }
dd { margin:0; }
footer { padding:0 48px 64px; color:var(--text-dim); font-size:14px; max-width:70ch; }
"""


def embed(still: str, base_dir: str) -> str:
    """A still or a clip as a data: URI, resolved against the MANIFEST's directory.

    WHY a data URI and not a path: this page can end up as a symlink in a shared folder, and a browser
    resolves a relative src against the symlink rather than the target. A <base> fixed that and left
    a worse bug standing - the path itself was built with `os.path.relpath(still)`, which is relative
    to whatever directory the process happened to start in. Run from another directory, a board written
    into a project's out folder came out pointing at `../../../../../elsewhere/dirA.png` and every
    panel rendered as a broken image on the one page that matters. Embedding removes the whole class:
    no cwd, no base, no symlink, and no file:// subresource policy to satisfy.
    """
    path = still if os.path.isabs(still) else os.path.join(base_dir, still)
    if not os.path.exists(path):
        sys.exit("still not found: %s (resolved from the manifest's directory)" % path)
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return "data:%s;base64,%s" % (mime, base64.b64encode(open(path, "rb").read()).decode())


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    outdir = os.path.dirname(os.path.abspath(out))
    dirs = spec["directions"]
    if not 2 <= len(dirs) <= 3:
        sys.exit("Two or three directions. One is not a choice and four is a survey.")

    cards = []
    for i, d in enumerate(dirs, 1):
        base = os.path.dirname(os.path.abspath(sys.argv[1]))
        rel = embed(d["still"], base)
        # WHY the clip is muted and autoplays: a board with three play buttons is three decisions
        # before the one being asked for. Controls stay on so a beat can be scrubbed.
        media = (
            f'<video src="{html.escape(embed(d["clip"], base))}" poster="{html.escape(rel)}"'
            ' autoplay loop muted playsinline controls></video>'
            if d.get("clip")
            else f'<img src="{html.escape(rel)}" alt="{html.escape(d["name"])}">'
        )
        cards.append(f"""  <figure>
    {media}
    <figcaption>
      <div class="name"><span>{i}</span>{html.escape(d['name'])}</div>
      <dl>
        <dt>Commits to</dt><dd>{html.escape(d['commits'])}</dd>
        <dt>Gives up</dt><dd>{html.escape(d['gives_up'])}</dd>
      </dl>
    </figcaption>
  </figure>""")

    now = ""
    if spec.get("now"):
        n = spec["now"]
        src = embed(n["still"], os.path.dirname(os.path.abspath(sys.argv[1])))
        now = (f'<figure class="now"><img src="{html.escape(src)}" alt="today">'
               f'<figcaption><div class="name">What ships today</div>'
               f'<div class="beat">{html.escape(n.get("note", ""))}</div></figcaption></figure>')

    page = f"""<!doctype html>
<meta charset="utf-8">
<title>Directions - {html.escape(spec['video'])}</title>
<style>{DEFAULTS}</style>
<link rel="stylesheet" href="_playground.css">
<style>{CSS}</style>
<header>
  <h1>{html.escape(spec['video'])} - direction</h1>
  <div class="beat">Same beat in all of them: {html.escape(spec['beat'])}</div>
</header>
<p class="note">Nothing is built until one of these is picked. They are not three designs of one
beat, they are three ways the whole video looks, and they disagree on purpose.</p>
{now}
<main>
{chr(10).join(cards)}
</main>
<footer>Pick one, or say what to change about one. The plan, the beats and every clip follow from
this answer, so it is worth thirty seconds now rather than a rebuild later.</footer>
"""
    os.makedirs(outdir, exist_ok=True)
    with open(out, "w") as f:
        f.write(page)
    print(os.path.abspath(out))


if __name__ == "__main__":
    main()
