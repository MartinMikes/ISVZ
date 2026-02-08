#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skript pro analýzu dat z ISVZ a filtrování ICT zakázek
"""

import json
import os
from datetime import datetime
import re

def load_json_file(filepath):
    """Načte JSON soubor"""
    print(f"Načítám soubor: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"  ✓ Úspěšně načteno")
        return data
    except Exception as e:
        print(f"  ✗ Chyba při načítání: {e}")
        return None

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
        'node.js', 'php', '.net', 'html', 'css', 'sql',
        'agile', 'scrum', 'devops', 'microservices', 'ai', 'ml',
        'machine learning', 'umělá inteligence', 'data analytics',
        'business intelligence', 'bi ', 'crm', 'erp systém'
    ]
    
    # Negativní klíčová slova (HW, správa)
    negative_keywords = [
        'dodávka hardware', 'dodávka hw', 'dodávka počítač',
        'dodávka server', 'dodávka notebook', 'dodávka tiskárn',
        'správa sítě', 'správa infrastruktury', 'helpdesk',
        'technická podpora', 'administrativa systému',
        'provoz systému', 'údržba hardware', 'servis hardware',
        'instalace hardware', 'kabeláž', 'switching', 'routing'
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

def is_open_tender(tender):
    """Kontrola, zda je zakázka stále otevřená"""
    # Hledáme termíny pro podání nabídek
    deadline_fields = [
        'lhutaProPodaniNabidek',
        'lhutaProPodaniZadostiOUcast',
        'datumUverejneni',
        'stavVZ'
    ]
    
    # Kontrola stavu zakázky
    if 'stavVZ' in tender:
        stav = tender['stavVZ']
        # Vyloučíme uzavřené/zrušené zakázky
        if any(x in str(stav).lower() for x in ['uzavřen', 'zrušen', 'ukončen', 'closed', 'cancelled']):
            return False
    
    # Kontrola termínu pro podání nabídek
    for field in deadline_fields:
        if field in tender and 'lhut' in field.lower():
            deadline_str = tender[field]
            if deadline_str:
                try:
                    # Pokus o parsování data
                    deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
                    now = datetime.now(deadline.tzinfo) if deadline.tzinfo else datetime.now()
                    if deadline > now:
                        return True
                except:
                    pass
    
    # Pokud nemáme info o termínu, předpokládáme že je otevřená
    return True

def analyze_file(filepath, file_type):
    """Analyzuje jeden JSON soubor"""
    data = load_json_file(filepath)
    if not data:
        return []
    
    results = []
    
    # Určení struktury dat
    items = []
    if isinstance(data, dict):
        if 'zakazky' in data:
            items = data['zakazky']
        elif 'items' in data:
            items = data['items']
        elif 'data' in data:
            items = data['data']
        else:
            # Zkusíme projít všechny hodnoty
            for key, value in data.items():
                if isinstance(value, list):
                    items = value
                    break
    elif isinstance(data, list):
        items = data
    
    print(f"  Nalezeno {len(items)} položek")
    
    for idx, item in enumerate(items):
        if idx % 100 == 0 and idx > 0:
            print(f"  Zpracováno {idx}/{len(items)}...")
        
        # Kontrola, zda je otevřená
        if not is_open_tender(item):
            continue
        
        # Sestavení textu pro analýzu
        search_text = ""
        
        # Pole, která mohou obsahovat relevantní info
        text_fields = [
            'nazev', 'nazevZakazky', 'predmetZakazky', 'popis',
            'hlavniPredmet', 'doplnkovePredmety', 'popisPredmetu',
            'cpv', 'cpvKody', 'dodatecneInformace'
        ]
        
        for field in text_fields:
            if field in item:
                value = item[field]
                if isinstance(value, str):
                    search_text += " " + value
                elif isinstance(value, list):
                    search_text += " " + " ".join(str(v) for v in value)
                elif isinstance(value, dict):
                    search_text += " " + str(value)
        
        # Kontrola ICT
        if is_ict_related(search_text):
            results.append({
                'typ': file_type,
                'nazev': item.get('nazev') or item.get('nazevZakazky', 'N/A'),
                'evidencniCislo': item.get('evidencniCisloZakazky') or item.get('evidencniCislo', 'N/A'),
                'zadavatel': item.get('nazevZadavatele') or item.get('zadavatel', {}).get('nazev', 'N/A'),
                'predmet': search_text[:500],
                'lhutaPodani': item.get('lhutaProPodaniNabidek') or item.get('lhutaProPodaniZadostiOUcast', 'N/A'),
                'url': item.get('url') or item.get('odkaz', 'N/A'),
                'celkovaHodnota': item.get('odhadovanaHodnota') or item.get('celkovaHodnota', 'N/A')
            })
    
    print(f"  ✓ Nalezeno {len(results)} relevantních ICT zakázek")
    return results

def main():
    """Hlavní funkce"""
    print("=" * 80)
    print("ANALÝZA DAT ISVZ - HLEDÁNÍ ICT ZAKÁZEK")
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
            print(f"\n{'=' * 80}")
            print(f"Analyzuji: {file_type} ({filename})")
            print(f"{'=' * 80}")
            results = analyze_file(filepath, file_type)
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
            f.write("PŘEHLED ICT ZAKÁZEK Z ISVZ\n")
            f.write(f"Datum vytvoření: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write("=" * 80 + "\n\n")
            
            for idx, result in enumerate(all_results, 1):
                f.write(f"\n{idx}. {result['nazev']}\n")
                f.write("-" * 80 + "\n")
                f.write(f"Typ: {result['typ']}\n")
                f.write(f"Evidenční číslo: {result['evidencniCislo']}\n")
                f.write(f"Zadavatel: {result['zadavatel']}\n")
                f.write(f"Lhůta podání: {result['lhutaPodani']}\n")
                if result['celkovaHodnota'] != 'N/A':
                    f.write(f"Hodnota: {result['celkovaHodnota']}\n")
                f.write(f"URL: {result['url']}\n")
                f.write(f"\nPředmět:\n{result['predmet'][:500]}...\n")
                f.write("\n")
        
        print(f"✓ Textový report uložen do: {report_file}")
        
        # Výpis prvních 5 pro náhled
        print("\n" + "=" * 80)
        print("NÁHLED PRVNÍCH 5 ZAKÁZEK:")
        print("=" * 80)
        for idx, result in enumerate(all_results[:5], 1):
            print(f"\n{idx}. {result['nazev']}")
            print(f"   Typ: {result['typ']}")
            print(f"   Zadavatel: {result['zadavatel']}")
            print(f"   Lhůta: {result['lhutaPodani']}")
            print(f"   Evidence: {result['evidencniCislo']}")
    else:
        print("\n⚠ Nebyly nalezeny žádné relevantní ICT zakázky.")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
