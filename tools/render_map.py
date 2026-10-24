"""Rysuje docs/findings_map.png z wyniku silnika na pliku syntetycznym (do README).

Uruchom po: python tools/make_sample.py
"""
from collections import Counter
from pathlib import Path
import tempfile

import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from vtsqa.__main__ import run

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample" / "rembertow_syntetyczne.gpkg"
OUT = ROOT / "docs" / "findings_map.png"

STYLE = {  # te same kolory co qgis/findings.qml
    "blad": dict(color="#b23a2e", marker="o", s=150, label="error / błąd / Fehler"),
    "ostrzezenie": dict(color="#e2a028", marker="^", s=170, label="warning / ostrzeżenie / Warnung"),
    "informacja": dict(color="#3b6a8f", marker="s", s=110, label="note / informacja / Hinweis"),
}

trees = gpd.read_file(SAMPLE, layer="drzewa")
with tempfile.TemporaryDirectory() as d:
    out = Path(d) / "f.gpkg"
    run(SAMPLE, "drzewa", out, "en")
    fnd = gpd.read_file(out, layer="findings")

fig, ax = plt.subplots(figsize=(11, 8.2), dpi=110)
fig.patch.set_facecolor("#fbfcf9")
ax.set_facecolor("#eef1ec")
areas = trees[trees.geom_type.isin(["Polygon", "MultiPolygon"])]
pts = trees[trees.geom_type.isin(["Point", "MultiPoint"])]
areas.plot(ax=ax, color="#b9d4c0", edgecolor="#2f6b4a", linewidth=0.8)
pts.plot(ax=ax, color="#2f6b4a", markersize=14)
cnt = Counter(fnd["waga"])
handles = [Line2D([], [], marker="o", color="none", markerfacecolor="#b9d4c0", markeredgecolor="#2f6b4a",
                  markersize=10, label="tree, class 1 (area)"),
           Line2D([], [], marker="o", color="none", markerfacecolor="#2f6b4a", markersize=5,
                  label="tree, class 2–3 (point)")]
for sev, st in STYLE.items():
    sub = fnd[fnd["waga"] == sev]
    if len(sub):
        ax.scatter(sub.geometry.x, sub.geometry.y, c=st["color"], marker=st["marker"], s=st["s"],
                   edgecolors="white", linewidths=1.2, zorder=5)
    handles.append(Line2D([], [], marker=st["marker"], color="none", markerfacecolor=st["color"],
                          markeredgecolor="white", markersize=10, label=f"{st['label']} ({cnt.get(sev, 0)})"))
placed = []
for _, r in fnd.sort_values("nr").iterrows():
    x, y = r.geometry.x, r.geometry.y
    crowded = any(abs(x - px) < 60 and abs(y - py) < 20 for px, py in placed)
    placed.append((x, y))
    ax.annotate(f"{r['nr']} · {r['regula']}", (x, y), xytext=(7, -15 if crowded else 6),
                textcoords="offset points", fontsize=8, color="#1d2a22",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8), zorder=6)
minx, miny, maxx, maxy = trees.total_bounds
ax.plot([minx, minx + 100], [miny - 25, miny - 25], color="#1d2a22", lw=3)
ax.text(minx + 50, miny - 40, "100 m", ha="center", va="top", fontsize=9, color="#1d2a22")
ax.set_xlim(minx - 40, maxx + 90)
ax.set_ylim(miny - 70, maxy + 40)
ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel(""); ax.set_ylabel("")
for sp in ax.spines.values():
    sp.set_color("#cdd6cc")
ax.set_title("Standard 688/2025 · synthetic sample, Rembertów (EPSG:2178)\n"
             f"{len(trees)} trees · {len(fnd)} findings · not City of Warsaw data",
             loc="left", fontsize=12, color="#1d2a22")
ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False, fontsize=9)
fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.25)
print(f"-> {OUT}")
