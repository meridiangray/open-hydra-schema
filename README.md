# open-hydra-schema

[![Support me on Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/meridiangray)

A pinned, exact copy of the schema files that ship in [hydra](https://github.com/meridiangray/open-hydra)'s template archive, so the schema has its own version history.

`schema/` mirrors an archive's `.hydra/schema/` folder, file for file:

| Path | What it is |
|---|---|
| `schema/ftm/followthemoney/` | The vendored [FollowTheMoney](https://followthemoney.tech) entity types (MIT, see [NOTICE.md](NOTICE.md)) |
| `schema/ftm/config/` | `common.yaml` (extra record-card fields) and `findfields.yaml` |
| `schema/extensions/` | Types and properties hydra adds on top of FtM (`Artifact`, `sources`, `upstream`, collation; deals: `transaction`, `capacity`, Event `amount` / `currency`) |
| `schema/direction.yaml` | Which end of each relationship is the parent, and which are sideways |
| `schema/params/` | Per-type match, distinct and fold policy |
| `schema/wikidata/` | The Wikidata layer, kept apart from FtM and the extensions: `properties.yaml` (which Wikidata property each field and geo-link role is), `classes.yaml` (Wikidata classes to types). Applied after the model loads; every key must name a type and field of that model |
| `archive/` | The archive format itself: one JSON Schema (draft 2020-12) per authored file (`hydra.yaml`, `wiki.yaml`, records, citations, verdicts, tasks, workflows, history snapshots, universe files, packages, `hydra-pack.json`), `files.yaml` naming every file, and [README.md](archive/README.md) generated from them |

Everything else in an archive is data, not schema: collections, sources, verdicts, parsed builds. `archive/` says what shape each file has; the rules files (`positions.yaml`, `hints.yaml`...) are named there and still described by their own header comments.

## Keeping it in sync

open-hydra's template is the source of truth; this repository pins it.

```sh
python sync.py            # copy the template's .hydra/schema into schema/ and its archive/ into archive/ (one step),
                          # rebuild archive/README.md from the schemas, rewrite MANIFEST.sha256
python sync.py --from DIR # copy from another schema folder
python sync.py --check    # exit 1 if schema/ or archive/ no longer matches MANIFEST.sha256, or README.md is stale
python sync.py --check --from ../hydra-git/src/hydra/template/.hydra/schema   # ...or the template itself
```

Commit the result and tag it. `MANIFEST.sha256` lists the SHA-256 of every file (paths from this repository's root: `schema/...`, `archive/...`), so a tag identifies the exact schema and spec. Edit the spec in the template (`.hydra/schema/archive/`), where hydra's coverage test runs against it; never in `archive/` here.

## Using it

You don't need this repository to use hydra: `hydra-ctl init` already puts this schema in every new archive.

Use it to put an existing archive back on a known schema, for example after editing the schema by hand:

```sh
git clone --depth 1 https://github.com/meridiangray/open-hydra-schema
rm -rf /path/to/case/.hydra/schema
cp -r open-hydra-schema/schema /path/to/case/.hydra/schema
hydra-ctl check /path/to/case
hydra-ctl build /path/to/case --force
```

In PowerShell, the middle two lines are:

```powershell
Remove-Item -Recurse -Force C:\path\to\case\.hydra\schema
Copy-Item -Recurse open-hydra-schema\schema C:\path\to\case\.hydra\schema
```

Delete the old folder first: copying on top of it keeps files this version doesn't have.

## License

Copyright (c) 2026 Meridian Gray. MIT licensed ([LICENSE](LICENSE)), the same license as the template this schema comes from. The vendored FollowTheMoney files are MIT too, under their own copyright ([NOTICE.md](NOTICE.md)).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Before a pull request can merge, you agree once to the [Contributor Agreement](CLA.md).
