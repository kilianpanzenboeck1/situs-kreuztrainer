"""Arbeitspaket für ein Kapitel erzeugen: work/<CH>.md (Originalfragen kompakt, in Batches).
Aufruf: python3 tools/prepare.py D1"""
import sys
from common import quiz, config, flags, flag_text, P

ch_id = sys.argv[1]
chs, qs = quiz(); cfg = config(); fl = flags()
from common import dupes
DU = dupes(); items = [q for q in qs if q['c'] == ch_id and q['id'] not in DU]
bs = cfg['batch_size_originals']
out = [f"# {chs[ch_id]['partTitle']} – {chs[ch_id]['title']} ({len(items)} Originalfragen, Ziel {len(items)*cfg['variants_per_question']} Varianten)\n",
       f"Varianten-IDs: V-<src>-1, V-<src>-2 … · Stil: STYLE.md · Ausgabe: cards/{ch_id}.json\n"]
for i, q in enumerate(items):
    if i % bs == 0:
        out.append(f"\n## Batch {i//bs+1}\n")
    lsg = dict(q['o']).get(q['a'], '?') if q['a'] else '— keine Lösung in der Vorlage —'
    out.append(f"### {q['id']}  (Nr. {q['n']}){'  [BILD ' + ','.join(q['img']) + ']' if q.get('img') else ''}")
    out.append(q['q'])
    for k, t in q['o']:
        out.append(f"- {k.upper()}{'*' if q['a'] and k == q['a'] else ''} {t}")
    out.append(f"Lösung: {(q['a'] or '?').upper()} – {lsg}")
    ft = flag_text(q, fl)
    if ft: out.append(f"⚠ {ft}")
    out.append('')
open(P('work', f'{ch_id}.md'), 'w', encoding='utf-8').write('\n'.join(out))
print(f"work/{ch_id}.md: {len(items)} Fragen, {(len(items)+bs-1)//bs} Batches")
