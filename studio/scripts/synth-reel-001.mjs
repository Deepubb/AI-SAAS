// Original, procedurally synthesized sound design + score for Reel 001 (no samples, no
// third-party audio). Every cue is placed on the frame where the picture event happens;
// see reels/reel-001/sfx_cues.csv and edit_notes.md. Output: public/audio/reel-001-raw.wav
import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const SR = 48000;
const FPS = 30;
const FRAMES = 780;
const N = Math.round((FRAMES / FPS) * SR);
const L = new Float32Array(N);
const R = new Float32Array(N);
const at = (frame) => Math.round((frame / FPS) * SR);
const sec = (s) => Math.round(s * SR);

let seed = 7;
const rnd = () => {
  seed = (seed * 1664525 + 1013904223) >>> 0;
  return (seed / 4294967296) * 2 - 1;
};

// ---------- building blocks ----------
const noise = (len) => Float32Array.from({ length: len }, rnd);
const brown = (len) => {
  const out = new Float32Array(len);
  let v = 0;
  for (let i = 0; i < len; i++) {
    v = (v + 0.02 * rnd()) * 0.998;
    out[i] = v * 3.5;
  }
  return out;
};

// RBJ biquad; `freq` may be a number or a function of progress 0..1 (updated every 32 samples).
const biquad = (x, type, freq, q = 0.707) => {
  const y = new Float32Array(x.length);
  let x1 = 0, x2 = 0, y1 = 0, y2 = 0, b0, b1, b2, a1, a2;
  const coeffs = (f) => {
    const w = (2 * Math.PI * Math.min(f, SR * 0.45)) / SR;
    const cs = Math.cos(w), al = Math.sin(w) / (2 * q);
    let c;
    if (type === "lp") c = [(1 - cs) / 2, 1 - cs, (1 - cs) / 2];
    else if (type === "hp") c = [(1 + cs) / 2, -(1 + cs), (1 + cs) / 2];
    else c = [al, 0, -al];
    const a0 = 1 + al;
    [b0, b1, b2] = c.map((v) => v / a0);
    a1 = (-2 * cs) / a0;
    a2 = (1 - al) / a0;
  };
  for (let i = 0; i < x.length; i++) {
    if (i % 32 === 0) coeffs(typeof freq === "function" ? freq(i / x.length) : freq);
    const v = b0 * x[i] + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2;
    x2 = x1; x1 = x[i]; y2 = y1; y1 = v;
    y[i] = v;
  }
  return y;
};

// Attack (s) then exponential decay with time constant tau (s).
const env = (len, attack, tau) =>
  Float32Array.from({ length: len }, (_, i) => {
    const t = i / SR;
    return t < attack ? t / attack : Math.exp(-(t - attack) / tau);
  });

// Sine with frequency function f(progress) and optional extra harmonics.
const tone = (len, f, harmonics = [1]) => {
  const out = new Float32Array(len);
  let ph = 0;
  for (let i = 0; i < len; i++) {
    const fr = typeof f === "function" ? f(i / len) : f;
    ph += (2 * Math.PI * fr) / SR;
    let v = 0;
    harmonics.forEach((a, k) => (v += a * Math.sin(ph * (k + 1))));
    out[i] = v;
  }
  return out;
};

const mul = (a, b) =>
  a.map((v, i) => v * (typeof b === "number" ? b : typeof b === "function" ? b(i / a.length) : b[i]));
const mix = (...xs) => {
  const out = new Float32Array(Math.max(...xs.map((x) => x.length)));
  xs.forEach((x) => x.forEach((v, i) => (out[i] += v)));
  return out;
};
const bell = (p) => Math.sin(Math.PI * p);

// Place mono signal at sample `start` with equal-power pan (-1..1, or a function of progress).
const place = (start, x, gain = 1, pan = 0) => {
  for (let i = 0; i < x.length; i++) {
    const n = start + i;
    if (n < 0 || n >= N) continue;
    const p = typeof pan === "function" ? pan(i / x.length) : pan;
    const a = ((p + 1) * Math.PI) / 4;
    L[n] += x[i] * gain * Math.cos(a);
    R[n] += x[i] * gain * Math.sin(a);
  }
};

// ---------- cues ----------
const slice = () => {
  const len = sec(0.7);
  const bright = mul(biquad(noise(len), "hp", 4200), env(len, 0.001, 0.045));
  const zing = mul(tone(len, (p) => 1800 + 5200 * Math.exp(-p * 40)), env(len, 0.001, 0.03));
  const thump = mul(tone(len, (p) => 50 + 45 * Math.exp(-p * 12)), env(len, 0.002, 0.12));
  const tail = mul(biquad(noise(len), "bp", 2200, 1.2), env(len, 0.002, 0.2));
  return mix(mul(bright, 0.8), mul(zing, 0.28), mul(thump, 0.75), mul(tail, 0.16));
};

