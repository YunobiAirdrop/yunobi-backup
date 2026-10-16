#!/usr/bin/env python3
"""Rebuild a Descript pasteboard with word ranges cut.

A cut is not a text edit. Each surviving run of words becomes a TAU whose
audioSegment slices the same media at that run's word timings, so the paste
carries the video with it. Paragraph breaks live in the text as "\n", never in
the TAU boundaries - a TAU split to drop a filler must NOT start a paragraph.

usage: recut2.py <cuts.json> [payload.json] [typos.json]
"""
import json, os, re, sys, copy, uuid, unicodedata

D = os.path.expanduser("~/.descript-clip")   # `load()` falls back to the live grab
FILLERS = {"uh","um","uhh","umm","uhm","er","erm","ah","mm","hmm","mhm"}

def norm(w):
    # strip edge apostrophes too: the copied token is "'cause" and the alignment
    # word is "cause", and five of those sink the whole run on the safety check.
    return re.sub(r"^'+|'+$", "", re.sub(r"[^\w']", "", unicodedata.normalize("NFKC", w))).lower()

def is_filler(w):
    """A standalone hesitation, or a truncated fragment like 'e-' / 'aud-'."""
    n = re.sub(r"[^\w'-]", "", unicodedata.normalize("NFKC", w)).lower()
    return n in FILLERS or (len(n) > 1 and n.endswith("-"))

PALETTE = {                      # Descript's own highlight names; alpha 64 is its convention
    "yellow":   ("Yellow",   [245, 200, 120, 64]),
    "red":      ("Red",      [240, 140, 170, 64]),
    "orange":   ("Orange",   [240, 160, 130, 64]),
    "green":    ("Green",    [140, 190, 140, 64]),
    "blue":     ("Blue",     [180, 215, 240, 64]),
    "purple":   ("Purple",   [200, 190, 240, 64]),
    "coral":    ("Coral",    [235, 100,  80, 64]),
    "magenta":  ("Magenta",  [235, 130, 230, 64]),
    "lime":     ("Lime",     [150, 240,  90, 64]),
    "seafoam":  ("Seafoam",  [140, 240, 180, 64]),
    "lavender": ("Lavender", [130, 130, 235, 64]),
    "grey":     ("Grey",     [200, 200, 200, 64]),
    "sand":     ("Sand",     [250, 152,   5, 64]),
}

# The cue legend the editor reads. One colour, one instruction, no overlap.
CUES = {
    "blue":     "B-ROLL - replace the picture with a full-frame clip here",
    "green":    "ON-SCREEN TEXT - caption or list keyed over the face",
    "purple":   "FIGURE - draw this as a diagram or an analogy",
    "orange":   "CTA - dress with a subscribe / like / book-a-call overlay",
    "coral":    "BRAND ASSET - product box, logo, or a shelf asset",
    "yellow":   "EMPHASIS - punch in, this line carries the point",
    "red":      "PROBLEM - needs a retake or a fix before publish",
}

def apply_styles(new, payload, styles):
    """Bold / highlight phrases in the script.

    A range is (location, length) in CHARACTERS of that TAU's own string, so a
    phrase straddling a TAU boundary is styled per TAU. Every highlight id used
    must be registered in the payload's `highlighters` list or it dangles.
    """
    used = {}
    for t in new:
        if t.get("isBlocked"):      # a cue on struck-through text is noise, never an instruction
            continue
        s0 = t["text"]["string"]
        attrs = t["text"].get("attributes") or []
        for sp in styles:
            for m in re.finditer(re.escape(sp["phrase"]), s0):
                if sp.get("bold"):
                    attrs.append({"attribute": {"name": "bold", "value": True},
                                  "range": {"location": m.start(), "length": len(m.group(0))}})
                if sp.get("italic"):
                    attrs.append({"attribute": {"name": "italic", "value": True},
                                  "range": {"location": m.start(), "length": len(m.group(0))}})
                if sp.get("highlight"):
                    hid = "0x:highlight:%s" % sp["highlight"]
                    used[hid] = sp["highlight"]
                    attrs.append({"attribute": {"name": "highlight", "value": hid},
                                  "range": {"location": m.start(), "length": len(m.group(0))}})
        t["text"]["attributes"] = attrs
    hl = payload["data"][0].get("highlighters") or []
    have = {h["id"] for h in hl}
    for hid, key in used.items():
        if hid not in have and key in PALETTE:
            name, color = PALETTE[key]
            hl.append({"id": hid, "name": name, "color": color})
    payload["data"][0]["highlighters"] = hl
    return payload


