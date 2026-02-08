"""
Zobrazení a analýza ICT zakázek.

Načte vyfiltrované ICT zakázky a zobrazí je v přehledné formě
včetně základní analýzy.
"""

import json
from datetime import datetime
from collections import Counter
import sys

# Nastavení pro Windows konzoli
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def format_currency(amount):
    """Formátuje částku v Kč"""
    if amount is None:
        return "Neuvedena"
    return f"{amount:,.0f} Kč".replace(',', ' ')


def format_date(date_str):
    """Formátuje datum do lidsky čitelné formy"""
    if not date_str:
        return "Neuvedeno"
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%d.%m.%Y %H:%M')
    except:
        return date_str


def analyze_ict_tenders(file_path):
    """Analýza a zobrazení ICT zakázek"""
    
    print(f"📂 Načítám soubor: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Chyba: {e}")
        return
    
    metadata = data.get('metadata', {})
    zakazky = data.get('data', [])
    
    print(f"\n{'='*80}")
    print(f"  PŘEHLED ICT VEŘEJNÝCH ZAKÁZEK")
    print(f"{'='*80}\n")
    
    # Metadata
    print("📊 METADATA")
    print(f"   Období: {metadata.get('obdobi_od', 'N/A')} až {metadata.get('obdobi_do', 'N/A')}")
    print(f"   Celkem zakázek v originálu: {metadata.get('puvodni_pocet_zakazek', 'N/A')}")
    print(f"   Otevřených zakázek: {metadata.get('filtrovanych_zakazek', 'N/A')}")
    print(f"   ICT zakázek: {len(zakazky)}")
    print(f"   Filtrováno: {metadata.get('filtrovano_datum', 'N/A')[:19]}")
    
    if not zakazky:
        print("\n❌ Žádné ICT zakázky nebyly nalezeny.")
        return
    
    # Statistiky
    print(f"\n{'='*80}")
    print("📈 STATISTIKY")
    print(f"{'='*80}\n")
    
    druhy = Counter()
    rezimy = Counter()
    celkova_hodnota = 0
    hodnoty = []
    lhuty = []
    cpv_kody = Counter()
    
    for zakazka in zakazky:
        vz = zakazka.get('verejna_zakazka', {})
        
        # Druh
        druh = vz.get('druh_verejne_zakazky')
        if druh:
            druhy[druh] += 1
        
        # Režim
        rezim = vz.get('rezim_verejne_zakazky')
        if rezim:
            rezimy[rezim] += 1
        
        # Hodnota
        hodnota = vz.get('predpokladana_hodnota_bez_DPH_v_CZK')
        if hodnota:
            celkova_hodnota += hodnota
            hodnoty.append(hodnota)
        
        # CPV kódy
        predmet = vz.get('predmet', {})
        cpv = predmet.get('hlavni_kod_CPV')
        if cpv:
            cpv_prefix = cpv[:2]  # První 2 číslice
            cpv_kody[cpv_prefix] += 1
        
        # Lhůty
        for cast in vz.get('casti_verejne_zakazky', []):
            zp = cast.get('zadavaci_postup_pro_cast', {})
            for lhuta in zp.get('lhuty', []):
                if 'podání nabíd' in lhuta.get('druh_lhuty', ''):
                    datum_konce = lhuta.get('datum_a_cas_konce_lhuty')
                    if datum_konce:
                        lhuty.append(datum_konce)
                        break
    
    # Druh zakázky
    print("🏷️  Rozdělení podle druhu:")
    for druh, count in druhy.most_common():
        percent = count / len(zakazky) * 100
        print(f"   {druh}: {count} ({percent:.1f}%)")
    
    # Režim
    print("\n📋 Rozdělení podle režimu:")
    for rezim, count in rezimy.most_common():
        percent = count / len(zakazky) * 100
        print(f"   {rezim}: {count} ({percent:.1f}%)")
    
    # CPV kódy
    print("\n🏗️  Top CPV kategorie:")
    cpv_names = {
        '48': 'Software a informační systémy',
        '72': 'IT služby',
        '30': 'Počítačová zařízení',
        '45': 'Stavební práce',
        '50': 'Opravy a údržba',
        '77': 'Zemědělství, lesnictví',
        '75': 'Veřejná správa',
    }
    for cpv, count in cpv_kody.most_common(5):
        name = cpv_names.get(cpv, 'Ostatní')
        percent = count / len(zakazky) * 100
        print(f"   CPV {cpv}** ({name}): {count} ({percent:.1f}%)")
    
    # Hodnoty
    if hodnoty:
        print("\n💰 Finanční statistiky:")
        print(f"   Celková hodnota: {format_currency(celkova_hodnota)}")
        print(f"   Průměrná hodnota: {format_currency(sum(hodnoty)/len(hodnoty))}")
        print(f"   Minimální hodnota: {format_currency(min(hodnoty))}")
        print(f"   Maximální hodnota: {format_currency(max(hodnoty))}")
        print(f"   Zakázek s uvedenou hodnotou: {len(hodnoty)}/{len(zakazky)}")
    
    # Lhůty
    if lhuty:
        print("\n⏰ Lhůty:")
        now = datetime.now()
        lhuty_sorted = sorted(lhuty)
        
        nejblizsi = lhuty_sorted[0] if lhuty_sorted else None
        if nejblizsi:
            try:
                nejblizsi_dt = datetime.fromisoformat(nejblizsi.replace('Z', '+00:00'))
                rozdil = (nejblizsi_dt - now).days
                print(f"   Nejbližší lhůta: {format_date(nejblizsi)} (za {rozdil} dní)")
            except:
                print(f"   Nejbližší lhůta: {nejblizsi}")
        
        nejvzdalenejsi = lhuty_sorted[-1] if lhuty_sorted else None
        if nejvzdalenejsi:
            print(f"   Nejvzdálenější lhůta: {format_date(nejvzdalenejsi)}")
    
    # Seznam zakázek
    print(f"\n{'='*80}")
    print("📝 SEZNAM ICT ZAKÁZEK")
    print(f"{'='*80}\n")
    
    for i, zakazka in enumerate(zakazky, 1):
        vz = zakazka.get('verejna_zakazka', {})
        
        print(f"\n{i}. {vz.get('identifikator_NIPEZ', 'N/A')}")
        print(f"   {'─' * 76}")
        
        # Název
        nazev = vz.get('nazev_verejne_zakazky', 'Bez názvu')
        print(f"   📌 {nazev}")
        
        # Základní info
        druh = vz.get('druh_verejne_zakazky', 'N/A')
        rezim = vz.get('rezim_verejne_zakazky', 'N/A')
        print(f"   🏷️  {druh} | {rezim}")
        
        # Hodnota
        hodnota = vz.get('predpokladana_hodnota_bez_DPH_v_CZK')
        print(f"   💰 {format_currency(hodnota)}")
        
        # CPV kód
        predmet = vz.get('predmet', {})
        cpv = predmet.get('hlavni_kod_CPV')
        if cpv:
            print(f"   🏗️  CPV: {cpv}")
        
        # Lhůta
        for cast in vz.get('casti_verejne_zakazky', []):
            zp = cast.get('zadavaci_postup_pro_cast', {})
            for lhuta in zp.get('lhuty', []):
                if 'podání nabíd' in lhuta.get('druh_lhuty', ''):
                    datum_konce = lhuta.get('datum_a_cas_konce_lhuty')
                    if datum_konce:
                        try:
                            dt = datetime.fromisoformat(datum_konce.replace('Z', '+00:00'))
                            now = datetime.now()
                            dny_do_konce = (dt - now).days
                            
                            if dny_do_konce < 0:
                                status = "⚠️  VYPRŠELA"
                            elif dny_do_konce <= 3:
                                status = "🔴 VELMI BLÍZKO"
                            elif dny_do_konce <= 7:
                                status = "🟡 BLÍZKO"
                            else:
                                status = "🟢 V POŘÁDKU"
                            
                            print(f"   ⏰ Lhůta: {format_date(datum_konce)} (za {dny_do_konce} dní) {status}")
                        except:
                            print(f"   ⏰ Lhůta: {datum_konce}")
                        break
            
            # URL pro podání
            spec_podani = zp.get('specifikace_podani', {})
            url_podani = spec_podani.get('internetova_adresa_pro_podani')
            if url_podani:
                print(f"   🌐 Podání: {url_podani}")
            
            # Dokumentace
            for dok in zp.get('informace_o_zadavacich_dokumentacich', []):
                url_dok = dok.get('zadavaci_dokumentace_je_dostupna_na')
                if url_dok:
                    print(f"   📄 Dokumentace: {url_dok}")
                    break
            
            break  # Jen první část
        
        # Popis (zkrácený)
        popis = predmet.get('popis_predmetu', '')
        if popis:
            popis_short = popis[:200] + '...' if len(popis) > 200 else popis
            print(f"   📝 {popis_short}")
    
    print(f"\n{'='*80}")
    print(f"  KONEC PŘEHLEDU")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    file_path = '../data/VZ/VZ-2026-01-ICT.json'
    analyze_ict_tenders(file_path)
