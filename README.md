# ISVZ Analýza ICT zakázek

Automatizované nástroje pro filtrování a analýzu dat z **Informačního systému o veřejných zakázkách (ISVZ NIPEZ)** se zaměřením na **otevřené ICT zakázky** vhodné pro programátory a vývojáře.

## 🎯 Co tento nástroj dělá?

**Měsíčně stahuje a zpracovává** veřejné zakázky:

1. **Filtruje otevřené zakázky** (~970 z 71 000) - pouze ty, kde můžete podat nabídku
2. **Vybírá ICT zakázky** (~145 zakázek) - programování, web, software, IT služby  
3. **Hodnotí technologickou shodu** (1-5 ⭐) - .NET, React, SharePoint, Power Platform...
4. **Generuje přehledy** - Markdown reporty a CSV pro Excel
5. **Porovnává měsíce** - co je nového, co se změnilo

## ⚡ Rychlý start

**Nejjednodušší způsob (NOVÉ!):**

```powershell
# PowerShell - jeden příkaz pro všechno
.\run_monthly.ps1

# Nebo Batch (dvojklik)
run_monthly.bat
```

Hotovo! Skripty automaticky stáhnou, zpracují a porovnají data.

---

**Manuální způsob (3 příkazy):**

```powershell
# 1. Stáhnout data
.\download_vz.ps1 -Year 2026 -Month 2
python monthly_process.py --year 2026 --month 2 --download

# 2. Zpracovat (5 kroků: filtr OPEN → ICT → doporučení → reporty)
python monthly_process.py --year 2026 --month 2

# 3. Porovnat s minulým měsícem
python monthly_process.py --compare 2026 2
```

**Výstupy:**
- 📊 `output/csv/VZ-ICT.csv` - otevřít v Excelu, filtrovat, analyzovat
- 📝 `output/reports/VZ-ICT_2026-02.md` - přehled všech zakázek
- 🔍 `output/reports/DIFF_VZ_02-2026.md` - co je nového

## 📊 Příklad statistik (leden 2026)

| Kategorie | Počet | Hodnota |
|-----------|-------|---------|
| **Celkem zakázek v ISVZ** | 71 377 | - |
| **Otevřené zakázky** | 970 (1.4%) | 91.7 mld Kč |
| **ICT zakázky** | 145 (15% z otevřených) | 2.75 mld Kč |
| **⭐⭐⭐⭐⭐ Top shoda** | 9 (6.2%) | 66 mil Kč |
| **⭐⭐⭐⭐ Silná shoda** | 62 (42.8%) | 1.41 mld Kč |

**Průměrná hodnota ICT zakázky:** 19 mil Kč

## 📁 Struktura projektu

```
ISVZ/
├── 📄 README.md                    # Tento soubor
├── 📄 QUICKSTART.md                # ⭐ Začni tady! (rychlý start)
├── 🔄 monthly_process.py           # Hlavní orchestrace
├── 📥 download_vz.ps1              # Stahování VZ (PowerShell)
├── ⚡ run_monthly.ps1               # ⭐ NOVÉ! Kompletní workflow (PowerShell)
├── ⚡ run_monthly.bat               # ⭐ NOVÉ! Kompletní workflow (Batch)
│
├── 📁 scripts/                     # 🔧 Zpracovací skripty (5 kroků)
│   ├── filter_open_tenders.py          # Krok 1: Otevřené VZ
│   ├── filter_ict_tenders.py           # Krok 2: ICT z VZ
│   ├── filter_dns_ict.py               # Krok 3: ICT z DNS
│   ├── add_recommendations.py          # Krok 4: Doporučení 1-5
│   └── generate_reports.py             # Krok 5: MD + CSV reporty
│
├── 📁 docs/                        # 📖 Dokumentace
│   ├── MONTHLY_README.md               # Měsíční workflow
│   ├── REPORT_GENERATION.md            # CSV struktura (32 sloupců)
│   ├── DOPORUCOVACI_SYSTEM.md          # Systém hodnocení
│   ├── POROVNANI_MESICU.md             # Diff reporty
│   ├── EXCEL_INTEGRACE.md              # Excel návod
│   └── ...                             # Další dokumenty
│
├── 📁 data/                        # 💾 Data (ne v Git)
│   ├── VZ/VZ-2026-01.json              # Originál (1.3 GB)
│   ├── VZ/VZ-2026-01-OPEN.json         # Otevřené (30 MB)
│   ├── VZ/VZ-2026-01-ICT.json          # ICT s doporučením (4 MB)
│   └── DNS/...                         # DNS kategorie
│
├── 📁 output/                      # 📊 Výstupy
│   ├── csv/
│   │   ├── VZ-ICT.csv                  # ⭐ Nejnovější (Excel ready)
│   │   └── 2026/01/...                 # Archiv
│   └── reports/
│       ├── VZ-ICT_2026-01.md           # ⭐ Souhrn
│       ├── DIFF_VZ_01-2026.md          # ⭐ Co je nového
│       └── 2026/01/...                 # Detailní reporty
│
└── 📁 archive/                     # 📦 Historické soubory
```

