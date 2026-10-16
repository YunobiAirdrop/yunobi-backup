#!/usr/bin/env node
"use strict";

/**
 * This checks that the log scaffold is present, retrofits it where it is not, and appends entries
 * without letting the log grow into a second body.
 */

const { readFileSync, writeFileSync, existsSync, readdirSync, statSync } = require("node:fs");
const { join, basename, dirname, resolve, relative } = require("node:path");

const USAGE = `heal.cjs - keep the failure log inside a skill honest

  heal.cjs check [paths...]              Which skills carry the scaffold, which do not
  heal.cjs retrofit <skill> [--apply]    Add the missing parts of the scaffold
  heal.cjs log <skill> <entry> [--apply] Append a dated entry, newest first
  heal.cjs fold <skill>                  Entries old enough to belong in the body

Options
  --apply       Write the change (retrofit and log are dry runs by default)
  --date <ymd>  Date for a logged entry (default: today, local time)
  --long        Log an entry over 240 characters anyway
  --json        Machine-readable output
  --quiet       Only skills missing something

With no paths, check scans ./skills and ./.claude/skills. Exits 1 when a skill
is missing the scaffold.`;

/** The heading the log lives under. Fixed, because tools and prose both cite it. */
const LOG_HEADING = "## Learned Patterns";

/**
 * The description is preloaded into every session for every skill in the registry, and this sentence
 * does nothing for the choice of which skill to load...
 */
// The quantifier between the verb and the noun is free: "appends new failure modes", "appends every
// new failure mode", "appends any failure it hits" all make the same promise...
const HEAL_PROMISE =
  /appends?\s+(?:\w+\s+){0,3}(?:failure\s+modes?|patterns?)[^.]*\bafter each run\b/i;

/** An entry: `- YYYY-MM-DD: what went wrong, what to do instead.` */
const ENTRY = /^-\s+\*{0,2}(\d{4}-\d{2}-\d{2})\s*(?:\([^)]*\))?\s*[,.:\u2013\u2014-]\s*(.+)$/;

/**
 * Reading only the ISO form reported eight logs as empty while they held between 8 and 300 entries,
 * so the 25-entry ceiling never fired on the logs furthest past it.
 */
const ENTRY_DATED =
  /^-\s+\*{0,2}(\d{1,2})\s+([A-Z][a-z]{2})[a-z]*\.?\s+(\d{4})\s*[,.:\u2014\u2013-]*\s*(.+)$/;
const MONTHS = "jan feb mar apr may jun jul aug sep oct nov dec".split(" ");

/**
 * A skill published for other people to fork carries its lessons without the author's calendar...
 */
const ENTRY_UNDATED = /^-\s+(.+)$/;

/**
 * That is the signal to fold the hardened ones into the prose, not to raise the number.
 */
const LOG_ENTRIES_MAX = 25;

/**
 * Past this many characters an entry has stopped being a rule and started being the story of the run
 * that found it, which belongs in git.
 */
const ENTRY_CHARS_MAX = 240;

/** Entries a log needs before "no replayable ask anywhere" reads as a dropped convention. */
const ASK_COVERAGE_FLOOR = 5;

/**
 * An entry this old has either changed how the body describes the work, or it
 * never mattered. Either way it stops earning its line.
 */
const FOLD_AFTER_DAYS = 180;

function today(override) {
  if (override) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(override)) {
      throw new Error(`--date must be YYYY-MM-DD, got \`${override}\``);
    }
    return override;
  }
  const now = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
}

function daysBetween(from, to) {
  const ms = Date.parse(`${to}T00:00:00Z`) - Date.parse(`${from}T00:00:00Z`);
  return Math.round(ms / 86400000);
}

/** Resolve a skill argument to its SKILL.md, accepting either the file or its directory. */
function skillFile(target) {
  const path = resolve(target);
  if (path.endsWith("SKILL.md")) {
    if (!existsSync(path)) throw new Error(`${path} does not exist.`);
    return path;
  }
  const file = join(path, "SKILL.md");
  if (!existsSync(file))
    throw new Error(`${path} has no SKILL.md, so it is not a skill directory.`);
  return file;
}

