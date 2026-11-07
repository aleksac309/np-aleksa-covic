# ruff: noqa  # namjerno loš polazni kod, ostaje neizmijenjen radi poređenja
"""Polazni (monolitni) skript za obradu rezervacija.

Namjerno je napisan kao jedna funkcija koja radi sve: čita CSV fajl,
računa iznose, pravi izvještaj, upisuje ga u fajl i "šalje" mail.
Služi samo kao polazna tačka za refaktoring - ne mijenjati.
"""

import csv
from datetime import datetime


def obradi_rezervacije():
    ukupno = 0
    po_tipu = {}
    broj = 0
    otkazane = 0

    f = open("rezervacije.csv", encoding="utf-8")
    reader = csv.reader(f)
    next(reader)
    for red in reader:
        if red[5] == "otkazana":
            otkazane += 1
            continue
        dolazak = datetime.strptime(red[2], "%Y-%m-%d")
        noci = int(red[3])
        cijena = float(red[4])
        iznos = noci * cijena
        # sezona: jul i avgust su 30% skuplji
        if dolazak.month == 7 or dolazak.month == 8:
            iznos = iznos * 1.3
        # popust 10% za boravak od 7 i više noći
        if noci >= 7:
            iznos = iznos * 0.9
        ukupno += iznos
        if red[1] in po_tipu:
            po_tipu[red[1]] += iznos
        else:
            po_tipu[red[1]] = iznos
        broj += 1
    f.close()

    tekst = "IZVJESTAJ O REZERVACIJAMA\n"
    tekst += "Broj rezervacija: " + str(broj) + "\n"
    tekst += "Otkazane: " + str(otkazane) + "\n"
    for tip in po_tipu:
        tekst += tip + ": " + str(round(po_tipu[tip], 2)) + "\n"
    tekst += "Ukupno: " + str(round(ukupno, 2)) + "\n"

    open("izvjestaj.txt", "w").write(tekst)
    print("Mail poslat na recepcija@hotel.me")
    print(tekst)


obradi_rezervacije()
