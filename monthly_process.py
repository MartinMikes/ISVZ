"""
Měsíční zpracování veřejných zakázek z ISVZ.

Stahuje data, filtruje otevřené a ICT zakázky, 
a vytváří rozdílové soubory mezi měsíci.
"""

import json
import os
import sys
import io
from datetime import datetime
from pathlib import Path
import urllib.request
import argparse

# Fix pro Windows console - UTF-8 podpora emoji
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Přidej scripts do cesty pro importy
scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')
sys.path.insert(0, scripts_dir)


def download_file(url, dest_path):
    """Stáhne soubor z URL"""
    print(f"📥 Stahuji: {url}")
    try:
        urllib.request.urlretrieve(url, dest_path)
        file_size = os.path.getsize(dest_path)
        size_mb = file_size / (1024 * 1024)
        print(f"✅ Staženo: {dest_path} ({size_mb:.1f} MB)")
        return True
    except Exception as e:
        print(f"❌ Chyba při stahování: {e}")
        return False


def download_month_data(year, month, data_dir="data", skip_vz=True):
    """
    Stáhne data pro daný měsíc do odpovídajících podsložek.
    
    Args:
        year: Rok (např. 2026)
        month: Měsíc (1-12)
        data_dir: Základní adresář pro data
        skip_vz: Přeskočit velký VZ soubor (doporučeno, stáhnout ručně)
    """
    
    # Vytvoř adresáře pokud neexistují
    Path(data_dir).mkdir(exist_ok=True)
    for category in ['VZ', 'DNS', 'SON', 'SK', 'RVP']:
        Path(os.path.join(data_dir, category)).mkdir(exist_ok=True)
    
    # URL base
    base_url = f"https://isvz.nipez.cz/sites/default/files/content/opendata-rvz"
    
    # Seznam souborů s jejich kategoriemi
    # Nový formát: KATEGORIE-YYYY-MM.json (pro lepší chronologické řazení)
    month_str = f"{month:02d}"
    files = [
        ('VZ', f"VZ-{year}-{month_str}.json"),
        ('DNS', f"DNS-{year}-{month_str}.json"),
        ('SON', f"SON-{year}-{month_str}.json"),
        ('SK', f"SK-{year}-{month_str}.json"),
        ('RVP', f"RVP-{year}-{month_str}.json")
    ]
    
    print(f"\n{'='*70}")
    print(f"  STAHOVÁNÍ DAT PRO {month}/{year}")
    print(f"{'='*70}\n")
    
    success_count = 0
    
    for category, filename in files:
        # Přeskočit VZ pokud je velký
        if skip_vz and filename.startswith("VZ-"):
            print(f"⚠️  Přeskakuji {filename} (velký soubor - stáhněte ručně)")
            print(f"   URL: {base_url}/{filename}")
            continue
        
        url = f"{base_url}/{filename}"
        dest = os.path.join(data_dir, category, filename)
        
        # Přeskočit pokud už existuje
        if os.path.exists(dest):
            print(f"⏭️  Existuje: {category}/{filename}")
            success_count += 1
            continue
        
        if download_file(url, dest):
            success_count += 1
    
    print(f"\n✅ Staženo {success_count} souborů")
    
    return success_count > 0


