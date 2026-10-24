# Reel 001 — art bible (Gate B, locked)

## Canvas
1080×1920, 30 fps, 780 frames (26.0 s). H.264 High, yuv420p, BT.709 limited range, AAC-LC 48 kHz stereo 320 kb/s.
Safe area for type: 220 px top, 420 px bottom, 90 px sides (`studio/src/theme.ts`).

## Palette
| Token | Hex | Use |
|---|---|---|
| black | `#0A0A0A` | base |
| glass / charcoal | `#111114` / `#1A1A1C` | the dark surface the line tears through |
| offWhite | `#F2EDE4` | primary type |
| muted | `#8A867F` | labels, gutters |
| accent (chartreuse) | `#D4FF3A` | **only** the luminous line, selection box, key words |
| accentHot | `#F4FFC9` | line core, glints |
| warm / ember | `#E2A868` / `#3B2A24` | the dusk hero picture only |

Rule: chartreuse means "the director's hand". It never fills a background.

## Type
- Display: **Inter Display** 700/900 (OFL-1.1). No more than five words of large type per beat.
- Functional: **JetBrains Mono** 400/500 (Apache-2.0 build) for file paths, labels and real code.
- Font files and license texts are bundled in `studio/public/fonts/`.

## Motif
A luminous line → becomes a frame (selection box) → becomes a shot → becomes the finished picture,
then closes back into a line for the loop. The horizon at y = 960 is the line's home in every shot.

## Motion grammar
- Physical causes only: the line *tears* the glass, layers *snap* home (springs with mild overshoot),
  type *rises out of* the line it is masked by.
- Expo-out for arrivals (`bezier(0.16,1,0.3,1)`), quad/cubic in for departures; no spin or zoom transitions.
- Holds are deliberate: Shot 03 freeze, type holds in 07–08. Every other second has motion.
- One signature effect per ~10 s: slice-to-frame (0–1 s), exploded schematic (5–9 s), re-ignition (15 s).

## Sound logo
Tactile click → low pulse → resolving air: heard at 0 s (strike + 55 Hz pulse) and at 15.2 s (sub impact + air).
