import json
from collections import defaultdict, Counter
from datetime import datetime

def analyze_open_tenders(file_path):
    """Analyzuje stavy a podmínky pro identifikaci otevřených zakázek"""
    
    print(f"Načítám soubor {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    zakazky = data.get('data', [])
    print(f"Celkem zakázek: {len(zakazky)}\n")
    
    # Statistiky
    stats = {
        'formulare_typy': Counter(),
        'formulare_oznameni': Counter(),
        'stav_zadavaciho_postupu': Counter(),
        'druh_zadavaciho_postupu': Counter(),
        'lhuty_druhy': Counter(),
        'vysledek_ukonceni': Counter(),
        'datum_zahajeni_exists': 0,
        'datum_ukonceni_exists': 0,
        'lhuty_exists': 0,
        'aktivni_lhuty': 0,
    }
    
    # Příklady otevřených a zavřených zakázek
    open_examples = []
    closed_examples = []
    
    current_date = datetime.now()
    
    for i, zakazka in enumerate(zakazky):
        vz = zakazka.get('verejna_zakazka', {})
        
        # Zadávací postupy
        for zp in vz.get('zadavaci_postupy', []):
            # Uveřejňovací formuláře
            for formular in zp.get('uverejnovaci_formulare', []):
                typ_form = formular.get('typ_formulare', 'N/A')
                typ_ozn = formular.get('typ_oznameni', 'N/A')
                stats['formulare_typy'][typ_form] += 1
                stats['formulare_oznameni'][typ_ozn] += 1
            
            # Zadávací postupy pro části
            for zpc in zp.get('zadavaci_postupy_pro_casti', []):
                zpp = zpc  # V části může být celá struktura zadávacího postupu
        
        # Části veřejné zakázky
        for cast in vz.get('casti_verejne_zakazky', []):
            zpp = cast.get('zadavaci_postup_pro_cast', {})
            
            if zpp:
                # Stav
                stav = zpp.get('stav')
                if stav:
                    stats['stav_zadavaciho_postupu'][stav] += 1
                
                # Druh zadávacího postupu
                druh = zpp.get('druh_zadavaciho_postupu')
                if druh:
                    stats['druh_zadavaciho_postupu'][druh] += 1
                
                # Data zahájení/ukončení
                if zpp.get('datum_zahajeni_zadavaciho_postupu'):
                    stats['datum_zahajeni_exists'] += 1
                
                if zpp.get('datum_ukonceni_zadavaciho_postupu'):
                    stats['datum_ukonceni_exists'] += 1
                
                # Lhůty
                lhuty = zpp.get('lhuty', [])
                if lhuty:
                    stats['lhuty_exists'] += 1
                    
                    for lhuta in lhuty:
                        druh_lhuty = lhuta.get('druh_lhuty', 'N/A')
                        stats['lhuty_druhy'][druh_lhuty] += 1
                        
                        # Aktivní lhůta?
                        if lhuta.get('aktivni') == True:
                            stats['aktivni_lhuty'] += 1
                        
                        # Kontrola konec lhůty
                        datum_konce = lhuta.get('datum_a_cas_konce_lhuty')
                        if datum_konce:
                            try:
                                konce_dt = datetime.fromisoformat(datum_konce.replace('Z', '+00:00'))
                                # Je lhůta ještě v platnosti?
                            except:
                                pass
                
                # Výsledek
                vysledek = zpp.get('vysledek', {})
                if vysledek:
                    vysledek_ukonceni = vysledek.get('vysledek_ukonceni_zadavaciho_postupu')
                    if vysledek_ukonceni:
                        stats['vysledek_ukonceni'][vysledek_ukonceni] += 1
                    
                    # Datum zrušení?
                    datum_zruseni = vysledek.get('datum_a_cas_zruseni_postupu')
                
                # Příklad otevřené zakázky
                if i < 5 and len(open_examples) < 3:
                    # Pokud má lhůty a nemá výsledek ukončení
                    if lhuty and not vysledek.get('vysledek_ukonceni_zadavaciho_postupu'):
                        open_examples.append({
                            'identifikator': vz.get('identifikator_NIPEZ'),
                            'nazev': vz.get('nazev_verejne_zakazky'),
                            'druh': vz.get('druh_verejne_zakazky'),
                            'datum_zahajeni': zpp.get('datum_zahajeni_zadavaciho_postupu'),
                            'datum_ukonceni': zpp.get('datum_ukonceni_zadavaciho_postupu'),
                            'stav': zpp.get('stav'),
                            'lhuty': [{
                                'druh': l.get('druh_lhuty'),
                                'konec': l.get('datum_a_cas_konce_lhuty'),
                                'aktivni': l.get('aktivni')
                            } for l in lhuty[:2]],
                            'vysledek': vysledek.get('vysledek_ukonceni_zadavaciho_postupu')
                        })
                
                # Příklad uzavřené zakázky
                if i < 100 and len(closed_examples) < 3:
                    if vysledek.get('vysledek_ukonceni_zadavaciho_postupu'):
                        closed_examples.append({
                            'identifikator': vz.get('identifikator_NIPEZ'),
                            'nazev': vz.get('nazev_verejne_zakazky'),
                            'druh': vz.get('druh_verejne_zakazky'),
                            'datum_zahajeni': zpp.get('datum_zahajeni_zadavaciho_postupu'),
                            'datum_ukonceni': zpp.get('datum_ukonceni_zadavaciho_postupu'),
                            'stav': zpp.get('stav'),
                            'vysledek': vysledek.get('vysledek_ukonceni_zadavaciho_postupu'),
                            'datum_zruseni': vysledek.get('datum_a_cas_zruseni_postupu')
                        })
    
    return stats, open_examples, closed_examples

def save_state_analysis(stats, open_ex, closed_ex, output_file):
    """Uloží analýzu stavů do markdown"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Analýza stavů a filtrování otevřených zakázek ISVZ\n\n")
        
        f.write("## Klíčová zjištění pro filtrování otevřených zakázek\n\n")
        f.write("### Kritéria pro identifikaci OTEVŘENÝCH zakázek:\n\n")
        f.write("1. **Absence výsledku ukončení** - pole `vysledek.vysledek_ukonceni_zadavaciho_postupu` musí být `null` nebo prázdné\n")
        f.write("2. **Existence aktivních lhůt** - pole `lhuty[]` obsahuje záznamy\n")
        f.write("3. **Datum konce lhůty** - `datum_a_cas_konce_lhuty` je v budoucnosti (po aktuálním datu)\n")
        f.write("4. **Druh lhůty** - zejména `\"Lhůta pro podání nabídek\"` nebo `\"Lhůta pro podání žádostí o účast\"`\n")
        f.write("5. **Datum ukončení postupu** - pole `datum_ukonceni_zadavaciho_postupu` je `null`\n\n")
        
        f.write("### Kde hledat?\n\n")
        f.write("Struktura v JSON:\n")
        f.write("```\n")
        f.write("data[]\n")
        f.write("  └─ verejna_zakazka\n")
        f.write("       └─ casti_verejne_zakazky[]\n")
        f.write("            └─ zadavaci_postup_pro_cast\n")
        f.write("                 ├─ datum_zahajeni_zadavaciho_postupu\n")
        f.write("                 ├─ datum_ukonceni_zadavaciho_postupu  <-- NULL = aktivní\n")
        f.write("                 ├─ lhuty[]                             <-- Kontrola termínů\n")
        f.write("                 │    ├─ druh_lhuty\n")
        f.write("                 │    ├─ datum_a_cas_konce_lhuty        <-- > nyní\n")
        f.write("                 │    └─ aktivni\n")
        f.write("                 └─ vysledek\n")
        f.write("                      └─ vysledek_ukonceni_zadavaciho_postupu  <-- NULL = aktivní\n")
        f.write("```\n\n")
        
        f.write("## Statistiky\n\n")
        
        f.write("### Typy formulářů\n\n")
        f.write("| Typ formuláře | Počet |\n")
        f.write("|--------------|-------|\n")
        for typ, count in stats['formulare_typy'].most_common():
            f.write(f"| {typ} | {count} |\n")
        f.write("\n")
        
        f.write("### Typy oznámení\n\n")
        f.write("| Typ oznámení | Počet |\n")
        f.write("|--------------|-------|\n")
        for typ, count in stats['formulare_oznameni'].most_common():
            f.write(f"| {typ} | {count} |\n")
        f.write("\n")
        
        if stats['stav_zadavaciho_postupu']:
            f.write("### Stavy zadávacího postupu\n\n")
            f.write("| Stav | Počet |\n")
            f.write("|------|-------|\n")
            for stav, count in stats['stav_zadavaciho_postupu'].most_common():
                f.write(f"| {stav} | {count} |\n")
            f.write("\n")
        
        f.write("### Druhy zadávacího postupu\n\n")
        f.write("| Druh | Počet |\n")
        f.write("|------|-------|\n")
        for druh, count in stats['druh_zadavaciho_postupu'].most_common():
            f.write(f"| {druh} | {count} |\n")
        f.write("\n")
        
        f.write("### Druhy lhůt\n\n")
        f.write("| Druh lhůty | Počet |\n")
        f.write("|------------|-------|\n")
        for druh, count in stats['lhuty_druhy'].most_common():
            f.write(f"| {druh} | {count} |\n")
        f.write("\n")
        
        if stats['vysledek_ukonceni']:
            f.write("### Výsledky ukončení zadávacího postupu\n\n")
            f.write("| Výsledek | Počet |\n")
            f.write("|----------|-------|\n")
            for vysl, count in stats['vysledek_ukonceni'].most_common():
                f.write(f"| {vysl} | {count} |\n")
            f.write("\n")
        
        f.write("### Další statistiky\n\n")
        f.write(f"- Zakázky s datem zahájení: {stats['datum_zahajeni_exists']}\n")
        f.write(f"- Zakázky s datem ukončení: {stats['datum_ukonceni_exists']}\n")
        f.write(f"- Zakázky s lhůtami: {stats['lhuty_exists']}\n")
        f.write(f"- Aktivní lhůty: {stats['aktivni_lhuty']}\n\n")
        
        f.write("## Příklady\n\n")
        
        if open_ex:
            f.write("### Příklad pravděpodobně OTEVŘENÉ zakázky\n\n")
            for ex in open_ex:
                f.write(f"**{ex['identifikator']}**: {ex['nazev']}\n\n")
                f.write(f"- **Druh**: {ex['druh']}\n")
                f.write(f"- **Datum zahájení**: {ex['datum_zahajeni']}\n")
                f.write(f"- **Datum ukončení**: {ex['datum_ukonceni']} *(NULL = probíhá)*\n")
                f.write(f"- **Stav**: {ex['stav']}\n")
                f.write(f"- **Výsledek ukončení**: {ex['vysledek']} *(NULL = probíhá)*\n")
                f.write(f"- **Lhůty**:\n")
                for lhuta in ex['lhuty']:
                    f.write(f"  - {lhuta['druh']}: konec {lhuta['konec']}, aktivní: {lhuta['aktivni']}\n")
                f.write("\n")
        
        if closed_ex:
            f.write("### Příklad UZAVŘENÉ zakázky\n\n")
            for ex in closed_ex:
                f.write(f"**{ex['identifikator']}**: {ex['nazev']}\n\n")
                f.write(f"- **Druh**: {ex['druh']}\n")
                f.write(f"- **Datum zahájení**: {ex['datum_zahajeni']}\n")
                f.write(f"- **Datum ukončení**: {ex['datum_ukonceni']}\n")
                f.write(f"- **Stav**: {ex['stav']}\n")
                f.write(f"- **Výsledek ukončení**: {ex['vysledek']} ✓\n")
                f.write(f"- **Datum zrušení**: {ex['datum_zruseni']}\n")
                f.write("\n")

if __name__ == '__main__':
    file_path = 'isvz_data/VZ-01-2026.json'
    output_file = 'isvz_stavy_filtrovani.md'
    
    print("Spouštím analýzu stavů...")
    stats, open_ex, closed_ex = analyze_open_tenders(file_path)
    
    print(f"\nUkládám analýzu do {output_file}...")
    save_state_analysis(stats, open_ex, closed_ex, output_file)
    
    print("Hotovo!")
