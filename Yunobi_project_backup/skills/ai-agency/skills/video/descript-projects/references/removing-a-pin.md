# Taking a clip off a card: the transparent plate

Split out of `SKILL.md`. Read it when a placed clip has to come off the timeline.

## Lifting a pin off the timeline: the transparent plate

`media swap` repoints a pin at different media and `rm` deletes media, but **nothing removes a pin**,
so a clip placed on a card cannot simply be taken off from the terminal. The way round it is the
project's own alpha convention: Descript composites an alpha `.mov` pin over the camera, so a fully
transparent qtrle clip cut to the card's exact length hands that card back to the face underneath.

```sh
ffmpeg -y -f lavfi -i "color=c=black@0.0:s=1920x1080:r=30:d=<card seconds>,format=argb" \
  -vcodec qtrle -t <card seconds> plate.mov
```

Import it, `media swap` the unwanted clip for it, then `rename` and `mv` the survivor, because a
swap keeps the **old media's id and name** and consumes the new one. Card lengths come from the
document: anchor each card boundary to its tau, add `offsetFromAnchor`, and the gap to the next
boundary is the length. Match it or go a few hundredths over; short media freezes on its last frame.

**Swap by media id, never by name.** A project routinely holds two copies of the same stock clip and
a name match silently picks the unplaced one, which looks like a successful swap and changes nothing
on screen. Read the placed media's id out of the pin scene first.

