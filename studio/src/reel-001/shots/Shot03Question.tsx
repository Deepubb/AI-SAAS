import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { colors, fonts } from "../../theme";
import { MicroMonolith } from "./Shot02Montage";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Frame 122 (local 14): the "?" lands on the single dry click.
export const QUESTION_MARK_FRAME = 14;
// Shot 03 holds on the last frame of micro-shot C.
const MICRO_FREEZE = 23;

export const Shot03Question: React.FC = () => {
  const f = useCurrentFrame();
  const push = interpolate(f, [0, 47], [1, 1.07], { ...clamp, easing: Easing.out(Easing.quad) });
  const dim = interpolate(f, [0, 6], [0, 0.55], clamp);
  const card = interpolate(f, [2, 10], [0, 1], { ...clamp, easing: Easing.bezier(0.2, 0.9, 0.3, 1) });
  const mark = f >= QUESTION_MARK_FRAME;
  const caret = Math.floor(f / 8) % 2 === 0;

  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ transform: `scale(${push})`, transformOrigin: "540px 960px" }}>
        <MicroMonolith t={MICRO_FREEZE} glintX={null} />
      </AbsoluteFill>
      <AbsoluteFill style={{ backgroundColor: `rgba(5,5,6,${dim})` }} />
      <div
        style={{
          position: "absolute",
          left: 110,
          top: 740 + (1 - card) * 40,
          width: 860,
          height: 300,
          borderRadius: 28,
          opacity: card,
          background: "rgba(242,237,228,0.07)",
          border: "1.5px solid rgba(242,237,228,0.22)",
          backdropFilter: "blur(18px)",
          boxShadow: "0 30px 80px rgba(0,0,0,0.5)",
          padding: "40px 56px",
          boxSizing: "border-box",
        }}
      >
        <div style={{ fontFamily: fonts.mono, fontSize: 30, color: colors.muted, letterSpacing: 1 }}>&gt; prompt</div>
        <div
          style={{
            marginTop: 26,
            fontFamily: fonts.display,
            fontWeight: 900,
            fontSize: 112,
            lineHeight: 1,
            letterSpacing: -3,
            color: colors.offWhite,
            whiteSpace: "nowrap",
          }}
        >
          ONE PROMPT
          <span style={{ color: colors.accent, opacity: mark ? 1 : 0 }}>?</span>
          {!mark && (
            <span style={{ display: "inline-block", width: 10, height: 104, marginLeft: 8, background: colors.accent, opacity: caret ? 1 : 0, verticalAlign: -6 }} />
          )}
        </div>
      </div>
    </AbsoluteFill>
  );
};

