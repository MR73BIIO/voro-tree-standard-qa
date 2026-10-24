"""Testy silnika na syntetycznym pliku (tools/make_sample.py) i na pojedynczych rekordach."""
from collections import Counter
from pathlib import Path

import geopandas as gpd

from vtsqa.engine import add_months, check_record, check_records, period_months

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample" / "rembertow_syntetyczne.gpkg"


def test_matrix_zal7():
    assert period_months(1, "") == 36
    assert [period_months(2, u) for u in "ONSW"] == [36, 24, 12, 12]
    assert [period_months(3, u) for u in "ONSW"] == [24, 12, 6, 6]


def test_add_months_end_of_month():
    import datetime as dt
    assert add_months(dt.date(2026, 8, 31), 6) == dt.date(2027, 2, 28)


def test_clean_record_has_no_findings():
    rec = dict(nr="A1", klasa="2", uzytkowanie="N", data_ogledzin="2026-04-15", data_kolejnych="2028-04-15", obwod="120")
    assert check_record(rec, "Point") == []


def test_sample_expected_findings():
    gdf = gpd.read_file(SAMPLE, layer="drzewa")
    recs = [{**{k: r[k] for k in gdf.columns if k != "geometry"}, "_row": i + 1} for i, r in gdf.iterrows()]
    found = check_records(recs, [g.geom_type for g in gdf.geometry])
    got = Counter((f.rule, f.severity) for f in found)
    expected = Counter({
        ("R06", "blad"): 1, ("R02", "blad"): 1, ("R08", "blad"): 1, ("R04", "blad"): 1,
        ("R05", "blad"): 1, ("R09", "blad"): 1, ("R10", "blad"): 1,
        ("R03", "ostrzezenie"): 1, ("R01", "ostrzezenie"): 1, ("R08", "ostrzezenie"): 1,
        ("R07", "informacja"): 1,
    })
    assert got == expected
    assert all(set(f.msg) == {"pl", "de", "en"} for f in found)


def test_cli_quality_gate(tmp_path):
    from vtsqa.__main__ import run
    out = tmp_path / "f.gpkg"
    assert run(SAMPLE, "drzewa", out, "en", None) == 0
    assert run(SAMPLE, "drzewa", out, "en", "blad") == 1
    assert (tmp_path / "f.en.md").exists()
    assert len(gpd.read_file(out, layer="findings")) == 11
