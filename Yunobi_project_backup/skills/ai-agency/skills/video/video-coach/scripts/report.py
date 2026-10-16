#!/usr/bin/env python3
"""Render the coaching page: one self-contained HTML file, opened in Dia.

Input is a findings JSON built by the skill. Shape:

{
  "title": "...", "slug": "...", "date": "2026-08-19",
  "conceptId": "...", "compositionId": "...",
  "prior":   {"oneThing": "...", "fixed": true, "evidence": "..."} | null,
  "writing": {"score": 3.0, "priorScore": null, "note": "...",
              "lines": [{"id":"W1","name":"...","points":0,"quote":"..."}]},
  "oneThing": {"habit": "...", "costSeconds": 182, "evidence": "...", "instead": "..."},
  "numbers": [{"label":"Delivered words","value":"3,410","target":"3,600-4,200","verdict":"under"}],
  "blocks":  [{"planned":"The stakes","delivered":"yes","verdict":"delivered","note":"..."}],
  "cost":    [{"what":"...","seconds":41,"where":"block 19"}],
  "checks":  [{"id":"D1","name":"...","verdict":"pass","note":"...","source":"..."}],
  "alsoSeen":["...", "..."]
}

Every list may be empty. An empty `cost` prints "nothing", which is a good
result and has to look like one rather than like a rendering failure.

`points` may be null for a line with nothing to quote. It renders as unscored and
is subtracted from the denominator so the total never silently reads as a zero.
"""
import argparse
import html
import json

# Palette mirrors the brand's own design tokens, which are the colour SSOT.
# Inlined because this file has to open from disk with no network.
CSS = """
:root{
  --ink:oklch(0.12 0.04 258); --night:oklch(0.18 0.05 262); --veil:oklch(0.28 0.06 264);
  --dusk:oklch(0.22 0.05 262); --cream:oklch(0.97 0.01 55); --linen:oklch(0.985 0.003 55);
  --mist:oklch(0.9 0.006 55); --indigo:oklch(0.5 0.2 272); --indigo-light:oklch(0.68 0.16 272);
  --sand:oklch(0.78 0.08 40); --terra:oklch(0.65 0.2 30);
  --bg:var(--linen); --surface:#fff; --line:var(--mist);
  --text:oklch(0.15 0 0); --muted:oklch(0.45 0 0); --accent:var(--indigo);
}
@media (prefers-color-scheme:dark){:root{
  --bg:var(--ink); --surface:var(--night); --line:var(--veil);
  --text:var(--cream); --muted:oklch(0.72 0.01 55); --accent:var(--indigo-light);
}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);
  font:16px/1.6 "Satoshi",system-ui,-apple-system,sans-serif;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:56rem;margin:0 auto;padding:4rem 1.5rem 6rem}
h1{font:600 2rem/1.15 "Manrope",system-ui,sans-serif;margin:0 0 .25rem;letter-spacing:-.02em}
h2{font:600 1.05rem/1.3 "Manrope",system-ui,sans-serif;margin:3rem 0 .75rem;
  letter-spacing:.02em;text-transform:uppercase;color:var(--muted);font-size:.8rem}
.meta{color:var(--muted);font-size:.875rem;margin:0 0 2.5rem}
.meta code{font:.8rem/1 "Space Grotesk",ui-monospace,monospace;color:var(--muted)}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:1.5rem}
.prior{border-left:3px solid var(--accent)}
.prior.miss{border-left-color:var(--terra)}
.one{border-left:3px solid var(--terra);padding:1.75rem}
.one .habit{font:600 1.35rem/1.3 "Manrope",system-ui,sans-serif;margin:0 0 .75rem;letter-spacing:-.01em}
.one .cost{font:.8rem/1 "Space Grotesk",ui-monospace,monospace;color:var(--terra);
  text-transform:uppercase;letter-spacing:.08em;margin:0 0 1rem}
.one p{margin:.5rem 0}
.one .instead{margin-top:1rem;padding-top:1rem;border-top:1px solid var(--line)}
.score{display:flex;gap:1.5rem;align-items:baseline;flex-wrap:wrap;margin-bottom:1.25rem}
.score .n{font:600 3.25rem/1 "Manrope",system-ui,sans-serif;letter-spacing:-.03em}
.score .of{font:.85rem/1 "Space Grotesk",ui-monospace,monospace;color:var(--muted)}
.score .delta{font:.85rem/1 "Space Grotesk",ui-monospace,monospace;color:var(--muted)}
.pts{font:600 .8rem/1 "Space Grotesk",ui-monospace,monospace;white-space:nowrap}
.pts.p1{color:var(--accent)} .pts.p0{color:var(--terra)} .pts.ph{color:var(--muted)}
q{quotes:"\201C" "\201D";color:var(--muted);font-style:italic}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--surface)}
table{border-collapse:collapse;width:100%;font-size:.9rem}
th{text-align:left;font:600 .72rem/1 "Space Grotesk",ui-monospace,monospace;
  text-transform:uppercase;letter-spacing:.06em;color:var(--muted);
  padding:.85rem 1rem;border-bottom:1px solid var(--line);white-space:nowrap}
td{padding:.85rem 1rem;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:none}
.tag{display:inline-block;font:600 .7rem/1 "Space Grotesk",ui-monospace,monospace;
  text-transform:uppercase;letter-spacing:.05em;padding:.3rem .5rem;border-radius:5px;
  border:1px solid var(--line);color:var(--muted);white-space:nowrap}
.tag.pass,.tag.delivered,.tag.ok{color:var(--accent);border-color:var(--accent)}
.tag.fail,.tag.dropped,.tag.over,.tag.under{color:var(--terra);border-color:var(--terra)}
.tag.na,.tag.added,.tag.reordered,.tag.thinned{color:var(--muted)}
ul.plain{list-style:none;padding:0;margin:0}
ul.plain li{padding:.6rem 0;border-bottom:1px solid var(--line);font-size:.925rem}
ul.plain li:last-child{border-bottom:none}
.none{color:var(--muted);font-style:italic}
.src{display:block;font:.72rem/1.4 "Space Grotesk",ui-monospace,monospace;color:var(--muted);margin-top:.35rem}
"""


