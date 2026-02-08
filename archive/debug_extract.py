import json

def get_all_strings(obj, depth=0, max_depth=10):
    """Rekurzivně získá všechny stringy z objektu"""
    strings = []
    
    if depth > max_depth:
        return strings
    
    if isinstance(obj, str) and len(obj) > 3:  # Ignoruj krátké stringy
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

print("První položka - všechny stringy:")
strings = get_all_strings(data["data"][0])
print(f"Nalezeno {len(strings)} stringů")
print("\nPrvních 10:")
for s in strings[:10]:
    print(f"  - {s[:100]}")
