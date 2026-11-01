"""Kumulatives .apkg bauen (alle Kapitel mit cards/*.json, Status review/released; mit --all auch draft).
Stabile GUIDs -> erneuter Import aktualisiert Karten statt Duplikate. Aufruf: python3 tools/build.py [--all]"""
import sys, os, glob, html, hashlib
import genanki
from common import quiz, config, flags, flag_text, cards, P

chs, qs = quiz(); cfg = config(); fl = flags()
byid = {q['id']: q for q in qs}
IMG = P('..')
B = os.path.basename
def ipath(i): return i if i.startswith('img/') else 'img/' + i

CSS = """.card{font-family:-apple-system,Helvetica,Arial,sans-serif;font-size:19px;line-height:1.45;text-align:left;color:#1d1d1f;background:#fff;max-width:760px;margin:auto;padding:4px 10px}
.nightMode .card,.card.nightMode{color:#eee;background:#1e1e1e}
.stem{font-weight:600;margin-bottom:10px}.opts div{margin:5px 0}.opts b{display:inline-block;width:1.6em}
img{max-width:100%;border-radius:6px;margin:6px 0}
.ans{font-size:21px;font-weight:700;color:#1a7f37;margin:8px 0}.nightMode .ans{color:#5fd27a}
.expl{margin:8px 0}.dis div{margin:3px 0;font-size:16px;color:#555}.nightMode .dis div{color:#bbb}
.merk{background:#fff6d6;padding:6px 9px;border-radius:6px;margin:8px 0;font-size:16px}.nightMode .merk{background:#4a4120}
.flag{background:#fde2e1;padding:6px 9px;border-radius:6px;margin:8px 0;font-size:15px}.nightMode .flag{background:#5a2523}
.src{font-size:13px;color:#888;margin-top:10px}"""
FRONT = '<div class="stem">{{Frage}}</div>{{#Bild}}<div>{{Bild}}</div>{{/Bild}}<div class="opts">{{Optionen}}</div>'
BACK = ('{{FrontSide}}<hr id=answer><div class="ans">{{Antwort}}</div><div class="expl">{{Erklaerung}}</div>'
        '{{#Distraktoren}}<div class="dis">{{Distraktoren}}</div>{{/Distraktoren}}{{#Merkhilfe}}<div class="merk">💡 {{Merkhilfe}}</div>{{/Merkhilfe}}'
        '{{#Hinweis}}<div class="flag">⚠ {{Hinweis}}</div>{{/Hinweis}}<div class="src">{{Quelle}}</div>')
model = genanki.Model(cfg['model_id'], 'Situs Single Choice (Tamás)',
    fields=[{'name': n} for n in ['ID', 'Frage', 'Bild', 'Optionen', 'Antwort', 'Erklaerung', 'Distraktoren', 'Merkhilfe', 'Hinweis', 'Quelle']],
    templates=[{'name': 'SC', 'qfmt': FRONT, 'afmt': BACK}], css=CSS, sort_field_index=0)

e = html.escape
def opts_html(opts): return ''.join(f'<div><b>{k}</b>{e(t)}</div>' for k, t in opts)
def deck_id(name): return cfg['deck_id_base'] + int(hashlib.md5(name.encode()).hexdigest()[:6], 16)
def deck_name(ch_id, sub):
    c = chs[ch_id]; part = c['partTitle'].split('·')[0].strip()
    return f"{cfg['deck_root']}::{part} – {c['partTitle'].split('·')[1].strip()}::{c['title']}::{sub}"
def quelle(q): return f"Quelle: {chs[q['c']]['partTitle']} · {chs[q['c']]['title']} · Nr. {q['n']}"

include_draft = '--all' in sys.argv
decks = {}; media = set(); n_var = n_orig = 0
def deck(name):
    if name not in decks: decks[name] = genanki.Deck(deck_id(name), name)
    return decks[name]

for ch in cfg['order']:
    d = cards(ch)
    if d is None or (d.get('status', 'draft') == 'draft' and not include_draft): continue
    origs = [q for q in qs if q['c'] == ch]
    if cfg['include_originals']:
        for q in origs:
            img = ''.join(f'<img src="{B(i)}">' for i in q.get('img') or [])
            media.update(ipath(i) for i in q.get('img') or [])
            lsg = dict(q['o'])[q['a']]
            deck(deck_name(ch, 'Original')).add_note(genanki.Note(model=model, guid=genanki.guid_for('orig', q['id']),
                fields=[q['id'], e(q['q']), img, opts_html([(k.upper(), t) for k, t in q['o']]), f"{q['a'].upper()} – {e(lsg)}",
                        '', '', '', e(flag_text(q, fl)), quelle(q)], tags=['original', ch]))
            n_orig += 1
    for c in d['cards']:
        q = byid[c['src']]
        img = f'<img src="{B(c["img"])}">' if c.get('img') else ''
        if c.get('img'): media.add(ipath(c['img']))
        L = 'ABCDE'
        dis = ''.join(f'<div><b>{k}</b> {e(c["dis"][k])}</div>' for k in L if k in c['dis'])
        tags = ['variante', ch, 'typ::' + c['typ']] + (['prof'] if ch.startswith('D') else [])
        ft = flag_text(q, fl)
        if ft: tags.append('abklaeren')
        deck(deck_name(ch, 'Varianten')).add_note(genanki.Note(model=model, guid=genanki.guid_for('var', c['id']),
            fields=[c['id'], e(c['q']), img, opts_html(list(zip(L, c['o']))), f"{c['a']} – {e(c['o'][L.index(c['a'])])}",
                    e(c['expl']), dis, e(c.get('merk', '')), e(ft), quelle(q) + f" · Variante ({c['typ']})"], tags=tags))
        n_var += 1

os.makedirs(P('dist'), exist_ok=True)
out = P('dist', 'Situs-Anki.apkg')
pkg = genanki.Package(list(decks.values())); pkg.media_files = [os.path.join(IMG, m) for m in sorted(media)]
pkg.write_to_file(out)
print(f"{out}: {n_var} Varianten, {n_orig} Originale, {len(media)} Bilder, {len(decks)} Stapel")
