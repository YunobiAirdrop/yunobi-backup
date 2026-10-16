#!/usr/bin/env python3
"""Posting 5 video promo ke Threads x2 + FB Page malam ini.
Dijalankan dari chat live: tiap publish memicu approval user."""
import json, subprocess, sys, time, uuid

THREADS = [("beritaviraldotcom", "17841423460796922"),
           ("ngewebyuk", "17841442711837842")]
FB_PAGE = "1347201611814398"
DATA = json.load(open("/home/hatch/workspace/blog-otomatis/promo_out/posting_ig_2026-10-05.json"))
HASIL = "/home/hatch/workspace/blog-otomatis/promo_out/hasil-threads-fb-2026-10-05-malam.json"

def run(cmd, timeout=300):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode == 0, (p.stdout or p.stderr or "")[:200]
    except subprocess.TimeoutExpired:
        return False, "timeout-approval"

hasil = []
tugas = []
for r in DATA:
    for nama, tid in THREADS:
        tugas.append(("threads-" + nama, ["threads-cli", "publish-post",
            "--account-id", tid, "--text", (r["caption"] or "")[:480],
            "--media-item", json.dumps({"file": r["video"], "cover": r["cover"]})], r["slug"]))
    tugas.append(("fb-BeritaViraldotcom", ["facebook-cli", "pages", "posts", "create",
        "--page-id", FB_PAGE, "--text", (r["caption"] or "")[:900],
        "--request-id", str(uuid.uuid4()), "--privacy", "PUBLIC",
        "--file", r["video"]], r["slug"]))

start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
tugas = tugas[start:]

for i, (akun, cmd, slug) in enumerate(tugas, start=start):
    print(f"[{i+1}/15] {akun} - {slug}", flush=True)
    ok, out = run(cmd)
    print(("  OK" if ok else "  GAGAL/TIMEOUT ") + out[:120], flush=True)
    hasil.append({"akun": akun, "slug": slug, "ok": ok, "out": out})
    if not ok and "timeout" in out:
        print("  berhenti: menunggu approval", flush=True)
        break
    time.sleep(15)

json.dump(hasil, open(HASIL, "w"), ensure_ascii=False, indent=1)
print(f"\nSELESAI: {sum(1 for h in hasil if h['ok'])}/{len(hasil)}")