**Podrobnosti:** [FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md)

## 📖 Dokumentace

### 🆕 Pro nové uživatele
- **[QUICKSTART.md](QUICKSTART.md)** - ⭐ Začni tady! Kompletní návod krok za krokem

### 📅 Pravidelné používání
- **[MONTHLY_README.md](docs/MONTHLY_README.md)** - Měsíční workflow a automatizace

### 📊 Práce s daty
- **[REPORT_GENERATION.md](docs/REPORT_GENERATION.md)** - Struktura CSV (32 sloupců) a MD reportů
- **[EXCEL_INTEGRACE.md](docs/EXCEL_INTEGRACE.md)** - Import CSV do Excelu, filtry, grafy
- **[DOPORUCOVACI_SYSTEM.md](docs/DOPORUCOVACI_SYSTEM.md)** - Jak funguje hodnocení 1-5 ⭐
- **[POROVNANI_MESICU.md](docs/POROVNANI_MESICU.md)** - Rozdílové reporty mezi měsíci

### 📚 Referenční
- **[CISELNIKY_PREHLED.md](docs/CISELNIKY_PREHLED.md)** - Přehled číselníků (CPV, Druh, Stav...)
- **[NUTS_KRAJE.md](docs/NUTS_KRAJE.md)** - Převodní tabulka NUTS → Kraj
- **[FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md)** - Detailní struktura projektu

## 🔄 Měsíční workflow

### 1. Stažení dat (PowerShell + Python)

```powershell
# Stáhnout velký VZ soubor (1.3 GB)
.\download_vz.ps1 -Year 2026 -Month 2

# Stáhnout ostatní kategorie
python monthly_process.py --year 2026 --month 2 --download
```

### 2. Zpracování (5 automatických kroků)

```bash
python monthly_process.py --year 2026 --month 2
```

**Kroky:**
1. ✓ Filtrování otevřených VZ (970 zakázek)
2. ✓ Filtrování ICT z VZ (145 zakázek)
3. ✓ Filtrování ICT z DNS (14 zakázek)
4. ✓ Přidání doporučení 1-5 ⭐
5. ✓ Generování MD + CSV reportů

### 3. Porovnání s minulým měsícem

```bash
# Automaticky určí předchozí měsíc
python monthly_process.py --compare 2026 2

# Nebo explicitně
python monthly_process.py --compare 2026 1 2026 2
```

## 📊 Výstupy

### CSV soubory (pro Excel analýzu)

```
output/csv/
├── VZ-ICT.csv         ← ⭐ HLAVNÍ SOUBOR (32 sloupců, aktualizuje se měsíčně)
├── VZ-OPEN.csv        ← Všechny otevřené zakázky
├── DNS-ICT.csv        ← ICT z dynamických systémů
└── 2026/02/           ← Archiv s datem
    ├── VZ-ICT_2026-02.csv
    ├── VZ-OPEN_2026-02.csv
    └── DNS-ICT_2026-02.csv
```