def load(path=None):
    """The payload, and the word alignment of EVERY media it uses.

    One alignment is not enough. A take recorded in three sittings is three
    media in one composition, and mapping all of its words against the first
    one's alignment agreed on 740 of 5433 tokens (2026-08-25). Each TAU is
    mapped against the alignment of its own media instead.
    """
    p = json.load(open(path or (D + "/current.json")))
    d = p["data"][0]
    refs = {(t.get("audioSegment") or {}).get("mediaRefId") for t in d["copiedTaus"]}
    als = {}
    for m in d["mediaRefsCopyData"]:
        mid = m["mediaRef"]["id"]
        if mid not in refs:
            continue
        a = (m["mediaRef"].get("voiceover") or {}).get("metadata", {}).get("alignment")
        if a:
            als[mid] = a
    if not als:
        sys.exit("no word alignment for the TAUs' media")
    missing = sorted(r for r in refs if r and r not in als)
    if missing:
        names = {m["mediaRef"]["id"]: m["mediaRef"].get("displayName") for m in d["mediaRefsCopyData"]}
        sys.exit("no alignment for media still on the timeline: %s"
                 % ", ".join(str(names.get(r, r)) for r in missing))
    return p, als


def typo_pattern(bad):
    """`\b` only where the key actually has a word edge.

    Wrapping every key in \b makes a fix that ends in punctuation impossible:
    `we are at .` never matched, because \b after the full stop demands a word
    character that is not there (2026-08-25).
    """
    pat = re.escape(bad)
    if bad[:1].isalnum() or bad[:1] == "_":
        pat = r"\b" + pat
    if bad[-1:].isalnum() or bad[-1:] == "_":
        pat = pat + r"\b"
    return pat


def reseg(seg, offset, duration):
    """A rebuilt segment keeps every field of the one it came from.

    Reassembling it from named fields drops whatever Descript put there that we
    do not know about, and it CRASHES on the 10-second end pad Descript appends
    to a composition: that TAU has an audioSegment with no `mediaRefId` at all
    (562-TAU take, 2026-08-25).
    """
    return dict(seg, offset=offset, duration=duration, suppressAutoMerge=False, effects=[])


def copy_tokens(taus):
    """(tau_index, char_start, char_end, word) per token, char offsets tau-local."""
    return [[ti, m.start(), m.end(), m.group(0)]
            for ti, t in enumerate(taus)
            for m in re.finditer(r"\S+", t["text"]["string"])]

def map_to_alignment(toks, als, taus):
    """token -> its alignment WORD, by time.

    Text matching cannot tell twelve takes of one sentence apart; the TAU's own
    offset/duration can. Verify with word agreement, never with a count.

    A punctuation-only token - a bare `...` or `--` left standing by the
    transcriber - has NO alignment word, so it must not be counted in the
    window. Counting it makes the window one word too wide, and on a single-TAU
    take the widener then prepends index -1 and every word after it maps to its
    neighbour: 2127/5970 agreement on a 40-minute take, 2026-08-24.

    The value is the word dict, not an index into one list, because each TAU is
    resolved against the alignment of its own media and those index spaces are
    not comparable.
    """
    m = {}
    for ti, t in enumerate(taus):
        al = als.get((t.get("audioSegment") or {}).get("mediaRefId"))
        if not al:
            continue                      # the silent end pad carries no media
        real = [k for k, tk in enumerate(toks) if tk[0] == ti and norm(tk[3])]
        n = len(real)
        a = t["audioSegment"]; s0, s1 = a["offset"], a["offset"] + a["duration"]
        idx = [j for j, w in enumerate(al)
               if w["endTime"] > s0 + 1e-6 and w["startTime"] < s1 - 1e-6]
        while len(idx) > n:
            head = min(al[idx[0]]["endTime"], s1) - max(al[idx[0]]["startTime"], s0)
            tail = min(al[idx[-1]]["endTime"], s1) - max(al[idx[-1]]["startTime"], s0)
            idx.pop(0 if head <= tail else -1)
        while len(idx) < n and idx:
            b, a2 = idx[0] - 1, idx[-1] + 1
            gb = s0 - al[b]["endTime"] if b >= 0 else 1e9
            ga = al[a2]["startTime"] - s1 if a2 < len(al) else 1e9
            if gb >= 1e9 and ga >= 1e9:
                break                     # nothing left to borrow; a count check would lie
            idx.insert(0, b) if gb <= ga else idx.append(a2)
        idx = _best_window(al, idx, [toks[k][3] for k in real])
        for k in range(min(n, len(idx))):
            m[real[k]] = al[idx[k]]
    return m


