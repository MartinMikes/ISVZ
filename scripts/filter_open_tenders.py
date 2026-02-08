"""
Filtrování otevřených veřejných zakázek z ISVZ datasetu.

Načte velký JSON soubor a vyfiltruje pouze aktivní zakázky,
o které se můžete ucházet (mají aktivní lhůtu pro podání nabídky).
"""

import json
from datetime import datetime
import sys
import io

# Fix pro Windows console - UTF-8 podpora emoji (jen pokud běží standalone)
if sys.platform == 'win32' and not hasattr(sys.stdout, 'buffer'):
    pass  # Už je wrapped
elif sys.platform == 'win32' and hasattr(sys.stdout, 'buffer') and 'TextIOWrapper' not in str(type(sys.stdout)):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def is_open_tender(zakazka, current_date):
    """
    Zkontroluje, zda je zakázka otevřená pro ucházení.
    
    Kritéria:
    1. Nemá datum ukončení zadávacího postupu
    2. Nemá výsledek ukončení
    3. Má aktivní lhůtu pro podání nabídky/žádosti
    4. Datum konce lhůty je v budoucnosti
    5. Stav není dokončený/zrušený
    """
    vz = zakazka.get('verejna_zakazka', {})
    
    # Kontrola každé části veřejné zakázky
    for cast in vz.get('casti_verejne_zakazky', []):
        zp = cast.get('zadavaci_postup_pro_cast', {})
        
        # Pokud nemá zadávací postup, přeskočit
        if not zp:
            continue
        
        # 1. Kontrola: Nemá datum ukončení
        if zp.get('datum_ukonceni_zadavaciho_postupu'):
            continue
        
        # 2. Kontrola: Nemá výsledek ukončení
        vysledek = zp.get('vysledek')
        if vysledek and vysledek.get('vysledek_ukonceni_zadavaciho_postupu'):
            continue
        
        # 5. Kontrola: Stav není dokončený/zrušený
        stav = zp.get('stav')
        if stav in ['Dokončen/Zadán', 'Ukončeno plnění smlouvy', 'Zrušen', 'Neúspěšný']:
            continue
        
        # 3. a 4. Kontrola lhůt
        lhuty = zp.get('lhuty', [])
        if not lhuty:
            continue
        
        for lhuta in lhuty:
            druh_lhuty = lhuta.get('druh_lhuty', '')
            
            # Hledáme lhůtu pro podání nabídky nebo žádosti o účast
            if 'podání nabíd' in druh_lhuty or 'podání žádosti o účast' in druh_lhuty:
                datum_konce = lhuta.get('datum_a_cas_konce_lhuty')
                
                if datum_konce:
                    try:
                        # Parsování data (formát může být ISO 8601)
                        konce_dt = datetime.fromisoformat(datum_konce.replace('Z', '+00:00'))
                        
                        # Je lhůta stále v budoucnosti?
                        if konce_dt > current_date:
                            return True
                    except (ValueError, AttributeError):
                        # Pokud se nepodaří parsovat datum, pokračovat
                        continue
    
    return False


