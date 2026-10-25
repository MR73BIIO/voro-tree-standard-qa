# PREDICTION v0.2a — voro-tree-standard-qa

Status: **zapieczętowane 25.10.2026** (przed napisaniem `tools/inject.py` i przed pomiarem)
Silnik: `vtsqa/engine.py` w wersji v0.1.1 (DOI 10.5281/zenodo.23640565)
Płaszczyzna Pulsu: `pl-drzewa`

## 0. Skąd biorą się przewidywania

Wszystkie przewidywania poniżej powstały z czytania kodu `engine.py`, bez uruchamiania
silnika na nowych przypadkach. Niepewność jest realna w trzech miejscach:

1. odczyt GPKG (typy kolumn po zapisie i odczycie: tekst, data, liczba),
2. `vtsqa/__main__.py` (sposób przekazania typu geometrii i pól do silnika) — nie był czytany
   przy pisaniu tego pliku,
3. moje czytanie kolejności reguł i wczesnych wyjść (`return`) w `check_record`.

## 1. Prawda i pomiar

- `tools/inject.py` zapisuje GPKG i `truth.json`. `truth.json` zawiera to, co **powinno**
  zostać zgłoszone (etykieta recenzenta): lista `(nr, reguła, waga)` dla każdego przypadku.
- Pomiar: dopasowanie wyniku `vtsqa` do `truth.json` po `(nr, reguła, waga)`.
  Liczę: TP (zgodne), FN (prawda bez znaleziska), FP (znalezisko bez prawdy).
- Baza: 30 rekordów z generatora `make_sample.py` **bez** sekcji celowych błędów
  (klasa 1 jako obszar bez kategorii, klasy 2–3 jako punkty z kategorią, termin dokładnie
  wg macierzy, obwód 70–260 cm).

## 2. Przypadki

### A — typ = reguła (13 wariantów, jeden błąd na rekord)

| Wariant | Wstrzyknięcie | Prawda | Przewiduję |
|---|---|---|---|
| T1a | `klasa` = 7 | R01 błąd | R01 błąd |
| T1b | `klasa` = 4 | R01 ostrzeżenie | R01 ostrzeżenie |
| T2 | klasa 2/3, `uzytkowanie` = "" | R02 błąd | R02 błąd |
| T3 | klasa 1 + `uzytkowanie` z O/N/S/W | R03 ostrzeżenie | R03 ostrzeżenie |
| T4 | klasa 2/3, `uzytkowanie` = "X" | R04 błąd | R04 błąd |
| T5 | `data_kolejnych` = "2026-13-01" | R05 błąd | R05 błąd |
| T6a | `data_kolejnych` = macierz + 90 dni | R06 błąd | R06 błąd |
| T6b | `data_kolejnych` = macierz − 90 dni | R06 informacja | R06 informacja |
| T7 | `obwod` = 45 | R07 informacja | R07 informacja |
| T8a | klasa 2/3 jako poligon | R08 błąd | R08 błąd |
| T8b | klasa 1 jako punkt | R08 ostrzeżenie | R08 ostrzeżenie |
| T9 | `nr` skopiowany z nietkniętego rekordu | 1 × R09 błąd na parę | 1 × R09 błąd |
| T10 | `nr` = "" | R10 błąd | R10 błąd |

### B — prawdziwe błędy formatu z dostaw

| Przypadek | Wstrzyknięcie | Prawda | Przewiduję | Podstawa w kodzie |
|---|---|---|---|---|
| B1 | `data_ogledzin` = "45678" (liczba Excela) | R05 błąd | R05 błąd | regex RRRR-MM-DD |
| B2 | `data_kolejnych` = "25.10.2029" | R05 błąd | R05 błąd | regex RRRR-MM-DD |
| B3 | `klasa` = "2.0" | brak | brak | obcięcie ".0" |
| B4 | `klasa` = "II" | R01 błąd | R01 błąd | regex [1-5] |
| B5 | `klasa` = " 2" | brak | brak | `strip()` w `_txt` |
| B6 | `uzytkowanie` = "s" | brak | brak | `upper()` |
| B7 | `uzytkowanie` = " N" | brak | brak | `strip()` + `upper()` |
| B8 | `obwod` = "45,5" | R07 informacja | R07 informacja | zamiana przecinka |
| B9 | `obwod` = "45 cm" | R07 informacja | **brak (przeoczenie)** | `float()` się wywraca, wyjątek jest połykany |
| B10 | osobny plik: czysta baza z kolumnami typowanymi (data jako DATE, klasa jako liczba, obwód jako liczba) | brak | brak (niepewne) | `Timestamp` jest `datetime`; klasa "2.0" obcinana |

### C — granice progów

| Przypadek | Wstrzyknięcie | Prawda | Przewiduję |
|---|---|---|---|
| C1 | `obwod` = 60 | R07 informacja | R07 informacja (warunek ≤ 60) |
| C2 | `obwod` = 61 | brak | brak |
| C3 | `data_kolejnych` = macierz + 31 dni | brak | brak (warunek > 31) |
| C4 | `data_kolejnych` = macierz + 32 dni | R06 błąd | R06 błąd |

### M — dwa błędy w jednym rekordzie (kolejność reguł)

