# Datový model ISVZ - VZ-2026-01.json

## 📋 Přehled

Soubor obsahuje **71 377 veřejných zakázek** za období **leden 2026**.

## Metadata souboru

- **obdobi_od**: 2026-01-01T00:00:00
- **obdobi_do**: 2026-01-31T23:59:59
- **verze**: 2.6.2

---

## 🎯 Jak filtrovat OTEVŘENÉ zakázky (pro ucházení)

### Kritéria pro identifikaci otevřených zakázek:

1. ✅ **Datum ukončení postupu** = `null`
   - Cesta: `verejna_zakazka.casti_verejne_zakazky[].zadavaci_postup_pro_cast.datum_ukonceni_zadavaciho_postupu`

2. ✅ **Výsledek ukončení** = `null`
   - Cesta: `verejna_zakazka.casti_verejne_zakazky[].zadavaci_postup_pro_cast.vysledek.vysledek_ukonceni_zadavaciho_postupu`

3. ✅ **Lhůta pro podání nabídky** = existuje a je v budoucnosti
   - Cesta: `verejna_zakazka.casti_verejne_zakazky[].zadavaci_postup_pro_cast.lhuty[]`
   - Druh: `"Lhůta pro podání nabídky"` nebo `"Lhůta pro podání žádosti o účast"`
   - Kontrola: `datum_a_cas_konce_lhuty > DNES`

4. ✅ **Stav** ≠ `"Dokončen/Zadán"`, `"Ukončeno plnění smlouvy"`, `"Zrušen"`
   - Cesta: `verejna_zakazka.casti_verejne_zakazky[].zadavaci_postup_pro_cast.stav`
   - Ideální hodnota: `"Aktivní/Neukončen"` nebo `null`

### Příklad filtrovacího kódu (Python):

```python
from datetime import datetime

def is_open_tender(zakazka):
    """Zkontroluje, zda je zakázka otevřená pro ucházení"""
    vz = zakazka.get('verejna_zakazka', {})
    
    for cast in vz.get('casti_verejne_zakazky', []):
        zp = cast.get('zadavaci_postup_pro_cast', {})
        
        # 1. Nemá datum ukončení
        if zp.get('datum_ukonceni_zadavaciho_postupu'):
            continue
        
        # 2. Nemá výsledek ukončení
        vysledek = zp.get('vysledek', {})
        if vysledek.get('vysledek_ukonceni_zadavaciho_postupu'):
            continue
        
        # 3. Zkontroluj lhůty
        now = datetime.now()
        has_active_deadline = False
        
        for lhuta in zp.get('lhuty', []):
            druh = lhuta.get('druh_lhuty', '')
            if 'podání nabíd' in druh or 'podání žádosti' in druh:
                datum_konce = lhuta.get('datum_a_cas_konce_lhuty')
                if datum_konce:
                    try:
                        konce_dt = datetime.fromisoformat(datum_konce.replace('Z', '+00:00'))
                        if konce_dt > now:
                            has_active_deadline = True
                            break
                    except:
                        pass
        
        if has_active_deadline:
            return True
    
    return False
```

---

## 📊 Statistiky

### Stavy zadávacího postupu

| Stav | Počet | Popis |
|------|-------|-------|
| Dokončen/Zadán | 53 582 | ❌ Zakázka již zadána |
| Ukončeno plnění smlouvy | 17 666 | ❌ Smlouva dokončena |
| Zrušen | 12 672 | ❌ Postup zrušen |
| **Aktivní/Neukončen** | **407** | ✅ **Otevřená zakázka!** |
| Neúspěšný | 40 | ❌ Neúspěšný postup |

### Druhy lhůt (pro kontrolu termínů)

| Druh lhůty | Počet |
|------------|-------|
| **Lhůta pro podání nabídky** | **82 288** | ← KLÍČOVÉ! |
| **Lhůta pro podání žádosti o účast** | **710** | ← KLÍČOVÉ! |
| Lhůta pro podání žádosti o vysvětlení ZD | 5 875 |
| Lhůta pro vysvětlení zadávací dokumentace | 3 628 |
| Zadávací lhůta | 1 689 |

