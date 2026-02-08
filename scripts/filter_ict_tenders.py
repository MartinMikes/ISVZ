"""
Filtrování ICT veřejných zakázek z otevřených zakázek.

Načte otevřené zakázky a vyfiltruje pouze ty související s ICT,
programováním, softwarem, IT službami, atd.
"""

import json
from datetime import datetime
import re
import sys
import io

# Fix pro Windows console - UTF-8 podpora emoji (jen pokud běží standalone)
if sys.platform == 'win32' and not hasattr(sys.stdout, 'buffer'):
    pass  # Už je wrapped
elif sys.platform == 'win32' and hasattr(sys.stdout, 'buffer') and 'TextIOWrapper' not in str(type(sys.stdout)):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ICT klíčová slova pro vyhledávání
ICT_KEYWORDS = {
    # Software a vývoj
    'software', 'aplikace', 'app', 'program', 'vývoj', 'development',
    'kodování', 'coding', 'programování', 'programming',
    
    # IT služby
    'informační systém', 'is', 'it', 'ict', 'digitalizace',
    'cloud', 'saas', 'paas', 'iaas',
    
    # Webové technologie
    'web', 'webová aplikace', 'webové služby', 'website', 'portal', 'portál',
    'cms', 'e-shop', 'eshop', 'e-commerce',
    
    # Databáze
    'databáze', 'database', 'sql', 'nosql', 'oracle', 'postgresql', 'mysql',
    'mongodb', 'datové úložiště', 'data warehouse',
    
    # Správa IT
    'správa sítí', 'síťová infrastruktura', 'server', 'hosting',
    'it podpora', 'helpdesk', 'servicedesk', 'správa systémů',
    
    # Bezpečnost
    'kyberbezpečnost', 'cybersecurity', 'kybernetická bezpečnost',
    'zabezpečení dat', 'firewall', 'antivir',
    
    # Specifické technologie
    'microsoft', 'office 365', 'azure', 'aws', 'google cloud',
    'vmware', 'kubernetes', 'docker', 'api',
    
    # Dokumentové systémy
    'elektronická spisová služba', 'ess', 'essl', 'spisová služba',
    'elektronické podání', 'datové schránky', 'czech point',
    
    # Licences
    'softwarová licence', 'licence', 'předplatné software',
    
    # Další IT oblasti
    'mobilní aplikace', 'mobile app', 'desktop aplikace',
    'testování software', 'qa', 'quality assurance',
    'uživatelská dokumentace', 'technická dokumentace',
    'školení uživatelů', 'it školení',
}

# CPV kódy pro ICT
ICT_CPV_CODES = {
    '48': 'Softwarové balíky a informační systémy',
    '72': 'Služby v oblasti informačních technologií',
    '30200000': 'Zařízení počítačové',
    '30230000': 'Zařízení související s počítači',
    '48000000': 'Softwarové balíky a informační systémy',
    '48100000': 'Průmyslově specifické softwarové balíky',
    '48200000': 'Softwarové balíky pro síťové připojení a internet',
    '48300000': 'Softwarové balíky pro sestavování dokumentů',
    '48400000': 'Softwarové balíky pro transakce v obchodování',
    '48500000': 'Komunikační a multimediální softwarové balíky',
    '48600000': 'Databázové a operační softwarové balíky',
    '48700000': 'Softwarové balíky pro hry a vzdělávání',
    '48800000': 'Informační systémy a servery',
    '48900000': 'Softwarové balíky pro různé podnikové činnosti',
    '72000000': 'Služby v oblasti informačních technologií',
    '72100000': 'Služby v oblasti hardware',
    '72200000': 'Služby v oblasti software',
    '72300000': 'Služby v oblasti zpracování dat',
    '72400000': 'Služby v oblasti internetu',
    '72500000': 'Služby v oblasti počítačů',
    '72600000': 'Služby v oblasti počítačové podpory a poradenství',
}


def contains_ict_keywords(text):
    """Kontrola, zda text obsahuje ICT klíčová slova"""
    if not text:
        return False
    
    text_lower = text.lower()
    
    for keyword in ICT_KEYWORDS:
        # Použijeme word boundary pro přesné vyhledávání
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        if re.search(pattern, text_lower):
            return True
    
    return False


def has_ict_cpv_code(cpv_code):
    """Kontrola, zda CPV kód patří do ICT"""
    if not cpv_code:
        return False
    
    # CPV kód může být string nebo má být prefix některého z ICT kódů
    cpv_str = str(cpv_code)
    
    for ict_code in ICT_CPV_CODES.keys():
        if cpv_str.startswith(ict_code):
            return True
    
    return False


