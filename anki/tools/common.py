import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)

def load(path):
    with open(P(path), encoding='utf-8') as f:
        return json.load(f)

def quiz():
    d = load('source/quiz.json')
    ch = {c['id']: c for c in d['ch']}
    return ch, d['q']

def config():
    return load('config.json')

def flags():
    f = load('flags.json'); f.pop('_info', None); return f

def cards(ch_id):
    p = P('cards', f'{ch_id}.json')
    if not os.path.exists(p):
        return None
    return load(p)

def flag_text(q, fl):
    parts = []
    if q['id'] in fl: parts.append(fl[q['id']])
    if q.get('src') == 'korr' or q.get('notes'):
        parts += q.get('notes') or ['Lösung gegenüber der Vorlage korrigiert.']
    return ' '.join(parts)

def norm(s):
    return re.sub(r'[\s.\-()]+', ' ', s.lower()).strip()
