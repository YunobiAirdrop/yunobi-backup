#!/usr/bin/env python3
"""Internal link otomatis: untuk tiap artikel baru, AI pilihkan 3 topik
terkait dari riwayat artikel blog → jadi kotak 'Baca juga' (posting.py).
Pakai: ./venv/bin/python baca_juga.py --blog kabarviral   (1 req/blog)
"""
import argparse, glob, json, os, sys, time
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
sys.path.insert(0, BASE)
_src = open(os.path.join(BASE, "tulis_ulang.py")).read()
_g = {"__name__": "__lib__", "__file__": "tulis_ulang.py"}
sys.argv = ["tulis_ulang.py", "--blog", "kabarviral"]
exec(compile(_src.split("def main():")[0], "tulis_ulang.py", "exec"), _g)
ROUTER_URL, MODELS, get_api_keys = _g["ROUTER_URL"], _g["MODELS"], _g["get_api_keys"]

PROMPT = """Kamu editor SEO blog Indonesia. Untuk tiap ARTIKEL BARU, pilihkan 3 TOPIK TERKAIT dari DAFTAR RIWAYAT (pilih yang paling relevan, jangan asal).

ARTIKEL BARU:
{baru}

DAFTAR RIWAYAT (judul + label):
{riwayat}

Balas HANYA JSON: {{"<judul_artikel_baru>": ["topik terkait 1", "topik terkait 2", "topik terkait 3"]}}
Topik terkait = 2-4 kata kunci yang pembaca artikel itu kemungkinan cari juga."""

def _riwayat(blog_nama):
    pool = []
    for f in sorted(glob.glob(os.path.join(DATA, f"artikel_terkirim-{blog_nama}.json")))[-4:]:
        try:
            for a in json.load(open(f)):
                pool.append({"judul": a.get("judul", ""), "label": ", ".join(a.get("label", []))})
        except Exception:
            pass
    return pool[-60:]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--blog", required=True)
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(BASE, "config.json")))
    blog = next(b for b in cfg["blogs"] if b["nama"] == a.blog)
    blog_url = blog.get("url", "").rstrip("/")
    path = os.path.join(DATA, f"artikel-{a.blog}.json")
    if not os.path.exists(path):
        print("tidak ada artikel baru")
        return
    artikels = json.load(open(path))
    riwayat = _riwayat(a.blog)
    if not riwayat:
        print("riwayat kosong, lewati (posting.py pakai fallback label)")
        return
    baru_txt = "\n".join(f"- {x['judul']}" for x in artikels)
    riw_txt = "\n".join(f"- {r['judul']} [{r['label']}]" for r in riwayat)
    msg = PROMPT.format(baru=baru_txt, riwayat=riw_txt)
    mapping = {}
    for key in get_api_keys():
        for model in MODELS[:4]:
            try:
                r = requests.post(ROUTER_URL, headers={
                    "Authorization": f"Bearer {key}", "Content-Type": "application/json",
                    "HTTP-Referer": "https://kabarviralterkiniterbaru.blogspot.com/",
                    "X-Title": "Blog Otomatis",
                }, json={"model": model, "messages": [{"role": "user", "content": msg}],
                          "temperature": 0.5, "max_tokens": 2000}, timeout=150)
                if r.status_code in (429, 503):
                    if "per-day" in r.text or "free-models" in r.text:
                        break
                    time.sleep(5)
                    continue
                r.raise_for_status()
                dec = json.JSONDecoder()
                obj, _ = dec.raw_decode(r.text.strip())
                teks = obj["choices"][0]["message"]["content"].replace("```json", "").replace("```", "").strip()
                mapping = json.loads(teks[teks.find("{"):])
                break
            except Exception:
                time.sleep(3)
        if mapping:
            break
    n = 0
    for art in artikels:
        rel = mapping.get(art["judul"], [])[:3]
        if rel and blog_url:
            from urllib.parse import quote
            links = "".join(
                f'<li><a href="{blog_url}/search?q={quote(t)}">Baca juga: {t}</a></li>' for t in rel)
            art["baca_juga_html"] = (
                f'<div style="background:#f5f7fa;border-left:4px solid #e63946;'
                f'padding:12px 16px;margin:16px 0;"><strong>Baca juga:</strong>'
                f'<ul style="margin:8px 0 0 18px;">{links}</ul></div>')
            n += 1
    json.dump(artikels, open(path, "w"), ensure_ascii=False, indent=1)
    print(f"baca-juga terisi untuk {n}/{len(artikels)} artikel")

if __name__ == "__main__":
    main()
