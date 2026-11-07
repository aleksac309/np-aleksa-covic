import pytest

from prosjecna_cijena import prosjecna_cijena


def test_prosjecna_cijena():
    assert prosjecna_cijena([10, 20, 30]) == 20


def test_jedna_cijena():
    assert prosjecna_cijena([15]) == 15


def test_nulte_cijene():
    assert prosjecna_cijena([0, 0, 0]) == 0


def test_prazna_lista():
    with pytest.raises(ValueError):
        prosjecna_cijena([])