/**
 * A flat registry (`.claude/skills/<name>/`) and a packaged source (`ai-doc/skills/<area>/<name>/`)
 * are both real layouts, and a one-level scan reads the packaged one as empty...
 */
function discover(roots) {
  const found = [];
  const walk = (dir, depth) => {
    if (depth > 4) return;
    let entries;
    try {
      entries = readdirSync(dir);
    } catch {
      return;
    }
    for (const entry of entries) {
      if (entry.startsWith(".") || entry === "node_modules") continue;
      const child = join(dir, entry);
      let stats;
      try {
        stats = statSync(child);
      } catch {
        continue; // a dangling symlink is the clean pass's finding, not this one's
      }
      if (!stats.isDirectory()) continue;
      const file = join(child, "SKILL.md");
      if (existsSync(file)) found.push(file);
      else walk(child, depth + 1);
    }
  };
  for (const root of roots) {
    if (!existsSync(root)) continue;
    walk(root, 0);
  }
  return found.toSorted();
}

/**
 * The body is read as text rather than parsed as YAML on purpose: the only frontmatter facts needed
 * here are the name and whether the description makes the promise...
 */
function read(file) {
  const text = readFileSync(file, "utf8");
  const fence = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text);
  const frontmatter = fence ? fence[1] : "";
  const nameMatch = /^name:\s*["']?([^"'\n]+?)["']?\s*$/m.exec(frontmatter);
  const description = readDescription(frontmatter);

  // Case-insensitive: "## Learned patterns" is the same section, and reading it
  // as absent reports a skill with a full log as having none.
  const headingMatch = /\n##\s+learned\s+patterns\s*$/im.exec(text);
  const headingAt = headingMatch ? headingMatch.index : -1;
  const logBlock = headingAt === -1 ? null : text.slice(headingAt + 1);

  // Reading only the section then reports a 60-entry log as empty, so follow the link and count the
  // entries where they actually live.
  let entries = logBlock ? parseEntries(logBlock) : [];
  let entriesFile = null;
  // A skill that points at its log from a `Closing a run` step instead of from a `Learned Patterns`
  // heading is still a skill with a log...
  if (entries.length === 0) {
    const searched = logBlock || text;
    // A pointer written as ``[`x.md`](references/x.md)`` puts the bare filename leftmost, and
    // taking that one alone resolved to a path that does not exist...
    const targets = [...searched.matchAll(/\(([^)]*learn[^)]*\.md)\)|`([^`]*learn[^`]*\.md)`/gi)]
      .map((m) => m[1] || m[2])
      .flatMap((t) => [join(dirname(file), t), join(dirname(file), "references", t)]);
    const resolved = targets.find((t) => existsSync(t));
    if (resolved) {
      entries = parseEntries(readFileSync(resolved, "utf8"), { inBody: false });
      entriesFile = resolved;
    }
  }

  return {
    file,
    text,
    name: nameMatch ? nameMatch[1].trim() : basename(dirname(file)),
    description,
    hasLog: headingAt !== -1 || entriesFile !== null,
    /** True when the log is the last section, which is where it belongs. */
    logIsLast: logBlock !== null && !/\n##\s/.test(logBlock.slice(LOG_HEADING.length + 1)),
    entries,
    /** Set when the entries live in references/ rather than in the body. */
    entriesFile,
    bodyLines: text.split("\n").length,
  };
}

/**
 * Read line by line rather than by regex: a lookahead ending in `$` under /m stops at the first
 * end-of-line...
 */
function readDescription(frontmatter) {
  const lines = frontmatter.split("\n");
  const start = lines.findIndex((l) => l.startsWith("description:"));
  if (start === -1) return "";

  const collected = [lines[start].replace(/^description:\s*/, "")];
  for (let i = start + 1; i < lines.length; i++) {
    if (/^[a-z-]+:/i.test(lines[i])) break; // next top-level key
    collected.push(lines[i]);
  }
  return collected
    .join(" ")
    .replace(/^[|>][-+\d]*\s*/, "") // block scalar indicator
    .replace(/\s+/g, " ")
    .trim();
}

/**
 * Every entry in a log block.
 */
