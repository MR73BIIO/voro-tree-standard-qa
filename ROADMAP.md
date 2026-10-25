# Roadmapa / Roadmap

**PL** · [DE](#de) · [EN](#en)

## Cel

Wykonawca inwentaryzacji wrzuca swoją dostawę GeoPackage i w ciągu minuty widzi w QGIS, które rekordy łamią reguły standardu zamawiającego, z odwołaniem do konkretnego punktu. Zanim urząd zrobi odbiór.

## Model pracy

Każdy etap przechodzi ten sam cykl:

1. **R0 — rozpoznanie.** Co jest dostępne, w jakiej formie, czego brakuje. Wynik: plik R0 z datami i godzinami pomiarów.
2. **Przewidywanie.** Spisane i zacommitowane *przed* uruchomieniem, z pieczęcią SHA-256. Wpis `prediction` w Pulsie.
3. **Pomiar.** Uruchomienie na WSL, wynik zgodny na każdej maszynie.
4. **OUTCOME.** Werdykt: CONFIRMED, REFUTED albo NO DATA. Wpis `life` w Pulsie. REFUTED bez diagnozy zostaje otwarty.
5. **Publikacja.** Tylko to, co zrobione, zacommitowane i zmierzone. Release z DOI to wpis `milestone` w Pulsie.

Dane syntetyczne są oznaczone w nazwie pliku, w README i w polu `zrodlo`. Testy na danych syntetycznych sprawdzają silnik, nie są pomiarem i nie są „życiem” w Pulsie.

## Etapy

### v0.1 Fundament — zamknięte (v0.1.0, v0.1.1)

| Element | Stan |
|---|---|
| Silnik, 10 reguł R01–R10, komunikaty PL/DE/EN | zrobione |
| Syntetyczny GPKG Rembertów (30 drzew, 11 błędów) | zrobione |
| Styl QGIS dla `findings` (podpowiedź PL/DE/EN) | zrobione |
| Strona w przeglądarce, 3 języki | zrobione |
| Testy (5) i GitHub Actions, bramka jakości `--fail-on`, komenda `vtsqa` | zrobione |
| Mapa wyniku w README (z prawdziwego uruchomienia), README PL/DE/EN | zrobione |
| Repo publiczne, GitHub Pages, release v0.1.0, DOI 10.5281/zenodo.23624899 | zrobione |
| Puls: wpis `milestone` z DOI, PL/DE/EN | zrobione (#54, #55) |

**Kryterium wyjścia:** testy przechodzą; w QGIS warstwa `findings` pokazuje 11 znalezisk na pliku syntetycznym; strona działa na GitHub Pages w PL/DE/EN; release ma DOI; wpis milestone w Pulsie.

### v0.2a Pierwsze życia silnika — zamknięte (0.2.0)

- Przewidywanie L1–L4 z konsekwencjami K0–K7 zapieczętowane przed kodem wstrzykiwacza (Puls #56).
- Wstrzykiwacz `tools/inject.py` (zestawy A/B/C/M), `truth.json`, pomiar `tools/measure.py`.
- Wynik: 4/4 CONFIRMED (Puls #57–#60), `OUTCOME_v0_2a.md`, `results/v0_2a/`.
- Zmierzone ograniczenia (RULES.md): po pierwszym błędzie typu R01/R02/R04/R05 kontrola rekordu się kończy; obwód z jednostką (`45 cm`) pomijany bez komunikatu.

### v0.2b Warszawa na danych publicznych — skreślone

R0 zamknięte 25.10.2026: publiczny WMS m.st. Warszawy zwraca dla `ZIELEN_DRZEWA` tylko `OBJECTID`, bez klasy ryzyka, gatunku i obwodu. Zgodności ze Standardem nie da się sprawdzić na danych publicznych. Kontrola ma sens na dostawie GPKG wykonawcy.

### v0.2.1 Luki z v0.2a

- Zgłaszanie wszystkich błędów w rekordzie (bez przerywania po pierwszym).
- Komunikat dla obwodu z jednostką lub tekstem.
- Przewidywanie przed kodem, pomiar na tych samych zestawach, wpisy w Pulsie, release z DOI.

### VORO (osobny etap, po v0.2.1)

Podpięcie do organizmu VORO: pakiet domenowy, providery Observation i Outcome, bramka regresji K6. LifeKernel bez zmian.

### v0.3 Algorytm w QGIS

- Algorytm Processing, wzorem VORO TERYT QA: wybór warstwy, mapowanie pól, wynik w projekcie ze stylem.
- Bez dodatkowych pakietów: tylko to, co ma QGIS.

**Kryterium wyjścia:** na pliku syntetycznym algorytm w QGIS 3.40 daje te same 11 znalezisk co silnik z wiersza poleceń; release z DOI.

### v0.4 Pakiet reguł DE

- R0 na wytycznych FLL do kontroli drzew: co faktycznie określają (pola, interwały, klasy). Dopiero potem reguły w `rules/de_fll/`.

**Kryterium wyjścia:** opis reguł z odwołaniami do wytycznych i syntetyczny plik testowy z wykrytymi wszystkimi wstawionymi błędami.

### Poza zakresem

Ocena stanu zdrowotnego drzew, praca w terenie, arbotagi, abonament.

---

<a id="de"></a>
## DE

### Ziel

Ein Auftragnehmer lädt seine GeoPackage-Lieferung und sieht in QGIS innerhalb einer Minute, welche Datensätze das Regelwerk des Auftraggebers verletzen, mit Verweis auf den Abschnitt. Vor der Abnahme.

### Arbeitsweise

1. **R0 — Erkundung:** was verfügbar ist, in welcher Form, was fehlt. Ergebnis: R0-Datei mit Datum und Uhrzeit jeder Messung.
2. **Vorhersage:** vor dem Lauf geschrieben und committet, mit SHA-256-Siegel. Eintrag `prediction` im Puls.
3. **Messung:** Lauf auf WSL, gleiches Ergebnis auf jeder Maschine.
4. **OUTCOME:** CONFIRMED, REFUTED oder NO DATA. Eintrag `life` im Puls. REFUTED ohne Diagnose bleibt offen.
5. **Veröffentlichung:** nur Erledigtes, Committetes und Gemessenes. Release mit DOI ist ein `milestone` im Puls.

Synthetische Daten sind im Dateinamen, im README und im Feld `zrodlo` gekennzeichnet. Tests auf synthetischen Daten prüfen die Engine und gelten nicht als Messung.

### Etappen

| | Inhalt | Abschlusskriterium |
|---|---|---|
| v0.1 | Engine, 10 Regeln, synthetische Daten, QGIS-Stil, Webseite PL/DE/EN | 11 Befunde in QGIS, Seite auf GitHub Pages, Release mit DOI, Puls-Milestone |
| v0.2a | erste gemessene Läufe auf eingebauten Fehlern | 4/4 CONFIRMED — erledigt (0.2.0) |
| v0.2b | Warschau auf öffentlichen Daten | gestrichen: öffentlicher WMS liefert nur `OBJECTID` |
| v0.2.1 | alle Fehler pro Datensatz melden, Meldung für Umfang mit Einheit | Vorhersage, Messung, Release mit DOI |
| VORO | Anbindung an den VORO-Organismus | Regression K6 unverändert |
| v0.3 | QGIS-Processing-Algorithmus ohne Zusatzpakete | gleiche 11 Befunde in QGIS 3.40 |
| v0.4 | Regelpaket DE nach FLL-Baumkontrollrichtlinien, zuerst R0 | Regelbeschreibung mit Verweisen, alle Testfehler gefunden |

Nicht im Umfang: Zustandsbewertung, Feldarbeit, Baumplaketten, Abo.

---

<a id="en"></a>
## EN

### Goal

An inventory contractor loads their GeoPackage delivery and within a minute sees in QGIS which records break the client's standard, with a reference to the exact section. Before acceptance.

### How the work runs

1. **R0 — reconnaissance:** what is available, in what form, what is missing. Output: an R0 file with the date and time of each measurement.
2. **Prediction:** written and committed *before* the run, sealed with SHA-256. A `prediction` entry in Puls.
3. **Measurement:** run on WSL, same result on every machine.
4. **OUTCOME:** CONFIRMED, REFUTED or NO DATA. A `life` entry in Puls. REFUTED without a diagnosis stays open.
5. **Publication:** only what is done, committed and measured. A release with a DOI is a `milestone` in Puls.

Synthetic data is marked in the file name, the README and the `zrodlo` field. Tests on synthetic data check the engine; they are not measurements.

### Stages

| | Scope | Exit criterion |
|---|---|---|
| v0.1 | engine, 10 rules, synthetic data, QGIS style, web page PL/DE/EN | 11 findings in QGIS, page on GitHub Pages, release with DOI, Puls milestone |
| v0.2a | first measured runs on injected errors | 4/4 CONFIRMED — done (0.2.0) |
| v0.2b | Warsaw on public data | dropped: public WMS returns only `OBJECTID` |
| v0.2.1 | report all errors per record, message for girth with a unit | prediction, measurement, release with DOI |
| VORO | link to the VORO organism | K6 regression unchanged |
| v0.3 | QGIS Processing algorithm, no extra packages | same 11 findings in QGIS 3.40 |
| v0.4 | German rule pack based on FLL tree inspection guidelines, R0 first | rule description with references, all test errors found |

Out of scope: tree condition assessment, field work, tree tags, subscription.
