# Řídící skripty pro měsíční workflow

Dokumentace automatizovaných skriptů pro kompletní měsíční zpracování.

## 📋 Přehled

K dispozici jsou **2 řídící skripty**, které provádějí celý měsíční proces jedním příkazem:

1. **run_monthly.ps1** (PowerShell) - doporučeno
2. **run_monthly.bat** (Batch) - jednoduché dvojklik

## 🎯 Co skripty dělají?

Automaticky provedou **všechny 3 fáze** měsíčního procesu:

### Fáze 1: Stahování dat
- Velký VZ soubor (~1.3 GB) přes `download_vz.ps1`
- Ostatní kategorie (DNS, SON, SK, RVP) přes `monthly_process.py --download`

### Fáze 2: Zpracování (5 automatických kroků)
1. ✓ Filtrování otevřených VZ zakázek
2. ✓ Filtrování ICT zakázek z VZ
3. ✓ Filtrování ICT zakázek z DNS
4. ✓ Přidání doporučení (1-5 ⭐)
5. ✓ Generování MD + CSV reportů

### Fáze 3: Porovnání
- Automatické porovnání s předchozím měsícem
- Generování rozdílových reportů (DIFF_*)

## 🚀 Použití

### PowerShell script (run_monthly.ps1)

**Nejjednodušší:**
```powershell
.\run_monthly.ps1
```
Zpracuje aktuální měsíc (leden 2026 pokud spustíte v lednu 2026).

**Konkrétní měsíc:**
```powershell
.\run_monthly.ps1 -Year 2026 -Month 2
```

**Parametry:**

| Parametr | Popis | Příklad |
|----------|-------|---------|
| `-Year` | Rok (výchozí: aktuální) | `-Year 2026` |
| `-Month` | Měsíc 1-12 (výchozí: aktuální) | `-Month 2` |
| `-SkipDownload` | Přeskočit stahování (už máte data) | `-SkipDownload` |
| `-SkipVZ` | Jen stáhnout ostatní, VZ přeskočit | `-SkipVZ` |
| `-SkipComparison` | Neprovádět porovnání měsíců | `-SkipComparison` |

**Příklady:**
```powershell
# Zpracovat únor 2026 (vše)
.\run_monthly.ps1 -Year 2026 -Month 2

# Jen zpracovat data (bez stahování)
.\run_monthly.ps1 -SkipDownload

# Stáhnout jen malé soubory, VZ už mám
.\run_monthly.ps1 -SkipVZ

# Zpracovat bez porovnání
.\run_monthly.ps1 -SkipComparison
```

### Batch script (run_monthly.bat)

**Nejjednodušší:**
- Dvojklik na `run_monthly.bat`
- Nebo v CMD: `run_monthly.bat`

**Konkrétní měsíc:**
```batch
run_monthly.bat 2026 2
```

**Bez stahování:**
```batch
run_monthly.bat skip
```

**Parametry:**
- `run_monthly.bat` - aktuální měsíc
- `run_monthly.bat YYYY MM` - konkrétní měsíc
- `run_monthly.bat skip` - přeskočit stahování

## 📊 Výstupy skriptů

Po dokončení skripty zobrazí:

### Statistiky
```
📊 STATISTIKY:
   ICT zakázky (VZ):  145
   ICT zakázky (DNS): 14
```

### Cesty k hlavním výstupům
```
📁 HLAVNÍ VÝSTUPY:

   CSV (Excel ready):
   ⭐ output\csv\VZ-ICT.csv
      output\csv\VZ-OPEN.csv
      output\csv\DNS-ICT.csv

   Markdown reporty:
   ⭐ output\reports\VZ-ICT_2026-01.md
      output\reports\DIFF_VZ_01-2026.md

   Vyfiltrované JSON:
      data\VZ\VZ-2026-01-ICT.json
      data\DNS\DNS-2026-01-ICT.json
```

