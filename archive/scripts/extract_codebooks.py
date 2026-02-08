"""
Extrakce číselníků z ISVZ dat

Analyzuje velký JSON soubor a extrahuje všechny číselníky (pole s omezeným
počtem hodnot) včetně jejich frekvencí.
"""

import json
import sys
from collections import defaultdict, Counter
from pathlib import Path


class CodebookExtractor:
    """Extraktor číselníků z JSON struktury"""
    
    def __init__(self, max_unique_values=100):
        """
        Args:
            max_unique_values: Maximální počet unikátních hodnot pro číselník.
                              Pole s více hodnotami se považují za volný text.
        """
        self.max_unique_values = max_unique_values
        self.field_values = defaultdict(Counter)
        self.field_types = defaultdict(set)
        self.total_records = 0
        
    def extract_from_dict(self, data, path=""):
        """Rekurzivně extrahuje hodnoty z dictionary"""
        
        if not isinstance(data, dict):
            return
            
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            
            # Zpracuj hodnotu
            self._process_value(current_path, value)
            
            # Rekurzivně zpracuj vnořené struktury
            if isinstance(value, dict):
                self.extract_from_dict(value, current_path)
            elif isinstance(value, list):
                self.extract_from_list(value, current_path)
    
    def extract_from_list(self, data, path=""):
        """Extrahuje hodnoty z listu"""
        
        if not isinstance(data, list):
            return
            
        for item in data:
            if isinstance(item, dict):
                self.extract_from_dict(item, path)
            elif isinstance(item, list):
                self.extract_from_list(item, path)
            else:
                # Přímá hodnota v listu
                self._process_value(path, item)
    
    def _process_value(self, path, value):
        """Zpracuje jednotlivou hodnotu"""
        
        if value is None:
            self.field_types[path].add("null")
            return
        
        # Zaznamenej typ
        value_type = type(value).__name__
        self.field_types[path].add(value_type)
        
        # Nezpracovávej vnořené struktury
        if isinstance(value, (dict, list)):
            return
        
        # Pro číselníky zaznamenej hodnotu
        # Konvertuj na string pro snadnější práci
        if isinstance(value, bool):
            str_value = str(value)
        elif isinstance(value, (int, float)):
            # Ignoruj čísla které vypadají jako ID nebo hodnoty
            if isinstance(value, float) or abs(value) > 10000:
                return
            str_value = str(value)
        elif isinstance(value, str):
            # Ignoruj příliš dlouhé texty
            if len(value) > 200:
                return
            str_value = value
        else:
            str_value = str(value)
        
        # Zaznamenej hodnotu
        self.field_values[path][str_value] += 1
    
    def get_codebooks(self):
        """
        Vrátí pole která vypadají jako číselníky
        
        Returns:
            dict: {field_path: {value: count, ...}}
        """
        
        codebooks = {}
        
        for field_path, value_counter in self.field_values.items():
            unique_count = len(value_counter)
            
            # Je to číselník?
            if 1 <= unique_count <= self.max_unique_values:
                # Seřaď podle frekvence
                sorted_values = dict(value_counter.most_common())
                codebooks[field_path] = {
                    'unique_values': unique_count,
                    'total_occurrences': sum(value_counter.values()),
                    'values': sorted_values
                }
        
        return codebooks
    
    def get_all_fields(self):
        """Vrátí všechna nalezená pole s typy"""
        
        result = {}
        for field_path, types in self.field_types.items():
            value_count = len(self.field_values.get(field_path, {}))
            occurrence_count = sum(self.field_values.get(field_path, {}).values())
            
            result[field_path] = {
                'types': sorted(types),
                'unique_values': value_count,
                'total_occurrences': occurrence_count
            }
        
        return result