| Przypadek | Wstrzyknięcie | Prawda (oba błędy) | Przewiduję | Podstawa |
|---|---|---|---|---|
| M1 | T1a + T7 | R01 błąd, R07 inf. | **oba** | R07 jest sprawdzane przed R01 |
| M2 | T2 + T6a | R02 błąd, R06 błąd | **tylko R02** | wyjście po R02 |
| M3 | T10 + T1a | R10 błąd, R01 błąd | **oba** | R10 nie przerywa |
| M4 | T4 + T5 | R04 błąd, R05 błąd | **tylko R04** | wyjście po R04 |
| M5 | T8a + T2 | R08 błąd, R02 błąd | **oba** | R08 przed kategorią |
| M6 | T1b + T8a | R01 ostrz., R08 błąd | **tylko R01** | wyjście po R01 (klasa 4–5) |

## 3. Życia i przewidywane liczby

| Życie | Zbiór | Prawda | Przewiduję TP / FN / FP |
|---|---|---|---|
| L1 | golden (baza) + seed_A (seed 101) | 0 + 13 | 13 / 0 / 0 |
| L2 | seed_B (seed 202, ten sam skład co A) | 13 | 13 / 0 / 0 |
| L3 | B1–B9 (seed 303) + plik B10 | 5 | **4 / 1 / 0** (FN = B9) |
| L4 | C1–C4 + M1–M6 (seed 404) | 2 + 12 | **11 / 3 / 0** (FN = R06 w M2, R05 w M4, R08 w M6) |

Werdykt każdego życia: CONFIRMED, gdy TP, FN i FP zgadzają się dokładnie z tabelą,
a FN dotyczą dokładnie wskazanych przypadków. W przeciwnym razie REFUTED.
NO DATA, gdy pomiar się technicznie nie odbył.

## 4. Konsekwencje (zapisane przed wynikiem)

- **K0 — wszystkie cztery życia CONFIRMED.** Silnik zachowuje się tak, jak wynika z kodu,
  łącznie ze znanymi lukami. Następna decyzja: domena VORO `trees_688` i providery (krok 3
  ROADMAP v0.2a). Luki z B9 i M2/M4/M6 idą do nauki jako znane ograniczenia (punkt K4).
- **K1 — golden ma ≥ 1 znalezisko.** Baza i silnik są niespójne. Stop: najpierw poprawka
  bazy albo silnika, nowe przewidywanie dla L1. Pozostałe życia nie są liczone.
- **K2 — L1 lub L2 REFUTED (FN lub FP w wariantach A).** Błąd w regule. Poprawka reguły
  + test regresji, nowe przewidywanie. Bez tego żadna oferta nie mówi „wykrywa 10 typów”.
- **K3 — L3 REFUTED przez FP w B10 (plik typowany).** Silnik nie przyjmuje typowanych
  kolumn GPKG. Decyzja: warstwa normalizacji wejścia w v0.2.x z własnym przewidywaniem.
  Do tego czasu README i oferty nie twierdzą, że obsługują dowolny GPKG.
- **K4 — L3 CONFIRMED z FN = B9.** Przewidywanie trafione, luka potwierdzona: obwód
  z jednostką przechodzi po cichu. Decyzja: w v0.2.1 nowa informacja „obwód nieczytelny”
  (osobne przewidywanie). Opis luki do RULES.md od razu.
- **K5 — C REFUTED (przesunięcie o 1).** Próg działa inaczej niż w RULES.md. Poprawka kodu
  albo opisu, tak żeby oba mówiły to samo; test granic do `tests/`.
- **K6 — M REFUTED.** Źle przeczytałem kolejność reguł. Rzeczywistą kolejność zapisać
  w RULES.md (sekcja „kolejność sprawdzania”). Nie blokuje kroku 3.
- **K7 — maskowanie potwierdzone (M2, M4, M6).** Decyzja do podjęcia osobno, nie w v0.2a:
  czy silnik ma zgłaszać wszystkie błędy rekordu naraz. Do tego czasu RULES.md mówi
  wprost, że po R01, R02, R04, R05 sprawdzanie rekordu się kończy.

## 5. Co idzie do nauki

Każdy FN i FP z opisem przyczyny w `OUTCOME_v0_2a.md`; każda rozbieżność między
przewidywaniem a wynikiem jako osobny wpis, także gdy życie jest CONFIRMED
(np. trafne przewidywanie luki).

## 6. Kolejność pracy

1. Ten plik: commit, SHA-256, wpis `prediction` w Pulsie (`pl-drzewa`).
2. Dopiero potem: `tools/inject.py`, `truth.json`, skrypt pomiaru.
3. Pomiar L1–L4, `OUTCOME_v0_2a.md`, wpisy `life` w Pulsie.

---

## DE — Kurzfassung

Vorhersage vor dem Code für den Fehlerinjektor. Vier Leben: L1 golden + seed_A (13 Varianten,
erwartet 13/0/0), L2 seed_B (13/0/0), L3 echte Formatfehler aus Lieferungen (erwartet 4/1/0:
„45 cm“ beim Stammumfang wird still übergangen), L4 Schwellen und zwei Fehler pro Datensatz
(erwartet 11/3/0: nach R01, R02, R04 bricht die Prüfung des Datensatzes ab). Folgen K0–K7 sind
vor dem Ergebnis festgelegt.

## EN — Summary

Prediction written before the injector code. Four lives: L1 golden + seed_A (13 variants,
expected 13/0/0), L2 seed_B (13/0/0), L3 real format errors from deliveries (expected 4/1/0:
girth "45 cm" is silently skipped), L4 thresholds and two errors per record (expected 11/3/0:
the record check stops after R01, R02, R04). Consequences K0–K7 are fixed before the result.