def _best_window(al, idx, words):
    """Nudge a time-picked window by a word when the words say it is off by one.

    The widener borrows a neighbour whenever the time window under-selects, and
    it can borrow at the head where the tail was meant: the whole TAU then reads
    one word late. Two TAUs of a three-take composition did exactly that, 24
    tokens between them (2026-08-25). Time chooses the window; the words get the
    final say on where it starts.
    """
    if not idx:
        return idx
    n = len(idx)

    def score(start):
        if start < 0 or start + n > len(al):
            return -1
        return sum(1 for k in range(n) if norm(words[k]) == norm(al[start + k]["word"]))

    here = idx[0]
    best = max((here - 1, here, here + 1), key=lambda c: (score(c), c == here))
    if score(best) <= score(here):
        return idx
    return list(range(best, best + n))


def real_at(t2a, i, n):
    """The first token from i that carries an alignment word."""
    while i < n and i not in t2a:
        i += 1
    return i

def reanchor(components, taus, segmap, new):
    """Move every component onto the TAU that still holds its character position.

    A cut splits one TAU into several, so `tauAnchor.tauId` names a TAU that no
    longer exists. Pointing them all at new[0] - which is what this did until
    2026-08-20 - drops every scene boundary and every marker at the top of the
    script. There were 12 of them on a 65-TAU take: 11 scenes and "Why the move".
    """
    where = {t["id"]: i for i, t in enumerate(taus)}
    out = []
    for c in components:
        a = c.get("tauAnchor") or {}
        ti = where.get(a.get("tauId"))
        if ti is None or ti not in segmap:
            out.append(c); continue
        loc, segs = a.get("location", 0), segmap[ti]
        nid, c0 = segs[-1][0], segs[-1][1]
        for sid, s0, s1 in segs:
            if loc < s1:
                nid, c0 = sid, s0; break
        c = copy.deepcopy(c)
        c["tauAnchor"] = {"tauId": nid, "location": max(0, loc - c0)}
        out.append(c)
    return out


def slide_off_blocked(components, new):
    """A scene or marker whose anchor got ignored moves to the next live TAU.

    Otherwise the card opens on struck-through text - the "And I" false start
    carried a scene boundary, and the cut YouTube-channel take carried another.
    """
    live = [i for i, t in enumerate(new) if not t.get("isBlocked")]
    where = {t["id"]: i for i, t in enumerate(new)}
    for c in components:
        i = where.get((c.get("tauAnchor") or {}).get("tauId"))
        if i is None or not new[i].get("isBlocked"): continue
        nxt = next((j for j in live if j > i), live[-1] if live else None)
        if nxt is not None: c["tauAnchor"] = {"tauId": new[nxt]["id"], "location": 0}
    return components


def add_markers(payload, new, markers):
    """Name the sections. `markers` is [{"phrase": "...", "text": "Why the move"}].

    The phrase is matched against the surviving (unblocked) TAU text, so a marker
    lands on the take that ships, never on an ignored restart.
    """
    d = payload["data"][0]
    comps = d.get("copiedComponents", [])
    have = {c.get("text", "").strip() for c in comps if c["type"] == "markerComponent"}
    for m in markers:
        if m["text"].strip() in have: continue
        hit = next((t for t in new if not t.get("isBlocked") and m["phrase"] in t["text"]["string"]), None)
        if not hit: sys.exit("marker phrase not in any surviving TAU: %r" % m["phrase"])
        loc = hit["text"]["string"].index(m["phrase"])
        comps.append({"type": "markerComponent", "id": str(uuid.uuid4()),
                      "offsetFromBaseTime": 0, "offsetFromAnchor": 0,
                      "tauAnchor": {"tauId": hit["id"], "location": loc},
                      "sortTiebreaker": 0.5, "isBlocked": False,
                      "baseType": "trackComponent", "shortName": "component",
                      "text": m["text"]})
    d["copiedComponents"] = comps
    return payload


