## Publishing to the shelf

In dev, `/design/shelves` reads the folder directly, so dropping the file in is the whole publish
step. The deployed app has no filesystem, so the shelf it serves comes from
`src/lib/design-assets/assets.generated.ts`, which `pnpm dev` and `pnpm build` both rewrite
(the app's `gen:design-manifest` script runs it alone). A new *shelf* also needs its entry
in `src/lib/design-assets/groups.ts`; the boxes are `product-boxes`. A new clip reaches the
deployed app and the shared library at `/assets` on the next deploy, not before.
 Three things had to be true for any of it to work, and all three are done:

- `src/lib/server/design-assets.ts` matches `VIDEO_RE` as well as `IMAGE_RE` and tags each file
  `kind`, for both the live read and the generated listing.
- The gallery renders `<video autoplay loop muted playsinline>` for `kind: "video"`. A poster frame
  is wrong here: these overlays are bought for their timing, and a still of a CTA is just a button.
- Getting a clip off the shelf is a drag, not a copy. A page cannot put a file on the operating
  system's clipboard: `navigator.clipboard.write` takes PNG, plain text and HTML, and nothing else
  reaches a native app. So the copy button hands over one mid-clip frame, and the tile sets
  `DownloadURL` on its drag event, which drops the real `.mov` into Descript, Premiere or the
  Finder. The tile, the lightbox stage and the filmstrip all play `preview?.url ?? url`, because
  the shipped MOV renders as a blank rectangle in a browser.
