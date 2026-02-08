# Doporučená Nevyužitá Pole pro MD/CSV Reporty

## 📊 Přehled

Analýza souboru `data/VZ/VZ-2026-01-ICT.json` (145 zakázek) identifikovala užitečná pole, která **ZATÍM NEJSOU** v MD a CSV reportech.

---

## ⭐ TOP 10 Doporučení (seřazeno podle užitečnosti)

### 1. 🏆 **Kritéria hodnocení nabídek**

**Cesta:** `verejna_zakazka.casti_verejne_zakazky[0].zadavaci_postup_pro_cast.pravidla_pro_hodnoceni.kriteria_pro_hodnoceni_nabidek_nebo_navrhu[]`

**Vyplněnost:** ~100% (všechny zakázky mají kritéria)

**Ukázka:**
```json
[
  {
    "nazev_kriteria": "Nabídková cena",
    "vaha_kriteria": 60,
    "druh_kriteria": "Cena"
  },
  {
    "nazev_kriteria": "Technická úroveň",
    "vaha_kriteria": 40,
    "druh_kriteria": "Kvalita"
  }
]
```

**Proč je užitečné:**
- Vidíš **váhu technické kvality vs. ceny** (ne jen cena!)
- Vysoká váha kvality = příležitost pro inovativní řešení
- Nízká váha ceny = konkurence na technologii, ne na ceně

**Doporučení pro report:**
- MD: Sekce "Kritéria hodnocení" s tabulkou kritérií a vah
- CSV: Nové sloupce: `Kritérium 1 (%)`, `Kritérium 2 (%)`, nebo `Váha ceny (%)`, `Váha kvality (%)`

---

### 2. 🇪🇺 **Financování z EU**

**Cesta:** `verejna_zakazka.casti_verejne_zakazky[0].verejna_zakazka_je_alespon_castecne_financovana_z_prostredku_Evropske_unie`

**Vyplněnost:** ~36% (53 zakázek)

**Ukázka:** `true` / `false`

**Proč je užitečné:**
- EU projekty mají **specifické požadavky** (public reporting, transparence)
- Často **delší platební cykly**
- Vyšší nároky na **dokumentaci a compliance**
- Pozitivní: EU projekty = **vyšší rozpočty**

**Doporučení pro report:**
- MD: Přiddat ke "Základní informace" jako `- **Financování EU**: Ano/Ne`
- CSV: Nový sloupec `Financování EU` s hodnotami `Ano`/`Ne`/`-`

---

### 3. 🏢 **Kategorie a sektor zadavatele**

**Cesta:** 
- `verejna_zakazka.zadavaci_postupy[0].zadavatel_zadavaciho_postupu.zadavatele[0].kategorie_zadavatele`
- `verejna_zakazka.zadavaci_postupy[0].zadavatel_zadavaciho_postupu.zadavatele[0].hlavni_predmet_cinnosti_verejneho_zadavatele`

**Vyplněnost:** 92% (kategorie), 52% (hlavní předmět)

**Ukázka:**
- Kategorie: `"Česká republika a její státní orgány"`, `"Územní samosprávný celek"`, `"Veřejnoprávní instituce"`
- Hlavní předmět: `"Vzdělávání"`, `"Zdraví"`, `"Obecné veřejné služby"`, `"Sociální ochrana"`

**Proč je užitečné:**
- **Segmentace trhu** - vidíš, zda jde o stát, obce, školy, nemocnice...
- **Prioritizace** - např. zaměření jen na vysoké školy nebo zdravotnictví
- **Strategické plánování** - kde je největší poptávka po tvém portfoliu

**Doporučení pro report:**
- MD: Přidat k "Zadavatel": `- **Kategorie**: Územní samosprávný celek` + `- **Sektor**: Vzdělávání`
- CSV: Nové sloupce `Kategorie zadavatele`, `Sektor zadavatele`

---

### 4. 📅 **Doba trvání smlouvy**

**Cesta:** 
- `verejna_zakazka.casti_verejne_zakazky[0].doba_trvani.doba_trvani`
- `verejna_zakazka.casti_verejne_zakazky[0].doba_trvani.doba_trvani_jednotka`

**Vyplněnost:** Mix (~30-50% podle části)

**Ukázka:** `36` + `"měsíce"` = 3 roky, `730` + `"dny"` = 2 roky

**Proč je užitečné:**
- **Plánování kapacit** - dlouhé smlouvy = stabilní příjem
- **Strategie** - krátké smlouvy = rychlý cash, dlouhé = vztahy
- **Riziko** - delší smlouvy = větší závazek

**Doporučení pro report:**
- MD: Přidat sekci "Doba trvání smlouvy": `- **Délka**: 36 měsíců (3 roky)`
- CSV: Nový sloupec `Doba trvání` s normalizací na měsíce nebo roky

---

### 5. 💳 **Elektronická platba a objednávky**