def process_month(year, month, data_dir="data"):
    """
    Zpracuje data pro daný měsíc.
    
    1. Filtruje otevřené zakázky z VZ
    2. Filtruje ICT zakázky z VZ
    3. Filtruje ICT zakázky z DNS
    """
    
    month_str = f"{month:02d}"
    
    # VZ soubory v podsložce VZ/ - nový formát YYYY-MM
    vz_input = os.path.join(data_dir, "VZ", f"VZ-{year}-{month_str}.json")
    vz_open = os.path.join(data_dir, "VZ", f"VZ-{year}-{month_str}-OPEN.json")
    vz_ict = os.path.join(data_dir, "VZ", f"VZ-{year}-{month_str}-ICT.json")
    
    # DNS soubory v podsložce DNS/ - nový formát YYYY-MM
    dns_input = os.path.join(data_dir, "DNS", f"DNS-{year}-{month_str}.json")
    dns_ict = os.path.join(data_dir, "DNS", f"DNS-{year}-{month_str}-ICT.json")
    
    print(f"\n{'='*70}")
    print(f"  ZPRACOVÁNÍ DAT PRO {month}/{year}")
    print(f"{'='*70}\n")
    
    success = True
    
    # ===== VZ ZPRACOVÁNÍ =====
    
    # Zkontroluj zda existuje VZ soubor
    if not os.path.exists(vz_input):
        print(f"⚠️  Soubor {vz_input} neexistuje!")
        print(f"   Stáhněte ho ručně z:")
        print(f"   https://isvz.nipez.cz/sites/default/files/content/opendata-rvz/VZ-{year}-{month_str}.json")
        success = False
    else:
        # Krok 1: Filtrování otevřených zakázek
        print("🔍 KROK 1: Filtrování otevřených zakázek (VZ)\n")
        
        from filter_open_tenders import filter_open_tenders
        try:
            filter_open_tenders(vz_input, vz_open)
        except Exception as e:
            print(f"❌ Chyba při filtrování otevřených zakázek: {e}")
            success = False
        
        # Krok 2: Filtrování ICT zakázek z VZ
        if success:
            print(f"\n{'='*70}")
            print("🔍 KROK 2: Filtrování ICT zakázek (VZ)\n")
            
            from filter_ict_tenders import filter_ict_tenders
            try:
                filter_ict_tenders(vz_open, vz_ict)
            except Exception as e:
                print(f"❌ Chyba při filtrování ICT zakázek: {e}")
                success = False
    
    # ===== DNS ZPRACOVÁNÍ =====
    
    # Zkontroluj zda existuje DNS soubor
    if os.path.exists(dns_input):
        print(f"\n{'='*70}")
        print("🔍 KROK 3: Filtrování ICT z DNS\n")
        
        from filter_dns_ict import filter_dns_ict_tenders
        try:
            filter_dns_ict_tenders(dns_input, dns_ict)
        except Exception as e:
            print(f"❌ Chyba při filtrování DNS ICT: {e}")
            # Ne-kritická chyba, pokračuj
    else:
        print(f"\n⚠️  Soubor {dns_input} neexistuje - přeskakuji DNS")
    
    # ===== PŘIDÁNÍ DOPORUČENÍ =====
    
    if success:
        print(f"\n{'='*70}")
        print("🔍 KROK 4: Přidávání doporučení k ICT zakázkám\n")
        
        from add_recommendations import add_recommendations
        try:
            # Přepíše VZ-*-ICT.json s doporučeními
            add_recommendations(vz_ict, vz_ict)
            
            # Také DNS pokud existuje
            if os.path.exists(dns_ict):
                add_recommendations(dns_ict, dns_ict)
        except Exception as e:
            print(f"❌ Chyba při přidávání doporučení: {e}")
            # Ne-kritická chyba, pokračuj
    
    # ===== GENEROVÁNÍ REPORTŮ =====
    
    if success:
        print(f"\n{'='*70}")
        print("🔍 KROK 5: Generování reportů (MD + CSV)\n")
        
        from generate_reports import generate_reports_for_month
        try:
            generate_reports_for_month(year, month, data_dir, "output")
        except Exception as e:
            print(f"❌ Chyba při generování reportů: {e}")
            # Ne-kritická chyba, pokračuj
    
    # Souhrn
    if success:
        print(f"\n{'='*70}")
        print(f"✅ Zpracování dokončeno!")
        print(f"{'='*70}")
        print(f"\n📁 Výstupní soubory:")
        if os.path.exists(vz_open):
            print(f"   - {vz_open}")
        if os.path.exists(vz_ict):
            print(f"   - {vz_ict}")
        if os.path.exists(dns_ict):
            print(f"   - {dns_ict}")
    
    return success


def get_previous_month(year, month):
    """
    Vrátí předchozí měsíc a rok.
    
    Args:
        year: Rok (např. 2026)
        month: Měsíc 1-12 (např. 1)
    
    Returns:
        tuple: (předchozí_rok, předchozí_měsíc)
    """
    if month > 1:
        return (year, month - 1)
    else:
        return (year - 1, 12)


