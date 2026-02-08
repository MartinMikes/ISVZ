"""
Filtrování ICT zakázek z DNS (Dynamických nákupních systémů).

DNS může obsahovat ICT zakázky, ale má jinou strukturu než VZ.
"""

import json
import re
from datetime import datetime
import sys
import io

# Fix pro Windows console - UTF-8 podpora emoji (jen pokud běží standalone)
if sys.platform == 'win32' and not hasattr(sys.stdout, 'buffer'):
    pass  # Už je wrapped
elif sys.platform == 'win32' and hasattr(sys.stdout, 'buffer') and 'TextIOWrapper' not in str(type(sys.stdout)):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# ICT klíčová slova (stejná jako pro VZ)
ICT_KEYWORDS = {
    'software', 'aplikace', 'app', 'program', 'vývoj', 'development',
    'kodování', 'coding', 'programování', 'programming',
    'informační systém', 'is', 'it', 'ict', 'digitalizace',
    'cloud', 'saas', 'paas', 'iaas',
    'web', 'webová aplikace', 'webové služby', 'website', 'portal', 'portál',
    'cms', 'e-shop', 'eshop', 'e-commerce',
    'databáze', 'database', 'sql', 'nosql', 'oracle', 'postgresql', 'mysql',
    'mongodb', 'datové úložiště', 'data warehouse',
    'správa sítí', 'síťová infrastruktura', 'server', 'hosting',
    'it podpora', 'helpdesk', 'servicedesk', 'správa systémů',
    'kyberbezpečnost', 'cybersecurity', 'kybernetická bezpečnost',
    'zabezpečení dat', 'firewall', 'antivir',
    'microsoft', 'office 365', 'azure', 'aws', 'google cloud',
    'vmware', 'kubernetes', 'docker', 'api',
    'elektronická spisová služba', 'ess', 'essl', 'spisová služba',
    'elektronické podání', 'datové schránky', 'czech point',
    'softwarová licence', 'licence', 'předplatné software',
    'mobilní aplikace', 'mobile app', 'desktop aplikace',
    'testování software', 'qa', 'quality assurance',
    'uživatelská dokumentace', 'technická dokumentace',
    'školení uživatelů', 'it školení',
}


# CPV kódy pro ICT
ICT_CPV_CODES = {
    '48', '72', '30200000', '30230000',
    '48000000', '48100000', '48200000', '48300000', '48400000',
    '48500000', '48600000', '48700000', '48800000', '48900000',
    '72000000', '72100000', '72200000', '72300000', '72400000',
    '72500000', '72600000',
}


def contains_ict_keywords(text):
    """Kontrola, zda text obsahuje ICT klíčová slova"""
    if not text:
        return False
    
    text_lower = text.lower()
    
    for keyword in ICT_KEYWORDS:
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        if re.search(pattern, text_lower):
            return True
    
    return False


def has_ict_cpv_code(cpv_code):
    """Kontrola, zda CPV kód patří do ICT"""
    if not cpv_code:
        return False
    
    cpv_str = str(cpv_code)
    
    for ict_code in ICT_CPV_CODES:
        if cpv_str.startswith(ict_code):
            return True
    
    return False


def is_ict_dns(dns_record):
    """
    Kontrola, zda je DNS záznam ICT.
    
    Struktura DNS:
    {
        "dynamicky_nakupni_system": {
            "nazev_dynamickeho_nakupniho_systemu": "...",
            "zadavaci_postup_pro_zavedeni_dynamickeho_nakupniho_systemu": {
                "predmet": {
                    "popis_predmetu": "...",
                    "hlavni_kod_CPV": "...",
                    "vedlejsi_kod_CPV": [...]
                }
            }
        }
    }
    """
    
    dns = dns_record.get('dynamicky_nakupni_system', {})
    
    # 1. Kontrola názvu
    nazev = dns.get('nazev_dynamickeho_nakupniho_systemu', '')
    if contains_ict_keywords(nazev):
        return True
    
    # 2. Kontrola zadávacího postupu
    zp = dns.get('zadavaci_postup_pro_zavedeni_dynamickeho_nakupniho_systemu', {})
    
    # 3. Kontrola popisu předmětu
    predmet = zp.get('predmet', {})
    popis = predmet.get('popis_predmetu', '')
    if contains_ict_keywords(popis):
        return True
    
    # 4. Kontrola hlavního CPV kódu
    hlavni_cpv = predmet.get('hlavni_kod_CPV', '')
    if has_ict_cpv_code(hlavni_cpv):
        return True
    
    # 5. Kontrola vedlejších CPV kódů
    vedlejsi_cpv = predmet.get('vedlejsi_kod_CPV', [])
    for cpv in vedlejsi_cpv:
        if has_ict_cpv_code(cpv):
            return True
    
    return False


