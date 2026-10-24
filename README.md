**English** | [Polski](README.pl.md) | [Deutsch](README.de.md)

# VORO Tree Standard QA

[![tests](https://github.com/MR73BIIO/voro-tree-standard-qa/actions/workflows/tests.yml/badge.svg)](https://github.com/MR73BIIO/voro-tree-standard-qa/actions/workflows/tests.yml)
![python](https://img.shields.io/badge/python-3.10%2B-2f6b4a)
![license](https://img.shields.io/badge/license-GPL--2.0--or--later-2f6b4a)
![rules](https://img.shields.io/badge/rule%20pack-Warsaw%20688%2F2025-2f6b4a)

**Checks tree inventory data against the client's standard before acceptance, and shows every problem on the map.**

![Findings on the synthetic sample](docs/findings_map.png)

A tree inventory is handed over as a GeoPackage and usually checked by eye. This tool turns the client's standard into rules that run the same way every time: same data, same result, with a reference to the exact section. The first rule pack is the City of Warsaw *Standard for tree inspections and dendrological analyses* (Order 688/2025).

Web page (calculator and table check, PL/DE/EN): https://mr73biio.github.io/voro-tree-standard-qa/

## What it checks

10 rules, details in [rules/warszawa_688/RULES.md](rules/warszawa_688/RULES.md):

- risk class 1–3 (old 5-level scale flagged),
- site use category O/N/S/W where the Standard requires it, and not where it doesn't,
- next inspection date against the interval matrix in Annex 7,
- geometry type against the class (class 1 as an area, classes 2 and 3 as points),
- missing or duplicate inventory numbers, broken dates, girth ≤ 60 cm.

Every finding has a severity (error, warning, note), a message in Polish, German and English, and a reference to the Standard.

## Quick start

```bash
git clone https://github.com/MR73BIIO/voro-tree-standard-qa.git
cd voro-tree-standard-qa
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
python tools/make_sample.py
vtsqa data/sample/rembertow_syntetyczne.gpkg --lang en
```

Output: `rembertow_syntetyczne_findings.gpkg` (layer `findings`) and a report `rembertow_syntetyczne_findings.en.md`.

Result on the synthetic sample: 30 trees, 7 errors, 3 warnings, 1 note. All 11 deliberately inserted errors are found, with no false alarms.

### As a quality gate

```bash
vtsqa delivery.gpkg --fail-on blad
```

Exit code 1 when there is at least one error, so the check can stop a pipeline before the data goes out.

## In QGIS

1. Add the layer `drzewa` from `data/sample/rembertow_syntetyczne.gpkg`.
2. Add the layer `findings` from the output file.
3. On `findings`: Properties → Symbology → Style → Load Style → `qgis/findings.qml`.

Red circles are errors, yellow triangles warnings, blue squares notes. Hovering a point shows the message in PL, DE and EN and the section of the Standard.

## Sample data

`data/sample/rembertow_syntetyczne.gpkg` is **synthetic**: 30 trees placed in the area of Grawerska Street in Rembertów, invented attributes, 11 deliberate errors. It is not City of Warsaw data. Every record has `zrodlo = SYNTETYCZNE`. The public data check is documented in [rules/warszawa_688/R0.md](rules/warszawa_688/R0.md).

## What it does not do

It does not assess tree condition and does not replace an arborist. It checks whether the records follow the Standard's rules.

## Status

Version 0.1.0. Next steps and exit criteria: [ROADMAP.md](ROADMAP.md). Changes: [CHANGELOG.md](CHANGELOG.md).

## Licence

Code: GPL-2.0-or-later ([LICENSE](LICENSE)). Sample data, rule descriptions, QGIS style and docs: CC BY 4.0 ([LICENSE-DATA.md](LICENSE-DATA.md)). How to cite: [CITATION.cff](CITATION.cff).

---

Marcin Ruszczak (MR73BIIO) · ORCID [0009-0004-0170-4277](https://orcid.org/0009-0004-0170-4277) · Polish · German · Russian · English
