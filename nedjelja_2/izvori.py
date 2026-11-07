"""Izvori podataka o rezervacijama."""

import csv
from datetime import date
from pathlib import Path
from typing import Protocol

from modeli import Rezervacija


class IzvorRezervacija(Protocol):
    """Ugovor: sve što ume da vrati listu rezervacija."""

    def ucitaj(self) -> list[Rezervacija]: ...


def parsiraj_red(red: dict[str, str]) -> Rezervacija:
    """Pretvara jedan red CSV fajla u objekat Rezervacija."""
    return Rezervacija(
        gost=red["gost"],
        tip_sobe=red["tip_sobe"],
        dolazak=date.fromisoformat(red["dolazak"]),
        noci=int(red["noci"]),
        cijena_noci=float(red["cijena_noci"]),
        otkazana=red["status"] == "otkazana",
    )


class CsvIzvor:
    """Čita rezervacije iz CSV fajla sa zaglavljem."""

    def __init__(self, putanja: str | Path) -> None:
        self.putanja = Path(putanja)

    def ucitaj(self) -> list[Rezervacija]:
        with self.putanja.open(encoding="utf-8", newline="") as f:
            return [parsiraj_red(red) for red in csv.DictReader(f)]