function parseEntries(logBlock, { inBody = true } = {}) {
  const entries = [];
  const seen = new Set();
  const add = (date, text, raw) => {
    const key = normalise(text).toLowerCase();
    if (seen.has(key)) return; // a Contents list and its own headings are one log
    seen.add(key);
    entries.push({ date, text, raw });
  };
  for (const line of logBlock.split("\n")) {
    const trimmed = line.trim();
    // Reading one shape only lost a whole log; reading both without deduping counted every entry
    // twice.
    if (!inBody) {
      const head = /^#{2,3}\s+(.+)$/.exec(trimmed);
      if (head) {
        const [hit] = parseEntries(`- ${head[1]}`, { inBody: false });
        if (hit) add(hit.date, hit.text, trimmed);
        continue;
      }
    }
    // A `## ` heading ends the section, but only inside a body.
    if (inBody && /^##\s/.test(line) && !line.startsWith(LOG_HEADING)) break;
    const iso = ENTRY.exec(trimmed);
    if (iso) {
      add(iso[1], iso[2], trimmed);
      continue;
    }
    const dated = ENTRY_DATED.exec(trimmed);
    if (dated) {
      const month = MONTHS.indexOf(dated[2].toLowerCase());
      if (month === -1) continue;
      const date = `${dated[3]}-${String(month + 1).padStart(2, "0")}-${dated[1].padStart(2, "0")}`;
      add(date, dated[4], trimmed);
    }
    const undated = ENTRY_UNDATED.exec(trimmed);
    if (undated) {
      add(null, undated[1], trimmed);
      continue;
    }
    // Reading only first lines reported every wrapped log as carrying no `[ask: ...]` at all and
    // measured its entries at a fraction of their length...
    const last = entries[entries.length - 1];
    if (last && trimmed !== "" && /^\s+\S/.test(line)) {
      last.text = `${last.text} ${trimmed}`;
      last.raw = `${last.raw}\n${line}`;
    }
  }
  return entries;
}

/**
 * A skill with three of them heals by accident: the promise without the log has nowhere to write,
 * and the log without the final step is never written to.
 */
function audit(skill, now) {
  const missing = [];
  if (!HEAL_PROMISE.test(skill.text)) missing.push("heal-promise");
  // "If a run surfaces" makes the same commitment as "if this run surfaced".
  // What must not pass is a hedge, which is why "consider appending" is not here.
  if (!/if (?:this|a|the) run surface[sd]/i.test(skill.text)) missing.push("execution-step");
  if (!/append(ed)?[^.\n]*\bLearned Patterns\b/i.test(skill.text)) missing.push("checklist-item");
  if (!skill.hasLog) missing.push("learned-patterns");

  const warnings = [];
  if (skill.hasLog && !skill.logIsLast) {
    warnings.push("Learned Patterns is not the last section, so appends land mid-document.");
  }
  if (skill.hasLog && skill.entries.length === 0) {
    warnings.push("Learned Patterns is empty. Seed it from the run that motivated the skill.");
  }
  // A log of one-line rules can hold 128 entries and still be 130 lines, and warning on the count
  // there tells a maintainer to undo the fix.
  const meanChars =
    skill.entries.length > 0
      ? skill.entries.reduce((n, e) => n + e.text.length, 0) / skill.entries.length
      : 0;
  const inlineEvidence = meanChars > ENTRY_CHARS_MAX;
  const overlong = skill.entries.filter((e) => e.text.length > ENTRY_CHARS_MAX);
  if (overlong.length > 0) {
    warnings.push(
      `${overlong.length} entries over ${ENTRY_CHARS_MAX} characters (mean ${Math.round(meanChars)}). ` +
        `Rewrite them as the rule alone; the run belongs in git.`,
    );
  }
  if (skill.entries.length > LOG_ENTRIES_MAX && (inlineEvidence || !skill.entriesFile)) {
    warnings.push(
      `${skill.entries.length} entries is a second body. Compress each entry to its rule ` +
        `with compress_log.py, or fold the hardened ones into the prose.`,
    );
  }
  // WHY count the asks: `[ask: ...]` is the only thing in an entry that can be re-run, and replay
  // is the gap self-healing.md has named open since 2026-08-31.
  const asks = skill.entries.filter((e) => /\[ask:/i.test(e.text));
  if (skill.entries.length >= ASK_COVERAGE_FLOOR && asks.length === 0) {
    warnings.push(
      `No entry carries an \`[ask: ...]\`, so none of these ${skill.entries.length} can be replayed. ` +
        `Add it when a prompt caused the failure.`,
    );
  }
  const stale = skill.entries.filter((e) => e.date && daysBetween(e.date, now) > FOLD_AFTER_DAYS);
  if (stale.length > 0) {
    warnings.push(`${stale.length} entries older than ${FOLD_AFTER_DAYS} days. Run \`fold\`.`);
  }
  const dated = skill.entries.filter((e) => e.date);
  const unordered = dated.some((e, i) => i > 0 && e.date > dated[i - 1].date);
  if (unordered) warnings.push("Entries are not newest first.");

  return { missing, warnings, stale };
}

/**
 * The log goes last because appends target the end of the file, and the execution step goes into the
 * existing flow rather than a new section...
 */
/**
 * Appending to the end of the file is only correct when there is no log yet.
 */
function appendSection(text, section) {
  const heading = /\n##\s+learned\s+patterns\s*$/im.exec(text);
  const body = `${section.replace(/\s*$/, "")}\n`;
  if (!heading) return `${text.replace(/\s*$/, "")}\n\n${body}`;
  return `${text.slice(0, heading.index).replace(/\s*$/, "")}\n\n${body}\n${text.slice(heading.index + 1)}`;
}

function retrofit(skill, missing, now) {
  let text = skill.text;

  const PROMISE = "This skill appends new failure modes to its own pattern list after each run.";

  if (missing.includes("execution-step")) {
    // The promise rides along in the same section, because both parts speak to
    // the session that has already loaded the skill.
    const promise = missing.includes("heal-promise") ? `${PROMISE}\n\n` : "";
    text = appendSection(
      text,
      `## Closing a run\n\n${promise}If this run surfaced a failure mode not already listed, append it to Learned\nPatterns with today's date before finishing. A learning that stays in the\nconversation is lost when the conversation ends.`,
    );
  } else if (missing.includes("heal-promise")) {
    const closing = /\n## Closing a run\s*\n+/.exec(text);
    text = closing
      ? `${text.slice(0, closing.index + closing[0].length)}${PROMISE}\n\n${text.slice(closing.index + closing[0].length)}`
      : appendSection(text, `## Closing a run\n\n${PROMISE}`);
  }

  if (missing.includes("checklist-item")) {
    const checklist = /\n(- \[ \] .+\n)(?!\s*- \[ \])/;
    const item = "- [ ] New failure modes from this run appended to Learned Patterns\n";
    text = checklist.test(text)
      ? text.replace(checklist, (all, last) => `\n${last}${item}`)
      : appendSection(text, `## Verification\n\n${item}`);
  }

  if (missing.includes("learned-patterns")) {
    text = `${text.replace(/\s*$/, "")}\n\n${LOG_HEADING}\n\nAppended when a run surfaces something this skill did not already know. Newest first.\n\n- ${now}: Scaffold added by \`heal.cjs retrofit\`. Replace this line with the first real failure mode; an empty log trains the reader to skip the section.\n`;
  }

  return text;
}

/** One line per entry, dates descending, so the log reads newest first. */
function normalise(entry) {
  return entry.replace(/\s+/g, " ").trim().replace(/\.?$/, ".");
}

/** Compare on content alone, so a re-run does not log what punctuation hid. */
function sameEntry(a, b) {
  return normalise(a).toLowerCase() === normalise(b).toLowerCase();
}

/**
 * The section is rewritten rather than spliced because the log has three parts that a positional
 * insert keeps confusing: the heading, an optional line of prose introducing it...
 */
function appendEntry(skill, entry, now) {
  const line = `- ${now}: ${normalise(entry)}`;
  if (skill.entriesFile) {
    const text = readFileSync(skill.entriesFile, "utf8");
    const lines = text.split("\n");
    // Newest first, so the entry goes above the first one already there. With no
    // entries yet it goes at the end, under whatever prose introduces the file.
    const at = lines.findIndex((l) => ENTRY.test(l.trim()));
    if (at === -1) return `${text.replace(/\s*$/, "")}\n\n${line}\n`;
    // An index of one-line rules runs them together; a log of paragraphs separates them, and mixing
    // the two makes every append visible as a formatting change.
    const spaced = lines
      .slice(at + 1)
      .some((l, i) => l.trim() === "" && ENTRY.test((lines[at + i + 2] || "").trim()));
    lines.splice(at, 0, ...(spaced ? [line, ""] : [line]));
    return lines.join("\n");
  }
  if (!skill.hasLog) {
    return `${skill.text.replace(/\s*$/, "")}\n\n${LOG_HEADING}\n\n${line}\n`;
  }

  const start = skill.text.indexOf(`\n${LOG_HEADING}`) + 1;
  const after = skill.text.slice(start + LOG_HEADING.length);
  // A later `## ` heading ends the section. Without one the section runs to EOF,
  // which is where the log belongs anyway.
  const nextHeading = after.search(/\n##\s/);
  // Stop *on* the newline rather than past it, so the blank line separating the
  // log from whatever follows survives the rewrite.
  const end = nextHeading === -1 ? skill.text.length : start + LOG_HEADING.length + nextHeading;

  const section = skill.text.slice(start, end);
  const intro = [];
  const entries = [];
  for (const line of section.split("\n").slice(1)) {
    const [parsed] = parseEntries(line);
    if (parsed) entries.push(parsed);
    else if (line.trim() !== "") intro.push(line);
  }

  entries.push({ date: now, text: normalise(entry) });
  // Stable within a date, so entries logged on the same day keep the order they
  // were learned in rather than being reshuffled on every write.
  entries.sort((a, b) => {
    if (!a.date || !b.date) return 0;
    return a.date < b.date ? 1 : a.date > b.date ? -1 : 0;
  });

  const rebuilt =
    [
      LOG_HEADING,
      "",
      ...(intro.length > 0 ? [...intro, ""] : []),
      ...entries.map((e) => e.raw || (e.date ? `- ${e.date}: ${e.text}` : `- ${e.text}`)),
    ].join("\n") + "\n";

  return skill.text.slice(0, start) + rebuilt + skill.text.slice(end);
}

function main(argv) {
  const flags = { apply: false, json: false, quiet: false, date: null, long: false };
  const positionals = [];
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--apply") flags.apply = true;
    else if (arg === "--json") flags.json = true;
    else if (arg === "--quiet") flags.quiet = true;
    else if (arg === "--long") flags.long = true;
    else if (arg === "--date") flags.date = argv[++i];
    else if (arg === "-h" || arg === "--help") return usage(0);
    else if (arg.startsWith("--")) {
      process.stderr.write(`unknown flag \`${arg}\`\n\n${USAGE}\n`);
      return 2;
    } else positionals.push(arg);
  }

  const [command = "check", ...rest] = positionals;
  if (command === "help") return usage(0);

  const now = today(flags.date);
  const short = (p) => {
    const rel = relative(process.cwd(), p);
    return rel && !rel.startsWith("..") ? rel : p;
  };

  if (command === "check") {
    const roots =
      rest.length > 0
        ? rest.map((r) => resolve(r))
        : [resolve("skills"), resolve(".claude/skills")];
    // A root that is itself a skill is the single-skill case, not a registry.
    const files = roots.flatMap((root) =>
      existsSync(join(root, "SKILL.md")) ? [join(root, "SKILL.md")] : discover([root]),
    );
    if (files.length === 0) {
      process.stderr.write(`No SKILL.md found under ${roots.map(short).join(", ")}\n`);
      return 2;
    }

    const results = files.map((file) => {
      const skill = read(file);
      const { missing, warnings } = audit(skill, now);
      return { name: skill.name, path: file, entries: skill.entries.length, missing, warnings };
    });

    if (flags.json) {
      process.stdout.write(`${JSON.stringify({ checked: results.length, results }, null, 2)}\n`);
    } else {
      const shown = flags.quiet
        ? results.filter((r) => r.missing.length > 0 || r.warnings.length > 0)
        : results;
      const healing = results.filter((r) => r.missing.length === 0).length;
      process.stdout.write(`${healing}/${results.length} skills carry the failure log\n\n`);
      for (const r of shown) {
        const mark = r.missing.length === 0 ? "ok  " : "miss";
        const detail = r.missing.length === 0 ? `${r.entries} entries` : r.missing.join(", ");
        process.stdout.write(`  ${mark}  ${r.name}  ${detail}\n`);
        for (const w of r.warnings) process.stdout.write(`        ${w}\n`);
      }
      const broken = results.filter((r) => r.missing.length > 0);
      if (broken.length > 0) {
        process.stdout.write(`\nRetrofit one with \`heal.cjs retrofit <skill> --apply\`.\n`);
      }
    }
    return results.some((r) => r.missing.length > 0) ? 1 : 0;
  }

  if (command === "retrofit") {
    const [target] = rest;
    if (!target) {
      process.stderr.write("retrofit needs a skill directory or SKILL.md\n");
      return 2;
    }
    const file = skillFile(target);
    const skill = read(file);
    const { missing } = audit(skill, now);
    if (missing.length === 0) {
      process.stdout.write(`${skill.name} already carries all four parts.\n`);
      return 0;
    }
    const next = retrofit(skill, missing, now);
    if (flags.apply) writeFileSync(file, next);
    const prefix = flags.apply ? "added" : "would add";
    process.stdout.write(`${prefix} to ${short(file)}: ${missing.join(", ")}\n`);
    if (!flags.apply) process.stdout.write("\nRe-run with --apply to write it.\n");
    return 0;
  }

  if (command === "log") {
    const [target, ...words] = rest;
    // Strip it before the ceiling and the duplicate check, so both judge the rule alone.
    const entry = words
      .join(" ")
      .trim()
      .replace(/^\d{4}-\d{2}-\d{2}\s*:\s*/, "");
    if (!target || !entry) {
      process.stderr.write(
        'log needs a skill and an entry: heal.cjs log ./skills/x "what went wrong, what to do instead"\n',
      );
      return 2;
    }
    // Refuse before reading the skill: the writer has the run in front of them and is the only one
    // who can say which sentence is the rule.
    if (normalise(entry).length > ENTRY_CHARS_MAX && !flags.long) {
      process.stderr.write(
        `Entry is ${normalise(entry).length} characters; the ceiling is ${ENTRY_CHARS_MAX}.\n` +
          `Lead with the law, keep one checkable anchor, drop the run. --long to override.\n`,
      );
      return 2;
    }
    const file = skillFile(target);
    const skill = read(file);
    if (skill.entries.some((e) => sameEntry(e.text, entry))) {
      process.stdout.write(`Already logged, not repeating it.\n`);
      return 0;
    }
    const next = appendEntry(skill, entry, now);
    const dest = skill.entriesFile || file;
    if (flags.apply) writeFileSync(dest, next);
    const prefix = flags.apply ? "logged" : "would log";
    process.stdout.write(`${prefix} to ${short(dest)}:\n  - ${now}: ${entry}\n`);
    if (!flags.apply) process.stdout.write("\nRe-run with --apply to write it.\n");
    return 0;
  }

  if (command === "fold") {
    const [target] = rest;
    if (!target) {
      process.stderr.write("fold needs a skill directory or SKILL.md\n");
      return 2;
    }
    const skill = read(skillFile(target));
    const { stale } = audit(skill, now);
    if (flags.json) {
      process.stdout.write(`${JSON.stringify({ name: skill.name, stale }, null, 2)}\n`);
      return 0;
    }
    if (stale.length === 0) {
      process.stdout.write(
        `Nothing has hardened yet. ${skill.entries.length} entries, all recent.\n`,
      );
      return 0;
    }
    process.stdout.write(
      `${stale.length} entries older than ${FOLD_AFTER_DAYS} days.\n` +
        `Each one either changed how the body describes the work, in which case say it in the\n` +
        `body and delete the line, or it never mattered and the line goes anyway.\n\n`,
    );
    for (const e of stale) process.stdout.write(`  ${e.date}  ${e.text}\n`);
    return 0;
  }

  process.stderr.write(`unknown command \`${command}\`\n\n${USAGE}\n`);
  return 2;
}

function usage(code) {
  process.stdout.write(`${USAGE}\n`);
  return code;
}

if (require.main === module) {
  try {
    process.exitCode = main(process.argv.slice(2));
  } catch (error) {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = 2;
  }
}

module.exports = { read, audit, retrofit, appendEntry, parseEntries, discover, daysBetween };
