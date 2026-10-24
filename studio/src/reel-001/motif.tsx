import React, { useId } from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { CANVAS, colors } from "../theme";

export const clamp01 = (v: number) => Math.min(1, Math.max(0, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

// The opening line enters bottom-left and exits top-right through the canvas centre.
export const OPEN_LINE = { x1: -60, y1: 1130, x2: 1140, y2: 790 } as const;
export const OPEN_ANGLE_DEG =
  (Math.atan2(OPEN_LINE.y2 - OPEN_LINE.y1, OPEN_LINE.x2 - OPEN_LINE.x1) * 180) / Math.PI;

// Head of the opening line, 0..1 along OPEN_LINE. `rel` is the frame for the opening
// and frame - 780 for the loop tail, so frame 779 -> 0 is one continuous stroke.
export const openingHead = (rel: number) => clamp01(0.45 + rel * 0.092);

export const pointOnOpenLine = (p: number) => ({
  x: lerp(OPEN_LINE.x1, OPEN_LINE.x2, p),
  y: lerp(OPEN_LINE.y1, OPEN_LINE.y2, p),
});

type GlowLineProps = {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  intensity?: number;
};

export const GlowLine: React.FC<GlowLineProps> = ({ x1, y1, x2, y2, intensity = 1 }) => {
  const id = useId().replace(/:/g, "");
  // userSpaceOnUse: a horizontal line has a zero-height bbox, which kills bbox-relative filters.
  const region = { filterUnits: "userSpaceOnUse" as const, x: -400, y: -400, width: 1880, height: 2720 };
  return (
    <svg
      width={CANVAS.width}
      height={CANVAS.height}
      style={{ position: "absolute", inset: 0, overflow: "visible", mixBlendMode: "screen" }}
    >
      <defs>
        <filter id={`${id}w`} {...region}>
          <feGaussianBlur stdDeviation={26} />
        </filter>
        <filter id={`${id}m`} {...region}>
          <feGaussianBlur stdDeviation={5} />
        </filter>
      </defs>
      <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={colors.accent} strokeWidth={46} strokeLinecap="round"
        opacity={Math.min(1, 0.32 * intensity)} filter={`url(#${id}w)`} />
      <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={colors.accent} strokeWidth={11} strokeLinecap="round"
        opacity={Math.min(1, 0.75 * intensity)} filter={`url(#${id}m)`} />
      <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={colors.accentHot} strokeWidth={3.5} strokeLinecap="round"
        opacity={Math.min(1, 0.6 + 0.4 * intensity)} />
    </svg>
  );
};

export const Glint: React.FC<{ x: number; y: number; size?: number; opacity?: number }> = ({
  x,
  y,
  size = 1,
  opacity = 1,
}) => (
  <>
    <div
      style={{
        position: "absolute",
        left: x - 90 * size,
        top: y - 90 * size,
        width: 180 * size,
        height: 180 * size,
        borderRadius: "50%",
        background: `radial-gradient(circle, ${colors.accentHot} 0%, rgba(212,255,58,0.55) 18%, rgba(212,255,58,0) 62%)`,
        mixBlendMode: "screen",
        opacity,
      }}
    />
    <div
      style={{
        position: "absolute",
        left: x - 420 * size,
        top: y - 3 * size,
        width: 840 * size,
        height: 6 * size,
        background: "linear-gradient(90deg, rgba(244,255,201,0), rgba(244,255,201,0.9) 50%, rgba(244,255,201,0))",
        filter: "blur(2px)",
        mixBlendMode: "screen",
        opacity,
      }}
    />
  </>
);

export const Grain: React.FC<{ opacity?: number }> = ({ opacity = 0.09 }) => {
  const frame = useCurrentFrame();
  const id = useId().replace(/:/g, "");
  return (
    <svg
      width={CANVAS.width}
      height={CANVAS.height}
      style={{ position: "absolute", inset: 0, mixBlendMode: "overlay", opacity, pointerEvents: "none" }}
    >
      <filter id={id} filterUnits="userSpaceOnUse" x={0} y={0} width={CANVAS.width} height={CANVAS.height}>
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={frame % 24} stitchTiles="stitch" />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width={CANVAS.width} height={CANVAS.height} filter={`url(#${id})`} />
    </svg>
  );
};

// Dark glass surface: the "material" the opening line tears through.
export const Glass: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(ellipse 95% 60% at 50% 47%, #1a1a1f 0%, #0c0c0e 62%, #050506 100%)",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          position: "absolute",
          left: -700,
          top: 640 + (frame % 780) * 0.25,
          width: 2480,
          height: 380,
          transform: `rotate(${OPEN_ANGLE_DEG}deg)`,
          background:
            "linear-gradient(180deg, rgba(242,237,228,0) 0%, rgba(242,237,228,0.045) 50%, rgba(242,237,228,0) 100%)",
        }}
      />
    </AbsoluteFill>
  );
};

type SelectionBoxProps = {
  x: number;
  y: number;
  w: number;
  h: number;
  // 0 = corner brackets only, 1 = closed rectangle
  closed?: number;
  opacity?: number;
  stroke?: number;
};

export const SelectionBox: React.FC<SelectionBoxProps> = ({ x, y, w, h, closed = 0, opacity = 1, stroke = 3 }) => {
  const cl = 46;
  const lx = Math.min(w / 2, lerp(cl, w / 2, closed));
  const ly = Math.min(h / 2, lerp(cl, h / 2, closed));
  const d = [
    `M ${x} ${y + ly} L ${x} ${y} L ${x + lx} ${y}`,
    `M ${x + w - lx} ${y} L ${x + w} ${y} L ${x + w} ${y + ly}`,
    `M ${x + w} ${y + h - ly} L ${x + w} ${y + h} L ${x + w - lx} ${y + h}`,
    `M ${x + lx} ${y + h} L ${x} ${y + h} L ${x} ${y + h - ly}`,
  ].join(" ");
  return (
    <svg
      width={CANVAS.width}
      height={CANVAS.height}
      style={{
        position: "absolute",
        inset: 0,
        overflow: "visible",
        opacity,
        filter: "drop-shadow(0 0 8px rgba(212,255,58,0.55))",
      }}
    >
      <path d={d} fill="none" stroke={colors.accent} strokeWidth={stroke} strokeLinecap="square" />
    </svg>
  );
};
