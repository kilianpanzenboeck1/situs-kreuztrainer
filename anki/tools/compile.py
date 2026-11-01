"""Kompaktes Batch-Format in Kartenformat umwandeln.
Eingabe: JSON-Liste mit {"id","src","typ","q","right","wrong":[[Text, warum falsch] x4],"expl","merk","img","pos":"A-E"}
pos fehlt -> wird reihum A..E verteilt. Aufruf: python3 tools/compile.py work/X.src.json work/X.json"""
import sys, json
src, out = sys.argv[1], sys.argv[2]
L = 'ABCDE'; res = []
for i, c in enumerate(json.load(open(src))):
    pos = c.get('pos') or L[i % 5]; k = L.index(pos)
    wrong = c['wrong']; assert len(wrong) == 4, c['id']
    opts = [w[0] for w in wrong]; opts.insert(k, c['right'])
    dis = {}; wi = 0
    for j, l in enumerate(L):
        if j == k: continue
        dis[l] = wrong[wi][1]; wi += 1
    res.append({'id': c['id'], 'src': c['src'], 'typ': c['typ'], 'q': c['q'], 'o': opts, 'a': pos,
                'expl': c['expl'], 'dis': dis, 'merk': c.get('merk', ''), 'img': c.get('img')})
json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1)
print(f"{out}: {len(res)} Karten")
