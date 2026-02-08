# Generování reportů - Dokumentace

## 📋 Přehled

Automatické generování přehledných Markdown a CSV reportů z vyfiltrovaných JSON souborů veřejných zakázek.

**Nové funkce:**
- ⭐ Doporučení (1-5) podle technologické shody
- 🚫 Vyloučení stavebních prací z ICT
- 📊 Řazení podle doporučení (nejlepší nahoře)
- 📝 9 nových polí (kategorie, sektor, financování EU, SME...)

## 📊 Struktura CSV (32 sloupců)

### Kompletní seznam sloupců

#### 1-17: Základní informace
1. **ID NIPEZ** - Identifikátor zakázky v systému NIPEZ
2. **Název** - Název veřejné zakázky
3. **Druh** - Druh veřejné zakázky (Dodávky/Služby/Stavební práce)
4. **Režim** - Režim zadání (Nadlimitní/Podlimitní/...)
5. **Hodnota (Kč)** - Předpokládaná hodnota v Kč
6. **Stav** - Stav zadávacího řízení
7. **Druh postupu** - Druh zadávacího postupu (Otevřené řízení/...)
8. **El. nástroj** - Elektronický nástroj (TA/VVZ/NEN/...)
9. **CPV hlavní** - Hlavní CPV kód
10. **CPV popis** - Automatický popis CPV kódu
11. **Lhůta podání nabídky** - Datum a čas ve formátu DD.MM.YYYY HH:MM
12. **Lhůta žádost o účast** - Datum a čas (pokud existuje)
13. **Zadavatel** - Název zadavatele
14. **IČO zadavatele** - IČO zadavatele
15. **Místo plnění** - Textový popis místa plnění
16. **NUTS** - NUTS kód
17. **Kraj** - Název kraje (převedeno z NUTS pomocí číselníku)

#### 18: Doporučení
18. **Doporučení** - Skóre 1-5 ⭐ (1 = nejlepší shoda, pouze ICT)

#### 19-23: Nová pole - Fáze 1 (Priorita A)
19. **Financování EU** - Ano/Ne - alespoň částečně financováno z EU
20. **Kategorie zadavatele** - Typ zadavatele (Česká republika/Obec/Kraj/...)
21. **Sektor zadavatele** - Hlavní předmět činnosti veřejného zadavatele
22. **Datum zahájení** - Datum zahájení zadávacího postupu (YYYY-MM-DD)
23. **Váha ceny (%)** - Váha kritéria ceny v hodnocení nabídek (0-100)

#### 24-27: Nová pole - Fáze 2 (Priorita B)
24. **Doba trvání (měsíce)** - Doba trvání smlouvy normalizovaná na měsíce
25. **E-platba** - Ano/Ne - bude použita elektronická platba
26. **Vhodné pro SME** - Ano/Ne - vhodné pro malé a střední podniky
27. **Typ dle hodnoty** - Typ zakázky dle předpokládané hodnoty (Nadlimitní/Podlimitní veřejná zakázka)

#### 28-31: URL odkazy
28. **URL Profil zadavatele** - Odkaz na profil zadavatele
29. **URL Dokumentace** - Odkaz na zadávací dokumentaci
30. **URL Podání nabídek** - Odkaz na elektronické podání nabídek
31. **URL Otevírání** - Odkaz na otevírání nabídek

#### 32: Popis
32. **Popis (zkrácený)** - Prvních 200 znaků popisu předmětu zakázky

### Statistiky vyplněnosti (VZ-ICT 01/2026, 145 zakázek)

| Pole | Vyplněnost | Poznámka |
|------|------------|----------|
| **Kategorie zadavatele** | 99.3% | Nejlepší, téměř vždy dostupné |
| **Typ dle hodnoty** | 100% | Vždy vyplněno |
| **Sektor zadavatele** | 92.4% | Velmi dobrá dostupnost |
| **Váha ceny (%)** | 91.7% | Většinou dostupné |
| **Financování EU** | 100% | Vždy vyplněno (33.8% = Ano) |
| **E-platba** | 100% | Vždy vyplněno |
| **Vhodné pro SME** | 100% | Vždy vyplněno (33.1% = Ano) |
| **Doba trvání** | 0% | ⚠️ Pole v datech chybí |
| **Datum zahájení** | ~95% | Obvykle dostupné |

**Doporučení pro analýzy:**
- ✅ Nejvíce využitelná pole: Kategorie zadavatele, Typ dle hodnoty, Sektor, Váha ceny
- 🏢 SME filtr: 33% zakázek je vhodných pro malé a střední podniky
- 🇪🇺 EU projekty: 34% zakázek má financování z EU
- ⚠️ Doba trvání: Pole není v datech vyplňováno, plánované k odstranění

