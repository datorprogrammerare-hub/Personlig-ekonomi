# konto.py
# Författare: FRancisco Apcho 
# Kurs: Programmering 2
# Datum: 2026-0519
# Här definerar vi klassen konto (basklass) och två underklasser.
# Arv  = underklassen "ärver" allt från basklassen och kan lägga till mer.

from datetime import datetime

class Konto:
    """
    Basklass för alla typer av konton.
    Varje konto har: ägare, kontonummer, saldo och transaktioner.
    """

    def __init__(self, agare: str, kontonummer: str, saldo: float = 0.0 ):
        self.agare = agare
        self.kontonummer = kontonummer
        self.saldo = saldo
        self.transaktioner = []  # Lista med transaktion-objekt
    
    def satt_in(self, belopp:float, beskrivning: str = "Insättning") -> bool:
        """Sätter in pengar på kontot."""
        try:
            if belopp <= 0:
                raise ValueError("Beloppet måste vara posivit.")
            self.saldo += belopp
            self._registrera_transaktion("insättning", belopp, beskrivning)
            print(f" {belopp:.2f} kr satt in. Nytt saldo:{self.saldo:.2f} kr")
            return True
        except ValueError as e:
            print(f"X Fel:  {e}")
            return False
    
    def ta_ut(self, belopp: float, beskrivning: str = "Uttag") -> bool:
        """Tar ut pengar från kontot. Kan överskridas i underklasser."""
        try:
            if belopp <= 0:
                raise ValueError("Beloppet måste vara positivt.")
            if belopp > self.saldo:
                raise ValueError(f"Otillräckligt saldo. Tillgängligt: {self.saldo:.2f} Kr")
            self.saldo -= belopp
            self._registrera_transaktion("uttag", belopp, beskrivning)
            print(f" {belopp:.2f} Kr uttaget. Nytt saldo: {self.saldo:.2f} Kr")
            return True
        except ValueError as e:
            print(f"X Fel: {e}")
            return False
        
    def visa_saldo(self):
        """Skriver ut kontoinformation."""
        print(f"\n{'='*40}")
        print(f"Kontotyp:    {self.kontotyp()}")
        print(f"Ägare:       {self.agare}")
        print(f"Kontonummer: {self.kontonummer}")
        print(f"{'=*40'}")

    def kontotyp(self) -> str:
        """Polymorfism: varje underklass returnerar sin typ."""
        return "standardkonto"
    
    def _registrera_transaktion(self, typ: str, belopp: float, beskrivning: str):
        """Privat hjälpmetod för att lägga till en transaktion i listan."""
        from transaktion import Transaktion
        t = Transaktion(typ, belopp, self.kontonummer, beskrivning)
        self.transaktioner.append(t)

    def __str__(self):
        return f"{self.kontonummer()} [self.kontonummer] - {self.agare}: {self.saldo:.2f} kr"
    
# -------------------------------------------------------------------------------------
# UNDERKLASS 1: Spartkonto
# Ärver från Konto och lägger till räntafunktion
# -------------------------------------------------------------------------------------
class Sparkonto(Konto):
    """
    Sparkonto med ränta.
    Ärver allt från Konto + har en räntesats.
    """

    def __init__(self, agare: str, kontonummer: str, saldo: float = 0.0, ranta: float = 2.5):
        # Anropa basklassens __init__ med super()
        super().__init__(agare, kontonummer, saldo)
        self.ranta = ranta  # Räntasats i procent

    def kontotyp(self) -> str:
        """Överskriver basklassens metod -  detta är polymorfism."""
        return "Sparkonto"

    def berakna_ranta(self) -> float:
        """Beräknar och lägger till ärsränta på saldot."""
        rantebelopp = self.saldo * (self.ranta / 100)
        self.saldo += rantebelopp
        self._registrera_transaktion("ränta", rantebelopp, f"Årsränta {self.ranta}%")
        print(f"$ Ränta tillagd: {rantebelopp:.2f} kr ({self.ranta}%)")
        return rantebelopp
    
    def ta_ut(self, belopp: float, beskrivning: str = "Uttag") -> bool:
        """
        Överskriver ta_ut - sparkonto har en varning vid uttag.
        Polymorfism: samma metodnamn, men annat beteende.
        """
        print("  Observera: Uttag från sparkonto kan påverka din ränta.")
        return super().ta_ut(belopp, beskrivning)
    
    def visa_saldo(self):
        """Utökar basklassens metod med ränteinfo."""
        super().visa_saldo()
        print(f"Räntrsats:  {self.ranta}%")
        print(f"{'='*40}")

# --------------------------------------------------
# UNDERKLASS 2: Checkkonto
# Ärver från Konto och lägger till kreditgräns
# --------------------------------------------------
class Checkkonto(Konto):
    """
    Checkkonto med möjlighet till kredit (gå minus).
    """

    def __int__(self, agare: str, kontonummer: str, saldo: float = 0.0, kreditgrans: float = 5000.0):
        super().__init__(agare, kontonummer, saldo)
        self.kreditgrans = kreditgrans

    def kontotyp(self) -> str:
        return "Checkkonto"
    
    def ta_ut(self, belopp: float, beskrivning: str = "Uttag") -> bool:
        """
        Överskriver ta_ut - tillåter uttag upp till kreditgränsen.
        Polymorfism: annan logik för uttag än basklassen.
        """
        try:
            if belopp <= 0:
                raise ValueError("Beloppet måste vara positivt.")
            tillgangligt = self.saldo + self.kreditgrans
            if belopp > tillgangligt:
                raise ValueError(
                    f"Överskrider kreditgräns. Max tillgängligt: {tillgangligt:.2f} kr"
                )
            self.saldo -= belopp
            self._registrera_transaktion("uttag", belopp, beskrivning)
            print(f" {belopp:.2f} kr uttaget. Nytt saldo: {self.saldo:.2f} kr")
            if self.saldo < 0:
                print(f"  Kontot är {abs(self.saldo):.2f} kr i minus.")
            return True
        except ValueError as e:
            print(f"X Fel: {e}")
            return False
        
    def visa_saldo(self):
        super().visa_saldo()
        print(f"Kreditgräns: {self.kreditgrans:.2f} kr")
        print(f"{'='*40}")
    
