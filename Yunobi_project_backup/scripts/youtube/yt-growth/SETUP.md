# Setup yt-growth (sekali saja, ~15 menit + klik OAuth per channel)

Toolkit ini membaca analitik asli channel (views, CTR, retensi) dan bisa
me-refresh judul/deskripsi/tag video langsung via API resmi YouTube — gratis,
tanpa VidIQ/TubeBuddy, tanpa DataForSEO.

## Yang harus Yunobi lakukan (tidak bisa diwakilkan)

### 1. Buat project di Google Cloud Console (5 menit)
1. Buka https://console.cloud.google.com/ (login khususstokyunobi@gmail.com)
2. Buat project baru, nama mis. `yt-growth`
3. Di project itu, aktifkan 2 API:
   - **YouTube Data API v3**
   - **YouTube Analytics API**
   (cari di "APIs & Services > Library", klik Enable)
4. "APIs & Services > OAuth consent screen":
   - User type: **External**, isi nama aplikasi `yt-growth` + email kamu, simpan
   - Di "Test users", tambahkan `khususstokyunobi@gmail.com`
5. "APIs & Services > Credentials > Create Credentials > OAuth client ID":
   - Application type: **Desktop app**, nama `yt-growth`
   - Download JSON-nya → kirim ke saya (upload file di chat)

Saya yang simpan ke `~/.hermes/yt-growth/client_secret.json` (izin 600).

### 2. Otorisasi per channel (17x, @~1 menit tiap) — ✅ SELESAI 2026-10-08
Cara yang terbukti jalan (ditemukan lewat trial, 2026-10-08):
1. Buka link yang saya kasih di browser HP, login khususstokyunobi@gmail.com
2. **Klik akun Google utama dulu** — layar "Choose an account" TIDAK memuat
   pilihan channel; pemilih channel muncul SETELAH itu, pilih nama channel
   yang saya sebutkan (mis. "Lima Misteri"), BUKAN "khususstokyunobi"
3. Klik Allow/Setuju
4. Browser menampilkan error "This site can't be reached" (localhost) —
   normal. Salin SELURUH URL dari address bar, kirim ke saya
   (contoh: `http://localhost:8080/?state=...&code=4/0AX...`)
5. Saya tukarkan kode jadi token (tersimpan per channel di
   `~/.hermes/yt-growth/tokens/`, izin 600; kode tukar PKCE disimpan di
   `pkce.json` karena kode dari URL user perlu di-unquote)

Catatan: token TERIKAT PER CHANNEL — 1 token tidak bisa dipakai untuk
channel lain, jadi 17 token wajib (bukan 1 untuk semua).

### 3. Selesai
Setelah 17 token aktif ✅ (2026-10-08, `auth.py status` → 17/17),
cron mingguan `yt-seo-refresh-mingguan` sudah aktif: tiap Senin pagi
menarik analitik 17 channel, menemukan video views rendah berumur >90 hari,
dan menyiapkan judul/deskripsi baru (pakai formula packaging).
Eksekusi perubahan metadata TETAP butuh ketukan kamu.

## Catatan kuota (gratis)
- YouTube Data API: 10.000 unit/hari per project (laporan mingguan 17 channel
  hanya pakai ratusan unit — sangat cukup).
- YouTube Analytics API: kuota terpisah, longgar untuk pemakaian ini.
