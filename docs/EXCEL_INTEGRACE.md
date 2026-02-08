# Excel integrace - CSV soubory ISVZ

## 📊 Přehled

CSV soubory jsou generovány ve dvou verzích:
- **Nejnovější** (root `output/csv/`) - pro připojení v Excelu
- **Archivní** (`output/csv/YYYY/MM/`) - pro historické srovnání

## ⭐ Použití nejnovějších CSV v Excelu

### Výhody
- **Stálý název souboru** - nemusíte měnit cestu při aktualizaci
- **Automatická aktualizace** - při každém měsíčním běhu se data obnoví
- **Funkční dotazy a pivoty** - můžete vytvořit pokročilé Excel reporty

### Soubory

| Soubor | Obsah | Počet řádků (led 2026) |
|--------|-------|------------------------|
| `VZ-OPEN.csv` | Všechny otevřené zakázky | 970 |
| `VZ-ICT.csv` | ICT zakázky | 152 |
| `DNS-ICT.csv` | ICT z DNS | 14 |

**Umístění**: `output/csv/*.csv`

## 📥 Importování do Excelu

### Metoda 1: Import dat (doporučeno)

1. **Otevřít Excel**
2. **Data → Z textu/CSV**
3. **Vybrat soubor**: `output/csv/VZ-ICT.csv`
4. **Nastavení importu**:
   - Kódování: **65001: Unicode (UTF-8)**
   - Oddělovač: **Středník (;)**
   - Původ dat: **65001: Unicode (UTF-8)**
5. **Načíst data**

### Metoda 2: Power Query (pro pokročilé)

1. **Data → Získat data → Z textu/CSV**
2. **Vybrat** `output/csv/VZ-ICT.csv`
3. **Transformovat data** (volitelně):
   - Změnit datové typy
   - Filtrovat kraje
   - Přidat vypočítané sloupce
4. **Zavřít a načíst**

**Výhoda**: Při aktualizaci dat (Data → Aktualizovat vše) se data automaticky obnoví z CSV.

## 🔄 Aktualizace dat

### Automatická aktualizace

Po spuštění měsíčního procesu:
```bash
python monthly_process.py --year 2026 --month 2
```

Soubory v `output/csv/*.csv` se **přepíší** novými daty.

V Excelu:
1. **Data → Aktualizovat vše** (nebo Ctrl+Alt+F5)
2. Excel načte nová data z CSV
3. Pivoty a grafy se automaticky aktualizují

### Ruční aktualizace

Pokud CSV soubory byly přesunuty nebo změněny:
1. **Data → Dotazy a připojení**
2. **Upravit dotaz**
3. **Zdroj → Upravit nastavení**
4. **Změnit cestu** k CSV souboru

## 📋 Struktura CSV (18 sloupců)

| # | Sloupec | Datový typ | Příklad |
|---|---------|------------|---------|
| 1 | ID NIPEZ | Text | RVZ2600001030 |
| 2 | Název | Text | ČSSZ – Pořízení serverů... |
| 3 | Druh | Text | Dodávky / Služby |
| 4 | Režim | Text | Nadlimitní / Podlimitní |
| 5 | Hodnota (Kč) | Číslo | 45454545.0 |
| 6 | Stav | Text | Aktivní/Neukončen |
| 7 | Druh postupu | Text | Otevřené řízení |
| 8 | El. nástroj | Text | TA / NEN / VVZ |
| 9 | CPV hlavní | Text | 48000000 |
| 10 | CPV popis | Text | Softwarové balíky a IS |
| 11 | Lhůta podání nabídky | Datum+čas | 09.02.2026 09:00 |
| 12 | Lhůta žádost o účast | Datum+čas | 09.02.2026 09:00 |
| 13 | Zadavatel | Text | ČSSZ |
| 14 | IČO zadavatele | Text | 00006963 |
| 15 | Místo plnění | Text | Praha, Brno... |
| 16 | NUTS | Text | CZ010, CZ064... |
| 17 | Kraj | Text | Hlavní město Praha |
| 18 | **URL Profil zadavatele** | URL | https://tenderarena.cz |
| 19 | **URL Dokumentace** | URL | https://tenderarena.cz/... |
| 20 | **URL Podání nabídek** | URL | https://nen.nipez.cz/... |
| 21 | **URL Otevírání** | URL | https://tenderarena.cz/... |
| 22 | Popis (zkrácený) | Text | Předmět plnění... |

**Poznámky**:
- **Sloupec 17 (Kraj)** - přidán 2026-02-07
- **Sloupce 18-21 (URL)** - přidány 2026-02-08 pro snadný přístup k zakázkám
- **Celkem 22 sloupců** (dříve 18)

## 🎯 Příklady použití v Excelu

### 1. Pivot tabulka - zakázky podle krajů

1. **Vložit → Kontingenční tabulka**
2. **Řádky**: Kraj
3. **Hodnoty**: Počet položek (ID NIPEZ)
4. **Hodnoty**: Suma hodnoty (Kč)
5. **Seřadit**: Podle počtu (sestupně)

**Výsledek**: Přehled ICT zakázek podle krajů.

### 2. Graf - Top 10 krajů

1. Vytvořit pivot tabulku (viz výše)
2. **Vložit → Graf → Sloupcový graf**
3. Filtrovat Top 10 krajů
4. **Aktualizace**: Při nových datech se automaticky aktualizuje

### 3. Filtrování podle regionu

