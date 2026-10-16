#!/usr/bin/env python3
"""Laporan analitik per channel via YouTube Analytics API (gratis, kuota API resmi).

Pakai: python analytics.py SLUG [--days 28] [--top 50]
Output: JSON berisi ringkasan channel + daftar video (views, CTR, durasi tonton).
Dipakai cron mingguan untuk menemukan video CTR rendah yang layak di-refresh SEO-nya.

Memakai REST langsung (requests) karena googleapiclient/httplib2 tidak bisa
menembus proxy berautentikasi VM.
"""
import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

from auth import yt_get, ya_get

HERE = Path(__file__).parent
CHANNELS_FILE = HERE / "channels.yaml"


def load_channels():
    return yaml.safe_load(CHANNELS_FILE.read_text())["channels"]


def resolve_channel_id(slug, info):
    if info.get("channel_id"):
        return info["channel_id"]
    r = yt_get(slug, "/channels", {"forHandle": info["handle"], "part": "id"})
    items = r.get("items", [])
    if not items:
        sys.exit(f"Handle {info['handle']} tidak ditemukan.")
    cid = items[0]["id"]
    # cache ke channels.yaml
    txt = CHANNELS_FILE.read_text()
    old = f'handle: "{info["handle"]}"'
    new = f'handle: "{info["handle"]}", channel_id: "{cid}"'
    if old in txt:
        CHANNELS_FILE.write_text(txt.replace(old, new))
    return cid


def report(slug, days=28, top=50):
    info = load_channels()[slug]
    cid = resolve_channel_id(slug, info)
    end = date.today()
    start = end - timedelta(days=days)

    # Ringkasan channel
    ch = ya_get(slug, {
        "ids": f"channel=={cid}",
        "startDate": str(start), "endDate": str(end),
        "metrics": "views,estimatedMinutesWatched,subscribersGained",
    })
    summary = dict(zip(
        ["views", "watch_minutes", "subs_gained"],
        ch["rows"][0] if ch.get("rows") else [0, 0, 0],
    ))

    # Per video (catatan: impressions/CTR TIDAK tersedia di Analytics API
    # publik — pakai views + retensi sebagai sinyal underperform)
    r = ya_get(slug, {
        "ids": f"channel=={cid}",
        "startDate": str(start), "endDate": str(end),
        "metrics": "views,likes,estimatedMinutesWatched,averageViewDuration",
        "dimensions": "video", "sort": "-views", "maxResults": top,
    })

    vids = []
    for row in r.get("rows", []):
        vids.append({
            "video_id": row[0], "views": row[1], "likes": row[2],
            "watch_minutes": round(row[3], 1), "avg_view_sec": round(row[4], 1),
        })

    # Lengkapi judul + tanggal tayang
    if vids:
        ids = [v["video_id"] for v in vids]
        for i in range(0, len(ids), 50):
            det = yt_get(slug, "/videos", {
                "id": ",".join(ids[i:i + 50]), "part": "snippet"})
            meta = {it["id"]: (it["snippet"]["title"],
                               it["snippet"]["publishedAt"][:10])
                    for it in det.get("items", [])}
            for v in vids[i:i + 50]:
                t, d = meta.get(v["video_id"], ("?", "?"))
                v["title"] = t
                v["published"] = d

    out = {"channel": slug, "handle": info["handle"], "channel_id": cid,
           "days": days, "summary": summary, "videos": vids}
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--days", type=int, default=28)
    ap.add_argument("--top", type=int, default=50)
    a = ap.parse_args()
    report(a.slug, a.days, a.top)
