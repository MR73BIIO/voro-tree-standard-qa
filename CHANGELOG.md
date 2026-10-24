# Changelog

## 0.1.0 — 2026-10-24

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