### Klíčová pole pro obecné filtrování

#### Dostupné sekce v záznamu zakázky

- `verejna_zakazka` - hlavní informace o zakázce
- `historie_lhut` - historie změn lhůt
- `zdroj_dat` - zdroj dat (obvykle "VVZ")

#### Režim veřejné zakázky

- `Nadlimitní` (velké zakázky nad limity EU)
- `Podlimitní` (střední zakázky)
- `Veřejné zakázky malého rozsahu` (malé zakázky)

#### Druh veřejné zakázky

- `Dodávky` (nákup zboží)
- `Služby` (poskytování služeb)
- `Stavební práce` (stavby a rekonstrukce)

#### Typ veřejné zakázky

- `Nadlimitní veřejná zakázka`
- `Podlimitní veřejná zakázka`
- `Veřejná zakázka malého rozsahu`
---

## 📖 Příklady zakázek

### ✅ Příklad OTEVŘENÉ zakázky

**RVZ2600001221**: Revitalizace volnočasového areálu Svatošské údolí

- **Druh**: Stavební práce
- **Datum zahájení**: 2026-01-08T13:26:06
- **Datum ukončení**: `None` *(NULL = probíhá)* ✅
- **Stav**: `None` *(není dokončen)* ✅
- **Výsledek ukončení**: `None` *(probíhá)* ✅
- **Lhůty**:
  - 🕒 **Lhůta pro podání nabídky**: konec **2026-02-09 09:00** ✅
  - Zadávací lhůta: konec `None`

### ❌ Příklady UZAVŘENÝCH zakázek

**RVZ2600001263**: Překlady anotací pro odborné příspěvky pro účely DKRVO

- **Druh**: Služby
- **Datum zahájení**: 2025-11-28T00:00:00
- **Stav**: `Dokončen/Zadán` ❌
- **Výsledek ukončení**: `Uzavření smlouvy` ❌

**RVZ2600001679**: 03 Výzva k RD - oprava stanových přístřešků k PV3S

- **Druh**: Služby
- **Datum zahájení**: 2025-03-20T06:56:48
- **Datum ukončení**: 2025-05-28T07:09:59 ❌
- **Stav**: `Ukončeno plnění smlouvy` ❌
- **Výsledek ukončení**: `Uzavření smlouvy` ❌

---

## 🏗️ Struktura datového modelu

### Navigace k zadávacímu postupu

```
data[]                                              // Pole všech zakázek
  └─ verejna_zakazka                               // Hlavní objekt zakázky
       ├─ identifikator_NIPEZ                      // Jedinečný identifikátor
       ├─ nazev_verejne_zakazky                    // Název zakázky
       ├─ druh_verejne_zakazky                     // Dodávky/Služby/Stavební práce
       ├─ rezim_verejne_zakazky                    // Nadlimitní/Podlimitní/VZMR
       ├─ predpokladana_hodnota_bez_DPH_v_CZK      // Odhadovaná cena
       │
       └─ casti_verejne_zakazky[]                  // Zakázka může mít více částí
            ├─ identifikator_NIPEZ
            ├─ nazev_casti_verejne_zakazky
            ├─ predmet                              // CPV kódy, místo plnění
            │
            └─ zadavaci_postup_pro_cast             // ⭐ KLÍČOVÁ SEKCE!
                 ├─ druh_zadavaciho_postupu         // Otevřené řízení, atd.
                 ├─ datum_zahajeni_zadavaciho_postupu
                 ├─ datum_ukonceni_zadavaciho_postupu    // NULL = aktivní ✅
                 ├─ stav                                  // Aktivní/Neukončen ✅
                 │
                 ├─ lhuty[]                               // ⭐ Termíny!
                 │    ├─ druh_lhuty
                 │    ├─ datum_a_cas_konce_lhuty         // > DNES ✅
                 │    ├─ datum_a_cas_zacatku_lhuty
                 │    └─ aktivni
                 │
                 ├─ vysledek                              // Výsledek postupu
                 │    ├─ vysledek_ukonceni_zadavaciho_postupu  // NULL = probíhá ✅
                 │    ├─ datum_a_cas_zruseni_postupu
                 │    ├─ smlouva[]
                 │    └─ vybrani_dodavatele_zadavaciho_postupu[]
                 │
                 ├─ pravidla_pro_hodnoceni                // Kritéria hodnocení
                 │    └─ kriteria_pro_hodnoceni_nabidek_nebo_navrhu[]
                 │
                 ├─ specifikace_podani                    // Jak podat nabídku
                 │    ├─ internetova_adresa_pro_podani
                 │    ├─ jazyk_podani
                 │    └─ popis_jistoty
                 │
                 └─ kriteria_kvalifikace                  // Požadavky na dodavatele
```

