# Pomiar v0.2a (vtsqa 0.1.1)

| Zycie | Pliki | Prawda | Znalezione | TP / FN / FP | Przewidywane | FN (przypadek, regula) | Werdykt |
|---|---|---|---|---|---|---|---|
| L1 | golden.gpkg, seed_A.gpkg | 13 | 13 | 13 / 0 / 0 | 13 / 0 / 0 | — | **CONFIRMED** |
| L2 | seed_B.gpkg | 13 | 13 | 13 / 0 / 0 | 13 / 0 / 0 | — | **CONFIRMED** |
| L3 | seed_L3.gpkg, seed_L3_b10_typed.gpkg | 5 | 4 | 4 / 1 / 0 | 4 / 1 / 0 | B9:R07 | **CONFIRMED** |
| L4 | seed_L4.gpkg | 14 | 11 | 11 / 3 / 0 | 11 / 3 / 0 | M2:R06, M4:R05, M6:R08 | **CONFIRMED** |

## L3

- FN: `['F-014', 'R07', 'informacja']`

## L4

- FN: `['C-020', 'R06', 'blad']`
- FN: `['C-026', 'R05', 'blad']`
- FN: `['C-029', 'R08', 'blad']`
