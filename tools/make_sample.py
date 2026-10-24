"""Generuje SYNTETYCZNY plik GPKG do pokazu (Rembertow, EPSG:2178).

To nie sa dane m.st. Warszawy. Polozenie: okolica ul. Grawerskiej (Rembertow),
atrybuty wymyslone, czesc rekordow ma celowo wstawione bledy (opisane w EXPECTED).
"""
import datetime as dt
import random
from pathlib import Path

import geopandas as gpd
from pyproj import Transformer
from shapely.geometry import Point

OUT = Path(__file__).resolve().parents[1] / "data" / "sample" / "rembertow_syntetyczne.gpkg"
random.seed(688)
tr = Transformer.from_crs("EPSG:4326", "EPSG:2178", always_xy=True)
cx, cy = tr.transform(21.1600, 52.2520)


def add_months(d, n):
    import calendar
    y, m = divmod(d.month - 1 + n, 12)
    yy, mm = d.year + y, m + 1
    return dt.date(yy, mm, min(d.day, calendar.monthrange(yy, mm)[1]))


MATRIX = {2: {"O": 36, "N": 24, "S": 12, "W": 12}, 3: {"O": 24, "N": 12, "S": 6, "W": 6}}
rows = []
for i in range(1, 31):
    k = random.choice([1, 1, 2, 2, 3])
    uz = "" if k == 1 else random.choice("ONSW")
    d0 = dt.date(2026, 4, 1) + dt.timedelta(days=random.randint(0, 60))
    d1 = add_months(d0, 36 if k == 1 else MATRIX[k][uz])
    x, y = cx + random.uniform(-250, 250), cy + random.uniform(-250, 250)
    geom = Point(x, y).buffer(12) if k == 1 else Point(x, y)
    rows.append(dict(nr=f"WAW-R-{i:03d}", klasa=str(k), uzytkowanie=uz, data_ogledzin=str(d0),
                     data_kolejnych=str(d1), obwod=str(random.randint(70, 260)), zrodlo="SYNTETYCZNE", geometry=geom))


def setrow(key, **kw):
    r = next(r for r in rows if r["nr"] == key)
    r.update(kw)
    return r


def as_class(nr, k, uz, months=None, polygon=None):
    r = next(r for r in rows if r["nr"] == nr)
    d0 = dt.date.fromisoformat(r["data_ogledzin"])
    m = months if months is not None else (36 if k == 1 else MATRIX[k][uz])
    pt = r["geometry"].centroid
    geom = pt.buffer(12) if (polygon if polygon is not None else k == 1) else pt
    r.update(klasa=str(k), uzytkowanie=uz, data_kolejnych=str(add_months(d0, m)), geometry=geom)


# Celowe bledy (EXPECTED)
as_class("WAW-R-005", 3, "S", months=12)              # R06 blad: termin 1 rok zamiast 0,5 roku
as_class("WAW-R-008", 1, "S")                         # R03 ostrzezenie: klasa 1 z kategoria
as_class("WAW-R-011", 2, "N"); setrow("WAW-R-011", uzytkowanie="")  # R02 blad: brak kategorii
setrow("WAW-R-014", klasa="5")                        # R01 ostrzezenie: dawna skala
as_class("WAW-R-017", 2, "W"); setrow("WAW-R-017", obwod="45")      # R07 informacja
as_class("WAW-R-020", 3, "W", polygon=True)           # R08 blad: klasa 3 jako obszar
as_class("WAW-R-022", 2, "S"); setrow("WAW-R-022", uzytkowanie="X") # R04 blad
as_class("WAW-R-024", 2, "O"); setrow("WAW-R-024", data_kolejnych="2026-13-01")  # R05 blad
as_class("WAW-R-026", 2, "N"); as_class("WAW-R-027", 2, "N"); setrow("WAW-R-027", nr="WAW-R-026")  # R09 blad: duplikat numeru
as_class("WAW-R-028", 2, "S"); setrow("WAW-R-028", nr="")            # R10 blad
as_class("WAW-R-029", 1, "", polygon=False)           # R08 ostrzezenie: klasa 1 jako punkt

gdf = gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:2178")
OUT.parent.mkdir(parents=True, exist_ok=True)
if OUT.exists():
    OUT.unlink()
gdf.to_file(OUT, layer="drzewa", driver="GPKG")
print(f"{len(gdf)} rekordow -> {OUT}")
