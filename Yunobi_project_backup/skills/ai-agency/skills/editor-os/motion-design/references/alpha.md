# Alpha, and where it silently fails

The longest and most failure-prone part of this kit. An overlay that renders without its alpha channel looks correct in every preview and is wrong in the edit, so this is read rather than recalled.

## Alpha is where this silently fails

The project's `remotion.config.ts` sets h264 for opaque clips. An overlay that inherits it renders clean, exits
zero, and arrives as a video with a black rectangle where the transparency should be. Nothing
catches it except opening the file over footage, which is exactly the silent-invisibility failure
this skill is built around.

**Two lanes, two codecs, and picking the wrong one keys as a black rectangle.** A keyed clip going
onto an editor's timeline ships as **QuickTime Animation, `qtrle` with `argb` pixels, in a MOV**.
HEVC with alpha in a MOV is the lighter file, about a fifth of the size, and is the right one for a
shelf anybody downloads, because every plan of the editor reads it. But an HEVC-alpha MOV sideloaded
into an editor project has keyed as a black rectangle more than once, and the fix both times was
qtrle. So: "for the timeline" means qtrle, "for download" means HEVC.

**A MOV, not a WebM.** A six-format pack was tested in Descript: every MOV keys, GIF keys, WebM
does not. The WebM files were never faulty, both alpha checks pass on all of them. Descript simply
imports a VP9 alpha WebM and flattens it, and its *Supported file types* page promises transparency
for nothing, so importable and keyable are separate claims and only the test settles the second.

**qtrle is large for glass and grain.** Run-length coding gets one long run per scanline from an
opaque panel and none from a frosted one, so per-pixel grain is uncompressible. The same clips are
a fifth of the size as HEVC. Do not "fix" a large file by dropping the grain; check the bitrate
first. A host with an asset size cap is the other reason to ship HEVC.

Remotion cannot write HEVC or qtrle alpha, so the render is two steps, ProRes 4444 and then ffmpeg:

```bash
remotion render src/index.ts <CompId> <out>.mov \
  --config=remotion.prores.config.ts --codec=prores --prores-profile=4444 \
  --pixel-format=yuva444p10le --image-format=png
ffmpeg -v error -i <out>.mov -c:v hevc_videotoolbox -pix_fmt bgra \
  -alpha_quality 0.95 -b:v 40M -tag:v hvc1 -c:a copy -y <download>.mov
# for an editor timeline: ffmpeg -v error -i <out>.mov -c:v qtrle -pix_fmt argb -c:a copy -g 600 -y <timeline>.mov
```

`remotion.prores.config.ts` exists because the default config sets `Config.setCrf(16)` and ProRes
has no CRF, so a ProRes render through the opaque config dies before it writes a frame. `-pix_fmt
bgra` is what puts the alpha layer in; without it the file is opaque and nothing says so. `-c:a
copy` carries the sound track through untouched; `-an` there silently throws it away. `-b:v 40M` is
the top of the useful range: PSNR plateaus at 37.7dB above it, because the ceiling is
videotoolbox's 4:2:0 chroma rather than the bitrate.

**A WebM twin still gets rendered, as the browser preview.** No browser decodes an HEVC alpha layer,
so a `<video src="*.mov">` tile on a web page is a blank rectangle. Render a vp9 WebM for the page to
play and hand over the MOV on download. That is the WebM's only job, which is why `alphaPreviewWebm`
is named as it is: Remotion Studio gives you the preview, the CLI the deliverable. Do not put
`defaultCodec: "prores"` in the config, its CRF kills the render.

On Remotion 4.0.504 the alpha defaults must go through `calculateMetadata`. `defaultCodec`,
`defaultPixelFormat` and `defaultVideoImageFormat` are `<Composition>` props in the 4.0.512 docs
and do not exist in `CompositionProps` here, so passing them there fails the typecheck.

**Verify the alpha, do not assume it, and ffprobe cannot.** Both shipped formats keep alpha in a
side channel rather than in the pixel format, so `ffprobe` reports `yuv420p` on a correct file of
either kind. Worse, ffmpeg has no decoder for the HEVC alpha layer at all: it reads the MOV as
opaque and writes opaque frames from it, so an ffmpeg corner test passes a file that keys to a
black rectangle. AVFoundation is the only decoder on a Mac that reads the layer, so the check is a small Swift
script that decodes one frame through it and writes a PNG.

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 out.mov  # hevc or qtrle
# decode frame 1.5s through AVFoundation to /tmp/f.png (your small Swift script), then:
magick /tmp/f.png -format "%[pixel:p{10,10}]\n" info:      # expect srgba(0,0,0,0)

# the preview WebM
ffprobe -v error -show_entries stream_tags -of json out.webm   # expect alpha_mode: "1"
ffmpeg -v error -vcodec libvpx-vp9 -i out.webm -vframes 1 -pix_fmt rgba -f rawvideo - \
  | head -c 4 | xxd    # expect 00000000
```

A full-frame dark end card is the one overlay whose corner is not transparent, and that is correct:
it is a bed by design. Name it as an exception in your verifier rather than loosening the check.

What each overlay sounds like, and the ducking it needs, is in
[sound.md](sound.md).
