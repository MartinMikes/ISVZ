# Porovnávání měsíců - Dokumentace

## 📋 Přehled

Systém umožňuje porovnávat ICT zakázky mezi měsíci a vytvářet rozdílové reporty. Podporuje automatické určení předchozího měsíce i explicitní zadání obou měsíců.

## 🚀 Použití

### Základní syntaxe

```bash
# Auto-výpočet předchozího měsíce (doporučeno)
python monthly_process.py --compare YYYY MM

# Explicitní zadání obou měsíců
python monthly_process.py --compare YYYY1 MM1 YYYY2 MM2
```

### Příklady

#### 1️⃣ Automatické určení předchozího měsíce

```bash
# Porovná únor 2026 s lednem 2026
python monthly_process.py --compare 2026 2

# Výstup:
# 📅 Starší: 1/2026
# 📅 Novější: 2/2026
```

#### 2️⃣ Přechod mezi roky

```bash
# Porovná leden 2026 s prosincem 2025
python monthly_process.py --compare 2026 1

# Výstup:
# 📅 Starší: 12/2025
# 📅 Novější: 1/2026
```

#### 3️⃣ Explicitní zadání

```bash
# Porovná prosinec 2025 s lednem 2026
python monthly_process.py --compare 2025 12 2026 1
```

## 📁 Výstupní soubory

Reporty se ukládají s **krátkým názvem** vztahujícím se k novějšímu měsíci:

```
output/reports/
├── DIFF_VZ_02-2026.md      # VZ report pro únor 2026 (vs. leden 2026)
└── DIFF_DNS_02-2026.md     # DNS report pro únor 2026 (vs. leden 2026)
```

### Starý formát (již se nepoužívá)

```
DIFF_VZ_01-2026_vs_02-2026.md   ❌ Dlouhý, nepoužívá se
DIFF_VZ_02-2026.md              ✅ Krátký, aktuální formát
```

## 🔍 Obsah reportů

### Souhrn

```markdown
| Kategorie | Počet |
|-----------|-------|
| Zakázky v 1/2026 | 152 |
| Zakázky v 2/2026 | 183 |
| **Nové zakázky** | **45** |
| **Zmizely** | **14** |
| Společné | 138 |
```

### Detaily

- **Nové zakázky** - Kompletní výpis nových položek s názvem, hodnotou, lhůtou
- **Zmizely zakázky** - Položky které již nejsou v novém měsíci (vypršela lhůta, ukončeno)

## 🔄 Logika předchozího měsíce

```python
def get_previous_month(year, month):
    if month > 1:
        return (year, month - 1)  # Únor → Leden
    else:
        return (year - 1, 12)     # Leden → Prosinec předchozího roku
```

## ⚙️ Technické detaily

### Kategorie

Porovnání se provádí pro:
- **VZ** (Veřejné zakázky) - porovnává se `identifikator_NIPEZ`
- **DNS** (Dynamické nákupní systémy) - porovnává se `identifikator_NIPEZ`

### Požadované soubory

Pro porovnání musí existovat ICT soubory v obou měsících:

```
data/VZ/VZ-2026-01-ICT.json      ← Starší měsíc
data/VZ/VZ-2026-02-ICT.json      ← Novější měsíc
data/DNS/DNS-2026-01-ICT.json
data/DNS/DNS-2026-02-ICT.json
```

Pokud soubory chybí, zobrazí se varování:

```
⚠️  VZ soubory neexistují pro porovnání
```

## 💡 Tipy

### Měsíční workflow

```bash
# 1. Zpracovat nový měsíc
python monthly_process.py --year 2026 --month 2 --download

# 2. Automaticky porovnat s minulým měsícem
python monthly_process.py --compare 2026 2

# 3. Zkontrolovat report
cat output/reports/DIFF_VZ_02-2026.md
```

### Porovnání libovolných měsíců

```bash
# Porovnat např. leden s březnem (přeskočit únor)
python monthly_process.py --compare 2026 1 2026 3
```

### Čištění starých reportů

```powershell
# Smazat všechny staré reporty s dlouhými názvy
Remove-Item output\reports\DIFF_*_vs_*.md
```

## ❌ Chybové stavy

### Nesprávný počet argumentů

```bash
python monthly_process.py --compare 2026

# ❌ Chyba: --compare vyžaduje 2 nebo 4 argumenty
#    Příklady:
#      --compare 2026 1           (porovná s předchozím měsícem)
#      --compare 2025 12 2026 1   (porovná zadané měsíce)
```

### Chybějící data

```bash
python monthly_process.py --compare 2026 5

# ⚠️  VZ soubory neexistují pro porovnání
# ⚠️  DNS soubory neexistují pro porovnání
```

## 📊 Příklad výstupu

```
======================================================================
  POROVNÁNÍ MĚSÍCŮ
======================================================================

📅 Starší: 12/2025
📅 Novější: 1/2026

🔍 Porovnávám VZ (Veřejné zakázky)...
   Zakázek v 12/2025: 1
   Zakázek v 1/2026: 152
   Nové: 152 | Zmizely: 1 | Společné: 0
   💾 Report: output/reports\DIFF_VZ_01-2026.md

🔍 Porovnávám DNS (Dynamické nákupní systémy)...
   Záznamů v 12/2025: 7
   Záznamů v 1/2026: 14
   Nové: 11 | Zmizely: 4 | Společné: 3
   💾 Report: output/reports\DIFF_DNS_01-2026.md
```

## 🔗 Související dokumentace

- [MONTHLY_README.md](MONTHLY_README.md) - Kompletní měsíční workflow
- [FILE_STRUCTURE.md](FILE_STRUCTURE.md) - Struktura projektu
- [README.md](../README.md) - Hlavní dokumentace
