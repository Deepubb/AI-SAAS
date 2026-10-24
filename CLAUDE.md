# CLAUDE.md

This repo is an Instagram Reels brand studio: premium vertical proof films that demonstrate
Claude Code video-directing workflows, plus the free starter and paid toolkit that come after.

- Lead skill: `.claude/skills/instagram-reel-showrunner/`. Read `references/brand-bible.md` and
  `references/release-gates.md` before final production work.
- Each Reel lives in `reels/reel-NNN/` (planning docs) and `studio/src/reel-NNN/` (Remotion code).
- Canvas: 1080×1920, 30 fps, H.264/AAC. Theme tokens and the safe area are in `studio/src/theme.ts`.
- `studio/src/reel-001/shots.ts` mirrors `storyboard.csv`. CSV `end_frame` values are inclusive.
- Checks: `cd studio && npm run typecheck`. Check renders with `ffprobe`.
- Integrity rules: never call an unrendered video complete, never fake code or proof screens,
  never put a DIRECTOR CTA live before the free starter pack exists and has been tested, and
  never imply Anthropic sponsorship.
