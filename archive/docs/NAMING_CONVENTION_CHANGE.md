# Změna názvové konvence souborů

## 📋 Přehled změny

**Datum**: 2026-02-07

Byla provedena změna názvové konvence JSON souborů z formátu `KATEGORIE-MM-YYYY` na `KATEGORIE-YYYY-MM` pro zajištění správného chronologického řazení.

## 🎯 Důvod změny

### Problém se starým formátem

Starý formát `VZ-MM-YYYY.json`:
```
VZ-01-2026.json
VZ-02-2026.json
VZ-12-2025.json  ← Řadí se až za 02-2026!
```

Lexikografické řazení neodpovídá chronologickému pořadí.

### Řešení - nový formát

Nový formát `VZ-YYYY-MM.json`:
```
VZ-2025-12.json  ← Správně první
VZ-2026-01.json
VZ-2026-02.json
```

Lexikografické řazení = chronologické řazení ✅

## 📝 Provedené změny

### 1. Přejmenování existujících souborů

Všech 16 souborů v `data/` bylo přejmenováno:

| Starý název | Nový název |
|------------|-----------|
| `VZ-01-2026.json` | `VZ-2026-01.json` |
| `VZ-12-2025.json` | `VZ-2025-12.json` |
| `VZ-01-2026-OPEN.json` | `VZ-2026-01-OPEN.json` |
| `VZ-01-2026-ICT.json` | `VZ-2026-01-ICT.json` |
| `DNS-01-2026.json` | `DNS-2026-01.json` |
| ... | ... |

### 2. Aktualizované skripty

**Hlavní orchestrace:**
- `monthly_process.py`
  - `download_month_data()` - generování názvů souborů
  - `process_month()` - cesty k VZ a DNS souborům
  - `compare_months()` - cesty k ICT souborům

**Stahovací skripty:**
- `download_vz.ps1` - URL a cílová cesta

**Filtrovací skripty:**
- `scripts/filter_open_tenders.py` - výchozí cesty
- `scripts/filter_ict_tenders.py` - výchozí cesty
- `scripts/filter_dns_ict.py` - výchozí cesty
- `scripts/show_ict_tenders.py` - výchozí cesty
- `scripts/extract_codebooks.py` - výchozí cesty

### 3. Aktualizovaná dokumentace

**Hlavní dokumentace:**
- `README.md`
  - Tabulka kategorií
  - Vysvětlení konvence
  - Příklady struktury souborů
  - Všechny příklady použití

**Dokumentace workflow:**
- `docs/MONTHLY_README.md` - příklady zpracování
- `docs/POROVNANI_MESICU.md` - příklady porovnávání
- `docs/isvz_datamodel.md` - název zdrojového souboru
- `docs/CISELNIKY_PREHLED.md` - zdroj dat

### 4. Co nebylo změněno

**Archivní soubory** (v `archive/`) nebyly upravovány, protože:
- Nejsou součástí aktivního workflow
- Slouží pouze pro referenci
- Obsahují zastaralé cesty (např. `isvz_data/`)

## 🧪 Testování

### Test 1: Chronologické řazení
```powershell
Get-ChildItem data\VZ\*.json | Sort-Object Name
```
Výsledek:
```
VZ-2025-12-ICT.json
VZ-2025-12-OPEN.json
VZ-2025-12.json
VZ-2026-01-ICT.json
VZ-2026-01-OPEN.json
VZ-2026-01.json
```
✅ Správné pořadí

### Test 2: Porovnání měsíců
```bash
python monthly_process.py --compare 2026 1
```
✅ Funguje bez chyb, načítá správné soubory

### Test 3: Download skript
```powershell
.\download_vz.ps1 -Year 2026 -Month 2 -WhatIf
```
Výstup:
```
URL: https://isvz.nipez.cz/sites/default/files/content/opendata-rvz/VZ-2026-02.json
Cil: data\VZ\VZ-2026-02.json
```
✅ Správné URL a cesta

