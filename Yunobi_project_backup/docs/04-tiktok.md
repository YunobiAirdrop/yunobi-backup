# 04 — TikTok (@ngeweb.yuk)

## Status akun

- Akun: **@ngeweb.yuk** ("mis racun belanja"), TikTok Shop Affiliate AKTIF
  (terdaftar 2026-10-08 via aplikasi HP).
- Login browser berhasil. Posting via **Taisly** (skill `taisly-agent`).

## PIVOT FYP (2026-10-08, keputusan user)

> "ga bisa harus 600 pengikut, selama pengikut belum terpenuhi upload random
> saja kaya drama dll"

- Tempel produk / keranjang kuning butuh **600 followers** (akun baru: 5).
- Mode review produk **DIHENTIKAN SEMENTARA** (cron `tiktok-shop-review-harian`
  disabled; 38 produk + SOP tersimpan untuk nanti).
- Pengganti: **konten hiburan viral** — mini drama bersambung (cliffhanger),
  komedi skit, tebak-tebakan, fakta unik. SOP: `fyp-content.md`.
- Cron **`tiktok-fyp-harian`** — daily ~10:11 WIB, posting OTOMATIS via Taisly.
- Tiap laporan tanya jumlah followers; saat user konfirmasi 600 → aktifkan
  lagi review-harian.

## Pipeline review (arsip — aktif lagi setelah 600 followers)

- 38 produk di `produk.json` (17 komisi >Rp5.000: serum bulu mata Rp201.800,
  kipas mini Rp40.000, Medikacare Rp32.800; 21 tambahan Rp2.360–4.988).
- SOP (`SOP.md`): video ±30 dtk, alur TETAP: hook → demo pemakaian AI presenter
  → komentar terbaik → CTA keranjang kuning. Hook/angle BERBEDA tiap video.
- Komisi bisa berubah sewaktu-waktu (cek dashboard affiliate).
- Cron `tiktok-shop-ganti-produk` tiap 336 jam: ingatkan kirim produk baru.

## Skill terkait

- `tiktok-skills` (script, caption, hook FYP), `viral-hooks-skill` (100 formula hook),
  `taisly-agent` (publishing otomatis TikTok/IG Reels/YT Shorts/X/FB).
- Skill khusus TikTok-affiliate TIDAK ADA — dipakai tiktok-skills + viral-hooks.