def analyze_vz_file(input_file):
    """Analyzuje VZ soubor a extrahuje číselníky"""
    
    print("=" * 70)
    print("  EXTRAKCE ČÍSELNÍKŮ Z ISVZ DAT")
    print("=" * 70)
    print()
    
    # Načti soubor
    print(f"📂 Načítám soubor: {input_file}")
    
    file_size = Path(input_file).stat().st_size / (1024 * 1024 * 1024)
    if file_size > 0.5:
        print(f"⚠️  Pozor: Soubor je velmi velký ({file_size:.1f} GB), načítání může trvat...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("✅ Soubor načten úspěšně!")
    print()
    
    # Extrahuj číselníky
    records = data.get('data', [])
    total = len(records)
    
    print(f"📊 Celkový počet záznamů: {total:,}")
    print(f"🔍 Analyzuji strukturu a extrahuji číselníky...")
    print()
    
    extractor = CodebookExtractor(max_unique_values=100)
    
    for i, record in enumerate(records, 1):
        extractor.extract_from_dict(record)
        
        if i % 10000 == 0:
            print(f"   ... zpracováno {i:,}/{total:,} záznamů ({100*i/total:.1f}%)")
    
    extractor.total_records = total
    
    print()
    print("✅ Analýza dokončena!")
    print()
    
    return extractor


def save_codebooks_markdown(extractor, output_file):
    """Uloží číselníky do markdown souboru"""
    
    codebooks = extractor.get_codebooks()
    all_fields = extractor.get_all_fields()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# ISVZ Číselníky\n\n")
        f.write(f"Extrahováno z {extractor.total_records:,} záznamů.\n\n")
        
        # Obsah
        f.write("## Obsah\n\n")
        f.write("- [Přehled všech polí](#přehled-všech-polí)\n")
        f.write("- [Číselníky (detailně)](#číselníky-detailně)\n")
        f.write("- [Důležité číselníky](#důležité-číselníky)\n\n")
        
        # Přehled všech polí
        f.write("## Přehled všech polí\n\n")
        f.write("| Pole | Typy | Unikátní hodnoty | Výskytů |\n")
        f.write("|------|------|------------------|----------|\n")
        
        for field_path in sorted(all_fields.keys()):
            info = all_fields[field_path]
            types_str = ", ".join(info['types'])
            unique = info['unique_values']
            occurrences = info['total_occurrences']
            
            # Zvýrazni číselníky
            is_codebook = field_path in codebooks
            marker = "**" if is_codebook else ""
            
            f.write(f"| {marker}{field_path}{marker} | {types_str} | {unique:,} | {occurrences:,} |\n")
        
        f.write("\n")
        
        # Důležité číselníky
        f.write("## Důležité číselníky\n\n")
        
        important_keywords = [
            'druh', 'stav', 'typ', 'forma', 'kategorie', 'vysledek',
            'kod', 'role', 'status', 'rezim', 'metoda'
        ]
        
        important_codebooks = {}
        for field_path, data in codebooks.items():
            field_lower = field_path.lower()
            if any(keyword in field_lower for keyword in important_keywords):
                important_codebooks[field_path] = data
        
        f.write(f"Nalezeno {len(important_codebooks)} důležitých číselníků:\n\n")
        
        for field_path in sorted(important_codebooks.keys()):
            data = important_codebooks[field_path]
            f.write(f"### {field_path}\n\n")
            f.write(f"- **Unikátní hodnoty**: {data['unique_values']}\n")
            f.write(f"- **Celkem výskytů**: {data['total_occurrences']:,}\n\n")
            
            f.write("| Hodnota | Počet | Podíl |\n")
            f.write("|---------|-------|-------|\n")
            
            total = data['total_occurrences']
            for value, count in data['values'].items():
                percent = 100 * count / total
                # Escapuj pipe znaky
                safe_value = str(value).replace("|", "\\|")
                f.write(f"| {safe_value} | {count:,} | {percent:.2f}% |\n")
            
            f.write("\n")
        
        # Všechny číselníky
        f.write("## Číselníky (detailně)\n\n")
        f.write(f"Celkem nalezeno {len(codebooks)} číselníků:\n\n")
        
        for field_path in sorted(codebooks.keys()):
            data = codebooks[field_path]
            
            f.write(f"### {field_path}\n\n")
            f.write(f"- **Unikátní hodnoty**: {data['unique_values']}\n")
            f.write(f"- **Celkem výskytů**: {data['total_occurrences']:,}\n\n")
            
            # Jen top 20 hodnot pro úsporu místa
            values_list = list(data['values'].items())
            show_count = min(20, len(values_list))
            
            if show_count > 0:
                f.write("| Hodnota | Počet | Podíl |\n")
                f.write("|---------|-------|-------|\n")
                
                total = data['total_occurrences']
                for value, count in values_list[:show_count]:
                    percent = 100 * count / total
                    safe_value = str(value).replace("|", "\\|")
                    f.write(f"| {safe_value} | {count:,} | {percent:.2f}% |\n")
                
                if len(values_list) > show_count:
                    f.write(f"| ... | ... | ... |\n")
                    f.write(f"| *({len(values_list) - show_count} dalších hodnot)* | | |\n")
            
            f.write("\n")
    
    print(f"💾 Číselníky uloženy: {output_file}")
    print(f"   📊 Nalezeno {len(codebooks)} číselníků")
    print(f"   📋 Celkem {len(all_fields)} různých polí")


def save_codebooks_json(extractor, output_file):
    """Uloží číselníky do JSON souboru"""
    
    codebooks = extractor.get_codebooks()
    all_fields = extractor.get_all_fields()
    
    output = {
        'total_records': extractor.total_records,
        'total_fields': len(all_fields),
        'total_codebooks': len(codebooks),
        'all_fields': all_fields,
        'codebooks': codebooks
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"💾 JSON uložen: {output_file}")


def main():
    """Hlavní funkce"""
    
    # Parametry
    input_file = "../data/VZ/VZ-2026-01.json"
    output_md = "../output/ciselniky/isvz_ciselniky.md"
    output_json = "../output/ciselniky/isvz_ciselniky.json"
    
    # Kontrola existence
    if not Path(input_file).exists():
        print(f"❌ Soubor {input_file} neexistuje!")
        sys.exit(1)
    
    # Analyzuj
    extractor = analyze_vz_file(input_file)
    
    # Ulož výsledky
    print("💾 Ukládám výsledky...")
    save_codebooks_markdown(extractor, output_md)
    save_codebooks_json(extractor, output_json)
    
    print()
    print("=" * 70)
    print("✅ HOTOVO!")
    print("=" * 70)
    print()
    print(f"📄 Výstupy:")
    print(f"   - {output_md} - Přehledná dokumentace")
    print(f"   - {output_json} - JSON data pro programové zpracování")
    print()


if __name__ == '__main__':
    main()