**32 sloupců CSV obsahuje:**
- Základní info (ID, název, hodnota, lhůty, zadavatel...)
- **Doporučení** 1-5 ⭐ (technologická shoda)
- Kategorie a sektor zadavatele
- Financování EU, vhodnost pro SME
- Váha ceny v hodnocení
- URL odkazy (dokumentace, profil...)

### Markdown reporty

```
output/reports/
├── VZ-ICT_2026-02.md     ← ⭐ Tabulkový souhrn (nejnovější)
├── DIFF_VZ_02-2026.md    ← ⭐ Co je nového
└── 2026/02/
    └── VZ-ICT_2026-02.md ← Detailní report s plnými popisy
```

### Vyfiltrované JSON

```
data/VZ/
├── VZ-2026-02.json         ← Originál (1.3 GB)
├── VZ-2026-02-OPEN.json    ← ~970 otevřených (30 MB)
└── VZ-2026-02-ICT.json     ← ~145 ICT s doporučením (4 MB)
```

## 💡 Tipy pro analýzu

### V Excelu (VZ-ICT.csv)

1. **Seřadit podle doporučení** - nejlepší shody (⭐⭐⭐⭐⭐) nahoře
2. **Filtrovat podle kraje** - pouze váš region
3. **Filtr "Vhodné pro SME" = Ano** - zakázky pro malé firmy
4. **Filtr "Financování EU" = Ano** - EU projekty

### Prioritizace

**⭐⭐⭐⭐⭐ (1) - Top shoda:**
- .NET, C#, React, Vue, Angular
- SharePoint, Power Platform, M365
- Azure, cloud services

**⭐⭐⭐⭐ (2) - Silná shoda:**
- Web development, software, aplikace
- Databáze, integrace, API

**⭐⭐⭐ (3) - Dobrá shoda:**
- IT services, digitalizace
- Portály, ESS systémy

## 🔧 Technické detaily

### Požadavky

- Python 3.8+
- PowerShell 5.1+ (pro stahování VZ)
- ~2 GB volného místa

### Instalace

```bash
git clone https://github.com/MartinMikes/ISVZ.git
cd ISVZ
```

Žádné Python balíčky nejsou potřeba - používá pouze standardní knihovnu.

### Datové zdroje

**ISVZ NIPEZ Open Data:**
- URL: https://isvz.nipez.cz/opendata/nova/{YEAR}/kategorie
- Formát: JSON
- Aktualizace: měsíčně (cca 5.-7. den v měsíci)
- Velikost VZ: ~1.3 GB

## 🆘 Řešení problémů

**Chyba při stahování VZ:**
```
⚠️ Soubor VZ-2026-02.json neexistuje!
```
→ Stáhnout ručně z https://isvz.nipez.cz/opendata/nova/2026/kategorie  
→ Uložit jako `data\VZ\VZ-2026-02.json`

