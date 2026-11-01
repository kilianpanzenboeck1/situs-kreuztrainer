"""Prüft, ob Varianten-Stämme eines Kapitels schon in anderen Kapiteln vorkommen. Aufruf: python3 tools/stemdup.py CH"""
import sys, glob, json, os
from common import norm, P
ch = sys.argv[1]
other = {}
for f in glob.glob(P('cards', '*.json')):
    c = os.path.basename(f)[:-5]
    if c == ch: continue
    for k in json.load(open(f))['cards']:
        other[norm(k['q'])] = (c, k['id'], k['o'][ord(k['a'])-65])
for k in json.load(open(P('cards', ch + '.json')))['cards']:
    n = norm(k['q'])
    if n in other: print(k['id'], '≈', other[n])
