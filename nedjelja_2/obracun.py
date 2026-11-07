"""Pravila obračuna cijene jedne rezervacije."""

from modeli import Rezervacija

SEZONSKI_MJESECI = (7, 8)
SEZONSKO_POVECANJE = 1.3
NOCI_ZA_POPUST = 7
POPUST_DUGI_BORAVAK = 0.9


def izracunaj_iznos(rezervacija: Rezervacija) -> float:
    """Vraća iznos rezervacije sa sezonskim povećanjem i popustom za dugi boravak."""
    iznos = rezervacija.noci * rezervacija.cijena_noci
    if rezervacija.dolazak.month in SEZONSKI_MJESECI:
        iznos *= SEZONSKO_POVECANJE
    if rezervacija.noci >= NOCI_ZA_POPUST:
        iznos *= POPUST_DUGI_BORAVAK
    return round(iznos, 2)
