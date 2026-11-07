# Mini projekat 1 – Refaktoring obrade rezervacija

## Opis

Polazni skript `monolit.py` je jedna funkcija koja radi sve: čita `rezervacije.csv`,
računa iznos svake rezervacije (sezonsko povećanje od 30% za jul i avgust, popust od 10%
za boravak od 7 i više noći), preskače otkazane rezervacije, sabira iznose po tipu sobe,
upisuje izvještaj u `izvjestaj.txt` i "šalje mail" ispisom na konzolu.

Problemi polaznog skripta:

- **S (Single Responsibility):** jedna funkcija čita fajl, računa, formatira, upisuje i šalje.
  Svaka izmjena (novi format, novo pravilo cijene, novi kanal slanja) mijenja istu funkciju.
- **D (Dependency Inversion):** putanje `rezervacije.csv` i `izvjestaj.txt` su ugrađene u kod,
  pa se logika ne može testirati bez pravih fajlova.
- Fajlovi se otvaraju bez `with`, kolone se čitaju po indeksu (`red[5]`), nema tipova,
  a skript se izvršava čim se importuje.

## Struktura nakon refaktoringa

| Fajl | Odgovornost |
|---|---|
| `modeli.py` | `Rezervacija` i `Izvjestaj` (`@dataclass(frozen=True)`), validacija noćenja i cijene |
| `obracun.py` | `izracunaj_iznos()` – pravila cijene (sezona, popust) |
| `izvori.py` | Protocol `IzvorRezervacija` + implementacija `CsvIzvor` |
| `izvjestavanje.py` | Protocol `Izvjestavac`, `formatiraj()`, `KonzolniIzvjestavac`, `FajlIzvjestavac` |
| `servis.py` | `sastavi_izvjestaj()` i `ObradaRezervacija` koja povezuje izvor i izvještavače |
| `main.py` | jedino mjesto gdje se biraju konkretne klase (CSV, konzola, fajl) |
| `test_servis.py` | pytest testovi sa zamjenskim izvorom i izvještavačem |

**Princip S:** svaki modul ima jedan razlog za promjenu – novo pravilo cijene mijenja samo
`obracun.py`, novi format izvještaja samo `izvjestavanje.py`, novi izvor podataka samo `izvori.py`.

**Princip D:** `ObradaRezervacija` ne zna za CSV niti za fajlove. Kroz konstruktor prima
bilo šta što zadovoljava `IzvorRezervacija` (ima metodu `ucitaj()`) i listu objekata
koji zadovoljavaju `Izvjestavac` (imaju metodu `posalji()`). Zbog toga se u testovima
umjesto CSV fajla koristi `LazniIzvor` sa podacima iz memorije, a novi izvor
(npr. baza ili API) dodaje se bez izmjene servisa (princip O).

```python
servis = ObradaRezervacija(
    izvor=CsvIzvor("rezervacije.csv"),
    izvjestavaci=[KonzolniIzvjestavac(), FajlIzvjestavac("izvjestaj.txt")],
)
servis.obradi()
```

## Pokretanje

```
pip install -r requirements.txt
python main.py          # refaktorisana verzija
python monolit.py       # polazna verzija, za poređenje
python -m pytest -v
ruff check .
```

Obje verzije nad `rezervacije.csv` daju isti rezultat (5 rezervacija, 1 otkazana, ukupno 2508.80).

## Testovi

Testovi u `test_servis.py` koriste `LazniIzvor` (vraća listu rezervacija iz memorije)
i `LazniIzvjestavac` (pamti primljene izvještaje), pa ne zavise od fajlova:

- otkazane rezervacije se ne računaju u ukupan iznos,
- sezonsko povećanje i popust za dugi boravak, pojedinačno i zajedno,
- grupisanje iznosa po tipu sobe,
- prazan izvor daje prazan izvještaj,
- izvještavač dobija isti izvještaj koji servis vraća,
- `Rezervacija` odbija broj noćenja manji od 1,
- jedan integracioni test za `CsvIzvor` i `FajlIzvjestavac` preko privremenih fajlova (`tmp_path`).

## Rad sa AI asistentom

Korišćen je Claude Code (Claude Opus 5.5).

### Upotrijebljeni upiti

1. Upit za izradu rješenja (tekst zadatka iz prezentacije za nedjelju 2):

   > U podfolderu nedjelja_2/ uradi ovaj zadatak: Preuzeti dati monolitni skript za obradu
   > rezervacija (ili koristiti vlastiti). Refaktorisati ga u klase i funkcije primjenom
   > principa S i D. Uvesti Protocol za izvor podataka i za izvještavanje. Napisati najmanje
   > tri pytest testa sa zamjenskim izvorom podataka. U README-u navesti upotrijebljene upite
   > i ispravke generisanog koda. [...] Dati skript ne postoji, treba izmisliti svoj skript
   > koji radi nešto za rezervacije.

2. Upit za pregled dizajna (predložen na slajdu 16 prezentacije):

   > Uloga: iskusni softverski arhitekta. Zadatak: analizirati priloženi Python kod.
   > 1. Navesti narušene SOLID principe, sa brojem linije. 2. Objasniti praktičnu posljedicu
   > svakog narušavanja. 3. Predložiti refaktoring uz kratak primjer. 4. Predložiti tri testa
   > koja potvrđuju da se ponašanje nije promijenilo.
   > Ograničenje: ne uvoditi apstrakcije koje problem ne zahtijeva.

### Ispravke i provjera generisanog koda

- **Ruff je prijavio greške u `monolit.py`** (otvaranje fajla bez `with`, iteracija kroz
  rječnik bez `.items()`). Polazni skript je namjerno ostavljen loš radi poređenja, pa je
  na vrh dodat `# ruff: noqa`, a ispravke su urađene samo u refaktorisanom kodu.
- **Preduge linije** u `servis.py` i `test_servis.py` preformatirane su sa `ruff format`.
- **Zaokruživanje:** monolit zaokružuje tek na kraju, a nova verzija zaokružuje iznos
  svake rezervacije. To može dati razliku od jednog centa, pa je ručno provjereno da obje
  verzije nad datim podacima daju isti izvještaj.
- **Ograničavanje apstrakcija (YAGNI):** pravila cijene su ostala obična funkcija, a ne
  hijerarhija klasa `Tarifa`, jer zadatak traži Protocol samo za izvor i izvještavanje.
- **Tipovi:** kod je provjeren sa `mypy --strict` bez grešaka.

## Ograničenja

- Iznosi se računaju u `float`; za stvarni novac bolje je koristiti `decimal.Decimal`.
- Sezona se određuje samo po datumu dolaska, a ne po svakoj noći boravka.
- "Slanje maila" je ispis na konzolu; pravi mail bio bi nova klasa koja implementira `Izvjestavac`.
