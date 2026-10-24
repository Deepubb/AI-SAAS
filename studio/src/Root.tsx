import { Composition } from "remotion";
import { CANVAS } from "./theme";
import { Reel001Animatic, REEL_001_FRAMES } from "./reel-001/Animatic";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Reel001Animatic"
    component={Reel001Animatic}
    durationInFrames={REEL_001_FRAMES}
    fps={CANVAS.fps}
    width={CANVAS.width}
    height={CANVAS.height}
  />
);
