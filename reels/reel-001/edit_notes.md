# Reel 001 — edit notes

## How it was built
- Remotion composition per shot (`studio/src/reel-001/shots/Shot0N*.tsx`), sequenced by `Reel001.tsx` from the
  frame ranges in `shots.ts` (mirrors `storyboard.csv`).
- Variants: `Reel001` (closing card, **no CTA** — publishable now) and `Reel001CTA` (DIRECTOR CTA — **hold**
  until the free starter exists and the Manychat flow has been tested).
- Rebuild: `cd studio && npm install && npm run render:reel-001` (also regenerates proof excerpts + audio).

## Match cuts and their correspondence
| Cut (frame) | Correspondence |
|---|---|
| 35→36 | Framed horizon line at y = 960 → full-bleed telephoto horizon at y = 960. |
| 59→60, 83→84 | Same line height in every micro-shot; one glint keeps a constant left→right vector through both cuts. |
| 107→108 | Hard cut motivated by the music drop; the picture freezes on the same frame. |
| 155→156 | Freeze → the framed hero, same rect as the 1 s mark, before it tilts into layers. |
| 395→396 | Selection box from the last proof card grows into the exact hero frame rect (type-to-frame). |
| 527→528 | Same picture and camera; only the dim and the type change. |
| 743→744 | Picture is already back inside the frame rect; Shot 09 closes it into the slit. |
| 779→0 | The new line's head is on the same path and speed as frame 0 (`openingHead`), so the loop has no seam. |

## Sound map vs. `sfx_cues.csv`
Planned cue frames were kept except where the picture moved. In those cases the sound follows the picture:
| Planned | Final | Why |
|---|---|---|
| 270 "typography locks and UI taps" | 270/301/332/364 cuts + 277/308/339/371 highlight locks | Four proof cards; each gets a bass transfer on the cut and a tick when its selection box locks. |
| 456 sub impact | 456 | Line re-ignition lands exactly here (`IGNITE_FRAME`). |
| 528 "drop to warm chord" + type locks | chord eases in from 532; locks at 542 and 572 | A breath of near-silence before the chord; clicks land on the type locks (`LOCK_1`, `LOCK_2`). |
| 624 CTA arrival | 632 | The CTA finishes moving at 632 (`OFFER_LAND`). |
| — | 406/414/422/430/438 | Added: the modules snap home in Shot 06. |
| 774 loop crossfade | 746 closing air, 761 exit swish, 774 approach | The loop now has its own sound path into the frame-0 strike. |

Mastering: two-pass EBU R128 loudnorm to −15 LUFS, −3 dBTP before encoding (AAC adds about 1 dB of overshoot on the strike).