**Cesta:** 
- `verejna_zakazka.casti_verejne_zakazky[0].zadavaci_postup_pro_cast.obchodni_nebo_jine_podminky.bude_pouzita_elektronicka_platba`
- `verejna_zakazka.casti_verejne_zakazky[0].zadavaci_postup_pro_cast.obchodni_nebo_jine_podminky.budou_pouzivany_elektronicke_objednavky`

**Vyplněnost:** 94% (platba), 70% (objednávky)

**Ukázka:** `true` / `false`

**Proč je užitečné:**
- **Signál digitální zralosti** zadavatele
- **Rychlejší cash flow** (elektronické platby)
- **Efektivita procesů** (elektronické objednávky)
- Pozitivní pro **malé firmy** - méně papírování

**Doporučení pro report:**
- MD: Přidat k "Obchodní podmínky": `- **Elektronická platba**: Ano` + `- **Elektronické objednávky**: Ano`
- CSV: Nové sloupce `E-platba`, `E-objednávky` s `Ano`/`Ne`/`-`

---

### 6. 🔄 **Rámcová dohoda - detaily**

**Cesta:** 
- `verejna_zakazka.casti_verejne_zakazky[0].zadavaci_postup_pro_cast.informace_o_ramcove_dohode.zpusob_zadavani_verejnych_zakazek_na_zaklade_ramcove_dohody`
- `verejna_zakazka.casti_verejne_zakazky[0].zadavaci_postup_pro_cast.informace_o_ramcove_dohode.predpokladany_maximalni_pocet_ucastniku_ramcove_dohody`

**Vyplněnost:** 15% (způsob), 12% (počet účastníků)

**Ukázka:**
- Způsob: `"Zadávání veřejných zakázek bez obnovení soutěže"`, `"Zadávání veřejných zakázek s obnovením soutěže"`
- Počet: `1`, `3`, `6`

**Proč je užitečné:**
- **Bez obnovení soutěže** = jedna firma vyhrává vše po dobu trvání
- **S obnovením** = opakovaná šance v mini-soutěžích
- **Počet účastníků**: 1 = monopsonium (winner-takes-all), 6 = sdílený trh
- Strategické pro **dlouhodobé vztahy**

**Doporučení pro report:**
- MD: Nová sekce "Rámcová dohoda" (jen pokud existuje): `- **Způsob zadávání**: Bez obnovení soutěže` + `- **Max. počet účastníků**: 3`
- CSV: Nové sloupce `Je rámcová dohoda`, `RD - způsob`, `RD - počet účastníků`

---

### 7. 🏅 **Vhodnost pro malé a střední podniky**

**Cesta:** `verejna_zakazka.casti_verejne_zakazky[0].zadavaci_postup_pro_cast.verejna_zakazka_je_vhodna_pro_male_a_stredni_podniky`

**Vyplněnost:** ~43% (62 zakázek)

**Ukázka:** `true` / `false`

**Proč je užitečné:**
- **Signál přístupnosti** pro menší firmy
- Zadavatel **aktivně podporuje SME** (méně byrokracie, menší kauce...)
- Pozitivní pro tvůj profil (startup/SME)

**Doporučení pro report:**
- MD: Přidat k "Základní informace": `- **Vhodné pro SME**: Ano`
- CSV: Nový sloupec `Vhodné pro SME` s `Ano`/`Ne`/`-`

---

### 8. 📆 **Datum zahájení zadávacího postupu**

**Cesta:** `verejna_zakazka.casti_verejne_zakazky[0].zadavaci_postup_pro_cast.datum_zahajeni_zadavaciho_postupu`

**Vyplněnost:** ~100%

**Ukázka:** `"2026-01-07T07:48:25"`

**Proč je užitečné:**
- **Časová osa** - jak dlouho už zakázka běží
- **Urgence** - čerstvé vs. dlouhodobé soutěže
- **Trend** - sezónnost nových zakázek

**Doporučení pro report:**
- MD: Přidat k "Lhůty": `- **Zahájeno**: 07.01.2026 07:48`
- CSV: Nový sloupec `Datum zahájení` (formát DD.MM.YYYY)

---

### 9. 🔐 **Jistota (kauce)**

**Cesta:** 
- `verejna_zakazka.casti_verejne_zakazky[0].zadavaci_postup_pro_cast.specifikace_podani.jistota.vyse_jistoty`
- `verejna_zakazka.casti_verejne_zakazky[0].zadavaci_postup_pro_cast.specifikace_podani.jistota.vyse_jistoty_mena`

**Vyplněnost:** ~9% (13 zakázek)

**Ukázka:** `500000` + `"CZK"` = 500 tis. Kč kauce

**Proč je užitečné:**
- **Finanční bariéra vstupu** - vysoká kauce = problém pro malé firmy
- **Signál rizika** - zadavatel chce zajištění serióznosti
- **Strategické rozhodnutí** - stojí to za to?

**Doporučení pro report:**
- MD: Přidat k "Základní informace" (pokud existuje): `- **Jistota (kauce)**: 500 000 Kč`
- CSV: Nový sloupec `Jistota (Kč)`

---

