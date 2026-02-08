# Měsíční zpracování ISVZ zakázek

Automatizované měsíční zpracování veřejných zakázek z ISVZ včetně generování rozdílových reportů.

## 🎯 Použití

### 1. Zpracování aktuálního měsíce

```bash
# Stáhnout data a zpracovat (přeskočí velký VZ soubor)
python monthly_process.py --download

# Jen zpracovat (pokud už máte data)
python monthly_process.py
```

### 2. Zpracování konkrétního měsíce

```bash
# Stáhnout data pro prosinec 2025
python monthly_process.py --year 2025 --month 12 --download

# Zpracovat prosinec 2025
python monthly_process.py --year 2025 --month 12
```

### 3. Ruční stažení velkého VZ souboru

Kvůli velikosti (0.8-1.3 GB) je lepší stahovat VZ soubor ručně pomocí PowerShell skriptu:

```powershell
# Stáhnout pro aktuální měsíc
.\download_vz.ps1

# Stáhnout pro konkrétní měsíc
.\download_vz.ps1 -Year 2025 -Month 12
```

### 4. Porovnání dvou měsíců

```bash
# Porovnat prosinec 2025 a leden 2026
python monthly_process.py --compare 2025 12 2026 1
```

Vytvoří rozdílové reporty:
- `reports/DIFF_VZ_12-2025_vs_01-2026.md` - porovnání VZ (veřejných zakázek)
- `reports/DIFF_DNS_12-2025_vs_01-2026.md` - porovnání DNS (dynamických nákupních systémů)

## 📁 Výstupní soubory

Pro každý měsíc se vytvoří:

```
data/
├── VZ/
│   ├── VZ-MM-YYYY.json           # Stažený originál (~0.8-1.3 GB)
│   ├── VZ-MM-YYYY-OPEN.json      # Otevřené zakázky (~20-30 MB)
│   └── VZ-MM-YYYY-ICT.json       # ICT zakázky z VZ (~1-5 MB)
└── DNS/
    ├── DNS-MM-YYYY.json          # DNS originál (~2-5 MB)
    └── DNS-MM-YYYY-ICT.json      # ICT DNS (~200-500 KB)

output/reports/
├── DIFF_VZ_MM1-YYYY1_vs_MM2-YYYY2.md    # Rozdílový report VZ
└── DIFF_DNS_MM1-YYYY1_vs_MM2-YYYY2.md   # Rozdílový report DNS
```

## 🔄 Workflow pro měsíční aktualizaci

**Každý měsíc kolem 5.-7. dne** (kdy ISVZ publikuje nová data):

### Krok 1: Stažení dat

```powershell
# Stáhnout velký VZ soubor
.\download_vz.ps1 -Year 2026 -Month 2

# Stáhnout ostatní soubory
python monthly_process.py --year 2026 --month 2 --download
```

### Krok 2: Zpracování

```bash
# Zpracovat nový měsíc (VZ + DNS + generování reportů)
python monthly_process.py --year 2026 --month 2
```

