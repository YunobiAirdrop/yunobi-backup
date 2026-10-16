# Alpha, and where it silently fails

The longest and most failure-prone part of this kit. An overlay that renders without its alpha channel looks correct in every preview and is wrong in the edit, so this is read rather than recalled.

## Alpha is where this silently fails

`remotion.config.ts` sets h264 for the b-roll. An overlay that inherits it renders clean, exits
zero, and arrives as a video with a black rectangle where the transparency should be. Nothing
catches it except opening the file over footage, which is exactly the silent-invisibility failure
`motion-design` is built around.

**The shelf ships QuickTime Animation (`qtrle`) in a MOV, not WebM.** A six-format pack was tested
in Descript himself and reported back: every MOV keys, GIF keys, WebM does not. The eight WebM files
were never faulty, both alpha checks pass on all of them. Descript simply imports a VP9 alpha WebM
and flattens it. Descript's *Supported file types* page is a container x codec table that promises
transparency for nothing, so importable and keyable are separate claims and only the test settled
the second.

qtrle rather than ProRes 4444, which also keys: QuickTime Animation stores ARGB directly, so it is
lossless with no RGB→YUV step at all, where ProRes 4444 is 12-bit YUV applied to an 8-bit RGBA
source: more bits, less exact, five times the size. Sizes: qtrle 7-25MB, ProRes 30-100MB, HEVC
~0.6MB but lossy, WebM 0.2-0.9MB. GIF keys too and is not shipped, its alpha being 1-bit.

The qtrle figures roughly tripled when the frost layer went in, and that is expected rather than a
regression: QuickTime Animation is run-length encoding, and per-pixel grain is exactly what
run-length encoding cannot compress. It is the price of the surface, paid once per clip, and 25MB is
nothing for a file that lives on a local timeline. Do not "fix" it by dropping the grain.

**The file size is the statement's length, and nothing else.** Measured on `cta-skool`: the hold
costs zero bytes per frame, because a still pane is one RLE run; the whole bill is the ~20 entrance
frames and the ~8 exit frames, where the pane fades and scales and every pixel in it changes. So the
bill is the pane's area times those frames, and on a fixed-height shape the pane's area is its
width. Two measured points, ink box including the glow spill against the shipped MiB:
1380px/23.9MiB on `cta-call`, 1518px/26.3MiB on the first cut of `cta-skool` — the same ratio to
within a percent. **A hero statement past about 21 characters crosses Cloudflare's 25MiB per-asset
ceiling and fails the whole app's deploy.** Measure a candidate before rendering it, in seconds,
with `remotion still --props='{...}'` and `magick -format "%@"`; the entrance is the only other
lever and its 10-frame settle is shared by all three shapes, so shorten the words.

Remotion cannot write qtrle, so the render is two steps and `render:youtube-ctas-mov` does both:

```bash
remotion render src/index.ts <CompId> <out>.mov \
  --config=remotion.prores.config.ts --codec=prores --prores-profile=4444 \
  --pixel-format=yuva444p10le --image-format=png
ffmpeg -v error -i <out>.mov -c:v qtrle -pix_fmt argb -c:a copy -y <shelf>.mov
```

`remotion.prores.config.ts` exists because the default config sets `Config.setCrf(16)` and ProRes
has no CRF, so a ProRes render through the b-roll config dies before it writes a frame. `-c:a copy`
carries the sound track through untouched; `-an` there silently throws it away. `-g 600` is not
optional either: ffmpeg writes a full qtrle keyframe every 12 frames by default, which on clips that
hold still is about a third of the kit's total size in pure redundancy.

**A WebM twin still gets rendered, as the browser preview.** No browser decodes QuickTime Animation,
so a `<video src="*.mov">` tile on `/design/shelves` is a blank rectangle and `drawImage` off it an
empty canvas. `render:youtube-ctas` writes vp9 into `design/youtube-ctas-preview/`, the shelf plays
that, and download and drag hand over the MOV. That is the WebM's only remaining job, which is why
`alphaPreviewWebm` is named as it is: the Studio gives you the preview, the CLI the deliverable. Do
not put `defaultCodec: "prores"` in that file, the config's CRF kills it as it kills the CLI.

On Remotion 4.0.504 the alpha defaults must go through `calculateMetadata`. `defaultCodec`,
`defaultPixelFormat` and `defaultVideoImageFormat` are `<Composition>` props in the 4.0.512 docs
and do not exist in `CompositionProps` here, so passing them there fails the typecheck.

**Verify the alpha, do not assume it.** On the MOV, `ffprobe` must report `qtrle,argb` and an empty
corner must decode transparent. On the WebM, `ffprobe` reports `yuv420p` even on a correct file,
because WebM keeps alpha in a side channel rather than in the pixel format.

```bash
# the shipped MOV
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,pix_fmt -of csv=p=0 out.mov
ffmpeg -v error -ss 1.5 -i out.mov -vframes 1 -y /tmp/f.png
magick /tmp/f.png -format "%[pixel:p{10,10}]\n" info:      # expect srgba(0,0,0,0)

# the preview WebM
ffprobe -v error -show_entries stream_tags -of json out.webm   # expect alpha_mode: "1"
ffmpeg -v error -vcodec libvpx-vp9 -i out.webm -vframes 1 -pix_fmt rgba -f rawvideo - \
  | head -c 4 | xxd    # expect 00000000
```

`cta-end-card` is the one file whose corner is not transparent, and that is correct: it is a
full-frame dark bed by design and reads `srgba(0,5,20,0.86)` once its scrim is up.

What each overlay sounds like, and the ducking it needs, is in
[references/sound.md](sound.md).