def build_ignore(cuts, path=None, fillers=True, typos=None):
    """Mark cuts as Ignored (strikethrough) instead of deleting them.

    An ignored TAU keeps its text AND its audioSegment and sets isBlocked=true.
    Segments stay contiguous, so nothing is destroyed and any word can be
    un-ignored later in the editor.
    """
    p, als = load(path)
    taus = p["data"][0]["copiedTaus"]
    toks = copy_tokens(taus)
    t2a = map_to_alignment(toks, als, taus)
    real = [i for i, t in enumerate(toks) if norm(t[3])]   # a bare "..." has no alignment word
    agree = sum(1 for i in real if i in t2a and norm(toks[i][3]) == norm(t2a[i]["word"]))
    if agree < len(real) - 4:
        sys.exit("mapping unsafe: only %d/%d tokens agree on the word" % (agree, len(real)))
    cuts = list(cuts)
    if fillers:
        cuts += [{"start": i, "end": i + 1, "pass": 1, "reason": "filler", "text": t[3]}
                 for i, t in enumerate(toks) if is_filler(t[3])]
    # cut indices are TOKEN indices, the ones `dscript words` prints. They are NOT
    # alignment indices: the alignment carries words that fall in gaps between TAUs,
    # so the two drift apart (2 words by the end of a 2012-word take, 2026-08-20).
    cut = {x for c in cuts for x in range(c["start"], c["end"])}
    # An Ignore already in the composition must SURVIVE a second pass. Building
    # `blocked` from the new cut list alone un-ignores every earlier cut: on a
    # take already cut to 25:30, an EMPTY cut list rebuilt to 34:41 and handed
    # back nine minutes of struck-through restarts (2026-08-25).
    was = [taus[t[0]].get("isBlocked", False) for t in toks]
    blocked = [was[i] or (i in t2a and i in cut) for i in range(len(toks))]

    new, segmap = [], {}          # segmap: old tau index -> [(new id, char start, char end)]
    for ti, tau in enumerate(taus):
        idx = [i for i, t in enumerate(toks) if t[0] == ti]
        if not idx:
            keep = copy.deepcopy(tau)
            new.append(keep)
            segmap[ti] = [(keep["id"], 0, len(keep["text"]["string"]))]
            continue
        if not any(i in t2a for i in idx):
            # No token here has an alignment word: the 10-second end pad Descript
            # appends, whose text is a zero-width space and whose audioSegment
            # names no media. Carry it through untouched - rebuilding it walks
            # `real_at` off the end of the token list (2026-08-25).
            keep = copy.deepcopy(tau)
            new.append(keep)
            segmap[ti] = [(keep["id"], 0, len(keep["text"]["string"]))]
            continue
        src = tau["text"]["string"]
        segs, start = [], idx[0]
        for a, b in zip(idx, idx[1:] + [None]):
            if b is None or blocked[b] != blocked[a]:
                segs.append((start, a)); start = b
        for k, (a, b) in enumerate(segs):
            c0 = 0 if k == 0 else toks[a][1]
            c1 = len(src) if k == len(segs) - 1 else toks[segs[k+1][0]][1]
            ra = real_at(t2a, a, len(toks))
            # The FIRST segment keeps the TAU's own offset, the way the last one
            # keeps its end. Taking the first word's startTime instead throws away
            # the handle the previous edit left: a uniform 0.400s off the front of
            # 30 TAUs, which is exactly where the breath lives, and it made an
            # empty cut list a 10.9s edit (2026-08-25).
            t0 = (tau["audioSegment"]["offset"] if k == 0
                  else t2a[ra]["startTime"] if ra in t2a else tau["audioSegment"]["offset"])
            rn = real_at(t2a, segs[k+1][0], len(toks)) if k < len(segs) - 1 else None
            t1 = (t2a[rn]["startTime"] if rn is not None and rn in t2a
                  else tau["audioSegment"]["offset"] + tau["audioSegment"]["duration"])
            seg = tau["audioSegment"]
            nid = str(uuid.uuid4())
            segmap.setdefault(ti, []).append((nid, c0, c1))
            new.append({"id": nid,
                        "text": {"string": src[c0:c1], "attributes": []},
                        "audioSegment": reseg(seg, t0, max(t1 - t0, 0.01)),
                        "ignoreAlignment": False, "isBlocked": bool(blocked[a])})
    for t in new:   # "th-them" -> "them": a stutter the transcriber glued together
        t["text"]["string"] = re.sub(r"\b(\w{1,3})-(\1\w*)\b", r"\2", t["text"]["string"], flags=re.I)
    for bad, good in (typos or {}).items():
        for t in new:
            t["text"]["string"] = re.sub(typo_pattern(bad), good, t["text"]["string"])
    out = copy.deepcopy(p)
    d = out["data"][0]
    comps = reanchor(d.get("copiedComponents", []), taus, segmap, new)
    d["copiedComponents"] = slide_off_blocked(comps, new)
    d["copiedTaus"] = new
    out["text"] = ["".join(t["text"]["string"] for t in new)]
    return out, new, toks, blocked