Toto zpracuje:
1. **Filtrování VZ**: data/VZ/VZ-2026-02.json → VZ-2026-02-OPEN.json → VZ-2026-02-ICT.json
2. **Filtrování DNS**: data/DNS/DNS-2026-02.json → DNS-2026-02-ICT.json
3. **Generování reportů**:
   - **Markdown**: output/reports/2026/02/*.md (VZ-OPEN, VZ-ICT, DNS-ICT)
   - **CSV**: output/csv/2026/02/*.csv (VZ-OPEN, VZ-ICT, DNS-ICT)

### Krok 3: Porovnání s minulým měsícem

**Jednoduchý způsob** (automatický výpočet předchozího měsíce):

```bash
# Porovná únor 2026 s lednem 2026 (auto-určení)
python monthly_process.py --compare 2026 2
```

**Explicitní způsob** (zadat oba měsíce):

```bash
# Vytvořit rozdílové reporty (VZ + DNS)
python monthly_process.py --compare 2026 1 2026 2
```

Výstupní soubory (kratší názvy - vztahují se k novějšímu měsíci):
- `output/reports/DIFF_VZ_02-2026.md`
- `output/reports/DIFF_DNS_02-2026.md`

**Pozor na přechod mezi roky**: Skript správně detekuje, že leden 2026 → předchozí = prosinec 2025:

```bash
python monthly_process.py --compare 2026 1
# Automaticky porovná: 12/2025 → 1/2026
```

### Krok 4: Prohlížení reportů

**Markdown reporty** (přehledné pro čtení):
```bash
# Otevřít v prohlížeči nebo editoru
output/reports/2026/02/VZ-ICT_2026-02.md
```

**CSV exporty** (pro Excel/analýzy):
```bash
# Import do Excel
output/csv/2026/02/VZ-ICT_2026-02.csv
```

Více informací: **[docs/REPORT_GENERATION.md](REPORT_GENERATION.md)**

### Krok 5: Zobrazit ICT zakázky v konzoli

```bash
# Zobrazit ICT zakázky
python show_ict_tenders.py
# (upravte cestu v souboru na VZ-2026-02-ICT.json)
```

## 📊 Rozdílové reporty

Reporty obsahují:

- **Souhrn**: Statistiky o počtu zakázek/DNS
- **Nové**: Položky které se objevily v novém měsíci
- **Zmizely**: Položky které zmizely (obvykle vypršení lhůty nebo ukončení)

Pro VZ i DNS se vytváří samostatné reporty.

### Příklad (VZ)

```markdown
# Rozdílový report ICT zakázek

**Období**: 12/2025 → 1/2026

## Souhrn

| Kategorie | Počet |
|-----------|-------|
| Zakázky v 12/2025 | 1 |
| Zakázky v 1/2026 | 152 |
| **Nové zakázky** | **152** |
| **Zmizely** | **1** |
| Společné | 0 |

## ✅ Nové zakázky (152)

### 1. RVZ2600001030
**Název**: UTB – MILAN – FLKŘ - Pick to Light technologie
- **Druh**: Dodávky
- **Hodnota**: 862,790 Kč
- **Lhůta**: 2026-02-09T09:00:00
...
```

## 🤖 Automatizace

### Windows Task Scheduler

Vytvořte naplánovanou úlohu pro automatické měsíční spouštění:

1. Otevřete Task Scheduler
2. Vytvořte novou úlohu "ISVZ Měsíční zpracování"
3. Trigger: Měsíčně, 7. den v měsíci, 8:00
4. Action: 
   - Program: `powershell.exe`
   - Arguments: `-File "C:\cesta\k\download_vz.ps1" -Year (Get-Date).Year -Month (Get-Date).Month`
5. Vytvořte druhou action:
   - Program: `python`
   - Arguments: `monthly_process.py`
   - Start in: `C:\cesta\k\ISVZ`

### Bash script (Linux/Mac)

```bash
#!/bin/bash
# monthly_isvz.sh

YEAR=$(date +%Y)
MONTH=$(date +%-m)

cd /cesta/k/ISVZ

# Stáhnout data (VZ ručně)
python monthly_process.py --year $YEAR --month $MONTH --download

# Zpracovat
python monthly_process.py --year $YEAR --month $MONTH

# Porovnat s minulým měsícem
PREV_MONTH=$((MONTH - 1))
PREV_YEAR=$YEAR
if [ $PREV_MONTH -eq 0 ]; then
    PREV_MONTH=12
    PREV_YEAR=$((YEAR - 1))
fi

python monthly_process.py --compare $PREV_YEAR $PREV_MONTH $YEAR $MONTH
```

Přidejte do crontab:

```bash
# Spustit každý měsíc 7. dne v 8:00
0 8 7 * * /cesta/k/monthly_isvz.sh
```

## 🔧 Řešení problémů

### VZ soubor se nestáhne

**Problém**: BITS transfer selže nebo timeout

**Řešení**:
1. Zkuste znovu s PowerShell skriptem
2. Nebo stáhněte ručně z prohlížeče
3. URL: `https://isvz.nipez.cz/sites/default/files/content/opendata-rvz/VZ-MM-YYYY.json`

### Memory Error při zpracování

**Problém**: Nedostatek paměti pro velký JSON

**Řešení**:
1. Zavřete jiné aplikace
2. Restartujte Python
3. Počítač by měl mít alespoň 8 GB RAM

### Žádné otevřené zakázky

**Problém**: Ve starších měsících může být 0 otevřených zakázek

**Důvod**: Data obsahují zakázky z daného měsíce, ale k aktuálnímu datu už jejich lhůty vypršely

**Řešení**: Normální stav, není chyba

## 📅 Kalendář publikace dat

ISVZ publikuje nová data **vždy kolem 5. dne následujícího měsíce**:

- Leden 2026: Publikováno ~5.2.2026
- Únor 2026: Publikováno ~5.3.2026
- Březen 2026: Publikováno ~5.4.2026
- ...

## 📖 Související soubory

- `filter_open_tenders.py` - Základní filtrování otevřených zakázek
- `filter_ict_tenders.py` - Filtrování ICT zakázek
- `show_ict_tenders.py` - Zobrazení výsledků
- `isvz_datamodel.md` - Dokumentace datového modelu

---

*Verze: 1.0*  
*Datum: 7. února 2026*
