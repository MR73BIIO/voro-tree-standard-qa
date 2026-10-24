# Pakiet reguł: Warszawa, Standard 688/2025

Źródło: *Standard przeglądów i analiz dendrologicznych m.st. Warszawy*, załącznik do Zarządzenia nr 688/2025 Prezydenta m.st. Warszawy z 25.04.2025.
Quelle / Source: same document (Polish only).

Pola wejściowe / Eingabefelder / Input fields: `nr`, `klasa`, `uzytkowanie`, `data_ogledzin`, `data_kolejnych`, opcjonalnie `obwod` (cm na 130 cm) + geometria.

| ID | Waga | PL | DE | EN | Standard |
|---|---|---|---|---|---|
| R01 | błąd / ostrz. | Klasa ryzyka spoza 1–3 (4–5 = dawna skala, ostrzeżenie) | Risikoklasse außerhalb 1–3 (4–5 = alte Skala, Warnung) | Risk class outside 1–3 (4–5 = former scale, warning) | pkt 3.3, 4.1.2 |
| R02 | błąd | Klasa 2 lub 3 bez kategorii użytkowania O/N/S/W | Klasse 2 oder 3 ohne Nutzungskategorie | Class 2 or 3 without site use category | zał. 6, 7 |
| R03 | ostrz. | Klasa 1 z kategorią użytkowania | Klasse 1 mit Nutzungskategorie | Class 1 with a site use category | pkt 4.1.2, zał. 7 |
| R04 | błąd | Kategoria użytkowania spoza O/N/S/W | Nutzungskategorie außerhalb O/N/S/W | Site use category outside O/N/S/W | zał. 6 |
| R05 | błąd | Brak lub zły format daty (RRRR-MM-DD) | Datum fehlt oder falsches Format | Date missing or wrong format | zał. 2, 3 |
| R06 | błąd / info | Termin kolejnych oględzin niezgodny z macierzą (tolerancja 31 dni) | Nächste Kontrolle passt nicht zur Matrix (Toleranz 31 Tage) | Next inspection does not match the matrix (31-day tolerance) | zał. 7 |
| R07 | info | Obwód ≤ 60 cm: poza zakresem Standardu | Stammumfang ≤ 60 cm: außerhalb des Geltungsbereichs | Girth ≤ 60 cm: outside scope | pkt 3.2 |
| R08 | błąd / ostrz. | Geometria niezgodna z klasą: kl. 2–3 jako obszar (błąd), kl. 1 jako punkt (ostrz.) | Geometrie passt nicht zur Klasse | Geometry does not match the class | pkt 5.3.1 |
| R09 | błąd | Zdublowany numer inwentaryzacyjny | Doppelte Inventarnummer | Duplicate inventory number | zał. 3 |
| R10 | błąd | Brak numeru inwentaryzacyjnego | Inventarnummer fehlt | Inventory number missing | zał. 2, 3 |

## Macierz z załącznika 7 (miesiące)

| Klasa | O | N | S | W |
|---|---|---|---|---|
| 1 | 36 | 36 | 36 | 36 (bez kategorii) |
| 2 | 36 | 24 | 12 | 12 |
| 3 | 24 | 12 | 6 | 6 |

## Czego reguły nie sprawdzają

Samej oceny stanu zdrowotnego drzewa (zał. 5), poprawności gatunku, zdjęć ani arbotagów. To zostaje po stronie ogrodnika i dendrologa.