def filter_open_tenders(input_file, output_file):
    """Načte JSON a vyfiltruje otevřené zakázky"""
    
    print(f"📂 Načítám soubor: {input_file}")
    print("⚠️  Pozor: Soubor je velmi velký (1.3 GB), načítání může trvat...")
    
    # Načtení celého JSON souboru
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Soubor načten úspěšně!")
    except MemoryError:
        print("❌ CHYBA: Nedostatek paměti pro načtení souboru!")
        print("💡 Zkuste restartovat Python nebo zavřít další aplikace.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ CHYBA při načítání souboru: {e}")
        sys.exit(1)
    
    # Metadata
    metadata = {
        'obdobi_od': data.get('obdobi_od'),
        'obdobi_do': data.get('obdobi_do'),
        'verze': data.get('verze'),
        'filtrovano_datum': datetime.now().isoformat(),
        'puvodni_pocet_zakazek': 0,
        'filtrovanych_zakazek': 0
    }
    
    zakazky = data.get('data', [])
    metadata['puvodni_pocet_zakazek'] = len(zakazky)
    
    print(f"\n📊 Celkový počet zakázek v souboru: {len(zakazky)}")
    print(f"🔍 Filtrování otevřených zakázek...")
    
    # Aktuální datum
    current_date = datetime.now()
    print(f"📅 Referenční datum: {current_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Filtrování
    open_tenders = []
    processed = 0
    
    for zakazka in zakazky:
        processed += 1
        
        # Progress bar každých 10000 zakázek
        if processed % 10000 == 0:
            print(f"   ... zpracováno {processed}/{len(zakazky)} zakázek ({processed/len(zakazky)*100:.1f}%)")
        
        if is_open_tender(zakazka, current_date):
            open_tenders.append(zakazka)
    
    metadata['filtrovanych_zakazek'] = len(open_tenders)
    
    print(f"\n✅ Filtrování dokončeno!")
    print(f"📈 Nalezeno {len(open_tenders)} otevřených zakázek")
    print(f"📉 Odfiltrováno {len(zakazky) - len(open_tenders)} uzavřených zakázek")
    print(f"📊 Úspěšnost: {len(open_tenders)/len(zakazky)*100:.2f}% zakázek je otevřených")
    
    # Sestavení výstupního JSON
    output_data = {
        'metadata': metadata,
        'data': open_tenders
    }
    
    # Uložení do souboru
    print(f"\n💾 Ukládám výsledek do: {output_file}")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Soubor úspěšně uložen!")
        
        # Velikost souboru
        import os
        file_size = os.path.getsize(output_file)
        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1024*1024:
            size_str = f"{file_size/1024:.1f} KB"
        else:
            size_str = f"{file_size/(1024*1024):.1f} MB"
        
        print(f"📦 Velikost výstupního souboru: {size_str}")
        
    except Exception as e:
        print(f"❌ CHYBA při ukládání souboru: {e}")
        sys.exit(1)
    
    # Výpis několika příkladů
    if len(open_tenders) > 0:
        print(f"\n📋 Příklady otevřených zakázek:")
        for i, zakazka in enumerate(open_tenders[:5]):
            vz = zakazka.get('verejna_zakazka', {})
            print(f"\n   {i+1}. {vz.get('identifikator_NIPEZ')}")
            print(f"      Název: {vz.get('nazev_verejne_zakazky', 'N/A')[:80]}...")
            print(f"      Druh: {vz.get('druh_verejne_zakazky', 'N/A')}")
            
            hodnota = vz.get('predpokladana_hodnota_bez_DPH_v_CZK')
            if hodnota is not None:
                print(f"      Hodnota: {hodnota:,.0f} Kč")
            else:
                print(f"      Hodnota: Neuvedena")
            
            # Najít lhůtu
            for cast in vz.get('casti_verejne_zakazky', []):
                zp = cast.get('zadavaci_postup_pro_cast', {})
                for lhuta in zp.get('lhuty', []):
                    if 'podání nabíd' in lhuta.get('druh_lhuty', ''):
                        datum_konce = lhuta.get('datum_a_cas_konce_lhuty')
                        if datum_konce:
                            print(f"      ⏰ Lhůta do: {datum_konce}")
                            break
                break
    
    print(f"\n🎉 HOTOVO! Otevřené zakázky jsou uloženy v souboru: {output_file}")
    print(f"📍 Další krok: Filtrování podle ICT kritérií")


if __name__ == '__main__':
    input_file = '../data/VZ/VZ-2026-01.json'
    output_file = '../data/VZ/VZ-2026-01-OPEN.json'
    
    print("=" * 70)
    print("  FILTROVÁNÍ OTEVŘENÝCH VEŘEJNÝCH ZAKÁZEK - ISVZ")
    print("=" * 70)
    print()
    
    filter_open_tenders(input_file, output_file)
    
    print()
    print("=" * 70)
