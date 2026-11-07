"""Formatiranje i slanje izvještaja."""

from pathlib import Path
from typing import Protocol

from modeli import Izvjestaj


class Izvjestavac(Protocol):
    """Ugovor: sve što ume da primi gotov izvještaj i nekud ga proslijedi."""

    def posalji(self, izvjestaj: Izvjestaj) -> None: ...


def formatiraj(izvjestaj: Izvjestaj) -> str:
    """Pretvara izvještaj u čitljiv tekst."""
    linije = [
        "IZVJESTAJ O REZERVACIJAMA",
        f"Broj rezervacija: {izvjestaj.broj_rezervacija}",
        f"Otkazane: {izvjestaj.broj_otkazanih}",
    ]
    for tip, iznos in izvjestaj.po_tipu_sobe.items():
        linije.append(f"{tip}: {iznos:.2f}")
    linije.append(f"Ukupno: {izvjestaj.ukupno:.2f}")
    return "\n".join(linije) + "\n"


class KonzolniIzvjestavac:
    """Ispisuje izvještaj na standardni izlaz."""

    def posalji(self, izvjestaj: Izvjestaj) -> None:
        print(formatiraj(izvjestaj))


class FajlIzvjestavac:
    """Upisuje izvještaj u tekstualni fajl."""

    def __init__(self, putanja: str | Path) -> None:
        self.putanja = Path(putanja)

    def posalji(self, izvjestaj: Izvjestaj) -> None:
        self.putanja.write_text(formatiraj(izvjestaj), encoding="utf-8")
