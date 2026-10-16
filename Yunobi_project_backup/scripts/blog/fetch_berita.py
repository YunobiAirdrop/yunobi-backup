#!/usr/bin/env python3
"""Ambil berita terbaru dari RSS media Indonesia, simpan antrean ke data/antrean.json."""
import json, os, re, sys, time, argparse, subprocess
from datetime import datetime, timezone, timedelta
import feedparser

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
os.makedirs(DATA, exist_ok=True)

def get_blog(nama):
    with open(os.path.join(BASE, "config.json")) as f:
        cfg = json.load(f)
    for b in cfg["blogs"]:
        if b["nama"] == nama:
            return b
    print(f"Blog '{nama}' tidak ada di config.json")
    sys.exit(1)

_parser = argparse.ArgumentParser()
_parser.add_argument("--blog", default="kabarviral")
_blog = get_blog(_parser.parse_args().blog)
BLOG_NAMA = _blog["nama"]
FEEDS = _blog["feeds"]
MAX_PER_RUN = _blog.get("artikel_per_hari", 3)
SEEN_FILE = os.path.join(DATA, f"seen-{BLOG_NAMA}.json")
ANTREAN_FILE = os.path.join(DATA, f"antrean-{BLOG_NAMA}.json")


def load_seen():
    try:
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    except Exception:
        return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(sorted(seen)[-500:], f)

def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())

STOPWORDS = set("""yang dan di ke dari untuk dengan pada adalah ini itu dalam sebagai
oleh para saat telah akan juga tidak bisa ada lebih sangat atau karena jika agar
supaya namun tetapi sedangkan sementara antara terhadap kepada olehnya""".split())

def kata_kunci(judul, n=5):
    kata = re.findall(r"[A-Za-z]{4,}", judul.lower())
    unik = []
    for k in kata:
        if k not in STOPWORDS and k not in unik:
            unik.append(k)
        if len(unik) >= n:
            break
    return " ".join(unik)

def gambar_fallback(judul):
    """Cari gambar relevan via image-search kalau ekstraksi RSS gagal."""
    kw = kata_kunci(judul)
    if not kw:
        return ""
    try:
        r = subprocess.run(["/opt/hatch/bin/image-search", kw, "--max-results", "3"],
                           capture_output=True, text=True, timeout=40)
        data = json.loads(r.stdout)
        for res in data.get("results", []):
            url = res.get("media_url") or ""
            if not url.startswith("https://"):
                continue
            if "watermark" in url.lower():
                continue  # tolak gambar ber-watermark
            # preflight: pastikan URL hidup & bertipe gambar
            h = subprocess.run(
                ["curl", "-fsSLI", "-A", "Mozilla/5.0", "--connect-timeout", "8",
                 "--max-time", "15", url],
                capture_output=True, text=True, timeout=25)
            if "200" in (h.stdout.splitlines() or [""])[0] and "image/" in h.stdout.lower():
                return url
    except Exception:
        pass
    return ""

# dipakai di bawah sebagai last resort absolut (selalu ada gambarnya)
def gambar_default(blog):
    import hashlib
    seed = hashlib.md5(blog.encode()).hexdigest()[:8]
    return f"https://picsum.photos/seed/{blog}{seed}/1080/1080"


def main():
    seen = load_seen()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=36)
    items = []
    for source, url in FEEDS.items():
        try:
            d = feedparser.parse(url)
        except Exception as e:
            print(f"[{source}] gagal: {e}")
            continue
        for e in d.entries:
            link = (e.get("link") or "").strip()
            title = (e.get("title") or "").strip()
            if not link or not title:
                continue
            key = norm(title)[:80]
            if key in seen:
                continue
            pub = e.get("published_parsed") or e.get("updated_parsed")
            if pub:
                dt = datetime(*pub[:6], tzinfo=timezone.utc)
                if dt < cutoff:
                    continue
            else:
                dt = datetime.now(timezone.utc)
            summary_raw = e.get("summary", "") or e.get("description", "")
            summary = re.sub(r"<[^>]+>", "", summary_raw).strip()
            # Ekstrak URL gambar: enclosures -> media_content/thumbnail -> <img> summary
            gambar = ""
            for enc in (e.get("enclosures") or []):
                href = (enc.get("href") or "").strip()
                if href and enc.get("type", "").startswith("image/"):
                    gambar = href
                    break
            if not gambar:
                for mc in (e.get("media_content") or []):
                    href = (mc.get("url") or "").strip()
                    if href:
                        gambar = href
                        break
            if not gambar:
                for mt in (e.get("media_thumbnail") or []):
                    href = (mt.get("url") or "").strip()
                    if href:
                        gambar = href
                        break
            if not gambar:
                m_img = re.search(r'<img[^>]+src="([^"]+)"', summary_raw)
                if m_img:
                    gambar = m_img.group(1).replace("&amp;", "&")
            # Fallback: scrape og:image dari halaman artikel
            if not gambar:
                try:
                    import urllib.request
                    req = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
                    html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "ignore")
                    m_og = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', html)
                    if not m_og:
                        m_og = re.search(r'<meta[^>]+content="([^"]+)"[^>]+property="og:image"', html)
                    if m_og:
                        gambar = m_og.group(1).replace("&amp;", "&")
                except Exception:
                    pass
            # Fallback: cari gambar relevan via image-search
            if not gambar:
                gambar = gambar_fallback(title)
            # Last resort: JAMINAN selalu ada gambar
            if not gambar:
                gambar = gambar_default(BLOG_NAMA)
            items.append({
                "judul_asli": title,
                "link": link,
                "ringkasan": summary[:800],
                "sumber": source,
                "tanggal": dt.isoformat(),
                "gambar": gambar,
            })
            seen.add(key)
    # dedupe antar-feed berdasar kemiripan judul
    unik, judul_seen = [], set()
    for it in sorted(items, key=lambda x: x["tanggal"], reverse=True):
        k = norm(it["judul_asli"])[:50]
        if k in judul_seen:
            continue
        judul_seen.add(k)
        unik.append(it)
    antrean = unik[:MAX_PER_RUN]
    with open(ANTREAN_FILE, "w") as f:
        json.dump(antrean, f, ensure_ascii=False, indent=1)
    save_seen(seen)
    print(f"OK: {len(antrean)} berita masuk antrean")
    for a in antrean:
        print(" -", a["judul_asli"][:70])

if __name__ == "__main__":
    main()
