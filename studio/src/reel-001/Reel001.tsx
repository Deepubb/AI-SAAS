import React from "react";
import { AbsoluteFill, Html5Audio, Sequence, staticFile } from "remotion";
import { colors } from "../theme";
import { shots } from "./shots";
import { Shot01Slice } from "./shots/Shot01Slice";
import { Shot02Montage } from "./shots/Shot02Montage";
import { Shot03Question } from "./shots/Shot03Question";
import { Shot04Explode } from "./shots/Shot04Explode";
import { Shot05Proof } from "./shots/Shot05Proof";
import { Shot06Resolve } from "./shots/Shot06Resolve";
import { Shot07Thesis } from "./shots/Shot07Thesis";
import { Shot08Offer } from "./shots/Shot08Offer";
import { Shot09Loop } from "./shots/Shot09Loop";

export type Reel001Props = {
  // Only render the DIRECTOR comment CTA once the free starter pack is live and the funnel is tested.
  cta: boolean;
  audio: boolean;
};

export const REEL_001_FRAMES = shots[shots.length - 1].endFrame + 1;

export const Reel001: React.FC<Reel001Props> = ({ cta, audio }) => {
  const scenes: Record<string, React.ReactNode> = {
    "01": <Shot01Slice />,
    "02": <Shot02Montage />,
    "03": <Shot03Question />,
    "04": <Shot04Explode />,
    "05": <Shot05Proof />,
    "06": <Shot06Resolve />,
    "07": <Shot07Thesis />,
    "08": <Shot08Offer cta={cta} />,
    "09": <Shot09Loop cta={cta} />,
  };
  return (
    <AbsoluteFill style={{ backgroundColor: colors.black }}>
      {shots.map((s) => (
        <Sequence key={s.id} name={`Shot ${s.id}`} from={s.startFrame} durationInFrames={s.endFrame - s.startFrame + 1}>
          {scenes[s.id]}
        </Sequence>
      ))}
      {audio && <Html5Audio src={staticFile("audio/reel-001-mix.wav")} />}
    </AbsoluteFill>
  );
};