### Test 4: Kontrola starého formátu
```powershell
# Hledání VZ-MM-YYYY v aktivních souborech
Select-String -Path *.py,*.ps1,*.md -Pattern "(VZ|DNS)-\d{2}-\d{4}"
```
✅ Žádné výskyty v aktivních souborech

## 📖 Nová konvence

### Formát názvů

```
[KATEGORIE]-[YYYY]-[MM][-SUFFIX].json
```

Kde:
- `KATEGORIE`: VZ, DNS, SON, SK, RVP
- `YYYY`: Rok (4 číslice)
- `MM`: Měsíc (2 číslice, 01-12)
- `SUFFIX`: Volitelný (např. `-OPEN`, `-ICT`)

### Příklady

**Originální soubory:**
- `VZ-2026-01.json` - Leden 2026
- `VZ-2025-12.json` - Prosinec 2025

**Zpracované soubory:**
- `VZ-2026-01-OPEN.json` - Otevřené zakázky
- `VZ-2026-01-ICT.json` - ICT zakázky

**DNS soubory:**
- `DNS-2026-01.json` - Originál
- `DNS-2026-01-ICT.json` - Filtrované ICT

### URL na ISVZ portálu

ISVZ portál používá STEJNÝ formát `YYYY-MM`:
```
https://isvz.nipez.cz/sites/default/files/content/opendata-rvz/VZ-2026-01.json
```

Naše konvence je tedy **konzistentní s ISVZ**! ✅

## 🔄 Migrace

### Pro existující workflow

Pokud máte vlastní skripty používající staré názvy:

**1. Jednoduchá náhrada v kódu:**
```python
# Starý způsob
file_path = f"VZ-{month:02d}-{year}.json"

# Nový způsob
file_path = f"VZ-{year}-{month:02d}.json"
```

**2. Přejmenování existujících souborů:**
```powershell
# PowerShell skript pro přejmenování
Get-ChildItem data -Recurse -Filter "*.json" | ForEach-Object {
    if ($_.Name -match '^(\w+)-(\d{2})-(\d{4})(.*)\.json$') {
        $newName = "$($matches[1])-$($matches[3])-$($matches[2])$($matches[4]).json"
        Rename-Item $_.FullName -NewName $newName
    }
}
```

## ✅ Checklist implementace

- [x] Přejmenování všech 16 souborů v `data/`
- [x] Aktualizace `monthly_process.py` (3 funkce)
- [x] Aktualizace `download_vz.ps1`
- [x] Aktualizace 5 skriptů v `scripts/`
- [x] Aktualizace `README.md`
- [x] Aktualizace 4 souborů v `docs/`
- [x] Testování chronologického řazení
- [x] Testování porovnání měsíců
- [x] Testování download skriptu
- [x] Kontrola zbylých výskytů starého formátu
- [x] Vytvoření dokumentace změny

## 📚 Související dokumentace

- [README.md](../README.md) - Hlavní dokumentace s novou konvencí
- [MONTHLY_README.md](MONTHLY_README.md) - Měsíční workflow
- [POROVNANI_MESICU.md](POROVNANI_MESICU.md) - Porovnávání měsíců
- [FILE_STRUCTURE.md](FILE_STRUCTURE.md) - Struktura projektu

## 💡 Výhody nové konvence

1. **Chronologické řazení** - Soubory se automaticky řadí časově
2. **Konzistence s ISVZ** - Stejný formát jako na portálu
3. **Mezinárodní standard** - YYYY-MM je ISO 8601 formát
4. **Lepší UX** - Při prohlížení složky jsou soubory logicky seřazeny
5. **Jednodušší vyhledávání** - `VZ-2026-*` najde všechny soubory z roku 2026

## 🔮 Budoucí kompatibilita

Všechny budoucí soubory budou automaticky vytvořeny v novém formátu:
- `monthly_process.py` generuje nové názvy
- `download_vz.ps1` stahuje s novými názvy
- Všechny filtrovací skripty pracují s novými názvy

Zpětná kompatibilita se starými názvy **není** podporována.