## 🎯 Funkce

### Typy reportů

1. **VZ-OPEN** - Otevřené veřejné zakázky (všechny obory)
2. **VZ-ICT** - ICT veřejné zakázky (bez stavebních prací, s doporučeními)
3. **DNS-ICT** - ICT z dynamických nákupních systémů (s doporučeními)

### Výstupní formáty

- **Markdown (.md)** - Přehledné reporty s číselníkovými informacemi
- **CSV (.csv)** - Strukturovaná data pro import do Excel/databází

## 📁 Struktura výstupů

```
output/
├── reports/
│   ├── DIFF_VZ_*.md              # Rozdílové reporty (porovnání měsíců)
│   ├── VZ-OPEN_YYYY-MM.md        # Tabulkový souhrn - otevřené zakázky
│   ├── VZ-ICT_YYYY-MM.md         # Tabulkový souhrn - ICT zakázky
│   ├── DNS-ICT_YYYY-MM.md        # Tabulkový souhrn - DNS ICT
│   └── YYYY/MM/                  # Detailní měsíční reporty
│       ├── VZ-OPEN_YYYY-MM.md
│       ├── VZ-ICT_YYYY-MM.md
│       └── DNS-ICT_YYYY-MM.md
└── csv/
    ├── VZ-OPEN.csv               # ⭐ Nejnovější CSV (bez data, pro Excel)
    ├── VZ-ICT.csv                # ⭐ Nejnovější CSV (bez data, pro Excel)
    ├── DNS-ICT.csv               # ⭐ Nejnovější CSV (bez data, pro Excel)
    └── YYYY/MM/                  # CSV archiv
        ├── VZ-OPEN_YYYY-MM.csv
        ├── VZ-ICT_YYYY-MM.csv
        └── DNS-ICT_YYYY-MM.csv
```

**Příklad:** Leden 2026
```
output/reports/VZ-ICT_2026-01.md          ← Tabulkový souhrn (root)
output/reports/2026/01/VZ-ICT_2026-01.md  ← Detailní report (subfolder)
output/csv/VZ-ICT.csv                     ← Nejnovější CSV (přepisuje se)
output/csv/2026/01/VZ-ICT_2026-01.csv     ← CSV archiv
```

**Poznámka k CSV souborům**:
- Soubory bez data (`VZ-ICT.csv`) obsahují **vždy nejnovější data**
- Přepisují se při každém běhu `monthly_process.py`
- Ideální pro připojení v Excelu (automatická aktualizace)
- Archivní soubory s datem zůstávají pro historii

## 📝 Obsah Markdown reportů

### 1. Tabulkový souhrn (root složka)

Kompaktní přehled všech zakázek v jedné tabulce, umístěný přímo v `output/reports/`.

**Název**: `{TYP}_YYYY-MM.md` (např. `VZ-ICT_2026-01.md`)

**Obsah**:
- 📊 Rychlý přehled - statistiky (celková hodnota, průměr, rozdělení podle druhu)
- 📋 Tabulkový přehled - všechny zakázky v jedné tabulce

**Sloupce tabulky**:
| Sloupec | Popis | Příklad |
|---------|-------|---------|
| # | Pořadové číslo | 1, 2, 3... |
| ID NIPEZ | Identifikátor zakázky | `RVZ2600001030` |
| Název | Název zakázky (zkráceno na 60 znaků) | `UTB – MILAN – FLKŘ - Pick to Light...` |
| Druh | Druh zakázky | Dodávky / Služby / Stavební práce |
| Hodnota | Předpokládaná hodnota | `45454545 Kč` nebo `45.5M Kč` |
| Stav | Stav zakázky (zkráceno) | Aktivní / Zadán / neuvedeno |
| Lhůta | Datum lhůty | `09.02.2026` |
| Zadavatel | Název zadavatele (zkráceno) | `ČSSZ` / `Město Praha` |
| CPV | Hlavní CPV kód | `48000000` |
| Kraj | Kraj určený z NUTS kódu | `Hlavní město Praha` / `Zlínský kraj` |
| Místo | Místo plnění (zkráceno) | `Praha` / `CZ010` |

**Poznámky**:
- Velké částky automaticky převedeny na miliony (např. `45.5M Kč`)
- Dlouhé texty zkráceny třemi tečkami (`...`)
- Tento soubor se každý měsíc **přepíše** novými daty

### 2. Detailní report (YYYY/MM/ podsložka)

