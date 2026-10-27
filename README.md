# open-hydra-schema

[![Support me on Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/meridiangray)

A pinned, exact copy of the schema files that ship in [hydra](https://github.com/meridiangray/open-hydra)'s template archive, so the schema has its own version history.

`schema/` mirrors an archive's `.hydra/schema/` folder, file for file:

| Path | What it is |
|---|---|
| `schema/ftm/followthemoney/` | The vendored [FollowTheMoney](https://followthemoney.tech) entity types (MIT, see [NOTICE.md](NOTICE.md)) |
| `schema/ftm/config/` | `common.yaml` (extra record-card fields) and `findfields.yaml` |
| `schema/extensions/` | Types and properties hydra adds on top of FtM (`Artifact`, `sources`, collation) |
| `schema/direction.yaml` | Which end of each relationship is the parent, and which are sideways |
| `schema/params/` | Per-type match, distinct and fold policy |

Everything else in an archive is data or rules, not schema, and is not here: collections, sources, verdicts, `positions.yaml`, `hints.yaml`, parsed builds.

## Keeping it in sync

open-hydra's template is the source of truth; this repository pins it.

```sh
python sync.py            # copy ../open-hydra/src/hydra/template/.hydra/schema into schema/, rewrite MANIFEST.sha256
python sync.py --from DIR # copy from another schema folder
python sync.py --check    # exit 1 if schema/ no longer matches MANIFEST.sha256
python sync.py --check --from ../open-hydra/src/hydra/template/.hydra/schema   # ...or the template itself
```

Commit the result and tag it. `MANIFEST.sha256` lists the SHA-256 of every file, so a tag identifies the exact schema.

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
