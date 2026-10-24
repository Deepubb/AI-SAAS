import React, { useId, useMemo } from "react";
import { AbsoluteFill } from "remotion";
import { noise2D } from "@remotion/noise";
import { CANVAS, colors, HORIZON_Y } from "../theme";
import { Glint, GlowLine } from "./motif";

// Original dusk composition: sky, setting sun, far ridges, sea, foreground hill and the
// luminous horizon line. Each layer renders alone so Shot 04/06 can explode and re-stack it.
export type HeroLayer = "sky" | "sun" | "far" | "sea" | "near" | "line";
export const ALL_LAYERS: HeroLayer[] = ["sky", "sun", "far", "sea", "near", "line"];

type Camera = { scale: number; cx: number; cy: number; dx?: number; dy?: number };

type Props = {
  t: number;
  layers?: HeroLayer[];
  // horizontal drift in px; layers move by depth for parallax
  drift?: number;
  sunDrop?: number;
  lineProgress?: number;
  lineIntensity?: number;
  glintX?: number | null;
  camera?: Camera;
};

const W = CANVAS.width;
const H = CANVAS.height;

const ridge = (seed: string, base: number, amp: number, env: (x: number) => number, bottom: number) => {
  let d = `M -260 ${bottom} `;
  for (let x = -260; x <= W + 260; x += 10) {
    const n =
      noise2D(seed, x / 260, 0) * 0.55 + noise2D(seed, x / 80, 7) * 0.3 + noise2D(seed, x / 22, 13) * 0.08;
    d += `L ${x} ${(base - env(x) * amp * (0.62 + 0.38 * n)).toFixed(1)} `;
  }
  return d + `L ${W + 260} ${bottom} Z`;
};

const edgeEnv = (x: number) => Math.pow(Math.min(1.35, Math.abs(x - W / 2) / (W / 2)), 1.5);

const layerStyle = (dx: number): React.CSSProperties => ({ transform: `translateX(${dx}px)` });

export const HeroScene: React.FC<Props> = ({
  t,
  layers = ALL_LAYERS,
  drift = 0,
  sunDrop = 0,
  lineProgress = 1,
  lineIntensity = 1,
  glintX = null,
  camera,
}) => {
  const paths = useMemo(
    () => ({
      far1: ridge("far1", HORIZON_Y, 250, edgeEnv, HORIZON_Y + 2),
      far2: ridge("far2", HORIZON_Y, 150, edgeEnv, HORIZON_Y + 2),
      near: ridge("near", H + 20, 360, (x) => Math.pow(Math.max(0, 1 - x / 980), 1.25), H + 40),
    }),
    [],
  );
  const uid = useId().replace(/:/g, "");
  const has = (l: HeroLayer) => layers.includes(l);
  const sunY = 905 + sunDrop;

  const cam = camera
    ? {
        transform: `translate(${camera.dx ?? 0}px, ${camera.dy ?? 0}px) scale(${camera.scale})`,
        transformOrigin: `${camera.cx}px ${camera.cy}px`,
      }
    : undefined;

  return (
    <AbsoluteFill style={{ width: W, height: H, ...cam }}>
      {has("sky") && (
        <AbsoluteFill
          style={{
            background: `linear-gradient(180deg, #08080a 0%, #131216 30%, ${colors.ember} 43%, #9c6440 48.5%, ${colors.warm} 50%, #1d1719 50%, #050506 100%)`,
          }}
        />
      )}
      {has("sun") && (
        <AbsoluteFill style={layerStyle(drift * 0.12)}>
          <div
            style={{
              position: "absolute",
              left: W / 2 - 520,
              top: sunY - 520,
              width: 1040,
              height: 1040,
              borderRadius: "50%",
              background: "radial-gradient(circle, rgba(245,214,160,0.42) 0%, rgba(226,168,104,0.16) 32%, rgba(226,168,104,0) 66%)",
            }}
          />
          <svg width={W} height={H} style={{ position: "absolute", inset: 0 }}>
            <defs>
              <radialGradient id={`${uid}sun`} cx="50%" cy="42%" r="60%">
                <stop offset="0%" stopColor="#FFF8EA" />
                <stop offset="70%" stopColor="#F7DDB0" />
                <stop offset="100%" stopColor="#EDBB7C" />
              </radialGradient>
              <clipPath id={`${uid}clip`}>
                <rect x={0} y={0} width={W} height={HORIZON_Y} />
              </clipPath>
            </defs>
            <circle cx={W / 2} cy={sunY} r={118} fill={`url(#${uid}sun)`} clipPath={`url(#${uid}clip)`} />
          </svg>
        </AbsoluteFill>
      )}
      {has("far") && (
        <AbsoluteFill style={layerStyle(drift * 0.3)}>
          <svg width={W} height={H} style={{ position: "absolute", inset: 0, overflow: "visible" }}>
            <defs>
              <linearGradient id={`${uid}haze`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#2e2429" />
                <stop offset="100%" stopColor="#4a342b" />
              </linearGradient>
            </defs>
            <path d={paths.far1} fill={`url(#${uid}haze)`} />
            <path d={paths.far2} fill="#16131a" />
          </svg>
          <div
            style={{
              position: "absolute",
              left: -200 + Math.sin(t / 40) * 30,
              top: HORIZON_Y - 46,
              width: W + 400,
              height: 70,
              borderRadius: "50%",
              background: "rgba(226,168,104,0.22)",
              filter: "blur(22px)",
            }}
          />
        </AbsoluteFill>
      )}
      {has("sea") && (
        <AbsoluteFill>
          <div
            style={{
              position: "absolute",
              left: 0,
              top: HORIZON_Y,
              width: W,
              height: H - HORIZON_Y,
              background: "linear-gradient(180deg, #1d1719 0%, #0b0a0c 38%, #050506 100%)",
            }}
          />
          {Array.from({ length: 90 }).map((_, i) => {
            // Broken, flickering glitter path: random sizes and offsets so it never reads as a ladder.
            const depth = i / 90;
            const y = HORIZON_Y + 8 + Math.pow(depth, 1.5) * 560 + noise2D("ry", i, 0) * 6;
            const w = (20 + depth * 140) * (0.4 + 0.6 * Math.abs(noise2D("rw", i, t / 10)));
            const a = (1 - depth * 0.85) * Math.max(0, 0.15 + 0.55 * noise2D("ra", i, t / 5));
            const cx = W / 2 + drift * 0.12 + noise2D("rx", i, t / 18) * (20 + depth * 90);
            return (
              <div
                key={i}
                style={{
                  position: "absolute",
                  left: cx - w / 2,
                  top: y,
                  width: w,
                  height: 1.5 + depth * 3,
                  borderRadius: 2,
                  background: "#F3D5A6",
                  opacity: a,
                  filter: "blur(1.2px)",
                }}
              />
            );
          })}
        </AbsoluteFill>
      )}
      {has("near") && (
        <AbsoluteFill style={layerStyle(drift)}>
          <svg width={W} height={H} style={{ position: "absolute", inset: 0, overflow: "visible" }}>
            <path d={paths.near} fill="#040405" stroke="rgba(226,168,104,0.35)" strokeWidth={2} />
          </svg>
        </AbsoluteFill>
      )}
      {has("line") && (
        <AbsoluteFill>
          {lineProgress > 0 && (
            <GlowLine x1={-40} y1={HORIZON_Y} x2={-40 + lineProgress * (W + 80)} y2={HORIZON_Y} intensity={lineIntensity} />
          )}
          {glintX !== null && <Glint x={glintX} y={HORIZON_Y} />}
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