const pulse = () => {
  const len = sec(0.55);
  return mul(tone(len, 55, [1, 0.35, 0.1]), env(len, 0.012, 0.16));
};

const glassPass = () => {
  const len = sec(0.9);
  const partials = [620, 905, 1270, 1730, 2410].map((f, k) => mul(tone(len, f), env(len, 0.002, 0.28 / (1 + k * 0.4))));
  const body = mix(...partials.map((p, k) => mul(p, 0.22 / (k + 1))));
  const scrape = mul(biquad(noise(len), "bp", 1500, 2), env(len, 0.004, 0.06));
  return mix(body, mul(scrape, 0.35));
};

const airHit = () => {
  const len = sec(0.5);
  return mix(
    mul(biquad(noise(len), "hp", 6000), env(len, 0.001, 0.09)),
    mul(biquad(noise(len), "bp", (p) => 3200 - 2200 * p, 3), env(len, 0.003, 0.15)),
  );
};

const knock = () => {
  const len = sec(0.4);
  return mix(
    mul(tone(len, (p) => 120 + 70 * Math.exp(-p * 20)), env(len, 0.001, 0.07)),
    mul(biquad(noise(len), "bp", 1200, 3), env(len, 0.0005, 0.008)),
  );
};

const sweep = (len, from, to, q = 1.5) => mul(biquad(noise(len), "bp", (p) => from + (to - from) * p, q), bell);

const click = (freq = 3200, body = 900) => {
  const len = sec(0.12);
  return mix(
    mul(biquad(noise(len), "bp", freq, 4), env(len, 0.0003, 0.004)),
    mul(tone(len, body), mul(env(len, 0.0005, 0.012), 0.3)),
  );
};

const snap = (pitch) => {
  const len = sec(0.15);
  return mix(
    mul(biquad(noise(len), "bp", 2400 * pitch, 3), env(len, 0.0003, 0.006)),
    mul(tone(len, 420 * pitch), mul(env(len, 0.001, 0.025), 0.35)),
  );
};

const subImpact = () => {
  const len = sec(2.4);
  return mix(
    mul(tone(len, (p) => 40 + 32 * Math.exp(-p * 9), [1, 0.15]), env(len, 0.003, 0.55)),
    mul(mul(biquad(noise(len), "hp", 5000), env(len, 0.002, 0.35)), 0.22),
  );
};

// Additive pad: detuned pairs, soft harmonics, filter swept by `cutoff(progress)`.
const pad = (len, freqs, amp, cutoff) => {
  const voices = freqs.flatMap((f) => [f * 0.9985, f * 1.0015]).map((f) => tone(len, f, [1, 0.5, 0.33, 0.25, 0.2, 0.16]));
  return mul(biquad(mix(...voices), "lp", cutoff), amp);
};

