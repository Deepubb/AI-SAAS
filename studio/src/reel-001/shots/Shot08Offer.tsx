import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { colors, fonts, FRAME_RECT } from "../../theme";
import { FULL_BLEED, HeroWindow } from "../HeroWindow";
import { Glass, Glint, Grain, lerp, SelectionBox } from "../motif";
import { ThesisType } from "./Shot07Thesis";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const START = 624;

// CTA lands at local 8 (global 632) on the soft tactile accent.
export const OFFER_LAND = 8;

const box = { x: 130, y: 818, w: 820, h: 196 };

export const OfferType: React.FC<{ cta: boolean; f: number }> = ({ cta, f }) => {
  const inn = interpolate(f, [OFFER_LAND - 6, OFFER_LAND], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const twinkle = 0.5 + 0.5 * Math.sin(f / 5);
  return (
    <AbsoluteFill style={{ opacity: inn, transform: `translateY(${(1 - inn) * 26}px)` }}>
      <div style={{ position: "absolute", top: 712, width: 1080, textAlign: "center", fontFamily: fonts.display, fontWeight: 700, fontSize: 70, color: colors.offWhite, letterSpacing: -1 }}>
        {cta ? "COMMENT" : "THE DIRECTOR"}
      </div>
      <SelectionBox {...box} />
      <div
        style={{
          position: "absolute",
          top: box.y + 24,
          width: 1080,
          textAlign: "center",
          fontFamily: fonts.display,
          fontWeight: 900,
          fontSize: cta ? 150 : 128,
          lineHeight: 1,
          letterSpacing: -4,
          color: colors.accent,
          whiteSpace: "nowrap",
          marginTop: cta ? 0 : 10,
        }}
      >
        {cta ? "DIRECTOR" : "IS A FILE."}
      </div>
      <div style={{ position: "absolute", top: 1062, width: 1080, textAlign: "center", fontFamily: fonts.mono, fontWeight: 500, fontSize: 38, color: colors.offWhite, letterSpacing: 4 }}>
        {cta ? "FREE STARTER WORKFLOW" : "CINEMA, ENGINEERED."}
      </div>
      <Glint x={box.x} y={box.y} size={0.35} opacity={twinkle} />
      <Glint x={box.x + box.w} y={box.y + box.h} size={0.35} opacity={1 - twinkle} />
    </AbsoluteFill>
  );
};

export const Shot08Offer: React.FC<{ cta: boolean }> = ({ cta }) => {
  const f = useCurrentFrame();
  const thesisOut = interpolate(f, [0, 6], [1, 0], clamp);
  // Last second: the picture closes back into the framed window, ready for the loop.
  const shrink = interpolate(f, [92, 119], [0, 1], { ...clamp, easing: Easing.bezier(0.65, 0, 0.35, 1) });
  const rect = {
    x: lerp(0, FRAME_RECT.x, shrink),
    y: lerp(0, FRAME_RECT.y, shrink),
    w: lerp(FULL_BLEED.w, FRAME_RECT.w, shrink),
    h: lerp(FULL_BLEED.h, FRAME_RECT.h, shrink),
  };

  return (
    <AbsoluteFill>
      <Glass />
      <HeroWindow rect={rect} t={START + f} />
      <AbsoluteFill style={{ backgroundColor: "rgba(5,5,6,0.62)" }} />
      <SelectionBox {...FRAME_RECT} opacity={shrink} />
      <AbsoluteFill style={{ opacity: thesisOut }}>
        <ThesisType f={60} />
      </AbsoluteFill>

      <OfferType cta={cta} f={f} />
      <Grain />
    </AbsoluteFill>
  );
};
