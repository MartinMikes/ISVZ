import json

def get_all_strings(obj, depth=0, max_depth=10):
    strings = []
    if depth > max_depth:
        return strings
    if isinstance(obj, str) and len(obj) > 3:
        strings.append(obj)
    elif isinstance(obj, dict):
        for value in obj.values():
            strings.extend(get_all_strings(value, depth + 1, max_depth))
    elif isinstance(obj, list):
        for item in obj:
            strings.extend(get_all_strings(item, depth + 1, max_depth))
    return strings

with open("isvz_data/DNS-01-2026.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Hledám ICT klíčová slova ve všech položkách:")
ict_keywords = ['software', 'aplikace', 'web', 'it ', 'ict', 'systém', 'databáz', 'program']

for idx, item in enumerate(data["data"]):
    strings = get_all_strings(item)
    full_text = " ".join(strings).lower()
    
    for keyword in ict_keywords:
        if keyword in full_text:
            print(f"\n✓ Položka {idx+1} obsahuje '{keyword}'")
            # Vypíšeme relevantní stringy
            relevant = [s for s in strings if len(s) > 15 and not s.startswith('20') and not s.startswith('RVZ')]
            print(f"  Klíčové texty: {relevant[:5]}")
            break

print("\nCelkem položek:", len(data["data"]))
