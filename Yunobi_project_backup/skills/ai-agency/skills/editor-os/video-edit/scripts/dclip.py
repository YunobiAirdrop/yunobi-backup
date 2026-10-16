#!/usr/bin/env python3
"""Read/write the Descript rich pasteboard on the macOS clipboard."""

"""Usage:  python3 dclip.py [dump|load] [file]     (default: dump)"""
import base64, json, re, subprocess, sys, html, os, tempfile

HTML_GET = 'the clipboard as \xabclass HTML\xbb'

def osa(script):
    """Run AppleScript from a UTF-8 temp file.

    Never through stdin: osascript decodes piped bytes as MacRoman, so the
    \xab...\xbb raw-type brackets arrive mangled and the coercion fails with
    -1700 (seen 2026-08-20). A file also sidesteps the argv size limit."""
    fd, path = tempfile.mkstemp(suffix=".applescript")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f: f.write(script)
        return subprocess.run(["osascript", path], capture_output=True, text=True)
    finally:
        os.unlink(path)

def read_html():
    out = osa(HTML_GET)
    m = re.search(r'\xabdata HTML([0-9A-Fa-f]+)\xbb', out.stdout)
    if not m: sys.exit("no HTML flavor on clipboard: "+out.stderr.strip())
    return bytes.fromhex(m.group(1)).decode("utf-8","replace")

def decode():
    h = read_html()
    m = re.search(r'data-descript-pasteboard="([^"]+)"', h)
    if not m: sys.exit("no data-descript-pasteboard in HTML flavor")
    return json.loads(base64.b64decode(html.unescape(m.group(1)))), h

def write(payload, plain):
    b64 = base64.b64encode(json.dumps(payload,separators=(",",":")).encode()).decode()
    doc = "<meta charset='utf-8'><span data-descript-pasteboard=\"%s\">%s</span>" % (
        b64, html.escape(plain))
    hexs = doc.encode("utf-8").hex()
    script = ('set the clipboard to {\xabclass HTML\xbb:\xabdata HTML%s\xbb, '
              'string:"%s"}') % (hexs, plain.replace("\\","\\\\").replace('"','\\"').replace("\n","\\n"))
    r = osa(script)
    if r.returncode: sys.exit("clipboard write failed: "+r.stderr.strip())

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv)>1 else "dump"
    if cmd == "dump":
        p,_ = decode(); json.dump(p, open(sys.argv[2],"w"), indent=1)
        d = p["data"][0]
        print("taus", len(d["copiedTaus"]), "| chars", sum(len(t["text"]["string"]) for t in d["copiedTaus"]))
        for m in d["mediaRefsCopyData"]:
            al=(m["mediaRef"].get("voiceover") or {}).get("metadata",{}).get("alignment")
            if al: print("  alignment on", m["mediaRef"]["id"][:8], len(al), "words")
    elif cmd == "roundtrip":
        p,_ = decode(); plain = "".join(p.get("text") or [])
        write(p, plain)
        q,_ = decode()
        print("roundtrip identical:", json.dumps(q,sort_keys=True)==json.dumps(p,sort_keys=True))
