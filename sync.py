#!/usr/bin/env python3
"""Copy hydra's schema files into this repository, exactly (line endings made LF), and record their hashes.

    python sync.py [--from DIR]    copy DIR (default: ../open-hydra/src/hydra/template/.hydra/schema)
                                   into schema/, removing files DIR no longer has, and rewrite MANIFEST.sha256
    python sync.py --check         change nothing; exit 1 if schema/ and MANIFEST.sha256 disagree
                                   (or, with --from, if schema/ differs from DIR)

schema/ mirrors the archive's `.hydra/schema/` folder: direction.yaml, extensions/,
ftm/ (the vendored FollowTheMoney types and config) and params/. Rules, positions,
hints, verdicts and the like are not schema and are not copied.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE.parent / ("open-hydra" if (HERE.parent / "open-hydra").is_dir() else "hydra-git") / "src" / "hydra" / "template" / ".hydra" / "schema"
DEST = HERE / "schema"
MANIFEST = HERE / "MANIFEST.sha256"


def files(root: Path) -> dict[str, Path]:
    return {p.relative_to(root).as_posix(): p for p in sorted(root.rglob("*")) if p.is_file() and "__pycache__" not in p.parts}


def content(p: Path) -> bytes:
    """A file's bytes with LF line endings: a Windows checkout may hold CRLF, git stores LF
    (see .gitattributes), and the manifest must not depend on which one is on disk."""
    return p.read_bytes().replace(b"\r\n", b"\n")


def digest(p: Path) -> str:
    return hashlib.sha256(content(p)).hexdigest()


def manifest_text(root: Path) -> str:
    return "".join(f"{digest(p)}  {rel}\n" for rel, p in files(root).items())


def differences(a: Path, b: Path) -> list[str]:
    fa, fb = files(a), files(b)
    return ([f"only in {a.name}: {r}" for r in fa if r not in fb] + [f"only in {b.name}: {r}" for r in fb if r not in fa]
            + [f"differs: {r}" for r in fa if r in fb and digest(fa[r]) != digest(fb[r])])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from", dest="source", type=Path, default=None, help="the schema folder to copy")
    ap.add_argument("--check", action="store_true", help="change nothing; report differences")
    a = ap.parse_args(argv)
    src = (a.source or DEFAULT_SOURCE).resolve()
    if a.check:
        bad = ([] if not a.source else differences(src, DEST))
        if not MANIFEST.is_file() or MANIFEST.read_text(encoding="utf-8") != manifest_text(DEST):
            bad.append("MANIFEST.sha256 does not match schema/")
        print("\n".join(bad) if bad else f"ok: {len(files(DEST))} files match")
        return 1 if bad else 0
    if not src.is_dir():
        print(f"sync: {src} is not a folder; pass --from <schema folder>", file=sys.stderr)
        return 2
    if src == DEST:
        print("sync: the source is schema/ itself", file=sys.stderr)
        return 2
    shutil.rmtree(DEST, ignore_errors=True)
    for rel, p in files(src).items():
        (DEST / rel).parent.mkdir(parents=True, exist_ok=True)
        (DEST / rel).write_bytes(content(p))
    MANIFEST.write_text(manifest_text(DEST), encoding="utf-8", newline="\n")
    print(f"copied {len(files(DEST))} files from {src}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
