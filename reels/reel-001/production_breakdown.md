# Reel 001 — who and what made it (truthful breakdown)

- **Direction, code, sound design, QA:** Claude Code, working from the human-authored launch pack (brief, storyboard,
  cue sheet, brand bible, release gates), using the `instagram-reel-showrunner` skill in this repo.
  The partner skills it mentions (`premium-video-director`, `motion-video-director`, `eyecandy-visual-director`) and the
  Remotion Claude Code plugin were **not installed** in this session, so they were not used.
- **Picture:** 100 % Remotion (React) code: 2D vector shapes, CSS gradients/filters, and CSS 3D transforms on 2D
  layers for the schematic. No 3D renders, no stock footage, no AI-generated images or video.
- **Sound:** 100 % procedural synthesis in Node (`studio/scripts/synth-reel-001.mjs`): oscillators and filtered
  noise, no samples. Mastered with FFmpeg loudnorm.
- **Fonts:** Inter Display (OFL-1.1), JetBrains Mono (Apache-2.0 build).
- **Human review:** pending (see `qa_report.md`).

Accurate public claim: *"Directed and built with Claude Code + Remotion; original code-generated picture and sound;
human-reviewed before posting"* (the last part only after you've actually reviewed it).
Don't claim "made with one prompt" or "100 % automatic": it took iterative direction, multiple renders and QA fixes.
