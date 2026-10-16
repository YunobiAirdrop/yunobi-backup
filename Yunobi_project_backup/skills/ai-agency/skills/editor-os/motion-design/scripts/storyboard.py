#!/usr/bin/env python3
"""Write a keyframe storyboard: every beat as three stills, before a single clip is built.

WHY THIS EXISTS: `directions.py` answers "what does this video look like" with one still. It cannot
answer "does this beat carry the idea", because that is a question about change over time and one
frame has none. A treatment written as prose cannot answer it either - The author asked for the visuals
before deciding, and he was right: a beat that reads fine as a sentence ("the loop widens") is the
same sentence whether the frame earns it or not.

So this sits between the direction gate and `plan.md`: the argument, drawn, at three moments per
beat, cheap enough to throw away.

WHY INLINE SVG RATHER THAN RENDERED STILLS: the board can end up as a symlink in
a shared folder, and a browser resolves a relative `<img>` against the symlink's own
directory rather than the target's - the bug `directions.py` had to grow a `<base>` for. An inline
panel cannot 404. It also stays crisp at any zoom, which is what a review actually does, and it
costs no Chrome round-trip per frame.

WHY THE PANELS ARE SVG AND NOT REMOTION: nothing here is built yet. A Remotion composition per
candidate beat is an afternoon and the whole point of the gate is that it costs minutes. These
panels are drawings of an intention; the clip is the artefact.

    storyboard.py board.json out.html

board.json:
{
  "title": "Three pillars",
  "world": "One sentence on the world and the motif every beat inherits.",
  "flags": [{"tone": "warn|idea", "html": "Something to fix before anything is built."}],
  "beats": [
    {"rung": "2 · structure",
     "line": "The sentence this beat serves, verbatim.",
     "keyframes": [{"t": "0:00.0", "svg": "<circle .../>", "caption": "What changed."}]}
  ]
}

`svg` is the BODY of a 960x540 viewBox; the ground, the defs and the filters are supplied. Compose it
with the helpers below (`disc`, `bar`, `ring`, `lab`) from a python manifest, or paste raw SVG.

**Draw order is z-order and it is the commonest fault.** A ring written after the discs it connects
is drawn on top of them and reads as a circle laid over two circles rather than a circuit with two
stations. Connectors first, then the things they connect.

**No type in a panel, and nothing drawn that exists.** The read says the words, so a frame that sets
them competes with the voice for one channel and comprehension drops - the redundancy rule applies to
a keyframe exactly as it does to the clip. And a rectangle standing in for a real screen is a fiction
inside a document somebody is deciding from: capture the screen. Inline it with an `<image>` whose
href is a data URI, the way a captured real list is inlined in a manifest.
"""
import json, os, sys

INK = "#0b0d14"; DIM = "#1c2130"; EDGE = "#2b3145"; TEXT = "#e9e6e1"
MUTED = "#7f8598"; ACC = "#7c6cf0"; ACCL = "#a99bff"
W, H = 960, 540


# --- panel helpers: compose a body, never a whole file ---------------------------------------------

def lab(x, y, t, fill=MUTED, size=13, anchor="middle"):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" text-anchor="{anchor}" '
            f'font-family="ui-sans-serif,-apple-system,system-ui" letter-spacing="2.4">{t}</text>')


def disc(cx, cy, r=56, fill=DIM, stroke=EDGE, w=2, extra=""):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" {extra}/>'


