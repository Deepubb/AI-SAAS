import { AbsoluteFill, Sequence, useCurrentFrame } from "remotion";
import { colors, safeArea } from "../theme";
import { shots, type Shot } from "./shots";

export const REEL_001_FRAMES = shots[shots.length - 1].endFrame + 1;

// Gate C placeholder: timing-only animatic so the cut can be reviewed muted at
// phone size before any real shots are built. Replace each card with its shot.
const ShotCard: React.FC<{ shot: Shot }> = ({ shot }) => {
  const frame = useCurrentFrame();
  const length = shot.endFrame - shot.startFrame + 1;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.charcoal,
        color: colors.offWhite,
        fontFamily: "system-ui, sans-serif",
        padding: `${safeArea.top}px ${safeArea.side}px ${safeArea.bottom}px`,
        justifyContent: "space-between",
      }}
    >
      <div style={{ fontSize: 36, color: colors.muted, fontFamily: "monospace" }}>
        SHOT {shot.id} · {shot.purpose.toUpperCase()}
      </div>
      <div style={{ fontSize: 96, fontWeight: 800, lineHeight: 1.05, color: colors.offWhite }}>
        {shot.heroText ?? ""}
      </div>
      <div>
        <div style={{ fontSize: 32, fontFamily: "monospace", color: colors.muted }}>
          f{shot.startFrame + frame} · {((shot.startFrame + frame) / 30).toFixed(2)}s
        </div>
        <div style={{ height: 6, marginTop: 16, backgroundColor: colors.black }}>
          <div style={{ height: 6, width: `${((frame + 1) / length) * 100}%`, backgroundColor: colors.accent }} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const Reel001Animatic: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: colors.black }}>
    {shots.map((shot) => (
      <Sequence key={shot.id} from={shot.startFrame} durationInFrames={shot.endFrame - shot.startFrame + 1}>
        <ShotCard shot={shot} />
      </Sequence>
    ))}
  </AbsoluteFill>
);
