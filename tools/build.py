#!/usr/bin/env python3
"""Fill src/template.html with the programme data and write index.html.
Update the programme:
  curl -sL https://www.gamesground.de/programme/saturday -o /tmp/sat.html
  curl -sL https://www.gamesground.de/programme/sunday -o /tmp/sun.html
  python3 tools/parse_programme.py /tmp/sat.html /tmp/sun.html /tmp/raw.json
  python3 tools/build_data.py /tmp/raw.json data/programme.json
  python3 tools/build.py"""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root / 'data/programme.json').read_text(encoding='utf-8'))
blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
page = (root / 'src/template.html').read_text(encoding='utf-8').replace('__DATA__', blob)
(root / 'index.html').write_text(page, encoding='utf-8')
print('index.html:', len(data['sessions']), 'sessions')