def compare_months(year1, month1, year2=None, month2=None, data_dir="data", output_dir="output/reports"):
    """
    Porovná ICT zakázky mezi dvěma měsíci.
    
    Pokud není zadán year2/month2, automaticky se použije předchozí měsíc.
    
    Args:
        year1, month1: Starší měsíc (nebo pokud year2/month2 není zadáno, tak novější)
        year2, month2: Novější měsíc (nepovinné - auto-vypočítá se předchozí)
    
    Porovnává VZ i DNS kategorie a vytvoří rozdílové reporty.
    """
    
    # Pokud není zadán druhý měsíc, automaticky určíme předchozí
    if year2 is None or month2 is None:
        # year1/month1 je NOVĚJŠÍ měsíc
        year2, month2 = year1, month1
        year1, month1 = get_previous_month(year2, month2)
    
    month1_str = f"{month1:02d}"
    month2_str = f"{month2:02d}"
    
    print(f"\n{'='*70}")
    print(f"  POROVNÁNÍ MĚSÍCŮ")
    print(f"{'='*70}\n")
    print(f"📅 Starší: {month1}/{year1}")
    print(f"📅 Novější: {month2}/{year2}\n")
    
    Path(output_dir).mkdir(exist_ok=True)
    
    # Porovnání VZ - soubory v podsložce VZ/ - nový formát YYYY-MM
    vz_file1 = os.path.join(data_dir, "VZ", f"VZ-{year1}-{month1_str}-ICT.json")
    vz_file2 = os.path.join(data_dir, "VZ", f"VZ-{year2}-{month2_str}-ICT.json")
    
    if os.path.exists(vz_file1) and os.path.exists(vz_file2):
        print("🔍 Porovnávám VZ (Veřejné zakázky)...")
        compare_category(vz_file1, vz_file2, "VZ", year1, month1, year2, month2, output_dir)
    else:
        print(f"⚠️  VZ soubory neexistují pro porovnání")
    
    # Porovnání DNS - soubory v podsložce DNS/ - nový formát YYYY-MM
    dns_file1 = os.path.join(data_dir, "DNS", f"DNS-{year1}-{month1_str}-ICT.json")
    dns_file2 = os.path.join(data_dir, "DNS", f"DNS-{year2}-{month2_str}-ICT.json")
    
    if os.path.exists(dns_file1) and os.path.exists(dns_file2):
        print("\n🔍 Porovnávám DNS (Dynamické nákupní systémy)...")
        compare_category_dns(dns_file1, dns_file2, "DNS", year1, month1, year2, month2, output_dir)
    else:
        print(f"⚠️  DNS soubory neexistují pro porovnání")
    
    return True


def compare_category(file1, file2, category, y1, m1, y2, m2, output_dir):
    """Porovná jednu kategorii (VZ)"""
    
    # Načti data
    with open(file1, 'r', encoding='utf-8') as f:
        data1 = json.load(f)
    
    with open(file2, 'r', encoding='utf-8') as f:
        data2 = json.load(f)
    
    zakazky1 = data1.get('data', [])
    zakazky2 = data2.get('data', [])
    
    # Vytvoř mapu ID -> zakázka
    map1 = {}
    for z in zakazky1:
        vz = z.get('verejna_zakazka', {})
        id_nipez = vz.get('identifikator_NIPEZ')
        if id_nipez:
            map1[id_nipez] = z
    
    map2 = {}
    for z in zakazky2:
        vz = z.get('verejna_zakazka', {})
        id_nipez = vz.get('identifikator_NIPEZ')
        if id_nipez:
            map2[id_nipez] = z
    
    # Najdi rozdíly
    ids1 = set(map1.keys())
    ids2 = set(map2.keys())
    
    nove = ids2 - ids1
    zmizele = ids1 - ids2
    spolecne = ids1 & ids2
    
    print(f"   Zakázek v {m1}/{y1}: {len(zakazky1)}")
    print(f"   Zakázek v {m2}/{y2}: {len(zakazky2)}")
    print(f"   Nové: {len(nove)} | Zmizely: {len(zmizele)} | Společné: {len(spolecne)}")
    
    # Vytvoř report - kratší název (jen aktuální měsíc)
    diff_file = os.path.join(
        output_dir,
        f"DIFF_{category}_{m2:02d}-{y2}.md"
    )
    
    save_diff_report_vz(diff_file, map1, map2, nove, zmizele, spolecne, 
                        category, y1, m1, y2, m2, len(zakazky1), len(zakazky2))
    
    print(f"   💾 Report: {diff_file}")


