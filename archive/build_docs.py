#!/usr/bin/env python3
"""Write archive/README.md from the schemas in this folder, so the prose never drifts from the spec.

    python build_docs.py           rewrite README.md
    python build_docs.py --check   change nothing; exit 1 if README.md is not what the schemas would write

Needs PyYAML. The schemas are the source; edit them, never README.md.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
README = HERE / "README.md"
ORDER = ["hydra", "wiki", "record", "citation", "verdicts", "task", "workflow", "snapshot", "universe", "canon",
         "universe-collection", "archetype-decisions", "article", "packages-lock", "package", "pack"]


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def stem(path: Path) -> str:
    return path.name.removesuffix(".schema.yaml")


def squash(text) -> str:
    return " ".join(str(text or "").split())


def cell(text) -> str:
    return squash(text).replace("|", "\\|")


def type_of(s: dict) -> str:
    """A short reading of a (sub)schema's type for the table."""
    if "$ref" in s:
        ref = s["$ref"]
        return f"see [{ref.split('#')[0].removesuffix('.schema.yaml')}](#{ref.split('#')[0].removesuffix('.schema.yaml')})" \
            if not ref.startswith("#") else f"`{ref.rsplit('/', 1)[-1]}`"
    if "const" in s:
        return f"`{s['const']!r}`".replace("'", "")
    if "enum" in s:
        return " or ".join(f"`{str(v).lower() if isinstance(v, bool) else v}`" for v in s["enum"])
    for k in ("anyOf", "oneOf"):
        if k in s:
            return " or ".join(type_of(x) for x in s[k])
    t = s.get("type")
    if isinstance(t, list):
        t = " or ".join(t)
    if t == "array" and isinstance(s.get("items"), dict):
        return f"list of {type_of(s['items'])}"
    return t or "any"


def rows(s: dict, path: str, root: dict, required: bool, done: set, out: list, quiet: bool = False) -> None:
    """Flatten a schema into table rows: (path, type, required, description, status). A definition reached by $ref
    is spelled out the first time and only named after; `quiet` leaves out a row for a branch of anyOf."""
    if "$ref" in s and s["$ref"].startswith("#/"):
        name = s["$ref"].rsplit("/", 1)[-1]
        if name in done:
            if path and not quiet:
                out.append((path, type_of(s), required, s.get("description", ""), ""))
            return
        done.add(name)
        s = {**root.get("$defs", {}).get(name, {}), **{k: v for k, v in s.items() if k != "$ref"}}
    if path and not quiet:
        out.append((path, type_of(s), required, s.get("description", ""), s.get("x-status", "")))
    items = s.get("items")
    if isinstance(items, dict) and ("properties" in items or "$ref" in items or "anyOf" in items):
        rows(items, path + "[]", root, False, done, out)
    for k in ("anyOf", "oneOf"):
        for alt in s.get(k, []):
            if isinstance(alt, dict) and ("properties" in alt or "$ref" in alt or "items" in alt):
                rows(alt, path, root, False, done, out, quiet=True)
    req = set(s.get("required", []))
    for name, sub in (s.get("properties") or {}).items():
        rows(sub, f"{path}.{name}" if path else name, root, name in req, done, out)
    for pat, sub in (s.get("patternProperties") or {}).items():
        rows(sub, f"{path}.`{pat}`" if path else f"`{pat}`", root, False, done, out)
    ap = s.get("additionalProperties")
    if isinstance(ap, dict):
        rows(ap, f"{path}.<name>" if path else "<name>", root, False, done, out)


def section(path: Path) -> str:
    s = load(path)
    name = stem(path)
    status = s.get("x-status")
    lines = [f"## {s.get('title', name)}", "",
             f"`{path.name}`" + (f" &middot; status: **{status}**" if status else ""), "",
             str(s.get("description", "")).strip(), ""]
    out: list = []
    rows(s, "", s, False, set(), out)
    if out:
        lines += ["| Key | Type | Meaning |", "|---|---|---|"]
        for p, t, req, desc, st in out:
            key = f"`{p}`" if not p.startswith("`") and "`" not in p else p
            lines.append(f"| {key}{' *' if req else ''} | {cell(t)} | {cell(desc)}{' (' + st + ')' if st else ''} |")
        lines += ["", "\\* required", ""]
    if s.get("x-renames"):
        r = s["x-renames"]
        lines += [f"Renames read on import: " + ", ".join(f"`{k}` is read as `{v}`" for k, v in r["properties"].items())
                  + f". {squash(r.get('description'))}", ""]
    if s.get("x-import-only"):
        lines += [squash(s["x-import-only"]["description"]), ""]
    return "\n".join(lines)


def files_section() -> str:
    doc = load(HERE / "files.yaml")
    lines = ["## The files", "", "Every authored file an archive holds, and the schema that names it. "
             "Anything not listed here is not part of the format.", "",
             "| Path | Kind | Schema | Note |", "|---|---|---|---|"]
    for f in doc["files"]:
        sch = f"[{f['schema'].removesuffix('.schema.yaml')}](#{f['schema'].removesuffix('.schema.yaml')})" if f.get("schema") else "none yet"
        st = f.get("status")
        lines.append(f"| `{f['path']}` | {f['kind']}{' (' + st + ')' if st else ''} | {sch} | {cell(f.get('note', ''))} |")
    return "\n".join(lines) + "\n"


def render() -> str:
    schemas = {stem(p): p for p in HERE.glob("*.schema.yaml")}
    names = [n for n in ORDER if n in schemas] + sorted(n for n in schemas if n not in ORDER)
    head = ("# The archive format\n\n"
            "Generated from the JSON Schemas (draft 2020-12) in this folder by `build_docs.py`; do not edit by hand. "
            "`files.yaml` names every authored file and the schema that checks it. hydra's `check` validates "
            "`hydra.yaml` and `wiki.yaml` against these; its test suite walks the template and the demo archives and "
            "fails on any file or key this spec does not name.\n")
    body = [files_section()]
    for n in names:
        body.append(section(schemas[n]))
    return head + "\n" + "\n".join(body)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    text = render()
    if a.check:
        ok = README.is_file() and README.read_text(encoding="utf-8").replace("\r\n", "\n") == text
        print("ok" if ok else "archive/README.md is out of date: run build_docs.py", file=sys.stdout if ok else sys.stderr)
        return 0 if ok else 1
    README.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {README} from {len(list(HERE.glob('*.schema.yaml')))} schemas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
