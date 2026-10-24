import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { CANVAS, colors, HORIZON_Y } from "../../theme";
import { HeroScene } from "../HeroScene";
import { Glint, GlowLine, Grain } from "../motif";

const W = CANVAS.width;
export const MICRO_LEN = 24;

// One glint travels left -> right across all three micro-shots on y = HORIZON_Y,
// so every cut lands on the same motion vector.
export const montageGlintX = (f: number) => interpolate(f, [0, 71], [-80, W + 80]);

// A: telephoto on the sun meeting the line.
export const MicroHorizon: React.FC<{ t: number; glintX: number | null }> = ({ t, glintX }) => (
  <AbsoluteFill style={{ backgroundColor: colors.black }}>
    <HeroScene
      t={t + 40}
      sunDrop={t * 0.6}
      glintX={null}
      camera={{ scale: 2.25 + t * 0.006, cx: 540, cy: HORIZON_Y }}
    />
    {glintX !== null && <Glint x={glintX} y={HORIZON_Y} size={1.1} />}
    <Grain />
  </AbsoluteFill>
);

// B: an eclipse ring sliced by the line, anamorphic flare.
export const MicroRing: React.FC<{ t: number; glintX: number | null }> = ({ t, glintX }) => {
  const s = 1 + t * 0.003;
  return (
    <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 50%, #121115 0%, #050506 70%)" }}>
      <AbsoluteFill style={{ transform: `scale(${s})`, transformOrigin: `540px ${HORIZON_Y}px` }}>
        <div
          style={{
            position: "absolute",
            left: 540 - 430,
            top: HORIZON_Y - 430,
            width: 860,
            height: 860,
            borderRadius: "50%",
            background:
              "radial-gradient(circle closest-side, rgba(0,0,0,0) 64%, rgba(245,214,160,0.45) 70%, rgba(226,168,104,0.14) 80%, rgba(0,0,0,0) 100%)",
            filter: "blur(6px)",
          }}
        />
        <svg width={W} height={CANVAS.height} style={{ position: "absolute", inset: 0 }}>
          <circle cx={540} cy={HORIZON_Y} r={300} fill="#050506" stroke={colors.offWhite} strokeWidth={3} opacity={0.95} />
          <circle
            cx={540}
            cy={HORIZON_Y}
            r={300}
            fill="none"
            stroke="#FFF8EA"
            strokeWidth={7}
            strokeDasharray="260 1625"
            strokeLinecap="round"
            transform={`rotate(${-150 + t * 4} 540 ${HORIZON_Y})`}
            style={{ filter: "drop-shadow(0 0 14px rgba(245,214,160,0.9))" }}
          />
        </svg>
        <div
          style={{
            position: "absolute",
            left: -200,
            top: HORIZON_Y - 26,
            width: W + 400,
            height: 52,
            background: "linear-gradient(90deg, rgba(212,255,58,0), rgba(212,255,58,0.22) 50%, rgba(212,255,58,0))",
            filter: "blur(10px)",
          }}
        />
        <GlowLine x1={-40} y1={HORIZON_Y} x2={W + 40} y2={HORIZON_Y} intensity={1.1} />
      </AbsoluteFill>
      {glintX !== null && <Glint x={glintX} y={HORIZON_Y} size={1.1} />}
      <Grain />
    </AbsoluteFill>
  );
};

// C: monoliths raked by a horizontal blade of light.
const SLABS = [
  { x: 150, w: 130, top: 640, shade: "#0f0e12" },
  { x: 800, w: 110, top: 560, shade: "#0d0c10" },
  { x: 405, w: 270, top: 330, shade: "#18161b" },
];

export const MicroMonolith: React.FC<{ t: number; glintX: number | null }> = ({ t, glintX }) => {
  const floor = 1380;
  const s = 1.04 + t * 0.002;
  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, #060607 0%, #0e0d11 ${(floor / 1920) * 100}%, #17151a 100%)` }}>
      <AbsoluteFill style={{ transform: `scale(${s}) translateX(${-t * 0.5}px)`, transformOrigin: `540px ${HORIZON_Y}px` }}>
        {SLABS.map((slab) => (
          <div key={slab.x}>
            <div
              style={{
                position: "absolute",
                left: slab.x + slab.w * 0.6,
                top: floor,
                width: slab.w * 2.4,
                height: 60,
                background: "linear-gradient(90deg, rgba(0,0,0,0.75), rgba(0,0,0,0))",
                transform: "skewX(-55deg)",
                transformOrigin: "left top",
              }}
            />
            <div
              style={{
                position: "absolute",
                left: slab.x,
                top: slab.top,
                width: slab.w,
                height: floor - slab.top,
                background: `linear-gradient(90deg, ${slab.shade} 0%, #050506 100%)`,
                borderLeft: "2px solid rgba(242,237,228,0.16)",
              }}
            />
            <div
              style={{
                position: "absolute",
                left: slab.x,
                top: HORIZON_Y - 22,
                width: slab.w,
                height: 44,
                background: "linear-gradient(90deg, rgba(244,255,201,0.75), rgba(212,255,58,0.18))",
                filter: "blur(3px)",
                mixBlendMode: "screen",
              }}
            />
          </div>
        ))}
        <GlowLine x1={-40} y1={HORIZON_Y} x2={W + 40} y2={HORIZON_Y} intensity={0.9} />
      </AbsoluteFill>
      {glintX !== null && <Glint x={glintX} y={HORIZON_Y} size={1.1} />}
      <Grain />
    </AbsoluteFill>
  );
};

export const Shot02Montage: React.FC = () => {
  const f = useCurrentFrame();
  const glintX = montageGlintX(f);
  const t = f % MICRO_LEN;
  if (f < MICRO_LEN) return <MicroHorizon t={t} glintX={glintX} />;
  if (f < MICRO_LEN * 2) return <MicroRing t={t} glintX={glintX} />;
  return <MicroMonolith t={t} glintX={glintX} />;
};
