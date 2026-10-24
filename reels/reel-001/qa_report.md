# Reel 001 — QA report

Files checked: `renders/reel-001.mp4` (publishable, no CTA) and `renders/reel-001-cta-HOLD.mp4` (CTA, on hold).
Evidence: `qa/contact_sheet.jpg` (1 frame/s), `qa/cut_points.jpg` (both sides of every cut + loop seam),
`qa/cta_variant_frames.jpg`, `qa/audio_spectrum.png`.

**Verdict:** the no-CTA variant has no critical defects and is ready to post once a human has watched it on a
phone (with and without sound) and the name/handle review in gate 7 is done. The CTA variant is **rejected for now**
under gates 1 and 10: the free starter pack it promises doesn't exist yet.

## Measured (ffprobe / FFmpeg)
| Check | Result | Target |
|---|---|---|
| Resolution / fps / frames | 1080×1920, 30/1, 780 frames, 26.005 s | 1080×1920, 30, 780 ✅ |
| Video | H.264 High, yuv420p, BT.709 limited range | H.264, phone-safe ✅ |
| Audio | AAC-LC 48 kHz stereo, ~317 kb/s | AAC ✅ |
| Integrated loudness | −15.7 LUFS | −16 to −14 ✅ |
| True peak (after AAC) | −1.9 dBTP | ≤ −1 dBTP ✅ |
| Loudness range | 6.1 LU | — |
| Sample peaks at max | 2 (no clipping, max −2.7 dBFS) | none clipped ✅ |
| DC offset | 0.0003 | ≈0 ✅ |
| Stereo phase (mono compatibility) | mean +0.96, min +0.27 | > 0 ✅ |
| Black frames (blackdetect) | none; frame 0 average luma 34 with the line visible | no black first frame ✅ |
| Loop seam audio | last 10 ms −31 dB RMS → first 10 ms −27 dB RMS, fade on both edges | no pop ✅ |
| Freezes ≥ 0.3 s (freezedetect) | 4.3–5.2 s (planned Shot 03 freeze); 18.0–20.8 s and 21.4–23.9 s (type holds, background drift below detector threshold) | only designed holds ✅ |

## Gate A — internal diagnosis (0–2, not a virality prediction)
| First-frame clarity | Personal relevance | Curiosity | Emotional strength | Payoff | Shareability |
|---|---|---|---|---|---|
| 2 | 1 | 2 | 1 | 2 | 1 |

Notes: relevance is limited to people already curious about AI video workflows. The emotion is restrained wonder
rather than awe. The full-bleed dusk picture is attractive but simple next to a filmed or 3D hero.

## Release gates (`release-gates.md`)
| # | Gate | Status |
|---|---|---|
| 1 | Promise match | ✅ no-CTA variant. ❌ CTA variant until the starter pack exists. |
| 2 | Visual clarity / safe zones | ✅ All type inside 220 px top / 420 px bottom / 90 px side margins; checked at 216×384 in the contact sheet. The right-edge Instagram buttons sit below y ≈ 1100, and no type goes there after 1100. |
| 3 | Story | ✅ strike → payoff montage → question → reveal → proof → resolve → thesis → close → loop. |
| 4 | Craft | ✅ No easing jumps at cuts (see cut sheet). ⚠️ Fixed during QA: corona scale, ladder-like reflections, prompt card overflow, schematic/headline collision, proof text too small, dead freeze in Shot 04. |
| 5 | Sound | ✅ Cues frame-locked (spectrum). ✅ LUFS/TP above. ⚠️ Fixed during QA: room-tone beds were a loud sub-200 Hz rumble masking the planned silence; cut by about 18 dB. |
| 6 | Editing | ✅ Every match cut is documented in `edit_notes.md`. |
| 7 | Provenance | ✅ `asset_manifest.csv`: all picture and sound is original code; fonts are OFL/Apache with licenses bundled; no EYECANDY or third-party footage. Brand name/handle review not done (see below). |
| 8 | Truth | ✅ The schematic is labelled "conceptual view" on screen. The proof cards are generated from the real files at build time, and the code shown (`openingHead`) really drives the loop. |
| 9 | Tech | ✅ metadata, no black first frame, edge fades, loop continuity. |
| 10 | Funnel | ❌ Not applicable to the no-CTA cut. For the CTA cut: starter pack, Manychat trigger and test comment are all outstanding. |

## Defect log
| Timecode | Expected | Problem | Correction |
|---|---|---|---|
| 01:20–01:28 (f40–f59) | Organic sun glitter | Reflection read as evenly spaced bars ("ladder") | 90 randomised, flickering dashes |
| 01:28–02:24 (f60–f83) | Corona hugging the ring | Corona drawn ~40 % too large | `closest-side` gradient sizing |
| 03:18–05:06 (f108–f155) | "ONE PROMPT?" inside the card | "?" overflowed the card edge | 128 → 112 px |
| 05:06–09:00 (f156–f269) | Clean separation of headline and stack | Exploded stack rose into the headline; sky plane showed a warm slab below the horizon | Stack dropped 230 px; sky gradient ends at the horizon |
| 07:04–08:07 (f212–f247) | Living hold | 1.1 s dead freeze | Slow rotation creep |
| 09:00–13:06 (f270–f395) | Readable proof at phone size | 36 px mono too small; highlight box covered line numbers | 44 px mono, 68 px leading; box starts after the gutter |
| whole film | Quiet room tone | Brown-noise beds dominated the low end | Beds −18 dB, high-passed at 40–45 Hz |
| export | Phone-safe colour | Full-range yuvj420p | yuv420p, BT.709 tagged |

## Open items / not verified here
- **No human has watched or listened to this yet.** Review was done on frames, spectrum and measurements. Watch it
  on a phone, muted and then with sound, before posting.
- Not tested inside Instagram's own upload/transcode or against a live Instagram UI overlay.
- Revision candidate: the full-bleed hero (15–24 s) is a narrow band of light in a lot of dark frame. Consider a
  stronger hero (sourced or rendered plate) if retention data shows a drop there.
- Brand: "CLAUDE DIRECTED" handle/trademark review still pending. The reel itself shows no brand mark.
