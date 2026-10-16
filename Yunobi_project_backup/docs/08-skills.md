# 08 — Skill Terpasang

Lokasi: `~/workspace/skills/`. Total 11 paket (7 dipasang 2026-10-08 dini hari,
4 paket YouTube dipasang 2026-10-08 malam).

## Paket GitHub (7)

| Paket | Isi | Dipakai untuk |
|---|---|---|
| marketingskills | 50 skill: seo-audit, copywriting, content-strategy… | SEO & strategi konten |
| last30days-skill | Riset tren 30 hari terakhir | `trend_radar.py` (topik baru + celah konten) |
| humanizer | Anti-AI writing (Wikipedia "Signs of AI writing") | Prompt `tulis_ulang.py` |
| OpenMontage | 49 skill produksi video | Assembly Tiny Builders (preflight, quality gate, production log) |
| affiliate-skills | 50 skill afiliasi | Riset program afiliasi (openAffiliate) |
| youtube-marketing-skills | 21 skill: hook, ideate, metadata… | Formula packaging judul/hook (`packaging-formulas.md`) |
| ai-agency | video-hooks | Hook video |

**Audit**: repo bersih; `engagement-bot` di youtube-marketing **DITOLAK**
(melanggar ToS YouTube).

## Paket YouTube (4, 2026-10-08)

| Paket | Repo | Isi |
|---|---|---|
| yt-yutu | eat-pray-ai/yutu | CLI + MCP + skill: upload, SEO, komentar, playlist, branding (Go, perlu build) |
| yt-youtube-mcp | postoncehq/youtube-mcp | 9 skill: title/description/tag/script/shorts-script/thumbnail/calendar/channel-description |
| yt-youtube-agent-skill | nessalazne/youtube-agent-skill | 12 skill: audit, chapters, comment, edit, package, plan, **publish** (via Blotato, butuh approval eksplisit), retention, script, seo, shorts, viral |
| yt-youtube-skills | ZeroPointRepo/youtube-skills | 12 skill: transcript, captions, subtitles, youtube-api, data, search, channels, playlist |

**Hasil pencarian jujur**: tidak ada skill yang bisa bypass limit upload 24 jam
YouTube (server-side). Semua skill di atas pakai API resmi.

## Skill lain di workspace

`bloggingskills` (humanize+SEO blog), `tiktok-skills`, `viral-hooks-skill`
(100 formula), `taisly-agent` (auto-posting), `social-media-pro-max`,
`email-marketing-bible`, `seo-skills`, `Youtube-clipper-skill`, `vidmoat-skills`,
`vertical-video-editing-skill`, `creator-knowledge`, `antigravity-awesome-group-skills`.

## Cara pasang ulang

```bash
cd ~/workspace/skills
git clone --depth 1 https://github.com/eat-pray-ai/yutu.git yt-yutu
git clone --depth 1 https://github.com/postoncehq/youtube-mcp.git yt-youtube-mcp
git clone --depth 1 https://github.com/nessalazne/youtube-agent-skill.git yt-youtube-agent-skill
git clone --depth 1 https://github.com/ZeroPointRepo/youtube-skills.git yt-youtube-skills
# 7 paket pertama: pasang via skill_creator / salin manual (daftar di atas)
```
