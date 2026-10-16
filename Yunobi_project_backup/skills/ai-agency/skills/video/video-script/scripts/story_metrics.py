#!/usr/bin/env python3
"""Measure the story mechanics of a script or a transcript, deterministically.

WHY this exists: every rule in `storytelling`, `video-hooks` and `video-script` about seams,
hedges, contrast and prediction was checkable by eye and therefore checked differently every
time. This puts one number on each of them, with the offending sentence attached, so a review
argues with a measurement instead of with an impression.

What it does NOT do is judge. It counts. A high hedge count on a provenance-heavy script is
correct; the thresholds that turn a count into a verdict live in `video-edit`,
`references/checks.md`, calibrated against the 627-video corpus.

Pronouns are deliberately absent: `video-edit/scripts/take-stats.py` owns first and second
person and this would be the second copy of that count.

    python3 story_metrics.py transcript.txt --duration 1140
    python3 story_metrics.py script.json --json          # {"blocks":[{"name","spoken"}...]}
    python3 story_metrics.py --corpus <competitor-intel/data> [--check]   # self-check

**The self-check is not a validity test and does not pretend to be one.** None of these axes
separates a winner from a control in the corpus, so there is no separation for it to preserve. What
it guards is calibration: each rule's fire rate across 627 videos, recorded when the thresholds
were set. A pattern tightened or loosened later moves those rates, and a rule that fires on 90% of
the niche or on none of it has stopped being a gate. `--check` exits 1 when a rate leaves its band.
"""

import argparse
import json
import os
import re
import statistics
import sys

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
TERMINATOR = re.compile(r"[.!?]")
# Below this many sentence terminators per 100 words the text is an auto-caption track with no
# punctuation, and every sentence-shaped measurement below is measuring YouTube's ASR instead of
# the writing. 288 of the 627 videos in the corpus are like this. Punctuated prose runs 4 to 8.
PUNCTUATION_FLOOR = 1.0
WORD = re.compile(r"[a-z0-9'']+", re.I)
DIGIT = re.compile(r"\d")

# Transitions that carry the viewer across a seam. Split into two lists on purpose: the second is
# the subset already banned in vibe-kit/packages/lint/data/slop-words.js, and a re-hook built on
# one of those is counted as a fault rather than as a re-hook.
REHOOK = re.compile(
    r"\b(?:which is (?:exactly )?why|which would have|which is when|and that(?:'|’)?s (?:when|where|why)"
    r"|here(?:'|’)?s what happens|the problem with that|except that|only it|and then it"
    r"|that(?:'|’)?s not the (?:only|whole)|what that (?:means|costs)|watch what happens"
    r"|and this is where|but here(?:'|’)?s|which means (?:you|the|that)|that(?:'|’)?s when"
    r"|the second you|the moment you|and then the|only now|and that broke|which broke"
    r"|before you can .{0,30}, you have to)\b",
    re.I,
)
THROAT_CLEARING = re.compile(
    r"\b(?:here(?:'|’)?s the thing|it turns out|here(?:'|’)?s the problem|the truth is"
    r"|this is where it gets (?:interesting|crazy|good|fun)|but that(?:'|’)?s not even the"
    r"|what nobody (?:talks about|tells you)|here(?:'|’)?s what they (?:won(?:'|’)?t|will not) tell you"
    r"|let me be clear|make no mistake|let that sink in)\b",
    re.I,
)
CONTRAST = re.compile(r"\b(?:but|however|instead|except|actually|yet|whereas|although)\b", re.I)
# A seam is wider than the phrase list above. Anything that starts a sentence by turning the
# viewer somewhere new is a candidate boundary, and the cadence rule is about boundaries rather
# than about phrasing. WHY sentence-initial only: "but" mid-clause is a qualifier inside one
# thought, and counting it put a re-hook every nine words in a corpus that plainly has none.
SEAM_MARKER = re.compile(
    r"^(?:but|so|now|then|next|however|instead|actually|okay|alright|and (?:that|then|this)"
    r"|here(?:'|’)?s|the (?:second|third|fourth|fifth|next|last|other)|once you|before (?:we|you)"
    r"|let(?:'|’)?s|which is|what (?:that|this) means|that(?:'|’)?s (?:when|where|why))\b",
    re.I,
)