def bar(x, y, w_, h_, fill=DIM, stroke=EDGE, sw=2, extra=""):
    return (f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="10" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def ring(cx, cy, r, stroke=ACC, w=3):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{stroke}" stroke-width="{w}"/>'


def arc(x1, y1, r, x2, y2, stroke=ACC, w=3, sweep=1, marker=None):
    m = f' marker-end="url(#{marker})"' if marker else ""
    return (f'<path d="M{x1} {y1} A {r} {r} 0 0 {sweep} {x2} {y2}" fill="none" '
            f'stroke="{stroke}" stroke-width="{w}"{m}/>')


# --- the page ---------------------------------------------------------------------------------------

CSS = """
:root{--ink:#0b0d14;--line:#232838;--text:#e9e6e1;--dim:#8b90a3;--acc:#7c6cf0}
*{box-sizing:border-box}body{margin:0;background:var(--ink);color:var(--text);
 font:16px/1.6 ui-sans-serif,-apple-system,"SF Pro Text",system-ui}
header{padding:52px 44px 22px;border-bottom:1px solid var(--line)}
h1{margin:0 0 6px;font-size:26px;font-weight:600;letter-spacing:-.01em}
.sub{color:var(--dim);font-size:15px;max-width:80ch}
.flag{margin:24px 44px 0;max-width:82ch;padding:16px 20px;border:1px solid #e08a5a;border-radius:8px;
 background:rgba(224,138,90,.06);font-size:14.5px}
.flag b{color:#e08a5a}
.flag.idea{border-color:var(--acc);background:rgba(124,108,240,.07)}.flag.idea b{color:#b3a9ff}
main{padding:26px 44px 70px}
section{margin:34px 0 0;border-top:1px solid var(--line);padding-top:22px}
.bhead{display:flex;gap:16px;align-items:baseline;margin-bottom:14px}
.line{margin:0;font-size:18px;line-height:1.45}.line em{color:#b3a9ff;font-style:normal}
.rung{flex:none;padding:3px 10px;border-radius:99px;font-size:12px;white-space:nowrap;
 background:rgba(124,108,240,.16);color:#b3a9ff;border:1px solid rgba(124,108,240,.35)}
.strip{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
figure{margin:0}
.frame{border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#0b0d14;line-height:0}
.kf{width:100%;height:auto;display:block}
figcaption{color:var(--dim);font-size:13.5px;line-height:1.5;padding:9px 2px 0}
figcaption b{display:block;color:var(--text);font-variant-numeric:tabular-nums;font-size:12.5px;
 letter-spacing:.04em;margin-bottom:3px}
@media (max-width:1100px){.strip{grid-template-columns:1fr}}
"""


def svg(i, body):
    """One panel. The ground, the glow filter and the arrowhead come free, keyed per panel so two
    panels on one page cannot share an id."""
    return (f'<svg viewBox="0 0 {W} {H}" class="kf" role="img"><defs>'
            f'<filter id="g{i}" x="-60%" y="-60%" width="220%" height="220%">'
            f'<feGaussianBlur stdDeviation="14" result="b"/><feMerge><feMergeNode in="b"/>'
            f'<feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'<marker id="a{i}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
            f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{ACC}"/></marker></defs>'
            f'<rect width="{W}" height="{H}" fill="{INK}"/>{body}</svg>')


def build(spec):
    flags = "".join(
        f'<div class="flag {f.get("tone","warn") if f.get("tone")!="warn" else ""}">{f["html"]}</div>'
        for f in spec.get("flags", []))
    n, out = 0, []
    for b in spec["beats"]:
        cells = []
        for k in b["keyframes"]:
            body = k["svg"].replace("{i}", str(n))
            cells.append(f'<figure><div class="frame">{svg(n, body)}</div>'
                         f'<figcaption><b>{k["t"]}</b>{k["caption"]}</figcaption></figure>')
            n += 1
        out.append(f'<section><div class="bhead"><span class="rung">{b["rung"]}</span>'
                   f'<p class="line">{b["line"]}</p></div>'
                   f'<div class="strip">{"".join(cells)}</div></section>')
    return (f'<!doctype html><meta charset="utf-8"><title>{spec["title"]} - storyboard</title>'
            f'<style>{CSS}</style><header><h1>{spec["title"]} - storyboard</h1>'
            f'<div class="sub">{spec.get("world","")}</div></header>{flags}'
            f'<main>{"".join(out)}</main>')


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    open(out, "w").write(build(spec))
    total = sum(len(b["keyframes"]) for b in spec["beats"])
    print("%s  %d beats, %d keyframes" % (out, len(spec["beats"]), total))


if __name__ == "__main__":
    main()