**Pouze Praha**:
1. Data → Filtr (Ctrl+Shift+L)
2. Sloupec "Kraj" → Vybrat pouze "Hlavní město Praha"
3. **Výsledek**: 60 zakázek (leden 2026)

**Morava (JMK + MSK + OLK + ZLK)**:
1. Sloupec "Kraj" → Zaškrtnout:
   - Jihomoravský kraj
   - Moravskoslezský kraj
   - Olomoucký kraj
   - Zlínský kraj
2. **Výsledek**: 37 zakázek

### 4. Analýza lhůt - zakázky končící v nejbližších 7 dnech

1. **Přidat sloupec** "Zbývá dní":
   ```excel
   =DNES()-K2  // K2 = Lhůta podání nabídky
   ```
2. **Filtrovat**: Zbývá dní < 7
3. **Seřadit**: Podle lhůty (vzestupně)

## 📈 Pokročilé scénáře

### Automatické upozornění na nové zakázky

1. **Power Automate** (pokud máte Office 365):
   - Sledovat změny CSV souboru
   - Poslat email při nových datech
   
2. **Excel makro**:
   ```vba
   Sub AktualizovatData()
       ActiveWorkbook.RefreshAll
       MsgBox "Data aktualizována z " & Date
   End Sub
   ```

### Porovnání měsíců

1. Importovat **dva CSV soubory**:
   - `output/csv/2026/01/VZ-ICT_2026-01.csv` (leden)
   - `output/csv/2026/02/VZ-ICT_2026-02.csv` (únor)
2. Power Query → **Sloučit dotazy** podle ID NIPEZ
3. **Vypočítat rozdíl** v počtu zakázek

### Přímé odkazy na zakázky

**Nově v CSV (sloupce 18-21)** - URL odkazy pro rychlý přístup:

1. **Otevření zakázky jedním kliknutím**:
   - Excel automaticky rozpozná URL
   - Ctrl+klik na buňku → otevře odkaz v prohlížeči

2. **Hyperlinky v Excelu**:
   ```excel
   =HYPERLINK(S2, "Dokumentace")  // S2 = sloupec URL Dokumentace
   ```
   Vytvoří klikací odkaz s vlastním textem

3. **Hromadné otevírání**:
   - Vyfiltrovat zakázky (např. podle kraje)
   - Ctrl+klik na každý URL v sloupci "URL Dokumentace"
   - Otevře všechny dokumentace ve vybraných zakázkách

4. **URL v kontingenčních tabulkách**:
   - URL pole lze přidat jako sloupec hodnot
   - Zobrazí URL první zakázky v každé skupině
   - Umožňuje rychlý přístup k reprezentativním zakázkám

**Statistika URL (leden 2026)**:
- **URL Profil zadavatele**: 100% (152/152 zakázek)
- **URL Dokumentace**: 84% (128/152 zakázek)
- **URL Podání nabídek**: 100% (152/152 zakázek)
- **URL Otevírání**: 16% (25/152 zakázek)

## ⚠️ Poznámky

### Kódování UTF-8
- CSV soubory používají **UTF-8 s BOM**
- Excel automaticky rozpozná české znaky
- Pokud ne, změnit kódování na 65001: Unicode (UTF-8)

### Oddělovač
- Používá se **středník (;)** místo čárky
- Excel v českém prostředí automaticky rozpozná
- Pokud ne, změnit v Data → Z textu/CSV → Oddělovač: Středník

### Formát data
- Lhůty jsou ve formátu: `DD.MM.YYYY HH:MM`
- Excel může automaticky převést na datum
- Doporučeno: Nastavit sloupce K a L jako **Datum a čas**

### Velikost souboru
- `VZ-OPEN.csv`: ~480 KB (970 zakázek)
- `VZ-ICT.csv`: ~83 KB (152 zakázek)
- `DNS-ICT.csv`: ~2 KB (14 zakázek)

Excel bez problémů načte všechny soubory.

## 🔗 Související dokumentace

- **[REPORT_GENERATION.md](REPORT_GENERATION.md)** - Kompletní dokumentace reportů
- **[NUTS_KRAJE.md](NUTS_KRAJE.md)** - Regionální číselník
- **[MONTHLY_README.md](MONTHLY_README.md)** - Měsíční automatizace

## 📝 Tipy

1. **Používejte nejnovější CSV** (`output/csv/*.csv`) pro běžnou práci
2. **Archivní CSV** (`output/csv/YYYY/MM/`) pro historické srovnání
3. **Power Query** je lepší než přímý import (umožňuje transformace)
4. **Pivoty automaticky aktualizují** při obnovení dat
5. **Uložte Excel sešit** se zapamatovanými dotazy (neukládejte data, jen připojení)

## ❓ Řešení problémů

**Excel nezobrazuje české znaky**:
- Zkontrolovat kódování: 65001: Unicode (UTF-8)
- CSV soubory mají BOM (Byte Order Mark) pro automatickou detekci

**Data se neaktualizují**:
- Data → Dotazy a připojení → Pravý klik na dotaz → Aktualizovat
- Zkontrolovat cestu k souboru (může být relativní/absolutní)

**Špatný oddělovač**:
- Změnit v Power Query: Zdroj → Upravit nastavení → Oddělovač: Středník

**Datum jako text**:
- Power Query → Změnit typ → Datum/Čas
- Excel: Formát buněk → Datum → DD.MM.YYYY HH:MM