def build(cuts, path=None, fillers=True, typos=None):
    p, als = load(path)
    taus = p["data"][0]["copiedTaus"]
    toks = copy_tokens(taus)
    t2a = map_to_alignment(toks, als, taus)
    real = [i for i, t in enumerate(toks) if norm(t[3])]   # a bare "..." has no alignment word
    agree = sum(1 for i in real if i in t2a and norm(toks[i][3]) == norm(t2a[i]["word"]))
    if agree < len(real) - 4:
        sys.exit("mapping unsafe: only %d/%d tokens agree on the word" % (agree, len(real)))
    cuts = list(cuts)
    if fillers:
        cuts += [{"start": i, "end": i + 1, "pass": 1, "reason": "filler", "text": t[3]}
                 for i, t in enumerate(toks) if is_filler(t[3])]
    # cut indices are TOKEN indices, the ones `dscript words` prints. They are NOT
    # alignment indices: the alignment carries words that fall in gaps between TAUs,
    # so the two drift apart (2 words by the end of a 2012-word take, 2026-08-20).
    cut = {x for c in cuts for x in range(c["start"], c["end"])}
    keep = [i for i in range(len(toks)) if i in t2a and i not in cut]
    runs, cur = [], []
    for i in keep:
        if cur and toks[i][0] == toks[cur[-1]][0] and i == cur[-1] + 1: cur.append(i)
        else:
            if cur: runs.append(cur)
            cur = [i]
    if cur: runs.append(cur)

    new, segmap = [], {}
    for r in runs:
        ti = toks[r[0]][0]
        src = taus[ti]["text"]["string"]
        body = src[toks[r[0]][1]:toks[r[-1]][2]]
        # separator carries the paragraph break; a filler-split keeps one line
        a = r[0]
        if a > 0 and toks[a - 1][0] == ti:
            ws = src[toks[a - 1][2]:toks[a][1]]
        else:
            ws = "\n" if new else ""
        starts_para = "\n" in ws or not new
        text = ("\n" if "\n" in ws else (" " if new else "")) + body
        if starts_para:
            for k, ch in enumerate(text):
                if ch.isalpha():
                    if ch.islower(): text = text[:k] + ch.upper() + text[k+1:]
                    break
        rs, re_ = real_at(t2a, r[0], len(toks)), r[-1]
        while re_ > r[0] and re_ not in t2a: re_ -= 1
        if rs not in t2a or re_ not in t2a: continue
        s = t2a[rs]["startTime"]; e = t2a[re_]["endTime"]
        if e - s <= 0.01: continue
        seg = taus[ti]["audioSegment"]
        nid = str(uuid.uuid4())
        segmap.setdefault(ti, []).append((nid, toks[r[0]][1], toks[r[-1]][2]))
        new.append({"id": nid,
                    "text": {"string": text, "attributes": []},
                    "audioSegment": reseg(seg, s, e - s),
                    "ignoreAlignment": False, "isBlocked": False})
    for t in new:   # "th-them" -> "them": a stutter the transcriber glued together
        t["text"]["string"] = re.sub(r"\b(\w{1,3})-(\1\w*)\b", r"\2", t["text"]["string"], flags=re.I)
    for bad, good in (typos or {}).items():
        for t in new:
            t["text"]["string"] = re.sub(typo_pattern(bad), good, t["text"]["string"])
    out = copy.deepcopy(p)
    d = out["data"][0]
    for ti in range(len(taus)):      # a TAU deleted whole hands its anchors to the next survivor
        if ti not in segmap:
            nxt = next((j for j in range(ti + 1, len(taus)) if j in segmap), None)
            if nxt is not None: segmap[ti] = [(segmap[nxt][0][0], 0, 1 << 30)]
    d["copiedComponents"] = reanchor(d.get("copiedComponents", []), taus, segmap, new)
    d["copiedTaus"] = new
    d["storyboardCues"] = []
    out["text"] = ["".join(t["text"]["string"] for t in new)]
    return out, new, toks, keep

if __name__ == "__main__":
    cuts = json.load(open(sys.argv[1]))
    src = sys.argv[2] if len(sys.argv) > 2 else None
    typos = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else None
    styles = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else None
    out, new, toks, keep = build_ignore(cuts, src, typos=typos)   # Ignore, never delete
    if styles: out = apply_styles(new, out, styles)
    json.dump(out, open(D + "/recut_payload.json", "w"))
    open(D + "/recut_preview.txt", "w").write(out["text"][0])
    p0, _ = load(src)
    before = sum(t["audioSegment"]["duration"] for t in p0["data"][0]["copiedTaus"])
    plays = sum(t["audioSegment"]["duration"] for t in new if not t["isBlocked"])
    print("cuts %d | taus %d -> %d (%d blocked) | %.1fs -> plays %.1fs (%d:%02d)"
          % (len(cuts), len(p0["data"][0]["copiedTaus"]), len(new),
             sum(1 for t in new if t["isBlocked"]), before, plays, plays//60, plays%60))
