"""Batch-Datei (JSON-Liste von Karten) in cards/<CH>.json übernehmen; gleiche IDs werden ersetzt.
Aufruf: python3 tools/append.py <CH> work/<batch>.json"""
import sys, json, os
from common import P
ch, src = sys.argv[1], sys.argv[2]
p = P('cards', f'{ch}.json')
d = json.load(open(p)) if os.path.exists(p) else {'chapter': ch, 'status': 'draft', 'cards': []}
new = json.load(open(src)); ids = {c['id'] for c in new}
d['cards'] = [c for c in d['cards'] if c['id'] not in ids] + new
json.dump(d, open(p, 'w'), ensure_ascii=False, indent=1)
print(f"{ch}: +{len(new)} → {len(d['cards'])} Karten")
