"""
Prozkoumání struktury JSON souboru a identifikace nevyužitých polí.
"""

import json
import sys
import io

# Fix pro Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from collections import defaultdict
from typing import Any, Dict, Set

def explore_dict(obj: Any, prefix: str = "", found_fields: Set[str] = None, depth: int = 0, max_depth: int = 10) -> None:
    """Rekurzivně prozkoumá slovník a vypíše všechna pole."""
    if found_fields is None:
        found_fields = set()
    
    if depth > max_depth:
        return
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            field_path = f"{prefix}.{key}" if prefix else key
            if field_path not in found_fields:
                found_fields.add(field_path)
                
                # Zjisti typ hodnoty a ukázku
                if value is None:
                    value_info = "null"
                elif isinstance(value, bool):
                    value_info = f"boolean: {value}"
                elif isinstance(value, (int, float)):
                    value_info = f"number: {value}"
                elif isinstance(value, str):
                    sample = value[:100] if len(value) > 100 else value
                    value_info = f"string: \"{sample}\""
                elif isinstance(value, list):
                    if len(value) > 0:
                        value_info = f"array[{len(value)}] of {type(value[0]).__name__}"
                        # Prozkoumej první položku
                        explore_dict(value[0], f"{field_path}[0]", found_fields, depth + 1, max_depth)
                    else:
                        value_info = "array[0]"
                elif isinstance(value, dict):
                    value_info = f"object ({len(value)} keys)"
                    explore_dict(value, field_path, found_fields, depth + 1, max_depth)
                else:
                    value_info = f"other: {type(value).__name__}"
                
                if not isinstance(value, (dict, list)):
                    print(f"{'  ' * depth}{field_path}: {value_info}")
            
    elif isinstance(obj, list) and len(obj) > 0:
        explore_dict(obj[0], prefix, found_fields, depth, max_depth)


def analyze_field_usage(data: list) -> Dict[str, int]:
    """Analyzuje, jak často je které pole vyplněné."""
    field_counts = defaultdict(int)
    total = len(data)
    
    def count_fields(obj: Any, prefix: str = ""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                field_path = f"{prefix}.{key}" if prefix else key
                if value not in [None, "", [], {}]:
                    field_counts[field_path] += 1
                
                if isinstance(value, (dict, list)):
                    count_fields(value, field_path)
        elif isinstance(obj, list) and len(obj) > 0:
            count_fields(obj[0], prefix)
    
    for item in data:
        count_fields(item)
    
    return {k: (v, v/total*100) for k, v in sorted(field_counts.items(), key=lambda x: x[1], reverse=True)}


def main():
    print("=" * 80)
    print("ANALÝZA STRUKTURY JSON SOUBORU - VZ-2026-01-ICT.json")
    print("=" * 80)
    print()
    
    # Načti data
    with open('data/VZ/VZ-2026-01-ICT.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    data = json_data['data']
    print(f"Počet zakázek: {len(data)}")
    print()
    
    # Vezmi první zakázku pro strukturu
    sample = data[0]
    
    print("=" * 80)
    print("STRUKTURA PRVNÍ ZAKÁZKY")
    print("=" * 80)
    print()
    
    found = set()
    explore_dict(sample, "", found, max_depth=5)
    
    print()
    print("=" * 80)
    print("ANALÝZA VYPLNĚNOSTI POLÍ (% zakázek s neprázdnou hodnotou)")
    print("=" * 80)
    print()
    
    usage = analyze_field_usage(data)
    
    # Pole, která již používáme v reportech
    used_in_reports = {
        'verejna_zakazka.identifikator_NIPEZ',
        'verejna_zakazka.nazev_verejne_zakazky',
        'verejna_zakazka.druh_verejne_zakazky',
        'verejna_zakazka.rezim_verejne_zakazky',
        'verejna_zakazka.predpokladana_hodnota_bez_DPH_v_CZK',
        'verejna_zakazka.predmet.popis_predmetu',
        'verejna_zakazka.predmet.hlavni_kod_CPV',
        'verejna_zakazka.predmet.vedlejsi_kod_CPV',
        'verejna_zakazka.predmet.mista_plneni',
        'doporuceni'
    }
    
    print("\n🔵 POLE POUŽÍVANÁ V REPORTECH:")
    print("-" * 80)
    for field in sorted(used_in_reports):
        if field in usage:
            count, pct = usage[field]
            print(f"  ✓ {field:<70} {pct:5.1f}% ({count}/{len(data)})")
    
    print("\n🟢 UŽITEČNÁ POLE NEVYUŽITÁ V REPORTECH (>50% vyplněnost):")
    print("-" * 80)
    for field, (count, pct) in usage.items():
        if pct > 50 and field not in used_in_reports and not field.startswith('verejna_zakazka.casti'):
            print(f"  • {field:<70} {pct:5.1f}% ({count}/{len(data)})")
    
    print("\n🟡 ZAJÍMAVÁ POLE (10-50% vyplněnost):")
    print("-" * 80)
    for field, (count, pct) in usage.items():
        if 10 < pct <= 50 and field not in used_in_reports and not field.startswith('verejna_zakazka.casti'):
            print(f"  • {field:<70} {pct:5.1f}% ({count}/{len(data)})")
    
    print("\n📊 STATISTIKY SPECIFICKÝCH SEKCÍ:")
    print("-" * 80)
    
    # Analyzuj zadavací postupy
    zp_fields = {k: v for k, v in usage.items() if k.startswith('verejna_zakazka.zadavaci_postupy')}
    print(f"\n  Zadávací postupy ({len(zp_fields)} polí):")
    for field, (count, pct) in sorted(zp_fields.items(), key=lambda x: x[1][1], reverse=True)[:10]:
        field_short = field.replace('verejna_zakazka.zadavaci_postupy[0].', '...')
        print(f"    • {field_short:<68} {pct:5.1f}%")
    
    # Analyzuj části zakázky
    casti_fields = {k: v for k, v in usage.items() if k.startswith('verejna_zakazka.casti_verejne_zakazky')}
    print(f"\n  Části zakázky ({len(casti_fields)} polí):")
    for field, (count, pct) in sorted(casti_fields.items(), key=lambda x: x[1][1], reverse=True)[:10]:
        field_short = field.replace('verejna_zakazka.casti_verejne_zakazky[0].', '...')
        print(f"    • {field_short:<68} {pct:5.1f}%")


if __name__ == '__main__':
    main()
