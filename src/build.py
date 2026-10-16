#!/usr/bin/env python3
"""Build presentation.html (standalone) and orgscope-classic.html (artifact fragment) from src/classic.html.

Screens are embedded as base64 from the folder given as the first argument (files <name>.b64).
Run from the presentation folder:  python3 src/build.py /path/to/deckimg
"""
import os
import sys

IMG = sys.argv[1]
SRC = os.path.join(os.path.dirname(__file__), 'classic.html')
PLACEHOLDERS = [('__UPLOAD__', 'upload'), ('__UNITS__', 'units'), ('__KPI__', 'kpi-tiles'), ('__CLAUSE__', 'clause'),
                ('__DUPS__', 'dups'), ('__REGFN__', 'reg-fn'), ('__REGNORM__', 'reg-norm')]
HEAD = '''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="OrgScope · Demo Day presentation · HackAlem AI 2026, task 1">
<meta name="robots" content="noindex">
<style>[hidden]{display:none!important}</style>
'''

frag = open(SRC, encoding='utf8').read()
for ph, name in PLACEHOLDERS:
    with open(os.path.join(IMG, name + '.b64')) as f:
        b64 = f.read().strip()
    assert ph in frag, ph
    frag = frag.replace(ph, 'data:image/png;base64,' + b64)
open('orgscope-classic.html', 'w', encoding='utf8').write(frag)
i = frag.index('</style>') + len('</style>')
open('presentation.html', 'w', encoding='utf8').write(HEAD + frag[:i] + '\n</head>\n<body>\n' + frag[i:] + '\n</body>\n</html>\n')
print('built presentation.html', os.path.getsize('presentation.html'), 'bytes')
