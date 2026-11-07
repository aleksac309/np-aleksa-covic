# Napredno programiranje – Mini projekti

## Opis projekta

Ovaj repozitorijum koristi se za mini projekte iz predmeta Napredno programiranje.

## Mini projekat 1 – Priprema radnog okruženja

U okviru prvog zadatka implementirana je Python funkcija `prosjecna_cijena()` koja računa aritmetičku sredinu unijetih cijena.

## Korišćene tehnologije

- Python 3.12+
- Visual Studio Code
- pytest
- Ruff
- GitHub

## AI upit

Za generisanje funkcije korišćen je sljedeći upit:

"Napiši Python funkciju prosjecna_cijena koja prima listu brojeva i vraća njihovu prosječnu vrijednost. Obradi slučaj prazne liste."

## Uočeni nedostaci i ograničenja

- Funkcija ne provjerava da li su cijene negativne.
- Ne podržava vrijednosti zapisane kao stringovi.
- Koristi float, što može izazvati mala odstupanja pri računanju decimalnih vrijednosti.

## Testiranje

Za testiranje je korišćen pytest.

Pokretanje testova:
```
python -m pytest -v
```

Provjera kvaliteta koda:
```
ruff check .
```
