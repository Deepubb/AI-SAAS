# Claude Reels Brand Launch Pack

An original launch playbook for a premium Instagram page that demonstrates and eventually sells video-directing workflows made with Claude Code.

## Install
1. Merge `.claude/skills/instagram-reel-showrunner/` into your Claude Code project's `.claude/skills/` folder.
2. Keep previous `premium-video-director`, `eyecandy-visual-director`, and your existing `motion-video-director` skills in the project. The official Remotion Claude Code plugin is recommended.
3. Copy `reels/reel-001/` into the project, review the asset requirements, and open `MASTER_CLAUDE_PROMPT.md`.
4. Produce and **test** your genuinely free starter download before posting a CTA; configure Manychat with the exact correct Reel and keyword.
5. Do not upload this pack and advertise it as the completed video or complete paid product. It is a production plan and reusable showrunner skill, not a rendered film.

## Files
- `.claude/skills/instagram-reel-showrunner/SKILL.md`: reusable direction and production quality gates.
- `reels/reel-001/`: pilot creative brief, frame-accurate 26-second storyboard, SFX cues and truthful caption.
- `funnels/manychat_flow.md`: comment-to-DM starter message flow and test checklist.
- `strategy/launch_and_product.md`: 30-day publishing plan, lead-magnet and product ladder.
- `MASTER_CLAUDE_PROMPT.md`: ready to paste into Claude Code.

## Extra resources (check ongoing updates)
- https://www.remotion.dev/docs/ai/claude-code-plugin
- https://help.manychat.com/hc/en-us/articles/14281316989724-Instagram-Post-and-Reel-Comments-trigger
- https://help.manychat.com/hc/en-us/articles/14281290924444-How-to-connect-Instagram-to-Manychat
- https://eyecannndy.com/ (technique inspiration only)
- https://whop.com/blog/best-digital-products-to-sell/

Brand names, suggested pricing, motion art direction and scripts are hypotheses for testing, not verified guarantees of availability, revenue or virality.

## Project layout (this repo)
```
.claude/skills/instagram-reel-showrunner/   lead showrunner skill + brand bible + release gates
MASTER_CLAUDE_PROMPT.md                     paste-ready prompt for producing Reel 001
reels/reel-001/                             brief, storyboard, SFX cues, caption/offer
funnels/manychat_flow.md                    comment -> DM flow and test checklist
strategy/launch_and_product.md              30-day plan and product ladder
studio/                                     Remotion project (one composition per Reel)
```

## Studio (Remotion)
```bash
cd studio
npm install
npm run dev                        # Remotion Studio preview
npm run render:reel-001            # final Reel 001, no CTA   -> studio/out/reel-001.mp4
npm run render:reel-001-cta        # CTA variant (hold until the free starter is live)
npm run render:reel-001-animatic   # timing-only animatic
```
Each render first regenerates the proof excerpts from the real repo files (`scripts/extract-proof.mjs`) and the
synthesized, mastered soundtrack (`scripts/synth-reel-001.mjs` + `scripts/master-audio.mjs`). Both are
deterministic and gitignored. Requires FFmpeg on PATH.

If Remotion can't download its own headless browser, point it at one:
`REMOTION_BROWSER_EXECUTABLE=/path/to/chrome-headless-shell npm run render:reel-001`.

## Reel 001 status
Rendered and QA'd. See `reels/reel-001/qa_report.md`. Deliverables are in `reels/reel-001/renders/`; production docs
are `art_bible.md`, `script.md`, `edit_notes.md`, `asset_manifest.csv` and `production_breakdown.md`.