def compare_category_dns(file1, file2, category, y1, m1, y2, m2, output_dir):
    """Porovná DNS kategorii"""
    
    # Načti data
    with open(file1, 'r', encoding='utf-8') as f:
        data1 = json.load(f)
    
    with open(file2, 'r', encoding='utf-8') as f:
        data2 = json.load(f)
    
    zakazky1 = data1.get('data', [])
    zakazky2 = data2.get('data', [])
    
    # Vytvoř mapu ID -> záznam
    map1 = {}
    for z in zakazky1:
        dns = z.get('dynamicky_nakupni_system', {})
        id_nipez = dns.get('identifikator_NIPEZ')
        if id_nipez:
            map1[id_nipez] = z
    
    map2 = {}
    for z in zakazky2:
        dns = z.get('dynamicky_nakupni_system', {})
        id_nipez = dns.get('identifikator_NIPEZ')
        if id_nipez:
            map2[id_nipez] = z
    
    # Najdi rozdíly
    ids1 = set(map1.keys())
    ids2 = set(map2.keys())
    
    nove = ids2 - ids1
    zmizele = ids1 - ids2
    spolecne = ids1 & ids2
    
    print(f"   Záznamů v {m1}/{y1}: {len(zakazky1)}")
    print(f"   Záznamů v {m2}/{y2}: {len(zakazky2)}")
    print(f"   Nové: {len(nove)} | Zmizely: {len(zmizele)} | Společné: {len(spolecne)}")
    
    # Vytvoř report - kratší název (jen aktuální měsíc)
    diff_file = os.path.join(
        output_dir,
        f"DIFF_{category}_{m2:02d}-{y2}.md"
    )
    
    save_diff_report_dns(diff_file, map1, map2, nove, zmizele, spolecne,
                         category, y1, m1, y2, m2, len(zakazky1), len(zakazky2))
    
    print(f"   💾 Report: {diff_file}")


def save_diff_report_vz(file_path, map1, map2, nove, zmizele, spolecne,
                        category, y1, m1, y2, m2, count1, count2):
    """Uloží rozdílový report pro VZ"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"# Rozdílový report ICT {category}\n\n")
        f.write(f"**Období**: {m1}/{y1} → {m2}/{y2}\n\n")
        f.write(f"## Souhrn\n\n")
        f.write(f"| Kategorie | Počet |\n")
        f.write(f"|-----------|-------|\n")
        f.write(f"| Zakázky v {m1}/{y1} | {count1} |\n")
        f.write(f"| Zakázky v {m2}/{y2} | {count2} |\n")
        f.write(f"| **Nové zakázky** | **{len(nove)}** |\n")
        f.write(f"| **Zmizely** | **{len(zmizele)}** |\n")
        f.write(f"| Společné | {len(spolecne)} |\n\n")
        
        # Nové zakázky
        if nove:
            f.write(f"## ✅ Nové zakázky ({len(nove)})\n\n")
            for i, id_nipez in enumerate(sorted(nove), 1):
                z = map2[id_nipez]
                vz = z.get('verejna_zakazka', {})
                
                f.write(f"### {i}. {id_nipez}\n\n")
                f.write(f"**Název**: {vz.get('nazev_verejne_zakazky', 'N/A')}\n\n")
                f.write(f"- **Druh**: {vz.get('druh_verejne_zakazky', 'N/A')}\n")
                
                hodnota = vz.get('predpokladana_hodnota_bez_DPH_v_CZK')
                if hodnota:
                    f.write(f"- **Hodnota**: {hodnota:,.0f} Kč\n")
                
                # Lhůta
                for cast in vz.get('casti_verejne_zakazky', []):
                    zp = cast.get('zadavaci_postup_pro_cast', {})
                    for lhuta in zp.get('lhuty', []):
                        if 'podání nabíd' in lhuta.get('druh_lhuty', ''):
                            datum_konce = lhuta.get('datum_a_cas_konce_lhuty')
                            if datum_konce:
                                f.write(f"- **Lhůta**: {datum_konce}\n")
                                break
                    break
                
                f.write("\n")
        
        # Zmizely
        if zmizele:
            f.write(f"## ❌ Zmizely ({len(zmizele)})\n\n")
            for i, id_nipez in enumerate(sorted(zmizele), 1):
                z = map1[id_nipez]
                vz = z.get('verejna_zakazka', {})
                
                f.write(f"### {i}. {id_nipez}\n\n")
                f.write(f"**Název**: {vz.get('nazev_verejne_zakazky', 'N/A')}\n\n")
                f.write(f"- **Druh**: {vz.get('druh_verejne_zakazky', 'N/A')}\n\n")


def save_diff_report_dns(file_path, map1, map2, nove, zmizele, spolecne,
                         category, y1, m1, y2, m2, count1, count2):
    """Uloží rozdílový report pro DNS"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"# Rozdílový report ICT {category}\n\n")
        f.write(f"**Období**: {m1}/{y1} → {m2}/{y2}\n\n")
        f.write(f"## Souhrn\n\n")
        f.write(f"| Kategorie | Počet |\n")
        f.write(f"|-----------|-------|\n")
        f.write(f"| Záznamy v {m1}/{y1} | {count1} |\n")
        f.write(f"| Záznamy v {m2}/{y2} | {count2} |\n")
        f.write(f"| **Nové** | **{len(nove)}** |\n")
        f.write(f"| **Zmizely** | **{len(zmizele)}** |\n")
        f.write(f"| Společné | {len(spolecne)} |\n\n")
        
        # Nové
        if nove:
            f.write(f"## ✅ Nové DNS ({len(nove)})\n\n")
            for i, id_nipez in enumerate(sorted(nove), 1):
                z = map2[id_nipez]
                dns = z.get('dynamicky_nakupni_system', {})
                
                f.write(f"### {i}. {id_nipez}\n\n")
                f.write(f"**Název**: {dns.get('nazev_dynamickeho_nakupniho_systemu', 'N/A')}\n\n")
                
                zp = dns.get('zadavaci_postup_pro_zavedeni_dynamickeho_nakupniho_systemu', {})
                predmet = zp.get('predmet', {})
                cpv = predmet.get('hlavni_kod_CPV')
                if cpv:
                    f.write(f"- **CPV**: {cpv}\n")
                
                f.write("\n")
        
        # Zmizely
        if zmizele:
            f.write(f"## ❌ Zmizely ({len(zmizele)})\n\n")
            for i, id_nipez in enumerate(sorted(zmizele), 1):
                z = map1[id_nipez]
                dns = z.get('dynamicky_nakupni_system', {})
                
                f.write(f"### {i}. {id_nipez}\n\n")
                f.write(f"**Název**: {dns.get('nazev_dynamickeho_nakupniho_systemu', 'N/A')}\n\n")


