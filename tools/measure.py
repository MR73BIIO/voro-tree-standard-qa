"""Pomiar v0.2a: uruchamia vtsqa przez CLI (run) na zbiorach z inject.py i porownuje z truth.json.

Porownanie po (nr, regula, waga). Przewidywania przepisane z zapieczetowanego
PREDICTION_v0_2a.md (Puls #56, sha256 2820f2f8...35da5). Werdykt kazdego zycia:
CONFIRMED, gdy TP/FN/FP sa rowne przewidywanym, a FN dotycza dokladnie wskazanych
przypadkow (przypadek, regula). Inaczej REFUTED. NO DATA, gdy pomiar sie nie odbyl.

Uzycie:  python tools/measure.py [--data-dir data/v0_2a] [--out-dir results/v0_2a]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import geopandas as gpd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from vtsqa import __version__  # noqa: E402
from vtsqa.__main__ import run  # noqa: E402

PREDICTED = {  # zycie: (TP, FN, FP, zbior FN jako (przypadek, regula))
    "L1": (13, 0, 0, set()),
    "L2": (13, 0, 0, set()),
    "L3": (4, 1, 0, {("B9", "R07")}),
    "L4": (11, 3, 0, {("M2", "R06"), ("M4", "R05"), ("M6", "R08")}),
}


def found_in(path: Path, work: Path) -> Counter:
    out = work / (path.stem + "_findings.gpkg")
    run(path, "drzewa", out, "pl", None)
    f = gpd.read_file(out, layer="findings")
    return Counter((str(r["nr"]), str(r["regula"]), str(r["waga"])) for _, r in f.iterrows())


def compare(truth_cases: list[dict], found: Counter) -> dict:
    truth = Counter()
    owner = {}
    for c in truth_cases:
        for nr, rule, sev in c["expected"]:
            truth[(nr, rule, sev)] += 1
            owner[(nr, rule, sev)] = c["case"]
    tp = truth & found
    fn = truth - found
    fp = found - truth
    return {
        "truth": sum(truth.values()), "found": sum(found.values()),
        "TP": sum(tp.values()), "FN": sum(fn.values()), "FP": sum(fp.values()),
        "fn_cases": sorted((owner[k], k[1]) for k in fn),
        "fn": sorted(list(k) for k in fn), "fp": sorted(list(k) for k in fp),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, default=ROOT / "data" / "v0_2a")
    ap.add_argument("--out-dir", type=Path, default=ROOT / "results" / "v0_2a")
    a = ap.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((a.data_dir / "truth.json").read_text(encoding="utf-8"))

    lives: dict[str, dict] = {}
    for m in manifest:
        life = lives.setdefault(m["life"], {"files": [], "cases": [], "found": Counter(), "error": None})
        life["files"].append(m["file"])
        life["cases"] += m["cases"]
        try:
            life["found"] += found_in(a.data_dir / m["file"], a.out_dir)
        except Exception as e:  # pomiar sie nie odbyl
            life["error"] = f"{m['file']}: {type(e).__name__}: {e}"

    report, lines = {"vtsqa": __version__, "lives": {}}, [f"# Pomiar v0.2a (vtsqa {__version__})", ""]
    lines += ["| Zycie | Pliki | Prawda | Znalezione | TP / FN / FP | Przewidywane | FN (przypadek, regula) | Werdykt |",
              "|---|---|---|---|---|---|---|---|"]
    for name in sorted(lives):
        life = lives[name]
        tp_p, fn_p, fp_p, fncases_p = PREDICTED[name]
        if life["error"]:
            res, verdict = {"error": life["error"]}, "NO DATA"
            row = f"| {name} | {', '.join(life['files'])} | — | — | — | {tp_p} / {fn_p} / {fp_p} | — | NO DATA |"
        else:
            res = compare(life["cases"], life["found"])
            ok = ((res["TP"], res["FN"], res["FP"]) == (tp_p, fn_p, fp_p)
                  and set(map(tuple, res["fn_cases"])) == fncases_p)
            verdict = "CONFIRMED" if ok else "REFUTED"
            fnc = ", ".join(f"{c}:{r}" for c, r in res["fn_cases"]) or "—"
            row = (f"| {name} | {', '.join(life['files'])} | {res['truth']} | {res['found']} | "
                   f"{res['TP']} / {res['FN']} / {res['FP']} | {tp_p} / {fn_p} / {fp_p} | {fnc} | **{verdict}** |")
        res.update(verdict=verdict, predicted=[tp_p, fn_p, fp_p, sorted(fncases_p)])
        report["lives"][name] = res
        lines.append(row)

    for name, res in report["lives"].items():
        if res.get("fp") or res.get("fn"):
            lines += ["", f"## {name}", ""]
            lines += [f"- FN: `{k}`" for k in res.get("fn", [])]
            lines += [f"- FP: `{k}`" for k in res.get("fp", [])]
        if res.get("error"):
            lines += ["", f"## {name}", "", f"- blad pomiaru: `{res['error']}`"]

    (a.out_dir / "outcome.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    (a.out_dir / "outcome.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
