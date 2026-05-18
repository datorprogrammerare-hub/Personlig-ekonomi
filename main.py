# main.py
# Författare: Francisco Apcho 
# Kurs: Programmering 2
# Datum: 2026-0519
# Huvudprohtammet. Här körs allt.
# Meny-driven: användaren väljer vad de vill göra.

from konto import Konto, Sparkonto, Checkkonto
from databas import Databas
from valuta import hamta_valutakurser, visa_valutameny

def skriv_rubrik():
    print("\n" + "="*50)
    print("         PERSONLIG EKONOMI - Francisco Apcho ")
    print("="*50)

def skapa_kontonummer(db: Databas)  -> str:
    """Generar ett unikt kontonummer."""
    befintliga = {k.kontonummer for k in db.hamta_alla_konton()}
    nummer = 1000
    while f"KTO-{nummer}" in befintliga:
        nummer += 1
    return f"KTO-{nummer}"

def skapa_konto_meny(db: Databas):
    """Guidar användaren att skapa ett nytt konto."""
    print("\n--- SKAPA NYTT KONTO ---")
    agare = input("Ägarens namn: ").strip()
    if not agare:
        print(" X Namn kan inte vara tomt.")
        return
    
    print("\nVälja kontotyp:")
    print("  1. Sparkonto (med ränta)")
    print("  2. Checkkonto (med kreditgräns)")
    val = input("Ditt val (1/2): ").strip()

    kontonummer = skapa_kontonummer(db)

    try:
        if val == "1":
            ranta = float(input("Räntesats i % (standard 2.5): ") or "2.5")
            Konto = Sparkonto(agare, kontonummer, ranta=ranta)
        elif val == "2":
            kredit = float(input("Kreditgräns i kr (standard 5000): ") or "5000")
            konto = Checkkonto(agare, kontonummer, kreditgrans=kredit)
        else:
            print("X Ogiltigt val.")
            return
        
        db.spara_konto(konto)
        print(f"\n Konto skapat! Ditt kontonummer: {kontonummer}")
    except ValueError:
        print("X Ogiltigt belopp angivet.")

def lista_konton(db: Databas) -> list:
    """Visar alla konton och returnerar dem."""
    konton = db.hamta_alla_konton()
    if not konton:
        print("\  Inga konton hittades. ")
        return[]
    print("\n--- ALLA KONTON ---")
    for i, k in enumerate(konton, 1):
        print(f"  {i}.  {k}")
    return konton

def valj_konto(db: Databas):
    """Låter användaren välja ett konto och utföra åtgärder."""
    konton = lista_konton(db)
    if not konton:
        return
    
    try:
        val = int(input("\nVälj konto (nummer): ")) - 1
        if val < 0 or val >= len(konton):
            print("X Ogiltigt val.")
            return
    except ValueError:
        print("X Ange ett nummer. ")
        return

    Konto = konton[val]
    konto_meny(Konto,  db)

def konto_meny(konto, db: Databas):
    """Meny för ett specifikt konto."""
    while True:
        konto.visa_saldo()
        print("\nVad vill du göra?")
        print("  1. Sätt in pengar")
        print("  2. Ta ut pengar")
        print("  3. Visa transaktioner")
        print("  4. Visa saldo i annan valuta")
        if isinstance(konto, Sparkonto):
            print("  5. beräkna ränta")
        print("  O. Tillbaka")

        val = input("\nm Ditt val: ").strip()

        if val == "1":
            try:
                belopp = float(input("Belopp att sätta in (kr):  "))
                besk = input("Beskrivning (valfri): ").strip() or "Insättning"
                if konto.satt_in(belopp, besk):
                    db.spara_konto(Konto)
                    #spara transaktione i databasen
                    if konto.transaktioner:
                        db.spara_transaktion(konto.transaktioner[-1])
            except ValueError:
                print("X Ange ett giltigt belopp.")

        elif val == "2":
            try:
                belopp = float(input("Belopp att ta ut (kr): "))
                besk = input("beskrivning (valfri): ").strip() or "Uttag"
                if konto.ta_ut(belopp, besk):
                    db.spara_konto(konto)
                    if konto.trasaktioner:
                        db.spara_transaktion(konto.transaktioner[-1])
            except ValueError:
                print("X Ange ett giltigt belopp. ")

        elif val == "3":
            visa_transaktioner(konto.kontonummer, db)

        elif val == "4":
            kurser = hamta_valutakurser()
            visa_valutameny(konto.saldo, kurser)

        elif val == "5" and isinstance(konto, Sparkonto):
            konto.berakna_ranta()
            db.spara_konto(konto)
            if konto.transaktioner:
                db.spara_transaktion(konto.transaktioner[-1])

        elif val == "0":
            break
        else:
            print("X Ogiltigt val, försök igen. ")

def visa_transaktioner(kontonummer: str, db: Databas):
    """Visar transaktionshistorik för ett konto."""
    transaktioner = db.hamta_transaktioner(kontonummer)
    if not transaktioner:
        print("\n  Inga transaktioner hittades. ")
        return
    
    print(f"\n--- TRANSAKTIONER FÖR {kontonummer} ---")
    print(f"{'Datum':<17} {'Typ':<13} {'Belopp':<12} {'beskrivning'}")
    print("-" * 60)
    for typ, belopp, besk, datum in transaktioner:
        pil = "+" if typ in ("insättning", "ränta") else "-"
        print(f"{datum:<17} {typ.captalize():<13} {pil} {belopp:>9.2f} kr {besk} ")

def ta_bort_konto_meny(db: Databas):
    """Låter användaren ta bort ett konto."""
    konton = lista_konton(db)
    if not konton:
        return
    try:
        val = int(input("\nVälj konto att ta bort (nummer): "))  - 1
        if val < 0 or val > len(konton):
            print("X Ogiltigt val.")
            return
        konto = konton[val]
        bekrafta = input(f" Ta bort konto {konto.kontonummer}? (ja/nej): ").strip().lower()
        if bekrafta == "ja":
            db.ta_bort_konto(konto.kontonummer)
        else:
            print("Åtgärd avbruten.")
    except ValueError:
        print("X Ange ett nummer.")

def huvud_meny():
    """Startar programmet och visar huvudmenyn."""
    skriv_rubrik()
    db = Databas()  # öppnar/skapar databasen

    while True:
        print("\n--- HUVUDMENY ---")
        print("  1. Skapa nytt konto")
        print("  2. Visa och hantera konto")
        print("  3. Lista alla konton")
        print("  4. Ta bort konto")
        print("  0. Avluta")

        val = input("\nDitt val: ").strip()
        
        if val == "1":
            skapa_konto_meny(db)
        elif val == "2":
            valj_konto(db)
        elif val == "3":
            lista_konton(db)
        elif val == "4":
            ta_bort_konto_meny(db)
        elif val == "0":
            print("\n Tack för att du använde Personlig Ekonomi. Hej då!")
            break
        else:
            print("X Ogiltigt val, försök igen.")

# Körs bara om filen körs direkt (inte importeras)
if __name__ == "__main__":
    huvud_meny()

