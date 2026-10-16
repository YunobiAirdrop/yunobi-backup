# UPLOAD PLAN — Strange Tales (@StrangeTales-g6n) — 2026-10-16
# Dieksekusi pada jendela ketukan persetujuan user 20:00–23:00 WIB via browser task.

## Akun
- Google login: khususstokyunobi@gmail.com (kredensial di Secure Vault; 2FA via ketuk HP user)
- Channel: Strange Tales — handle @StrangeTales-g6n (channel_id UCAVSqZjG8Af_pm_1uD5wRzA)

## Video (3 shorts, 1080x1920, <100MB, voice Miles, AI disclosure WAJIB dicentang)
1. FILE: /home/hatch/workspace/youtube-otomatis/strange-tales/2026-10-16/strangetales-s1-2026-10-16.mp4
   JADWAL: 2026-10-16 21:00 WIB (Scheduled, bukan publish langsung)
   JUDUL: Fish Fall From the Sky in Honduras — Real?! #shorts #weirdfacts #strangetales
   DESKRIPSI: (lihat s1/upload-meta.md — salin persis)
2. FILE: /home/hatch/workspace/youtube-otomatis/strange-tales/2026-10-16/strangetales-s2-2026-10-16.mp4
   JADWAL: 2026-10-17 03:00 WIB (Scheduled)
   JUDUL: This Glacier in Antarctica BLEEDS Red — Real?! #shorts #weirdfacts #strangetales
   DESKRIPSI: (lihat s2/upload-meta.md — salin persis)
3. FILE: /home/hatch/workspace/youtube-otomatis/strange-tales/2026-10-16/strangetales-s3-2026-10-16.mp4
   JADWAL: 2026-10-17 07:00 WIB (Scheduled)
   JUDUL: These Rocks Move Alone Across the Desert — Real?! #shorts #weirdfacts #strangetales
   DESKRIPSI: (lihat s3/upload-meta.md — salin persis)

## Instruksi browser task
- Buka YouTube Studio (studio.youtube.com) dengan akun di atas; pilih channel Strange Tales bila multi-channel.
- Upload satu per satu via tombol Create > Upload videos; set Title, Description, Tags persis dari upload-meta.md.
- Pada langkah "Altered content / AI disclosure": pilih YA/CENTANG (konten dibuat dengan AI).
- Visibility: Schedule → set tanggal & jam WIB sesuai di atas (pastikan timezone Asia/Jakarta).
- Shorts terdeteksi otomatis dari aspek 9:16 + durasi <60 dtk. Jangan set sebagai Premiere.
- Setelah 3 terunggah: VERIFIKASI di Content > Videos bahwa ketiganya berstatus "Scheduled" pada jam yang benar.
- Gagal karena BATAS HARIAN YouTube → JANGAN retry: tulis ~/workspace/youtube-otomatis/retry-queue/strangetales-2026-10-16.json
  format: {"date":"2026-10-16","channel":"@StrangeTales-g6n","items":[{"file":"...","title":"...","scheduled":"2026-10-16 21:00 WIB","status":"gagal-batas-harian"}, ...]}
  (watchdog 20:00 esok hari mengeksekusi antrean ≥23 jam). Gagal sebab lain → retry segera saat itu juga.

## Catatan produksi V2
- V1 (Lead Masks/Sodder/Dyatlov) DIBATALKAN karena tidak cocok gaya channel (lihat archive-v1-offstyle/ALASAN.txt).
- V2 = fenomena alam misterius sesuai gaya channel 100%: Lluvia de Peces, Blood Falls, Sailing Stones.
- SFX rekaman asli: TIDAK tersedia di VM ini (library backup hanya berisi manifest, tanpa file audio) → video tanpa bed SFX; dicatat sebagai gap.