### Hierarchie polí (kompletní seznam)

```
historie_lhut: array[dict]
  datum_a_cas_zaznamu: string
  identifikator_NIPEZ_ke_kteremu_se_zaznamy_vztahuji: string
  zaznamy: array[dict]
    aktivni: null
    datum_a_cas_konce_lhuty: null
    datum_a_cas_zacatku_lhuty: null
    doba_trvani_lhuty: integer
    doba_trvani_lhuty_jednotka: string
    druh_lhuty: string
    identifikator: null
verejna_zakazka: object
  casova_znacka: string
  casti_verejne_zakazky: array[dict]
    druh_casti_verejne_zakazky: string
    hodnoty_koncese: array[]
    identifikator_NIPEZ: string
    identifikator_v_elektronickem_nastroji: null
    identifikatory_v_elektronickem_nastroji: array[dict]
      identifikator: string
      kod_nastroje: string
    informace_o_financnich_prostredcich_EU: array[]
    interniIdentifikatorVerejneZakazkyPridelenyZadavatelem: string
    maximalni_mozny_pocet_prodlouzeni_smlouvy: integer
    nazev_casti_verejne_zakazky: string
    oduvodneni_pouziti_zjednoduseneho_rezimu: null
    popis_prodlouzeni: null
    popis_vyhrazene_zmeny_zavazku: string
    predmet: object
      hlavni_kod_CPV: string
      mista_plneni: array[dict]
        dalsi_informace_o_miste_plneni: string
        kod_zeme_mista_plneni: string
        misto_plneni_jine: null
        nuts: string
      polozky_predmetu: array[]
      popis_predmetu: string
      v_oblasti_obrany_a_bezpecnosti: boolean
      vedlejsi_kod_CPV: array[str]
    predpokladana_hodnota_bude_uverejnena: boolean
    predpokladana_hodnota_casti_bez_DPH: float
    predpokladana_hodnota_casti_bez_DPH_mena: string
    predpokladana_hodnota_casti_bez_DPH_v_CZK: null
    predpokladana_hodnota_vsech_verejnych_zakazek_ktere_mohou_byt_zadany_na_zaklade_ramcove_dohody_bez_DPH: null
    predpokladana_hodnota_vsech_verejnych_zakazek_ktere_mohou_byt_zadany_na_zaklade_ramcove_dohody_bez_DPH_mena: null
    predpokladana_hodnota_vsech_verejnych_zakazek_ktere_mohou_byt_zadany_na_zaklade_ramcove_dohody_bez_DPH_v_CZK: null
    rezim_casti_verejne_zakazky: null
    rezim_dle_volby_zadavatele: null
    vedlejsi_druhy_casti_verejne_zakazky: array[]
    verejna_zakazka_je_alespon_castecne_financovana_z_prostredku_Evropske_unie: boolean
    vyhrazena_zmena_zavazku: null
    zadavaci_postup_pro_cast: object
      dalsi_informace: null
      dalsi_informace_v_souvislosti_s_odmenami: null
      dalsi_pozadavky: object
        informace_o_bezpecnostni_proverce: null
        je_pozadovana_bezpecnostni_proverka: boolean
        osvedceni_o_vzdelani_a_odborne_kvalifikaci_pracovniku: string
      datum_ukonceni_zadavaciho_postupu: null
      datum_zahajeni_zadavaciho_postupu: string
      doba_trvani: object
        datum_konce_doby_trvani: string
        datum_zacatku_doby_trvani: string
        doba_trvani: null
        doba_trvani_jednotka: null
        doba_trvani_jine: null
      dokumenty: array[]
      druh_zadavaciho_postupu: string
      duvod_pro_pouziti_vyjimky: null
      enviromentalni_zadavani_podle_kriterii: array[str]
      environmentalni_zadavani: array[]
      evidence_vysledku_zadavaciho_postupu: null
      hodnota_cen_odmen_jinych_plateb: null
      hodnota_cen_odmen_jinych_plateb_mena: null
      hodnoty_podanych_nabidek: null
      identifikator_CELEX_pravniho_predpisu_EU: null
      informace_o_dalsi_fazi_vicefazoveho_zadavaciho_postupu: array[]
      informace_o_danovych_pravnich_predpisech: array[]
      informace_o_otevirani_podani: array[]
      informace_o_pracovnepravnich_predpisech: array[]
      informace_o_predpisech_v_oblasti_zivotniho_prostredi: array[]
      informace_o_ramcove_dohode: object
        datum_konce_doby_trvani: null
        datum_zacatku_doby_trvani: null
        doba_trvani: null
        doba_trvani_jednotka: null
        doba_trvani_jine: null
        oduvodneni_doby_trvani_ramcove_dohody: null
        predpokladany_maximalni_pocet_ucastniku_ramcove_dohody: null
        ramcova_dohoda_ma_stanoven_maximalni_pocet_ucastniku: null
        typ_ramcove_dohody: null
        zpusob_zadavani_verejnych_zakazek_na_zaklade_ramcove_dohody: null
      informace_o_zadavacich_dokumentacich: array[dict]
        informace_o_pristupu_k_zadavaci_dokumentaci_jsou_na: null
        oduvodneni_omezeneho_pristupu_k_zadavaci_dokumentaci: null
        pristup_k_zadavaci_dokumentaci_je_omezen: boolean
        zadavaci_dokumentace_je_dostupna_na: string
      je_pozadovana_pravni_forma_seskupeni_dodavatelu_jimz_bude_verejna_zakazka_zadana: boolean
      kategorie_zadavaciho_postupu: null
      kriteria_kvalifikace: object
        ekonomicka_kvalifikace: null
        kriteria_kvalifikace: array[]
        profesni_zpusobilost: null
        technicka_kvalifikace: null
        zakladni_zpusobilost: null
        zakladni_zpusobilost_a_duvody_pro_vylouceni: array[str]
        zdroj_kriterii_kvalifikace: string
      lhuty: array[dict]
        aktivni: null
        datum_a_cas_konce_lhuty: null
        datum_a_cas_zacatku_lhuty: null
        doba_trvani_lhuty: integer
        doba_trvani_lhuty_jednotka: string
        druh_lhuty: string
        identifikator: null
      namitky: array[]
      narizeni_o_zahranicnich_subvencich: boolean
      navaznost_na_vysledek_jineho_zadavaciho_postupu: null
      nestandardni_stavy: array[]
      obchodni_nebo_jine_podminky: object
        bude_pouzita_elektronicka_platba: boolean
        budou_pouzivany_elektronicke_objednavky: boolean
        dalsi_zvlastni_podminky_kterym_podleha_plneni_zakazky_predevsim_pokud_jde_o_zabezpeceni_dodavek_a_duvernost_informaci: null
        hlavni_podminky_financovani_a_platebni_podminky_pripadne_odkaz_na_prislusna_ustanoveni_ktera_tyto_podminky_upravuji: string
      ocenovane_umisteni: null
      odkaz_na_profil: null
      oduvodneni_jednaciho_rizeni_bez_uverejneni: array[]
      oduvodneni_pouziti_jrsu_nebo_soutezniho_dialogu: null
      oduvodneni_pouziti_zkraceni_lhuty_v_zadavacim_postupu: null
      plneni_teto_verejne_zakazky_je_vyhrazeno_v_ramci_programu_chranenych_zamestnani: boolean
      plneni_zakazky_vyhrazeno_v_ramci_programu_chranenych_zamestnani: boolean
      pocet_zaslanych_zaevidovanych_vysvetleni_zadavaci_dokumentace: null
      podane_nabidky_nebo_zadosti_o_ucast: array[]
      popis_odpovedneho_zadavani: array[dict]
        oduvodneni_nezohledneni_odpovedneho_zadavani: null
        popis_odpovedneho_zadavani: null
        typ_odpovedneho_zadavani: string
      popis_zadavaciho_postupu_v_pripade_ze_se_jedna_o_dobrovolne_uverejneni_v_TED: null
      povinnosti_v_souvislosti_s_vyuzitim_poddodavatele: array[]
      pravidla_pro_hodnoceni: object
        dalsi_informace_o_pouziti_elektronicke_aukce: null
        ekonomicka_vyhodnost: null
        hodnoceni_nabidkove_ceny: null
        hodnota_pevne_ceny_bez_DPH: null
        hodnota_pevne_ceny_s_DPH: null
        internetova_adresa_elektronicke_aukce: null
        kriteria_pro_hodnoceni_nabidek_nebo_navrhu: array[dict]
          cleneni_nabidkove_ceny: null
          druh_kriteria: string
          identifikace: string
          jednotka: null
          kriterium_je_ciselne_vyjadritelne: null
          nazev_kriteria: string
          omezeni_shora_pro_ucely_hodnoceni: null
          omezeni_shora_pro_vylouceni: null
          omezeni_zdola_pro_ucely_hodnoceni: null
          omezeni_zdola_pro_vylouceni: null
          popis_kriteria_hodnoceni: string
          poradi: null
          subkriteria_pro_hodnoceni_nabidek_nebo_navrhu: array[]
          typ_kriteria: null
          typ_vztahu_kriteria: null
          vaha: string
          vaha_kriteria: float
        mena: null
        metoda_hodnoceni: null
        pevna_cena_za_jednotku_nebo_celkem: null
        pouziti_automatickeho_losu_v_pripade_shodneho_hodnoceni: null
        pouziti_elektronicke_aukce_v_zadavacim_postupu: boolean
        vzorec_pro_hodnoceni: null
      pravni_forma_kterou_musi_mit_seskupeni_dodavatelu_jimz_bude_verejna_zakazka_zadana: null
      pravni_predpis_EU: string
      pravni_predpis_EU_na_zaklade_nehoz_probiha_zadavaci_postup: null
      presne_informace_o_lhutach_pro_prezkumna_rizeni: null
      pusobnost_mezinarodni_dohody_o_verejnych_zakazkach: boolean
      socialne_odpovedne_zadavani: array[str]
      specifikace_podani: object
        budou_prijimany_varianty_nabidky: boolean
        internetova_adresa_pro_podani: string
        jazyk_podani: string
        je_pozadovan_uznavany_elektronicky_podpis_nebo_pecet: boolean
        jistota: boolean
        nabidky_musi_byt_podany_ve_forme_elektronickych_katalogu_nebo_musi_zahrnovat_elektronicky_katalog: boolean
        oduvodneni_nemoznosti_elektronickeho_podavani: null
        popis_jistoty: string
        popis_listinneho_podani: null
        povoleni_odtajneni_podani_pred_vyprsenim_lhuty: null
        typ_aktualniho_podani: null
        zadavatel_provede_nakup_z_elektronickych_katalogu_vice_dodavatelu: null
        zpusob_podani: string
      spolecne_zadavani_zadavatelu_z_ruznych_statu: array[dict]
        popis: string
        rozhodny_pravni_predpis_pro_zadavani_verejne_zakazky_a_jeho_prezkum: string
      stav: null
      stret_zajmu: array[]
      ucastnici: array[]
      ucastnici_jimz_zanikla_ucast_v_zadavacim_postupu: array[]
      udeleni_cen_odmen_jinych_plateb: null
      uplatneni_podminek_pristupnosti_pro_osoby_s_postizenim_v_technickych_specifikacich: array[dict]
        oduvodneni_proc_nebyly_zahrnuty_podminky_pristupnosti: null
        uplatneni_podminek_pristupnosti_pro_osoby_s_postizenim: string
      verejna_zakazka_je_vhodna_pro_male_a_stredni_podniky: boolean
      verejny_ZP: null
      vysledek: object
        datum_a_cas_zruseni_postupu: string
        oduvodneni_zruseni_zadavaciho_postupu: null
        smlouva: array[]
        udaje_o_nizkoemisnich_vozidlech: array[]
        vybrani_dodavatele_zadavaciho_postupu: array[]
        vysledek_ukonceni_zadavaciho_postupu: null
      zadavani_inovaci: array[str]
      zadavatel_postupuje_dle_parag_61_odst_3_ZZVZ: boolean
      zadavatel_si_vyhrazuje_pravo_zadat_verejnou_zakazku_na_zaklade_puvodnich_nabidek_bez_dalsich_jednani: null
      zkraceni_lhuty: boolean
  druh_verejne_zakazky: string
  hodnoty_koncese: array[]
  identifikator_NIPEZ: string
  identifikator_v_elektronickem_nastroji: null
  identifikatory_v_elektronickem_nastroji: array[dict]
    identifikator: string
    kod_nastroje: string
  interniIdentifikatorVerejneZakazkyPridelenyZadavatelem: null
  nazev_verejne_zakazky: string
  oduvodneni_nerozdeleni_nadlimitni_verejne_zakazky_na_casti: null
  predmet: object
    hlavni_kod_CPV: string
    mista_plneni: array[dict]
      dalsi_informace_o_miste_plneni: string
      kod_zeme_mista_plneni: string
      misto_plneni_jine: null
      nuts: string
    polozky_predmetu: array[]
    popis_predmetu: string
    v_oblasti_obrany_a_bezpecnosti: boolean
    vedlejsi_kod_CPV: array[]
  predpokladana_hodnota_bez_DPH: float
  predpokladana_hodnota_bez_DPH_mena: string
  predpokladana_hodnota_bez_DPH_v_CZK: float
  predpokladana_hodnota_bude_uverejnena: boolean
  predpokladana_hodnota_vsech_verejnych_zakazek_ktere_mohou_byt_zadany_na_zaklade_ramcove_dohody_bez_DPH: null
  predpokladana_hodnota_vsech_verejnych_zakazek_ktere_mohou_byt_zadany_na_zaklade_ramcove_dohody_bez_DPH_mena: null
  predpokladana_hodnota_vsech_verejnych_zakazek_ktere_mohou_byt_zadany_na_zaklade_ramcove_dohody_bez_DPH_v_CZK: null
  rezim_dle_volby_zadavatele: null
  rezim_verejne_zakazky: string
  typ_verejne_zakazky_dle_vyse_predpokladane_hodnoty: string
  vedlejsi_druhy_verejne_zakazky: array[]
  zadavaci_postupy: array[dict]
    dalsi_informace: null
    do_kterych_casti_muze_dodavatel_podat_nabidku: null
    evidencni_cislo_zadavaciho_postupu_ve_VVZ: null
    evidencni_cislo_zadavaciho_postupu_ve_vestniku_verejnych_zakazek: string
    externi_administrator: array[]
    identifikator_NIPEZ: string
    identifikator_v_elektronickem_nastroji: null
    identifikatory_v_elektronickem_nastroji: array[dict]
      identifikator: string
      kod_nastroje: string
    nejvyssiPocetCastiKtereMohouBytZadanyJednomuUchazeci: null
    pocetCastiDoKterychMuzeBytNabidkaPodana: null
    uverejnovaci_formulare: array[dict]
      datum_a_cas_odeslani_do_TED: null
      datum_a_cas_odeslani_k_uverejneni: string
      datum_a_cas_uverejneni_v_TED: null
      datum_a_cas_uverejneni_ve_VVZ: string
      evidencni_cislo_formulare: string
      hodnota_vsech_verejnych_zakazek_uvedenych_v_oznameni: null
      hodnota_vsech_verejnych_zakazek_uvedenych_v_oznameni_mena: null
      identifikator_oznameni_verze: null
      opravy: array[dict]
        datum_a_cas_kdy_byla_zadavaci_dokumentace_opravena: string
        oduvodneni_opravy: string
        oprava_zadavaci_dokumentace_nebo_souteznich_podminek: boolean
        popis_duvodu_opravy: string
        popis_opravy: string
      typ_formulare: string
      typ_oznameni: string
      verze_oznameni: null
    zadavaci_postupy_pro_casti: array[dict]
      identifikator_NIPEZ: string
      identifikator_v_elektronickem_nastroji: null
      identifikatory_v_elektronickem_nastroji: array[dict]
        identifikator: string
        kod_nastroje: string
    zadavatel_zadavaciho_postupu: object
      pravidla_pro_postup_zadavatele: null
      zadavatele: array[dict]
        adresa_profilu: string
        hlavni_predmet_cinnosti_verejneho_zadavatele: string
        kategorie_zadavatele: string
        predmet_relevantni_cinnosti: null
        provozni_jednotka_s_funkcni_samostatnosti: object
          kod_NUTS: null
          nazev_provozni_jednotky_s_funkcni_samostatnosti: null
          sidlo: null
        role_zadavatele: string
        subjekt: object
          ico: string
          identifikator_v_elektronickem_nastroji: null
          jiny_identifikator: null
          kod_NUTS: string
          maly_a_stredni_podnik: null
          nazev_subjektu: string
          nipez_id_subjektu: null
          sidlo: null
          stat_adresa: null
        zadava_zadavaci_postup: null
zdroj_dat: string
```


