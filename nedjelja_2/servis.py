"""Servis koji povezuje izvor podataka, obračun i izvještavanje."""

from collections.abc import Sequence

from izvjestavanje import Izvjestavac
from izvori import IzvorRezervacija
from modeli import Izvjestaj, Rezervacija
from obracun import izracunaj_iznos


def sastavi_izvjestaj(rezervacije: Sequence[Rezervacija]) -> Izvjestaj:
    """Sabira iznose aktivnih rezervacija, ukupno i po tipu sobe."""
    po_tipu: dict[str, float] = {}
    aktivne = [r for r in rezervacije if not r.otkazana]
    for r in aktivne:
        po_tipu[r.tip_sobe] = round(
            po_tipu.get(r.tip_sobe, 0.0) + izracunaj_iznos(r), 2
        )
    return Izvjestaj(
        broj_rezervacija=len(aktivne),
        broj_otkazanih=len(rezervacije) - len(aktivne),
        ukupno=round(sum(po_tipu.values()), 2),
        po_tipu_sobe=po_tipu,
    )


class ObradaRezervacija:
    """Zavisi samo od apstrakcija (Protocol), a konkretne klase dobija spolja."""

    def __init__(
        self, izvor: IzvorRezervacija, izvjestavaci: Sequence[Izvjestavac]
    ) -> None:
        self.izvor = izvor
        self.izvjestavaci = list(izvjestavaci)

    def obradi(self) -> Izvjestaj:
        izvjestaj = sastavi_izvjestaj(self.izvor.ucitaj())
        for izvjestavac in self.izvjestavaci:
            izvjestavac.posalji(izvjestaj)
        return izvjestaj
