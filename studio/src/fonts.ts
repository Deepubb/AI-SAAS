import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";
import { fonts } from "./theme";

// Inter Display (OFL-1.1) and JetBrains Mono (Apache-2.0), bundled in public/fonts with their licenses.
const faces = [
  { family: fonts.display, file: "InterDisplay-Medium.otf", weight: "500" },
  { family: fonts.display, file: "InterDisplay-Bold.otf", weight: "700" },
  { family: fonts.display, file: "InterDisplay-Black.otf", weight: "900" },
  { family: fonts.mono, file: "JetBrainsMono-Regular.ttf", weight: "400" },
  { family: fonts.mono, file: "JetBrainsMono-Medium.ttf", weight: "500" },
];

export const fontsReady = Promise.all(
  faces.map((f) => loadFont({ family: f.family, url: staticFile(`fonts/${f.file}`), weight: f.weight })),
);
