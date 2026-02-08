# Analýza kategorií ISVZ

Přehled všech kategorií stažených z ISVZ a jejich relevance pro ICT zakázky.

## 📊 Souhrn kategorií (leden 2026)

| Kategorie | Název | Počet záznamů | ICT záznamy | % ICT | Status |
|-----------|-------|---------------|-------------|-------|--------|
| **VZ** | Veřejná zakázka | 71,377 (970 open) | 152 | 15.67% z open | ✅ Zpracováno |
| **DNS** | Dynamický nákupní systém | 223 | 14 | 6.28% | ✅ Zpracováno |
| **SON** | Soutěž o návrh | 22 | 0 | 0% | ⚠️ Není ICT |
| **SK** | Systém kvalifikace | 8 | 0 | 0% | ⚠️ Není ICT |
| **RVP** | Řízení na výběr poddodavatele | 0 | 0 | - | ⚠️ Prázdné |

## 🎯 Doporučení pro filtrování

### ✅ Zpracovávat:

1. **VZ (Veřejná zakázka)** - PRIORITA 1
   - Největší zdroj ICT zakázek
   - 152 ICT zakázek z 970 otevřených
   - Celková hodnota: 3.26 mld Kč
   - **Filtrování**: filter_open_tenders.py → filter_ict_tenders.py

2. **DNS (Dynamický nákupní systém)** - PRIORITA 2
   - Druhý největší zdroj ICT
   - 14 ICT záznamů z 223 celkem
   - Menší soubory (~4 MB), rychlé zpracování
   - **Filtrování**: filter_dns_ict.py

### ⚠️ Nepotřebné:

3. **SON (Soutěž o návrh)**
   - Architektonické soutěže
   - Zaměřeno na stavební návrhy
   - 0% ICT obsah
   - Ukázka: "Soutěž o návrh - Evangelická fara", "Krajinářská studie"

4. **SK (Systém kvalifikace)**
   - Kvalifikační systémy
   - Málá záznamů (8)
   - 0% ICT obsah
   - Zaměřeno na stavební/dopravní oblasti

5. **RVP (Řízení na výběr poddodavatele)**
   - Často prázdné
   - Zaměřeno na výběr subdodavatelů
   - 0% ICT obsah

## 📈 Statistiky ICT (leden 2026)

### VZ - Veřejné zakázky

```
Celkem zakázek:    71,377
Otevřených:           970 (1.36%)
ICT:                  152 (15.67% z otevřených)
Celková hodnota:   3.26 mld Kč
Průměrná hodnota: 28.1 mil. Kč
```

**Rozdělení podle druhu:**
- Dodávky: 79 (52.0%)
- Služby: 66 (43.4%)
- Stavební práce: 7 (4.6%)

**Top CPV kategorie:**
- 72** (IT služby): 48 zakázek
- 48** (Software a IS): 38 zakázek
- 30** (PC zařízení): 6 zakázek

### DNS - Dynamické nákupní systémy

```
Celkem DNS:        223
ICT DNS:            14 (6.28%)
```

**Příklady:**
- DNS pro informační systém SEIWIN
- Dynamický nákupní systém na poskytování IT služeb
- DNS pro dodávky výpočetní techniky a ICT vybavení
- Spotřební materiál ICT

## 🔄 Měsíční porovnání (prosinec 2025 → leden 2026)

### VZ

```
VZ 12/2025:    1 ICT zakázka
VZ 01/2026:  152 ICT zakázky
Nové:        152
Zmizely:       1
```

### DNS

```
DNS 12/2025:   7 ICT záznamů
DNS 01/2026:  14 ICT záznamů
Nové:         11
Zmizely:       4
Společné:      3
```

## 💡 Poznatky

1. **VZ je hlavní zdroj** - 15.67% otevřených VZ zakázek je ICT
2. **DNS je užitečný doplněk** - 6.28% DNS je ICT, menší soubory
3. **SON, SK, RVP nejsou relevantní** - 0% ICT obsah
4. **Leden 2026 má více ICT než prosinec 2025** - nový měsíc = nové zakázky
5. **DNS má stabilnější záznamy** - 3 společné mezi měsíci (dlouhodobé systémy)

## 🛠️ Implementace

Aktuální stav zpracování:

- ✅ VZ filtrování implementováno v `filter_open_tenders.py` + `filter_ict_tenders.py`
- ✅ DNS filtrování implementováno v `filter_dns_ict.py`
- ✅ Obě kategorie integrovány do `monthly_process.py`
- ✅ Porovnání mezi měsíci podporuje VZ i DNS
- ✅ Samostatné reporty: `DIFF_VZ_*.md` a `DIFF_DNS_*.md`

## 📝 Závěr

Pro efektivní sledování ICT příležitostí v ISVZ stačí zpracovávat **pouze VZ a DNS** kategorie. 
Ostatní kategorie (SON, SK, RVP) neobsahují ICT zakázky a není nutné je zpracovávat.

**Doporučený měsíční workflow:**
1. Stáhnout VZ a DNS soubory
2. Zpracovat: `python monthly_process.py --year YYYY --month MM`
3. Porovnat: `python monthly_process.py --compare YYYY1 MM1 YYYY2 MM2`
4. Zkontrolovat `reports/DIFF_VZ_*.md` a `reports/DIFF_DNS_*.md`