**Chyba při zpracování:**
```
❌ Chyba při filtrování otevřených zakázek
```
→ Zkontrolovat zda máte správný soubor v `data\VZ\`  
→ Zkusit znovu spustit `python monthly_process.py --year 2026 --month 2`

## 📜 Licence

MIT License - viz [LICENSE](LICENSE)

## 🤝 Přispívání

Pull requesty vítány! Pro větší změny prosím nejdříve otevřete issue.

## 📞 Kontakt

Martin Mikeš - projekt vznikl pro osobní potřebu filtrování ICT zakázek

---

**Důležité odkazy:**
- 📖 [QUICKSTART.md](QUICKSTART.md) - Rychlý start
- 📅 [MONTHLY_README.md](docs/MONTHLY_README.md) - Měsíční workflow
- 📊 [REPORT_GENERATION.md](docs/REPORT_GENERATION.md) - CSV struktura
- ⭐ [DOPORUCOVACI_SYSTEM.md](docs/DOPORUCOVACI_SYSTEM.md) - Hodnocení
- 📑 [EXCEL_INTEGRACE.md](docs/EXCEL_INTEGRACE.md) - Excel návod

## 📊 Výsledky (leden 2026)

### Veřejné zakázky (VZ)

| Kategorie | Počet | Podíl |
|-----------|-------|-------|
| **Celkem zakázek** | 71 377 | 100% |
| **Otevřené zakázky** | 970 | 1.36% |
| **ICT zakázky** | 152 | 15.67% z otevřených |

### Dynamické nákupní systémy (DNS)

| Kategorie | Počet | Podíl |
|-----------|-------|-------|
| **Celkem DNS** | 223 | 100% |
| **ICT DNS** | 14 | 6.28% |

### ICT zakázky podle druhu

| Druh | Počet | Podíl |
|------|-------|-------|
| Dodávky | 79 | 54.5% |
| Služby | 66 | 45.5% |

### Finanční statistiky ICT zakázek

- **Celková hodnota**: 2.75 mld Kč
- **Průměrná hodnota**: 24.7 mil. Kč
- **Zakázek s hodnotou**: 111 / 145

### Top CPV kategorie

| CPV | Kategorie | Počet |
|-----|-----------|-------|
| 72** | IT služby | 48 |
| 48** | Software a IS | 38 |
| 30** | PC zařízení | 6 |

## 🔍 Kritéria filtrování

### Otevřené zakázky (filter_open_tenders.py)

1. ✅ `datum_ukonceni_zadavaciho_postupu` = `null`
2. ✅ `vysledek.vysledek_ukonceni_zadavaciho_postupu` = `null`
3. ✅ Má aktivní lhůtu pro podání nabídky v budoucnosti
4. ✅ Stav není "Dokončen/Zadán", "Ukončeno plnění smlouvy" nebo "Zrušen"

### ICT zakázky (filter_ict_tenders.py)

**Vyloučení:**

- ❌ Stavební práce (i když obsahují ICT keywords)

**Klíčová slova:**

- Software, aplikace, programování, vývoj, IT, ICT
- Web, portál, e-shop, mobilní aplikace
- Databáze, cloud, API, server
- Informační systém, digitalizace
- Kyberbezpečnost, firewall
- Microsoft, Office 365, Azure, AWS
- Elektronická spisová služba

**CPV kódy:**

- `48******` - Softwarové balíky a IS
- `72******` - IT služby
- `30200000` - Počítačová zařízení

## ⭐ Doporučovací systém

Každá ICT zakázka je automaticky hodnocena podle technologické shody s profilem.

### Hodnocení (1-5)

- **⭐⭐⭐⭐⭐ (1)** - Top match: .NET, C#, React, Vue, SharePoint, Power Platform, Microsoft 365, Azure
- **⭐⭐⭐⭐ (2)** - Strong: Web, software, aplikace, vývoj, integrace, databáze
- **⭐⭐⭐ (3)** - Medium: IT služby, digitalizace, portál, ESS
- **⭐⭐ (4)** - Weak: Hardware, síť, IT podpora, bezpečnost
- **⭐ (5)** - Low: Obecné ICT bez tech. detailů

### Technologický profil

**Tier 1 keywords (nejvyšší shoda):**
- .NET, C#, ASP.NET, Blazor
- React, Vue, Angular, Next.js
- SharePoint, Power Platform, Power Apps, Power Automate, Power BI
- Microsoft 365, Teams, Azure, Dynamics 365

**Statistika pro leden 2026:**
- 9 zakázek s hodnocením 1 (6.2%)
- 62 zakázek s hodnocením 2 (42.8%)
- 74 zakázek celkem s hodnocením 1-3 (51.0%)

**Použití:**
- Všechny reporty (MD i CSV) seřazeny podle doporučení (nejlepší nahoře)
- V CSV sloupec "Doporučení" - snadné filtrování v Excelu
- V MD tabulce vizuální hvězdičky pro rychlý přehled

## 🗺️ Regionální filtrování

Všechny generované reporty (MD i CSV) obsahují informace o **kraji** pro snadné regionální filtrování.

### Automatické mapování NUTS → Kraj

- Používá číselník `data/nuts_kraje.json`
- Mapuje NUTS 3 kódy (např. `CZ010`, `CZ064`) na názvy krajů
- 14 krajů ČR (včetně Hlavního města Prahy)

**Příklad v CSV:**
```csv
NUTS;Kraj
CZ010;Hlavní město Praha
CZ064;Jihomoravský kraj
CZ072;Zlínský kraj
```

**Použití v Excelu:**

Pro **nejnovější data** (doporučeno):
1. Excel → Data → Z textu/CSV
2. Vybrat `output/csv/VZ-ICT.csv` (bez data v názvu)
3. Soubor se automaticky aktualizuje při každém měsíčním běhu
4. Excel může mít připojené dotazy/pivoty

Pro **archivní data** (historické srovnání):
1. Otevřít `output/csv/YYYY/MM/VZ-ICT_YYYY-MM.csv`
2. Použít automatický filtr (Data → Filtr)
3. Filtrovat sloupec "Kraj" podle regionu

**V Markdown reportech:**
- Tabulkový souhrn má sloupec "Kraj"
- Detailní reporty obsahují sekci "📍 Místo plnění" s krajem

## 📊 Číselníky

Pro detailní přehled všech číselníků a jejich hodnot viz:

- **[docs/CISELNIKY_PREHLED.md](docs/CISELNIKY_PREHLED.md)** - Rychlý přehled klíčových číselníků
- **[docs/isvz_ciselniky.md](docs/isvz_ciselniky.md)** - Kompletní dokumentace 272 číselníků

### Klíčové číselníky

- **Druh zakázky**: Dodávky (46%), Služby (33%), Stavební práce (21%)
- **Stav**: Aktivní/Neukončen (407 zakázek = 0.48%)
- **Druh zadávacího postupu**: 15 různých typů
- **Elektronický nástroj**: TA (83%), NEN (12%), VVZ (5%)

Extrakce číselníků: `python scripts/extract_codebooks.py`

## 📈 Porovnávání měsíců

Podrobný návod na porovnávání ICT zakázek mezi měsíci:

- **[docs/POROVNANI_MESICU.md](docs/POROVNANI_MESICU.md)** - Kompletní dokumentace porovnávání

**Rychlé použití:**

```bash
# Automatické porovnání s předchozím měsícem
python monthly_process.py --compare 2026 1

