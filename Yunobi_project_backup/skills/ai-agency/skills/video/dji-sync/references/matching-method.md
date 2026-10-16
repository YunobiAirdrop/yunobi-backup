# How the match is decided, and why not the obvious ways

Three signals were measured against a confirmed true/false take pair. Two of them fail:

| Signal | True take | False take | Verdict |
| --- | --- | --- | --- |
| Envelope correlation | r ≈ 0.00 | r ≈ 0.00 | **Useless.** A chest lav and a room mic have unrelated envelopes on identical speech. |
| Correlation peak height (PSR) | median 15.1 | median 7.1 (max 23.1) | **Overlaps.** Cannot separate on its own. |
| **Offset agreement across windows** | **0.15 ms spread** | **5.9 ms spread** | **This is the discriminator.** |

So the pipeline aligns once globally with GCC-PHAT, then re-measures the offset independently
in every 2-second window. A genuine match holds the same offset everywhere because it is the
same physical event hitting two mics. A false one wanders.

## Precision

Alignment is sub-sample. GCC-PHAT with parabolic peak interpolation resolves well under one
sample at 48 kHz (20.8 µs), the agreeing windows are averaged to sharpen it further, and the
fractional part is applied as an exact FFT phase ramp rather than rounded away. Verified on
the burned file: every window read 0.000 ms with 0.0000 ms spread.

**Clock drift is the real enemy on long takes, not the initial offset.** Measured −13.9 ppm on
this transmitter: 0.5 ms across a 36 s reel, which is nothing, but ≈ 8 ms across ten minutes,
which is visible. The per-window offsets already exist, so a slope is fitted for free and the
take is resampled only when projected drift exceeds 10 ms. Below that a single offset is
applied, because resampling a clean signal for a sub-millisecond gain is a bad trade.

## Why silence is cut before whisper sees a solo take

Cutting silence looks like a file-size trick. It is not. It is the only reason the transcript
has any content at all. Measured on the first real take, 20m17s recorded on a walk, 233.7 MB:
the whole file gave 249 words and **none** of the real content, while the same take VAD-cut to
1m00s gave 130 words and all of it.

Given twenty minutes of near-silence, whisper locks into a repeat loop: 38 of the 42 lines it
returned were the same sentence, and the actual thinking on the take, an all-in-one assistant,
the ClickUp to Sheets user base in D1, a video about a skill cleaner, **did not appear once**.
The transcript looked plausible and was worthless. Feed it only the spoken parts and all of it
comes back. Size is the free side effect: 233.7 MB to 168 KB, **1393x**, at 24 kbps mono Opus.

## VAD decides, an amplitude gate cannot

A fixed dB threshold is not a usable discriminator. On that same take, `silenceremove` at
−50/−45/−40/−35 dB kept 488/230/113/50 s: a ten-fold swing across 15 dB, so the number would
need retuning for every recording depending on how loud he was and where he was standing.
Silero VAD reports 49.8 s independently, which agrees with the −35 dB reading, and it needs no
tuning. The gate is worth running only as a cross-check when a result looks wrong.
