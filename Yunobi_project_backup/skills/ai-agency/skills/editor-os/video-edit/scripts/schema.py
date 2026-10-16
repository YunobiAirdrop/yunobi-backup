#!/usr/bin/env python3
"""Every file one stage hands the next is checked against its schema, on read and on write.

The schemas live in `../schemas/`, one per file, and the studio reads the same ones through
vibe-kit's `packages/studio/src/schema.ts`. This validator knows only the keywords those schemas use: type,
required, properties, additionalProperties, items, prefixItems, minItems, maxItems, enum, const,
pattern, minimum, minLength and anyOf. A schema using anything else is refused, so a keyword
can't be silently ignored.

A bad file exits 2 with the file, the JSON path and what was expected:

    pins.json: [3].media must be a string

    python3 schema.py pins path/to/pins.json    # check one file by hand
"""
import hashlib, json, os, re, sys

SCHEMAS = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "schemas")
KNOWN = {"$schema", "title", "description", "type", "required", "properties",
         "additionalProperties", "items", "prefixItems", "minItems", "maxItems", "enum", "const",
         "pattern", "minimum", "minLength", "anyOf"}
TYPE_WORD = {"string": "a string", "number": "a number", "integer": "an integer",
             "boolean": "a boolean", "object": "an object", "array": "an array", "null": "null"}


class SchemaError(SystemExit):
    """Exit status 2, with the message kept for a caller that catches it."""

    def __init__(self, message):
        super().__init__(2)
        self.message = message

    def __str__(self):
        return self.message


def schema(name):
    with open(os.path.join(SCHEMAS, name + ".schema.json")) as f:
        return json.load(f)


def _is(value, t):
    if t == "string":
        return isinstance(value, str)
    if t == "integer":
        # 3.0 counts, as it does in JSON Schema and in schema.ts.
        return (isinstance(value, int) and not isinstance(value, bool)) or (
            isinstance(value, float) and value.is_integer())
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "boolean":
        return isinstance(value, bool)
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, list)
    if t == "null":
        return value is None
    raise ValueError("unknown type %r in a schema" % t)


def _show(v):
    return json.dumps(v, ensure_ascii=False)


def _join(path, key):
    if isinstance(key, int):
        return "%s[%d]" % (path, key)
    return "%s.%s" % (path, key) if path else key


def _types(s):
    t = s.get("type")
    return [t] if isinstance(t, str) else (t or [])


def validate(value, s, path=""):
    """Every place `value` breaks schema `s`, as (path, what was expected) pairs."""
    unknown = set(s) - KNOWN
    if unknown:
        raise ValueError("schema keyword %s is not supported by schema.py" % sorted(unknown)[0])
    types = _types(s)
    if types and not any(_is(value, t) for t in types):
        return [(path, "must be " + " or ".join(TYPE_WORD[t] for t in types))]
    if "const" in s and value != s["const"]:
        return [(path, "must be %s" % _show(s["const"]))]
    if "enum" in s and value not in s["enum"]:
        return [(path, "must be one of " + ", ".join(_show(e) for e in s["enum"]))]
    errs = []
    if isinstance(value, str):
        if "minLength" in s and len(value) < s["minLength"]:
            errs.append((path, "must not be empty" if s["minLength"] == 1
                         else "must be at least %d characters" % s["minLength"]))
        if "pattern" in s and not re.search(s["pattern"], value):
            errs.append((path, "must match /%s/" % s["pattern"]))
    if _is(value, "number") and "minimum" in s and value < s["minimum"]:
        errs.append((path, "must be at least %s" % _show(s["minimum"])))
    if isinstance(value, dict):
        for key in s.get("required", []):
            if key not in value:
                errs.append((_join(path, key), "is required"))
        props = s.get("properties", {})
        extra = s.get("additionalProperties", True)
        for key, v in value.items():
            if key in props:
                errs += validate(v, props[key], _join(path, key))
            elif extra is False:
                errs.append((_join(path, key), "is not allowed here (allowed: %s)" % ", ".join(props)))
            elif isinstance(extra, dict):
                errs += validate(v, extra, _join(path, key))
    if isinstance(value, list):
        if "minItems" in s and len(value) < s["minItems"]:
            errs.append((path, "must have at least %d items" % s["minItems"]))
        if "maxItems" in s and len(value) > s["maxItems"]:
            errs.append((path, "must have at most %d items" % s["maxItems"]))
        prefix = s.get("prefixItems", [])
        for i, v in enumerate(value):
            sub = prefix[i] if i < len(prefix) else s.get("items")
            if sub is not None:
                errs += validate(v, sub, _join(path, i))
    if "anyOf" in s:
        errs += _any(value, s["anyOf"], path)
    return errs


def _any(value, branches, path):
    """Pass when one branch passes. Otherwise report the branch the value is closest to."""
    tried = []
    for b in branches:
        types = _types(b)
        if types and not any(_is(value, t) for t in types):
            continue
        e = validate(value, b, path)
        if not e:
            return []
        tried.append(e)
    if not tried:
        words = []
        for b in branches:
            words += [TYPE_WORD[t] for t in _types(b) if TYPE_WORD[t] not in words]
        return [(path, "must be " + " or ".join(words))]
    return min(tried, key=len)


def message(label, errs):
    lines = ["%s: %s" % (label, ("%s %s" % (p, w)) if p else w) for p, w in errs[:10]]
    if len(errs) > 10:
        lines.append("%s: and %d more" % (label, len(errs) - 10))
    return "\n".join(lines)


def check(value, name, label):
    """Raise SchemaError naming every fault, or return the value untouched."""
    errs = validate(value, schema(name))
    if errs:
        _fail(message(label, errs))
    return value


def _fail(msg):
    print(msg, file=sys.stderr)
    raise SchemaError(msg)


def load(path, name):
    """Read and validate one boundary file. `name` is the schema, e.g. "pins"."""
    label = os.path.basename(path)
    try:
        with open(path) as f:
            value = json.load(f)
    except FileNotFoundError:
        _fail("%s: not found at %s" % (label, path))
    except json.JSONDecodeError as e:
        _fail("%s: not valid JSON (line %d column %d: %s)" % (label, e.lineno, e.colno, e.msg))
    return check(value, name, label)


def dump(path, name, value, indent=2):
    """Validate, then write. A writer that produces a bad file is refused before it lands."""
    check(value, name, os.path.basename(path))
    with open(path, "w") as f:
        json.dump(value, f, indent=indent, ensure_ascii=False)
        f.write("\n")


def needle_text(n):
    """The words of one needle, whichever of the four shapes needles.schema.json allows."""
    if isinstance(n, str):
        return n
    if isinstance(n, list):
        return n[1]
    return n.get("t") or n.get("from")


def passes():
    """The ordered pass list both run.py and the studio read."""
    return load(os.path.join(SCHEMAS, "passes.json"), "passes")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    load(sys.argv[2], sys.argv[1])
    print("%s: ok" % os.path.basename(sys.argv[2]))
