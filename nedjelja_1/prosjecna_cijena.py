def prosjecna_cijena(cijene: list[float]) -> float:
    if len(cijene) == 0:
        raise ValueError("Lista cijena ne smije biti prazna.")

    return sum(cijene) / len(cijene)


cijene = [10, 20, 30, 40]
print(prosjecna_cijena(cijene))
