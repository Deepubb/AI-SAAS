import React from "react";
import { AbsoluteFill } from "remotion";
import { HORIZON_Y } from "../theme";
import { HeroScene, type HeroLayer } from "./HeroScene";

export type Rect = { x: number; y: number; w: number; h: number };
export const FULL_BLEED: Rect = { x: 0, y: 0, w: 1080, h: 1920 };

// Hero composition seen through a rectangular window, in canvas coordinates. Shots 06–08 share
// one camera (scale 1.06, drift -t*0.8) so the scene never jumps between them.
export const HeroWindow: React.FC<{
  rect: Rect;
  t: number;
  layers?: HeroLayer[];
  offsetX?: number;
  children?: React.ReactNode;
}> = ({ rect, t, layers, offsetX = 0, children }) => (
  <div style={{ position: "absolute", left: rect.x, top: rect.y, width: rect.w, height: rect.h, overflow: "hidden" }}>
    <div style={{ position: "absolute", left: -rect.x, top: -rect.y, width: 1080, height: 1920 }}>
      <AbsoluteFill style={{ transform: `translateX(${offsetX}px)` }}>
        <HeroScene t={t} layers={layers} drift={-t * 0.8} lineProgress={1} lineIntensity={1} camera={{ scale: 1.06, cx: 540, cy: HORIZON_Y }} />
      </AbsoluteFill>
      {children}
    </div>
  </div>
);
