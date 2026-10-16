#!/usr/bin/env node
// Prints the best-performing short-form transcripts for a niche, ranked by breakout, to read before drafting.
// usage: node top-band.mjs [keyword ...] [--n 8] [--max-seconds 90]
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

// The transcripts folder: COMPETITOR_INTEL_DATA, or `top-band.internal.json` beside this file, which stays out of the public copy.
const local = new URL("top-band.internal.json", import.meta.url);
const configured =
  process.env.COMPETITOR_INTEL_DATA ??
  (fs.existsSync(local) ? JSON.parse(fs.readFileSync(local, "utf8")).data : null);
if (!configured) {
  console.error("Set COMPETITOR_INTEL_DATA to the folder of <source>/tiktok-transcripts/ exports.");
  process.exit(1);
}
const DATA = configured.replace(/^~(?=\/)/, os.homedir());
const args = process.argv.slice(2);
const flag = (name, fallback) => {
  const i = args.indexOf(name);
  return i === -1 ? fallback : Number(args.splice(i, 2)[1]);
};
const n = flag("--n", 8);
const maxSeconds = flag("--max-seconds", 90);
const keywords = args.map((k) => k.toLowerCase());

const rows = [];
for (const src of fs.readdirSync(DATA)) {
  const dir = path.join(DATA, src, "tiktok-transcripts");
  if (!fs.existsSync(dir)) continue;
  for (const file of fs.readdirSync(dir)) {
    try {
      const j = JSON.parse(fs.readFileSync(path.join(dir, file), "utf8"));
      const text = j.fullText ?? "";
      if (!text || (j.durationSeconds ?? 0) > maxSeconds) continue;
      if (keywords.length && !keywords.some((k) => text.toLowerCase().includes(k))) continue;
      rows.push({ src, breakout: j.breakout ?? 0, seconds: j.durationSeconds, url: j.url, text });
    } catch {}
  }
}
rows.sort((a, b) => b.breakout - a.breakout);
console.log(
  `${rows.length} Shorts match${keywords.length ? ` [${keywords.join(", ")}]` : ""}; top ${Math.min(n, rows.length)} by breakout:\n`,
);
for (const r of rows.slice(0, n)) {
  console.log(`## ${r.src}, ${r.breakout.toFixed(1)}x, ${r.seconds}s  ${r.url}\n${r.text}\n`);
}