def filter_dns_ict_tenders(input_file, output_file):
    """Načte DNS data a vyfiltruje ICT záznamy"""
    
    print(f"📂 Načítám soubor: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Soubor načten úspěšně!")
    except Exception as e:
        print(f"❌ CHYBA při načítání souboru: {e}")
        return
    
    # Metadata
    metadata = {
        'obdobi_od': data.get('obdobi_od'),
        'obdobi_do': data.get('obdobi_do'),
        'verze': data.get('verze'),
        'filtrovano_datum': datetime.now().isoformat(),
        'kategorie': 'DNS',
        'puvodni_pocet': 0,
        'ict_pocet': 0
    }
    
    zakazky = data.get('data', [])
    metadata['puvodni_pocet'] = len(zakazky)
    
    print(f"\n📊 Počet DNS záznamů: {len(zakazky)}")
    print(f"🔍 Filtrování ICT záznamů...")
    
    # Filtrování
    ict_dns = []
    
    for zaznam in zakazky:
        if is_ict_dns(zaznam):
            ict_dns.append(zaznam)
    
    metadata['ict_pocet'] = len(ict_dns)
    
    print(f"\n✅ Filtrování dokončeno!")
    print(f"📈 Nalezeno {len(ict_dns)} ICT DNS záznamů")
    print(f"📉 Odfiltrováno {len(zakazky) - len(ict_dns)} ne-ICT záznamů")
    print(f"📊 Úspěšnost: {len(ict_dns)/len(zakazky)*100:.2f}% záznamů je ICT")
    
    # Sestavení výstupního JSON
    output_data = {
        'metadata': metadata,
        'data': ict_dns
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
    if len(ict_dns) > 0:
        print(f"\n📋 Příklady ICT DNS záznamů:")
        for i, zaznam in enumerate(ict_dns[:10], 1):
            dns = zaznam.get('dynamicky_nakupni_system', {})
            nazev = dns.get('nazev_dynamickeho_nakupniho_systemu', 'N/A')
            
            print(f"\n   {i}. {nazev[:100]}")
            
            # CPV kód
            zp = dns.get('zadavaci_postup_pro_zavedeni_dynamickeho_nakupniho_systemu', {})
            predmet = zp.get('predmet', {})
            cpv = predmet.get('hlavni_kod_CPV')
            if cpv:
                print(f"      CPV: {cpv}")
            
            # Identifikátor
            id_nipez = dns.get('identifikator_NIPEZ')
            if id_nipez:
                print(f"      ID: {id_nipez}")
    
    print(f"\n🎉 HOTOVO! ICT DNS záznamy jsou uloženy v souboru: {output_file}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.json', '-ICT.json')
    else:
        # Výchozí pro leden 2026
        input_file = '../data/DNS/DNS-2026-01.json'
        output_file = '../data/DNS/DNS-2026-01-ICT.json'
    
    print("=" * 70)
    print("  FILTROVÁNÍ ICT Z DNS (DYNAMICKÝCH NÁKUPNÍCH SYSTÉMŮ)")
    print("=" * 70)
    print()
    
    filter_dns_ict_tenders(input_file, output_file)
    
    print()
    print("=" * 70)