# "You are probably thinking X" and its family. The strongest form of pointing at the viewer.
THOUGHT_NARRATION = re.compile(
    r"\b(?:you(?:'|’)?re probably (?:thinking|wondering)|you might be (?:thinking|wondering)"
    r"|you(?:'|’)?re (?:sitting there )?thinking|i know what you(?:'|’)?re thinking"
    r"|the question you(?:'|’)?re (?:asking|probably asking)|the objection you"
    r"|if you(?:'|’)?re (?:like|anything like)|what you(?:'|’)?re thinking (?:right now|here)"
    r"|the thing you(?:'|’)?re worried about|you(?:'|’)?ll be asking)\b",
    re.I,
)
# Loss aversion framing: a warning rather than an offer.
NEGATIVE_FRAME = re.compile(
    r"\b(?:worst (?:thing|possible)|biggest mistake|the mistake (?:most|everyone|people)"
    r"|stop (?:doing|writing|posting|building|using)|never (?:ever )?(?:do|post|write|send|start)"
    r"|is killing your|is costing you|do(?:n(?:'|’)?t| not) make this|you(?:'|’)?re doing (?:this|it) wrong"
    r"|harder than it (?:has|needs) to be|this is why you(?:'|’)?re (?:not|still))\b",
    re.I,
)
# A named idea. Term branding: the name is what the recap and the artefact CTA point at.
TERM_BRAND = re.compile(
    r"(?:\bi call (?:this|it|these|them)\b|\b(?:it|this) is called the\b|\bcalled the\b"
    r"|\bthe [A-Z][\w-]+(?: [A-Z][\w-]+){0,3} (?:Method|Framework|Loop|Rule|System|Effect|Ladder|Score|Test|Gate|Pass|Stack)\b)",
)
# The pivot humanizer caps at one per script: define a thing by denying another first.
NEGATION_PIVOT = re.compile(
    r"\b(?:it(?:'|’)?s |it is |that(?:'|’)?s |this is )?not (?:just |only |merely )?"
    r"(?:a|an|the|about)?[^,.;:]{2,45}[,.] (?:it(?:'|’)?s|it is|that(?:'|’)?s|this is|they(?:'|’)?re)\b",
    re.I,
)
# Hedges. Allowed on the provenance of a claim, never on an instruction: the classifier below
# splits them on whether the sentence is talking about where a number came from.
# WHY a verb list rather than a bare modal: "predict what might happen next" is a mechanism being
# described, not a softened instruction, and matching every `might` reported 19 hedges in a
# transcript that softens about four things. A hedge is only a hedge when it is hedging advice.
HEDGE = re.compile(
    r"\b(?:(?:might|may|could|can probably)\s+(?:work|help|be worth|want|need|notice|see|find|make"
    r"|improve|change|get|give|start|try|end up|be the|be a)"
    r"|maybe (?:you|try|start|it)|probably (?:want|should|worth)|it depends|sort of|kind of"
    r"|i think(?: that)?|i guess|in my opinion|it seems|arguably|tends to|your mileage)\b",
    re.I,
)
PROVENANCE = re.compile(
    r"\b(?:estimate[ds]?|estimated|roughly|approximately|about \d|around \d|median|sample|control"
    r"|not measured|hypothesis|source|measured|data|per cent|percent|%|n=\d|study|survey"
    r"|your mileage|depends on your)\b",
    re.I,
)
# The prediction the head fake breaks, and the reveal that breaks it.
EXPECTATION = re.compile(
    r"\b(?:you(?:'|’)?d expect|you would expect|you(?:'|’)?d (?:think|assume)|most people (?:assume|think|believe)"
    r"|everyone (?:assumes|thinks|believes)|the obvious (?:answer|move|fix)|sounds backwards"
    r"|you(?:'|’)?d imagine|conventional wisdom|the assumption is)\b",
    re.I,
)
REVEAL = re.compile(
    r"\b(?:what actually happen|the real (?:reason|answer|problem)|it was never|had never been"
    r"|was not (?:a|the|about)|the opposite (?:happened|is true)|and that is the whole|nobody had)\b",
    re.I,
)
# Stakes: a character, something at risk, and a clock. All three, or the prediction machine
# never starts.
STAKES_CHARACTER = re.compile(
    r"\b(?:my client|the client|a founder|the founder|an agency|the agency|the owner|the ops"
    r"|his|her|their team|a friend|somebody|someone|a guy|a customer|the buyer|you)\b",
    re.I,
)
STAKES_RISK = re.compile(
    r"\b(?:about to lose|at risk|on the line|was going to (?:lose|blow|miss|break)|nearly lost"
    r"|cost (?:him|her|them|us|me) |broke|failed|fell over|walked away|churned|refund|blew through"
    r"|would have (?:lost|cost)|down to (?:his|her|their|our) last)\b",
    re.I,
)
STAKES_CLOCK = re.compile(
    r"\b(?:\d+\s*(?:seconds|minutes|hours|days|weeks|months)\b|by (?:friday|monday|tomorrow|tonight)"
    r"|that (?:night|morning|afternoon)|the next (?:morning|day)|before the|deadline|within (?:a|the|\d)"
    r"|in (?:a|one|two|three) (?:week|day|hour|month))\b",
    re.I,
)


