# transaktion.py
# Författare: FRancisco Apcho 
# Kurs: Programmering 2
# Datum: 2026-0519
# Klassen Transaktion representerar en enskild händelse på ett konto.
# Varje insättning, uttag eller räntebetalning sparas som ett Transaktion-objekt.

from datetime import datetime

class Transaktion:
    """
    Representerar en transaktion (insättning, uttag, ränta)

    Attribut:
        typ         : "insättning", "uttag" eller "ränta"
        belopp      : Hur mycket pengar (alltid positivt tal)
        kontonummer : Vilket konto transaktionen tillhör
        beskrivning : fritext-beskrivning
        datum       : Tidpunkt för transaktionen (sätts automatiskt)
    """
    def __init__(self, typ: str, belopp: float, kontonummer: str, beskrivning: str = ""):
        self.typ = typ
        self.belopp = belopp
        self.kontonummer = kontonummer
        self.beskrivning = beskrivning
        self.datum = datetime.now()  # Automatisk tidsstämpel

    def till_dict(self) -> dict:
        """
        Omvandlar transaktionen till en ordbok (dictionary).
        Används när vi sparar till databasen.
        """
        return {
            "typ": self.typ,
            "belopp": self.belopp,
            "kontonummer": self.kontonummer,
            "beskrivning": self.beskrivning,
            "datum": self.datum.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def __str__(self):
        """Gör att print(transaktion) ger läsbar text."""
        pil = "+" if self.typ == "insättning" or self.typ  == "ränta" else "-"
        return (
            f"{self.datum.strftime('%Y-%m-%d %H:%M')} |"
            f"{self.typ.capitalize():12} | "
            f"{pil}{self.belopp:>10.2f} kr |"
            f"{self.beskrivning}"
        )
 
    