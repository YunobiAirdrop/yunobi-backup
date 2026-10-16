# 07 — Kredensial (DAFTAR LOKASI SAJA)

> ⛔ **Dokumen ini TIDAK berisi nilai kredensial apa pun.**
> Semua file di bawah ini harus **dibuat manual di mesin baru** (atau dipindah
> via jalur aman). Jangan pernah commit nilai kredensial ke repo.

## File kredensial (permission 600)

| Lokasi | Isi | Cara buat ulang |
|---|---|---|
| `~/.hermes/.env` | OpenRouter API key Yunobi, `COMPOSIO_CONSUMER_KEY`, `NINEROUTER_API_KEY` | Isi manual dari catatan user |
| `~/.hermes/google-oauth-blogger.env` | OAuth Client ID + Secret Google (project Blogger) | Google Cloud Console → buat ulang |
| `~/.hermes/blogger-tokens.json` | Token OAuth Blogger (auto-refresh) | Flow manual: auth URL → tambah redirect URI `http://127.0.0.1:8080/` → test user → kode otorisasi → token |
| `~/.hermes/.dashboard-pw` | Password dashboard 9Router | Set manual |
| `~/.config/ngrok/ngrok.yml` | Token ngrok (paket gratis — praktis tidak berguna) | ngrok.com |
| `~/workspace/youtube-otomatis/yt-growth/` token OAuth | 17 token OAuth per channel (project `yt-growth-510917`, client `yt-growth-desktop`) | User klik manual per channel via HP (pemilih channel muncul SETELAH klik akun utama) |
| `/etc/9router-proxy.env` | Proxy env untuk 9Router (`NODE_USE_ENV_PROXY=1`, CA bundle) | Salin dari mesin lama |

## Secure Vault (runtime)

- Login Google `khususstokyunobi@gmail.com` (dipakai browser task YouTube + Blogger).
- Login Shopee via Google OAuth (`stokakunwebyunobi@gmail.com`).
- Password browser: ada yang TRANSIENT (mis. "Sepuluh10" — TikTok) → **jangan
  disimpan/di-quote di mana pun**; minta ulang ke user saat dibutuhkan.

## Akun & login

| Akun | Dipakai untuk |
|---|---|
| khususstokyunobi@gmail.com | 18 channel YouTube + 10 blog Blogger (login browser) |
| akuntyunobi17@gmail.com | Gmail utama operasi (1 Gmail policy) |
| stokakunwebyunobi@gmail.com | Shopee Affiliate (OAuth) |
| @beritaviraldotcom (IG), @beritaviraldotcom + @ngewebyuk (Threads), FB Page BeritaViraldotcom | Promo afiliasi (instagram-cli / threads-cli / facebook-cli) |
| @ngeweb.yuk (TikTok) | TikTok Shop Affiliate + FYP |

## Checklist mesin baru

1. [ ] Buat `~/.hermes/.env` (600) — 3 key
2. [ ] Buat `~/.hermes/google-oauth-blogger.env` (600)
3. [ ] Jalankan flow OAuth Blogger → `blogger-tokens.json` (600)
4. [ ] Isi Secure Vault: login Google, Shopee
5. [ ] OAuth ulang 17 channel yt-growth (klik manual via HP)
6. [ ] Verifikasi `hermes doctor` lolos + `hermes -z` tidak 402 (butuh top-up kredit)
