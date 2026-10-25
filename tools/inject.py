"""Wstrzykiwacz bledow v0.2a: zbiory testowe + truth.json (prawda recenzenta, bez silnika).

Zapieczetowane przewidywanie: PREDICTION_v0_2a.md (Puls #56). Ten plik powstal PO pieczeci.
Kazdy przypadek trafia do innego rekordu. Rekord docelowy najpierw jest ustawiany jako czysty
(klasa, kategoria, termin wg macierzy, geometria zgodna z klasa), potem dostaje blad.

Uzycie:
  python tools/inject.py                    # zapis do data/v0_2a/
  python tools/inject.py --out-dir /tmp/x   # zapis gdzie indziej
"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import random
from pathlib import Path

import geopandas as gpd
import pandas as pd
from pyproj import Transformer
from shapely.geometry import Point

ROOT = Path(__file__).resolve().parents[1]
MATRIX = {2: {"O": 36, "N": 24, "S": 12, "W": 12}, 3: {"O": 24, "N": 12, "S": 6, "W": 6}}
N_RECORDS = 30
_tr = Transformer.from_crs("EPSG:4326", "EPSG:2178", always_xy=True)
CX, CY = _tr.transform(21.1600, 52.2520)


def add_months(d: dt.date, n: int) -> dt.date:
    y, m = divmod(d.month - 1 + n, 12)
    yy, mm = d.year + y, m + 1
    return dt.date(yy, mm, min(d.day, calendar.monthrange(yy, mm)[1]))


def months(k: int, uz: str) -> int:
    return 36 if k == 1 else MATRIX[k][uz]


def base(seed: int, prefix: str) -> list[dict]:
    """Czysta baza: 30 rekordow bez zadnego bledu wg Standardu."""
    rnd = random.Random(seed)
    rows = []
    for i in range(1, N_RECORDS + 1):
        k = rnd.choice([1, 1, 2, 2, 3])
        uz = "" if k == 1 else rnd.choice("ONSW")
        d0 = dt.date(2026, 4, 1) + dt.timedelta(days=rnd.randint(0, 60))
        x, y = CX + rnd.uniform(-250, 250), CY + rnd.uniform(-250, 250)
        pt = Point(x, y)
        rows.append(dict(nr=f"{prefix}-{i:03d}", klasa=str(k), uzytkowanie=uz, data_ogledzin=str(d0),
                         data_kolejnych=str(add_months(d0, months(k, uz))), obwod=str(rnd.randint(70, 260)),
                         zrodlo="SYNTETYCZNE", geometry=pt.buffer(12) if k == 1 else pt))
    return rows


def as_class(r: dict, k: int, uz: str, polygon: bool | None = None) -> dict:
    """Ustawia rekord jako czysty dla klasy k i kategorii uz."""
    d0 = dt.date.fromisoformat(r["data_ogledzin"])
    pt = r["geometry"].centroid
    poly = (k == 1) if polygon is None else polygon
    r.update(klasa=str(k), uzytkowanie=uz, data_kolejnych=str(add_months(d0, months(k, uz))),
             geometry=pt.buffer(12) if poly else pt)
    return r


def shift(r: dict, days: int) -> None:
    r["data_kolejnych"] = str(dt.date.fromisoformat(r["data_kolejnych"]) + dt.timedelta(days=days))


def label(rows: list[dict], r: dict) -> str:
    """Etykieta, ktora silnik nada rekordowi w warstwie findings."""
    return r["nr"] or f"#{rows.index(r) + 1}"


# --- przypadki: funkcja(rows, r, donor) -> lista (regula, waga) prawdy ---------------------
def _t9(rows, r, donor):
    as_class(r, 2, "N"); r["nr"] = donor["nr"]
    return [("R09", "blad", donor["nr"])]


CASES = {
    # A
    "T1a": lambda rows, r, d: (as_class(r, 2, "N"), r.update(klasa="7"), [("R01", "blad")])[-1],
    "T1b": lambda rows, r, d: (as_class(r, 2, "N"), r.update(klasa="4"), [("R01", "ostrzezenie")])[-1],
    "T2": lambda rows, r, d: (as_class(r, 2, "S"), r.update(uzytkowanie=""), [("R02", "blad")])[-1],
    "T3": lambda rows, r, d: (as_class(r, 1, ""), r.update(uzytkowanie="O"), [("R03", "ostrzezenie")])[-1],
    "T4": lambda rows, r, d: (as_class(r, 3, "N"), r.update(uzytkowanie="X"), [("R04", "blad")])[-1],
    "T5": lambda rows, r, d: (as_class(r, 2, "O"), r.update(data_kolejnych="2026-13-01"), [("R05", "blad")])[-1],
    "T6a": lambda rows, r, d: (as_class(r, 2, "N"), shift(r, 90), [("R06", "blad")])[-1],
    "T6b": lambda rows, r, d: (as_class(r, 3, "O"), shift(r, -90), [("R06", "informacja")])[-1],
    "T7": lambda rows, r, d: (as_class(r, 2, "W"), r.update(obwod="45"), [("R07", "informacja")])[-1],
    "T8a": lambda rows, r, d: (as_class(r, 3, "S", polygon=True), [("R08", "blad")])[-1],
    "T8b": lambda rows, r, d: (as_class(r, 1, "", polygon=False), [("R08", "ostrzezenie")])[-1],
    "T9": _t9,
    "T10": lambda rows, r, d: (as_class(r, 2, "N"), r.update(nr=""), [("R10", "blad")])[-1],
    # B
    "B1": lambda rows, r, d: (as_class(r, 2, "N"), r.update(data_ogledzin="45678"), [("R05", "blad")])[-1],
    "B2": lambda rows, r, d: (as_class(r, 2, "N"), r.update(data_kolejnych="25.10.2029"), [("R05", "blad")])[-1],
    "B3": lambda rows, r, d: (as_class(r, 2, "N"), r.update(klasa="2.0"), [])[-1],
    "B4": lambda rows, r, d: (as_class(r, 2, "N"), r.update(klasa="II"), [("R01", "blad")])[-1],
    "B5": lambda rows, r, d: (as_class(r, 2, "N"), r.update(klasa=" 2"), [])[-1],
    "B6": lambda rows, r, d: (as_class(r, 2, "S"), r.update(uzytkowanie="s"), [])[-1],
    "B7": lambda rows, r, d: (as_class(r, 2, "N"), r.update(uzytkowanie=" N"), [])[-1],
    "B8": lambda rows, r, d: (as_class(r, 2, "O"), r.update(obwod="45,5"), [("R07", "informacja")])[-1],
    "B9": lambda rows, r, d: (as_class(r, 2, "O"), r.update(obwod="45 cm"), [("R07", "informacja")])[-1],
    # C
    "C1": lambda rows, r, d: (as_class(r, 2, "N"), r.update(obwod="60"), [("R07", "informacja")])[-1],
    "C2": lambda rows, r, d: (as_class(r, 2, "N"), r.update(obwod="61"), [])[-1],
    "C3": lambda rows, r, d: (as_class(r, 2, "N"), shift(r, 31), [])[-1],
    "C4": lambda rows, r, d: (as_class(r, 2, "N"), shift(r, 32), [("R06", "blad")])[-1],
    # M
    "M1": lambda rows, r, d: (as_class(r, 2, "N"), r.update(klasa="7", obwod="45"),
                              [("R01", "blad"), ("R07", "informacja")])[-1],
    "M2": lambda rows, r, d: (as_class(r, 2, "S"), shift(r, 90), r.update(uzytkowanie=""),
                              [("R02", "blad"), ("R06", "blad")])[-1],
    "M3": lambda rows, r, d: (as_class(r, 2, "N"), r.update(nr="", klasa="7"),
                              [("R10", "blad"), ("R01", "blad")])[-1],
    "M4": lambda rows, r, d: (as_class(r, 2, "N"), r.update(uzytkowanie="X", data_kolejnych="2026-13-01"),
                              [("R04", "blad"), ("R05", "blad")])[-1],
    "M5": lambda rows, r, d: (as_class(r, 3, "S", polygon=True), r.update(uzytkowanie=""),
                              [("R08", "blad"), ("R02", "blad")])[-1],
    "M6": lambda rows, r, d: (as_class(r, 2, "N", polygon=True), r.update(klasa="4"),
                              [("R01", "ostrzezenie"), ("R08", "blad")])[-1],
}

A = ["T1a", "T1b", "T2", "T3", "T4", "T5", "T6a", "T6b", "T7", "T8a", "T8b", "T9", "T10"]
B = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9"]
CM = ["C1", "C2", "C3", "C4", "M1", "M2", "M3", "M4", "M5", "M6"]

SETS = [  # (plik, seed, prefiks, przypadki, zycie)
    ("golden", 688, "G", [], "L1"),
    ("seed_A", 101, "A", A, "L1"),
    ("seed_B", 202, "B", A, "L2"),
    ("seed_L3", 303, "F", B, "L3"),
    ("seed_L4", 404, "C", CM, "L4"),
]


def build(seed: int, prefix: str, cases: list[str]) -> tuple[list[dict], list[dict]]:
    rows = base(seed, prefix)
    rnd = random.Random(seed * 7 + 1)
    idx = rnd.sample(range(N_RECORDS), len(cases) + 1)  # +1: dawca dla T9
    donor = rows[idx[-1]]
    truth = []
    for case, i in zip(cases, idx):
        r = rows[i]
        exp = CASES[case](rows, r, donor)
        truth.append({"case": case, "row": i + 1,
                      "expected": [[e[2] if len(e) == 3 else None, e[0], e[1]] for e in exp]})
    for t in truth:  # etykiety po wszystkich zmianach (nr mogl sie zmienic)
        r = rows[t["row"] - 1]
        for e in t["expected"]:
            e[0] = e[0] or label(rows, r)
    return rows, truth


def typed_b10(seed: int) -> tuple[list[dict], list[dict]]:
    """B10: czysta baza zapisana z typami kolumn (data, liczba calkowita, liczba)."""
    rows = base(seed, "T")
    for r in rows:
        r["data_ogledzin"] = dt.date.fromisoformat(r["data_ogledzin"])
        r["data_kolejnych"] = dt.date.fromisoformat(r["data_kolejnych"])
        r["klasa"] = int(r["klasa"])
        r["obwod"] = float(r["obwod"])
    return rows, [{"case": "B10", "row": None, "expected": []}]


def write(rows: list[dict], path: Path) -> None:
    gdf = gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:2178")
    for col in ("data_ogledzin", "data_kolejnych"):  # B10: obiekty date -> prawdziwe pole daty w GPKG
        if gdf[col].map(lambda v: isinstance(v, dt.date)).all():
            gdf[col] = pd.to_datetime(gdf[col])
    if path.exists():
        path.unlink()
    gdf.to_file(path, layer="drzewa", driver="GPKG")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", type=Path, default=ROOT / "data" / "v0_2a")
    out = ap.parse_args().out_dir
    out.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, seed, prefix, cases, life in SETS:
        rows, truth = build(seed, prefix, cases)
        write(rows, out / f"{name}.gpkg")
        manifest.append({"file": f"{name}.gpkg", "seed": seed, "life": life, "cases": truth})
    rows, truth = typed_b10(305)
    write(rows, out / "seed_L3_b10_typed.gpkg")
    manifest.append({"file": "seed_L3_b10_typed.gpkg", "seed": 305, "life": "L3", "cases": truth})
    (out / "truth.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    for m in manifest:
        n = sum(len(c["expected"]) for c in m["cases"])
        print(f"{m['life']} {m['file']}: {len(m['cases'])} przypadkow, prawda = {n} znalezisk")
    print(f"-> {out / 'truth.json'}")


if __name__ == "__main__":
    main()
