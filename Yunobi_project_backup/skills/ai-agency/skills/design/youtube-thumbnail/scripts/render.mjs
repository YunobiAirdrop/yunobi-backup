#!/usr/bin/env node
// Renders one thumbnail from a prompt plus reference images.
//
// No dependencies. Node 20 or later.
//
//   export GOOGLE_API_KEY=...
//   node scripts/render.mjs --prompt prompt.txt --ref face.webp --ref tile.png \
//                          --out out/option-a.png --passes 2
//
// WHY reference images rather than a longer prompt: a photograph of a real person
// is not describable. Handed in as an argument the model composites around it and
// identity is exact and free. Described in words it is invented.
//
// WHY more than one key lane: image quotas run out mid-session and the failure is
// a 429 on the first call of a batch. A second lane turns that into a slower run
// instead of a dead one. A lane is abandoned only when the LANE is the problem
// (429, or 401/403 naming the key). A malformed request is returned as-is, because
// retrying it on the next key just spends the next key on the same bad request.

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import path from "node:path";

const MODEL = process.env.IMAGE_MODEL || "gemini-3.1-flash-image";
// Override to route through a proxy or an AI gateway that speaks the same API.
const BASE = process.env.IMAGE_API_BASE || "https://generativelanguage.googleapis.com/v1beta";

function args(argv) {
  const out = { refs: [], passes: 1 };
  for (let i = 0; i < argv.length; i += 1) {
    const flag = argv[i];
    const value = argv[i + 1];
    if (flag === "--prompt") { out.prompt = value; i += 1; }
    else if (flag === "--text") { out.text = value; i += 1; }
    else if (flag === "--ref") { out.refs.push(value); i += 1; }
    else if (flag === "--out") { out.out = value; i += 1; }
    else if (flag === "--passes") { out.passes = Math.max(1, Number(value) || 1); i += 1; }
    else if (flag === "--aspect") { out.aspect = value; i += 1; }
  }
  return out;
}

// Extra headers for a gateway or proxy, as "Name: value" pairs separated by
// newlines or commas. With these set and no key present, the gateway is assumed
// to hold the upstream credential itself.
function extraHeaders() {
  const raw = process.env.IMAGE_API_HEADERS;
  if (!raw) return {};
  return Object.fromEntries(
    raw.split(/[\n,]+/).map((pair) => pair.trim()).filter(Boolean).map((pair) => {
      const at = pair.indexOf(":");
      return [pair.slice(0, at).trim(), pair.slice(at + 1).trim()];
    }),
  );
}

function lanes() {
  const found = [];
  for (const name of ["GOOGLE_API_KEY", "GOOGLE_API_KEY_BACKUP", "GOOGLE_GENERATIVE_AI_API_KEY"]) {
    const key = process.env[name];
    if (key && !found.some((lane) => lane.key === key)) found.push({ name, key });
  }
  if (found.length === 0 && Object.keys(extraHeaders()).length > 0) {
    found.push({ name: "gateway", key: null });
  }
  return found;
}

const MIME = { ".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg", ".jpeg": "image/jpeg" };

function inlineImage(file) {
  if (!existsSync(file)) throw new Error(`reference image not found: ${file}`);
  const mimeType = MIME[path.extname(file).toLowerCase()];
  if (!mimeType) throw new Error(`unsupported reference type: ${file}`);
  return { inlineData: { mimeType, data: readFileSync(file).toString("base64") } };
}

async function render(prompt, refs, aspect) {
  const body = {
    contents: [{ role: "user", parts: [{ text: prompt }, ...refs.map(inlineImage)] }],
    generationConfig: { responseModalities: ["IMAGE"], imageConfig: { aspectRatio: aspect } },
  };

  let last = "no API key found: set GOOGLE_API_KEY (or IMAGE_API_HEADERS for a gateway)";
  for (const lane of lanes()) {
    const res = await fetch(`${BASE}/models/${MODEL}:generateContent`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        ...extraHeaders(),
        ...(lane.key ? { "x-goog-api-key": lane.key } : {}),
      },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      last = `${lane.name}: ${res.status} ${(await res.text()).slice(0, 300)}`;
      // Only a lane problem justifies spending the next key.
      if (![401, 403, 429].includes(res.status)) break;
      continue;
    }

    const json = await res.json();
    const part = json.candidates?.[0]?.content?.parts?.find((p) => p.inlineData);
    if (!part) { last = `${lane.name}: response carried no image`; continue; }
    return { bytes: Buffer.from(part.inlineData.data, "base64"), lane: lane.name };
  }
  throw new Error(last);
}

const opts = args(process.argv.slice(2));
const prompt = opts.text ?? (opts.prompt ? readFileSync(opts.prompt, "utf8") : null);

if (!prompt || !opts.out) {
  console.error("usage: render.mjs --prompt <file> | --text <string>  --out <file.png>");
  console.error("                  [--ref <image>]...  [--passes N]  [--aspect 16:9]");
  process.exit(1);
}

mkdirSync(path.dirname(path.resolve(opts.out)), { recursive: true });

// Several passes of one prompt differ more than another paragraph of instruction
// would, and picking is cheaper than prompting.
for (let pass = 1; pass <= opts.passes; pass += 1) {
  const file = opts.passes === 1
    ? opts.out
    : opts.out.replace(/(\.[^.]+)$/, `-${pass}$1`);
  try {
    const { bytes, lane } = await render(prompt, opts.refs, opts.aspect ?? "16:9");
    writeFileSync(file, bytes);
    console.log(`ok    ${file}  (${lane})`);
  } catch (error) {
    console.error(`fail  ${file}  ${error.message}`);
    process.exitCode = 1;
  }
}