Kompletní informace o každé zakázce včetně všech číselníkových údajů.

**Název**: `{TYP}_YYYY-MM.md` v podsložce `YYYY/MM/`

### Hlavička

```markdown
# ICT veřejné zakázky - leden 2026

**Vygenerováno**: 07.02.2026 22:08
**Počet zakázek**: 152
```

### Statistiky

#### Podle druhu zakázky
| Druh | Počet | Podíl |
|------|-------|-------|
| Dodávky | 79 | 52.0% |
| Služby | 66 | 43.4% |
| Stavební práce | 7 | 4.6% |

#### Podle hodnoty
- **Celková hodnota**: 3 257 744 216 Kč
- **Průměrná hodnota**: 28 084 002 Kč
- **Zakázek s hodnotou**: 116 / 152

### Detail zakázky

Pro každou zakázku obsahuje:

#### 📌 Základní informace
- **Druh**: Dodávky / Služby (stavební práce vyloučeny z ICT)
- **Režim**: Nadlimitní / Podlimitní / ...
- **Hodnota**: Částka v Kč
- **Stav**: Aktivní/Neukončen / Dokončen/Zadán / ...
- **Typ dle hodnoty**: Nadlimitní veřejná zakázka / Podlimitní veřejná zakázka
- **Financování EU**: Ano / Ne
- **Datum zahájení**: YYYY-MM-DD (datum zahájení zadávacího řízení)

#### 🔧 Zadávací postup
- **Druh postupu**: Otevřené řízení / Zjednodušené podlimitní / ...
- **Elektronický nástroj**: TA / VVZ / NEN

#### ⭐ Doporučení (pouze ICT)
- Známka 1-5 podle technologické shody
- Zobrazeno jako hvězdičky: ⭐⭐⭐⭐⭐ (1) až ⭐ (5)
- Detail viz [DOPORUCOVACI_SYSTEM.md](DOPORUCOVACI_SYSTEM.md)

#### 📝 Předmět zakázky
Textový popis předmětu veřejné zakázky (zkráceno na 500 znaků).

#### 🏷️ CPV klasifikace
- **Hlavní CPV**: Kód + automatický popis (např. `48000000` - Softwarové balíky)
- **Vedlejší CPV**: Seznam doplňkových kódů
- **Kritéria hodnocení**: Cena XX% / Kvalita XX% (pokud je dostupné)

#### ⏰ Lhůty
- **Lhůta pro podání nabídky**: Datum a čas (formát DD.MM.YYYY HH:MM)
- **Lhůta pro podání žádosti o účast**: Datum a čas (pokud existuje)

#### 🏛 Zadavatel
- **Název**: Název zadavatele
- **IČO**: IČO zadavatele
- **Kategorie**: Česká republika / Obec / Kraj / ... (99% vyplněnost)
- **Sektor**: Hlavní předmět činnosti (92% vyplněnost)
- **Profil zadavatele**: URL odkaz

#### 📍 Místo plnění
- **NUTS kód**: CZ010 / CZ020 / ...
- **Kraj**: Název kraje (převedeno z NUTS)

#### ℹ️ Další informace
- **Vhodné pro SME**: Ano / Ne (33% zakázek = Ano)
- **E-platba**: Ano / Ne (elektronická platba)
- **Doba trvání**: X měsíců (pokud je uvedeno - velmi vzácné)

#### 🏢 Zadavatel
- **Název**: Jméno zadavatele
- **IČO**: Identifikační číslo
- **Kategorie**: Česká republika / Obec / Kraj / ... (99% vyplněnost)
- **Sektor**: Hlavní předmět činnosti (92% vyplněnost)
- **Profil zadavatele**: Odkaz na profil (pokud je k dispozici)

#### 📍 Místo plnění
- **Místo**: Konkrétní místo (pokud uvedeno)
- **NUTS kód**: Kód NUTS regionu (např. CZ010 - Praha)
- **Kraj**: Název kraje určený z NUTS kódu

#### ℹ️ Další informace
- **Vhodné pro SME**: Ano / Ne (33% zakázek = Ano)
- **E-platba**: Ano / Ne (elektronická platba)
- **Doba trvání**: X měsíců (pokud je uvedeno - velmi vzácné)

#### 🔗 Odkazy
- **Zadávací dokumentace**: Odkaz ke stažení dokumentace
- **Podání nabídek**: Odkaz pro elektronické podání
- **Otevírání nabídek**: Odkaz k otevírání (pokud je k dispozici)

## 💾 CSV formát

### Struktura

