import { Composition } from "remotion";
import "./fonts";
import { CANVAS } from "./theme";
import { Reel001Animatic } from "./reel-001/Animatic";
import { Reel001, REEL_001_FRAMES, type Reel001Props } from "./reel-001/Reel001";

const canvas = { durationInFrames: REEL_001_FRAMES, fps: CANVAS.fps, width: CANVAS.width, height: CANVAS.height };

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Reel001" component={Reel001} {...canvas} defaultProps={{ cta: false, audio: true } satisfies Reel001Props} />
    <Composition id="Reel001CTA" component={Reel001} {...canvas} defaultProps={{ cta: true, audio: true } satisfies Reel001Props} />
    <Composition id="Reel001Animatic" component={Reel001Animatic} {...canvas} />
  </>
);