def main():
    """Hlavní funkce"""
    
    parser = argparse.ArgumentParser(
        description="Měsíční zpracování veřejných zakázek z ISVZ"
    )
    
    parser.add_argument(
        '--year', '-y',
        type=int,
        default=datetime.now().year,
        help='Rok (výchozí: aktuální rok)'
    )
    
    parser.add_argument(
        '--month', '-m',
        type=int,
        default=datetime.now().month,
        help='Měsíc 1-12 (výchozí: aktuální měsíc)'
    )
    
    parser.add_argument(
        '--download', '-d',
        action='store_true',
        help='Stáhnout data před zpracováním'
    )
    
    parser.add_argument(
        '--compare', '-c',
        nargs='+',
        metavar=('YEAR', 'MONTH'),
        help='Porovnat měsíce: --compare 2026 1 (auto předchozí) nebo --compare 2025 12 2026 1'
    )

    parser.add_argument(
        '--data-dir',
        default='data',
        help='Adresář s daty (výchozí: data)'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("  MĚSÍČNÍ ZPRACOVÁNÍ VEŘEJNÝCH ZAKÁZEK - ISVZ")
    print("=" * 70)

    # Porovnání dvou měsíců
    if args.compare:
        if len(args.compare) == 2:
            # Pouze rok a měsíc -> auto předchozí měsíc
            year, month = map(int, args.compare)
            compare_months(year, month, data_dir=args.data_dir)
        elif len(args.compare) == 4:
            # Kompletní specifikace obou měsíců
            y1, m1, y2, m2 = map(int, args.compare)
            compare_months(y1, m1, y2, m2, args.data_dir)
        else:
            print("❌ Chyba: --compare vyžaduje 2 nebo 4 argumenty")
            print("   Příklady:")
            print("     --compare 2026 1           (porovná s předchozím měsícem)")
            print("     --compare 2025 12 2026 1   (porovná zadané měsíce)")
            return
        return
    
    # Stahování
    if args.download:
        download_month_data(args.year, args.month, args.data_dir)
    
    # Zpracování
    process_month(args.year, args.month, args.data_dir)


if __name__ == '__main__':
    main()
