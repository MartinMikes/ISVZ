# ISVZ Analýza ICT zakázek

Nástroje pro filtrování a analýzu dat z Informačního systému o veřejných zakázkách (ISVZ NIPEZ) se zaměřením na **otevřené ICT zakázky** vhodné pro programátory a vývojáře.

## Open Data ISZV (Informační systém o veřejných zakázkách)

Na webu [ISVZ](https://isvz.nipez.cz/opendata/nova/2026/kategorie) (pro rok 2026) jsou uvedeny tyto kategorie JSON souborů:

| **Zkratka** | **Kategorie** | **JSON soubor na portálu ISVZ** | **Přejmenovaný JSON po stažení** |
|---------|-----------|-------------|-------------|
| **VZ** | Veřejná zakázka | `VZ-01-2026.json` | `VZ-2026-01.json` |
| **DNS** | Dynamický nákupní systém | `DNS-01-2026.json` | `DNS-2026-01.json` |
| **SON** | Soutěž o návrh | `SON-01-2026.json` | `SON-2026-01.json` |
| **SK** | Systém kvalifikace | `SK-01-2026.json` | `SK-2026-01.json` |
| **RVP** | Řízení na výběr poddodavatele | `RVP-01-2026.json` | `RVP-2026-01.json` |

Názvy JSON souborů mají po stažení a změně jmennou konvenci [KATEGORIE]-[YYYY]-[MM].json, kde:

- **KATEGORIE** je 2-3 písmenná zkratka kategorie uvedená v tabulce výše
- **YYYY** je rok vypublikování JSON souboru
- **MM** je měsíc vypublikování JSON souboru

**Poznámka:** Toto pořadí (YYYY-MM) zajišťuje správné chronologické řazení souborů.

## 📁 Struktura projektu

```
ISVZ/
├── README.md                      # Hlavní dokumentace
├── monthly_process.py             # 🔄 Orchestrace měsíčního zpracování
├── download_vz.ps1                # 📥 PowerShell skript pro stahování
│
├── scripts/                       # 🔧 Aktivní skripty
│   ├── filter_open_tenders.py         # Filtrování otevřených VZ zakázek
│   ├── filter_ict_tenders.py          # Filtrování ICT z VZ
│   ├── filter_dns_ict.py              # Filtrování ICT z DNS
│   ├── show_ict_tenders.py            # Zobrazení přehledu ICT zakázek
│   ├── extract_codebooks.py           # Extrakce číselníků
│   └── explore_other_categories.py    # Průzkum kategorií
│
├── docs/                          # 📖 Dokumentace
│   ├── isvz_datamodel.md              # Datový model ISVZ
│   ├── isvz_stavy_filtrovani.md       # Analýza stavů
│   ├── isvz_ciselniky.md              # Kompletní číselníky
│   ├── CISELNIKY_PREHLED.md           # Rychlý přehled číselníků
│   ├── CATEGORY_ANALYSIS.md           # Analýza kategorií
│   ├── MONTHLY_README.md              # Měsíční automatizace
│   └── FILE_STRUCTURE.md              # Struktura projektu
│
├── data/                          # 💾 Datové soubory (ne v Git)
│   ├── nuts_kraje.json              # 🗺️ Číselník NUTS → Kraj
│   ├── VZ/                            # Veřejné zakázky
│   │   ├── VZ-2026-01.json                # Původní dataset (~1.3 GB)
│   │   ├── VZ-2026-01-OPEN.json           # Otevřené zakázky (28.6 MB)
│   │   └── VZ-2026-01-ICT.json            # ICT zakázky (4.0 MB)
│   ├── DNS/                           # Dynamické nákupní systémy
│   │   ├── DNS-2026-01.json               # DNS dataset (~4 MB)
│   │   └── DNS-2026-01-ICT.json           # ICT DNS (~500 KB)
│   ├── SON/                           # Soutěže o návrh
│   ├── SK/                            # Systémy kvalifikace
│   └── RVP/                           # Výběr poddodavatelů
│
├── output/                        # 📊 Generované výstupy
│   ├── ciselniky/
│   │   └── isvz_ciselniky.json        # JSON číselníky
│   ├── reports/
│   │   ├── DIFF_VZ_*.md               # Rozdílové reporty (porovnání měsíců)
│   │   ├── DIFF_DNS_*.md              # Rozdílové reporty DNS
│   │   ├── VZ-OPEN_YYYY-MM.md         # 📊 Tabulkový souhrn otevřených VZ
│   │   ├── VZ-ICT_YYYY-MM.md          # 📊 Tabulkový souhrn ICT VZ
│   │   ├── DNS-ICT_YYYY-MM.md         # 📊 Tabulkový souhrn ICT DNS
│   │   └── YYYY/MM/                   # Detailní měsíční reporty (MD)
│   │       ├── VZ-OPEN_YYYY-MM.md     # Detailní report otevřených VZ
│   │       ├── VZ-ICT_YYYY-MM.md      # Detailní report ICT VZ
│   │       └── DNS-ICT_YYYY-MM.md     # Detailní report ICT DNS
│   └── csv/
│       ├── VZ-OPEN.csv               # ⭐ Nejnovější CSV (přepisuje se)
│       ├── VZ-ICT.csv                # ⭐ Nejnovější CSV (přepisuje se)
│       ├── DNS-ICT.csv               # ⭐ Nejnovější CSV (přepisuje se)
│       └── YYYY/MM/                  # Měsíční CSV archiv
│           ├── VZ-OPEN_YYYY-MM.csv   # CSV otevřených VZ (archiv)
│           ├── VZ-ICT_YYYY-MM.csv    # CSV ICT VZ (archiv)
│           └── DNS-ICT_YYYY-MM.csv   # CSV ICT DNS (archiv)
│
└── archive/                       # 📦 Staré/debug skripty
    ├── analyze_*.py                   # Analytické skripty
    ├── debug_*.py                     # Debug skripty
    └── ict_zakazky_report.*           # Staré reporty
```

## 🚀 Rychlý start

### Jednorázové použití

### Krok 1: Stažení dat

Data se stahují z oficiálního portálu ISVZ NIPEZ:

- **URL**: <https://isvz.nipez.cz/sites/default/files/content/opendata-rvz/VZ-MM-YYYY.json>

```powershell
# Vytvoření adresářů
New-Item -ItemType Directory -Force -Path ".\data\VZ"
New-Item -ItemType Directory -Force -Path ".\data\DNS"

# Stažení velkého VZ souboru (doporučeno použít PowerShell skript)
.\download_vz.ps1 -Year 2026 -Month 1
```

### Krok 2: Filtrování otevřených zakázek

```bash
python scripts/filter_open_tenders.py
```

**Výstup:**

- Soubor: `data/VZ/VZ-2026-01-OPEN.json`
- Nalezeno: **970 otevřených zakázek** (1.36% z celku)

### Krok 3: Filtrování ICT zakázek

```bash
python scripts/filter_ict_tenders.py
```

**Výstup:**

- Soubor: `data/VZ/VZ-2026-01-ICT.json`
- Nalezeno: **145 ICT zakázek** (14.95% z otevřených, vyloučeny stavební práce)

### Krok 4: Přidání doporučení

```bash
python scripts/add_recommendations.py
```

**Přidá:**

- Hodnocení 1-5 podle technologické shody (1 = nejlepší)
- Keywords: .NET, React, Vue, SharePoint, Microsoft 365, Power Platform, Azure
- Statistika: 9× ⭐⭐⭐⭐⭐ (6.2%), 62× ⭐⭐⭐⭐ (42.8%)

### Krok 5: Zobrazení výsledků

```bash
python scripts/show_ict_tenders.py
```

**Zobrazí:**

- Metadata a statistiky
- Finanční přehled (celková hodnota: **2.7 mld Kč**)
- Seznam všech ICT zakázek s lhůtami, odkazy a doporučeními

---

## 🔄 Měsíční automatizace

Pro **pravidelné měsíční zpracování** nových dat viz **[docs/MONTHLY_README.md](docs/MONTHLY_README.md)**

### Rychlé použití

```bash
# Stáhnout a zpracovat nový měsíc (včetně generování reportů)
.\download_vz.ps1 -Year 2026 -Month 2
python monthly_process.py --year 2026 --month 2 --download

# Porovnat s minulým měsícem (automaticky určí předchozí)
python monthly_process.py --compare 2026 2

# Nebo explicitně zadat oba měsíce
python monthly_process.py --compare 2026 1 2026 2
```

Vytvoří:

**JSON soubory:**
- `data/VZ/VZ-2026-02-OPEN.json` - Otevřené VZ zakázky
- `data/VZ/VZ-2026-02-ICT.json` - ICT zakázky z VZ (s doporučeními 1-5)
- `data/DNS/DNS-2026-02-ICT.json` - ICT záznamy z DNS (s doporučeními 1-5)

**Markdown reporty:**
- `output/reports/2026/02/VZ-OPEN_2026-02.md` - Přehled otevřených VZ
- `output/reports/2026/02/VZ-ICT_2026-02.md` - Přehled ICT VZ (seřazeno podle doporučení)
- `output/reports/2026/02/DNS-ICT_2026-02.md` - Přehled ICT DNS (seřazeno podle doporučení)

**CSV exporty:**
- `output/csv/2026/02/VZ-OPEN_2026-02.csv` - CSV export otevřených VZ
- `output/csv/2026/02/VZ-ICT_2026-02.csv` - CSV export ICT VZ (32 sloupců včetně doporučení + nových polí)
- `output/csv/2026/02/DNS-ICT_2026-02.csv` - CSV export ICT DNS (32 sloupců včetně doporučení + nových polí)
- `output/csv/VZ-ICT.csv` - **Nejnovější CSV** bez datumu v názvu (pro snadnou integraci do Excel)
- `output/csv/DNS-ICT.csv` - **Nejnovější CSV** bez datumu v názvu

**Nová pole v CSV (od verze s doporučením):**
- Financování EU, Kategorie zadavatele, Sektor zadavatele, Datum zahájení
- Váha ceny (%), Doba trvání (měsíce), E-platba, Vhodné pro SME, Typ dle hodnoty

**Rozdílové reporty:**
- `output/reports/DIFF_VZ_02-2026.md` - Rozdílový report VZ (porovnání s 01-2026)
- `output/reports/DIFF_DNS_02-2026.md` - Rozdílový report DNS (porovnání s 01-2026)

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
