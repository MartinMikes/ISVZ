# NUTS → Kraj - Regionální číselník

## 📍 Přehled

Číselník pro mapování NUTS kódů na názvy krajů ČR, používaný pro regionální filtrování veřejných zakázek.

## 🗺️ Mapování NUTS 3 (kraje)

| NUTS | Kraj | Region soudr. | Poznámka |
|------|------|---------------|----------|
| CZ010 | Hlavní město Praha | Praha | Hl. město Praha |
| CZ020 | Středočeský kraj | Střední Čechy | - |
| CZ031 | Jihočeský kraj | Jihozápad | - |
| CZ032 | Plzeňský kraj | Jihozápad | - |
| CZ041 | Karlovarský kraj | Severozápad | - |
| CZ042 | Ústecký kraj | Severozápad | - |
| CZ051 | Liberecký kraj | Severovýchod | - |
| CZ052 | Královéhradecký kraj | Severovýchod | - |
| CZ053 | Pardubický kraj | Severovýchod | - |
| CZ063 | Kraj Vysočina | Jihovýchod | - |
| CZ064 | Jihomoravský kraj | Jihovýchod | Brno |
| CZ071 | Olomoucký kraj | Střední Morava | - |
| CZ072 | Zlínský kraj | Střední Morava | - |
| CZ080 | Moravskoslezský kraj | Moravskoslezsko | Ostrava |

**Celkem**: 14 krajů (NUTS 3)

## 📋 Hierarchie NUTS

```
CZ (ČR)
├── NUTS 1: CZ0 (celá ČR)
├── NUTS 2: 8 regionů soudržnosti (CZ01-CZ08)
└── NUTS 3: 14 krajů (CZ010-CZ080)
```

## 📊 Použití v projektu

### Soubor číselníku

**Umístění**: `data/nuts_kraje.json`

**Struktura**:
```json
{
  "metadata": {
    "description": "Číselník NUTS → Kraj pro ČR",
    "source": "https://portal.uur.cz/...",
    "created": "2026-02-07",
    "version": "1.0"
  },
  "nuts_kraje": {
    "CZ010": "Hlavní město Praha",
    "CZ020": "Středočeský kraj",
    ...
  },
  "nuts_regiony": {
    "CZ01": "Praha",
    "CZ02": "Střední Čechy",
    ...
  }
}
```

### Automatické doplňování

Při generování reportů (`scripts/generate_reports.py`):

1. **Načtení**: Číselník se načte při startu skriptu
2. **Mapování**: Funkce `get_kraj_from_nuts()` převede NUTS → Kraj
3. **Doplnění**: Kraj se přidá do všech výstupních formátů:
   - MD reporty (detailní): sekce "📍 Místo plnění"
   - MD reporty (tabulkové): sloupec "Kraj"
   - CSV soubory: sloupec "Kraj" (pozice 17/18)

### Příklad použití

**Vstup (z JSON zakázky)**:
```json
{
  "mista_plneni": [
    {
      "nuts": "CZ064",
      "dalsi_informace_o_miste_plneni": "Brno"
    }
  ]
}
```

**Výstup (v reportech)**:
- NUTS: `CZ064`
- Kraj: `Jihomoravský kraj`
- Místo: `Brno`

## 📈 Statistiky ICT zakázek (leden 2026)

Rozložení 152 ICT zakázek podle krajů:

| Pořadí | Kraj | Počet | Podíl |
|--------|------|-------|-------|
| 1. | Hlavní město Praha | 60 | 39.5% |
| 2. | Jihomoravský kraj | 17 | 11.2% |
| 3. | Moravskoslezský kraj | 9 | 5.9% |
| 4. | Středočeský kraj | 8 | 5.3% |
| 5. | Ústecký kraj | 7 | 4.6% |
| 6. | Karlovarský kraj | 6 | 3.9% |
| 7. | Olomoucký kraj | 6 | 3.9% |
| 8. | Královéhradecký kraj | 5 | 3.3% |
| 9. | Pardubický kraj | 5 | 3.3% |
| 10. | Zlínský kraj | 5 | 3.3% |
| 11. | Liberecký kraj | 4 | 2.6% |
| 12. | Plzeňský kraj | 3 | 2.0% |
| 13. | Kraj Vysočina | 2 | 1.3% |
| 14. | Jihočeský kraj | 1 | 0.7% |
| - | Neuvedeno | 14 | 9.2% |

**Poznámky**:
- Praha dominuje s téměř 40% ICT zakázek
- Jihomoravský kraj (Brno) je druhý s 11%
- 14 zakázek nemá vyplněný NUTS kód

## 🔍 Filtrování v Excelu

### Postup

1. Otevřít CSV soubor: `output/csv/2026/01/VZ-ICT_2026-01.csv`
2. Data → Filtr (nebo Ctrl+Shift+L)
3. Kliknout na šipku u sloupce "Kraj"
4. Vybrat kraje, které chcete zobrazit

### Příklady filtrů

**Pouze Praha**:
- Zaškrtnout pouze "Hlavní město Praha"
- Výsledek: 60 zakázek

**Morava (JMK + MSK + OLK + ZLK)**:
- Zaškrtnout: Jihomoravský, Moravskoslezský, Olomoucký, Zlínský
- Výsledek: 37 zakázek

**Bez Prahy**:
- Zrušit zaškrtnutí u "Hlavní město Praha"
- Výsledek: 92 zakázek

## 📚 Zdroje

- **Oficiální zdroj**: [Úřad pro územní rozvoj - NUTS](https://portal.uur.cz/spravni-usporadani-cr-organy-uzemniho-planovani/nuts.asp)
- **ČSÚ**: [Klasifikace CZ-NUTS](https://www.czso.cz/csu/czso/3_klasifikace_cz_nuts_nuts_2004)
- **Wikipedia**: [CZ-NUTS](https://cs.wikipedia.org/wiki/CZ-NUTS)

## ⚠️ Údržba

**Číselník není nutné měsíčně aktualizovat** - NUTS klasifikace se mění jen výjimečně (obvykle při změně administrativního členění ČR).

Poslední aktualizace NUTS 3 pro ČR byla v roce 2018 (změna označení).

**Kontrola aktuálnosti**: Pokud ČSÚ nebo Eurostat publikuje změny v klasifikaci CZ-NUTS, aktualizovat soubor `data/nuts_kraje.json`.
