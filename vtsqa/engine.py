"""Silnik reguł: kontrola danych drzew względem Standardu 688/2025 m.st. Warszawy.

Wejście: warstwa drzew (GeoPackage) z polami
    nr, klasa, uzytkowanie, data_ogledzin, data_kolejnych, [obwod]
Wyjście: lista znalezisk (finding) z wagą, komunikatem PL/DE/EN i odwołaniem do Standardu.
"""
from __future__ import annotations

import calendar
import datetime as dt
import re
from dataclasses import dataclass, field

REQUIRED_FIELDS = ["nr", "klasa", "uzytkowanie", "data_ogledzin", "data_kolejnych"]

# Załącznik 7: częstotliwość oględzin w miesiącach
MATRIX = {
    2: {"O": 36, "N": 24, "S": 12, "W": 12},
    3: {"O": 24, "N": 12, "S": 6, "W": 6},
}
CLASS1_MONTHS = 36
TOLERANCE_DAYS = 31

SEVERITY_ORDER = {"blad": 0, "ostrzezenie": 1, "informacja": 2}


def period_months(klasa: int, uz: str | None) -> int | None:
    if klasa == 1:
        return CLASS1_MONTHS
    return MATRIX.get(klasa, {}).get(uz or "")


def years_label(months: int, lang: str) -> str:
    labels = {
        "pl": {6: "0,5 roku", 12: "1 rok"},
        "de": {6: "0,5 Jahre", 12: "1 Jahr"},
        "en": {6: "0.5 year", 12: "1 year"},
    }
    if months in labels[lang]:
        return labels[lang][months]
    n = months // 12
    return {"pl": f"{n} lata", "de": f"{n} Jahre", "en": f"{n} years"}[lang]


def add_months(d: dt.date, n: int) -> dt.date:
    y, m = divmod(d.month - 1 + n, 12)
    year, month = d.year + y, m + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return dt.date(year, month, day)


def parse_date(value) -> dt.date | None:
    if value is None:
        return None
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    s = str(value).strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return None
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        return None


def _txt(value) -> str:
    if value is None:
        return ""
    s = str(value).strip()
    return "" if s.lower() in ("nan", "none") else s


@dataclass
class Finding:
    nr: str
    rule: str
    severity: str  # blad | ostrzezenie | informacja
    msg: dict = field(default_factory=dict)  # {"pl":..., "de":..., "en":...}
    ref: str = ""


def _f(nr, rule, sev, ref, pl, de, en):
    return Finding(nr=nr, rule=rule, severity=sev, msg={"pl": pl, "de": de, "en": en}, ref=ref)


