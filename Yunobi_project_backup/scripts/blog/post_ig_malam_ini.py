#!/usr/bin/env python3
"""Posting 5 video promo afiliasi ke IG @beritaviraldotcom malam ini.
Dijalankan dari chat live: tiap post-feed memicu approval user."""
import json, subprocess, sys, time

ACCT = "17841462795414201"
DATA = json.load(open("/home/hatch/workspace/blog-otomatis/promo_out/posting_ig_2026-10-05.json"))

# mulai dari index argv[1] bila diberikan (untuk lanjutkan sisa)
start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
hasil = []
for i, r in enumerate(DATA[start:], start=start):
    print(f"\n[{i+1}/5] {r['nama']}", flush=True)
    cmd = ["instagram-cli", "post-feed", "--account-id", ACCT,
           "--file", r["video"], "--cover", r["cover"],
           "--caption", r["caption"]]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        ok = p.returncode == 0
        out = (p.stdout or p.stderr or "")[:300]
        print(("OK " if ok else "GAGAL ") + out[:150], flush=True)
        hasil.append({"slug": r["slug"], "ok": ok, "out": out})
    except subprocess.TimeoutExpired:
        print("TIMEOUT menunggu approval", flush=True)
        hasil.append({"slug": r["slug"], "ok": False, "out": "timeout-approval"})
        break
    time.sleep(20)

json.dump(hasil, open("/home/hatch/workspace/blog-otomatis/promo_out/hasil-ig-2026-10-05-malam.json", "w"),
          ensure_ascii=False, indent=1)
print("\nSELESAI:", sum(1 for h in hasil if h["ok"]), "/", len(hasil))