def e(v):
    return html.escape(str(v if v is not None else ""))


def tag(v):
    return f'<span class="tag {e(str(v).lower())}">{e(v)}</span>'


def table(headers, rows):
    if not rows:
        return '<p class="none">nothing</p>'
    head = "".join(f"<th>{e(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="scroll"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def build(d):
    parts = []
    parts.append(f"<h1>{e(d['title'])}</h1>")
    parts.append(
        f'<p class="meta">Recording review, {e(d.get("date",""))} &middot; '
        f'concept <code>{e(d.get("conceptId",""))}</code> &middot; '
        f'composition <code>{e(d.get("compositionId",""))}</code></p>')

    prior = d.get("prior")
    if prior:
        ok = bool(prior.get("fixed"))
        parts.append("<h2>Last time I said</h2>")
        parts.append(
            f'<div class="card prior {"" if ok else "miss"}">'
            f'<p><strong>{e(prior["oneThing"])}</strong></p>'
            f'<p>{tag("fixed" if ok else "not fixed")} {e(prior.get("evidence",""))}</p></div>')

    wr = d.get("writing")
    if wr:
        lines = wr.get("lines", [])
        scored = [l for l in lines if l.get("points") is not None]
        denom = len(scored)
        total = wr.get("score")
        if total is None:
            total = sum(l["points"] for l in scored)
        prev = wr.get("priorScore")
        # Always one decimal: 3.0 and 3.5 are different recordings and a score
        # printed as "3" reads as a rounded impression rather than a measurement.
        delta = ("first recording scored" if prev is None
                 else f"last time {prev:.1f} / 10, {total - prev:+.1f}")
        parts.append("<h2>Writing</h2>")
        parts.append(
            f'<div class="card"><div class="score">'
            f'<span class="n">{total:.1f}</span>'
            f'<span class="of">out of 10, on {denom} scored lines</span>'
            f'<span class="delta">{e(delta)}</span></div>'
            + (f'<p>{e(wr["note"])}</p>' if wr.get("note") else "") + "</div>")

        def pt(v):
            if v is None:
                return '<span class="pts ph">unscored</span>'
            cls = "p1" if v == 1 else ("p0" if v == 0 else "ph")
            return f'<span class="pts {cls}">{v:g}</span>'

        parts.append(table(
            ["", "Line", "", "What earned or lost it"],
            [[f'<code>{e(l["id"])}</code>', e(l["name"]), pt(l.get("points")),
              (f'<q>{e(l["quote"])}</q>' if l.get("quote") else '<span class="none">nothing to quote</span>')]
             for l in lines]))

    one = d["oneThing"]
    parts.append("<h2>The one thing</h2>")
    cost = f'costs {one["costSeconds"]}s in this take' if one.get("costSeconds") else "measured below"
    parts.append(
        f'<div class="card one"><p class="cost">{e(cost)}</p>'
        f'<p class="habit">{e(one["habit"])}</p>'
        f'<p>{e(one.get("evidence",""))}</p>'
        f'<p class="instead"><strong>Instead:</strong> {e(one.get("instead",""))}</p></div>')

    parts.append("<h2>The take in numbers</h2>")
    parts.append(table(
        ["", "Measured", "Target", ""],
        [[e(n["label"]), f'<strong>{e(n["value"])}</strong>', e(n.get("target", "")),
          tag(n["verdict"]) if n.get("verdict") else ""] for n in d.get("numbers", [])]))

    parts.append("<h2>Plan against take</h2>")
    parts.append(table(
        ["Planned block", "Verdict", "Note"],
        [[e(b["planned"]), tag(b["verdict"]), e(b.get("note", ""))] for b in d.get("blocks", [])]))

    parts.append("<h2>What the drift cost</h2>")
    parts.append(table(
        ["What was lost", "Seconds", "Where"],
        [[e(c["what"]), e(c.get("seconds", "")), e(c.get("where", ""))] for c in d.get("cost", [])]))

    parts.append("<h2>Against the strategy</h2>")
    parts.append(table(
        ["", "Check", "Verdict", "Note"],
        [[f'<code>{e(c["id"])}</code>', e(c["name"]), tag(c["verdict"]),
          e(c.get("note", "")) + (f'<span class="src">{e(c["source"])}</span>' if c.get("source") else "")]
         for c in d.get("checks", [])]))

    parts.append("<h2>Also seen</h2>")
    seen = d.get("alsoSeen", [])
    parts.append("<ul class='plain'>" + "".join(f"<li>{e(s)}</li>" for s in seen) + "</ul>"
                 if seen else '<p class="none">nothing</p>')

    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{e(d["title"])} &middot; recording review</title>'
            f"<style>{CSS}</style></head><body><main class='wrap'>"
            + "".join(parts) + "</main></body></html>")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("findings")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args()
    d = json.load(open(args.findings))
    open(args.out, "w").write(build(d))
    print(args.out)


if __name__ == "__main__":
    main()
