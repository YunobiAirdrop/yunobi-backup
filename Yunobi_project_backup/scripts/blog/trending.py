#!/usr/bin/env python3
"""Riset topik viral harian: baca antrean berita hari ini per blog,
minta AI memilih 10 topik paling potensial viral + angle tulisnya.
Output: data/trending-YYYY-MM-DD.json — dipakai laporan pagi & ide besok.
Pakai: ./venv/bin/python trending.py [--blog kabarviral]
"""
import argparse, datetime, glob, json, os, sys, time
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
sys.path.insert(0, BASE)
_src = open(os.path.join(BASE, "tulis_ulang.py")).read()
_g = {"__name__": "__lib__", "__file__": "tulis_ulang.py"}
sys.argv = ["tulis_ulang.py", "--blog", "kabarviral"]
exec(compile(_src.split("def main():")[0], "tulis_ulang.py", "exec"), _g)
ROUTER_URL, MODELS, get_api_keys = _g["ROUTER_URL"], _g["MODELS"], _g["get_api_keys"]

PROMPT = """Kamu analis tren berita Indonesia untuk blog "{niche}". Dari daftar headline hari ini, pilih 10 TOPIK paling potensial VIRAL (bikin orang klik & share).

Headline hari ini:
{daftar}

Balas HANYA JSON valid:
{{"topik": [{{"judul_asli": "...", "alasan_viral": "...", "angle_saran": "sudut tulis yang paling menarik"}}]}}
Pilih yang emosional, dekat dengan hidup pembaca, atau kontroversial sehat. Jangan pilih berita basi."""

def riset(blog_nama, niche, headlines):
    if not headlines:
        return {"topik": []}
    daftar = "\n".join(f"- {h}" for h in headlines[:40])
    msg = PROMPT.format(niche=niche, daftar=daftar)
    for key in get_api_keys():
        for model in MODELS[:4]:
            try:
                r = requests.post(ROUTER_URL, headers={
                    "Authorization": f"Bearer {key}", "Content-Type": "application/json",
                    "HTTP-Referer": "https://kabarviralterkiniterbaru.blogspot.com/",
                    "X-Title": "Blog Otomatis",
                }, json={"model": model, "messages": [{"role": "user", "content": msg}],
                          "temperature": 0.7, "max_tokens": 1500}, timeout=120)
                if r.status_code in (429, 503):
                    if "per-day" in r.text or "free-models" in r.text:
                        break
                    time.sleep(5)
                    continue
                r.raise_for_status()
                dec = json.JSONDecoder()
                obj, _ = dec.raw_decode(r.text.strip())
                teks = obj["choices"][0]["message"]["content"]
                teks = teks.replace("```json", "").replace("```", "").strip()
                s = teks.find("{")
                return json.loads(teks[s:])
            except Exception:
                time.sleep(3)
    return {"topik": []}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--blog", default="")
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(BASE, "config.json")))
    blogs = [b for b in cfg["blogs"] if not a.blog or b["nama"] == a.blog]
    hari = datetime.date.today().isoformat()
    hasil = {"tanggal": hari, "blogs": {}}
    for b in blogs:
        antrean = os.path.join(DATA, f"antrean-{b['nama']}.json")
        headlines = []
        if os.path.exists(antrean):
            try:
                headlines = [x.get("judul_asli", "") for x in json.load(open(antrean))]
            except Exception:
                pass
        print(f"Riset trending {b['nama']}: {len(headlines)} headline...")
        top = riset(b["nama"], b.get("niche", "campuran"), headlines)
        hasil["blogs"][b["nama"]] = top
        print(f"  -> {len(top.get('topik', []))} topik terpilih")
        time.sleep(2)
    out = os.path.join(DATA, f"trending-{hari}.json")
    json.dump(hasil, open(out, "w"), ensure_ascii=False, indent=1)
    print("Tersimpan:", out)

if __name__ == "__main__":
    main()
