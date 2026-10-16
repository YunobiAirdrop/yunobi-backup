#!/usr/bin/env python3
"""Update judul/deskripsi/tag video via YouTube Data API (gratis, REST langsung).

Default DRY-RUN (hanya tampilkan perubahan). Eksekusi nyata butuh --apply
DAN persetujuan user (aturan: aksi yang mengubah channel user wajib approval).

Pakai: python yt_push.py SLUG --video VIDEO_ID [--title ...] [--description ...]
       [--tags "a,b,c"] [--apply]
"""
import argparse
import sys

from auth import yt_get, yt_put


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--video", required=True)
    ap.add_argument("--title", default=None)
    ap.add_argument("--description", default=None)
    ap.add_argument("--tags", default=None, help="pisahkan koma")
    ap.add_argument("--apply", action="store_true", help="eksekusi nyata")
    a = ap.parse_args()

    items = yt_get(a.slug, "/videos",
                   {"id": a.video, "part": "snippet"}).get("items", [])
    if not items:
        sys.exit(f"Video {a.video} tidak ditemukan / bukan milik channel ini.")
    sn = items[0]["snippet"]

    new_snippet = {
        "title": a.title if a.title is not None else sn["title"],
        "description": a.description if a.description is not None else sn["description"],
        "tags": a.tags.split(",") if a.tags is not None else sn.get("tags", []),
        "categoryId": sn["categoryId"],
    }
    for k in ("defaultLanguage", "defaultAudioLanguage"):
        if sn.get(k):
            new_snippet[k] = sn[k]

    changed = [k for k in ("title", "description", "tags")
               if new_snippet.get(k) != sn.get(k)]
    if not changed:
        print("Tidak ada perubahan.")
        return

    print(f"Video : {a.video}\nJudul lama: {sn['title']}")
    for k in changed:
        print(f"\n--- {k} BARU ---\n{new_snippet[k]}")

    if not a.apply:
        print("\n[DRY-RUN] Tambahkan --apply untuk eksekusi nyata.")
        return

    yt_put(a.slug, "/videos", {"part": "snippet"},
           {"id": a.video, "snippet": new_snippet})
    print("\nOK, metadata terupdate.")


if __name__ == "__main__":
    main()
