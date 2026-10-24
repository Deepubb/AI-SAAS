import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { colors, fonts, FRAME_RECT, safeArea } from "../../theme";
import { Grain, lerp, SelectionBox } from "../motif";
import { proofExcerpts } from "../proof.generated";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Card i starts at CARD_STARTS[i] (global 270, 301, 332, 364). Highlight locks 7 frames in.
export const CARD_STARTS = [0, 31, 62, 94];
export const HIGHLIGHT_DELAY = 7;
const LEN = 126;
const LINE_H = 68;
const CODE_TOP = 800;

const HEADLINE = ["STORY", "→", "MOTION", "→", "SOUND"];
// Which headline words are lit for each card.
const LIT = [1, 1, 3, 5];

export const Shot05Proof: React.FC = () => {
  const f = useCurrentFrame();
  const idx = CARD_STARTS.filter((s) => f >= s).length - 1;
  const local = f - CARD_STARTS[idx];
  const ex = proofExcerpts[idx];
  const next = idx + 1 < CARD_STARTS.length ? CARD_STARTS[idx + 1] : LEN;
  const cardLen = next - CARD_STARTS[idx];

  const reveal = interpolate(local, [0, 6], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const track = interpolate(local, [0, cardLen], [1, 1.07]);
  const hl = interpolate(local, [HIGHLIGHT_DELAY - 3, HIGHLIGHT_DELAY], [0, 1], clamp);
  // Type-to-frame match cut: the last highlight grows into the hero frame for Shot 06.
  const toFrame = interpolate(f, [114, 125], [0, 1], { ...clamp, easing: Easing.bezier(0.7, 0, 0.2, 1) });

  const hlTop = CODE_TOP + ex.highlight * LINE_H - 10;
  const box = {
    x: lerp(140, FRAME_RECT.x, toFrame),
    y: lerp(hlTop, FRAME_RECT.y, toFrame),
    w: lerp(900, FRAME_RECT.w, toFrame),
    h: lerp(LINE_H + 8, FRAME_RECT.h, toFrame),
  };

  return (
    <AbsoluteFill style={{ backgroundColor: "#0D0D10" }}>
      <AbsoluteFill style={{ opacity: 1 - toFrame }}>
        <AbsoluteFill
          style={{
            transform: `scale(${track})`,
            transformOrigin: "540px 900px",
            clipPath: `inset(0 ${(1 - reveal) * 100}% 0 0)`,
          }}
        >
          <div style={{ position: "absolute", left: safeArea.side, top: 640, fontFamily: fonts.mono, fontSize: 32, color: colors.accent }}>
            {ex.path}
          </div>
          <div style={{ position: "absolute", left: safeArea.side, top: 690, fontFamily: fonts.mono, fontSize: 24, color: colors.muted, letterSpacing: 2 }}>
            REAL FILE · LINES {ex.startLine}–{ex.startLine + ex.lines.length - 1}
          </div>
          {ex.lines.map((line, i) => (
            <div
              key={i}
              style={{
                position: "absolute",
                left: 70,
                top: CODE_TOP + i * LINE_H,
                width: 980,
                height: LINE_H,
                display: "flex",
                fontFamily: fonts.mono,
                fontSize: 44,
                lineHeight: `${LINE_H}px`,
                whiteSpace: "pre",
                overflow: "hidden",
                color: i === ex.highlight ? colors.offWhite : "rgba(242,237,228,0.42)",
                WebkitMaskImage: "linear-gradient(90deg, #000 82%, transparent 100%)",
              }}
            >
              <span style={{ width: 64, flexShrink: 0, color: colors.muted, textAlign: "right", marginRight: 22 }}>
                {ex.startLine + i}
              </span>
              {line}
            </div>
          ))}
        </AbsoluteFill>
      </AbsoluteFill>

      <SelectionBox {...box} closed={1} opacity={hl} />

      <div
        style={{
          position: "absolute",
          left: safeArea.side,
          top: safeArea.top + 40,
          display: "flex",
          gap: 22,
          fontFamily: fonts.display,
          fontWeight: 900,
          fontSize: 62,
          letterSpacing: -2,
          opacity: 1 - toFrame,
        }}
      >
        {HEADLINE.map((w, i) => (
          <span key={i} style={{ color: i < LIT[idx] ? (i === LIT[idx] - 1 ? colors.accent : colors.offWhite) : "rgba(242,237,228,0.16)" }}>
            {w}
          </span>
        ))}
      </div>
      <Grain opacity={0.06} />
    </AbsoluteFill>
  );
};
