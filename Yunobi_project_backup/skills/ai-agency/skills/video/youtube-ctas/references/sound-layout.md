## The sound layout of a video

Where the sounds go, how loud, and how often. The kit itself is in `sound.md`; this is the system it
plays inside. Everything numbered here was measured off four Kallaway uploads (three 20s openers and
two 2-minute body sections, `yt-dlp -f bestaudio`, 48k stereo) rather than recalled.

### The four numbers the whole mix hangs off

| | measured on the reference | what to deliver |
| --- | --- | --- |
| Integrated loudness | **-13.1 to -14.4 LUFS** across five clips | -14 LUFS, which is YouTube's own target |
| Loudness range | **LRA 1.1 to 1.6** | under 2.0 |
| True peak | **-0.41 to -0.72 dBTP** | -1.0 dBTP on the master, -1.5 on any asset that will be re-encoded |
| Voice level | median **-20 dBFS** per 43ms frame, p90 -17 | the anchor everything else is set against |

**LRA 1.4 is the finding.** It means the loudest thing in the video and the quietest are about one
and a half decibels apart: the voice, the design hits and whatever music there is all sit on the same
line. That is not a mastering trick applied at the end, it is a mix where nothing is allowed to be
quiet. A video mixed with 8dB of range sounds amateur next to it at the same LUFS, because the
viewer's phone is competing with a room and every dip below the line is a dip into inaudible.

YouTube turns loud uploads down and never turns quiet ones up, so delivering under -14 LUFS is
volume given away for nothing.

### There is no music bed in the body

In the two body sections, the sustained gaps between sentences measure **-38 and -51 dBFS**. A bed
running under the voice would put a floor there 15-20dB higher. So: dry voice, and the music is a
device that arrives for a section and leaves, not a carpet under 12 minutes.

That is what makes the sparse design elements audible. Both halves of that sentence are load-bearing:
a bed forces every sound effect louder to be heard over it, and louder effects are what "over-edited"
means.

### The density law

| | a designed low hit | a sustained air move |
| --- | --- | --- |
| first 20 seconds | every **3-4s** | every **4s**, median length **0.17s** |
| body, minutes 3-5 | every **7.5s**, and in one video every 60s | every **7.5-11s** |

Roughly **four times the density in the opener as in the body**, and the body of a 12-minute video
carries something like 60-90 designed sounds in total, not 500. The count is not the craft; the
placement is.

Discriminating a real design element from speech, if this is ever re-measured: **energy below 60Hz
that a voice cannot produce** (sub share > 0.22 above -34 dBFS), and **air-dominated frames sustained
past 160ms**, which is longer than any sibilant.

### Which voice goes where

| the edit does this | the kit plays this | note |
| --- | --- | --- |
| a graphic arrives, a jump cut, a scene change | `whoosh` | on the frame, never one frame early |
| a menu, a selection, a state changing on screen | `ui` | 7 frames. It is a punctuation mark, not an event |
| a number, a result, a point landing | `chime` | no sub in it, so it can play over a word |
| a click on a screen recording | `click` | dry. Reverb on a click sounds like a stairwell |
| typing on a screen recording | `type-2s` / `type-4s` | already scattered; cut to length, never loop |
| the video starts, or the end card | `braam` or `hype` from the produced set | the two places a trailer sound is right |

There is no channel mark in the kit. `mark`, `open` and `cut` were written and cut on 27 Aug 2026;
the reference channel does not use one either, which is what the opener measurement said in the
first place.

### Six rules that keep it clean

1. **One element per beat.** Air or weight, never both, except in `mark` where the pair *is* the
   sound. Two design elements on one cut is the single most common way an edit reads as amateur.
2. **Never two cuts in a row.** If consecutive cuts both got a whoosh, delete one. The reference
   channel goes 7-11 seconds between them in the body.
3. **On the frame, not before it.** The transient lands on the first frame of the new shot. A sound
   that arrives early reads as a mistake even to someone who cannot say why.
4. **Silence is the loudest device.** Cut everything for a beat before the biggest claim. It costs
   nothing and no plugin does it for you.
5. **Leave 250Hz-3.5kHz to the voice.** Design sits below 160Hz or above 1kHz. Nothing in the clean
   kit has a fundamental in the voice band, which is why none of it needs ducking.
6. **Levels are baked in, not ridden.** Every file in `out/clean-kit/` already carries its own
   ceiling: the transition at -4 dBTP, the chime at -3, the mouse at -5, the typing runs at -7. Drop
   them in at unity and change nothing.

### Where a sound comes from, in order of preference

1. **The kit**, for anything whose object is simple enough to model: a struck bell, a switch, a
   mouse. It is exact to the frame and costs nothing.
2. **Generated locally**, when a texture is wanted that no oscillator will write - a room, a crowd, a
   machine, weather. See the model section in `sound.md`.
3. **A library**, for anything that is a real object in a real room - every transition, in
   practice. The written whoosh measured correctly and still lost to a bought one, because the room
   is the part no oscillator writes. One licence ledger holds what has been bought and what
   its licence covers.
4. **A recording**, which is free and better than all three when the object is on the desk. A phone
   at 20cm and 30 seconds of typing is a better keyboard than any model will generate.