def sentences(text):
    return [s.strip() for s in SENTENCE_SPLIT.split(text) if s.strip()]


def hits(pattern, text, limit=6):
    """Every matching sentence, with the character offset the match started at."""
    out = []
    for match in pattern.finditer(text):
        start = text.rfind(".", 0, match.start()) + 1
        end = text.find(".", match.end())
        end = len(text) if end == -1 else end + 1
        out.append({"at": match.start(), "text": text[start:end].strip()[:220]})
        if len(out) >= limit:
            break
    return out


def carries_fact(sentence):
    """Delete the transition and see whether anything is left standing.

    The proxy for "a fact crossed the seam" is a digit, a mid-sentence capitalised token (a
    product, a person, a tool), or a rare content word. A transition sentence built out of nothing
    but function words and adjectives fails, which is the throat-clearing this is looking for.
    """
    stripped = THROAT_CLEARING.sub(" ", REHOOK.sub(" ", sentence))
    stripped = CONTRAST.sub(" ", stripped)
    if DIGIT.search(stripped):
        return True
    tokens = stripped.split()
    for token in tokens[1:]:
        if token[:1].isupper() and token.lower() not in {"i", "i'm", "i'll", "i've"}:
            return True
    words = [w.lower() for w in WORD.findall(stripped)]
    content = [w for w in words if w not in FUNCTION_WORDS and len(w) > 3]
    return len(content) >= 3


FUNCTION_WORDS = {
    "that", "this", "there", "here", "what", "which", "when", "then", "than", "with", "your",
    "you", "they", "them", "their", "have", "has", "had", "will", "would", "could", "should",
    "about", "into", "from", "just", "even", "also", "very", "really", "most", "more", "next",
    "thing", "things", "stuff", "part", "point", "going", "gets", "get", "make", "makes", "want",
    "important", "interesting", "better", "best", "good", "great", "crazy", "actually",
}


