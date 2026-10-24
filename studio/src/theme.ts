// Brand bible art system (see .claude/skills/instagram-reel-showrunner/references/brand-bible.md).
export const CANVAS = { width: 1080, height: 1920, fps: 30 } as const;

export const colors = {
  black: "#0A0A0A",
  charcoal: "#1A1A1C",
  glass: "#111114",
  offWhite: "#F2EDE4",
  muted: "#8A867F",
  // Single vivid accent: chartreuse (chosen over electric coral for Reel 001).
  accent: "#D4FF3A",
  accentHot: "#F4FFC9",
  warm: "#E2A868",
  ember: "#3B2A24",
} as const;

export const fonts = {
  display: "Inter Display",
  mono: "JetBrains Mono",
} as const;

// Keep type clear of Instagram's caption/action UI.
export const safeArea = { top: 220, bottom: 420, side: 90 } as const;

// The recurring "framed composition" window and the horizon the luminous line rides on.
export const FRAME_RECT = { x: 90, y: 370, w: 900, h: 1180 } as const;
export const HORIZON_Y = 960;
