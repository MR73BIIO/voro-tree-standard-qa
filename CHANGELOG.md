# Changelog

## 0.2.0 — 2026-10-25

**PL**
- v0.2a: pierwsze zmierzone życia. Przewidywanie L1–L4 (K0–K7) zapieczętowane przed kodem; wstrzykiwacz `tools/inject.py`, pomiar `tools/measure.py`.
- Wynik 4/4 CONFIRMED: `OUTCOME_v0_2a.md`, `results/v0_2a/`.
- `RULES.md`: kolejność sprawdzania i dwa zmierzone ograniczenia (przerwanie po pierwszym błędzie typu R01/R02/R04/R05; obwód z jednostką pomijany).
- ROADMAP: v0.2b skreślone (publiczny WMS daje tylko `OBJECTID`), następny etap v0.2.1.

**DE**
- v0.2a: erste gemessene Läufe. Vorhersage L1–L4 (K0–K7) vor dem Code versiegelt; Fehler-Injektor `tools/inject.py`, Messung `tools/measure.py`.
- Ergebnis 4/4 CONFIRMED: `OUTCOME_v0_2a.md`, `results/v0_2a/`.
- `RULES.md`: Prüfreihenfolge und zwei gemessene Grenzen.
- ROADMAP: v0.2b gestrichen, nächste Etappe v0.2.1.

**EN**
- v0.2a: first measured runs. Prediction L1–L4 (K0–K7) sealed before the code; error injector `tools/inject.py`, measurement `tools/measure.py`.
- Result 4/4 CONFIRMED: `OUTCOME_v0_2a.md`, `results/v0_2a/`.
- `RULES.md`: check order and two measured limits.
- ROADMAP: v0.2b dropped, next stage v0.2.1.

## 0.1.1 — 2026-10-25

DOI: [10.5281/zenodo.23640565](https://doi.org/10.5281/zenodo.23640565) (wersja / Version / version 0.1.1)

**PL**
- `tools/make_sample.py` domyślnie zapisuje do bieżącego katalogu; plik w repo nadpisuje tylko z `--update-repo-sample`. Nowa opcja `--out`. Zawartość danych bez zmian (ten sam seed, 30 rekordów).
- `rules/warszawa_688/R0.md`: R0 zamknięte. Publiczny WMS m.st. Warszawy zwraca dla `ZIELEN_DRZEWA` tylko `OBJECTID` (114 wierszy, 109 z `OBJECTID`, 5 pustych), bez atrybutów wymaganych przez Standard 688/2025.

**DE**
- `tools/make_sample.py` schreibt standardmäßig ins aktuelle Verzeichnis; die Datei im Repo wird nur mit `--update-repo-sample` überschrieben. Neue Option `--out`. Daten unverändert.
- `R0.md`: R0 geschlossen. Der öffentliche WMS liefert für `ZIELEN_DRZEWA` nur `OBJECTID`, keine Attribute.

**EN**
- `tools/make_sample.py` writes to the current directory by default; the repo file is overwritten only with `--update-repo-sample`. New `--out` option. Data unchanged.
- `R0.md`: R0 closed. The public WMS returns only `OBJECTID` for `ZIELEN_DRZEWA`, no attributes.

## 0.1.0 — 2026-10-24

DOI: [10.5281/zenodo.23624899](https://doi.org/10.5281/zenodo.23624899) (wersja / Version / version 0.1.0), [10.5281/zenodo.23624898](https://doi.org/10.5281/zenodo.23624898) (wszystkie wersje / alle Versionen / all versions)

**PL**
- Silnik reguł R01–R10 dla Standardu 688/2025 m.st. Warszawy, komunikaty PL/DE/EN.
- Syntetyczny plik `data/sample/rembertow_syntetyczne.gpkg`: 30 drzew, 11 celowo wstawionych błędów.
- Wynik na pliku syntetycznym: 7 błędów, 3 ostrzeżenia, 1 informacja; wykryte wszystkie 11 wstawionych błędów.
- Styl QGIS `qgis/findings.qml`, strona `docs/index.html` (PL/DE/EN), mapa wyniku `docs/findings_map.png`.
- Komenda `vtsqa`, bramka jakości `--fail-on` (kod wyjścia 1), 5 testów w GitHub Actions.

**DE**
- Regel-Engine R01–R10 für den Warschauer Standard 688/2025, Meldungen PL/DE/EN.
- Synthetische Datei `data/sample/rembertow_syntetyczne.gpkg`: 30 Bäume, 11 absichtlich eingebaute Fehler.
- Ergebnis: 7 Fehler, 3 Warnungen, 1 Hinweis; alle 11 eingebauten Fehler gefunden.
- QGIS-Stil `qgis/findings.qml`, Webseite `docs/index.html` (PL/DE/EN), Ergebniskarte `docs/findings_map.png`.
- Befehl `vtsqa`, Qualitätsschranke `--fail-on` (Exit-Code 1), 5 Tests in GitHub Actions.

**EN**
- Rule engine R01–R10 for the Warsaw Standard 688/2025, messages in PL/DE/EN.
- Synthetic file `data/sample/rembertow_syntetyczne.gpkg`: 30 trees, 11 deliberate errors.
- Result: 7 errors, 3 warnings, 1 note; all 11 inserted errors found.
- QGIS style `qgis/findings.qml`, web page `docs/index.html` (PL/DE/EN), result map `docs/findings_map.png`.
- `vtsqa` command, quality gate `--fail-on` (exit code 1), 5 tests in GitHub Actions.
