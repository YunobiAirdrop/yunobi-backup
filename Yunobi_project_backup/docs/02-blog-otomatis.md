# 02 — Blog Otomatis (10 Blog)

## Daftar blog

| Key | Nama blog | Blog ID | Niche |
|---|---|---|---|
| kabarviral | KabarViral | 2214484859238970994 | campuran (blog utama) |
| teknopedia | TEKNO PEDIA | 7454786879662803920 | teknologi |
| infokesehatan | info kesehatan hari ini | 4472618985643360981 | kesehatan |
| ekonomibisnis | ekonomi bisnis info | 3837990085079931876 | keuangan |
| gayahidup | Gaya Hidup Kekinian | 6262982910681826900 | hiburan |
| olahraga | olahraga terbaru | 3309326452444173317 | olahraga |
| wisata | WisataIndo | 7833035171023355034 | wisata |
| kuliner | KulinerNusantara | 5675665322743920850 | kuliner |
| otomotif | OtomotifInfo | 2186034656474186441 | otomotif |
| pendidikan | PendidikanCerdas | 1839534200092814818 | pendidikan |

Config: `blog-otomatis/config.json`. Semua `artikel_per_hari=1`.

## Volume (aturan user 2026-10-05)

**6 artikel/hari total**: KabarViral SELALU dapat 1 (blog utama), 5 artikel lainnya
rotasi ke 5 blog berbeda tiap hari dari 9 sisanya. File `rotasi-blog.txt` mencatat
giliran — dibaca & diupdate tiap run. Evergreen & digest **nonaktif**.

## Pipeline (`./jalan.sh` di `blog-otomatis/`)

```
fetch_berita.py  →  trending.py  →  per blog terpilih:
  tulis_ulang.py (1 artikel, humanizer anti-AI + SEO)
  baca_juga.py
  posting_web.py → tulis instruksi ke data/webpost/instruksi-{blog}.txt
                 → cetak SPAWN_BROWSER_TASK:{blog}:{n}
```

Setelah `jalan.sh`: untuk tiap blog, spawn **maks 2 browser task paralel** dengan isi
file instruksi → posting via **blogger.com web UI** (login khususstokyunobi@gmail.com).
Artikel terposting: pindahkan `data/artikel-{blog}.json` → `data/artikel_terkirim-{blog}.json`.

## Kenapa via web UI (PENTING)

- **Blogger API diblokir Google sejak 2026-10-03** (pelanggaran kebijakan, global).
  Baca masih bisa, posting via API ditolak. Banding pernah diajukan.
- Mail-to-Blogger aktif tapi **tidak diproses** (tidak tayang/draf/balasan).
- Browser terkelola **tidak bisa akses localhost VM** → artikel harus ditempel
  di deskripsi browser task, bukan via URL lokal.

## Kuota AI

- OpenRouter free-tier: 50 req/hari/akun, reset 07:00 WIB. Rotasi 9 key ≈ 450 req/hari.
- `tulis_ulang.py`: budget **24 percobaan/artikel** + backoff 20s. Model 429/503 →
  catat, jangan spam retry.
- Urutan MODELS: `gemma-4-26b` dulu (2026-10-08: nemotron-3.5-lightning konsisten
  return non-JSON dan menghabiskan budget).
- Kuota dipakai bersama `bikin_resep.py` + pipeline blog (~63 req/hari).
- Share scripts butuh `artikel-{blog}.json` di **pipeline ROOT** (bukan data/) —
  agregatkan dari batch harian (cp-*.json, sh-*.json, tk-*.json, mini-*.json),
  skip rewrite gagal (judul "...").

## Cron terkait

- `blog-otomatis-harian` — daily 15:11 WIB (goal: kabarviral-automated-news-blog)
- `verifikasi-pagi-blog` — daily 17:11 WIB: cek feed publik vs snapshot kemarin +
  cek bounce Gmail 24 jam
- `share-ig-harian` — daily 20:11 WIB: IG reel → video_script → thread_gen → FB → Threads
- `ekspansi-blog-2mingguan` — tiap 336 jam (run pertama 2026-10-17): buat 10 blog
  baru via browser + tema + config + halaman statis. Antrean niche: `niche-rotasi.json`.

## Aturan konten

- **Duplikat antar blog DITOLAK** (penalti Google/AdSense).
- Tema v1.19 (5 varian warna) terpasang semua blog; backup tema KabarViral 55KB.
- Postingan IG wajib hashtag. Caption IG: 6 framework (cerita, before/after,
  masalah-solusi, hot take, listicle, rekomendasi jujur).
- Gambar: fallback RSS → og:image → image-search (tolak watermark) → picsum;
  validasi magic bytes; rusak → posting diskip.
