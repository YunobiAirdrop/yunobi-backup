#!/usr/bin/env node
// install.mjs — installer for the vertical-video-editing-skill.
//
// Copies the bundled `skills/video-editing/` into a Claude Code skills
// directory so the skill becomes available to Claude.
//
//   npx vertical-video-editing-skill            # install to ~/.claude/skills (user/global)
//   npx vertical-video-editing-skill --project  # install to ./.claude/skills (this project)
//   npx vertical-video-editing-skill --dir PATH # install into PATH/video-editing
//   npx vertical-video-editing-skill --force    # overwrite an existing install
//
// No dependencies — Node 16+ only.

import { cpSync, existsSync, mkdirSync, rmSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const pkgRoot = resolve(__dirname, "..");
const srcSkill = join(pkgRoot, "skills", "video-editing");
const SKILL_NAME = "video-editing";

function parseArgs(argv) {
  const o = { force: false, project: false, dir: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--force" || a === "-f") o.force = true;
    else if (a === "--project" || a === "-p") o.project = true;
    else if (a === "--dir") o.dir = argv[++i];
    else if (a === "--help" || a === "-h") o.help = true;
  }
  return o;
}

function help() {
  console.log(`
vertical-video-editing-skill — installer

Usage:
  npx vertical-video-editing-skill [options]

Options:
  -p, --project    Install into ./.claude/skills (current project)
      --dir PATH   Install into a custom skills directory
  -f, --force      Overwrite an existing install
  -h, --help       Show this help

Default target: ~/.claude/skills/${SKILL_NAME}
`);
}

function version() {
  try {
    return JSON.parse(readFileSync(join(pkgRoot, "package.json"), "utf8")).version;
  } catch {
    return "?";
  }
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) return help();

  if (!existsSync(srcSkill)) {
    console.error(`✗ Bundled skill not found at ${srcSkill}`);
    process.exit(1);
  }

  let skillsDir;
  if (args.dir) skillsDir = resolve(args.dir);
  else if (args.project) skillsDir = resolve(process.cwd(), ".claude", "skills");
  else skillsDir = join(homedir(), ".claude", "skills");

  const dest = join(skillsDir, SKILL_NAME);

  if (existsSync(dest)) {
    if (!args.force) {
      console.error(
        `✗ ${dest} already exists.\n  Re-run with --force to overwrite, or remove it first.`
      );
      process.exit(1);
    }
    rmSync(dest, { recursive: true, force: true });
  }

  mkdirSync(skillsDir, { recursive: true });
  cpSync(srcSkill, dest, { recursive: true });

  console.log(`
✓ Installed video-editing skill (v${version()})
  → ${dest}

Next steps:
  • Restart Claude Code (or reload skills) so it picks up the new skill.
  • Make sure HyperFrames + ffmpeg are available: \`npx hyperframes --version\`, \`ffmpeg -version\`.
  • Add your own visual style under ${dest}/styles/ (copy _template).

Use it by giving Claude a script + media and asking for a finished 9:16 short.
`);
}

main();