// ---------- timeline (frames) ----------
// 0: slice strike — pans with the line travelling bottom-left to top-right
place(at(0), slice(), 0.9, (p) => -0.6 + Math.min(1, p * 6) * 1.2);
// 3..107: low pulse motif, 100 BPM, stops dead for the micro-drop at 108
for (let f = 3; f < 108; f += 18) place(at(f), pulse(), 0.55);
// Montage edit points: three distinct textures
place(at(36), glassPass(), 0.8, -0.25);
place(at(60), airHit(), 0.45, 0.1);
place(at(84), knock(), 0.7, 0.2);
// Movement pass tracking the glint left -> right across the montage
place(at(62), sweep(at(46), 500, 2600), 0.18, (p) => -0.85 + 1.7 * p);
// 122: the "?" lands — one close dry click in silence
place(at(122), click(3400, 950), 0.75);
// 156..396: deeper studio room tone under the schematic and proof
place(at(150), mul(biquad(biquad(brown(at(252)), "lp", 220), "hp", 45), (p) => Math.min(1, p * 8, (1 - p) * 8)), 0.045);
// 166..190: five micro mechanical snaps on each layer arrival, alternating sides
[166, 172, 178, 184, 190].forEach((f, i) => place(at(f), snap(1 + i * 0.09), 0.55, i % 2 ? 0.35 : -0.35));
// 200..262: subtle rising motif
[220, 261.63, 329.63, 440].forEach((f, i) => {
  const len = sec(1.1);
  place(at(200 + i * 15), mul(tone(len, f, [1, 0.3, 0.1]), env(len, 0.06, 0.4)), 0.09, -0.2 + i * 0.13);
});
// 240..269: convergence riser into the node, hard stop on the cut
place(at(240), mul(sweep(at(30), 300, 3200, 1.2), (p) => p * p), 0.25);
// 270..395: proof cards — bass transfer on each cut, switch tick when the highlight locks
[270, 301, 332, 364].forEach((f) => {
  const len = sec(0.4);
  place(at(f), mul(tone(len, 70, [1, 0.2]), env(len, 0.003, 0.11)), 0.5);
  place(at(f), click(2600, 700), 0.35);
  place(at(f + 7), click(4200, 1300), 0.3, 0.15);
});
// 384..396: swell under the type-to-frame match cut
place(at(380), mul(sweep(at(16), 900, 2400, 1), (p) => p), 0.16);
// 396..456: rising harmonic build (A minor add9), filter opening into the hit
{
  const len = at(60);
  const build = pad(len, [110, 164.81, 220, 246.94, 261.63, 329.63], 0.05, (p) => 300 + 3800 * p * p);
  place(at(396), mul(build, (p) => p * p), 1);
}
// 406..438: modules snap home
[406, 414, 422, 430, 438].forEach((f, i) => place(at(f), snap(0.85 + i * 0.07), 0.5, i % 2 ? 0.45 : -0.45));
// 456: sub impact on the hero resolve, then a sustained afterglow to 528
place(at(456), subImpact(), 0.95);
{
  const len = at(76);
  const glow = pad(len, [110, 164.81, 220, 329.63, 493.88], 0.04, 2200);
  place(at(456), mul(glow, (p) => Math.min(1, p * 10) * (1 - p) ** 1.5), 1);
}
// 528: a breath, then the warm sustained chord (F maj9) through the CTA
{
  const len = at(250);
  const chord = pad(len, [87.31, 130.81, 220, 261.63, 329.63, 392], 0.035, 1800);
  const shape = (p) => {
    const s = p * len / SR;
    const attack = Math.min(1, Math.max(0, (s - 0.15) / 0.7));
    const release = Math.min(1, Math.max(0, (8.0 - s) / 0.7));
    return attack * release * (0.85 + 0.15 * Math.sin(2 * Math.PI * 0.25 * s));
  };
  place(at(528), mul(chord, shape), 1);
}
// 542, 572: type locks
place(at(542), click(2800, 160), 0.6, -0.1);
place(at(572), click(2800, 180), 0.6, 0.1);
// 632: soft tactile CTA arrival, then a light textured beat
place(at(632), mix(mul(tone(sec(0.2), 600), env(sec(0.2), 0.002, 0.025)), mul(biquad(noise(sec(0.2)), "lp", 1500), env(sec(0.2), 0.001, 0.015))), 0.4);
for (let f = 641, k = 0; f < 740; f += 9, k++) {
  const len = sec(0.12);
  place(at(f), mul(biquad(noise(len), "hp", 7000), env(len, 0.001, 0.022)), 0.07, k % 2 ? 0.4 : -0.4);
  if (k % 2 === 0) place(at(f), mul(tone(sec(0.3), 58), env(sec(0.3), 0.003, 0.08)), 0.16);
}
// 746..770: frame closes into the slit, line exits right
place(at(746), sweep(at(16), 3000, 700, 1.2), 0.16, 0);
place(at(761), sweep(at(10), 1200, 4200, 2), 0.14, (p) => p * 0.9);
// 775..779: the new line's approach, leading straight into the frame-0 strike
place(at(774), mul(biquad(noise(at(6)), "hp", 3000), (p) => p ** 3), 0.18, -0.6);
// Low room bed for the whole film so silences are designed, not digital
place(0, biquad(biquad(brown(N), "lp", 260), "hp", 40), 0.007);

// Edge fades: 2 ms in (the strike still reads as a hard transient), 8 ms out to avoid a pop at the loop seam.
for (let i = 0; i < sec(0.002); i++) { const g = i / sec(0.002); L[i] *= g; R[i] *= g; }
for (let i = 0; i < sec(0.008); i++) { const g = i / sec(0.008); L[N - 1 - i] *= g; R[N - 1 - i] *= g; }

// ---------- write 24-bit PCM WAV ----------
let peak = 0;
for (let i = 0; i < N; i++) peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i]));
const norm = 0.5 / peak; // headroom for the mastering pass
const data = Buffer.alloc(N * 2 * 3);
for (let i = 0; i < N; i++) {
  [L[i], R[i]].forEach((v, c) => {
    const s = Math.max(-8388608, Math.min(8388607, Math.round(v * norm * 8388607)));
    data.writeIntLE(s, (i * 2 + c) * 3, 3);
  });
}
const header = Buffer.alloc(44);
header.write("RIFF", 0);
header.writeUInt32LE(36 + data.length, 4);
header.write("WAVEfmt ", 8);
header.writeUInt32LE(16, 16);
header.writeUInt16LE(1, 20);
header.writeUInt16LE(2, 22);
header.writeUInt32LE(SR, 24);
header.writeUInt32LE(SR * 2 * 3, 28);
header.writeUInt16LE(6, 32);
header.writeUInt16LE(24, 34);
header.write("data", 36);
header.writeUInt32LE(data.length, 40);
const out = join(dirname(fileURLToPath(import.meta.url)), "..", "public", "audio", "reel-001-raw.wav");
mkdirSync(dirname(out), { recursive: true });
writeFileSync(out, Buffer.concat([header, data]));
console.log(`wrote ${out} (${(N / SR).toFixed(2)} s)`);
