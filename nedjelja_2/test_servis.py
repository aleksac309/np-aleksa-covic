from datetime import date

import pytest

from izvjestavanje import FajlIzvjestavac
from izvori import CsvIzvor
from modeli import Izvjestaj, Rezervacija
from obracun import izracunaj_iznos
from servis import ObradaRezervacija


class LazniIzvor:
    """Zamjenski izvor: vraća rezervacije iz memorije umjesto iz fajla."""

    def __init__(self, rezervacije: list[Rezervacija]) -> None:
        self.rezervacije = rezervacije

    def ucitaj(self) -> list[Rezervacija]:
        return self.rezervacije


class LazniIzvjestavac:
    """Zamjenski izvještavač: samo pamti šta je primio."""

    def __init__(self) -> None:
        self.primljeni: list[Izvjestaj] = []

    def posalji(self, izvjestaj: Izvjestaj) -> None:
        self.primljeni.append(izvjestaj)


def rez(
    tip: str = "dvokrevetna",
    mjesec: int = 3,
    noci: int = 2,
    cijena: float = 100,
    otkazana: bool = False,
) -> Rezervacija:
    return Rezervacija("Gost", tip, date(2026, mjesec, 1), noci, cijena, otkazana)


def obradi(rezervacije: list[Rezervacija]) -> tuple[Izvjestaj, LazniIzvjestavac]:
    izvjestavac = LazniIzvjestavac()
    izvjestaj = ObradaRezervacija(LazniIzvor(rezervacije), [izvjestavac]).obradi()
    return izvjestaj, izvjestavac


def test_otkazane_rezervacije_se_ne_racunaju():
    izvjestaj, _ = obradi([rez(), rez(otkazana=True)])
    assert izvjestaj.broj_rezervacija == 1
    assert izvjestaj.broj_otkazanih == 1
    assert izvjestaj.ukupno == pytest.approx(200)


def test_sezonsko_povecanje_i_popust_za_dugi_boravak():
    izvjestaj, _ = obradi([rez(mjesec=7, noci=2), rez(mjesec=3, noci=7)])
    # jul: 2 * 100 * 1.3 = 260; mart, 7 noći: 7 * 100 * 0.9 = 630
    assert izvjestaj.ukupno == pytest.approx(890)


def test_iznosi_se_grupisu_po_tipu_sobe():
    izvjestaj, _ = obradi(
        [rez("apartman", cijena=150), rez("apartman"), rez("jednokrevetna")]
    )
    assert izvjestaj.po_tipu_sobe == pytest.approx(
        {"apartman": 500, "jednokrevetna": 200}
    )


def test_prazan_izvor_daje_prazan_izvjestaj():
    izvjestaj, _ = obradi([])
    assert izvjestaj == Izvjestaj(0, 0, 0.0, {})


def test_izvjestavac_prima_isti_izvjestaj_koji_servis_vraca():
    izvjestaj, izvjestavac = obradi([rez()])
    assert izvjestavac.primljeni == [izvjestaj]


def test_sezona_i_popust_zajedno():
    # avgust, 10 noći: 10 * 100 * 1.3 * 0.9 = 1170
    assert izracunaj_iznos(rez(mjesec=8, noci=10)) == pytest.approx(1170)


def test_neispravan_broj_noci_se_odbija():
    with pytest.raises(ValueError):
        rez(noci=0)


def test_csv_izvor_i_fajl_izvjestavac(tmp_path):
    csv_fajl = tmp_path / "rez.csv"
    csv_fajl.write_text(
        "gost,tip_sobe,dolazak,noci,cijena_noci,status\n"
        "Ana,jednokrevetna,2026-03-12,3,50,potvrdjena\n"
        "Marko,dvokrevetna,2026-05-20,2,80,otkazana\n",
        encoding="utf-8",
    )
    izlaz = tmp_path / "izvjestaj.txt"
    ObradaRezervacija(CsvIzvor(csv_fajl), [FajlIzvjestavac(izlaz)]).obradi()
    tekst = izlaz.read_text(encoding="utf-8")
    assert "Broj rezervacija: 1" in tekst
    assert "Otkazane: 1" in tekst
    assert "Ukupno: 150.00" in tekst
