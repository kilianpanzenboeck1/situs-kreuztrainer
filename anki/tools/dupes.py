"""Findet Originalfragen in B/C, die eine frühere Frage (Reihenfolge laut config) mit gleicher Lösung wiederholen.
Schreibt dupes.json {id: abdeckende_id}. Diese Originale bekommen keine eigenen Varianten
(ihre Varianten existieren schon beim abdeckenden Original). Aufruf: python3 tools/dupes.py"""
import json
from common import quiz, config, norm, P
chs, qs = quiz(); cfg = config()
rank = {c: i for i, c in enumerate(cfg['order'])}
qs = sorted(qs, key=lambda q: (rank.get(q['c'], 99), q['n']))
key = lambda q: (norm(q['q'])[:80], norm(dict(q['o']).get(q['a'], '')) if q['a'] else None)
seen, dup = {}, {}
for q in qs:
    k = key(q)
    if k[1] is not None and k in seen and q['c'][0] in 'BC':
        dup[q['id']] = seen[k]
    else:
        seen.setdefault(k, q['id'])
json.dump(dup, open(P('dupes.json'), 'w'), ensure_ascii=False, indent=1)
import collections; print(len(dup), 'Dubletten', dict(collections.Counter(next(x['c'] for x in qs if x['id']==i) for i in dup)))
