# Remotion API reference

Vendored from Remotion's own agent-skills package, unedited: `remotion/remotion-*/`, each a
router into its own `REFERENCE.md`. Look up the mechanism here; the craft decisions above
(the direction gate, the motion vocabulary, the registers) still govern what gets built.

Preserve user changes: a user may edit generated code outside the conversation. If a change in
the working tree looks surprising, do not overwrite it. Assume it was intentional, or ask.

| Job | Reference |
|---|---|
| Create a video or a new Remotion project | [remotion-create/REFERENCE.md](remotion/remotion-create/REFERENCE.md) |
| Writing Remotion React Markup | [remotion-markup/REFERENCE.md](remotion/remotion-markup/REFERENCE.md) |
| Static maps, animated routes, GeoJSON, Mapbox, MapLibre, MapTiler, 3D flyovers | [remotion-maps/REFERENCE.md](remotion/remotion-maps/REFERENCE.md) |
| Trimming, cropping or reading metadata from video in the browser | [remotion-multimedia/REFERENCE.md](remotion/remotion-multimedia/REFERENCE.md) |
| Structuring markup so Studio can write interactive edits back to code | [remotion-interactivity/REFERENCE.md](remotion/remotion-interactivity/REFERENCE.md) |
| Rendering beyond a plain `npx remotion render` | [remotion-render/REFERENCE.md](remotion/remotion-render/REFERENCE.md) |
| Opening or configuring Remotion Studio | [remotion-studio/REFERENCE.md](remotion/remotion-studio/REFERENCE.md) |
| Captions: generating, displaying, importing SRT | [remotion-captions/REFERENCE.md](remotion/remotion-captions/REFERENCE.md) |
| A Remotion-powered SaaS: `<Player>`, Lambda, Vercel, Cloudflare, Express.js | [remotion-saas/REFERENCE.md](remotion/remotion-saas/REFERENCE.md) |
| Looking up current Remotion API docs | [remotion-docs/REFERENCE.md](remotion/remotion-docs/REFERENCE.md) |
| Upgrading Remotion, related and Mediabunny packages, installed skills | [remotion-upgrade/REFERENCE.md](remotion/remotion-upgrade/REFERENCE.md) |

**Re-vendoring:** these sub-directories track upstream Remotion Agent Skills verbatim. Don't
edit them here; pull a fresh copy from the published package and replace the `remotion/`
subdirectory whole, keeping this router file and the craft sections in `SKILL.md` untouched.
