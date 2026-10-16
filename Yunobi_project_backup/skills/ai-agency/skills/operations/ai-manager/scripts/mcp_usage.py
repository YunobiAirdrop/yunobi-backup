#!/usr/bin/env python3
"""MCP servers, subagents and plugin skills actually called in the last N days.

Usage: python3 mcp_usage.py [days=45]
Counts tool_use events in ~/.claude/projects/*/*.jsonl, then lists every configured
server with zero calls: the delete candidates for the session-context pass.
"""
import collections, glob, json, os, re, sys, time
from pathlib import Path

days = int(sys.argv[1]) if len(sys.argv) > 1 else 45
home = Path.home()
cutoff = time.time() - days * 86400
files = [f for f in glob.glob(str(home / ".claude/projects/*/*.jsonl")) if os.path.getmtime(f) > cutoff]

tool = re.compile(r'"type":"tool_use","id":"[^"]*","name":"mcp__([^"]+?)__')
agent = re.compile(r'"subagent_type":"([^"]+)"')
skill = re.compile(r'"skill":"([a-z0-9-]+:[^"]+)"')
calls, last, repos, agents, skills = (collections.Counter(), {}, collections.defaultdict(set),
                                      collections.Counter(), collections.Counter())
for f in files:
    text = open(f, errors="ignore").read()
    repo = Path(f).parent.name.replace("-Users-" + home.name + "-Studio-", "")
    for m in tool.findall(text):
        calls[m] += 1
        repos[m].add(repo)
        last[m] = max(last.get(m, 0), os.path.getmtime(f))
    agents.update(agent.findall(text))
    skills.update(skill.findall(text))

print(f"{len(files)} transcripts, last {days} days\n\nMCP calls:")
for name, n in calls.most_common():
    print(f"  {n:5}  {name:40} last {time.strftime('%m-%d', time.localtime(last[name]))}  {','.join(sorted(repos[name])[:4])}")

configured = {}
cj = json.loads((home / ".claude.json").read_text())
for k in cj.get("mcpServers", {}):
    configured[k] = "user"
for proj, v in cj.get("projects", {}).items():
    for k in v.get("mcpServers", {}) or {}:
        configured.setdefault(k, Path(proj).name)
for f in glob.glob(str(home / "Studio/*/.mcp.json")):
    for k in json.loads(Path(f).read_text()).get("mcpServers", {}):
        configured.setdefault(k, Path(f).parent.name)
dead = [f"{k} ({w})" for k, w in sorted(configured.items()) if not any(c == k or c.startswith(k.replace("-", "_")) for c in calls)]
print("\nConfigured, never called:\n  " + ("\n  ".join(dead) or "none"))
print("\nSubagents:", ", ".join(f"{k} {n}" for k, n in agents.most_common(15)) or "none")
print("Plugin skills:", ", ".join(f"{k} {n}" for k, n in skills.most_common(15)) or "none")
env = json.loads((home / ".claude/settings.json").read_text()).get("env", {})
print("\nclaude.ai connectors:", "off" if env.get("ENABLE_CLAUDEAI_MCP_SERVERS") == "false" else "ON (every one loads its schemas)")
print("Claude in Chrome default:", cj.get("claudeInChromeDefaultEnabled"))
