# Backup Repo — Operasi Konten Otomatis Yunobi

Repo ini adalah **dokumentasi + script portabel** seluruh operasi konten otomatis yang
dibangun sejak 2026-09-30. Tujuannya: kalau suatu hari project dipindah ke mesin
atau asisten lain, semuanya bisa jalan lagi **tanpa mulai dari 0**.

> ⚠️ **Repo ini TIDAK berisi kredensial.** Semua API key, token OAuth, password,
> dan secret HARUS dibuat ulang manual di mesin baru. Lihat `docs/07-kredensial.md`
> untuk daftar lengkap lokasi kredensial.

## Isi repo

| Path | Isi |
|---|---|
| `docs/01-perjalanan.md` | Kronologi 2026-09-30 → 2026-10-08: pivot & keputusan besar |
| `docs/02-blog-otomatis.md` | 10 blog Blogger, pipeline `jalan.sh`, volume 6/hari |
| `docs/03-youtube.md` | 18 channel YouTube, aturan anti-mogok, batas 24 jam |
| `docs/04-tiktok.md` | Pivot konten FYP TikTok (syarat 600 followers) |
| `docs/05-afiliasi-shopee.md` | 36 produk Shopee, pipeline promo harian |
| `docs/06-cron.md` | Daftar semua cron aktif + jadwal + perintah |
| `docs/07-kredensial.md` | **Daftar lokasi kredensial (tanpa nilai)** — dibuat manual |
| `docs/08-skills.md` | Skill terpasang (11 paket) + lokasi |
| `docs/09-keputusan-user.md` | Preferensi & penolakan user — JANGAN ditawarkan ulang |
| `scripts/` | Script kunci (sudah disanitasi dari secret) |
| `.gitignore` | Abaikan media, data, token, env |

## Arsitektur singkat

```
blog-otomatis/          Pipeline 10 blog: fetch → trending → tulis_ulang → posting_web
                        (posting via browser web UI — Blogger API diblokir Google)
youtube-otomatis/       18 channel: produksi video (ffmpeg) → upload via browser task
                        (upload butuh ketukan persetujuan user 20:00–23:00 WIB)
kisah-islami/ dkk       4 channel agama: footage Pexels (bukan AI)
tiktok-shop-affiliate/  Konten FYP TikTok @ngeweb.yuk (pivot: kejar 600 followers)
skills/                 11 paket skill (SEO, humanizer, YouTube, TikTok, afiliasi)
```

## Cara pakai repo ini di mesin baru

1. Baca `docs/01-perjalanan.md` untuk konteks, lalu `docs/09-keputusan-user.md`
   (aturan main yang TIDAK boleh dilanggar).
2. Siapkan kredensial sesuai `docs/07-kredensial.md` (OAuth Google, OpenRouter key,
   login browser, Secure Vault).
3. Salin `scripts/` ke lokasi kerja, sesuaikan path absolut (`/home/hatch/workspace/...`).
4. Daftarkan ulang cron sesuai `docs/06-cron.md`.
5. Install skill sesuai `docs/08-skills.md`.

## Prinsip operasional (ringkas)

- **Ketukan persetujuan user 20:00–23:00 WIB** untuk semua posting/upload — jangan
  pernah bypass, jangan biarkan ketukan terbuang untuk upload yang pasti gagal.
- **Verifikasi sebelum lapor**: setiap posting/upload harus dicek benar-benar
  tayang di tujuannya sebelum dilaporkan berhasil.
- **Bahasa Indonesia**, singkat, padat, angka dulu — itu gaya komunikasi user.
- Jangan tawarkan ulang hal yang sudah ditolak user (lihat `docs/09-keputusan-user.md`).

---
*Disusun 2026-10-08 dari MEMORY.md + daily log 2026-10-01 s/d 2026-10-08.*
