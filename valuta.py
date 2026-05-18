# Valuta.py
# Författare: Francisco Apcho 
# Kurs: Programmering 2
# Datum: 2026-0519
# Hämtar aktuella valutakurser från ett gratis extern API.
# API = ett sätt att kommunicera med en annan tjänst via internet.
# Vi använder: https://open.er-api.com (kräver ingen API-nyckel)

import urllib.request # Inbyggt i Python - ingen installation krävs
import json

VALUTA_API_URL = "https://open.er-api.com/v6/latest/SEK"

def hamta_valutakurser() -> dict:
    """
    Hämta aktuella valutakurser med SEK som bas.
    Returnerar en ordbok: {"USD": 0.091, "EURO": 0.085, ...}
    eller en tom ordbok om hämtningen misslyckas.
    """
    try:
        print("  Hämtar valutakurser från API...")
        with urllib.request.urlopen(VALUTA_API_URL, timeout=5) as svar:
            data = json.loads(svar.read().decode())

        if data.get("result") == "success":
            kurser = data["rates"]
            print("  Valutakurser hämtade!")
            return kurser
        else:
            print("   API svarade men data saknas.")
            return {}
        
    except Exception as e:
        # Felhantering: om internet saknas eller API är
        print(f"X Kunde inte hämta valutakurser: {e}")
        print("   Använder reservvärden istället.")
        # Reservvärden ifall API:et är nere
        return {
            "USD": 0.091,
            "EUR": 0.085,
            "GBP": 0.072,
            "NOK": 0.97,
            "DKK": 0.63
        }
    

def konsertera(belopp_sek: float, till_valuta: str, kurser: dict) -> float:
    """
    Konverterar ett belopp från SEK till en annan valuta.
    Args:
        belopp_sek   : Belopp i svenska kronor
        till_valuta  : Valutakod t.ex. "USD", "EUR"
        kurser       : Ordbok med kurser från hamta_valutakurser()

    Returns:
        Konverterat belopp, eller -1 om valutan inte hittas.
    """
    till_valuta = till_valuta.upper()
    if till_valuta not in kurser:
        print(f"X Valuta '{till_valuta}' hittades inte.")
        return -1.0
    return belopp_sek * kurser[till_valuta]

def visa_valutameny(saldo_sek: float, kurser: dict):
    """Visa saldot i flera valutor."""
    vanliga_valutor = ["USD", "EUR", "GBP", "NOK", "DKK"]
    print(f"\n{'='*45}")
    print(f"  Ditt saldo i olika valutor ({saldo_sek:.2f} SEK)")
    print(f"{'='*45}")
    for valuta in vanliga_valutor:
        if valuta in kurser:
            konverterat = konverterat(saldo_sek, valuta, kurser)
            print(f"  {valuta}: {konverterat:>10.2f}")
    print(f"{'='*45}")