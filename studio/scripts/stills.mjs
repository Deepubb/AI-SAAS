// Renders individual frames of a composition with one bundle, for review and QA evidence.
// Usage: node scripts/stills.mjs <compositionId> <outDir> <frame> [frame...]
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import { mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const [id, outDir, ...frames] = process.argv.slice(2);
if (!id || !outDir || frames.length === 0) {
  console.error("usage: node scripts/stills.mjs <compositionId> <outDir> <frame> [frame...]");
  process.exit(1);
}
const studio = join(dirname(fileURLToPath(import.meta.url)), "..");
const browserExecutable = process.env.REMOTION_BROWSER_EXECUTABLE || null;
const serveUrl = await bundle({ entryPoint: join(studio, "src/index.ts") });
const composition = await selectComposition({ serveUrl, id, browserExecutable });
mkdirSync(outDir, { recursive: true });
for (const f of frames.map(Number)) {
  const output = join(outDir, `${id}-f${String(f).padStart(3, "0")}.png`);
  await renderStill({ serveUrl, composition, frame: f, output, browserExecutable, overwrite: true });
  console.log(output);
}
