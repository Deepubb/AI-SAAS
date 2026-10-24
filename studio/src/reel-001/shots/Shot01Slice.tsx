import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { FRAME_RECT, HORIZON_Y } from "../../theme";
import { HeroScene } from "../HeroScene";
import { Glass, GlowLine, Grain, lerp, OPEN_ANGLE_DEG, OPEN_LINE, openingHead, pointOnOpenLine, SelectionBox } from "../motif";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const CX = 540;

// The slit the line tears open, rotating level and widening into the framed composition.
// Shot 09 runs the same window in reverse, so both are driven by `open` (0 slit -> 1 frame).
export const SliceWindow: React.FC<{ open: number; t: number; edge: number }> = ({ open, t, edge }) => {
  const angle = lerp(OPEN_ANGLE_DEG, 0, open);
  const w = lerp(1520, FRAME_RECT.w, open);
  const h = lerp(4, FRAME_RECT.h, open);
  const left = CX - w / 2;
  const top = HORIZON_Y - h / 2;
  if (open <= 0) return null;
  return (
    <div
      style={{
        position: "absolute",
        left,
        top,
        width: w,
        height: h,
        transform: `rotate(${angle}deg)`,
        overflow: "hidden",
        boxShadow: `0 0 0 2px rgba(212,255,58,${edge}), 0 0 40px rgba(212,255,58,${edge * 0.45})`,
      }}
    >
      <div
        style={{
          position: "absolute",
          left: -left,
          top: -top,
          width: 1080,
          height: 1920,
          transform: `rotate(${-angle}deg)`,
          transformOrigin: `${CX}px ${HORIZON_Y}px`,
        }}
      >
        <HeroScene t={t} drift={-t * 0.8} camera={{ scale: lerp(1.32, 1.06, open), cx: CX, cy: HORIZON_Y }} />
      </div>
    </div>
  );
};

export const Shot01Slice: React.FC = () => {
  const f = useCurrentFrame();
  const head = pointOnOpenLine(openingHead(f));
  const impact = interpolate(f, [0, 4, 16], [1.9, 1.6, 1.0], clamp);
  const open = interpolate(f, [9, 28], [0, 1], { ...clamp, easing: Easing.bezier(0.16, 1, 0.3, 1) });
  const settle = interpolate(f, [24, 34], [0, 1], clamp);

  return (
    <AbsoluteFill>
      <Glass />
      <SliceWindow open={open} t={f} edge={1 - settle} />
      <AbsoluteFill style={{ opacity: 1 - open }}>
        <GlowLine x1={OPEN_LINE.x1} y1={OPEN_LINE.y1} x2={head.x} y2={head.y} intensity={impact} />
        <div
          style={{
            position: "absolute",
            left: head.x - 260,
            top: head.y - 260,
            width: 520,
            height: 520,
            borderRadius: "50%",
            background: "radial-gradient(circle, rgba(244,255,201,0.55), rgba(212,255,58,0) 65%)",
            opacity: impact - 1,
            mixBlendMode: "screen",
          }}
        />
      </AbsoluteFill>
      <SelectionBox {...FRAME_RECT} opacity={settle} />
      <Grain />
    </AbsoluteFill>
  );
};
