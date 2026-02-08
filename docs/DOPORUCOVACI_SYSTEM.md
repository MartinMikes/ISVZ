# Doporučovací systém pro ICT zakázky

## 📋 Přehled

Každá ICT zakázka je automaticky hodnocena systémem doporučení (známka 1-5) podle technologické shody s vaším profilem.

**Profil:** Vývoj webů, software, aplikací a systémů s .NET a React/Vue + konzultace/implementace Microsoft 365, SharePoint, Power Platform

## ⭐ Hodnocení (1-5)

| Známka | Význam | Popis |
|--------|--------|-------|
| **⭐⭐⭐⭐⭐ (1)** | **Top match** | Vysoká shoda s .NET/React/Microsoft technologiemi |
| **⭐⭐⭐⭐ (2)** | **Strong** | Web, software, aplikace, vývoj, integrace |
| **⭐⭐⭐ (3)** | **Medium** | IT služby, digitalizace, portály, ESS |
| **⭐⭐ (4)** | **Weak** | Hardware, infrastruktura, IT podpora |
| **⭐ (5)** | **Low** | Obecné ICT bez technických detailů |

## 🎯 Technologický profil

### Tier 1 - Top Match (známka 1)

**Podmínka:** Alespoň 1 keyword match

**.NET ekosystém:**
- `.net`, `dotnet`, `c#`, `csharp`, `asp.net`, `blazor`, `maui`

**Frontend frameworky:**
- `react`, `vue`, `angular`, `next.js`, `nuxt`

**Microsoft 365 a Power Platform:**
- `sharepoint`, `power platform`, `power apps`, `power automate`, `power bi`
- `microsoft 365`, `m365`, `office 365`, `o365`, `teams`, `onedrive`
- `dynamics 365`

**Azure služby:**
- `azure`, `azure devops`, `azure ad`, `entra id`, `azure functions`

**Microsoft technologie:**
- `microsoft`, `sql server`, `windows server`, `exchange`

### Tier 2 - Strong (známka 2)

**Podmínka:** Alespoň 1 keyword match (pokud není Tier 1)

**Web development:**
- `web`, `webová aplikace`, `webové služby`, `website`, `portál`, `portal`
- `e-shop`, `eshop`, `e-commerce`, `cms`

**Software development:**
- `software`, `aplikace`, `app`, `vývoj software`, `vývoj aplikací`
- `programování`, `development`, `programming`

**Systémy a integrace:**
- `informační systém`, `systém`, `integrace`, `api`, `rest api`
- `microservices`, `mikroslužby`

**Databáze:**
- `databáze`, `database`, `sql`, `mssql`, `postgresql`, `mysql`

**Cloud a DevOps:**
- `cloud`, `saas`, `paas`, `devops`, `ci/cd`, `git`

**Konzultace:**
- `konzultace`, `poradenství`, `consulting`, `implementace`

### Tier 3 - Medium (známka 3)

**IT služby:**
- `it služby`, `ict`, `digitalizace`, `digital transformation`

**Obecné IT:**
- `it řešení`, `it systém`, `it infrastruktura`
- `elektronizace`, `automatizace`

**Dokumentové systémy:**
- `elektronická spisová služba`, `ess`, `essl`
- `datové schránky`, `czech point`

**Mobilní:**
- `mobilní aplikace`, `mobile app`, `ios`, `android`

### Tier 4 - Weak (známka 4)

**Hardware a infrastruktura:**
- `hardware`, `server`, `síť`, `síťová infrastruktura`
- `networking`, `router`, `switch`

**IT podpora:**
- `it podpora`, `helpdesk`, `servicedesk`, `správa systémů`
- `monitoring`, `backup`, `disaster recovery`

**Bezpečnost:**
- `kyberbezpečnost`, `cybersecurity`, `firewall`, `antivir`
- `zabezpečení`, `security`

### Tier 5 - Low (známka 5)

**Podmínka:** Žádné specifické keywords z vyšších tierů

- Obecné ICT zakázky bez technických detailů
- Zakázky s minimálním popisem

## 🔍 Jak funguje hodnocení

### Analýza textů

Systém prohledává tyto části zakázky:
1. **Název zakázky** (`nazev_verejne_zakazky`)
2. **Popis předmětu** (`popis_predmetu`)
3. **Části zakázky** - názvy a popisy všech částí

### Rozhodovací logika

