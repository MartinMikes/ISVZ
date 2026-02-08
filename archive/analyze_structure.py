import json
import sys
from collections import defaultdict

def analyze_json_structure(file_path, sample_size=10):
    """Analyzuje strukturu JSON souboru a vrátí datový model"""
    
    print(f"Načítám soubor {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        # Načteme jen metadata a několik prvních záznamů
        data = json.load(f)
    
    print(f"Soubor načten. Analyzuji strukturu...")
    
    result = {
        'metadata': {},
        'schema': {},
        'sample_values': {},
        'statistics': {}
    }
    
    # Metadata
    for key in data:
        if key != 'data':
            result['metadata'][key] = data[key]
    
    # Zjistíme počet zakázek
    zakazky = data.get('data', [])
    result['statistics']['total_count'] = len(zakazky)
    
    print(f"Celkem zakázek: {len(zakazky)}")
    
    # Analyzujeme strukturu na vzorku
    def get_structure(obj, prefix='', depth=0):
        """Rekurzivně analyzuje strukturu objektu"""
        structure = {}
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                full_key = f"{prefix}.{key}" if prefix else key
                
                if value is None:
                    structure[full_key] = 'null'
                elif isinstance(value, bool):
                    structure[full_key] = 'boolean'
                elif isinstance(value, int):
                    structure[full_key] = 'integer'
                elif isinstance(value, float):
                    structure[full_key] = 'float'
                elif isinstance(value, str):
                    structure[full_key] = 'string'
                elif isinstance(value, list):
                    if len(value) > 0:
                        structure[full_key] = f'array[{type(value[0]).__name__}]'
                        if isinstance(value[0], dict) and depth < 5:
                            # Analyzujeme první prvek pole
                            nested = get_structure(value[0], full_key, depth + 1)
                            structure.update(nested)
                    else:
                        structure[full_key] = 'array[]'
                elif isinstance(value, dict) and depth < 5:
                    structure[full_key] = 'object'
                    nested = get_structure(value, full_key, depth + 1)
                    structure.update(nested)
        
        return structure
    
    # Sbíráme hodnoty pro klíčová pole
    key_fields = defaultdict(set)
    
    for i, zakazka in enumerate(zakazky[:sample_size]):
        if i == 0:
            # První zakázka - kompletní struktura
            result['schema'] = get_structure(zakazka)
        
        # Sbíráme hodnoty pro klíčová pole
        vz = zakazka.get('verejna_zakazka', {})
        
        # Režim
        if vz.get('rezim_verejne_zakazky'):
            key_fields['rezim_verejne_zakazky'].add(vz['rezim_verejne_zakazky'])
        
        # Druh
        if vz.get('druh_verejne_zakazky'):
            key_fields['druh_verejne_zakazky'].add(vz['druh_verejne_zakazky'])
        
        # Typ
        if vz.get('typ_verejne_zakazky_dle_vyse_predpokladane_hodnoty'):
            key_fields['typ_verejne_zakazky'].add(vz['typ_verejne_zakazky_dle_vyse_predpokladane_hodnoty'])
        
        # Fáze (pokud existuje)
        if 'faze' in zakazka:
            for faze in zakazka.get('faze', []):
                if isinstance(faze, dict):
                    if faze.get('kod_faze'):
                        key_fields['kod_faze'].add(faze['kod_faze'])
                    if faze.get('nazev_faze'):
                        key_fields['nazev_faze'].add(faze['nazev_faze'])
                    if faze.get('stav'):
                        key_fields['stav_faze'].add(faze['stav'])
        
        # Nabídky
        if 'nabidky' in zakazka:
            nabidky = zakazka.get('nabidky', [])
            if nabidky and isinstance(nabidky, list):
                for nabidka in nabidky[:3]:
                    if isinstance(nabidka, dict) and 'stav' in nabidka:
                        key_fields['stav_nabidky'].add(nabidka['stav'])
        
        # Zjistíme dostupné top-level klíče
        for key in zakazka.keys():
            key_fields['top_level_keys'].add(key)
    
    # Převedeme sety na seznamy pro JSON
    result['sample_values'] = {k: sorted(list(v)) for k, v in key_fields.items()}
    
    # Vzorová zakázka
    if zakazky:
        result['sample_record'] = zakazky[0]
    
    return result

def save_markdown_report(analysis, output_file):
    """Uloží analýzu do markdown souboru"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Datový model ISVZ - VZ-01-2026.json\n\n")
        
        # Metadata
        f.write("## Metadata souboru\n\n")
        for key, value in analysis['metadata'].items():
            f.write(f"- **{key}**: {value}\n")
        
        # Statistiky
        f.write("\n## Statistiky\n\n")
        f.write(f"- **Celkový počet zakázek**: {analysis['statistics']['total_count']}\n")
        
        # Možné hodnoty klíčových polí
        f.write("\n## Klíčová pole pro filtrování\n\n")
        
        if 'top_level_keys' in analysis['sample_values']:
            f.write("### Dostupné sekce v záznamu zakázky\n\n")
            for key in analysis['sample_values']['top_level_keys']:
                f.write(f"- `{key}`\n")
            f.write("\n")
        
        if 'rezim_verejne_zakazky' in analysis['sample_values']:
            f.write("### Režim veřejné zakázky\n\n")
            for value in analysis['sample_values']['rezim_verejne_zakazky']:
                f.write(f"- `{value}`\n")
            f.write("\n")
        
        if 'druh_verejne_zakazky' in analysis['sample_values']:
            f.write("### Druh veřejné zakázky\n\n")
            for value in analysis['sample_values']['druh_verejne_zakazky']:
                f.write(f"- `{value}`\n")
            f.write("\n")
        
        if 'typ_verejne_zakazky' in analysis['sample_values']:
            f.write("### Typ veřejné zakázky\n\n")
            for value in analysis['sample_values']['typ_verejne_zakazky']:
                f.write(f"- `{value}`\n")
            f.write("\n")
        
        if 'kod_faze' in analysis['sample_values']:
            f.write("### Kód fáze\n\n")
            for value in analysis['sample_values']['kod_faze']:
                f.write(f"- `{value}`\n")
            f.write("\n")
        
        if 'nazev_faze' in analysis['sample_values']:
            f.write("### Název fáze\n\n")
            for value in analysis['sample_values']['nazev_faze']:
                f.write(f"- `{value}`\n")
            f.write("\n")
        
        if 'stav_faze' in analysis['sample_values']:
            f.write("### Stav fáze\n\n")
            for value in analysis['sample_values']['stav_faze']:
                f.write(f"- `{value}`\n")
            f.write("\n")
        
        if 'stav_nabidky' in analysis['sample_values']:
            f.write("### Stav nabídky\n\n")
            for value in analysis['sample_values']['stav_nabidky']:
                f.write(f"- `{value}`\n")
            f.write("\n")
        
        # Struktura dat
        f.write("\n## Struktura datového modelu\n\n")
        f.write("### Hierarchie polí\n\n")
        f.write("```\n")
        
        # Setřídíme pole hierarchicky
        sorted_fields = sorted(analysis['schema'].items())
        for field, field_type in sorted_fields:
            depth = field.count('.')
            indent = '  ' * depth
            field_name = field.split('.')[-1]
            f.write(f"{indent}{field_name}: {field_type}\n")
        
        f.write("```\n\n")
        
        # Ukázka záznamu
        f.write("\n## Ukázka záznamu (zkrácená)\n\n")
        f.write("```json\n")
        
        # Vytiskneme zkrácenou verzi prvního záznamu
        sample = analysis.get('sample_record', {})
        if 'verejna_zakazka' in sample:
            vz = sample['verejna_zakazka']
            sample_short = {
                'verejna_zakazka': {
                    'identifikator_NIPEZ': vz.get('identifikator_NIPEZ'),
                    'nazev_verejne_zakazky': vz.get('nazev_verejne_zakazky'),
                    'druh_verejne_zakazky': vz.get('druh_verejne_zakazky'),
                    'rezim_verejne_zakazky': vz.get('rezim_verejne_zakazky'),
                    'typ_verejne_zakazky_dle_vyse_predpokladane_hodnoty': vz.get('typ_verejne_zakazky_dle_vyse_predpokladane_hodnoty'),
                    'predpokladana_hodnota_bez_DPH_v_CZK': vz.get('predpokladana_hodnota_bez_DPH_v_CZK'),
                }
            }
            if 'faze' in sample:
                sample_short['faze'] = sample.get('faze', [])[:1]
            
            f.write(json.dumps(sample_short, indent=2, ensure_ascii=False))
        
        f.write("\n```\n")

if __name__ == '__main__':
    file_path = 'isvz_data/VZ-01-2026.json'
    output_file = 'isvz_datamodel.md'
    
    print("Spouštím analýzu datového modelu...")
    analysis = analyze_json_structure(file_path, sample_size=50)
    
    print(f"Ukládám report do {output_file}...")
    save_markdown_report(analysis, output_file)
    
    print("Hotovo!")
