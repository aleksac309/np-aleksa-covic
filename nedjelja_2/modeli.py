"""Domenski modeli: podaci o rezervaciji i o izvještaju."""

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Rezervacija:
    gost: str
    tip_sobe: str
    dolazak: date
    noci: int
    cijena_noci: float
    otkazana: bool = False

    def __post_init__(self) -> None:
        if self.noci <= 0:
            raise ValueError("Broj noćenja mora biti pozitivan.")
        if self.cijena_noci < 0:
            raise ValueError("Cijena noćenja ne smije biti negativna.")


@dataclass(frozen=True)
class Izvjestaj:
    broj_rezervacija: int
    broj_otkazanih: int
    ukupno: float
    po_tipu_sobe: dict[str, float] = field(default_factory=dict)
