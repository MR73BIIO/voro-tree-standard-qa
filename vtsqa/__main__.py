"""Uruchomienie: vtsqa WEJSCIE.gpkg [--layer NAZWA] [--out WYNIK.gpkg] [--lang pl|de|en] [--fail-on blad|ostrzezenie]

Zapisuje warstwę znalezisk `findings` (punkty) do pliku GeoPackage i raport Markdown obok niego.
Z --fail-on kończy się kodem 1, gdy są znaleziska o tej wadze lub poważniejsze (bramka jakości).
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

import geopandas as gpd
import pyogrio

from . import __version__
from .engine import REQUIRED_FIELDS, SEVERITY_ORDER, check_records, _txt

SEV_LABEL = {
    "pl": {"blad": "błąd", "ostrzezenie": "ostrzeżenie", "informacja": "informacja"},
    "de": {"blad": "Fehler", "ostrzezenie": "Warnung", "informacja": "Hinweis"},
    "en": {"blad": "error", "ostrzezenie": "warning", "informacja": "note"},
}
TXT = {
    "pl": {"title": "Raport kontroli danych drzew — Standard 688/2025", "src": "Plik", "rec": "Rekordów",
           "sum": "Podsumowanie", "list": "Znaleziska", "none": "Brak znalezisk.",
           "cols": "| Nr | Reguła | Waga | Komunikat | Standard |"},
    "de": {"title": "Prüfbericht Baumdaten — Standard 688/2025", "src": "Datei", "rec": "Datensätze",
           "sum": "Zusammenfassung", "list": "Befunde", "none": "Keine Befunde.",
           "cols": "| Nr. | Regel | Gewicht | Meldung | Standard |"},
    "en": {"title": "Tree data check report — Standard 688/2025", "src": "File", "rec": "Records",
           "sum": "Summary", "list": "Findings", "none": "No findings.",
           "cols": "| No. | Rule | Severity | Message | Standard |"},
}


def run(path: Path, layer: str | None, out: Path, lang: str, fail_on: str | None = None) -> int:
    layers = [name for name, _ in pyogrio.list_layers(path)]
    layer = layer or layers[0]
    gdf = gpd.read_file(path, layer=layer)
    missing = [f for f in REQUIRED_FIELDS if f not in gdf.columns]
    if missing:
        print(f"Brak pól / fehlende Felder / missing fields: {', '.join(missing)}", file=sys.stderr)
        return 2

    records, gtypes, points = [], [], {}
    for i, row in gdf.iterrows():
        rec = {k: row.get(k) for k in gdf.columns if k != "geometry"}
        rec["_row"] = i + 1
        records.append(rec)
        geom = row.geometry
        gtypes.append(geom.geom_type if geom is not None else None)
        key = _txt(rec.get("nr")) or f"#{i + 1}"
        if geom is not None and key not in points:
            points[key] = geom.representative_point()

    findings = check_records(records, gtypes)
    rows = [{
        "nr": f.nr, "regula": f.rule, "waga": f.severity,
        "msg_pl": f.msg["pl"], "msg_de": f.msg["de"], "msg_en": f.msg["en"],
        "standard": f.ref, "geometry": points.get(f.nr),
    } for f in findings]
    fgdf = gpd.GeoDataFrame(rows, geometry="geometry", crs=gdf.crs) if rows else gpd.GeoDataFrame(
        columns=["nr", "regula", "waga", "msg_pl", "msg_de", "msg_en", "standard", "geometry"],
        geometry="geometry", crs=gdf.crs)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    fgdf.to_file(out, layer="findings", driver="GPKG")

    cnt = Counter(f.severity for f in findings)
    t, sl = TXT[lang], SEV_LABEL[lang]
    lines = [f"# {t['title']}", "", f"- {t['src']}: `{path.name}` (layer `{layer}`)", f"- {t['rec']}: {len(gdf)}", "",
             f"## {t['sum']}", ""]
    lines += [f"- {sl[s]}: {cnt.get(s, 0)}" for s in ("blad", "ostrzezenie", "informacja")]
    lines += ["", f"## {t['list']}", ""]
    if findings:
        lines += [t["cols"], "|---|---|---|---|---|"]
        lines += [f"| {f.nr} | {f.rule} | {sl[f.severity]} | {f.msg[lang]} | {f.ref} |" for f in findings]
    else:
        lines.append(t["none"])
    report = out.with_suffix(f".{lang}.md")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{t['rec']}: {len(gdf)} | {sl['blad']}: {cnt.get('blad', 0)} | {sl['ostrzezenie']}: {cnt.get('ostrzezenie', 0)} | "
          f"{sl['informacja']}: {cnt.get('informacja', 0)}")
    print(f"-> {out} (findings)\n-> {report}")
    if fail_on and any(SEVERITY_ORDER[f.severity] <= SEVERITY_ORDER[fail_on] for f in findings):
        return 1
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="vtsqa", description="Kontrola danych drzew wg Standardu 688/2025 m.st. Warszawy")
    p.add_argument("input", type=Path)
    p.add_argument("--layer")
    p.add_argument("--out", type=Path)
    p.add_argument("--lang", choices=["pl", "de", "en"], default="pl")
    p.add_argument("--fail-on", choices=["blad", "ostrzezenie"],
                   help="kod wyjścia 1, gdy są znaleziska o tej wadze lub poważniejsze / exit 1 on findings of this severity or worse")
    p.add_argument("--version", action="version", version=f"vtsqa {__version__}")
    a = p.parse_args()
    out = a.out or a.input.with_name(a.input.stem + "_findings.gpkg")
    return run(a.input, a.layer, out, a.lang, a.fail_on)


if __name__ == "__main__":
    sys.exit(main())