def check_record(rec: dict, geom_type: str | None = None) -> list[Finding]:
    """Sprawdza jeden rekord. geom_type: 'Point', 'Polygon', 'MultiPolygon'... albo None."""
    out: list[Finding] = []
    nr = _txt(rec.get("nr"))
    label = nr or f"#{rec.get('_row', '?')}"

    # R10: brak numeru inwentaryzacyjnego
    if not nr:
        out.append(_f(label, "R10", "blad", "zał. 2, zał. 3",
                      "Brak numeru inwentaryzacyjnego.",
                      "Inventarnummer fehlt.",
                      "Inventory number is missing."))

    # R07: obwód ≤ 60 cm
    ob_raw = _txt(rec.get("obwod")).replace(",", ".")
    if ob_raw:
        try:
            ob = float(ob_raw)
            if ob <= 60:
                out.append(_f(label, "R07", "informacja", "pkt 3.2",
                              f"Obwód {ob:g} cm (≤ 60 cm na wysokości 130 cm): drzewo poza zakresem Standardu, chyba że zakwalifikowano je indywidualnie.",
                              f"Stammumfang {ob:g} cm (≤ 60 cm in 130 cm Höhe): außerhalb des Geltungsbereichs, sofern nicht einzeln einbezogen.",
                              f"Girth {ob:g} cm (≤ 60 cm at 130 cm): outside the Standard's scope unless included individually."))
        except ValueError:
            pass

    # R01: klasa ryzyka
    k_raw = _txt(rec.get("klasa"))
    if k_raw.endswith(".0"):
        k_raw = k_raw[:-2]
    if not re.fullmatch(r"[1-5]", k_raw):
        out.append(_f(label, "R01", "blad", "pkt 4.1.2",
                      f"Klasa „{k_raw or 'brak'}” spoza dozwolonych wartości 1–3.",
                      f"Klasse „{k_raw or 'leer'}“ liegt außerhalb der zulässigen Werte 1–3.",
                      f"Class \"{k_raw or 'empty'}\" is outside the allowed values 1–3."))
        return out
    k = int(k_raw)
    if k > 3:
        out.append(_f(label, "R01", "ostrzezenie", "pkt 3.3",
                      f"Klasa {k} pochodzi z dawnej skali 5-stopniowej. Termin z poprzedniej metody obowiązuje do kolejnych oględzin, potem trzeba nadać klasę 1–3.",
                      f"Klasse {k} stammt aus der früheren 5-stufigen Skala. Der alte Termin gilt bis zur nächsten Kontrolle, danach ist eine Klasse 1–3 zu vergeben.",
                      f"Class {k} comes from the former 5-level scale. The old date applies until the next inspection, then a class 1–3 must be assigned."))
        return out

    # R08: typ geometrii względem klasy (pkt 5.3.1)
    if geom_type:
        is_area = geom_type in ("Polygon", "MultiPolygon")
        is_point = geom_type in ("Point", "MultiPoint")
        if k == 1 and is_point:
            out.append(_f(label, "R08", "ostrzezenie", "pkt 5.3.1",
                          "Klasa 1 zapisana jako punkt. Standard dokumentuje drzewa umiarkowanego ryzyka jako obszar.",
                          "Klasse 1 als Punkt erfasst. Der Standard dokumentiert Bäume mit mäßigem Risiko als Fläche.",
                          "Class 1 recorded as a point. The Standard records moderate-risk trees as an area."))
        if k in (2, 3) and is_area:
            out.append(_f(label, "R08", "blad", "pkt 5.3.1",
                          f"Klasa {k} zapisana jako obszar. Drzewa klas 2 i 3 inwentaryzuje się punktowo.",
                          f"Klasse {k} als Fläche erfasst. Bäume der Klassen 2 und 3 werden als Einzelpunkte erfasst.",
                          f"Class {k} recorded as an area. Class 2 and 3 trees must be recorded as individual points."))

    uz = _txt(rec.get("uzytkowanie")).upper()
    # R03: klasa 1 z kategorią użytkowania
    if k == 1 and uz:
        out.append(_f(label, "R03", "ostrzezenie", "pkt 4.1.2, zał. 7",
                      f"Klasa 1 ma kategorię użytkowania „{uz}”. Standard nie przypisuje jej drzewom umiarkowanego ryzyka.",
                      f"Klasse 1 hat die Nutzungskategorie „{uz}“. Der Standard sieht für Bäume mit mäßigem Risiko keine vor.",
                      f"Class 1 has site use category \"{uz}\". The Standard assigns none to moderate-risk trees."))
    # R02: klasa 2/3 bez kategorii
    if k > 1 and not uz:
        out.append(_f(label, "R02", "blad", "zał. 6, zał. 7",
                      f"Klasa {k} bez kategorii użytkowania terenu (O/N/S/W). Nie da się wyznaczyć terminu.",
                      f"Klasse {k} ohne Nutzungskategorie (O/N/S/W). Das Intervall lässt sich nicht bestimmen.",
                      f"Class {k} has no site use category (O/N/S/W). The interval cannot be set."))
        return out
    # R04: dozwolone kategorie
    if k > 1 and uz not in MATRIX[k]:
        out.append(_f(label, "R04", "blad", "zał. 6",
                      f"Nieznana kategoria użytkowania „{uz}”. Dozwolone: O, N, S, W.",
                      f"Unbekannte Nutzungskategorie „{uz}“. Zulässig: O, N, S, W.",
                      f"Unknown site use category \"{uz}\". Allowed: O, N, S, W."))
        return out

    # R05: daty
    d0, d1 = parse_date(rec.get("data_ogledzin")), parse_date(rec.get("data_kolejnych"))
    if d0 is None:
        out.append(_f(label, "R05", "blad", "zał. 2, zał. 3",
                      "Brak lub błędny format daty oględzin (wymagane RRRR-MM-DD).",
                      "Kontrolldatum fehlt oder hat ein falsches Format (JJJJ-MM-TT).",
                      "Inspection date missing or in the wrong format (YYYY-MM-DD)."))
        return out
    if d1 is None:
        out.append(_f(label, "R05", "blad", "zał. 2, zał. 3",
                      "Brak lub błędny format daty kolejnych oględzin (wymagane RRRR-MM-DD).",
                      "Datum der nächsten Kontrolle fehlt oder hat ein falsches Format (JJJJ-MM-TT).",
                      "Next inspection date missing or in the wrong format (YYYY-MM-DD)."))
        return out

    # R06: termin zgodny z macierzą z zał. 7
    m = period_months(k, uz)
    exp = add_months(d0, m)
    diff = (d1 - exp).days
    cls = f"{k} / {uz}" if k > 1 else "1"
    if diff > TOLERANCE_DAYS:
        out.append(_f(label, "R06", "blad", "zał. 7",
                      f"Termin kolejnych oględzin {d1} jest późniejszy niż wymagany {exp} ({years_label(m, 'pl')} dla klasy {cls}).",
                      f"Nächste Kontrolle am {d1} liegt nach dem geforderten Termin {exp} ({years_label(m, 'de')} für Klasse {cls}).",
                      f"Next inspection {d1} is later than the required {exp} ({years_label(m, 'en')} for class {cls})."))
    elif diff < -TOLERANCE_DAYS:
        out.append(_f(label, "R06", "informacja", "zał. 7, pkt 5.3",
                      f"Termin {d1} jest wcześniejszy niż wymagany {exp}. To dopuszczalne, ale warto sprawdzić, czy nie wynika z pomyłki.",
                      f"Termin {d1} liegt vor dem geforderten {exp}. Zulässig, aber prüfen, ob kein Eingabefehler vorliegt.",
                      f"Date {d1} is earlier than the required {exp}. Allowed, but check it is not a typo."))
    return out


def check_records(records: list[dict], geom_types: list[str | None] | None = None) -> list[Finding]:
    """Sprawdza wszystkie rekordy, łącznie z regułą R09 (duplikaty numerów)."""
    geom_types = geom_types or [None] * len(records)
    findings: list[Finding] = []
    seen: dict[str, int] = {}
    for rec in records:
        nr = _txt(rec.get("nr"))
        if nr:
            seen[nr] = seen.get(nr, 0) + 1
    for nr, n in seen.items():
        if n > 1:
            findings.append(_f(nr, "R09", "blad", "zał. 3",
                               f"Numer inwentaryzacyjny {nr} występuje {n} razy.",
                               f"Inventarnummer {nr} kommt {n}-mal vor.",
                               f"Inventory number {nr} appears {n} times."))
    for rec, gt in zip(records, geom_types):
        findings.extend(check_record(rec, gt))
    findings.sort(key=lambda f: (SEVERITY_ORDER[f.severity], f.rule, f.nr))
    return findings
