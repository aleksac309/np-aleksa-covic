"""Ulazna tačka: ovdje se biraju konkretne implementacije i povezuju u servis."""

from pathlib import Path

from izvjestavanje import FajlIzvjestavac, KonzolniIzvjestavac
from izvori import CsvIzvor
from servis import ObradaRezervacija

FOLDER = Path(__file__).parent


def main() -> None:
    servis = ObradaRezervacija(
        izvor=CsvIzvor(FOLDER / "rezervacije.csv"),
        izvjestavaci=[KonzolniIzvjestavac(), FajlIzvjestavac(FOLDER / "izvjestaj.txt")],
    )
    servis.obradi()


if __name__ == "__main__":
    main()