Soubory používají:
- **Oddělovač**: středník (`;`)
- **Kódování**: UTF-8 s BOM (správné zobrazení v Excel)
- **Zalomení řádků**: CRLF (Windows kompatibilní)

### Použití CSV sloupců (32 celkem)

Kompletní seznam viz sekce "Struktura CSV (32 sloupců)" výše.

**Nejdůležitější sloupce pro filtrování:**
- **Doporučení** - řazení podle priority (1-5)
- **Kategorie zadavatele** - filtr podle typu zadavatele
- **Sektor zadavatele** - filtr podle oblasti činnosti
- **Kraj** - regionální filtrování
- **Vhodné pro SME** - filtr pro malé a střední podniky
- **Financování EU** - filtr EU projektů
- **Váha ceny (%)** - analýza důrazu na cenu vs. kvalitu
- **Typ dle hodnoty** - nadlimitní vs. podlimitní zakázky

## 🚀 Použití

### Automatické generování (v rámci měsíčního procesu)

```bash
python monthly_process.py --year 2026 --month 2
```

Automaticky vygeneruje reporty po dokončení filtrování.

### Ruční generování

```bash
cd scripts
python generate_reports.py --year 2026 --month 2
```

### Parametry

```bash
python generate_reports.py [OPTIONS]

Options:
  --year, -y YEAR           Rok (výchozí: aktuální)
  --month, -m MONTH         Měsíc 1-12 (výchozí: aktuální)
  --data-dir DIR            Adresář s daty (výchozí: ../data)
  --output-dir DIR          Výstupní adresář (výchozí: ../output)
```

### Použití CSV v Excelu

**Nejnovější data (doporučeno)**:

Excel může načítat data přímo ze souborů bez data:
1. Excel → Data → Z textu/CSV
2. Vybrat `output/csv/VZ-ICT.csv`
3. Importovat data
4. Při příštím měsíčním běhu se soubor automaticky aktualizuje

**Výhody**:
- Stálý název souboru (`VZ-ICT.csv`)
- Automatická aktualizace při každém měsíčním běhu
- Excel může mít připojené dotazy/pivoty

**Archivní data**:

Pro historické srovnání použít soubory s datem:
- `output/csv/2026/01/VZ-ICT_2026-01.csv`
- `output/csv/2026/02/VZ-ICT_2026-02.csv`

## 🔍 Číselníkové informace

### NUTS → Kraj

Reporty automaticky mapují NUTS kódy na názvy krajů pomocí číselníku `data/nuts_kraje.json`.

**Mapování NUTS 3 (kraje):**
| NUTS | Kraj |
|------|------|
| CZ010 | Hlavní město Praha |
| CZ020 | Středočeský kraj |
| CZ031 | Jihočeský kraj |
| CZ032 | Plzeňský kraj |
| CZ041 | Karlovarský kraj |
| CZ042 | Ústecký kraj |
| CZ051 | Liberecký kraj |
| CZ052 | Královéhradecký kraj |
| CZ053 | Pardubický kraj |
| CZ063 | Kraj Vysočina |
| CZ064 | Jihomoravský kraj |
| CZ071 | Olomoucký kraj |
| CZ072 | Zlínský kraj |
| CZ080 | Moravskoslezský kraj |

**Použití pro filtrování:**
- CSV soubory obsahují sloupec "Kraj" pro snadné filtrování v Excelu
- MD reporty zobrazují kraj v sekci "📍 Místo plnění"
- Tabulkové souhrny mají sloupec "Kraj" pro rychlý regionální přehled

### CPV kódy (automatické překlady)

Skript obsahuje mapování hlavních ICT CPV kódů:

| CPV | Popis |
|-----|-------|
| 30* | Kancelářské a výpočetní stroje |
| 30200000 | Počítačová zařízení a příslušenství |
| 48* | Softwarové balíky a informační systémy |
| 72* | IT služby: konzultace, vývoj, internet |
| 72000000 | IT služby |
| 72200000 | Programátorské služby |

### Stavy zakázek

Reporty zobrazují aktuální stav podle číselníku:
- **Aktivní/Neukončen** - zakázka běží
- **Dokončen/Zadán** - zakázka zadána
- **Ukončeno plnění smlouvy** - smlouva dokončena
- **Zrušen** - zakázka zrušena
- **Neúspěšný** - neúspěšné zadání

### Druhy zadávacího postupu

Např.:
- Otevřené řízení
- Otevřená výzva při zadávání VZ malého rozsahu
- Zjednodušené podlimitní řízení
- Jednací řízení bez uveřejnění
- ...

(Kompletní seznam v `docs/CISELNIKY_PREHLED.md`)

## 📊 Příklady použití

