import re

with open("ict_zakazky_report.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Rozdělíme na řádky
lines = content.split('\n')

md_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Hlavní hlavička
    if i < 10 and '=' * 40 in line and i > 0:
        prev_line = lines[i-1].strip()
        if prev_line and not prev_line.startswith('='):
            md_lines.append(f"# {prev_line}\n")
            i += 1
            continue
    
    # Položka zakázky - hlavička s číslem
    if re.match(r'^\d+\.\s+', line):
        # Číslo a název zakázky
        md_lines.append(f"\n## {line.strip()}\n")
        i += 1
        # Přeskočíme separator
        if i < len(lines) and '=' * 40 in lines[i]:
            i += 1
        continue
    
    # Separator mezi položkami
    if '=' * 40 in line:
        i += 1
        continue
    
    # Sekce "Předmět zakázky"
    if line.strip() == "Předmět zakázky:":
        md_lines.append(f"\n**{line.strip()}**\n")
        i += 1
        # Přeskočíme separator
        if i < len(lines) and '-' * 40 in lines[i]:
            i += 1
        continue
    
    # Separator podtržítkem
    if '-' * 40 in line:
        i += 1
        continue
    
    # Metadata položky (Typ:, Evidence:, atd.)
    if ':' in line and any(line.startswith(x) for x in ['Typ:', 'Evidenční', 'Zadavatel:', 'Datum', 'Lhůta', 'Hodnota:', 'URL:']):
        md_lines.append(f"**{line.strip()}**  \n")
        i += 1
        continue
    
    # Prázdné řádky a ostatní
    if line.strip():
        md_lines.append(line + '\n')
    else:
        md_lines.append('\n')
    
    i += 1

# Uložíme
with open("ict_zakazky_report.md", "w", encoding="utf-8") as f:
    f.write(''.join(md_lines))

print("✓ Markdown soubor vytvořen: ict_zakazky_report.md")
