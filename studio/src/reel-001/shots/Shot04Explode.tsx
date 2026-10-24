import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { colors, fonts, FRAME_RECT, HORIZON_Y, safeArea } from "../../theme";
import { HeroScene } from "../HeroScene";
import { MODULES, ModuleGlyph } from "../modules";
import { Grain } from "../motif";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Layer i locks at local frame SNAP_START + i * SNAP_GAP (global 166, 172, 178, 184, 190).
export const SNAP_START = 10;
export const SNAP_GAP = 6;
const GAP = 165;
const PERSPECTIVE = 2600;
const TILT_X = 54;
// Drop the stack so its rising top clears the headline.
const STACK_DROP = 230;
const TILT_Z = -34;

export const Shot04Explode: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const tilt = interpolate(f, [0, 22], [0, 1], { ...clamp, easing: Easing.bezier(0.45, 0, 0.2, 1) });
  const converge = interpolate(f, [92, 112], [0, 1], { ...clamp, easing: Easing.bezier(0.7, 0, 0.84, 0) });
  const scale = interpolate(tilt, [0, 1], [1, 0.6]) * interpolate(converge, [0, 1], [1, 0.02]);
  const rx = TILT_X * tilt;
  // Slow creep so the settled stack never reads as a dead freeze during the headline hold.
  const rz = TILT_Z * tilt + f * 0.06;
  const headline = interpolate(f, [44, 54], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const headlineOut = interpolate(f, [90, 98], [1, 0], clamp);
  const node = interpolate(f, [100, 113], [0, 1], clamp);

  const planeZ = (i: number) => {
    const s = spring({ frame: f - (SNAP_START + i * SNAP_GAP) + 6, fps, config: { damping: 14, stiffness: 220, mass: 0.6 } });
    return i * GAP * s * (1 - converge);
  };

  // Project each plane's right-edge midpoint to place its label in screen space.
  const project = (z: number) => {
    const rad = (d: number) => (d * Math.PI) / 180;
    const px = FRAME_RECT.w / 2;
    const x1 = px * Math.cos(rad(rz));
    const y1 = px * Math.sin(rad(rz));
    const y2 = y1 * Math.cos(rad(rx)) - z * Math.sin(rad(rx));
    const z2 = y1 * Math.sin(rad(rx)) + z * Math.cos(rad(rx));
    const k = PERSPECTIVE / (PERSPECTIVE - z2 * scale);
    return { x: 540 + x1 * scale * k, y: HORIZON_Y + STACK_DROP * tilt + y2 * scale * k };
  };

  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, #141317 0%, #060607 75%)" }}>
      <AbsoluteFill style={{ perspective: PERSPECTIVE, perspectiveOrigin: `540px ${HORIZON_Y + STACK_DROP * tilt}px` }}>
        <div
          style={{
            position: "absolute",
            left: FRAME_RECT.x,
            top: FRAME_RECT.y + STACK_DROP * tilt,
            width: FRAME_RECT.w,
            height: FRAME_RECT.h,
            transformStyle: "preserve-3d",
            transform: `scale(${scale}) rotateX(${rx}deg) rotateZ(${rz}deg)`,
          }}
        >
          {MODULES.map((m, i) => (
            <div
              key={m.name}
              style={{
                position: "absolute",
                inset: 0,
                overflow: "hidden",
                transform: `translateZ(${planeZ(i)}px)`,
                border: `2px solid rgba(212,255,58,${0.25 + 0.5 * tilt})`,
                background: i === 0 ? undefined : `rgba(212,255,58,${0.03 * tilt})`,
              }}
            >
              <div style={{ position: "absolute", left: -FRAME_RECT.x, top: -FRAME_RECT.y, width: 1080, height: 1920 }}>
                <HeroScene t={156 + f} layers={m.layers} drift={-(156 + f) * 0.8} camera={{ scale: 1.06, cx: 540, cy: HORIZON_Y }} />
              </div>
            </div>
          ))}
        </div>
      </AbsoluteFill>

      {MODULES.map((m, i) => {
        const on = interpolate(f, [SNAP_START + i * SNAP_GAP, SNAP_START + i * SNAP_GAP + 4], [0, 1], clamp) * (1 - converge);
        const p = project(planeZ(i));
        return (
          <div
            key={m.name}
            style={{
              position: "absolute",
              left: Math.min(p.x + 24, 700),
              top: p.y - 30,
              display: "flex",
              alignItems: "center",
              gap: 16,
              opacity: on,
              transform: `translateX(${(1 - on) * 30}px)`,
            }}
          >
            <div style={{ width: 40, height: 2, background: colors.accent }} />
            <ModuleGlyph glyph={m.glyph} scale={0.45} />
            <div style={{ fontFamily: fonts.mono, fontWeight: 500, fontSize: 38, color: colors.offWhite, letterSpacing: 2 }}>{m.name}</div>
          </div>
        );
      })}

      <div
        style={{
          position: "absolute",
          left: safeArea.side,
          top: safeArea.top + 20,
          opacity: headline * headlineOut,
          transform: `translateY(${(1 - headline) * 24}px)`,
        }}
      >
        <div style={{ fontFamily: fonts.display, fontWeight: 700, fontSize: 64, color: colors.muted, letterSpacing: -1 }}>IT'S A</div>
        <div style={{ fontFamily: fonts.display, fontWeight: 900, fontSize: 112, lineHeight: 0.98, color: colors.offWhite, letterSpacing: -3 }}>
          DIRECTING
          <br />
          SYSTEM
        </div>
      </div>

      <div
        style={{
          position: "absolute",
          left: safeArea.side,
          bottom: safeArea.bottom - 60,
          fontFamily: fonts.mono,
          fontSize: 24,
          color: colors.muted,
          letterSpacing: 3,
          opacity: tilt * (1 - converge),
        }}
      >
        SCHEMATIC · CONCEPTUAL VIEW
      </div>

      <div
        style={{
          position: "absolute",
          left: 540 - 140,
          top: HORIZON_Y + STACK_DROP - 140,
          width: 280,
          height: 280,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${colors.accentHot} 0%, rgba(212,255,58,0.6) 12%, rgba(212,255,58,0) 60%)`,
          opacity: node,
          transform: `scale(${0.4 + 0.6 * node})`,
          mixBlendMode: "screen",
        }}
      />
      <Grain />
    </AbsoluteFill>
  );
};