## Ukázka záznamu (zkrácená)

```

---

## 📌 Souhrn - Rychlý návod

### Pro filtrování otevřených zakázek kontrolujte:

1. **Navigace**: `data[].verejna_zakazka.casti_verejne_zakazky[].zadavaci_postup_pro_cast`

2. **Musí platit**:
   - `datum_ukonceni_zadavaciho_postupu` je `null`
   - `vysledek.vysledek_ukonceni_zadavaciho_postupu` je `null`
   - `lhuty[]` obsahuje aktivní lhůtu s `druh_lhuty` = "Lhůta pro podání nabídky"
   - `datum_a_cas_konce_lhuty` je v budoucnosti (> DNES)
   - `stav` není "Dokončen/Zadán", "Ukončeno plnění smlouvy" nebo "Zrušen"

### Užitečná pole:

- **Základní info**: `identifikator_NIPEZ`, `nazev_verejne_zakazky`, `druh_verejne_zakazky`
- **Hodnota**: `predpokladana_hodnota_bez_DPH_v_CZK`
- **Místo**: `predmet.mista_plneni[].nuts`
- **CPV kód**: `predmet.hlavni_kod_CPV`
- **Zadávání**: `druh_zadavaciho_postupu`
- **Podání**: `specifikace_podani.internetova_adresa_pro_podani`
- **Dokumentace**: `informace_o_zadavacich_dokumentacich[].zadavaci_dokumentace_je_dostupna_na`

### Odhad otevřených zakázek:

Ze statistik: **~407 zakázek** má stav "Aktivní/Neukončen" a **14 865 aktivních lhůt** bylo nalezeno.

---

*Vygenerováno analýzou souboru VZ-2026-01.json obsahujícího 71 377 veřejných zakázek*
