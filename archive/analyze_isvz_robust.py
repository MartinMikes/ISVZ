#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Robustní skript pro analýzu ISVZ dat - zvládá i velké a částečně poškozené soubory
"""

import json
import os
from datetime import datetime
import re

def is_ict_related(text):
    """Kontrola, zda text souvisí s ICT/programováním"""
    if not text:
        return False
    
    text_lower = text.lower()
    
    # Klíčová slova pro ICT/programování
    ict_keywords = [
        'software', 'aplikace', 'aplikací', 'programov', 'vývoj', 'web',
        'informační systém', 'is ', 'it ', 'ict', 'databáz', 'database',
        'cloud', 'api', 'rozhraní', 'integrace', 'portál', 'platforma',
        'mobilní aplikace', 'webov', 'digital', 'kódování', 'programátor',
        'developer', 'backend', 'frontend', 'fullstack', 'saas',
        'implementace systému', 'sw ', 'software development',
        'app ', 'javascript', 'python', 'java', 'react', 'angular',
        'node.js', 'php', '.net', 'dotnet', 'html', 'css', 'sql',
        'agile', 'scrum', 'devops', 'microservices', 'ai', 'ml',
        'machine learning', 'umělá inteligence', 'data analytics',
        'business intelligence', 'bi ', 'crm', 'erp systém', 'registr',
        'egovernment', 'e-government', 'datové schránky', 'digitalizace', 'modernizace'
    ]
    
    # Negativní klíčová slova (HW, správa)
    negative_keywords = [
        'dodávka hardware', 'dodávka hw', 'dodávka počítač',
        'dodávka server', 'dodávka notebook', 'dodávka tiskárn',
        'správa sítě', 'správa infrastruktury', 'helpdesk',
        'technická podpora', 'administrativa systému',
        'provoz systému', 'údržba hardware', 'servis hardware',
        'instalace hardware', 'kabeláž', 'switching', 'routing',
        'toner', 'cartridge', 'spotřební materiál'
    ]
    
    # Nejprve kontrola negativních klíčových slov
    for keyword in negative_keywords:
        if keyword in text_lower:
            return False
    
    # Kontrola pozitivních klíčových slov
    for keyword in ict_keywords:
        if keyword in text_lower:
            return True
    
    return False

def parse_date(date_str):
    """Parsování data z různých formátů"""
    if not date_str or date_str == 'N/A':
        return None
    
    try:
        # ISO formát s timezone
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except:
        try:
            # ISO formát bez timezone
            return datetime.fromisoformat(date_str)
        except:
            try:
                # České datum DD.MM.YYYY
                return datetime.strptime(date_str, '%d.%m.%Y')
            except:
                return None

def is_open_tender(tender):
    """Kontrola, zda je zakázka stále otevřená"""
    
    # Kontrola stavu zakázky
    stav = tender.get('stavVZ', '')
    if any(x in str(stav).lower() for x in ['uzavřen', 'zrušen', 'ukončen', 'closed', 'cancelled']):
        return False
    
    # Kontrola termínu pro podání nabídek
    deadline_fields = ['lhutaProPodaniNabidek', 'lhutaProPodaniZadostiOUcast']
    
    for field in deadline_fields:
        deadline_str = tender.get(field)
        if deadline_str:
            deadline = parse_date(deadline_str)
            if deadline:
                now = datetime.now(deadline.tzinfo) if deadline.tzinfo else datetime.now()
                if deadline > now:
                    return True
    
    # Pokud nemáme info o termínu a není uzavřená, považujeme za otevřenou
    if not any(tender.get(f) for f in deadline_fields):
        return True
    
    return False

def extract_text_from_item(item):
    """Extrahuje všechen relevantní text z položky - rekurzivně všechny stringy"""
    text_parts = []
    
    def extract_recursive(obj, depth=0):
        if depth > 10:  # Omezíme hloubku rekurze
            return
        
        if isinstance(obj, str) and len(obj) > 3:  # Ignoruj velmi krátké stringy
            text_parts.append(obj)
        elif isinstance(obj, dict):
            for value in obj.values():
                extract_recursive(value, depth + 1)
        elif isinstance(obj, list):
            for v in obj:
                extract_recursive(v, depth + 1)
    
    extract_recursive(item)
    return " ".join(text_parts)

def analyze_json_stream(filepath, file_type):
    """Analyzuje JSON soubor po částech - pro velké soubory"""
    print(f"  Načítám soubor: {filepath}")
    results = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Načteme JSON
            data = json.load(f)
            
        # Určení struktury dat
        items = []
        if isinstance(data, dict):
            # Hledáme pole se zakázkami
            for key in ['zakazky', 'items', 'data', 'polozky']:
                if key in data and isinstance(data[key], list):
                    items = data[key]
                    break
            
            # Pokud nenajdeme známý klíč, vezmeme první pole
            if not items:
                for key, value in data.items():
                    if isinstance(value, list) and len(value) > 0:
                        items = value
                        break
        elif isinstance(data, list):
            items = data
        
        print(f"  Nalezeno {len(items)} položek k analýze")
        
        # Zpracování položek
        for idx, item in enumerate(items):
            if idx % 500 == 0 and idx > 0:
                print(f"    Zpracováno {idx}/{len(items)}... (zatím {len(results)} ICT zakázek)")
            
            # Kontrola, zda je otevřená
            if not is_open_tender(item):
                continue
            
            # Extrakce textu
            search_text = extract_text_from_item(item)
            
            # Kontrola ICT
            if is_ict_related(search_text):
                # Extrakce dat z vnořené struktury
                def safe_get(d, *keys):
                    """Bezpečně získá hodnotu z vnořeného dict"""
                    for key in keys:
                        if isinstance(d, dict):
                            d = d.get(key)
                        else:
                            return 'N/A'
                    return d if d else 'N/A'
                
                results.append({
                    'typ': file_type,
                    'nazev': (safe_get(item, 'dynamicky_nakupni_system', 'nazev_dynamickeho_nakupniho_systemu') or
                             safe_get(item, 'soutez_o_navrh', 'nazev_souteze_o_navrh') or
                             safe_get(item, 'nazev') or safe_get(item, 'nazevZakazky')),
                    'evidencniCislo': (safe_get(item, 'dynamicky_nakupni_system', 'evidencni_cislo_ve_Vestniku_verejnych_zakazek') or
                                      safe_get(item, 'evidencniCisloZakazky') or safe_get(item, 'evidencniCislo')),
                    'zadavatel': safe_get(item, 'nazevZadavatele'),
                    'predmet': search_text[:800],
                    'lhutaPodani': (safe_get(item, 'lhutaProPodaniNabidek') or safe_get(item, 'lhutaProPodaniZadostiOUcast')),
                    'datumUverejneni': safe_get(item, 'datumUverejneni'),
                    'url': safe_get(item, 'url'),
                    'celkovaHodnota': (safe_get(item, 'odhadovanaHodnota') or safe_get(item, 'celkovaHodnota')),
                    'mena': safe_get(item, 'mena')
                })
        
        print(f"  ✓ Nalezeno {len(results)} relevantních ICT zakázek")
        
    except Exception as e:
        print(f"  ✗ Chyba při zpracování: {e}")
    
    return results

def main():
    """Hlavní funkce"""
    print("=" * 80)
    print("ROBUSTNÍ ANALÝZA DAT ISVZ - HLEDÁNÍ ICT ZAKÁZEK")
    print("=" * 80)
    print()
    
    data_dir = "isvz_data"
    
    # Seznam souborů k analýze
    files_to_analyze = [
        ('VZ-01-2026.json', 'Veřejná zakázka'),
        ('DNS-01-2026.json', 'Dynamický nákupní systém'),
        ('SON-01-2026.json', 'Soutěž o návrh'),
        ('SK-01-2026.json', 'Systém kvalifikace'),
        ('RVP-01-2026.json', 'Řízení na výběr poddodavatele')
    ]
    
    all_results = []
    
    for filename, file_type in files_to_analyze:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath) / (1024 * 1024)
            print(f"\n{'=' * 80}")
            print(f"Analyzuji: {file_type} ({filename}) - {file_size:.1f} MB")
            print(f"{'=' * 80}")
            
            if file_size > 1:  # Soubor větší než 1 MB
                results = analyze_json_stream(filepath, file_type)
            else:
                results = analyze_json_stream(filepath, file_type)
            
            all_results.extend(results)
        else:
            print(f"\n⚠ Soubor nenalezen: {filepath}")
    
    # Výpis výsledků
    print("\n" + "=" * 80)
    print(f"CELKEM NALEZENO: {len(all_results)} RELEVANTNÍCH ICT ZAKÁZEK")
    print("=" * 80)
    
    if all_results:
        # Uložení do výstupního souboru
        output_file = "ict_zakazky_vysledky.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Výsledky uloženy do: {output_file}")
        
        # Vytvoření čitelného reportu
        report_file = "ict_zakazky_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("PŘEHLED ICT ZAKÁZEK Z ISVZ (leden 2026)\n")
            f.write(f"Datum vytvoření: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write(f"Celkem nalezeno: {len(all_results)} zakázek\n")
            f.write("=" * 80 + "\n\n")
            
            for idx, result in enumerate(all_results, 1):
                f.write(f"\n{'=' * 80}\n")
                f.write(f"{idx}. {result['nazev']}\n")
                f.write("=" * 80 + "\n")
                f.write(f"Typ: {result['typ']}\n")
                f.write(f"Evidenční číslo: {result['evidencniCislo']}\n")
                f.write(f"Zadavatel: {result['zadavatel']}\n")
                f.write(f"Datum uveřejnění: {result.get('datumUverejneni', 'N/A')}\n")
                f.write(f"Lhůta podání nabídek: {result['lhutaPodani']}\n")
                if result['celkovaHodnota'] != 'N/A':
                    f.write(f"Odhadovaná hodnota: {result['celkovaHodnota']} {result.get('mena', 'CZK')}\n")
                if result['url'] != 'N/A':
                    f.write(f"URL: {result['url']}\n")
                f.write(f"\nPředmět zakázky:\n")
                f.write("-" * 80 + "\n")
                f.write(f"{result['predmet']}\n")
                f.write("\n")
        
        print(f"✓ Textový report uložen do: {report_file}")
        
        # Výpis prvních 10 pro náhled
        print("\n" + "=" * 80)
        print(f"NÁHLED PRVNÍCH {min(10, len(all_results))} ZAKÁZEK:")
        print("=" * 80)
        for idx, result in enumerate(all_results[:10], 1):
            print(f"\n{idx}. {result['nazev'][:100]}")
            print(f"   Typ: {result['typ']}")
            print(f"   Zadavatel: {result['zadavatel'][:80]}")
            print(f"   Lhůta: {result['lhutaPodani']}")
            print(f"   Evidence: {result['evidencniCislo']}")
            if result['celkovaHodnota'] != 'N/A':
                print(f"   Hodnota: {result['celkovaHodnota']} {result.get('mena', 'CZK')}")
    else:
        print("\n⚠ Nebyly nalezeny žádné relevantní ICT zakázky.")
    
    print("\n" + "=" * 80)
    print("HOTOVO!")
    print("=" * 80)

if __name__ == "__main__":
    main()