def measure(text, duration_seconds=None, blocks=None):
    """Every story metric for one script or transcript.

    `blocks` (a list of {"name", "spoken"}) enables the per-seam verdict; without it the seam
    section reports cadence over the whole text instead, which is what a raw transcript allows.
    """
    sents = sentences(text)
    words = WORD.findall(text)
    word_count = len(words)
    terminators = len(TERMINATOR.findall(text))
    punctuated = word_count > 0 and (terminators * 100 / word_count) >= PUNCTUATION_FLOOR
    per_1k = (lambda n: round(n * 1000 / word_count, 2)) if word_count else (lambda n: None)

    rehook_sents = [s for s in sents if REHOOK.search(s) or THROAT_CLEARING.search(s)]
    seam_sents = [s for s in sents if SEAM_MARKER.search(s)]
    empty = [s for s in rehook_sents if not carries_fact(s)]
    throat = [s for s in sents if THROAT_CLEARING.search(s)]

    hedge_all = [s for s in sents if HEDGE.search(s)]
    hedge_instruction = [s for s in hedge_all if not PROVENANCE.search(s)]

    contrast_sents = [s for s in sents if CONTRAST.search(s)]

    result = {
        "words": word_count,
        "sentences": len(sents),
        "punctuated": punctuated,
        "terminatorsPer100Words": round(terminators * 100 / word_count, 2) if word_count else None,
        "durationSeconds": duration_seconds,
        "seams": {
            "rehookSentences": len(rehook_sents),
            "rehooksPer10Min": _per_10min(len(rehook_sents), duration_seconds),
            "seamMarkers": len(seam_sents),
            "seamMarkersPer10Min": _per_10min(len(seam_sents), duration_seconds),
            "seamsCarryingFact": sum(1 for s in seam_sents if carries_fact(s)),
            "emptyRehooks": len(empty),
            "throatClearing": len(throat),
            "throatClearingHits": hits(THROAT_CLEARING, text),
            "emptyRehookHits": [{"text": s[:220]} for s in empty[:6]],
        },
        "locks": {
            "contrastSentencePct": round(100 * len(contrast_sents) / len(sents), 1) if sents else None,
            "contrastPer1k": per_1k(len(contrast_sents)),
            "thoughtNarration": len(THOUGHT_NARRATION.findall(text)),
            "thoughtNarrationHits": hits(THOUGHT_NARRATION, text, 4),
            "negativeFrames": len(NEGATIVE_FRAME.findall(text)),
            "termBrands": len(TERM_BRAND.findall(text)),
            "termBrandHits": hits(TERM_BRAND, text, 4),
            "hedgesOnInstruction": len(hedge_instruction),
            "hedgesOnInstructionPer1k": per_1k(len(hedge_instruction)),
            "hedgesOnProvenance": len(hedge_all) - len(hedge_instruction),
            "hedgeHits": [{"text": s[:220]} for s in hedge_instruction[:6]],
            "negationPivots": len(NEGATION_PIVOT.findall(text)),
            "negationPivotHits": hits(NEGATION_PIVOT, text, 4),
        },
        "prediction": {
            "expectationSet": len(EXPECTATION.findall(text)),
            "reveals": len(REVEAL.findall(text)),
            "expectationHits": hits(EXPECTATION, text, 4),
        },
        "stakes": _stakes(text, sents),
    }
    if blocks:
        result["seams"]["perBlock"] = _per_block(blocks)
    if duration_seconds:
        # Measured on loop openers, not on seam markers. A sentence-initial "so" is a connective
        # inside one thought; the cadence rule is about a question being reopened, and only the
        # phrase list sees that. Counting connectives put a "re-hook" every 13 seconds, which is a
        # measurement of English rather than of storytelling.
        result["seams"]["longestGapSeconds"] = _longest_gap(text, sents, rehook_sents, duration_seconds)
        result["seams"]["medianGapSeconds"] = _median_gap(text, sents, rehook_sents, duration_seconds)
    return result


def _per_10min(count, duration_seconds):
    if not duration_seconds:
        return None
    return round(count * 600 / duration_seconds, 2)


