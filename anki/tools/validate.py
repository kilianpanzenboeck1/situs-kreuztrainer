"""Formale Prüfung der Variantenkarten. Aufruf: python3 tools/validate.py [CH ...]  (ohne Argument: alle vorhandenen)
cards/<CH>.json Format:
{"chapter": "D1", "status": "draft|review|released", "cards": [
  {"id": "V-SD1-1-1", "src": "SD1-1", "typ": "umkehrung", "q": "Stamm", "o": ["A..","B..","C..","D..","E.."],
   "a": "C", "expl": "2-4 Sätze", "dis": {"A": "warum falsch", "B": "...", "D": "...", "E": "..."},
   "merk": "optional", "img": "img/i12.jpg (Pfad wie in quiz.json) oder null"}]}"""
import sys, os, glob, collections
from common import dupes, quiz, config, cards, norm, P

TYPES = {'umkehrung', 'perspektive', 'nachbarschaft', 'klinik', 'bild'}
chs, qs = quiz(); cfg = config()
byid = {q['id']: q for q in qs}
targets = sys.argv[1:] or sorted(os.path.basename(p)[:-5] for p in glob.glob(P('cards', '*.json')))
errors = 0; seen = set()
for ch in targets:
    d = cards(ch)
    if d is None:
        print(f"{ch}: keine cards/{ch}.json"); continue
    per_src = collections.Counter(); types = collections.Counter(); ans = collections.Counter()
    for c in d['cards']:
        e = []
        cid = c.get('id', '?')
        if cid in seen: e.append('ID doppelt')
        seen.add(cid)
        if c.get('src') not in byid: e.append(f"src {c.get('src')} unbekannt")
        elif byid[c['src']]['c'] != ch: e.append('src gehört zu anderem Kapitel')
        if c.get('typ') not in TYPES: e.append(f"typ {c.get('typ')}")
        o = c.get('o', [])
        if len(o) != 5: e.append(f"{len(o)} Optionen")
        if len({norm(x) for x in o}) != len(o): e.append('doppelte Option')
        if c.get('a') not in list('ABCDE'): e.append('a nicht A–E')
        if not c.get('q', '').strip(): e.append('Stamm leer')
        if len(c.get('expl', '')) < 40: e.append('Erklärung zu kurz')
        wrong = set('ABCDE') - {c.get('a')}
        if set(c.get('dis', {})) != wrong: e.append(f"dis-Schlüssel {sorted(c.get('dis', {}))} ≠ {sorted(wrong)}")
        if c.get('img') and not os.path.exists(P('..', c['img'] if c['img'].startswith('img/') else 'img/' + c['img'])): e.append(f"Bild {c['img']} fehlt")
        if c.get('typ') == 'bild' and not c.get('img'): e.append('typ bild ohne img')
        if e:
            errors += len(e); print(f"  ✗ {cid}: {'; '.join(e)}")
        per_src[c.get('src')] += 1; types[c.get('typ')] += 1; ans[c.get('a')] += 1
    DU = dupes(); orig = [q['id'] for q in qs if q['c'] == ch and q['id'] not in DU]
    missing = [s for s in orig if per_src[s] < cfg['variants_per_question']]
    print(f"{ch} [{d.get('status','draft')}]: {len(d['cards'])} Karten · {len(orig)-len(missing)}/{len(orig)} Originale abgedeckt · Typen {dict(types)} · Lösungen {dict(sorted(ans.items()))}")
    if missing: print(f"  offen: {', '.join(missing)}")
print('OK' if errors == 0 else f'{errors} Fehler')
sys.exit(1 if errors else 0)