### Excel import

1. Otevřít Excel
2. Data → Z textu/CSV
3. Vybrat soubor `.csv`
4. Kódování: UTF-8
5. Oddělovač: Středník
6. Import

### Power BI

```powerquery
let
    Source = Csv.Document(File.Contents("output/csv/2026/01/VZ-ICT_2026-01.csv"),
        [Delimiter=";", Encoding=65001])
in
    Source
```

### Python pandas

```python
import pandas as pd

df = pd.read_csv('output/csv/2026/01/VZ-ICT_2026-01.csv', 
                 sep=';', 
                 encoding='utf-8-sig')
print(df.head())
```

## 🎨 Vlastní úpravy

### Přidání dalších CPV kódů

V souboru `scripts/generate_reports.py`:

```python
def get_cpv_description(cpv_code: str) -> str:
    cpv_map = {
        '30': 'Kancelářské a výpočetní stroje',
        '48': 'Softwarové balíky',
        '72': 'IT služby',
        # Přidejte vlastní:
        '90': 'Vaše kategorie',
    }
    # ...
```

### Změna struktury CSV

Upravte funkci `generate_csv_report()` a přidejte/odeberte sloupce podle potřeby.

### Změna délky popisu

```python
# V generate_markdown_report()
if len(popis) > 500:  # Změňte na 1000 pro delší popisy
    popis = popis[:497] + "..."

# V generate_csv_report()
if len(popis) > 200:  # Změňte na 300 pro CSV
    popis = popis[:197] + "..."
```

## 🔄 Integrace do workflow

### Měsíční proces

Reporty se generují automaticky jako **KROK 4** v `monthly_process.py`:

1. KROK 1: Filtrování otevřených zakázek (VZ)
2. KROK 2: Filtrování ICT zakázek (VZ)
3. KROK 3: Filtrování ICT z DNS
4. **KROK 4: Generování reportů (MD + CSV)** ← NOVÝ

### Výstup workflow

```
✅ Vygenerováno reportů: 6 (MD + CSV)

📁 Výstupní složky:
   - output\reports/2026/01/
   - output\csv/2026/01/
```

## ⚙️ Technické detaily

### Kódování

- **Windows console**: Automatická oprava UTF-8 encoding
- **Markdown soubory**: UTF-8 bez BOM
- **CSV soubory**: UTF-8 **s BOM** (pro správné zobrazení v Excel)

### Výkon

- **VZ-OPEN** (970 záznamů): ~2 sekundy
- **VZ-ICT** (152 záznamů): <1 sekunda
- **DNS-ICT** (14 záznamů): <1 sekunda

### Závislosti

Používá pouze standardní knihovny Python 3:
- `json` - načítání JSON souborů
- `csv` - generování CSV
- `pathlib` - práce se složkami
- `datetime` - formátování datumů

## 🐛 Řešení problémů

### CSV se špatně zobrazuje v Excel

**Problém**: Diakritika nebo špatné oddělovače.

**Řešení**: 
1. Zkontrolujte, že Excel používá UTF-8
2. Při importu vyberte "Středník" jako oddělovač
3. Soubory mají UTF-8 s BOM, což Excel rozpozná automaticky

### Markdown obsahuje "None" místo hodnot

**Problém**: Data v JSON chybí nebo mají hodnotu `null`.

**Řešení**: Je to normální - některé zakázky nemají všechna pole vyplněná. Skript zobrazí "neuvedeno".

### Reporty se negenerují

**Problém**: Chybí vstupní JSON soubory.

**Řešení**: 
1. Nejdřív spusťte filtrování: `python monthly_process.py --year 2026 --month 1`
2. Zkontrolujte, že existují soubory `*-OPEN.json` a `*-ICT.json`

## 📚 Související dokumentace

- [MONTHLY_README.md](MONTHLY_README.md) - Měsíční workflow
- [CISELNIKY_PREHLED.md](CISELNIKY_PREHLED.md) - Číselníky ISVZ
- [FILE_STRUCTURE.md](FILE_STRUCTURE.md) - Struktura projektu
- [README.md](../README.md) - Hlavní dokumentace

## 💡 Tipy

1. **Pravidelné archivace**: Staré reporty můžete přesunout do `archive/reports/`
2. **Git ignoruje**: Reporty jsou v `.gitignore`, protože se regenerují
3. **CSV pro analýzy**: Použijte CSV pro import do BI nástrojů
4. **MD pro sdílení**: Markdown reporty jsou přehledné pro prezentace
5. **Chronologie**: Reporty jsou ve složkách YYYY/MM pro snadné procházení
