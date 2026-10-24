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
npm run render:reel-001-animatic   # -> studio/out/reel-001-animatic.mp4
```
`Reel001Animatic` is only a timing animatic (Gate C): placeholder cards built from the
storyboard frame ranges, with hero text kept inside Instagram's safe area. It is **not** the
finished film. Swap in each real shot as it gets built, and keep `studio/src/reel-001/shots.ts`
in sync with `reels/reel-001/storyboard.csv`.

If Remotion can't download its own headless browser, pass one with
`--browser-executable=/path/to/chrome-headless-shell`.