def is_ict_tender(zakazka):
    """
    Kontrola, zda je zakázka ICT.
    
    Kontroluje:
    1. Název zakázky
    2. Popis předmětu
    3. CPV kódy (hlavní i vedlejší)
    4. Vyloučení stavebních prací
    """
    vz = zakazka.get('verejna_zakazka', {})
    
    # Vyloučit stavební práce
    druh = vz.get('druh_verejne_zakazky', '')
    if druh == 'Stavební práce':
        return False
    
    # 1. Kontrola názvu
    nazev = vz.get('nazev_verejne_zakazky', '')
    if contains_ict_keywords(nazev):
        return True
    
    # 2. Kontrola popisu předmětu
    predmet = vz.get('predmet', {})
    popis = predmet.get('popis_predmetu', '')
    if contains_ict_keywords(popis):
        return True
    
    # 3. Kontrola hlavního CPV kódu
    hlavni_cpv = predmet.get('hlavni_kod_CPV', '')
    if has_ict_cpv_code(hlavni_cpv):
        return True
    
    # 4. Kontrola vedlejších CPV kódů
    vedlejsi_cpv = predmet.get('vedlejsi_kod_CPV', [])
    for cpv in vedlejsi_cpv:
        if has_ict_cpv_code(cpv):
            return True
    
    # 5. Kontrola částí zakázky
    for cast in vz.get('casti_verejne_zakazky', []):
        # Název části
        nazev_casti = cast.get('nazev_casti_verejne_zakazky', '')
        if contains_ict_keywords(nazev_casti):
            return True
        
        # Předmět části
        predmet_casti = cast.get('predmet', {})
        popis_casti = predmet_casti.get('popis_predmetu', '')
        if contains_ict_keywords(popis_casti):
            return True
        
        # CPV kódy části
        hlavni_cpv_casti = predmet_casti.get('hlavni_kod_CPV', '')
        if has_ict_cpv_code(hlavni_cpv_casti):
            return True
        
        vedlejsi_cpv_casti = predmet_casti.get('vedlejsi_kod_CPV', [])
        for cpv in vedlejsi_cpv_casti:
            if has_ict_cpv_code(cpv):
                return True
    
    return False


def filter_ict_tenders(input_file, output_file):
    """Načte otevřené zakázky a vyfiltruje ICT zakázky"""
    
    print(f"📂 Načítám soubor: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Soubor načten úspěšně!")
    except Exception as e:
        print(f"❌ CHYBA při načítání souboru: {e}")
        return
    
    # Metadata
    metadata = data.get('metadata', {})
    original_count = len(data.get('data', []))
    
    print(f"\n📊 Počet otevřených zakázek: {original_count}")
    print(f"🔍 Filtrování ICT zakázek...")
    
    # Filtrování
    zakazky = data.get('data', [])
    ict_tenders = []
    
    for zakazka in zakazky:
        if is_ict_tender(zakazka):
            ict_tenders.append(zakazka)
    
    print(f"\n✅ Filtrování dokončeno!")
    print(f"📈 Nalezeno {len(ict_tenders)} ICT zakázek")
    print(f"📉 Odfiltrováno {original_count - len(ict_tenders)} ne-ICT zakázek")
    print(f"📊 Úspěšnost: {len(ict_tenders)/original_count*100:.2f}% zakázek je ICT")
    
    # Sestavení výstupního JSON
    output_metadata = metadata.copy()
    output_metadata['filtrovano_ict_datum'] = datetime.now().isoformat()
    output_metadata['pred_ict_filtrem'] = original_count
    output_metadata['po_ict_filtru'] = len(ict_tenders)
    
    output_data = {
        'metadata': output_metadata,
        'data': ict_tenders
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
        if file_size < 1024*1024:
            size_str = f"{file_size/1024:.1f} KB"
        else:
            size_str = f"{file_size/(1024*1024):.1f} MB"
        
        print(f"📦 Velikost výstupního souboru: {size_str}")
        
    except Exception as e:
        print(f"❌ CHYBA při ukládání souboru: {e}")
        return
    
    # Výpis příkladů
    if len(ict_tenders) > 0:
        print(f"\n📋 Příklady ICT zakázek:")
        for i, zakazka in enumerate(ict_tenders[:10]):
            vz = zakazka.get('verejna_zakazka', {})
            print(f"\n   {i+1}. {vz.get('identifikator_NIPEZ')}")
            print(f"      Název: {vz.get('nazev_verejne_zakazky', 'N/A')[:100]}")
            print(f"      Druh: {vz.get('druh_verejne_zakazky', 'N/A')}")
            
            hodnota = vz.get('predpokladana_hodnota_bez_DPH_v_CZK')
            if hodnota is not None:
                print(f"      Hodnota: {hodnota:,.0f} Kč")
            
            # CPV kód
            predmet = vz.get('predmet', {})
            cpv = predmet.get('hlavni_kod_CPV')
            if cpv:
                cpv_popis = ICT_CPV_CODES.get(cpv[:2], ICT_CPV_CODES.get(cpv[:8], ''))
                if cpv_popis:
                    print(f"      CPV: {cpv} - {cpv_popis}")
                else:
                    print(f"      CPV: {cpv}")
    
    print(f"\n🎉 HOTOVO! ICT zakázky jsou uloženy v souboru: {output_file}")


if __name__ == '__main__':
    input_file = '../data/VZ/VZ-2026-01-OPEN.json'
    output_file = '../data/VZ/VZ-2026-01-ICT.json'
    
    print("=" * 70)
    print("  FILTROVÁNÍ ICT VEŘEJNÝCH ZAKÁZEK")
    print("=" * 70)
    print()
    
    filter_ict_tenders(input_file, output_file)
    
    print()
    print("=" * 70)
