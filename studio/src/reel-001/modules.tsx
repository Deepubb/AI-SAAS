import React from "react";
import { colors } from "../theme";
import type { HeroLayer } from "./HeroScene";

// The five directing modules, each paired with the hero layer it "owns" in the schematic.
export type Module = { name: string; layers: HeroLayer[]; glyph: React.ReactNode };

const stroke = { fill: "none", stroke: colors.accent, strokeWidth: 4, strokeLinecap: "round" as const };

export const MODULES: Module[] = [
  {
    name: "STORY",
    layers: ["sky", "sun"],
    glyph: <path d="M 6 58 C 30 58, 40 10, 62 12 S 92 46, 114 20" {...stroke} />,
  },
  {
    name: "SHOTS",
    layers: ["far"],
    glyph: (
      <g {...stroke}>
        <rect x={6} y={18} width={30} height={40} />
        <rect x={45} y={18} width={30} height={40} />
        <rect x={84} y={18} width={30} height={40} />
      </g>
    ),
  },
  {
    name: "MOTION",
    layers: ["sea"],
    glyph: <path d="M 6 60 C 60 60, 60 10, 114 10" {...stroke} />,
  },
  {
    name: "SOUND",
    layers: ["near"],
    glyph: (
      <g {...stroke}>
        {[22, 40, 14, 52, 30, 46, 18, 36].map((h, i) => (
          <line key={i} x1={10 + i * 14} y1={36 - h / 2} x2={10 + i * 14} y2={36 + h / 2} />
        ))}
      </g>
    ),
  },
  {
    name: "QA",
    layers: ["line"],
    glyph: (
      <g {...stroke}>
        <rect x={6} y={14} width={44} height={44} />
        <path d="M 16 36 L 26 46 L 42 24" />
        <line x1={64} y1={28} x2={114} y2={28} />
        <line x1={64} y1={46} x2={100} y2={46} />
      </g>
    ),
  },
];

export const ModuleGlyph: React.FC<{ glyph: React.ReactNode; scale?: number }> = ({ glyph, scale = 1 }) => (
  <svg width={120 * scale} height={70 * scale} viewBox="0 0 120 70" style={{ overflow: "visible" }}>
    {glyph}
  </svg>
);
