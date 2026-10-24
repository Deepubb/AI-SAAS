import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { FRAME_RECT } from "../../theme";
import { Glass, GlowLine, Grain, OPEN_LINE, openingHead, pointOnOpenLine, SelectionBox } from "../motif";
import { SliceWindow } from "./Shot01Slice";
import { OfferType } from "./Shot08Offer";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const START = 744;

// Reverse of Shot 01: the frame closes into the slit, the line leaves to the right, and a new
// line enters from the left so frame 779 flows straight into frame 0.
export const Shot09Loop: React.FC<{ cta: boolean }> = ({ cta }) => {
  const f = useCurrentFrame();
  const textOut = interpolate(f, [0, 6], [1, 0], clamp);
  const open = interpolate(f, [2, 17], [1, 0], { ...clamp, easing: Easing.bezier(0.7, 0, 0.84, 0) });
  const tail = interpolate(f, [17, 26], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
  const head = openingHead(START + f - 780);
  const exitStart = pointOnOpenLine(tail);
  const enterHead = pointOnOpenLine(head);

  return (
    <AbsoluteFill>
      <Glass />
      <SliceWindow open={open} t={START + f} edge={1 - open} />
      {/* Shot 08 dims the picture under the CTA; release it as the frame closes. */}
      <AbsoluteFill style={{ backgroundColor: `rgba(5,5,6,${0.62 * interpolate(f, [0, 12], [1, 0], clamp)})` }} />
      <SelectionBox {...FRAME_RECT} opacity={open} />
      {open < 1 && tail < 1 && (
        <AbsoluteFill style={{ opacity: 1 - open }}>
          <GlowLine x1={exitStart.x} y1={exitStart.y} x2={OPEN_LINE.x2} y2={OPEN_LINE.y2} intensity={1.2} />
        </AbsoluteFill>
      )}
      {head > 0 && <GlowLine x1={OPEN_LINE.x1} y1={OPEN_LINE.y1} x2={enterHead.x} y2={enterHead.y} intensity={1.9} />}
      <AbsoluteFill style={{ opacity: textOut }}>
        <OfferType cta={cta} f={60} />
      </AbsoluteFill>
      <Grain />
    </AbsoluteFill>
  );
};
