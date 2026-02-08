import json

with open("isvz_data/DNS-01-2026.json", "r", encoding="utf-8") as f:
    data = json.load(f)

item = data["data"][0]
print("Struktura první položky:")
print(json.dumps(item, ensure_ascii=False, indent=2)[:2000])
