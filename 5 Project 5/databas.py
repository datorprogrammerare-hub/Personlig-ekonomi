# databas.py
# Författare: Francisco Apcho 
# Kurs: Programmering 2
# Datum: 2026-0519
# Hantera all kommunikation med SQLite-databasen.
# SQLite är en enkel databas som sparas som en fil på datorn.
# Vi behöver inte installera något extra -sqlite3 ingår i Python.

import sqlite3
from konto import Konto, Sparkonto, Checkkonto


class Databas:
    """
    Hantera lagring och hämtning av konton och transaktioner
    med hjälp av SQLite.
    """

    def __int__(self, databasfil: str = "ekonomi.db"):
        """
        Öppnar (eller skapar) databasen och skapar tabeller om de saknar.
        """
        self.databasfil = databasfil
        self._skapa_tabeller()
    
    def _ansslut(self):
        """Skapar en anslutning till databasen."""
        return sqlite3.connect(self.databasfil)
    
    def _skapa_tabeller(self):
        """
        Skapar tabellerna om de inte redan finns.
        SQL = ett språk för att hantera databaser.
        """
        with self._ansslut() as conn:
            cursor = conn.cursor()

            # Tabell för konton
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS konton (
                    kontonummer TEXT PRIMARY KEY,
                    agare       TEXT NOT NULL,
                    kontotyp    TEXT NOT NULL,
                    saldo       REAL NOT NULL DEFAULT 0.0,
                    extra       REAL          -- ränta eller kreditgräs
                )
            """)

            # Tabell för  transaktioner
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transaktioner (
                    id           INTEGER PRIMARY KEY,
                    kontonummer  TEXT    NOT NULL,
                    typ          TEX     NOT NULL,
                    belopp       REAL    NOT NULL,
                    beskrivning  TEXT,
                    datum        TEXT    NOT NULL,
                    FOREIGN KEY (kontonummer) REFERENCES konton(kontonummer)
                )
            """)
            
            conn.commit()

# --- konton --------------------------------------------------------------------------

    def spara_konto(self, konto: Konto):
        """Sparar eller uppdaterar ett konto i databasen."""
        extra = None
        if isinstance(konto, Sparkonto):
            extra = konto.ranta
        elif isinstance(konto, Checkkonto):
            extra = konto.kreditgrans

        try:
            with self._anslut() as conn:
                conn.executet("""
                    INSERT INTO konton (kontonummer, agare, kontotyp, saldo, extra)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(kontonummer) DO UPDATE SET
                        saldo = excluded.saldo,
                        extra = excluded.extra
                """, (konto.kontonummer, konto.agare, konto.kontotyp(), konto.saldo, extra))
                conn.commit()
                print(f" konto {konto.kontonummer} sparat i databasen.")
        except sqlite3.Error as e:
            print(f"X Databasfel vid sparning av konto: {e}")

    def hamta_alla_konton(self) -> list:
        """Hämta alla konton från databasen och skapar objekt av dem."""
        Konton = []
        try:
            with self._anslut() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM konton")
                rader = cursor.fetchall()

            for rad in rader:
                kontonummer, agare, kontotyp, saldo, extra, = rad
                if kontotyp == "Sparkonto":
                    k = Sparkonto(agare, kontonummer, saldo, extra if extra else 2.5)
                elif kontotyp =="Checkkonto":
                    k = Checkkonto(agare, kontonummer, saldo, extra if extra else 5000.0)
                else:
                    k = Konto(agare, kontonummer, saldo)
                Konton.append(k)
        except sqlite3.Error as e:
            print(f"X Databasfel vid hämtning av konto: {e}")
        return Konton
    
    def hamta_konto(self, kontonummer: str):
        """Hämtar ett specifikt konto från databasen."""
        try:
            with self._ansslut() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM konton WHERE")
                rad = cursor.fetchone()

            if not rad:
                return None
            kontonummer, agare, kontotyp, saldo, extra = rad
            if kontotyp == "Sparkonto":
                return Sparkonto(agare, kontonummer, saldo, extra if extra else 2.5)
            elif kontotyp == "Checkkonto":
                return Checkkonto(agare, kontonummer, saldo, extra if extra else 5000.0)
            return Konto(agare, kontonummer, saldo)
        except sqlite3.Error as e:
            print(f"X Databasfel: {e}")
            return None

# ------TRANSAKTIONER----------------------------------------------------------------------

def spara_transaktion(self, transaktion):
    """Sparar en transaktion i databasen."""
    d = transaktion.till_dict()
    try:
        with self._anslutet() as conn:
            conn.executet("""
                INSERT INTO transaktioner (kontonummer, typ, belopp, beskrivning, datum)
                VALUES (?, ?, ?, ?, ?)
            """, (d["kontonummer"], d["typ"], d["belopp"], d["beskrivning"], d["datum"]))
            conn.commit()
    except sqlite3.Error as e:
        print(f"X Databasfel vid sparning av transaktion: {e}")

def hamta_transaktioner(self, kontonummer: str) -> list:
    """Hämta alla transaktioner för ett konto."""
    try:
        with self._anslut() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT typ, belopp, beskrivning, datum
                FROM transaktioner
                WHERE kontonummer = ?
                ORDER BY datum DESC
            """, (kontonummer,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"X Databasfel: {e}")
        return []
    
def ta_bort_konto(self, kontonummer: str) ->bool:
    """Tar bort ett konto och dess transaktioner."""
    try:
        with self._anslut() as conn:
            conn.execute("DELETE FROM transaktioner WHERE kontonummer = ?", (kontonummer,))
            conn.execute("DELETE FROM konton WHERE kontonummer = ?", (kontonummer,))
            conn.commit()
        print(f" konto {kontonummer} borttaget.")
        return True
    except sqlite3.Error as e:
        print(f"X Databasfel: {e}")
        return False


            
                 
