import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { FRAME_RECT, HORIZON_Y } from "../../theme";
import { FULL_BLEED, HeroWindow } from "../HeroWindow";
import { MODULES } from "../modules";
import { Glass, Glint, GlowLine, Grain, lerp, SelectionBox } from "../motif";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const START = 396;

// Module i snaps home at local LOCK_START + i * LOCK_GAP (global 406, 414, 422, 430, 438).
export const LOCK_START = 10;
export const LOCK_GAP = 8;
// The line re-ignites and lands on the sub impact at local 60 (global 456).
export const IGNITE_FRAME = 60;

export const Shot06Resolve: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = START + f;
  const expand = interpolate(f, [44, 58], [0, 1], { ...clamp, easing: Easing.bezier(0.65, 0, 0.35, 1) });
  const rect = {
    x: lerp(FRAME_RECT.x, 0, expand),
    y: lerp(FRAME_RECT.y, 0, expand),
    w: lerp(FRAME_RECT.w, FULL_BLEED.w, expand),
    h: lerp(FRAME_RECT.h, FULL_BLEED.h, expand),
  };
  const head = interpolate(f, [IGNITE_FRAME - 5, IGNITE_FRAME], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
  const bloom = interpolate(f, [IGNITE_FRAME, IGNITE_FRAME + 2, IGNITE_FRAME + 24], [0, 1, 0], clamp);
  const glintX = interpolate(f, [IGNITE_FRAME, 131], [-80, 1160], clamp);

  return (
    <AbsoluteFill>
      <Glass />
      {MODULES.map((m, i) => {
        const lock = spring({ frame: f - (LOCK_START + i * LOCK_GAP) + 7, fps, config: { damping: 16, stiffness: 240, mass: 0.7 } });
        const from = i % 2 === 0 ? -1150 : 1150;
        return <HeroWindow key={m.name} rect={rect} t={t} layers={m.layers} offsetX={from * (1 - lock)} />;
      })}
      <SelectionBox {...FRAME_RECT} opacity={1 - expand} closed={interpolate(f, [0, 8], [1, 0], clamp)} />
      {head > 0 && (
        <AbsoluteFill style={{ opacity: 1 - bloom * 0.2 }}>
          <GlowLine x1={-40} y1={HORIZON_Y} x2={-40 + head * 1160} y2={HORIZON_Y} intensity={1 + bloom * 1.2} />
        </AbsoluteFill>
      )}
      <AbsoluteFill
        style={{
          background: "radial-gradient(ellipse 70% 18% at 50% 50%, rgba(244,255,201,0.55), rgba(212,255,58,0) 70%)",
          opacity: bloom,
          mixBlendMode: "screen",
        }}
      />
      {f >= IGNITE_FRAME && <Glint x={glintX} y={HORIZON_Y} />}
      <Grain />
    </AbsoluteFill>
  );
};
