"""
Přidání doporučení (1-5) k ICT zakázkám na základě keyword analýzy.

Hodnotí zakázky podle technologické shody s profilem:
- Vývoj webů, software, aplikací a systémů (.NET, React, Vue)
- Konzultace/implementace Microsoft 365, SharePoint, Power Platform
- Microsoft technologie obecně

Známka 1 (nejlepší) až 5 (nejhorší).
"""

import json
from datetime import datetime
import re
import sys
import io

# Fix pro Windows console - UTF-8 podpora emoji
if sys.platform == 'win32' and not hasattr(sys.stdout, 'buffer'):
    pass
elif sys.platform == 'win32' and hasattr(sys.stdout, 'buffer') and 'TextIOWrapper' not in str(type(sys.stdout)):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# Klíčová slova podle technologické shody
KEYWORDS_TIER_1 = {
    # .NET ekosystém
    '.net', 'dotnet', 'c#', 'csharp', 'asp.net', 'blazor', 'maui',
    
    # Frontend frameworky
    'react', 'vue', 'angular', 'next.js', 'nuxt',
    
    # Microsoft 365 a Power Platform
    'sharepoint', 'power platform', 'power apps', 'power automate', 
    'power bi', 'microsoft 365', 'm365', 'office 365', 'o365',
    'teams', 'onedrive', 'dynamics 365',
    
    # Azure služby
    'azure', 'azure devops', 'azure ad', 'entra id', 'azure functions',
    
    # Microsoft technologie
    'microsoft', 'sql server', 'windows server', 'exchange',
}

KEYWORDS_TIER_2 = {
    # Web development
    'web', 'webová aplikace', 'webové služby', 'website', 'portál', 'portal',
    'e-shop', 'eshop', 'e-commerce', 'cms',
    
    # Software development
    'software', 'aplikace', 'app', 'vývoj software', 'vývoj aplikací',
    'programování', 'development', 'programming',
    
    # Systémy a integrace
    'informační systém', 'systém', 'integrace', 'api', 'rest api',
    'microservices', 'mikroslužby',
    
    # Databáze
    'databáze', 'database', 'sql', 'mssql', 'postgresql', 'mysql',
    
    # Cloud a DevOps
    'cloud', 'saas', 'paas', 'devops', 'ci/cd', 'git',
    
    # Konzultace
    'konzultace', 'poradenství', 'consulting', 'implementace',
}

KEYWORDS_TIER_3 = {
    # IT služby
    'it služby', 'ict', 'digitalizace', 'digital transformation',
    
    # Obecné IT
    'it řešení', 'it systém', 'it infrastruktura',
    'elektronizace', 'automatizace',
    
    # Dokumentové systémy
    'elektronická spisová služba', 'ess', 'essl',
    'datové schránky', 'czech point',
    
    # Mobilní
    'mobilní aplikace', 'mobile app', 'ios', 'android',
}

KEYWORDS_TIER_4 = {
    # Hardware a infrastruktura
    'hardware', 'server', 'síť', 'síťová infrastruktura',
    'networking', 'router', 'switch',
    
    # IT podpora
    'it podpora', 'helpdesk', 'servicedesk', 'správa systémů',
    'monitoring', 'backup', 'disaster recovery',
    
    # Bezpečnost
    'kyberbezpečnost', 'cybersecurity', 'firewall', 'antivir',
    'zabezpečení', 'security',
}

# Tier 5 = ostatní ICT bez specifických keywords


def count_keyword_matches(text, keywords):
    """Spočítá počet výskytů keywords v textu"""
    if not text:
        return 0
    
    text_lower = text.lower()
    matches = 0
    
    for keyword in keywords:
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        if re.search(pattern, text_lower):
            matches += 1
    
    return matches


