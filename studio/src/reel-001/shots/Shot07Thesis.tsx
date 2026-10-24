import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { colors, fonts, HORIZON_Y } from "../../theme";
import { FULL_BLEED, HeroWindow } from "../HeroWindow";
import { Grain } from "../motif";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const START = 528;

// Type locks (global 542 and 572) — each lands with a dry click.
export const LOCK_1 = 14;
export const LOCK_2 = 44;

const word: React.CSSProperties = {
  fontFamily: fonts.display,
  fontWeight: 900,
  fontSize: 118,
  lineHeight: 1,
  letterSpacing: -3,
  textAlign: "center",
  width: "100%",
  whiteSpace: "nowrap",
};

// Type rises out of the horizon line (above) and drops out of it (below), masked by the line.
export const ThesisType: React.FC<{ f: number }> = ({ f }) => {
  const up = interpolate(f, [LOCK_1 - 8, LOCK_1], [1, 0], { ...clamp, easing: Easing.bezier(0.2, 0.9, 0.25, 1) });
  const down = interpolate(f, [LOCK_2 - 8, LOCK_2], [1, 0], { ...clamp, easing: Easing.bezier(0.2, 0.9, 0.25, 1) });
  return (
    <>
      <div style={{ position: "absolute", left: 0, top: HORIZON_Y - 190, width: 1080, height: 184, overflow: "hidden" }}>
        <div style={{ ...word, position: "absolute", top: 38, color: colors.offWhite, transform: `translateY(${up * 150}px)` }}>
          NOT A PROMPT.
        </div>
      </div>
      <div style={{ position: "absolute", left: 0, top: HORIZON_Y + 6, width: 1080, height: 184, overflow: "hidden" }}>
        <div style={{ ...word, position: "absolute", top: 28, color: colors.accent, transform: `translateY(${-down * 150}px)` }}>
          A DIRECTOR.
        </div>
      </div>
    </>
  );
};

export const Shot07Thesis: React.FC = () => {
  const f = useCurrentFrame();
  const dim = interpolate(f, [0, 8], [0, 0.62], clamp);
  return (
    <AbsoluteFill>
      <HeroWindow rect={FULL_BLEED} t={START + f} />
      <AbsoluteFill style={{ backgroundColor: `rgba(5,5,6,${dim})` }} />
      <ThesisType f={f} />
      <Grain />
    </AbsoluteFill>
  );
};