### Nabídka otevření složky
```
Otevřít složku s výstupy? (A/n):
```
- Stisknout Enter nebo 'A' → otevře `output\csv\`
- Napsat 'n' → ukončí bez otevření

## 🎨 Funkce skriptů

### PowerShell (run_monthly.ps1)

**Výhody:**
- ✅ Barevný výstup (lépe čitelné)
- ✅ Kontrola Python instalace
- ✅ Detailní statistiky z JSON souborů
- ✅ Měření času běhu
- ✅ Pokročilé parametry

**Ukázkový výstup:**
```
╔════════════════════════════════════════════════════════════════════╗
║  ISVZ - MĚSÍČNÍ ZPRACOVÁNÍ VEŘEJNÝCH ZAKÁZEK                      ║
║  Automatický workflow pro 2/2026                                   ║
╚════════════════════════════════════════════════════════════════════╝

ℹ️  Kontroluji Python...
✅ Python nalezen: Python 3.11.0

========================================================================
  📥 KROK 1/3: STAHOVÁNÍ DAT
========================================================================

✅ VZ soubor stážen
✅ Ostatní soubory staženy

========================================================================
  ⚙️  KROK 2/3: ZPRACOVÁNÍ DAT
========================================================================
...
```

### Batch (run_monthly.bat)

**Výhody:**
- ✅ Jednoduché spuštění dvojklikem
- ✅ Funguje bez PowerShell
- ✅ Kompatibilní se starými Windows
- ✅ Barevný výstup (Windows 10+)

**Ideální pro:**
- Uživatele, kteří preferují GUI
- Automatizaci přes Task Scheduler
- Starší systémy

## ⚙️ Technické detaily

### Co skripty volají

```
run_monthly.ps1 / run_monthly.bat
    │
    ├─► download_vz.ps1 -Year YYYY -Month MM
    │   └─► Stahuje VZ-YYYY-MM.json (1.3 GB)
    │
    ├─► python monthly_process.py --download
    │   └─► Stahuje DNS, SON, SK, RVP
    │
    ├─► python monthly_process.py --year YYYY --month MM
    │   └─► 5 kroků zpracování
    │
    └─► python monthly_process.py --compare YYYY MM
        └─► Rozdílové reporty
```

### Kontrola chyb

**PowerShell:**
- Kontroluje `$LASTEXITCODE` každého příkazu
- Pokud selže zpracování → ukončí script s chybou
- Pokud selže stahování/porovnání → varování a pokračuje

**Batch:**
- Kontroluje `errorlevel` každého příkazu
- Pokud selže zpracování → pauza a exit
- Pokud selže stahování/porovnání → varování a pokračuje

## 🔧 Řešení problémů

### PowerShell script nelze spustit

**Chyba:**
```
run_monthly.ps1 cannot be loaded because running scripts is disabled
```

**Řešení:**
```powershell
# Dočasně povolit
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# Nebo přímo spustit
powershell -ExecutionPolicy Bypass -File run_monthly.ps1
```

### Python není nalezen

**Chyba:**
```
❌ Python není nainstalován nebo není v PATH!
```

**Řešení:**
1. Nainstalovat Python z https://www.python.org/downloads/
2. Při instalaci zaškrtnout "Add Python to PATH"
3. Restartovat terminál

### VZ soubor se nepodařilo stáhnout

**Chyba:**
```
⚠️ VZ soubor se nepodařilo stáhnout
```

**Řešení:**
1. Stáhnout ručně z https://isvz.nipez.cz/opendata/nova/2026/kategorie
2. Uložit jako `data\VZ\VZ-2026-02.json`
3. Spustit znovu s `-SkipVZ` nebo `skip`

## 💡 Tipy

**Pravidelné měsíční spouštění:**
```powershell
# Vytvořit úlohu v Task Scheduler
# Akce: powershell.exe
# Argumenty: -ExecutionPolicy Bypass -File "C:\Git\ISVZ\run_monthly.ps1"
# Spouštěč: Měsíčně, 7. den v měsíci, 8:00
```

**Automatizace bez interakce:**
```powershell
.\run_monthly.ps1 -SkipComparison | Out-File log.txt
```

**Testování bez stahování:**
```powershell
.\run_monthly.ps1 -SkipDownload
```

## 📚 Související dokumentace

- [QUICKSTART.md](../QUICKSTART.md) - Rychlý start pro nové uživatele
- [MONTHLY_README.md](MONTHLY_README.md) - Detailní popis měsíčního procesu
- [FILE_STRUCTURE.md](FILE_STRUCTURE.md) - Struktura projektu

---

**Doporučení:** Používejte **run_monthly.ps1** pro nejlepší uživatelský zážitek!
