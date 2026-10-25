[English](README.md) | **Polski** | [Deutsch](README.de.md)

# VORO Tree Standard QA

[![tests](https://github.com/MR73BIIO/voro-tree-standard-qa/actions/workflows/tests.yml/badge.svg)](https://github.com/MR73BIIO/voro-tree-standard-qa/actions/workflows/tests.yml)
![python](https://img.shields.io/badge/python-3.10%2B-2f6b4a)
![license](https://img.shields.io/badge/license-GPL--2.0--or--later-2f6b4a)
![rules](https://img.shields.io/badge/pakiet%20regu%C5%82-Warszawa%20688%2F2025-2f6b4a)
[![DOI](https://zenodo.org/badge/1432513049.svg)](https://doi.org/10.5281/zenodo.23624898)

**Sprawdza dane z inwentaryzacji drzew względem standardu zamawiającego, zanim pójdą do odbioru, i pokazuje każdy problem na mapie.**

![Znaleziska na pliku syntetycznym](docs/findings_map.png)

Inwentaryzację drzew oddaje się jako GeoPackage i zwykle sprawdza się ją na oko. To narzędzie zamienia standard zamawiającego na reguły, które działają za każdym razem tak samo: te same dane, ten sam wynik, z odwołaniem do konkretnego punktu. Pierwszy pakiet reguł to warszawski *Standard przeglądów i analiz dendrologicznych* (Zarządzenie 688/2025).

Strona (kalkulator i kontrola tabeli, PL/DE/EN): https://mr73biio.github.io/voro-tree-standard-qa/

## Co sprawdza

10 reguł, opis w [rules/warszawa_688/RULES.md](rules/warszawa_688/RULES.md):

- klasa ryzyka 1–3 (dawna skala 5-stopniowa oznaczona),
- kategoria użytkowania terenu O/N/S/W tam, gdzie Standard jej wymaga, i jej brak tam, gdzie jej nie przewiduje,
- termin kolejnych oględzin względem macierzy z załącznika 7,
- typ geometrii względem klasy (klasa 1 jako obszar, klasy 2 i 3 jako punkty),
- brak lub dubel numeru inwentaryzacyjnego, błędne daty, obwód ≤ 60 cm.

Każde znalezisko ma wagę (błąd, ostrzeżenie, informacja), komunikat po polsku, niemiecku i angielsku oraz odwołanie do Standardu.

## Szybki start

```bash
git clone https://github.com/MR73BIIO/voro-tree-standard-qa.git
cd voro-tree-standard-qa
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
python tools/make_sample.py
vtsqa data/sample/rembertow_syntetyczne.gpkg --lang pl
```

Wynik: `rembertow_syntetyczne_findings.gpkg` (warstwa `findings`) i raport `rembertow_syntetyczne_findings.pl.md`.

Na pliku syntetycznym: 30 drzew, 7 błędów, 3 ostrzeżenia, 1 informacja. Wszystkie 11 celowo wstawionych błędów wykryte, bez fałszywych alarmów.

### Jako bramka jakości

```bash
vtsqa dostawa.gpkg --fail-on blad
```

Kod wyjścia 1, gdy jest choć jeden błąd. Kontrolę można więc wpiąć w proces i zatrzymać dane, zanim wyjdą.

## W QGIS

1. Dodaj warstwę `drzewa` z `data/sample/rembertow_syntetyczne.gpkg`.
2. Dodaj warstwę `findings` z pliku wynikowego.
3. Na `findings`: Właściwości → Styl → Styl → Wczytaj styl → `qgis/findings.qml`.

Czerwone kółka to błędy, żółte trójkąty ostrzeżenia, niebieskie kwadraty informacje. Po najechaniu na punkt widać komunikat w PL, DE i EN oraz punkt Standardu.

## Dane przykładowe

`data/sample/rembertow_syntetyczne.gpkg` to dane **syntetyczne**: 30 drzew rozmieszczonych w okolicy ul. Grawerskiej w Rembertowie, atrybuty wymyślone, 11 celowo wstawionych błędów. To nie są dane m.st. Warszawy. Każdy rekord ma `zrodlo = SYNTETYCZNE`. Rozpoznanie danych publicznych: [rules/warszawa_688/R0.md](rules/warszawa_688/R0.md).

## Czego nie robi

Nie ocenia stanu zdrowotnego drzewa i nie zastępuje ogrodnika ani dendrologa. Sprawdza, czy zapisy są zgodne z regułami Standardu.

## Stan

Wersja 0.2.0. Pierwsze zmierzone życia (v0.2a): 4 uruchomienia na zestawach wstrzykniętych błędów, 4/4 CONFIRMED, wyniki w [OUTCOME_v0_2a.md](OUTCOME_v0_2a.md); znane ograniczenia w [RULES.md](rules/warszawa_688/RULES.md). Kolejne etapy i kryteria ich zamknięcia: [ROADMAP.md](ROADMAP.md). Zmiany: [CHANGELOG.md](CHANGELOG.md).

## Licencja

Kod: GPL-2.0-or-later ([LICENSE](LICENSE)). Dane przykładowe, opis reguł, styl QGIS i dokumentacja: CC BY 4.0 ([LICENSE-DATA.md](LICENSE-DATA.md)). Jak cytować: [CITATION.cff](CITATION.cff).

---

Marcin Ruszczak (MR73BIIO) · ORCID [0009-0004-0170-4277](https://orcid.org/0009-0004-0170-4277) · polski · niemiecki · rosyjski · angielski