# Výstup: DIFF_VZ_01-2026.md, DIFF_DNS_01-2026.md
```

Systém automaticky určí předchozí měsíc (včetně přechodu mezi roky).

## 🛠️ Rozšíření

### Přidat další klíčová slova

V `scripts/filter_ict_tenders.py` upravte set `ICT_KEYWORDS`:

```python
ICT_KEYWORDS = {
    'software', 'aplikace', 'it',
    'vaše_nové_klíčové_slovo',
    # ...
}
```

### Změnit CPV kódy

V `scripts/filter_ict_tenders.py` upravte dictionary `ICT_CPV_CODES`:

```python
ICT_CPV_CODES = {
    '48': 'Software',
    '72': 'IT služby',
    'nový_cpv_kód': 'Popis',
}
```

### Filtrovat podle hodnoty

Upravte funkci `is_ict_tender()` v `scripts/filter_ict_tenders.py`:

```python
hodnota = vz.get('predpokladana_hodnota_bez_DPH_v_CZK')
if hodnota and hodnota < 1000000:  # Jen pod 1 mil. Kč
    return False
```

## 📦 Git a verzování

Projekt používá `.gitignore` pro optimalizaci velikosti repozitáře:

### ✅ Co je trackováno v Gitu

- Veškerý zdrojový kód (scripts/, *.py,*.ps1)
- Kompletní dokumentace (docs/, README.md)
- **Filtrované výstupy**: *-ICT.json,*-OPEN.json (~4-30 MB)
- Konfigurační soubory

### ❌ Co je ignorováno

- **Velké originální soubory**: VZ-*.json (~1.3 GB), DNS-*.json
- Kategorie bez ICT: SON/, SK/, RVP/
- Generované reporty: output/reports/
- Python cache: **pycache**/

**Úspora**: ~2.2 GB na repozitář (originální soubory se stahují ručně)

## 🔍 Příklady ICT zakázek

1. **ČSSZ – Pořízení serverů pro centrální provoz aplikací OSVČ**
   - Hodnota: 45.5 mil. Kč
   - Lhůta: 11.02.2026
   - CPV: 48822000

2. **Ekonomicko-provozní řešení - MS Dynamics 365**
   - Hodnota: 26.8 mil. Kč
   - Lhůta: 10.02.2026
   - CPV: 72263000

3. **Subskripce licencí Adobe AEM FORMS**
   - Hodnota: 8.4 mil. Kč
   - Lhůta: 27.02.2026
   - CPV: 72253200

## 📖 Dokumentace

- **isvz_datamodel.md** - Kompletní dokumentace datového modelu s příklady filtrovacího kódu
- **isvz_stavy_filtrovani.md** - Analýza stavů a kritérií pro filtrování otevřených zakázek

## 📝 Poznámky

### Aktualizace dat

- Data ISVZ se aktualizují **vždy k 5. dni měsíce**
- Pro nový měsíc stáhněte nový JSON soubor (např. `VZ-2026-02.json`)
- Upravte cesty v skriptech

### Limitace

1. **Velikost souboru**: Hlavní VZ soubor je ~1.3 GB, načítání může trvat
2. **False positives**: Některé ne-ICT zakázky mohou obsahovat ICT klíčová slova
3. **Chybějící data**: Ne všechny zakázky mají vyplněnou hodnotu nebo všechny údaje

## 🔍 Řešení problémů

### Chyba načítání

```
FileNotFoundError: No such file or directory
```

**Řešení**: Ujistěte se, že soubory jsou v `isvz_data/` adresáři.

### Memory Error

```
MemoryError
```

**Řešení**: Zavřete jiné aplikace nebo restartujte Python.

### Žádné ICT zakázky

```
Nalezeno 0 ICT zakázek
```

**Řešení**:

1. Zkontrolujte, že máte soubor `VZ-2026-01-OPEN.json`
2. Zkuste upravit klíčová slova v `filter_ict_tenders.py`

## 📚 Další zdroje

- **ISVZ NIPEZ**: <https://isvz.nipez.cz/>
- **Open Data**: <https://isvz.nipez.cz/centrum-podpory/napoveda/webovy-portal-isvz/opendata/>
- **Registr veřejných zakázek**: <https://portal-vz.cz/>

## 📄 Licence

Tento projekt je určen pro osobní a výzkumné účely. Data pocházejí z veřejných zdrojů ISVZ NIPEZ.

---

**Vytvořeno**: 7. února 2026  
**Dataset**: ISVZ leden 2026  
**Verze**: 2.0

## 📚 Další zdroje

- **ISVZ NIPEZ**: <https://isvz.nipez.cz/>
- **Open Data dokumentace**: <https://isvz.nipez.cz/centrum-podpory/napoveda/webovy-portal-isvz/opendata/open-data-dokumentace-json-formatu>
- **Registr veřejných zakázek**: <https://portal-vz.cz/nipez/registr-verejnych-zakazek/>

## 📄 Licence

Tento projekt je určen pro osobní a výzkumné účely. Data pocházejí z veřejných zdrojů ISVZ NIPEZ.

---

**Vytvořeno**: 2026-02-07  
**Poslední aktualizace**: 2026-02-07