```python
if tier1_matches >= 1:
    return 1  # Top match
elif tier2_matches >= 3:
    return 2  # Hodně matches z tier 2
elif tier2_matches >= 1:
    return 2  # Alespoň jeden match z tier 2
elif tier3_matches >= 2:
    return 3  # Nějaké matches z tier 3
elif tier3_matches >= 1 or tier2_matches > 0:
    return 3
elif tier4_matches >= 1:
    return 4  # Hardware/infrastruktura
else:
    return 5  # Žádné specifické keywords
```

### Příklady hodnocení

#### ⭐⭐⭐⭐⭐ Známka 1 - Top match

**Zakázka:** "Servis a podpora ekonomického informačního systému Microsoft Dynamics 365 Business Central"

**Matched keywords:**
- `microsoft` (Tier 1)
- `dynamics 365` (Tier 1)
- `informační systém` (Tier 2)

**Důvod:** 2× match z Tier 1 → automaticky známka 1

---

**Zakázka:** "Microsoft Enterprise Agreement a MPSA - obnova licenční smlouvy"

**Matched keywords:**
- `microsoft` (Tier 1)

**Důvod:** 1× match z Tier 1 → známka 1

---

#### ⭐⭐⭐⭐ Známka 2 - Strong

**Zakázka:** "Vytvoření eHEALTH platformy pro komunikaci, výměnu a sdílení informací"

**Matched keywords:**
- `aplikace` (Tier 2)
- `systém` (Tier 2)
- `integrace` (Tier 2)

**Důvod:** 3× match z Tier 2 → známka 2

---

**Zakázka:** "Komplexní zajištění pěstebních prací s použitím vlastního materiálu"

**Matched keywords:**
- `software` (Tier 2) - v popisu zmíněn software pro plánování

**Důvod:** 1× match z Tier 2 → známka 2

---

#### ⭐⭐⭐ Známka 3 - Medium

**Zakázka:** "Elektronická spisová služba pro městský úřad"

**Matched keywords:**
- `elektronická spisová služba` (Tier 3)
- `ess` (Tier 3)

**Důvod:** 2× match z Tier 3 → známka 3

---

#### ⭐⭐ Známka 4 - Weak

**Zakázka:** "Dodávka síťových prvků a serverů"

**Matched keywords:**
- `síť` (Tier 4)
- `server` (Tier 4)

**Důvod:** 2× match z Tier 4 (hardware) → známka 4

---

#### ⭐ Známka 5 - Low

**Zakázka:** "ICT hardware"

**Matched keywords:** Žádné specifické

**Důvod:** Minimální popis, žádné matches → známka 5

## 📊 Statistiky (leden 2026)

### Distribuce doporučení

| Známka | Počet | Podíl | Hvězdičky |
|--------|-------|-------|-----------|
| 1 | 9 | 6.2% | ⭐⭐⭐⭐⭐ |
| 2 | 62 | 42.8% | ⭐⭐⭐⭐ |
| 3 | 3 | 2.1% | ⭐⭐⭐ |
| 4 | 10 | 6.9% | ⭐⭐ |
| 5 | 61 | 42.1% | ⭐ |
| **Celkem** | **145** | **100%** | |

### Klíčové metriky

- **Top matches (1-2):** 71 zakázek (49.0%)
- **Vhodné (1-3):** 74 zakázek (51.0%)
- **Méně vhodné (4-5):** 71 zakázek (49.0%)

### TOP 5 zakázek (leden 2026)

1. **⭐⭐⭐⭐⭐** Subskripce licencí Adobe AEM FORMS - 8.4 mil. Kč
2. **⭐⭐⭐⭐⭐** Ekonomicko-provozní řešení (Microsoft tech) - 26.8 mil. Kč
3. **⭐⭐⭐⭐⭐** Nákup vybavení Microsoft Teams Rooms - 6.7 mil. Kč
4. **⭐⭐⭐⭐⭐** Microsoft Enterprise Agreement a MPSA - 9.9 mil. Kč
5. **⭐⭐⭐⭐⭐** Servis Microsoft Dynamics 365 Business Central - 22.0 mil. Kč

## 📁 Použití v reportech

### Markdown reporty

**Individuální záznamy:**
```markdown
### 1. Název zakázky

**ID NIPEZ**: `RVZ2600036961`

**Doporučení**: ⭐⭐⭐⭐⭐ (1/5)

#### 📌 Základní informace
...
```

