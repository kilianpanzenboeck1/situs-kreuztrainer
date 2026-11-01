"""Fortschritt anzeigen und STATUS.md neu schreiben. Aufruf: python3 tools/status.py"""
import collections
from common import quiz, config, cards, P

chs, qs = quiz(); cfg = config()
cnt = collections.Counter(q['c'] for q in qs)
lines = ['# Situs-Anki – Fortschritt', '', '(automatisch erzeugt von tools/status.py)', '']
nxt = None
for st in cfg['stages']:
    lines.append(f"## {st['name']}")
    for ch in st['chapters']:
        d = cards(ch); goal = cnt[ch] * cfg['variants_per_question']
        n = len(d['cards']) if d else 0; s = d.get('status', 'draft') if d else 'offen'
        if nxt is None and s != 'released': nxt = ch
        lines.append(f"- [{'x' if s == 'released' else ' '}] {ch} {chs[ch]['title']} – {n}/{goal} Karten – {s}")
    lines.append('')
lines.append(f"**Nächstes Kapitel:** {nxt or '— alles fertig —'}")
open(P('STATUS.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
