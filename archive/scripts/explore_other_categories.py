"""
Průzkum struktury ostatních ISVZ kategorií.
Zjistí, zda DNS, SON, SK, RVP obsahují ICT zakázky.
"""

import json
import os
from collections import Counter

def explore_json_structure(file_path, max_sample=5):
    """Prozkoumá strukturu JSON souboru"""
    
    print(f"\n{'='*70}")
    print(f"  {os.path.basename(file_path)}")
    print(f"{'='*70}\n")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Chyba: {e}")
        return None
    
    # Metadata
    print("📊 METADATA:")
    for key in data:
        if key != 'data':
            print(f"   {key}: {data[key]}")
    
    # Data
    items = data.get('data', [])
    print(f"\n📈 Počet záznamů: {len(items)}")
    
    if not items:
        print("   ⚠️  Žádná data")
        return None
    
    # Top-level klíče
    print("\n🔑 Top-level klíče v záznamu:")
    first_item = items[0]
    for key in first_item.keys():
        print(f"   - {key}")
    
    # Vzorky dat
    print(f"\n📋 Vzorky ({min(max_sample, len(items))} záznamů):\n")
    
    for i, item in enumerate(items[:max_sample], 1):
        print(f"{i}. ", end="")
        
        # Podle typu kategorie extrahuj relevantní info
        if 'dynamicky_nakupni_system' in item:
            dns = item['dynamicky_nakupni_system']
            nazev = dns.get('nazev_dynamickeho_nakupniho_systemu', 'N/A')
            print(f"DNS: {nazev[:80]}")
            
        elif 'soutez_o_navrh' in item:
            son = item['soutez_o_navrh']
            nazev = son.get('nazev_souteze_o_navrh', 'N/A')
            print(f"SON: {nazev[:80]}")
            
        elif 'system_kvalifikace' in item:
            sk = item['system_kvalifikace']
            nazev = sk.get('nazev_systemu_kvalifikace', 'N/A')
            print(f"SK: {nazev[:80]}")
            
        elif 'rizeni_vyberu_poddodavatele' in item:
            rvp = item['rizeni_vyberu_poddodavatele']
            nazev = rvp.get('nazev', 'N/A')
            print(f"RVP: {nazev[:80]}")
        else:
            print(f"Neznámá struktura: {list(item.keys())}")
    
    return {
        'file': os.path.basename(file_path),
        'count': len(items),
        'structure': first_item.keys() if items else []
    }


def search_ict_in_text(text):
    """Hledá ICT klíčová slova v textu"""
    if not text:
        return False
    
    text_lower = text.lower()
    
    ict_keywords = [
        'software', 'aplikace', 'informační systém', 'it ', 'ict',
        'web', 'databáze', 'cloud', 'server', 'digitalizace',
        'programování', 'vývoj', 'kódování'
    ]
    
    for keyword in ict_keywords:
        if keyword in text_lower:
            return True
    
    return False


def analyze_category_for_ict(file_path, category_type):
    """Analyzuje kategorii na přítomnost ICT"""
    
    print(f"\n{'='*70}")
    print(f"  ANALÝZA ICT: {os.path.basename(file_path)}")
    print(f"{'='*70}\n")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Chyba: {e}")
        return
    
    items = data.get('data', [])
    
    if not items:
        print("⚠️  Žádná data")
        return
    
    ict_count = 0
    ict_examples = []
    
    for item in items:
        is_ict = False
        nazev = None
        
        if category_type == 'DNS' and 'dynamicky_nakupni_system' in item:
            dns = item['dynamicky_nakupni_system']
            nazev = dns.get('nazev_dynamickeho_nakupniho_systemu', '')
            popis = dns.get('zadavaci_postup_pro_zavedeni_dynamickeho_nakupniho_systemu', {}).get('predmet', {}).get('popis_predmetu', '')
            
            if search_ict_in_text(nazev) or search_ict_in_text(popis):
                is_ict = True
        
        elif category_type == 'SON' and 'soutez_o_navrh' in item:
            son = item['soutez_o_navrh']
            nazev = son.get('nazev_souteze_o_navrh', '')
            popis = son.get('predmet', {}).get('popis_predmetu', '')
            
            if search_ict_in_text(nazev) or search_ict_in_text(popis):
                is_ict = True
        
        elif category_type == 'SK' and 'system_kvalifikace' in item:
            sk = item['system_kvalifikace']
            nazev = sk.get('nazev_systemu_kvalifikace', '')
            popis = sk.get('popis', '')
            
            if search_ict_in_text(nazev) or search_ict_in_text(popis):
                is_ict = True
        
        elif category_type == 'RVP' and 'rizeni_vyberu_poddodavatele' in item:
            rvp = item['rizeni_vyberu_poddodavatele']
            nazev = rvp.get('nazev', '')
            popis = rvp.get('predmet', {}).get('popis_predmetu', '')
            
            if search_ict_in_text(nazev) or search_ict_in_text(popis):
                is_ict = True
        
        if is_ict:
            ict_count += 1
            if len(ict_examples) < 10:
                ict_examples.append(nazev)
    
    print(f"📊 Výsledky:")
    print(f"   Celkem záznamů: {len(items)}")
    print(f"   ICT záznamů: {ict_count}")
    print(f"   Procento: {ict_count/len(items)*100:.2f}%")
    
    if ict_examples:
        print(f"\n📋 Příklady ICT záznamů:")
        for i, example in enumerate(ict_examples, 1):
            print(f"   {i}. {example[:100]}")
    else:
        print(f"\n⚠️  Žádné ICT záznamy nenalezeny")


if __name__ == '__main__':
    data_dir = 'isvz_data'
    
    # Najdi všechny non-VZ JSON soubory
    categories = {
        'DNS': [],
        'SON': [],
        'SK': [],
        'RVP': []
    }
    
    for file in os.listdir(data_dir):
        if file.endswith('.json'):
            for cat in categories.keys():
                if file.startswith(cat):
                    categories[cat].append(os.path.join(data_dir, file))
    
    print("=" * 70)
    print("  PRŮZKUM OSTATNÍCH KATEGORIÍ ISVZ")
    print("=" * 70)
    
    # Projdi každou kategorii
    for category, files in categories.items():
        if not files:
            continue
        
        print(f"\n\n{'#'*70}")
        print(f"  KATEGORIE: {category}")
        print(f"{'#'*70}")
        
        # Prozkoumej strukturu (první soubor)
        if files:
            explore_json_structure(files[0], max_sample=3)
        
        # Analyzuj všechny soubory na ICT
        for file in files:
            analyze_category_for_ict(file, category)
    
    print("\n\n" + "=" * 70)
    print("  SOUHRN")
    print("=" * 70)
    print("\nKATEGORIE PRO BUDOUCÍ ZPRACOVÁNÍ:")
    print("  - DNS (Dynamické nákupní systémy) - MŮŽE obsahovat ICT")
    print("  - SON (Soutěže o návrh) - MŮŽE obsahovat ICT")
    print("  - SK (Systémy kvalifikace) - Většinou ne-ICT")
    print("  - RVP (Výběr poddodavatelů) - Většinou ne-ICT")
