# ISVZ ICT Zakázky - Rychlý Start

Jednoduchý návod pro měsíční zpracování veřejných zakázek z ISVZ.

## 🎯 Co tento nástroj dělá?

Automaticky **stahuje, filtruje a analyzuje** veřejné zakázky z ISVZ (Informační systém o veřejných zakázkách):

1. **Filtruje otevřené zakázky** - pouze ty, o které se můžete ucházet
2. **Vybírá ICT zakázky** - programování, software, web, IT služby
3. **Hodnotí shodu** - známka 1-5 podle technologií (.NET, React, SharePoint...)
4. **Generuje reporty** - Markdown a CSV soubory pro analýzu
5. **Porovnává měsíce** - co je nového oproti minulému měsíci

## ⚡ Nejjednodušší způsob (NOVÉ!)

### Windows - Jeden soubor

**PowerShell (doporučeno):**
```powershell
.\run_monthly.ps1
```

**Batch (dvojklik):**
```
run_monthly.bat
```

**To je vše!** Skripty automaticky:
- ✅ Stáhnou aktuální měsíc
- ✅ Zpracují data (5 kroků)
- ✅ Porovnají s minulým měsícem
- ✅ Ukážou výsledky

### Pokročilé použití

```powershell
# Konkrétní měsíc
.\run_monthly.ps1 -Year 2026 -Month 2

# Přeskočit stahování (už máte data)
.\run_monthly.ps1 -SkipDownload

# Jen stáhnout VZ, ostatní přeskočit
.\run_monthly.ps1 -SkipVZ

# Batch verze
run_monthly.bat 2026 2         # Únor 2026
run_monthly.bat skip           # Bez stahování
```

## 📅 Manuální workflow (pokud chcete kontrolu nad každým krokem)

## 📅 Manuální workflow (pokud chcete kontrolu nad každým krokem)

### Krok 1: Stažení dat

```powershell
# Stáhnout velký VZ soubor (1.3 GB) - PowerShell
.\download_vz.ps1 -Year 2026 -Month 2

# Stáhnout ostatní kategorie (DNS, SON...) - Python
python monthly_process.py --year 2026 --month 2 --download
```

### Krok 2: Zpracování

```bash
# Zpracovat data (filtry + reporty)
python monthly_process.py --year 2026 --month 2
```

**Provede:**
- ✓ Krok 1: Filtrování otevřených zakázek (VZ)
- ✓ Krok 2: Filtrování ICT zakázek (VZ)
- ✓ Krok 3: Filtrování ICT z DNS
- ✓ Krok 4: Přidání doporučení (1-5)
- ✓ Krok 5: Generování MD a CSV reportů

### Krok 3: Porovnání s minulým měsícem

```bash
# Automaticky porovná s předchozím měsícem
python monthly_process.py --compare 2026 2

# Nebo explicitně zadáme oba měsíce
python monthly_process.py --compare 2026 1 2026 2
```

## 📊 Výstupy

Po zpracování najdete:

### CSV soubory (pro Excel)
```
output/csv/
├── VZ-ICT.csv         ← NEJNOVĚJŠÍ (aktualizuje se každý měsíc)
├── VZ-OPEN.csv        ← NEJNOVĚJŠÍ
├── DNS-ICT.csv        ← NEJNOVĚJŠÍ
└── 2026/02/           ← Archiv s datem
    ├── VZ-ICT_2026-02.csv
    ├── VZ-OPEN_2026-02.csv
    └── DNS-ICT_2026-02.csv
```

**CSV obsahuje 32 sloupců:**
- Základní info (ID, název, hodnota, lhůty...)
- **Doporučení** (1-5 ⭐)
- Kategorie a sektor zadavatele
- Financování EU, vhodnost pro SME
- URL odkazy (dokumentace, profil zadavatele...)

### Markdown reporty
```
output/reports/
├── VZ-ICT_2026-02.md     ← Tabulkový souhrn (nejnovější)
├── DIFF_VZ_02-2026.md    ← Rozdíly oproti minulému měsíci
└── 2026/02/
    └── VZ-ICT_2026-02.md ← Detailní report s popisy
```

### Vyfiltrované JSON
```
data/
├── VZ/
│   ├── VZ-2026-02.json         ← Originál (1.3 GB)
│   ├── VZ-2026-02-OPEN.json    ← ~970 otevřených (30 MB)
│   └── VZ-2026-02-ICT.json     ← ~145 ICT s doporučením (4 MB)
└── DNS/
    ├── DNS-2026-02.json        ← Originál (3 MB)
    └── DNS-2026-02-ICT.json    ← ~14 ICT (200 KB)
```

## 🎯 Jak pracovat s výsledky?

### 1. Otevřít CSV v Excelu
```
Klikněte na: output\csv\VZ-ICT.csv
```

**Filtry které využijete:**
- Seřadit podle **Doporučení** (1 = nejlepší)
- Filtr **Kraj** - pouze váš region
- Filtr **Vhodné pro SME** = Ano
- Filtr **Financování EU** = Ano (pokud chcete EU projekty)

### 2. Číst Markdown reporty
```
Otevřít: output\reports\VZ-ICT_2026-02.md
```

**Co najdete:**
- 📊 Statistiky (celková hodnota, průměr...)
- 📋 Tabulka všech zakázek
- Seřazeno podle doporučení (nejlepší nahoře)

### 3. Zkontrolovat rozdíly
```
Otevřít: output\reports\DIFF_VZ_02-2026.md
```

**Zjistíte:**
- 🆕 Nové zakázky (oproti minulému měsíci)
- ❌ Zrušené zakázky
- 📝 Změny ve stavu

## 💡 Tipy

**Doporučení (1-5):**
- ⭐⭐⭐⭐⭐ (1) = .NET, React, SharePoint, Power Platform
- ⭐⭐⭐⭐ (2) = Web, software, databáze
- ⭐ (5) = Obecná ICT bez specifických tech

**Nejdůležitější sloupce v CSV:**
- **Doporučení** - prioritizace
- **Lhůta podání nabídky** - deadline
- **Hodnota (Kč)** - velikost zakázky
- **Kraj** - regionální filtr
- **URL Dokumentace** - přímý odkaz

## 📖 Další dokumentace

- [MONTHLY_README.md](docs/MONTHLY_README.md) - Detailní workflow
- [REPORT_GENERATION.md](docs/REPORT_GENERATION.md) - Popis CSV struktury
- [DOPORUCOVACI_SYSTEM.md](docs/DOPORUCOVACI_SYSTEM.md) - Jak funguje hodnocení
- [EXCEL_INTEGRACE.md](docs/EXCEL_INTEGRACE.md) - Práce s CSV v Excelu
- [POROVNANI_MESICU.md](docs/POROVNANI_MESICU.md) - Rozdílové reporty

## ⚙️ Požadavky

- Python 3.8+
- PowerShell 5.1+ (pro stahování VZ)
- ~2 GB volného místa (pro data)

## 🆘 Pomoc

**Chyba při stahování VZ:**
- Zkuste stáhnout ručně z: https://isvz.nipez.cz/opendata/nova/2026/kategorie
- Uložit jako: `data\VZ\VZ-2026-02.json`

**Chyba při zpracování:**
- Zkontrolujte zda máte `VZ-2026-02.json` v `data\VZ\`
- Zkuste znovu: `python monthly_process.py --year 2026 --month 2`

**Více informací:**
- README.md - komplexní dokumentace
- docs/ - detailní návody
