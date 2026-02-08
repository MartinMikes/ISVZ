# Analýza stavů a filtrování otevřených zakázek ISVZ

## Klíčová zjištění pro filtrování otevřených zakázek

### Kritéria pro identifikaci OTEVŘENÝCH zakázek:

1. **Absence výsledku ukončení** - pole `vysledek.vysledek_ukonceni_zadavaciho_postupu` musí být `null` nebo prázdné
2. **Existence aktivních lhůt** - pole `lhuty[]` obsahuje záznamy
3. **Datum konce lhůty** - `datum_a_cas_konce_lhuty` je v budoucnosti (po aktuálním datu)
4. **Druh lhůty** - zejména `"Lhůta pro podání nabídek"` nebo `"Lhůta pro podání žádostí o účast"`
5. **Datum ukončení postupu** - pole `datum_ukonceni_zadavaciho_postupu` je `null`

### Kde hledat?

Struktura v JSON:
```
data[]
  └─ verejna_zakazka
       └─ casti_verejne_zakazky[]
            └─ zadavaci_postup_pro_cast
                 ├─ datum_zahajeni_zadavaciho_postupu
                 ├─ datum_ukonceni_zadavaciho_postupu  <-- NULL = aktivní
                 ├─ lhuty[]                             <-- Kontrola termínů
                 │    ├─ druh_lhuty
                 │    ├─ datum_a_cas_konce_lhuty        <-- > nyní
                 │    └─ aktivni
                 └─ vysledek
                      └─ vysledek_ukonceni_zadavaciho_postupu  <-- NULL = aktivní
```

## Statistiky

### Typy formulářů

| Typ formuláře | Počet |
|--------------|-------|
| Zahájení | 4703 |
| Výsledek | 2552 |
| Změna závazku ze smlouvy | 2537 |
| Plánování | 1 |

### Typy oznámení

| Typ oznámení | Počet |
|--------------|-------|
| 16 – Oznámení o zahájení zadávacího řízení – obecná veřejná zakázka | 4228 |
| 38 – Oznámení o změně závazku ze smlouvy – obecná veřejná zakázka | 2389 |
| 29 – Oznámení o výsledku zadávacího řízení – obecná veřejná zakázka | 2227 |
| 17 – Oznámení o zahájení zadávacího řízení – sektorová veřejná zakázka | 423 |
| 30 – Oznámení o výsledku zadávacího řízení – sektorová veřejná zakázka | 267 |
| 39 – Oznámení o změně závazku ze smlouvy – sektorová veřejná zakázka | 144 |
| 31 – Oznámení o výsledku zadávacího řízení – veřejná zakázka v oblasti obrany nebo bezpečnosti | 30 |
| 18 – Oznámení o zahájení zadávacího řízení – veřejná zakázka v oblasti obrany nebo bezpečnosti | 20 |
| 34 – Oznámení o výsledku zadávacího řízení – sektorová veřejná zakázka ve zjednodušeném režimu | 16 |
| 19 – Oznámení o zahájení koncesního řízení | 12 |
| 20 – Oznámení o zahájení zadávacího řízení – veřejná zakázka ve zjednodušeném režimu | 11 |
| 21 – Oznámení o zahájení zadávacího řízení – sektorová veřejná zakázka ve zjednodušeném režimu | 9 |
| 32 – Oznámení o výsledku koncesního řízení | 6 |
| 33 – Oznámení o výsledku zadávacího řízení – veřejná zakázka ve zjednodušeném režimu | 6 |
| E6 - Oznámení o změně závazku ze smlouvy - obrana a bezpečnost | 4 |
| 10 – Předběžné oznámení použité jako výzva k projevení předběžného zájmu – obecná veřejná zakázka | 1 |

### Stavy zadávacího postupu

| Stav | Počet |
|------|-------|
| Dokončen/Zadán | 53582 |
| Ukončeno plnění smlouvy | 17666 |
| Zrušen | 12672 |
| Aktivní/Neukončen | 407 |
| Neúspěšný | 40 |

### Druhy zadávacího postupu