def calculate_recommendation(zakazka):
    """
    Vypočítá doporučení (1-5) pro zakázku.
    
    Známka 1 (nejlepší) = vysoká shoda s .NET/React/Microsoft tech
    Známka 5 (nejhorší) = obecné ICT bez tech. detailů
    """
    vz = zakazka.get('verejna_zakazka', {})
    
    # Texty pro analýzu
    nazev = vz.get('nazev_verejne_zakazky', '')
    
    predmet = vz.get('predmet', {})
    popis = predmet.get('popis_predmetu', '')
    
    # CPV label (pokud je k dispozici)
    hlavni_cpv_label = ''  # Bude doplněno později z číselníku, prozatím prázdné
    
    # Kombinovaný text
    combined_text = f"{nazev} {popis} {hlavni_cpv_label}"
    
    # Také kontrolujeme části zakázky
    for cast in vz.get('casti_verejne_zakazky', []):
        nazev_casti = cast.get('nazev_casti_verejne_zakazky', '')
        predmet_casti = cast.get('predmet', {})
        popis_casti = predmet_casti.get('popis_predmetu', '')
        combined_text += f" {nazev_casti} {popis_casti}"
    
    # Počítání matches pro každý tier
    tier1_matches = count_keyword_matches(combined_text, KEYWORDS_TIER_1)
    tier2_matches = count_keyword_matches(combined_text, KEYWORDS_TIER_2)
    tier3_matches = count_keyword_matches(combined_text, KEYWORDS_TIER_3)
    tier4_matches = count_keyword_matches(combined_text, KEYWORDS_TIER_4)
    
    # Rozhodování o známce
    if tier1_matches >= 2:  # Více matches z tier 1 = top priorita
        return 1
    elif tier1_matches >= 1:  # Alespoň jeden match z tier 1
        return 1
    elif tier2_matches >= 3:  # Hodně matches z tier 2
        return 2
    elif tier2_matches >= 1:  # Alespoň jeden match z tier 2
        return 2
    elif tier3_matches >= 2:  # Nějaké matches z tier 3
        return 3
    elif tier3_matches >= 1 or tier2_matches > 0:
        return 3
    elif tier4_matches >= 1:  # Hardware/infrastruktura
        return 4
    else:  # Žádné specifické keywords
        return 5


def add_recommendations(input_file, output_file):
    """Načte ICT zakázky a přidá k nim doporučení"""
    
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
    zakazky = data.get('data', [])
    
    print(f"\n📊 Počet ICT zakázek: {len(zakazky)}")
    print(f"🎯 Přidávám doporučení...")
    
    # Statistika doporučení
    recommendations_stats = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    # Přidání doporučení ke každé zakázce
    for zakazka in zakazky:
        recommendation = calculate_recommendation(zakazka)
        zakazka['doporuceni'] = recommendation
        recommendations_stats[recommendation] += 1
    
    print(f"\n✅ Doporučení přidána!")
    print(f"\n📊 Statistika doporučení:")
    print(f"   ⭐⭐⭐⭐⭐ (1) Top match:     {recommendations_stats[1]:3d} zakázek ({recommendations_stats[1]/len(zakazky)*100:5.1f}%)")
    print(f"   ⭐⭐⭐⭐  (2) Strong:        {recommendations_stats[2]:3d} zakázek ({recommendations_stats[2]/len(zakazky)*100:5.1f}%)")
    print(f"   ⭐⭐⭐   (3) Medium:        {recommendations_stats[3]:3d} zakázek ({recommendations_stats[3]/len(zakazky)*100:5.1f}%)")
    print(f"   ⭐⭐    (4) Weak:          {recommendations_stats[4]:3d} zakázek ({recommendations_stats[4]/len(zakazky)*100:5.1f}%)")
    print(f"   ⭐     (5) Low:           {recommendations_stats[5]:3d} zakázek ({recommendations_stats[5]/len(zakazky)*100:5.1f}%)")
    
    # Sestavení výstupního JSON
    output_metadata = metadata.copy()
    output_metadata['doporuceni_pridana'] = datetime.now().isoformat()
    output_metadata['doporuceni_statistika'] = recommendations_stats
    
    output_data = {
        'metadata': output_metadata,
        'data': zakazky
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
    
    # Výpis příkladů TOP zakázek
    if recommendations_stats[1] > 0:
        print(f"\n🌟 Příklady TOP zakázek (doporučení = 1):")
        top_tenders = [z for z in zakazky if z.get('doporuceni') == 1]
        for i, zakazka in enumerate(top_tenders[:5]):
            vz = zakazka.get('verejna_zakazka', {})
            print(f"\n   {i+1}. {vz.get('identifikator_NIPEZ')}")
            print(f"      Název: {vz.get('nazev_verejne_zakazky', 'N/A')[:100]}")
            
            hodnota = vz.get('predpokladana_hodnota_bez_DPH_v_CZK')
            if hodnota is not None:
                print(f"      Hodnota: {hodnota:,.0f} Kč")
    
    print(f"\n🎉 HOTOVO! Zakázky s doporučeními jsou uloženy v souboru: {output_file}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        input_file = '../data/VZ/VZ-2026-01-ICT.json'
        output_file = '../data/VZ/VZ-2026-01-ICT.json'  # Přepíše původní
    
    print("=" * 70)
    print("  PŘIDÁNÍ DOPORUČENÍ K ICT ZAKÁZKÁM")
    print("=" * 70)
    print()
    
    add_recommendations(input_file, output_file)
    
    print()
    print("=" * 70)
