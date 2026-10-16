#!/usr/bin/env python3
"""Harvest the phrases people actually type into TikTok, for a seed keyword.

The rule this serves is already in SKILL.md: a hook is ultra specific or it is not a hook, and
the viewer has to identify. The failure it prevents is a writer inventing what the viewer would
say. `customer-voice` solves that from 367 recorded calls; this solves it from search demand,
which is the second corpus of the viewer's own words and the only one that is free and current.

WHAT IT IS NOT. This skill's most replicated finding is that hook construction does not separate
winners from controls, so a harvested phrase is not a lever on views. It is vocabulary, filed the
same way `references/hook-teardown.md` is filed, plus one thing that teardown does not carry: the
phrase was typed by a person who wanted the answer. That makes it evidence for the *subject*
(`idea-mining`) and the *title* first, and for the hook wording second.

  python3 search-demand.py "agency owner"                  # one seed, fully expanded
  python3 search-demand.py "agency owner" "n8n" "clickup"   # several seeds, one table
  python3 search-demand.py "ai agent" --plain              # no expansion, the bare autocomplete
  python3 search-demand.py "ai agent" --json               # machine-readable

WHY the expansion. TikTok returns 10 suggestions per query, which is the manual method and its
ceiling. Two expansions lift that. The a-z pass appends each letter to the seed and returns the
long tail underneath the top 10. The modifier pass wraps the seed in the shapes a problem is
typed in ("how to X", "X without", "X not working"), because the a-z pass alone comes back almost
entirely topics: on the first real run it produced 642 topics, 33 problems and 2 questions, and
the phrases worth a hook are the other two columns.

Read the two differently. An a-z phrase was volunteered by the index. A modifier phrase was
prompted by the query, so the index confirmed it exists rather than nominating it, and `from`
carries which query produced it so the distinction survives into the table.

The endpoint is TikTok's own web-search autocomplete, unauthenticated, no signature. `score` is
TikTok's predicted click-through for that suggestion in that dropdown; it ranks, it is not a
search volume, and nobody should quote it as one. `seen` is how many of the 27 queries surfaced
the phrase, which is the more honest breadth signal of the two.
"""

import argparse
import json
import re
import string
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict

ENDPOINT = "https://www.tiktok.com/api/search/general/sug/"
BASE_PARAMS = {
    "aid": "1988",
    "app_language": "en",
    "app_name": "tiktok_web",
    "browser_language": "en-US",
    "channel": "tiktok_web",
    "device_platform": "web_pc",
    "from_page": "search",
    "os": "mac",
    "region": "US",
    "webcast_language": "en",
}
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

PREFIXES = ("how to", "why", "what", "how do i", "best", "is")
SUFFIXES = ("without", "not", "vs", "mistakes", "for beginners", "free", "worth it", "too")

QUESTION_STARTS = (
    "how", "why", "what", "when", "where", "which", "who", "can", "should",
    "do", "does", "did", "is", "are", "will", "would",
)
PROBLEM_WORDS = {
    "not", "without", "stop", "stopped", "quit", "fix", "fixing", "broken", "hard",
    "struggle", "struggling", "fail", "failing", "failed", "mistake", "mistakes",
    "wrong", "hate", "worth", "alternative", "alternatives", "instead", "vs",
    "versus", "cheap", "cheaper", "free", "scam", "overwhelmed", "burnout",
    "stuck", "slow", "expensive", "problem", "problems", "issue", "issues",
    "beginner", "beginners", "first", "start", "starting", "avoid", "no",
}


def suggest(keyword):
    params = dict(BASE_PARAMS, keyword=keyword)
    url = ENDPOINT + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.tiktok.com/"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        payload = json.load(resp)
    out = []
    for item in payload.get("sug_list") or []:
        content = (item.get("content") or "").strip().lower()
        if not content:
            continue
        score = float((item.get("extra_info") or {}).get("predict_ctr_score") or 0.0)
        out.append((content, score))
    return out


def classify(phrase):
    words = phrase.split()
    if words[0] in QUESTION_STARTS:
        return "question"
    if PROBLEM_WORDS & set(words):
        return "problem"
    return "topic"


def harvest(seeds, expand, delay, min_words, max_words):
    best = defaultdict(float)
    seen = defaultdict(int)
    origin = {}
    queries = []
    for seed in seeds:
        queries.append(seed)
        if expand:
            queries.extend(f"{seed} {letter}" for letter in string.ascii_lowercase)
            queries.extend(f"{prefix} {seed}" for prefix in PREFIXES)
            queries.extend(f"{seed} {suffix}" for suffix in SUFFIXES)

    for i, query in enumerate(queries, 1):
        try:
            results = suggest(query)
        except Exception as exc:  # noqa: BLE001 - a dead query must not kill the run
            print(f"  ! {query}: {exc}", file=sys.stderr)
            continue
        for content, score in results:
            best[content] = max(best[content], score)
            seen[content] += 1
            origin.setdefault(content, query)
        print(f"  {i}/{len(queries)} {query} -> {len(results)}", file=sys.stderr)
        time.sleep(delay)

    rows = []
    for phrase, score in best.items():
        n_words = len(phrase.split())
        if not min_words <= n_words <= max_words:
            continue
        if not re.search(r"[a-z]", phrase):
            continue
        rows.append(
            {
                "phrase": phrase,
                "words": n_words,
                "kind": classify(phrase),
                "score": round(score, 5),
                "seen": seen[phrase],
                "from": origin[phrase],
            }
        )
    rows.sort(key=lambda r: (-r["seen"], -r["score"]))
    return rows, len(queries)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("seeds", nargs="+", help="core niche keywords, quoted")
    ap.add_argument("--plain", action="store_true", help="no a-z expansion, the bare 10 per seed")
    ap.add_argument("--min-words", type=int, default=3, help="default 3, the tweet's floor")
    ap.add_argument("--max-words", type=int, default=6, help="default 6, the tweet's ceiling")
    ap.add_argument("--delay", type=float, default=0.35, help="seconds between requests")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows, n_queries = harvest(
        args.seeds, not args.plain, args.delay, args.min_words, args.max_words
    )

    if args.json:
        print(json.dumps({"seeds": args.seeds, "queries": n_queries, "phrases": rows}, indent=2))
        return

    print(f"\n# TikTok search demand: {', '.join(args.seeds)}")
    print(f"\n{n_queries} queries, {len(rows)} phrases of {args.min_words}-{args.max_words} words.")
    print("`score` is TikTok's predicted CTR for the suggestion, not a volume. `seen` is how many")
    print("queries surfaced the phrase.\n")
    for kind in ("question", "problem", "topic"):
        group = [r for r in rows if r["kind"] == kind]
        if not group:
            continue
        print(f"\n## {kind} ({len(group)})\n")
        print("| phrase | seen | score |")
        print("| --- | --- | --- |")
        for r in group:
            print(f"| {r['phrase']} | {r['seen']} | {r['score']} |")


if __name__ == "__main__":
    main()
