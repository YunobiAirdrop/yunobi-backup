#!/usr/bin/env python3
"""Resolve a phrase cut list into the token-index cut list `dscript apply` wants.

A needle written as token indices is unauditable and drifts by one the moment
anything upstream changes. Write it as the words themselves instead:

    [{"text": "I can bet you remember the first call ... ever la...",
      "nth": 1, "pass": 1, "reason": "restart"}]

`nth` (1-based) picks the occurrence when a phrase repeats; omit it and the
phrase must be unique or this refuses to resolve. Output is the cuts.json that
`dscript apply` reads, with the resolved words echoed for the eye.

usage: resolve.py phrases.json [cuts.json]
"""
import json, os, re, sys, unicodedata

HOME = os.path.expanduser("~/.descript-clip")

def norm(w):
    return re.sub(r"^'+|'+$", "", re.sub(r"[^\w']", "", unicodedata.normalize("NFKC", w))).lower()

def load_tokens():
    p = json.load(open(os.path.join(HOME, "current.json")))
    text = "".join(t["text"]["string"] for t in p["data"][0]["copiedTaus"])
    return re.findall(r"\S+", text)

def run(nt, i, want):
    """Consume `want` from position i, stepping over punctuation-only tokens.

    A bare "..." or "--" is its own token in the script and normalises to
    nothing, so a phrase written as prose has to be allowed to skip it - and the
    span still has to END on a real word, or the cut takes the next one's space.
    """
    k = i
    for w in want:
        while k < len(nt) and not nt[k]:
            k += 1
        if k >= len(nt) or nt[k] != w:
            return None
        k += 1
    return k

def back(nt, i, pre):
    k = i
    for w in reversed(pre):
        k -= 1
        while k >= 0 and not nt[k]:
            k -= 1
        if k < 0 or nt[k] != w:
            return False
    return True

def main():
    toks = load_tokens()
    nt = [norm(t) for t in toks]
    phrases = json.load(open(sys.argv[1]))
    out, bad, used = [], [], []
    for c in phrases:
        want = [norm(w) for w in c["text"].split() if norm(w)]
        pre = [norm(w) for w in c.get("pre", "").split() if norm(w)]
        post = [norm(w) for w in c.get("post", "").split() if norm(w)]
        hits = [(i, j) for i in range(len(nt))
                for j in [run(nt, i, want)] if j is not None
                and (not pre or back(nt, i, pre))
                and (not post or run(nt, j, post) is not None)]
        if not hits:
            bad.append("NO MATCH  %r" % c["text"][:90]); continue
        n = c.get("nth")
        if n is None:
            if len(hits) > 1:
                bad.append("%d MATCHES (add nth) %r" % (len(hits), c["text"][:90])); continue
            a, b = hits[0]
        else:
            if n > len(hits):
                bad.append("only %d matches, nth=%d  %r" % (len(hits), n, c["text"][:90])); continue
            a, b = hits[n - 1]
        out.append({"start": a, "end": b, "pass": c.get("pass", 1),
                    "reason": c.get("reason", ""), "text": " ".join(toks[a:b])})
        used.append((a, b, len(hits)))
    out.sort(key=lambda c: c["start"])
    for x, y in zip(out, out[1:]):
        if y["start"] < x["end"]:
            bad.append("OVERLAP %d-%d and %d-%d" % (x["start"], x["end"], y["start"], y["end"]))
    if bad:
        print("\n".join(bad)); sys.exit("refusing to write a cut list with %d faults" % len(bad))
    for c in out:
        a, b = c["start"], c["end"]
        print("%5d-%-5d p%d  ...%s  [[%s]]  %s..." % (
            a, b, c["pass"], " ".join(toks[max(0, a - 5):a]),
            " ".join(toks[a:b])[:120], " ".join(toks[b:b + 6])))
    dst = sys.argv[2] if len(sys.argv) > 2 else "cuts.json"
    json.dump(out, open(dst, "w"), indent=1)
    cut_words = sum(c["end"] - c["start"] for c in out)
    print("%d needles, %d of %d words cut = %.1f%% -> %s"
          % (len(out), cut_words, len(toks), 100.0 * cut_words / len(toks), dst))

if __name__ == "__main__":
    main()
