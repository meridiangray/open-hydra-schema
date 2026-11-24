# The archive format

Generated from the JSON Schemas (draft 2020-12) in this folder by `build_docs.py`; do not edit by hand. `files.yaml` names every authored file and the schema that checks it. hydra's `check` validates `hydra.yaml` and `wiki.yaml` against these; its test suite walks the template and the demo archives and fails on any file or key this spec does not name.

## The files

Every authored file an archive holds, and the schema that names it. Anything not listed here is not part of the format.

| Path | Kind | Schema | Note |
|---|---|---|---|
| `hydra.yaml` | authored | [hydra](#hydra) |  |
| `wiki.yaml` | authored | [wiki](#wiki) |  |
| `hydra-package.yaml` | derived | [package](#package) | only inside a package |
| `hydra-pack.json` | derived | [pack](#pack) | only inside a .hydra pack |
| `collections/*.json` | authored | [record](#record) |  |
| `**/.gitkeep` | authored | none yet | keeps an empty folder |
| `.hydra/LICENSE-template.txt` | authored | none yet |  |
| `.hydra/rules/*.yaml` | authored (unspecified) | none yet | positions, hints, badges, archetypes, launchers, vocabularies, capacity, keys, standards, groups, kinship, wikidata, scope, geo: each file's header describes it |
| `.hydra/rules/defaults/*.yaml` | authored (unspecified) | none yet | the shipped defaults: positions, archetypes, domains, launchers |
| `.hydra/schema/wikidata/properties.yaml` | schema | [wikidata](#wikidata) | the Wikidata layer: which Wikidata property each field is (`_meta.wd`), and the fields with none; applied after ftm/ and extensions/ load, never read as types |
| `.hydra/schema/wikidata/classes.yaml` | schema | [wikidata](#wikidata) | the Wikidata layer: which Wikidata class (P31) each type is |
| `.hydra/schema/**` | schema | none yet | ftm/, extensions/ (artifact, collate, capacity, geo), params/<Type>.param.yaml, direction.yaml, wikidata/ (the Wikidata layer), and this spec in archive/ |
| `.hydra/sources/entries/*.json` | authored | [record](#record) |  |
| `.hydra/sources/files/**` | media | none yet | captured source text and files read by read_source |
| `.hydra/sources/citations.jsonl` | authored | [citation](#citation) |  |
| `.hydra/review/**/verdicts.yaml` | authored | [verdicts](#verdicts) |  |
| `.hydra/review/suggest-dismissed.yaml` | authored | none yet | which Review decisions the Suggestions box's Dismiss made, so its Reset undoes only those (hydra/suggest.py) |
| `.hydra/ui/favorites.json` | authored | none yet | the reader's favourite entities, in order (wiki/favorites.py); a preference, not a fact |
| `.hydra/ui/settings.json` | authored | none yet | the reader's interface choices for this archive: views, folds, filters, map base and layers, notification marks (wiki/uiprefs.py); a preference, not a fact |
| `.hydra/chats/*.jsonl` | authored | none yet | chat sessions attached to the archive (hydra/chatstore.py); one message a line |
| `.hydra/resources/layers/*.geojson` | authored | none yet | an archive layer on the Atlas: a GeoJSON FeatureCollection in lon/lat with its name (geo/layers.py) |
| `.hydra/resources/**` | media | none yet | icons, media and brand files that hints.yaml and wiki.yaml point at |
| `.hydra/tasks/*.md` | authored | [task](#task) |  |
| `.hydra/tasks/*.calls.jsonl` | authored | none yet | the MCP's call log for a task: one row per tool call its holder made, no source text |
| `.hydra/workflows/*.yaml` | authored | [workflow](#workflow) |  |
| `.hydra/contexts/*.yaml` | authored | none yet | an archive's own contexts: the brief a task runs under (hydra/contexts.py) |
| `.hydra/articles/*.md` | authored | [article](#article) |  |
| `.hydra/packages/lock.yaml` | authored | [packages-lock](#packages-lock) |  |
| `.hydra/enrich/*.jsonl` | authored | none yet | the enrichment ledger: what Enrich wrote into each entry (enrichlog.py) |
| `.hydra/mcp.yaml` | authored | none yet | which tools a hydra-mcp client sees in this archive, layered over the machine-wide mcp.yaml: toolsets, tools {on, off}, locked (hydra_mcp/config.py) |
| `.hydra/write.lock` | derived | none yet | runtime: names the process now writing; never kept, snapshotted or packed |
| `.hydra/history/snapshots/*.json` | derived | [snapshot](#snapshot) |  |
| `.hydra/history/**` | derived | none yet | objects/, refs/, HEAD: history.py's docstring |
| `.hydra/parsed/**` | derived | none yet |  |
| `.hydra/cache/**` | derived | none yet |  |
| `universe/universe.yaml` | authored | [universe](#universe) |  |
| `universe/canon.jsonl` | authored | [canon](#canon) |  |
| `universe/wiki.yaml` | authored | [wiki](#wiki) |  |
| `universe/review/verdicts.yaml` | authored | [verdicts](#verdicts) |  |
| `universe/collections/*.yaml` | authored | [universe-collection](#universe-collection) |  |
| `universe/members/*.hydra` | authored | none yet | an embedded member, itself a pack |
| `universe/backdrop/**` | authored (unspecified) | none yet | backdrop.yaml, themes/, archetypes.yaml, icons/, geo/: universe/backdrop.py's docstring |
| `universe/.parsed/**` | derived | none yet |  |

## hydra.yaml

`hydra.schema.yaml`

The archive manifest, at the archive's root. Written by `hydra-ctl init`, by `defaults`, by the Archive Configuration page and by hand. Read by every command; a key not named here is ignored by hydra and reported by `check` (archive.unknown-key).

| Key | Type | Meaning |
|---|---|---|
| `name` | string | The archive's display name (Archive Configuration writes it; `universe.yaml` title follows it). |
| `prefix` | string | The id prefix of the archive's collections when a collection names none (`<prefix>:<record id>`). Lowercase letters, digits, dot, dash and underscore; not one of the reserved source names. |
| `format` | integer | The archive format number: the one authoritative stamp. A hydra refuses an archive whose format is newer than its own. Format 3 stamps it here only (format 2 also wrote it into `collections/manifest.json` and `.hydra/parsed/build.yaml`). |
| `ftm` | string | SHA-256 of the vendored FollowTheMoney schema (`.hydra/schema/ftm`) the archive was made with. Stamped by `init` and by export; `check` compares it with the files (archive.ftm-changed). |
| `subject` | object | The charted subject (the org chart's root). |
| `subject.label` | string |  |
| `subject.type` | string |  |
| `search` | `all` or `no-text` or `names` | How far searches look. `all`; `no-text` (not notes, description...); `names` (names and ids). |
| `same_name` | `review` or `merge` | Two records with one exact name and nothing else in common: `review` (the default) asks, `merge` merges. A type's `<Type>.param.yaml` `same_name` wins over this key. |
| `history` | `true` or `false` or `on` or `off` | `on` (the default) takes a snapshot of the authored files after each command that writes them; `off` takes none. YAML reads a bare `on` as true and `off` as false; both forms are accepted. |
| `description` | string | A few lines about the archive, shown on the wiki's front page under the header. |
| `author` | string | The default author of history steps and saves (`$HYDRA_AUTHOR` wins over it). |
| `tasks` | object | Settings for agent tasks. |
| `tasks.stale_after` | string | How long a checked-out task may go without activity before its lock counts as stale and another session can take it over without `force` (default `2h`). A number and a unit: `30m`, `2h`, `1d`. |
| `defaults_off` | list of `generic` or `hierarchy` or `hints` | The shipped hierarchy defaults this archive switches off. Written by `hydra-ctl defaults`. |
| `collections` | object | Per-collection settings, by collection name (the file name without `.json`). |
| `collections.<name>` | object | One collection's settings. |
| `collections.<name>.title` | string | What every surface shows in place of the collection name. Absent: the name. |
| `collections.<name>.icon` | string | The collection's icon on the Collections page, an icon-library name (`tabler:folder`, `game:spell-book`). Absent: `tabler:folder`. |
| `collections.<name>.prefix` | string | The id prefix this collection's records get (format 2 kept it in `collections/manifest.json`). Absent: the archive's `prefix`, else one made from the collection's name. The list of collections the last build read, with each one's file, prefix and record count, is `.hydra/parsed/collections.json` (derived). |
| `collections.<name>.views` | object | The wiki views this collection has, by view. Each value is `true` (on, as the view's defaults have it), `false` (off), one spec, or a list of specs (several handles for one view). |
| `collections.<name>.views.org` | boolean or `viewSpec` or list of `viewSpec` |  |
| `collections.<name>.views.org.focus` | string | An H id or a record id; one that names no entity fails `view_check`. |
| `collections.<name>.views.org.depth` | integer |  |
| `collections.<name>.views.org.edges` | list of string | Relationship schemas to follow. |
| `collections.<name>.views.org.from` | integer or string | A year. |
| `collections.<name>.views.org.to` | integer or string | A year. |
| `collections.<name>.views.org.within` | `collection` or `universe` | `collection` (the default): only this collection or group; `universe`: everything. |
| `collections.<name>.views.org.title` | string | The handle's label. |
| `collections.<name>.views.org[]` | `viewSpec` |  |
| `collections.<name>.views.links` | `viewValue` |  |
| `collections.<name>.views.radial` | `viewValue` |  |
| `collections.<name>.views.map` | `viewValue` |  |
| `collections.<name>.views.timeline` | `viewValue` |  |
| `collections.<name>.views.graph` | `viewValue` |  |
| `collections.<name>.wiki` | see [wiki](#wiki) | This collection's pages' overrides of `wiki.yaml`, merged key by key over it. |
| `collection_groups` | object | Named sets of collections that views and the Collections page treat as one. |
| `collection_groups.<name>` | object |  |
| `collection_groups.<name>.title` | string |  |
| `collection_groups.<name>.collections` * | list of string |  |

\* required

## wiki.yaml

`wiki.schema.yaml`

How an archive's wiki looks and what a page holds. Read from the archive's root `wiki.yaml` (a member's default) and from `universe/wiki.yaml` (over every member's); a mapping merges key by key, anything else replaces. `hydra.yaml` `collections.<name>.wiki` overrides it again for one collection's pages. The Archive Configuration page writes `title` and `header_card` into `universe/wiki.yaml`; `hydra-ctl wiki define` writes `define` and `sections`.

| Key | Type | Meaning |
|---|---|---|
| `title` | string or object | The left rail's heading and the site's name. Text, or {text, sub} with a subtitle. |
| `title.text` | string |  |
| `title.sub` | string |  |
| `rail_image` | object | How the left rail's image is drawn, a `square` (default) or a `circle` mask over the same square crop. |
| `rail_image.shape` | `square` or `circle` |  |
| `title_style` | object | How the left rail's title is set in type. Only keys that differ from the defaults are written; the theme still sets the colour. |
| `title_style.font` | `theme` or `georgia` or `serif` or `sans` or `mono` or `palatino` or `garamond` or `optima` or `futura` | The typeface: theme (default, the theme's heading font), georgia, serif, sans, mono, palatino, garamond, optima or futura. |
| `title_style.size` | number | Size in rem, from 1.0 to 2.2 (default 1.55). |
| `title_style.weight` | `300` or `400` or `600` or `700` | Weight: 300, 400 (default), 600 or 700. |
| `title_style.tracking` | number | Letter spacing in em, from -0.02 to 0.2 (default 0.012). |
| `title_style.case` | `normal` or `upper` or `smallcaps` | `normal` (as written, default), `upper` or `smallcaps`. |
| `title_style.align` | `left` or `center` | `center` (default, under a square image) or `left`. |
| `about` | string | One sentence for the front page. |
| `view` | `wiki` or `geo` or `radial` or `org` or `messaging` or `agentic` or `blank` | The view a project opens at. |
| `layout` | `float` or `column` | `float` (default): the infobox floats beside the text; `column`: it keeps a column of its own. |
| `flags` | `circle` or `rect` or `square` or `none` | The flag drawn beside a country. |
| `navboxes` | boolean | The boxes of related entries at the foot of a page (on by default). |
| `landing` | list of string | The main page's sections, in order. Known: domains, featured, current, decades, recent, attention, added, deals, groups, explore, people, years_ago, in_office. |
| `chips` | list of string | Which labels sit under a page's title, in order (a provider name each). |
| `sections` | object | Per page type (or a parent type), the sections a page gets, in order. A section is a built-in name or one from `define`. |
| `sections.<name>` | list of string |  |
| `panel` | list of object | An entry's views and their buttons, in order. |
| `panel[]` | object |  |
| `panel[].label` * | string |  |
| `panel[].icon` | string |  |
| `panel[].sections` * | list of string |  |
| `panel[].titles` | object | Section to the button's label when that section is the first one it holds. |
| `panel[].titles.<name>` | string |  |
| `define` | object | Sections of your own, by name (`hydra-ctl wiki define` writes them). |
| `define.<name>` | object | A section of your own. |
| `define.<name>.title` | string |  |
| `define.<name>.relations` | object |  |
| `define.<name>.relations.edge` * | string | A role (`person`, `post`, `event`, `tenure`, `kin`, `ownership`, `representation`) or a relationship name. |
| `define.<name>.relations.side` | `source` or `target` |  |
| `define.<name>.relations.verb` | string or array |  |
| `define.<name>.relations.other` | string | Only relationships whose other end is this type or one that extends it. |
| `define.<name>.relations.former` | boolean |  |
| `define.<name>.columns` | list of string or object | `name`, `verb`, `share`, `status`, `period`, `date`, `deal`, `thumb`, `badges`; `{label, column}` or `{label, prop}`. |
| `define.<name>.columns[]` | string or object |  |
| `define.<name>.columns[].label` | string |  |
| `define.<name>.columns[].column` | string |  |
| `define.<name>.columns[].prop` | string |  |
| `define.<name>.sort` | list of string |  |
| `define.<name>.view` | `table` or `list` or `timeline` |  |
| `define.<name>.min` | integer |  |
| `define.<name>.props` | string or array | Instead of `relations`: a table of this page's own properties. |
| `lead` | object | A page's opening sentence, per schema (or parent schema); a template with `{slot}` and `[optional part]`; `false` writes none. |
| `lead.<name>` | string or `False` |  |
| `roles` | object | Which schema plays each role the built-in sections look for (`person`, `post`, ...). |
| `roles.<name>` | string |  |
| `field_labels` | object | The heading in "Mentioned in", by the field that names the page. |
| `field_labels.<name>` | string |  |
| `edge_labels` | object | The heading a relationship's list gets, by relationship and by which end the page is. |
| `edge_labels.<name>` | object |  |
| `edge_labels.<name>.source` | string |  |
| `edge_labels.<name>.target` | string |  |
| `icons` | object | Page type to an icon file name under `.hydra/resources/icons/` (letters, digits, `-`). |
| `icons.<name>` | string |  |
| `badges` | object | How a hint badge token is worded; `null` hides it. |
| `badges.<name>` | string or null |  |
| `badge_rules` | object | Derived-badge rules, by badge key; layered over hydra's and the archive's `.hydra/rules/badges.yaml`. `null` drops a rule; a rule naming an existing key changes only what it says. |
| `badge_rules.<name>` | null or `badgeRule` |  |
| `badge_rules.<name>.label` | string |  |
| `badge_rules.<name>.short` | string |  |
| `badge_rules.<name>.group` | `role` or `service` or `industry` |  |
| `badge_rules.<name>.icon` | string |  |
| `badge_rules.<name>.tip` | string |  |
| `badge_rules.<name>.title` | string | A regular expression over a post's title (write it in single quotes). |
| `badge_rules.<name>.ongoing` | boolean |  |
| `badge_rules.<name>.when` | list of object | Conditions, any one of which fires the badge (see `wiki/badges.py`). |
| `badge_rules.<name>.except` | list of object | Conditions, none of which may hold. |
| `derived_badges` | boolean or object | `false` switches derived badges off; `{max: N}` caps how many a page shows (default 8). |
| `derived_badges.max` | integer |  |
| `link_colours` | object | Relationship family to a colour, as the Symbology page sets them. |
| `link_colours.<name>` | string |  |
| `timeline_marks` | object | Relationship type to what the Timeline draws when a link has a start and no end, as the Symbology page sets them: start (a diamond at the start), fades (a post's bar fading out, with a ? cap) or runs (a bar to today). Unset types: posts fade, others are a start mark (wiki/timelineview.py). |
| `timeline_marks.<name>` | `start` or `fades` or `runs` |  |
| `identifiers` | object | How an `upstream: <namespace>:<key>` value names the outside site; the url takes `{id}`. `null` drops a built-in. |
| `identifiers.<name>` | null or object |  |
| `identifiers.<name>.label` * | string |  |
| `identifiers.<name>.url` * | string |  |
| `theme` | object | The wiki's look, over a theme's own colours. |
| `theme.base` | string | A built-in (shore, dune, tide, tan, light), a theme file's or a VS Code theme's name. |
| `theme.fonts` | object |  |
| `theme.fonts.heading` | string |  |
| `theme.fonts.body` | string |  |
| `theme.radius` | string |  |
| `theme.light` | object | Any colour variable of the theme (bg, ink, muted, line, soft, panel, head, headink, link, accent...). |
| `theme.light.<name>` | string |  |
| `theme.dark` | object |  |
| `theme.dark.<name>` | string |  |
| `radial` | object | What the Radial view's filters start with. |
| `radial.hide` | list of string |  |
| `radial.hide_links` | list of string |  |
| `radial.hub` | integer |  |
| `radial.depth` | `1` or `2` or `3` |  |
| `map` | object | The Atlas. |
| `map.national` | list of string | Entry types whose country alone is worth drawing (schema or its label). |
| `map.hide` | list of string | Entry types switched off at first. |
| `map.lang` | string | The basemap's label language. |
| `header_card` | object | The front page's header image (Archive Configuration writes it; the file is in `.hydra/resources/brand/`). |
| `header_card.file` * | string | The file name in `.hydra/resources/brand/` (`header-card.<ext>`). |
| `header_card.focus` | list of number | The focal point, x and y as percentages. |
| `header_card.title_over` | boolean | Whether the title is drawn over the image. |

\* required

## A collection record

`record.schema.yaml`

One record of `collections/<name>.json` or `.hydra/sources/entries/<name>.json` (the files are a JSON array when saved by hydra, JSON lines when imported; both are read, and written back in the form read). A record is the three keys `id`, `schema` and `properties`, in FollowTheMoney's shape, plus the one envelope extension `_meta`. Nothing else may sit beside them. Images and badges are never record fields: a record does not name its own picture; they are linked by rule in `.hydra/rules/hints.yaml` (`thumb`, `portrait`, `logo`, `badge`).

| Key | Type | Meaning |
|---|---|---|
| `id` * | string | The record id, unique in the archive once prefixed (`<collection prefix>:<id>`). |
| `schema` * | string | A schema name from `.hydra/schema` (`Person`, `Organization`, `GeoLink`...). |
| `properties` * | object | Property name to a list of text values. FtM stores every value as text, dates as ISO prefixes. |
| `properties.<name>` | list of string |  |
| `_meta` | object | Qualifiers hydra keeps beside the record without breaking an FtM export. |
| `_meta.approx` | object | A date property's qualifier: a source's "c. 1748" keeps `1748` in the property and `circa` here. EDTF-aligned: circa `1748~`, before `[..1800]`, after `[1900..]`, decade `195X`, uncertain `1748?`. |
| `_meta.approx.<name>` | `circa` or `before` or `after` or `decade` or `uncertain` |  |
| `_meta.basis` | object | What a field's value rests on when it is not (only) a kept source's statement, `{field: state}`: chosen in Labels and never shown. Wikidata's P5102 "nature of statement" is the same idea. |
| `_meta.basis.<name>` | `sourceless` or `assumed` or `inferred` or `reported` or `recalled` or `estimated` or `disputed` |  |
| `_meta.cites` | list of string | The ids of the kept sources a relationship record cites. FtM gives a relationship (Ownership, Family...) no `sources`, so a save moves their URLs into `sourceUrl` and keeps the ids here while the batch is checked; the record is written without it (`storable`), so a file holds it only if something wrote it otherwise. |
| `_meta.extra` | object | Values for properties the record's type does not have, `{field: {values, wd}}`: kept, never dropped, until they are assigned to a field, to a property of the archive's own, or dropped. `field` is the name the values came under, or the label of their Wikidata code when they came under a code (`P1449`). |
| `_meta.extra.<name>` | object | One field the type lacks, with its values and their code. |
| `_meta.extra.<name>.values` * | list of string | The values, as text. |
| `_meta.extra.<name>.wd` | string or null | The Wikidata property the values came under or were marked with; null when none is known. |
| `_meta.wd` | object | The Wikidata property behind a field, `{field: P-code}`; written by the Wikidata import and by labelling. |
| `_meta.wd.<name>` | string |  |

\* required

Renames read on import: `proof` is read as `sources`. Names an importer reads as hydra's, so an export writes them back (FTM_RENAMES in ingest.py). `Family`'s `person`, `relative` and `relationship` are FtM's own names and are not renamed.

Keys an import accepts and does not keep as record fields: `entities` wraps a list; `referents` is a list of ids an upstream tool merged into the record (read for identity as `_referents`, never written back); `statements` (per-value provenance) and `{entity, composed, statements}` (FtM entity_sources) are folded into a record.

## A citation row

`citation.schema.yaml`

One line of `.hydra/sources/citations.jsonl`: where in a source a record's facts are. One row per record and source; the latest row for a pair wins; a row with every detail blank removes the pair's row. A call number that belongs to the whole document is its own field, `accessNumber`, on the source's record, not here.

| Key | Type | Meaning |
|---|---|---|
| `record` * | string | A record of the last build, `<prefix>:<id>`. |
| `source` * | string | A source document, `<prefix>:<id>` (a record under `.hydra/sources/entries/`, or any Document the build holds). |
| `pages` | string | Pages, as the source prints them on the document (`14`, `14-15`, `iv`, `I-16`). 80 characters at most. A PDF's printed numbers are not its page count: see `pdfPages`. |
| `pdfPages` | string | Pages of the document as a file, counted from its first page (`20`, `20-21`): the page a PDF viewer shows. The Pollard report's PDF page 20 prints "1"; PDF page 126 prints "I-16". Either of `pages` and `pdfPages` may be left out. 80 characters at most. |
| `locator` | string | A call number, folio, box, paragraph or timestamp. 200 characters at most. |
| `quote` | string | The words quoted, as `read_source` returned them. 2000 characters at most. |

\* required

## Verdicts (the decision grammar)

`verdicts.schema.yaml`

A `verdicts.yaml`: one flat mapping of decisions, `<kind>-<subject>: <value>`. Written by `answer`, `review`, the Review page and the Suggestions box; read on every build. Every `verdicts.yaml` under `.hydra/review/` at any depth is read, and so is `universe/review/verdicts.yaml` (the universe's pins). Two files that disagree about one decision: `rejected` wins.

| Kind | Key | Value | Meaning | |---|---|---|---| | `merge` | `merge-<16 hex>` | `confirmed` or `rejected`, or `{status, basis}` | two records are, or are not, one entity | | `place` | `place-<16 hex>` | as `merge` | a record is, or is not, placed under another | | `ref` | `ref-<16 hex>` | a record id, or `none` | what an ambiguous or unresolved reference means | | `cap` | `cap-<record id>` (archive) or `cap-H-<body>` (universe) | one of the entity's names | the caption shown | | `stub` | `stub-<slug>` | a schema name | a name no record has becomes one entity | | `geo` | `geo-H-<body>` | comma list of location ids, or `auto` | the primary geometry a person chose | | `loc` | `loc-<id>` | a Place H, a candidate number or `none` | what an unresolved place name means (draft) | | `site` | `site-<id>` | `confirmed` or `rejected` | a proposed GeoLink (draft) | | `wd` | `wd-H-<body>` | a Wikidata item `Q<digits>` or `none` | which item is this entry (draft) | | `arch` | `arch-H-<body>` | `{<archetype id>: yes or no}` | whether an entry is of an archetype (lives in `universe/review/verdicts.yaml`; format 2 kept it in `universe/review/archetypes.yaml`, which `hydra-ctl upgrade` folds in) | | `sug` | `sug-<body>.<id>` | `rejected` | a suggestion the person turned down | | `end` | `end-<relationship record id>` | `{end: YYYY[-MM[-DD]], basis: <kind>:<id>}`, `{state: holds}` or `{state: unknown}` | where an Occupancy, Employment or Membership with a start and no end stopped: a judgement, built as an inferred end, never as a stated `endDate` |

`basis` is a fingerprint of the evidence at the time of the decision: a confirmation whose basis no longer matches lapses to `confirmed-stale` (asked again, not applied); a rejection stays applied and is marked stale.

| Key | Type | Meaning |
|---|---|---|
| `^(merge|place)-[0-9a-f]{16}$` | `confirmed` or `rejected` or object |  |
| `^(merge|place)-[0-9a-f]{16}$`.status * | `confirmed` or `rejected` |  |
| `^(merge|place)-[0-9a-f]{16}$`.basis | string |  |
| `^ref-[0-9a-f]{16}$` | string |  |
| `^cap-.+$` | string |  |
| `^stub-.+$` | string |  |
| `^geo-H-[0-9a-hjkmnp-tv-z]{12}$` | string |  |
| `^loc-.+$` | string |  |
| `^site-.+$` | `status` |  |
| `^wd-H-[0-9a-hjkmnp-tv-z]{12}$` | string |  |
| `^arch-H-[0-9a-hjkmnp-tv-z]{12}$` | object |  |
| `^arch-H-[0-9a-hjkmnp-tv-z]{12}$`.<name> | `yes` or `no` |  |
| `^sug-[0-9a-hjkmnp-tv-z]{12}\..+$` | `rejected` |  |
| `^end-.+$` | object or object |  |
| `^end-.+$`.end * | string |  |
| `^end-.+$`.basis * | string |  |
| `^end-.+$`.state * | `holds` or `unknown` |  |

\* required

## A task file's front matter

`task.schema.yaml`

`.hydra/tasks/<id>.md`: Markdown with YAML front matter (the schema below), then one `## <block title>` section per block of the workflow with a checkbox line per step, then `## Log`. The checkbox lines are `- [ ] <code> <text>` with `[ ]` open, `[x]` done, `[!]` blocked, `[-]` skipped, and ` => <result>` after the text. Keys beyond these are not part of the format.

| Key | Type | Meaning |
|---|---|---|
| `id` * | string | `tsk-` and ten Crockford base32 characters. |
| `title` * | string |  |
| `workflow` * | string | A workflow name (built in, or one of `.hydra/workflows/`). |
| `context` | string or null | The context the task runs under (built in, or one of `.hydra/contexts/`); fixed at the first write. |
| `route` | list of string | The workflows the task runs, in order; `workflow` is the first. Step codes of a route of several carry their position (`2.A1`). |
| `model` | string or null | The model of the latest holder. |
| `client` | string or null | The client of the latest holder. |
| `collection` | string or null |  |
| `views` | list of string | The wiki views the task adds blocks for. |
| `guides` | list of string | Guides the task's agent reads. |
| `authorized` | list of string | MCP tools the person has let the agent confirm without asking again. |
| `status` * | `open` or `checked-out` or `blocked` or `done` |  |
| `holder` | string or null | Who has the task checked out. |
| `since` | string or null |  |
| `last_activity` | string or null | The last step, added step or logged write by the holder; the task is stale when this is older than `tasks.stale_after`. |
| `closed_by` | string or null |  |
| `closed_at` | string or null |  |
| `start_snapshot` | string or null | The history snapshot when the task was checked out. |
| `end_snapshot` | string or null |  |
| `sources` | list of string | Sources the task recorded. |
| `claims` | list of object |  |
| `claims[]` | object |  |
| `claims[].step` * | string |  |
| `claims[].section` | string |  |
| `claims[].claim` * | string |  |
| `claims[].evidence` | list of string |  |
| `claims[].by` | string |  |
| `claims[].at` | string |  |

\* required

## A workflow

`workflow.schema.yaml`

`.hydra/workflows/<name>.yaml`: an archive's own workflow, or one overriding a built-in of the same `name`. The step list a task starts from, and the guide it renders as. Built-ins live in hydra's `workflows/*.yaml` and have the same shape.

| Key | Type | Meaning |
|---|---|---|
| `name` * | string |  |
| `title` | string |  |
| `use_when` | string |  |
| `guides` | list of string | Guide topics the task's agent reads first. |
| `authorize` | list of string | MCP tools a task may be created with permission to confirm. |
| `notes` | string |  |
| `blocks` * | object | Blocks of steps, by code, in order. |
| `blocks.<name>` | object |  |
| `blocks.<name>.title` | string | `{subject}` is replaced in a `repeat: subject` block. |
| `blocks.<name>.repeat` | `subject` | `subject`: the block is made once per subject the task names. |
| `blocks.<name>.steps` | list of `step` |  |
| `blocks.<name>.steps[]` | list of string or object |  |
| `blocks.<name>.steps[].code` * | string |  |
| `blocks.<name>.steps[].text` * | string | The checkbox line. |
| `blocks.<name>.steps[].tool` | string |  |
| `blocks.<name>.steps[].do` | string | What the agent does. |
| `blocks.<name>.steps[].done` | string | What is true when the step is done. |
| `blocks.<name>.steps[].stop` | string | When to stop and tell the person. |
| `blocks.<name>.steps[].verify` | string | A check that must pass before the step can be ticked (`view_check:org`, `geo_clean`). |
| `blocks.<name>.steps[].guide` | string |  |
| `view_blocks` | object | Per wiki view, a block that replaces hydra's own for that view. |
| `view_blocks.<name>` | object |  |
| `view_blocks.<name>.code` | string |  |
| `view_blocks.<name>.title` | string |  |
| `view_blocks.<name>.guide` | string |  |
| `view_blocks.<name>.steps` | list of `step` |  |
| `view_blocks.<name>.steps[]` | `step` |  |

\* required

## A history snapshot

`snapshot.schema.yaml`

`.hydra/history/snapshots/<id>.json`: the authored files at one moment, by SHA-256 (the files themselves are zlib-compressed in `objects/`). History tracks `hydra.yaml`, `wiki.yaml`, `collections/`, `.hydra/` and `universe/`, minus `.hydra/parsed/`, `cache/`, `history/`, `schema/ftm/` and `universe/.parsed/`. Snapshots are never rewritten; `restore` and `merge` add on top. The one exception is `squash`, asked for by name, which writes a snapshot with `squashed` set.

Two kinds. A *step* (`auto: true`, no `kind`) is the undo journal: every writing command takes one. A *save* (`kind: save`) is a change a person or agent names, with `fields` describing every step since the last save; the steps fold under it. `signature`, when present, is a detached signature over the save's canonical JSON (keys sorted, no spaces, `signature` and `id` removed), made with `gpg --detach-sign --armor` or `ssh-keygen -Y sign -n hydra`.

| Key | Type | Meaning |
|---|---|---|
| `parents` * | list of string | Parent snapshot ids (two for a merge, none for the first). |
| `files` * | object | Archive-relative path to the SHA-256 of its content. |
| `files.<name>` | string |  |
| `message` * | string |  |
| `author` * | string |  |
| `auto` | boolean | `true` for a step. |
| `time` * | string | ISO 8601, UTC. |
| `kind` | `save` | `save` for a save; absent for a step. |
| `squashed` | integer | How many snapshots this one replaced. |
| `fields` | object | What a save covers (only on `kind: save`). |
| `fields.message` * | string |  |
| `fields.description` | string |  |
| `fields.entities` | list of object | Records added, changed or removed since the last save. |
| `fields.entities[]` | object |  |
| `fields.entities[].collection` | string |  |
| `fields.entities[].path` | string |  |
| `fields.entities[].id` * | string |  |
| `fields.entities[].name` | string |  |
| `fields.entities[].change` * | `added` or `changed` or `removed` |  |
| `fields.sources` | list of string | Source record ids added. |
| `fields.packages` | list of string or object | Packages installed since the last save (name and version). |
| `fields.author` | string |  |
| `signature` | object | A detached signature over the save's canonical JSON. |
| `signature.method` * | `gpg` or `ssh` |  |
| `signature.key` | string | The gpg key id, or the ssh key path. |
| `signature.sig` * | string | The armoured signature. |

\* required

## universe.yaml

`universe.schema.yaml`

`universe/universe.yaml`: the universe layer's manifest. A universe is a second layer beside the archive's own; its members are where records come from. Every member is read only, compiled in memory with the archive build, so its own merges, rejections and caption pins hold. A record is named across the universe as `<member>/<record id>`.

| Key | Type | Meaning |
|---|---|---|
| `title` | string | The universe's name (Archive Configuration keeps it equal to `hydra.yaml` name). |
| `uid` | string | Eight Crockford base32 characters, minted once. H ids derive from it, so two copies of a universe derive the same H for the same cluster. |
| `members` * | object | Members by name. `self` is this folder's own archive layer. |
| `members.<name>` | object |  |
| `members.<name>.pack` | string | An embedded member, relative to `universe/` (`members/<name>.hydra`). |
| `members.<name>.path` | string | A linked member, relative to `universe/`. |
| `members.<name>.sha256` | string | The linked member's bytes, pinned. |

\* required

## A canon row (the H-table)

`canon.schema.yaml`

One line of `universe/canon.jsonl`: the universe's promises. One row per H that something depends on; an H nobody has published or decided has no row (state `c`, derived again by every build). Only review and publishing write it, and a state only moves forward (`c` to `p` to `d`). An H is `H-<state><flags>-<body>`: the body is 12 Crockford base32 characters derived from the universe uid and the anchor record; the flags digit is always 0 here (builds compute flags and never write them back).

| Key | Type | Meaning |
|---|---|---|
| `h` * | string |  |
| `anchor` | string | The record ref the body was derived from, `<member>/<record id>`. |
| `members` | list of string | Record refs when the row was written (its basis). |
| `not` | list of string | Bodies this H must never merge with. |
| `redirect` | string | The body this H was merged into (written by review). |
| `title` | string | Its title when written (a tombstone keeps it). |
| `seq` | integer |  |
| `published` | string | The date it became `p`. |
| `decided` | string | The date it became `d`. |
| `by` | string | Who wrote the row. |
| `source` | string | On what evidence (pins). |

\* required

## universe/collections/<slug>.yaml

`universe-collection.schema.yaml`

A curated list of entries in the universe, by H.

| Key | Type | Meaning |
|---|---|---|
| `title` | string |  |
| `members` * | list of string |  |

\* required

## An article's front matter

`article.schema.yaml`

`.hydra/articles/<H body>.md` (format 3, design D11): an entry's prose, kept apart from its records and keyed by the H body so it survives merges. YAML front matter lists the sections; each section's Markdown follows under a marker line `<!-- section <id> -->`. A section with `from` and no `forked` arrived from outside and cannot be edited; editing forks it (it becomes the archive's own text, keeping `from` and the licence). Citations in prose are `[^source-id p.23]`.

| Key | Type | Meaning |
|---|---|---|
| `sections` * | list of object |  |
| `sections[]` | object |  |
| `sections[].id` * | string | Unique in the article; the marker line names it. |
| `sections[].heading` * | string |  |
| `sections[].from` | string | Where an imported section came from: `enwiki:<Title>@<revision id>`. |
| `sections[].licence` | string | The licence an imported section carries (CC BY-SA 4.0 for Wikipedia). |
| `sections[].forked` | boolean | An imported section the archive edited: now its own text, provenance kept. |

\* required

## .hydra/packages/lock.yaml

`packages-lock.schema.yaml`

What an archive uses from installed packages (format 3, design D12), like a lock file: the same archive on another machine resolves the same bytes (`hydra-ctl package sync`). Order matters: a lookup of icons, themes, archetypes and rules takes the first package in lock order that has the file. Removing a package never touches records.

| Key | Type | Meaning |
|---|---|---|
| `packages` * | list of object |  |
| `packages[]` | object |  |
| `packages[].name` * | string |  |
| `packages[].version` * | string |  |
| `packages[].sha256` * | string | The SHA-256 of the package's manifest (which holds every file's hash). |
| `packages[].scope` * | `machine` or `universe` | `machine`: the machine's shared store; `universe`: this universe's backdrop. |

\* required

## hydra-package.yaml

`package.schema.yaml`

A package (format 3, design D12): the standard universe hydra ships and anything people share, in one format. A package is a folder (or a `.hydrapkg` zip of it) holding this manifest and the files it provides. It is installed into a content-addressed store, never overwritten. The manifest's hash, which covers every file's hash, is the package's identity.

| Key | Type | Meaning |
|---|---|---|
| `name` * | string | `owner/name`, lowercase letters, digits and `-`. |
| `version` * | string | Quote it, so YAML keeps `2026.11.0` text. |
| `description` | string |  |
| `licence` * | list of string | One or more licence names. |
| `attribution` | string |  |
| `depends` | list of string |  |
| `provides` * | object |  |
| `provides.geo` | list of object |  |
| `provides.geo[]` | object |  |
| `provides.geo[].layer` * | string |  |
| `provides.geo[].file` * | string | A relative path inside the package (no leading slash, no `..`, no backslash). |
| `provides.geo[].critical` | boolean | What the Atlas needs to draw at all; the rest install on demand. |
| `provides.symbology` | object |  |
| `provides.symbology.icons` | `path` |  |
| `provides.symbology.badges` | `path` |  |
| `provides.symbology.hints` | `path` |  |
| `provides.archetypes` | `path` |  |
| `provides.timeline` | `path` | A Timeline kit, how the Timeline draws kinds of fact, classes of event and posts (wiki/timelinekit.py). |
| `provides.themes` | list of `path` |  |
| `provides.themes[]` | `path` |  |
| `files` | object | Every file of the package, path to `sha256:<hex>`. |
| `files.<name>` | string |  |

\* required

## hydra-pack.json

`pack.schema.yaml`

The index inside a `.hydra` file (a zip of an archive; `hydra-ctl pack`). Pack format 1 is independent of the archive format: a hydra unpacks any pack whose format it reads and refuses one whose file hashes differ. The same archive always packs to the same bytes (sorted entries, fixed timestamps). Backups, `__pycache__`, activation markers and symbolic links never go in; neither does a file that looks like a secret (`*.pem`, `*.key`, `id_rsa*`, `id_ed25519*`, `.env`, `.env.*`, `secrets.*`, `*.p12`, `*.pfx`, `credentials.json`): `pack` and history snapshots refuse it by name. A secret never sits in an archive, a pack, history or an export.

| Key | Type | Meaning |
|---|---|---|
| `format` * | `1` | The pack format; 1. |
| `name` * | string |  |
| `parsed` * | boolean | Whether the last build (`.hydra/parsed/`, `universe/.parsed/`) is in the pack. |
| `files` * | object | Every file in the pack, path to the SHA-256 of its content. |
| `files.<name>` | string |  |
| `history` | `True` | `true` when `.hydra/history/` is kept (absent otherwise). |
| `layers` | list of `archive` or `universe` | Present only with a universe layer. |
| `members` | object | Present only with a universe layer. Each embedded member (`universe/members/<name>.hydra`), name to SHA-256. |
| `members.<name>` | string |  |

\* required

## The Wikidata layer

`wikidata.schema.yaml`

One file of `.hydra/schema/wikidata/` (published as `schema/wikidata/`): which Wikidata property each field is (`properties.yaml`) and which Wikidata class each type is (`classes.yaml`). The layer sits beside FollowTheMoney (`ftm/`) and hydra's extensions (`extensions/`), never inside them, and is applied after they load: every key must name a type and field of the loaded model (a parent type's field counts, and `GeoLink.<role>` a role of `.hydra/rules/geo.yaml`); one that does not is an error in the layer, never a change to the model. An archive's own copy replaces the one hydra ships, and the archive's `.hydra/rules/wikidata.yaml` (the import map) is laid on top.

| Key | Type | Meaning |
|---|---|---|
| `properties` | object | `Schema.field` or a bare `field` to its Wikidata property code: the code every claim hydra writes carries in the record's `_meta.wd`. `Schema.field` wins over the bare field; a bare field must be a field of some type. |
| `properties.<name>` | string |  |
| `none` | list of `key` | Fields that have no Wikidata property, keyed as in `properties`, so "not mapped yet" and "no such property" differ. A key is never in both. |
| `none[]` | string | `Schema.field`, `GeoLink.<role>` or a bare `field`. |
| `classes` | object | A Wikidata class (P31, instance of) to the type an item of that class is made as. |
| `classes.<name>` | string |  |

\* required