### 10. 📊 **Typ zakázky dle výše hodnoty**

**Cesta:** `verejna_zakazka.typ_verejne_zakazky_dle_vyse_predpokladane_hodnoty`

**Vyplněnost:** ~100%

**Ukázka:** `"Veřejná zakázka malého rozsahu"`, `"Nadlimitní veřejná zakázka"`, `"Podlimitní veřejná zakázka"`

**Proč je užitečné:**
- **Kategorizace podle velikosti** (malá vs. velká)
- **Regulatorní nároky** - nadlimitní = více formalit
- **Strategie** - zaměření jen na velké/malé zakázky

**Doporučení pro report:**
- MD: Přidat k "Základní informace": `- **Typ dle hodnoty**: Nadlimitní veřejná zakázka`
- CSV: Nový sloupec `Typ dle hodnoty`

---

## 📝 Souhrn doporučení

### Priorita A - VELMI DOPORUČUJI PŘIDAT:

1. ✅ **Kritéria hodnocení** (váha ceny vs. kvality)
2. ✅ **Financování EU** (Ano/Ne)
3. ✅ **Kategorie zadavatele** (stát/obec/škola/...)
4. ✅ **Sektor zadavatele** (vzdělávání/zdraví/...)
5. ✅ **Datum zahájení** postupu

### Priorita B - DOPORUČUJI (užitečné pro filtrování):

6. ✅ **Doba trvání smlouvy** (měsíce/roky)
7. ✅ **Elektronická platba** (Ano/Ne)
8. ✅ **Vhodné pro SME** (Ano/Ne)
9. ✅ **Typ dle hodnoty** (malá/podlimitní/nadlimitní)

### Priorita C - VOLITELNÉ (pro pokročilé):

10. 🔄 **Rámcová dohoda** - způsob a počet účastníků (jen 15%)
11. 💰 **Jistota/kauce** (jen 9% zakázek)
12. 📜 **Elektronické objednávky** (Ano/Ne)

---

## 🎯 Doporučená implementace

### Fáze 1 (Quick Win) - Priorita A:
```csv
# Přidat 5 nových sloupců
Financování EU;Kategorie zadavatele;Sektor zadavatele;Datum zahájení;Váha ceny (%)
Ano;Územní samosprávný celek;Vzdělávání;07.01.2026;60
```

### Fáze 2 (Extended) - Priorita B:
```csv
# Přidat další 4 sloupce
Doba trvání (měsíce);E-platba;Vhodné pro SME;Typ dle hodnoty
36;Ano;Ano;Nadlimitní VZ
```

### Fáze 3 (Advanced) - Priorita C:
```csv
# Přidat pokročilá pole
Je rámcová dohoda;RD - způsob;RD - účastníků;Jistota (Kč);E-objednávky
Ano;Bez obnovení;3;500000;Ano
```

---

## 📈 Příklad kompletního CSV řádku (s novými poli):

```csv
RVZ2600001410;Microsoft EA;Dodávky;Nadlimitní;9900000;...;⭐⭐⭐⭐⭐;Ano;Veřejnoprávní instituce;Bezpečnost;23.01.2026;60;48;Ano;Ano;Nadlimitní VZ;;;500000;Ano
```

**Legenda nových sloupců (18-28):**
- **18. Financování EU:** Ano
- **19. Kategorie zadavatele:** Veřejnoprávní instituce
- **20. Sektor zadavatele:** Bezpečnost
- **21. Datum zahájení:** 23.01.2026
- **22. Váha ceny (%):** 60
- **23. Doba trvání (měsíce):** 48
- **24. E-platba:** Ano
- **25. Vhodné pro SME:** Ano
- **26. Typ dle hodnoty:** Nadlimitní VZ
- **27. Je rámcová dohoda:** - (prázdné)
- **28. RD - účastníků:** - (prázdné)
- **29. Jistota (Kč):** 500000
- **30. E-objednávky:** Ano

**Celkem sloupců:** 23 (původně) + 12 (nových) = **35 sloupců**

---

## 🚀 Další kroky

1. **Rozhodnout**, které pole z Priorit A/B/C přidat
2. **Upravit** `scripts/generate_reports.py` - funkci `extract_tender_info()`
3. **Aktualizovat** CSV hlavičku a MD šablonu
4. **Otestovat** na VZ-2026-01-ICT.json
5. **Vygenerovat** nové reporty
6. **Aktualizovat** dokumentaci (REPORT_GENERATION.md)

---

## 💡 Poznámky k implementaci

**Vyplněnost polí:**
- Kritéria hodnocení: 100% ✅
- Kategorie zadavatele: 92% ✅
- Financování EU: 36% ⚠️ (ale velmi důležité)
- Rámcová dohoda: 15% ⚠️ (pokročilé uživatelé)
- Jistota: 9% ⚠️ (spíše informativní)

**Pole s nízkou vyplněností** (<10%) můžeš přidat, ale zobrazovat jen když existují (v MD jako volitelná sekce, v CSV jako prázdné).