**Tabulkový přehled:**
```markdown
| # | Doporučení | ID NIPEZ | Název | ... |
|---|------------|----------|-------|-----|
| 1 | ⭐⭐⭐⭐⭐ (1) | RVZ... | ... | ... |
| 2 | ⭐⭐⭐⭐⭐ (1) | RVZ... | ... | ... |
```

### CSV exporty

**Sloupec:** `Doporučení` (pozice 18)

**Hodnoty:** 1, 2, 3, 4, 5

**Příklad:**
```csv
ID NIPEZ;Název;...;Doporučení;...
RVZ2600036961;Subskripce licencí Adobe AEM FORMS;...;1;...
RVZ2600000127;ČSSZ – Pořízení serverů;...;2;...
```

### Excel filtrování

**Filtrovat TOP matches:**
1. Otevřít `output/csv/VZ-ICT.csv`
2. Data → Filtr
3. Sloupec "Doporučení" → Vybrat 1, 2
4. → Zobrazí 71 nejlepších zakázek

**Podmíněné formátování:**
```excel
=IF(R2=1, "⭐⭐⭐⭐⭐",
 IF(R2=2, "⭐⭐⭐⭐",
  IF(R2=3, "⭐⭐⭐",
   IF(R2=4, "⭐⭐", "⭐"))))
```

## 🔧 Technická implementace

### Script

**Soubor:** `scripts/add_recommendations.py`

**Použití:**
```bash
# Samostatně
python scripts/add_recommendations.py data/VZ/VZ-2026-01-ICT.json data/VZ/VZ-2026-01-ICT.json

# V rámci měsíčního procesu (automaticky)
python monthly_process.py --year 2026 --month 1
```

### Workflow integrace

1. `filter_open_tenders.py` - Filtruje otevřené zakázky
2. `filter_ict_tenders.py` - Filtruje ICT (vyloučí stavební práce)
3. **`add_recommendations.py`** - Přidá doporučení 1-5
4. `generate_reports.py` - Vygeneruje reporty (seřazeno podle doporučení)

### Datová struktura

**V JSON souboru:**
```json
{
  "metadata": {
    "doporuceni_pridana": "2026-02-08T00:56:45.123456",
    "doporuceni_statistika": {
      "1": 9,
      "2": 62,
      "3": 3,
      "4": 10,
      "5": 61
    }
  },
  "data": [
    {
      "verejna_zakazka": { ... },
      "doporuceni": 1
    }
  ]
}
```

## 💡 Tipy pro použití

### Prioritizace zakázek

1. **Začněte s ⭐⭐⭐⭐⭐ (1)** - nejlepší shoda, nejvyšší šance
2. **Pokračujte ⭐⭐⭐⭐ (2)** - silná shoda, vhodné projekty
3. **Zvažte ⭐⭐⭐ (3)** - střední shoda, pokud máte kapacitu
4. **Vyhněte se ⭐⭐ (4) a ⭐ (5)** - nízká shoda

### Kombinace s dalšími kritérii

**Excel pivot tabulka:**
- Řádky: Doporučení
- Sloupce: Kraj
- Hodnoty: Počet zakázek, Suma hodnot

**Filtrování:**
```excel
Doporučení = 1 nebo 2
AND Kraj = "Hlavní město Praha"
AND Hodnota < 50 000 000
```

### Monitoring změn

**Měsíční porovnání:**
- Kolik nových TOP matches (1-2) přibyl
o
- Jaká je průměrná hodnota TOP zakázek
- Které kraje mají nejvíce vhodných zakázek

## 🔄 Aktualizace systému

### Úprava technologického profilu

**Soubor:** `scripts/add_recommendations.py`

**Přidání nového keywordu:**
```python
KEYWORDS_TIER_1 = {
    # ... existující
    'nová_technologie',  # Přidat zde
}
```

**Změna váhy:**
```python
if tier1_matches >= 2:  # Zvýšit požadavek
    return 1
```

### Re-hodnocení existujících dat

```bash
# Znovu spustit hodnocení
python scripts/add_recommendations.py data/VZ/VZ-2026-01-ICT.json data/VZ/VZ-2026-01-ICT.json

# Znovu vygenerovat reporty
python scripts/generate_reports.py --year 2026 --month 01
```

## 📚 Související dokumentace

- **[README.md](../README.md)** - Celkový přehled projektu
- **[REPORT_GENERATION.md](REPORT_GENERATION.md)** - Generování reportů
- **[EXCEL_INTEGRACE.md](EXCEL_INTEGRACE.md)** - Použití v Excelu
- **[MONTHLY_README.md](MONTHLY_README.md)** - Měsíční workflow
