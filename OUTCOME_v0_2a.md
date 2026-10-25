# OUTCOME v0.2a — voro-tree-standard-qa

Przewidywanie: `PREDICTION_v0_2a.md`, sha256 `2820f2f8556fd59dedd9c7d5aff813278939b850d5b802eaa8016443bec35da5`, Puls #56 (25.10.2026 13:11).
Dane i kod pomiaru zacommitowane przed pomiarem: `9a39db5` (`tools/inject.py`, `tools/measure.py`, `data/v0_2a/`).
Pomiar: 25.10.2026 ~13:15, `python tools/measure.py`, vtsqa 0.1.1, uruchomienie przez CLI (odczyt GPKG jak u klienta).
Surowy wynik: `results/v0_2a/outcome.json`, `results/v0_2a/outcome.md`.

## Wynik

| Życie | Zbiór | Prawda | TP / FN / FP | Przewidywane | Werdykt |
|---|---|---|---|---|---|
| L1 | golden + seed_A (13 wariantów reguł) | 0 + 13 | 13 / 0 / 0 | 13 / 0 / 0 | **CONFIRMED** |
| L2 | seed_B (ten sam skład, inny seed) | 13 | 13 / 0 / 0 | 13 / 0 / 0 | **CONFIRMED** |
| L3 | błędy formatu z dostaw B1–B9 + plik typowany B10 | 5 | 4 / 1 / 0 (FN: B9) | 4 / 1 / 0 (FN: B9) | **CONFIRMED** |
| L4 | granice C1–C4 + dwa błędy w rekordzie M1–M6 | 14 | 11 / 3 / 0 (FN: M2, M4, M6) | 11 / 3 / 0 (FN: M2, M4, M6) | **CONFIRMED** |

Fałszywe alarmy: 0 we wszystkich plikach (150 rekordów w 5 plikach + 30 w pliku typowanym).

## Konsekwencje (z pieczęci)

- **K0** — cztery życia CONFIRMED. Następna decyzja: domena VORO `trees_688` i providery (krok 3 ROADMAP v0.2a).
- **K4** — luka B9 potwierdzona (obwód `45 cm` pomijany bez komunikatu). Opis w `rules/warszawa_688/RULES.md` od dziś; poprawka w v0.2.1 z osobnym przewidywaniem.
- **K7** — maskowanie potwierdzone (M2, M4, M6). RULES.md opisuje kolejność sprawdzania i wczesne wyjścia. Decyzja „zgłaszać wszystkie błędy rekordu” — osobno, nie w v0.2a.
- K1, K2, K3, K5, K6 — nie zaszły. W szczególności K3: plik GPKG z kolumnami typowanymi przeszedł bez fałszywych alarmów.

## Nauka

1. Przewidywanie z czytania kodu trafiło w 4 z 4 życiach, łącznie z dwiema lukami. Trafność dotyczy kodu, który znam; prawdziwa dostawa wykonawcy może mieć formaty spoza B1–B10.
2. M1 (klasa 7 + obwód 45) daje oba znaleziska, bo R07 jest sprawdzane przed R01 — kolejność reguł nie jest „od najważniejszej”.
3. Wstrzykiwacz w pierwszej wersji zapisywał daty pliku B10 jako tekst. Wykryte przy kontroli plików przed commitem, poprawione przed pomiarem. Kontrola typów kolumn zostaje stałym krokiem.

---

**DE:** Vier Leben, alle CONFIRMED (13/0/0, 13/0/0, 4/1/0, 11/3/0), 0 Fehlalarme. Bestätigte Lücken: Stammumfang „45 cm“ wird still übergangen; nach R01, R02, R04, R05 endet die Prüfung des Datensatzes.

**EN:** Four lives, all CONFIRMED (13/0/0, 13/0/0, 4/1/0, 11/3/0), 0 false alarms. Confirmed gaps: girth "45 cm" is skipped silently; the record check stops after R01, R02, R04, R05.