def _stakes(text, sents):
    """The triad, measured over the opening third, where the stakes have to land."""
    head = " ".join(sents[: max(1, len(sents) // 3)])
    return {
        "character": bool(STAKES_CHARACTER.search(head)),
        "risk": bool(STAKES_RISK.search(head)),
        "clock": bool(STAKES_CLOCK.search(head)),
        "triadComplete": all(
            bool(p.search(head)) for p in (STAKES_CHARACTER, STAKES_RISK, STAKES_CLOCK)
        ),
        "openingDigits": len(DIGIT.findall(head)),
    }


def _longest_gap(text, sents, marked, duration_seconds):
    """The worst stretch with no re-hook in it, in seconds, assuming an even read.

    WHY estimated rather than read off the cue timings: a script has no timings at all, and the
    rule it is checked against (one every 60 to 90 seconds) has to apply to both. The estimate is
    words-elapsed over words-total times runtime, which is exact enough to find a four-minute
    stretch and is never used to argue about ten.
    """
    gaps = _gaps(sents, marked, duration_seconds)
    return round(max(gaps), 1) if gaps else None


def _median_gap(text, sents, marked, duration_seconds):
    """The typical distance between one turn and the next, which is what a cadence rule names."""
    gaps = _gaps(sents, marked, duration_seconds)
    return round(statistics.median(gaps), 1) if gaps else None


def _gaps(sents, marked, duration_seconds):
    total_words = sum(len(WORD.findall(s)) for s in sents) or 1
    marks, elapsed = [0.0], 0
    for sentence in sents:
        elapsed += len(WORD.findall(sentence))
        if sentence in marked:
            marks.append(elapsed * duration_seconds / total_words)
    marks.append(duration_seconds)
    return [b - a for a, b in zip(marks, marks[1:])]


def _per_block(blocks):
    """One verdict a seam: does the block's last sentence close and open at once."""
    out = []
    for block in blocks[:-1]:
        spoken = block.get("spoken", "")
        lines = [line.strip("- ").strip() for line in spoken.splitlines() if line.strip()]
        last = lines[-1] if lines else ""
        has_transition = bool(REHOOK.search(last) or CONTRAST.search(last) or THROAT_CLEARING.search(last))
        out.append({
            "block": block.get("name", "?"),
            "lastBeat": last[:180],
            "rehook": has_transition and carries_fact(last),
            "throatClearing": bool(THROAT_CLEARING.search(last)),
        })
    return out


# The gate. Two tiers, and the split is what makes it usable: FAIL is a banned construction or a
# number outside what the whole niche tolerates, WARN is inside the niche but short of the house
# target. A single-tier gate anchored on the house target failed 90% of 627 measured videos, which
# is an instrument that says nothing.
#
# Every threshold names its source. A `corpus` number is a percentile of those 627 videos; a
# `house` number is doctrine, and it is tighter than the niche on purpose, because the corpus
# measures reach and not one of these axes separated a winner from its own channel's controls in
# it. The niche median is what people do, never evidence of what works.
#
# (key, direction, warn, fail, source, needs_punctuation, why)
RULES = [
    ("throatClearing", "<=", 0, 0, "house; niche p75 is 0", False,
     "Banned transitions, from slop-words.js. Three quarters of the niche never uses one."),
    ("emptyRehooks", "<=", 0, 1, "house", True,
     "A re-hook with nothing carried across the seam is throat-clearing wearing a bridge."),
    ("negationPivots", "<=", 1, 3, "house; niche p75 0.18/1k", False,
     "One per script. Several in ninety seconds is the loudest machine-wrote-this signal there is."),
    ("hedgesOnInstructionPer1k", "<=", 3.23, 5.74, "corpus p75 / p90", False,
     "Hedge the provenance of a claim, never the instruction."),
    ("longestGapSeconds", "<=", 300, 831.2, "house / corpus p75", True,
     "The longest stretch with no question reopened. The niche p10 is 316s, so 300 is a target."),
    ("contrastSentencePct", ">=", 10.8, 8.8, "corpus p25 / p10", True,
     "Below the niche's bottom quartile for contrast: the piece states rather than turns."),
    ("triadComplete", "==", True, None, "house", True,
     "A character, something at risk and a clock, in the opening third. Never a fail: the niche p90 "
     "is 0, so either almost nobody sets stakes or this detector is too strict."),
]

BAND_EDGES = ("p10", "p25", "p50", "p75", "p90")


def _lookup(metrics, key):
    for section in ("seams", "locks", "prediction", "stakes"):
        if key in metrics.get(section, {}):
            return metrics[section][key]
    return metrics.get(key)


def _band(value, norm):
    """Which percentile band of the corpus this value lands in."""
    if value is None or not norm:
        return None
    edges = [(name, norm.get(name)) for name in BAND_EDGES if norm.get(name) is not None]
    if not edges:
        return None
    for name, edge in edges:
        if value <= edge:
            return f"<= {name}"
    return f"> {edges[-1][0]}"


def grade(metrics, norms=None):
    """Turn the counts into pass/fail rows, with the corpus percentile printed beside each."""
    norms = norms or load_norms()
    axes = (norms or {}).get("axes", {})
    rows = []
    for key, op, warn, fail, source, needs_punctuation, why in RULES:
        value = _lookup(metrics, key)
        blocked = needs_punctuation and not metrics.get("punctuated", True)
        if blocked or value is None:
            rows.append({
                "rule": key, "verdict": "n/a", "value": None, "warn": warn, "fail": fail,
                "source": source, "band": None,
                "why": "unpunctuated transcript, not measurable" if blocked else why,
            })
            continue
        rows.append({
            "rule": key,
            "verdict": _verdict(value, op, warn, fail),
            "value": value,
            "op": op,
            "warn": warn,
            "fail": fail,
            "source": source,
            "why": why,
            "band": _band(value, axes.get(key)),
        })
    return rows


def _verdict(value, op, warn, fail):
    def meets(limit):
        if limit is None:
            return True
        return value <= limit if op == "<=" else value >= limit if op == ">=" else value == limit

    if not meets(fail):
        return "fail"
    return "pass" if meets(warn) else "warn"


def load_norms():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "story-norms.json")
    return json.load(open(path)) if os.path.exists(path) else None


# Fire rates across the 627-video corpus when the thresholds were set, 29 Aug 2026, with the band
# each is allowed to move inside before the calibration counts as broken. A gate that fires on
# nearly everything and a gate that fires on nothing are the same useless instrument.
FIRE_RATES = {
    "throatClearing": (0.20, 0.10, 0.35),
    "longestGapSeconds": (0.14, 0.05, 0.30),
    "hedgesOnInstructionPer1k": (0.10, 0.03, 0.25),
    "negationPivots": (0.06, 0.01, 0.20),
    "contrastSentencePct": (0.06, 0.01, 0.20),
    "emptyRehooks": (0.05, 0.01, 0.20),
}


def corpus_check(data_dir, strict=False):
    """Re-derive every rule's fire rate over the corpus and compare it with the recorded one."""
    import glob

    counts, graded = {}, 0
    for path in sorted(glob.glob(os.path.join(data_dir, "*", "transcripts", "*.json"))):
        try:
            data = json.load(open(path))
        except (ValueError, OSError):
            continue
        text, duration = data.get("fullText") or "", data.get("durationSeconds")
        if not text or not duration or duration < 240:
            continue
        metrics = measure(text, duration)
        if metrics["words"] < 200:
            continue
        graded += 1
        for row in grade(metrics):
            if row["verdict"] == "fail":
                counts[row["rule"]] = counts.get(row["rule"], 0) + 1

    print(f"{graded} videos graded\n")
    print(f"{'rule':<28}{'fires on':>10}{'recorded':>10}   band")
    broken = 0
    for rule, (recorded, low, high) in FIRE_RATES.items():
        rate = counts.get(rule, 0) / graded if graded else 0.0
        inside = low <= rate <= high
        broken += not inside
        print(f"{rule:<28}{rate:>9.0%}{recorded:>10.0%}   {low:.0%}-{high:.0%}"
              f"{'' if inside else '   OUT OF BAND'}")
    print(f"\n{graded and sum(counts.values())} fails over {graded} videos.")
    if broken:
        print("A rule outside its band means the patterns moved and the thresholds need re-deriving\n"
              "against the corpus, not that the videos changed.")
    return 1 if (strict and broken) else 0


def _read(path):
    if path.endswith(".json"):
        data = json.load(open(path))
        if isinstance(data, dict) and "blocks" in data:
            blocks = data["blocks"]
            return "\n".join(b.get("spoken", "") for b in blocks), blocks
        if isinstance(data, dict) and "fullText" in data:
            return data["fullText"], None
    return open(path, encoding="utf-8").read(), None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="transcript .txt, transcript .json, or a script .json")
    parser.add_argument("--corpus", help="competitor-intel/data, to re-derive the fire rates")
    parser.add_argument("--check", action="store_true", help="exit 1 if a fire rate left its band")
    parser.add_argument("--duration", type=float, help="runtime in seconds, for the cadence numbers")
    parser.add_argument("--json", action="store_true", help="machine output")
    parser.add_argument("--grade", action="store_true", help="pass/fail rows against the corpus norms")
    args = parser.parse_args()

    if args.corpus:
        sys.exit(corpus_check(args.corpus, strict=args.check))
    if not args.path:
        parser.error("a path is required unless --corpus is given")
    if not os.path.exists(args.path):
        sys.exit(f"no such file: {args.path}")
    text, blocks = _read(args.path)
    result = measure(text, args.duration, blocks)

    if args.grade:
        rows = grade(result)
        if args.json:
            print(json.dumps({"metrics": result, "grade": rows}, indent=2))
            return
        norms = load_norms()
        if norms:
            print(f"graded against {norms['videos']} videos, {norms['channels']} channels")
        if not result["punctuated"]:
            print("NOTE: no sentence punctuation in this transcript. Sentence-shaped rules are n/a.")
        print()
        for row in rows:
            mark = {"pass": "PASS", "warn": "WARN", "fail": "FAIL", "n/a": " n/a"}[row["verdict"]]
            band = f"  [corpus {row['band']}]" if row["band"] else ""
            print(f"{mark}  {row['rule']:<26} {row['value']}  target {row.get('op','')} {row['warn']} ({row['source']}){band}")
            if row["verdict"] in ("fail", "warn"):
                print(f"        {row['why']}")
        failures = sum(1 for r in rows if r["verdict"] == "fail")
        warnings = sum(1 for r in rows if r["verdict"] == "warn")
        print(f"\n{failures} failed, {warnings} short of target, {len(rows)} rules")
        return

    if args.json:
        print(json.dumps(result, indent=2))
        return

    seams, locks, pred, stakes = result["seams"], result["locks"], result["prediction"], result["stakes"]
    print(f"{result['words']} words, {result['sentences']} sentences")
    print("\nSEAMS")
    print(f"  seam markers          {seams['seamMarkers']}  ({seams['seamMarkersPer10Min']} per 10 min)")
    print(f"  loop openers          {seams['rehookSentences']}  ({seams['rehooksPer10Min']} per 10 min)")
    if seams.get("medianGapSeconds"):
        print(f"  median gap            {seams['medianGapSeconds']}s")
    print(f"  empty (no fact)       {seams['emptyRehooks']}")
    print(f"  throat-clearing       {seams['throatClearing']}   BANNED")
    if seams.get("longestGapSeconds"):
        print(f"  longest gap           {seams['longestGapSeconds']}s")
    print("\nLOCKS")
    print(f"  contrast sentences    {locks['contrastSentencePct']}%")
    print(f"  thought narration     {locks['thoughtNarration']}")
    print(f"  negative frames       {locks['negativeFrames']}")
    print(f"  term brands           {locks['termBrands']}")
    print(f"  hedged instructions   {locks['hedgesOnInstruction']} ({locks['hedgesOnProvenance']} on provenance, allowed)")
    print(f"  negation pivots       {locks['negationPivots']}   cap is 1")
    print("\nPREDICTION")
    print(f"  expectation set       {pred['expectationSet']}")
    print(f"  reveals               {pred['reveals']}")
    print(f"\nSTAKES  character {stakes['character']}  risk {stakes['risk']}  clock {stakes['clock']}")
    for hit in seams["throatClearingHits"][:3]:
        print(f"\n  throat-clearing: {hit['text']}")
    for hit in locks["hedgeHits"][:3]:
        print(f"  hedged instruction: {hit['text']}")


if __name__ == "__main__":
    main()
