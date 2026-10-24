// Mirrors reels/reel-001/storyboard.csv — keep the two in sync.
// end_frame in the CSV is inclusive.
export type Shot = {
  id: string;
  startFrame: number;
  endFrame: number;
  purpose: string;
  heroText?: string;
};

export const shots: Shot[] = [
  { id: "01", startFrame: 0, endFrame: 35, purpose: "Interrupt scroll" },
  { id: "02", startFrame: 36, endFrame: 107, purpose: "Demonstrate payoff first" },
  { id: "03", startFrame: 108, endFrame: 155, purpose: "Create question", heroText: "ONE PROMPT?" },
  { id: "04", startFrame: 156, endFrame: 269, purpose: "Reveal directing intelligence", heroText: "IT'S A DIRECTING SYSTEM" },
  { id: "05", startFrame: 270, endFrame: 395, purpose: "Make proof specific", heroText: "STORY → MOTION → SOUND" },
  { id: "06", startFrame: 396, endFrame: 527, purpose: "Deliver emotional escalation" },
  { id: "07", startFrame: 528, endFrame: 623, purpose: "State differentiated idea", heroText: "NOT A PROMPT. A DIRECTOR." },
  { id: "08", startFrame: 624, endFrame: 743, purpose: "Present free offer", heroText: "COMMENT DIRECTOR | FREE STARTER WORKFLOW" },
  { id: "09", startFrame: 744, endFrame: 779, purpose: "Loop with intent" },
];
