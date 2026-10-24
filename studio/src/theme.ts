// Brand bible art system (see .claude/skills/instagram-reel-showrunner/references/brand-bible.md).
// Accent is tentative — chartreuse vs electric coral is still an open decision.
export const CANVAS = { width: 1080, height: 1920, fps: 30 } as const;

export const colors = {
  black: "#0A0A0A",
  charcoal: "#1A1A1C",
  offWhite: "#F2EDE4",
  accent: "#D4FF3A",
  muted: "#8A867F",
} as const;

// Keep type clear of Instagram's caption/action UI.
export const safeArea = { top: 220, bottom: 420, side: 90 } as const;
