// Two-pass EBU R128 loudness normalisation with FFmpeg, then a measurement report.
// Usage: node scripts/master-audio.mjs <in.wav> <out.wav>
// Target: -15 LUFS integrated, <= -3 dBTP pre-encode (release-gates.md suggests -16..-14 LUFS, <= -1 dBTP).
import { spawnSync } from "node:child_process";

const [input, output] = process.argv.slice(2);
// TP leaves headroom for AAC encoding, which adds ~1 dB of inter-sample overshoot on the strike.
const target = { I: -15, TP: -3, LRA: 11 };
// FFmpeg reports filter output on stderr.
const run = (args) => {
  const r = spawnSync("ffmpeg", ["-hide_banner", "-nostats", ...args], { encoding: "utf8" });
  if (r.status !== 0) throw new Error(r.stderr);
  return r.stderr;
};

const ln = `loudnorm=I=${target.I}:TP=${target.TP}:LRA=${target.LRA}`;
const pass1 = run(["-i", input, "-af", `${ln}:print_format=json`, "-f", "null", "-"]);
const m = JSON.parse(pass1.slice(pass1.lastIndexOf("{"), pass1.lastIndexOf("}") + 1));
run([
  "-y", "-i", input, "-af",
  `${ln}:linear=true:measured_I=${m.input_i}:measured_TP=${m.input_tp}:measured_LRA=${m.input_lra}:measured_thresh=${m.input_thresh}:offset=${m.target_offset},aresample=48000`,
  "-c:a", "pcm_s24le", output,
]);
const report = run(["-i", output, "-af", "ebur128=peak=true", "-f", "null", "-"]);
const summary = report.slice(report.lastIndexOf("Summary:"));
console.log(summary.trim());
