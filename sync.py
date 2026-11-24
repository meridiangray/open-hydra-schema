#!/usr/bin/env python3
"""Copy hydra's schema and archive spec into this repository, exactly (line endings made LF), and record their hashes.

    python sync.py [--from DIR]    copy DIR (default: ../hydra-git/src/hydra/template/.hydra/schema) in one step:
                                     DIR/archive/   -> archive/   (the spec: JSON Schemas and files.yaml)
                                     the rest of DIR -> schema/    (FtM types, extensions, params, direction)
                                   removing files DIR no longer has, regenerate archive/README.md from the
                                   schemas (archive/build_docs.py), and rewrite MANIFEST.sha256
    python sync.py --check         change nothing; exit 1 if schema/, archive/ and MANIFEST.sha256 disagree
                                   (or, with --from, if they differ from DIR; or README.md is out of date)

schema/ mirrors the archive's `.hydra/schema/` folder less its archive/ part: direction.yaml, extensions/, ftm/
(the vendored FollowTheMoney types and config) and params/. archive/ mirrors `.hydra/schema/archive/`, the format
spec hydra reads offline; archive/README.md and archive/build_docs.py live only here. Rules, positions, hints,
verdicts and the like are not schema and are not copied. MANIFEST.sha256 lists `schema/...` and `archive/...`
paths from this repository's root.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE.parent / ("open-hydra" if (HERE.parent / "open-hydra").is_dir() else "hydra-git") / "src" / "hydra" / "template" / ".hydra" / "schema"
DEST = HERE / "schema"
ARCHIVE = HERE / "archive"
OWN = {"README.md", "build_docs.py"}                 # in archive/ only: the generator and what it writes
MANIFEST = HERE / "MANIFEST.sha256"


def files(root: Path, skip: tuple[str, ...] = ()) -> dict[str, Path]:
    return {p.relative_to(root).as_posix(): p for p in sorted(root.rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts and p.relative_to(root).parts[0] not in skip
            and not (p.parent == root and p.name in OWN and root.name == "archive")}


def content(p: Path) -> bytes:
    """A file's bytes with LF line endings: a Windows checkout may hold CRLF, git stores LF
    (see .gitattributes), and the manifest must not depend on which one is on disk."""
    return p.read_bytes().replace(b"\r\n", b"\n")


def digest(p: Path) -> str:
    return hashlib.sha256(content(p)).hexdigest()


def published() -> dict[str, Path]:
    """Every file the manifest covers, by its path from this repository's root."""
    out = {f"schema/{r}": p for r, p in files(DEST).items()}
    out.update({f"archive/{r}": p for r, p in files(ARCHIVE).items()})
    if (ARCHIVE / "README.md").is_file():
        out["archive/README.md"] = ARCHIVE / "README.md"
    return out


def manifest_text() -> str:
    return "".join(f"{digest(p)}  {rel}\n" for rel, p in sorted(published().items()))


def differences(src: Path) -> list[str]:
    """How schema/ and archive/ differ from the source folder."""
    bad = []
    for name, a, b in (("schema", src, DEST), ("archive", src / "archive", ARCHIVE)):
        fa = files(a, skip=("archive",) if name == "schema" else ())
        fb = files(b)
        bad += ([f"only in source: {name}/{r}" for r in fa if r not in fb] + [f"only in {name}/: {r}" for r in fb if r not in fa]
                + [f"differs: {name}/{r}" for r in fa if r in fb and digest(fa[r]) != digest(fb[r])])
    return bad


def docs(check: bool) -> int:
    """Run archive/build_docs.py (needs PyYAML); a missing PyYAML is said, not hidden."""
    r = subprocess.run([sys.executable, str(ARCHIVE / "build_docs.py")] + (["--check"] if check else []))
    return r.returncode


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from", dest="source", type=Path, default=None, help="the schema folder to copy")
    ap.add_argument("--check", action="store_true", help="change nothing; report differences")
    a = ap.parse_args(argv)
    src = (a.source or DEFAULT_SOURCE).resolve()
    if a.check:
        bad = ([] if not a.source else differences(src))
        if not MANIFEST.is_file() or MANIFEST.read_text(encoding="utf-8") != manifest_text():
            bad.append("MANIFEST.sha256 does not match schema/ and archive/")
        if (ARCHIVE / "build_docs.py").is_file() and docs(check=True):
            bad.append("archive/README.md is out of date")
        print("\n".join(bad) if bad else f"ok: {len(published())} files match")
        return 1 if bad else 0
    if not src.is_dir():
        print(f"sync: {src} is not a folder; pass --from <schema folder>", file=sys.stderr)
        return 2
    if src in (DEST, ARCHIVE):
        print("sync: the source is schema/ or archive/ itself", file=sys.stderr)
        return 2
    spec = src / "archive"
    shutil.rmtree(DEST, ignore_errors=True)
    for rel, p in files(src, skip=("archive",)).items():
        (DEST / rel).parent.mkdir(parents=True, exist_ok=True)
        (DEST / rel).write_bytes(content(p))
    if spec.is_dir():
        for old in files(ARCHIVE):
            (ARCHIVE / old).unlink()
        for rel, p in files(spec).items():
            (ARCHIVE / rel).parent.mkdir(parents=True, exist_ok=True)
            (ARCHIVE / rel).write_bytes(content(p))
        if docs(check=False):
            print("sync: archive/README.md was not regenerated (build_docs.py needs PyYAML)", file=sys.stderr)
            return 3
    MANIFEST.write_text(manifest_text(), encoding="utf-8", newline="\n")
    print(f"copied {len(files(DEST))} schema files and {len(files(ARCHIVE))} spec files from {src}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
