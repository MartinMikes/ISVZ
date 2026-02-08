#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generátor reportů pro ISVZ veřejné zakázky.

Vytváří Markdown a CSV reporty z vyfiltrovaných JSON souborů (*-ICT.json, *-OPEN.json).
Reporty obsahují číselníkové informace a jsou organizovány do složek dle roku a měsíce.
"""

import sys
import io
import json
import os
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Fix pro Windows console encoding
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer') and 'TextIOWrapper' not in str(type(sys.stdout)):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


# Načtení NUTS → Kraj číselníku
def load_nuts_codebook() -> Dict[str, str]:
    """Načte číselník NUTS → Kraj."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    nuts_file = os.path.join(script_dir, '..', 'data', 'nuts_kraje.json')
    
    try:
        with open(nuts_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('nuts_kraje', {})
    except:
        return {}

# Globální číselník
NUTS_KRAJE = load_nuts_codebook()


def format_currency(amount: Optional[float]) -> str:
    """Formátuje částku v Kč."""
    if amount is None:
        return "neuvedeno"
    return f"{amount:,.0f} Kč".replace(",", " ")


def format_date(date_str: Optional[str]) -> str:
    """Formátuje datum do čitelné podoby."""
    if not date_str:
        return "neuvedeno"
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%d.%m.%Y %H:%M")
    except:
        return date_str


def get_cpv_description(cpv_code: str) -> str:
    """Vrátí popis CPV kódu."""
    cpv_map = {
        '30': 'Kancelářské a výpočetní stroje',
        '30200000': 'Počítačová zařízení a příslušenství',
        '30230000': 'Počítačová zařízení',
        '48': 'Softwarové balíky a informační systémy',
        '48000000': 'Softwarové balíky a informační systémy',
        '48800000': 'Informační systémy a servery',
        '72': 'IT služby: konzultace, vývoj software, internet a podpora',
        '72000000': 'IT služby',
        '72200000': 'Programátorské služby',
        '72400000': 'Internetové služby',
        '72500000': 'Počítačové služby',
    }
    
    # Zkusit přesnou shodu, pak prefix
    if cpv_code in cpv_map:
        return cpv_map[cpv_code]
    
    for key, value in cpv_map.items():
        if cpv_code.startswith(key):
            return value
    
    return "Ostatní"


def get_kraj_from_nuts(nuts_code: Optional[str]) -> str:
    """Vrátí název kraje z NUTS kódu."""
    if not nuts_code:
        return "neuvedeno"
    
    # NUTS kód může být i delší (např. CZ0100), vezmeme prvních 5 znaků
    nuts_prefix = nuts_code[:5] if len(nuts_code) >= 5 else nuts_code
    
    return NUTS_KRAJE.get(nuts_prefix, "neuvedeno")


def extract_tender_info(tender: Dict[str, Any]) -> Dict[str, Any]:
    """Extrahuje klíčové informace o zakázce."""
    vz = tender.get('verejna_zakazka', {})
    
    # Základní info
    info = {
        'id_nipez': vz.get('identifikator_NIPEZ', 'N/A'),
        'nazev': vz.get('nazev_verejne_zakazky', 'Bez názvu'),
        'druh': vz.get('druh_verejne_zakazky', 'neuvedeno'),
        'rezim': vz.get('rezim_verejne_zakazky', 'neuvedeno'),
        'hodnota': vz.get('predpokladana_hodnota_bez_DPH_v_CZK'),
    }
    
    # Předmět
    predmet = vz.get('predmet', {})
    info['popis'] = predmet.get('popis_predmetu', '').strip()
    info['cpv_hlavni'] = predmet.get('hlavni_kod_CPV', '')
    info['cpv_vedlejsi'] = predmet.get('vedlejsi_kod_CPV', [])
    info['cpv_popis'] = get_cpv_description(info['cpv_hlavni'])
    
    # Místo plnění
    mista = predmet.get('mista_plneni', [])
    if mista:
        info['nuts'] = mista[0].get('nuts', '')
        info['misto'] = mista[0].get('dalsi_informace_o_miste_plneni', '')
        info['kraj'] = get_kraj_from_nuts(info['nuts'])
    else:
        info['nuts'] = ''
        info['misto'] = ''
        info['kraj'] = 'neuvedeno'
    
    # Části zakázky - lhůty a stav
    casti = vz.get('casti_verejne_zakazky', [])
    if casti:
        cast = casti[0]
        zp = cast.get('zadavaci_postup_pro_cast', {})
        
        info['stav'] = zp.get('stav', 'neuvedeno')
        info['druh_postupu'] = zp.get('druh_zadavaciho_postupu', 'neuvedeno')
        info['elektronicky_nastroj'] = zp.get('elektronicky_nastroj', {}).get('kod', 'neuvedeno')
        
        # Lhůty
        lhuty = zp.get('lhuty', [])
        info['lhuta_podani'] = None
        info['lhuta_ucast'] = None
        
        for lhuta in lhuty:
            druh = lhuta.get('druh_lhuty', '')
            datum = lhuta.get('datum_a_cas_konce_lhuty')
            
            if 'podání nabíd' in druh:
                info['lhuta_podani'] = datum
            elif 'podání žádosti o účast' in druh:
                info['lhuta_ucast'] = datum
    else:
        info['stav'] = 'neuvedeno'
        info['druh_postupu'] = 'neuvedeno'
        info['elektronicky_nastroj'] = 'neuvedeno'
        info['lhuta_podani'] = None
        info['lhuta_ucast'] = None
    
    # Zadavatel - použít z zadavaci_postupy místo zadavatele
    zadavaci_postupy = vz.get('zadavaci_postupy', [])
    if zadavaci_postupy:
        zad_postup = zadavaci_postupy[0]
        zad_zadav = zad_postup.get('zadavatel_zadavaciho_postupu', {})
        zadavatele = zad_zadav.get('zadavatele', [])
        
        if zadavatele:
            subjekt = zadavatele[0].get('subjekt', {})
            info['zadavatel_nazev'] = subjekt.get('nazev_subjektu', 'neuvedeno')
            info['zadavatel_ico'] = subjekt.get('ico', '')
            info['url_profil_zadavatele'] = zadavatele[0].get('adresa_profilu', '')
        else:
            info['zadavatel_nazev'] = 'neuvedeno'
            info['zadavatel_ico'] = ''
            info['url_profil_zadavatele'] = ''
    else:
        info['zadavatel_nazev'] = 'neuvedeno'
        info['zadavatel_ico'] = ''
        info['url_profil_zadavatele'] = ''
    
    # URL odkazy - extrakce z částí zakázky
    if casti:
        cast = casti[0]
        zp = cast.get('zadavaci_postup_pro_cast', {})
        
        # Zadávací dokumentace
        zad_dok = zp.get('informace_o_zadavacich_dokumentacich', [])
        info['url_dokumentace'] = zad_dok[0].get('zadavaci_dokumentace_je_dostupna_na', '') if zad_dok else ''
        
        # Podání nabídek
        podani = zp.get('specifikace_podani', {})
        info['url_podani'] = podani.get('internetova_adresa_pro_podani', '')
        
        # Otevírání nabídek
        otevirani = zp.get('informace_o_otevirani_podani', [])
        info['url_otevirani'] = otevirani[0].get('misto_otevirani_podani', '') if otevirani else ''
    else:
        info['url_dokumentace'] = ''
        info['url_podani'] = ''
        info['url_otevirani'] = ''
    
    # Doporučení (pokud existuje)
    info['doporuceni'] = tender.get('doporuceni', '')
    
    # ===== NOVÁ POLE - FÁZE 1 & 2 =====
    
    # Fáze 1: Priorita A
    
    # 1. Financování EU
    if casti:
        info['financovani_eu'] = casti[0].get('verejna_zakazka_je_alespon_castecne_financovana_z_prostredku_Evropske_unie', False)
    else:
        info['financovani_eu'] = False
    
    # 2 & 3. Kategorie a sektor zadavatele
    if zadavaci_postupy:
        zad_postup = zadavaci_postupy[0]
        zad_zadav = zad_postup.get('zadavatel_zadavaciho_postupu', {})
        zadavatele = zad_zadav.get('zadavatele', [])
        
        if zadavatele:
            info['kategorie_zadavatele'] = zadavatele[0].get('kategorie_zadavatele', '')
            info['sektor_zadavatele'] = zadavatele[0].get('hlavni_predmet_cinnosti_verejneho_zadavatele', '')
        else:
            info['kategorie_zadavatele'] = ''
            info['sektor_zadavatele'] = ''
    else:
        info['kategorie_zadavatele'] = ''
        info['sektor_zadavatele'] = ''
    
    # 4. Datum zahájení
    if casti:
        zp = casti[0].get('zadavaci_postup_pro_cast', {})
        info['datum_zahajeni'] = zp.get('datum_zahajeni_zadavaciho_postupu', '')
    else:
        info['datum_zahajeni'] = ''
    
    # 5. Váha ceny v kritériích hodnocení
    if casti and len(casti) > 0:
        zp = casti[0].get('zadavaci_postup_pro_cast', {})
        if zp:
            pravidla = zp.get('pravidla_pro_hodnoceni', {})
            if pravidla:
                kriteria = pravidla.get('kriteria_pro_hodnoceni_nabidek_nebo_navrhu', [])
                
                vaha_ceny = 0
                for krit in kriteria:
                    druh = krit.get('druh_kriteria', '')
                    if 'Cena' in druh or 'cena' in druh.lower():
                        vaha = krit.get('vaha_kriteria', 0)
                        if isinstance(vaha, (int, float)):
                            vaha_ceny = vaha
                            break
                
                info['vaha_ceny'] = vaha_ceny if vaha_ceny > 0 else None
            else:
                info['vaha_ceny'] = None
        else:
            info['vaha_ceny'] = None
    else:
        info['vaha_ceny'] = None
    
    # Fáze 2: Priorita B
    
    # 6. Doba trvání smlouvy
    if casti and len(casti) > 0:
        doba = casti[0].get('doba_trvani', {})
        if doba:
            trvani = doba.get('doba_trvani')
            jednotka = doba.get('doba_trvani_jednotka', '')
            
            # Normalizace na měsíce
            if trvani and jednotka:
                if 'měsíc' in jednotka.lower():
                    info['doba_trvani_mesice'] = trvani
                elif 'rok' in jednotka.lower() or 'let' in jednotka.lower():
                    info['doba_trvani_mesice'] = trvani * 12
                elif 'd' in jednotka.lower():  # dny
                    info['doba_trvani_mesice'] = round(trvani / 30, 1)
                else:
                    info['doba_trvani_mesice'] = None
            else:
                info['doba_trvani_mesice'] = None
        else:
            info['doba_trvani_mesice'] = None
    else:
        info['doba_trvani_mesice'] = None
    
    # 7. Elektronická platba
    if casti and len(casti) > 0:
        zp = casti[0].get('zadavaci_postup_pro_cast', {})
        if zp:
            podminky = zp.get('obchodni_nebo_jine_podminky', {})
            if podminky:
                info['elektronicka_platba'] = podminky.get('bude_pouzita_elektronicka_platba', False)
            else:
                info['elektronicka_platba'] = False
        else:
            info['elektronicka_platba'] = False
    else:
        info['elektronicka_platba'] = False
    
    # 8. Vhodné pro SME
    if casti and len(casti) > 0:
        zp = casti[0].get('zadavaci_postup_pro_cast', {})
        if zp:
            info['vhodne_pro_sme'] = zp.get('verejna_zakazka_je_vhodna_pro_male_a_stredni_podniky', False)
        else:
            info['vhodne_pro_sme'] = False
    else:
        info['vhodne_pro_sme'] = False
    
    # 9. Typ dle hodnoty
    info['typ_dle_hodnoty'] = vz.get('typ_verejne_zakazky_dle_vyse_predpokladane_hodnoty', '')
    
    return info


def generate_markdown_report(data: List[Dict], output_file: str, report_type: str, year: int, month: int):
    """Generuje Markdown report s řazením podle doporučení."""
    
    month_names = {
        1: 'leden', 2: 'únor', 3: 'březen', 4: 'duben', 5: 'květen', 6: 'červen',
        7: 'červenec', 8: 'srpen', 9: 'září', 10: 'říjen', 11: 'listopad', 12: 'prosinec'
    }
    
    report_titles = {
        'ICT': 'ICT veřejné zakázky',
        'OPEN': 'Otevřené veřejné zakázky'
    }
    
    title = report_titles.get(report_type, 'Veřejné zakázky')
    month_name = month_names.get(month, str(month))
    
    # Seřadit data podle doporučení (nejlepší první)
    sorted_data = sorted(data, key=lambda x: x.get('doporuceni', 999))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Hlavička
        f.write(f"# {title} - {month_name} {year}\n\n")
        f.write(f"**Vygenerováno**: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n")
        f.write(f"**Počet zakázek**: {len(data)}\n\n")
        
        # Statistiky
        f.write("## 📊 Statistiky\n\n")
        
        # Podle druhu
        druhy = {}
        for item in sorted_data:
            info = extract_tender_info(item)
            druh = info['druh']
            druhy[druh] = druhy.get(druh, 0) + 1
        
        f.write("### Podle druhu zakázky\n\n")
        f.write("| Druh | Počet | Podíl |\n")
        f.write("|------|-------|-------|\n")
        for druh, count in sorted(druhy.items(), key=lambda x: x[1], reverse=True):
            podil = (count / len(data)) * 100
            f.write(f"| {druh} | {count} | {podil:.1f}% |\n")
        f.write("\n")
        
        # Celková hodnota
        total_value = 0
        value_count = 0
        for item in sorted_data:
            info = extract_tender_info(item)
            if info['hodnota']:
                total_value += info['hodnota']
                value_count += 1
        
        if value_count > 0:
            f.write("### Podle hodnoty\n\n")
            f.write(f"- **Celková hodnota**: {format_currency(total_value)}\n")
            f.write(f"- **Průměrná hodnota**: {format_currency(total_value / value_count)}\n")
            f.write(f"- **Zakázek s hodnotou**: {value_count} / {len(data)}\n\n")
        
        # Seznam zakázek
        f.write("---\n\n")
        f.write("## 📋 Seznam zakázek\n\n")
        
        for idx, item in enumerate(sorted_data, 1):
            info = extract_tender_info(item)
            
            f.write(f"### {idx}. {info['nazev']}\n\n")
            f.write(f"**ID NIPEZ**: `{info['id_nipez']}`\n\n")
            
            # Doporučení (pokud existuje)
            if info['doporuceni']:
                stars = '⭐' * (6 - info['doporuceni'])  # 5 hvězd pro 1, 1 hvězda pro 5
                f.write(f"**Doporučení**: {stars} ({info['doporuceni']}/5)\n\n")
            
            # Základní informace
            f.write("#### 📌 Základní informace\n\n")
            f.write(f"- **Druh**: {info['druh']}\n")
            f.write(f"- **Režim**: {info['rezim']}\n")
            f.write(f"- **Hodnota**: {format_currency(info['hodnota'])}\n")
            f.write(f"- **Stav**: {info['stav']}\n")
            f.write(f"- **Druh postupu**: {info['druh_postupu']}\n")
            f.write(f"- **Elektronický nástroj**: {info['elektronicky_nastroj']}\n")
            
            # Nová pole - Fáze 1 & 2
            if info['typ_dle_hodnoty']:
                f.write(f"- **Typ dle hodnoty**: {info['typ_dle_hodnoty']}\n")
            if info['financovani_eu']:
                f.write(f"- **Financování EU**: Ano\n")
            if info['vhodne_pro_sme']:
                f.write(f"- **Vhodné pro SME**: Ano\n")
            if info['datum_zahajeni']:
                f.write(f"- **Zahájeno**: {format_date(info['datum_zahajeni'])}\n")
            if info['doba_trvani_mesice']:
                roky = info['doba_trvani_mesice'] / 12
                if roky >= 1:
                    f.write(f"- **Doba trvání**: {info['doba_trvani_mesice']} měsíců ({roky:.1f} let)\n")
                else:
                    f.write(f"- **Doba trvání**: {info['doba_trvani_mesice']} měsíců\n")
            
            f.write("\n")
            
            # Předmět
            f.write("#### 📝 Předmět zakázky\n\n")
            if info['popis']:
                # Zkrátit popis pokud je dlouhý
                popis = info['popis']
                if len(popis) > 500:
                    popis = popis[:497] + "..."
                f.write(f"{popis}\n\n")
            
            # CPV kódy
            f.write("#### 🏷️ CPV klasifikace\n\n")
            f.write(f"- **Hlavní CPV**: `{info['cpv_hlavni']}` - {info['cpv_popis']}\n")
            if info['cpv_vedlejsi']:
                f.write(f"- **Vedlejší CPV**: {', '.join(f'`{cpv}`' for cpv in info['cpv_vedlejsi'])}\n")
            
            # Kritéria hodnocení
            if info['vaha_ceny'] is not None:
                vaha_kvality = 100 - info['vaha_ceny']
                f.write(f"- **Kritéria hodnocení**: Cena {info['vaha_ceny']}% / Kvalita {vaha_kvality}%\n")
            
            f.write("\n")
            
            # Lhůty
            if info['lhuta_podani'] or info['lhuta_ucast']:
                f.write("#### ⏰ Lhůty\n\n")
                if info['lhuta_podani']:
                    f.write(f"- **Lhůta pro podání nabídky**: {format_date(info['lhuta_podani'])}\n")
                if info['lhuta_ucast']:
                    f.write(f"- **Lhůta pro podání žádosti o účast**: {format_date(info['lhuta_ucast'])}\n")
                f.write("\n")
            
            # Zadavatel
            f.write("#### 🏢 Zadavatel\n\n")
            f.write(f"- **Název**: {info['zadavatel_nazev']}\n")
            if info['zadavatel_ico']:
                f.write(f"- **IČO**: {info['zadavatel_ico']}\n")
            if info['kategorie_zadavatele']:
                f.write(f"- **Kategorie**: {info['kategorie_zadavatele']}\n")
            if info['sektor_zadavatele']:
                f.write(f"- **Sektor**: {info['sektor_zadavatele']}\n")
            if info['url_profil_zadavatele']:
                f.write(f"- **Profil zadavatele**: [{info['url_profil_zadavatele']}]({info['url_profil_zadavatele']})\n")
            f.write("\n")
            
            # Místo plnění
            if info['misto'] or info['nuts'] or info['kraj']:
                f.write("#### 📍 Místo plnění\n\n")
                if info['misto']:
                    f.write(f"- **Místo**: {info['misto']}\n")
                if info['nuts']:
                    f.write(f"- **NUTS kód**: {info['nuts']}\n")
                if info['kraj'] != 'neuvedeno':
                    f.write(f"- **Kraj**: {info['kraj']}\n")
                f.write("\n")
            
            # Odkazy
            if info['url_dokumentace'] or info['url_podani'] or info['url_otevirani']:
                f.write("#### 🔗 Odkazy\n\n")
                if info['url_dokumentace']:
                    f.write(f"- **Zadávací dokumentace**: [{info['url_dokumentace']}]({info['url_dokumentace']})\n")
                if info['url_podani']:
                    f.write(f"- **Podání nabídek**: [{info['url_podani']}]({info['url_podani']})\n")
                if info['url_otevirani']:
                    f.write(f"- **Otevírání nabídek**: [{info['url_otevirani']}]({info['url_otevirani']})\n")
                f.write("\n")
            
            f.write("---\n\n")


def generate_csv_report(data: List[Dict], output_file: str):
    """Generuje CSV report s řazením podle doporučení."""
    
    # Seřadit data podle doporučení (nejlepší první)
    sorted_data = sorted(data, key=lambda x: x.get('doporuceni', 999))
    
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        
        # Hlavička
        writer.writerow([
            'ID NIPEZ',
            'Název',
            'Druh',
            'Režim',
            'Hodnota (Kč)',
            'Stav',
            'Druh postupu',
            'El. nástroj',
            'CPV hlavní',
            'CPV popis',
            'Lhůta podání nabídky',
            'Lhůta žádost o účast',
            'Zadavatel',
            'IČO zadavatele',
            'Místo plnění',
            'NUTS',
            'Kraj',
            'Doporučení',
            # Nové sloupce - Fáze 1
            'Financování EU',
            'Kategorie zadavatele',
            'Sektor zadavatele',
            'Datum zahájení',
            'Váha ceny (%)',
            # Nové sloupce - Fáze 2
            'Doba trvání (měsíce)',
            'E-platba',
            'Vhodné pro SME',
            'Typ dle hodnoty',
            # URL odkazy
            'URL Profil zadavatele',
            'URL Dokumentace',
            'URL Podání nabídek',
            'URL Otevírání',
            'Popis (zkrácený)'
        ])
        
        # Data
        for item in sorted_data:
            info = extract_tender_info(item)
            
            # Zkrátit popis
            popis = info['popis']
            if len(popis) > 200:
                popis = popis[:197] + "..."
            popis = popis.replace('\n', ' ').replace('\r', ' ')
            
            writer.writerow([
                info['id_nipez'],
                info['nazev'],
                info['druh'],
                info['rezim'],
                info['hodnota'] if info['hodnota'] else '',
                info['stav'],
                info['druh_postupu'],
                info['elektronicky_nastroj'],
                info['cpv_hlavni'],
                info['cpv_popis'],
                format_date(info['lhuta_podani']),
                format_date(info['lhuta_ucast']),
                info['zadavatel_nazev'],
                info['zadavatel_ico'],
                info['misto'],
                info['nuts'],
                info['kraj'],
                info['doporuceni'] if info['doporuceni'] else '',
                # Nové sloupce - Fáze 1
                'Ano' if info['financovani_eu'] else 'Ne',
                info['kategorie_zadavatele'] if info['kategorie_zadavatele'] else '',
                info['sektor_zadavatele'] if info['sektor_zadavatele'] else '',
                format_date(info['datum_zahajeni']) if info['datum_zahajeni'] else '',
                info['vaha_ceny'] if info['vaha_ceny'] is not None else '',
                # Nové sloupce - Fáze 2
                info['doba_trvani_mesice'] if info['doba_trvani_mesice'] else '',
                'Ano' if info['elektronicka_platba'] else 'Ne',
                'Ano' if info['vhodne_pro_sme'] else 'Ne',
                info['typ_dle_hodnoty'] if info['typ_dle_hodnoty'] else '',
                # URL odkazy
                info['url_profil_zadavatele'],
                info['url_dokumentace'],
                info['url_podani'],
                info['url_otevirani'],
                popis
            ])


def generate_table_summary(data: List[Dict], output_file: str, report_type: str, year: int, month: int):
    """
    Generuje tabulkový MD souhrn do root složky output/reports/.
    
    Přepíše předchozí soubor - obsahuje pouze aktuální měsíc.
    Slouží jako rychlý přehled nejdůležitějších informací v tabulce.
    Řadí zakázky podle doporučení.
    """
    
    month_names = {
        1: 'leden', 2: 'únor', 3: 'březen', 4: 'duben', 5: 'květen', 6: 'červen',
        7: 'červenec', 8: 'srpen', 9: 'září', 10: 'říjen', 11: 'listopad', 12: 'prosinec'
    }
    
    report_titles = {
        'VZ-ICT': 'ICT veřejné zakázky',
        'VZ-OPEN': 'Otevřené veřejné zakázky',
        'DNS-ICT': 'ICT dynamické nákupní systémy'
    }
    
    title = report_titles.get(report_type, 'Veřejné zakázky')
    month_name = month_names.get(month, str(month))
    
    # Seřadit data podle doporučení (nejlepší první)
    sorted_data = sorted(data, key=lambda x: x.get('doporuceni', 999))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Hlavička
        f.write(f"# {title} - {month_name} {year}\n\n")
        f.write(f"**Vygenerováno**: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n")
        f.write(f"**Počet zakázek**: {len(data)}\n\n")
        
        # Statistiky - kompaktní
        druhy = {}
        total_value = 0
        value_count = 0
        
        for item in sorted_data:
            info = extract_tender_info(item)
            druh = info['druh']
            druhy[druh] = druhy.get(druh, 0) + 1
            if info['hodnota']:
                total_value += info['hodnota']
                value_count += 1
        
        f.write("## 📊 Rychlý přehled\n\n")
        f.write(f"- **Celková hodnota**: {format_currency(total_value) if value_count > 0 else 'neuvedeno'}\n")
        f.write(f"- **Průměrná hodnota**: {format_currency(total_value / value_count) if value_count > 0 else 'neuvedeno'}\n")
        f.write(f"- **Rozdělení**: {', '.join([f'{druh}: {count}' for druh, count in sorted(druhy.items(), key=lambda x: x[1], reverse=True)])}\n\n")
        
        # Tabulka - hlavní část
        f.write("## 📋 Tabulkový přehled\n\n")
        
        # Hlavička tabulky
        f.write("| # | Doporučení | ID NIPEZ | Název | Druh | Hodnota | Stav | Lhůta | Zadavatel | CPV | Kraj |\n")
        f.write("|---|------------|----------|-------|------|---------|------|-------|-----------|-----|------|\n")
        
        # Data
        for idx, item in enumerate(sorted_data, 1):
            info = extract_tender_info(item)
            
            # Zkrátit název pokud je dlouhý
            nazev = info['nazev']
            if len(nazev) > 60:
                nazev = nazev[:57] + "..."
            
            # Zkrátit zadavatele
            zadavatel = info['zadavatel_nazev']
            if len(zadavatel) > 40:
                zadavatel = zadavatel[:37] + "..."
            
            # Formátovat hodnotu kompaktně
            hodnota_str = format_currency(info['hodnota'])
            if hodnota_str != "neuvedeno":
                # Zkrátit formát pro tabulku
                hodnota_str = hodnota_str.replace(" ", "").replace("Kč", " Kč")
                if len(hodnota_str) > 15:
                    # Převést na miliony pro velké částky
                    val = info['hodnota']
                    if val >= 1000000:
                        hodnota_str = f"{val/1000000:.1f}M Kč"
            
            # Zkrátit stav
            stav = info['stav'] if info['stav'] else 'neuvedeno'
            if stav == 'Aktivní/Neukončen':
                stav = 'Aktivní'
            elif stav == 'Dokončen/Zadán':
                stav = 'Zadán'
            elif stav != 'neuvedeno' and len(stav) > 15:
                stav = stav[:12] + "..."
            
            # Lhůta - jen datum
            lhuta = ""
            if info['lhuta_podani']:
                lhuta = format_date(info['lhuta_podani']).split()[0]  # Jen datum, bez času
            elif info['lhuta_ucast']:
                lhuta = format_date(info['lhuta_ucast']).split()[0]
            
            # CPV - jen kód
            cpv = info['cpv_hlavni'] if info['cpv_hlavni'] else '-'
            
            # Kraj - zkrácený název
            kraj = info['kraj']
            if kraj == 'neuvedeno':
                kraj = '-'
            elif len(kraj) > 20:
                # Zkrátit dlouhé názvy krajů (např. "Královéhradecký" -> "Královéhr...")
                kraj = kraj[:17] + "..."
            
            # Doporučení - hvězdičky
            doporuceni_str = ''
            if info['doporuceni']:
                stars = '⭐' * (6 - info['doporuceni'])
                doporuceni_str = f"{stars} ({info['doporuceni']})"
            else:
                doporuceni_str = '-'
            
            f.write(f"| {idx} | {doporuceni_str} | `{info['id_nipez']}` | {nazev} | {info['druh']} | {hodnota_str} | {stav} | {lhuta} | {zadavatel} | `{cpv}` | {kraj} |\n")
        
        # Poznámky
        f.write("\n---\n\n")
        f.write("### 📝 Poznámky\n\n")
        f.write("- **Doporučení**: ⭐⭐⭐⭐⭐ (1) = nejlepší shoda, ⭐ (5) = nejhorší shoda\n")
        f.write("- **M Kč**: Miliony Kč (např. 45.5M Kč = 45 500 000 Kč)\n")
        f.write("- **CPV**: Kód společného slovníku pro veřejné zakázky\n")
        f.write("- **Lhůta**: Datum konce lhůty pro podání nabídky/žádosti\n")
        f.write("- **Stav**: Aktuální stav zadávacího postupu\n")
        f.write("- **Kraj**: Určen z NUTS kódu místa plnění\n\n")
        f.write(f"📄 **Detail**: Viz `{year}/{month:02d}/{report_type}_{year}-{month:02d}.md`\n")
        f.write(f"💾 **CSV export**: Viz `csv/{year}/{month:02d}/{report_type}_{year}-{month:02d}.csv`\n")


def process_file(input_file: str, output_dir_md: str, output_dir_csv: str, year: int, month: int, report_type: str):
    """Zpracuje jeden JSON soubor a vytvoří MD a CSV reporty."""
    
    # Načti JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    data = content.get('data', [])
    
    if not data:
        print(f"   ⚠️  Soubor je prázdný, přeskakuji")
        return
    
    # Vytvoř strukturu složek: YYYY/MM/
    year_month = f"{year}/{month:02d}"
    md_path = os.path.join(output_dir_md, year_month)
    csv_path = os.path.join(output_dir_csv, year_month)
    
    Path(md_path).mkdir(parents=True, exist_ok=True)
    Path(csv_path).mkdir(parents=True, exist_ok=True)
    
    # Názvy výstupních souborů
    base_name = f"{report_type}_{year}-{month:02d}"
    md_file = os.path.join(md_path, f"{base_name}.md")
    csv_file = os.path.join(csv_path, f"{base_name}.csv")
    
    # Generuj reporty
    print(f"   📝 MD:  {md_file}")
    generate_markdown_report(data, md_file, report_type, year, month)
    
    print(f"   💾 CSV: {csv_file}")
    generate_csv_report(data, csv_file)
    
    # Zkopíruj CSV i do root složky (bez data v názvu) pro snadné použití v Excel
    latest_csv_file = os.path.join(output_dir_csv, f"{report_type}.csv")
    print(f"   📋 CSV (latest): {latest_csv_file}")
    generate_csv_report(data, latest_csv_file)
    
    # Generuj tabulkový souhrn v root složce output/reports/
    table_file = os.path.join(output_dir_md, f"{report_type}_{year}-{month:02d}.md")
    print(f"   📊 Tabulka: {table_file}")
    generate_table_summary(data, table_file, report_type, year, month)
    
    print(f"   ✅ Vygenerováno {len(data)} záznamů")



def generate_reports_for_month(year: int, month: int, data_dir: str = "data", output_base: str = "output"):
    """Generuje reporty pro daný měsíc."""
    
    print(f"\n{'='*70}")
    print(f"  GENEROVÁNÍ REPORTŮ PRO {month}/{year}")
    print(f"{'='*70}\n")
    
    output_dir_md = os.path.join(output_base, "reports")
    output_dir_csv = os.path.join(output_base, "csv")
    
    # Seznam souborů ke zpracování
    month_str = f"{month:02d}"
    files_to_process = [
        ('VZ', f"VZ-{year}-{month_str}-OPEN.json", 'VZ-OPEN'),
        ('VZ', f"VZ-{year}-{month_str}-ICT.json", 'VZ-ICT'),
        ('DNS', f"DNS-{year}-{month_str}-ICT.json", 'DNS-ICT'),
    ]
    
    processed = 0
    
    for category, filename, report_type in files_to_process:
        input_file = os.path.join(data_dir, category, filename)
        
        if not os.path.exists(input_file):
            print(f"⏭️  Přeskakuji {filename} (neexistuje)")
            continue
        
        print(f"🔍 Zpracovávám: {filename}")
        try:
            process_file(input_file, output_dir_md, output_dir_csv, year, month, report_type)
            processed += 1
        except Exception as e:
            print(f"   ❌ Chyba: {e}")
    
    if processed > 0:
        print(f"\n✅ Vygenerováno reportů: {processed * 2} (MD + CSV)")
        print(f"\n📁 Výstupní složky:")
        print(f"   - {output_dir_md}/{year}/{month:02d}/")
        print(f"   - {output_dir_csv}/{year}/{month:02d}/")
    else:
        print(f"\n⚠️  Žádné soubory ke zpracování")
    
    return processed > 0


def main():
    """Hlavní funkce."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generuje Markdown a CSV reporty z vyfiltrovaných JSON souborů"
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
        '--data-dir',
        default='../data',
        help='Adresář s daty (výchozí: ../data)'
    )
    
    parser.add_argument(
        '--output-dir',
        default='../output',
        help='Výstupní adresář (výchozí: ../output)'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("  GENERÁTOR REPORTŮ ISVZ")
    print("=" * 70)
    
    generate_reports_for_month(args.year, args.month, args.data_dir, args.output_dir)


if __name__ == '__main__':
    main()