| Druh | Počet |
|------|-------|
| Otevřená výzva při zadávání veřejných zakázek malého rozsahu | 26546 |
| Otevřené řízení | 24817 |
| Zadávání VZ v dynamickém nákupním systému | 11134 |
| Zjednodušené podlimitní řízení | 8413 |
| Zadávací postup na základě výjimky v ostatních případech | 6915 |
| Uzavřená výzva při zadávání veřejných zakázek malého rozsahu | 2889 |
| Postup s obnovením soutěže | 2857 |
| Přímé zadání při zadávání veřejných zakázek malého rozsahu | 2489 |
| Jednací řízení bez uveřejnění | 879 |
| Postup bez obnovení soutěže | 838 |
| Jednací řízení s uveřejněním | 439 |
| Užší řízení | 318 |
| Řízení pro zadání veřejné zakázky ve zjednodušeném režimu | 145 |
| Koncesní řízení | 43 |
| Řízení se soutěžním dialogem | 26 |

### Druhy lhůt

| Druh lhůty | Počet |
|------------|-------|
| Lhůta pro podání nabídky | 82288 |
| Lhůta pro podání žádosti o vysvětlení zadávací dokumentace | 5875 |
| Lhůta pro vysvětlení zadávací dokumentace | 3628 |
| Lhůta pro objasnění nebo doplnění údajů, dokladů, vzorků nebo modelů | 2965 |
| Zadávací lhůta | 1689 |
| Lhůta pro podání žádosti o účast | 710 |
| Lhůta pro vyřízení námitek | 266 |
| Lhůta pro podání předběžné nabídky | 38 |
| Předpokládané datum odeslání výzvy k podání nabídek v řízeních zahrnujících dvě fáze (nebo více fází) | 16 |
| Lhůta pro podání předběžného zájmu | 2 |
| Lhůta pro získání bezpečnostní prověrky | 1 |

### Výsledky ukončení zadávacího postupu

| Výsledek | Počet |
|----------|-------|
| Uzavření smlouvy | 60121 |
| Rozhodnutí o zrušení zadávacího postupu | 11641 |
| Uzavření rámcové dohody | 2017 |
| Ukončení zadávacího postupu dle § 40 odst. 5 zákona č. 134/2016 Sb. | 34 |

### Další statistiky

- Zakázky s datem zahájení: 86640
- Zakázky s datem ukončení: 5400
- Zakázky s lhůtami: 82563
- Aktivní lhůty: 14865

## Příklady

### Příklad pravděpodobně OTEVŘENÉ zakázky

**RVZ2600001221**: Revitalizace volnočasového areálu Svatošské údolí

- **Druh**: Stavební práce
- **Datum zahájení**: 2026-01-08T13:26:06
- **Datum ukončení**: None *(NULL = probíhá)*
- **Stav**: None
- **Výsledek ukončení**: None *(NULL = probíhá)*
- **Lhůty**:
  - Zadávací lhůta: konec None, aktivní: None
  - Lhůta pro podání nabídky: konec 2026-02-09T09:00:00, aktivní: None

### Příklad UZAVŘENÉ zakázky

**RVZ2600001263**: Překlady anotací pro odborné příspěvky pro účely DKRVO

- **Druh**: Služby
- **Datum zahájení**: 2025-11-28T00:00:00
- **Datum ukončení**: None
- **Stav**: Dokončen/Zadán
- **Výsledek ukončení**: Uzavření smlouvy ✓
- **Datum zrušení**: 0001-01-01T00:00:00

**RVZ2600001679**: 03 Výzva k RD - oprava stanových přístřešků k PV3S

- **Druh**: Služby
- **Datum zahájení**: 2025-03-20T06:56:48
- **Datum ukončení**: 2025-05-28T07:09:59
- **Stav**: Ukončeno plnění smlouvy
- **Výsledek ukončení**: Uzavření smlouvy ✓
- **Datum zrušení**: 0001-01-01T00:00:00

**RVZ2600001681**: Objednávka 1/2025 – dodávka obuvi pro HZS Zlínského kraje.

- **Druh**: Dodávky
- **Datum zahájení**: 2025-03-26T16:35:50
- **Datum ukončení**: 2025-06-16T09:08:57
- **Stav**: Ukončeno plnění smlouvy
- **Výsledek ukončení**: Uzavření smlouvy ✓
- **Datum zrušení**: 0001-01-01T00:00:00

