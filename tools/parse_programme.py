import re, html, json, sys
def txt(s):
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'</p>\s*<p[^>]*>', '\n\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s).replace('‍', '')
    return re.sub(r'[ \t]+', ' ', s).strip()
def parse(path):
    t = open(path, encoding='utf-8').read()
    items = t.split('class="collection_item_b2c w-dyn-item"')[1:]
    out = []
    for it in items:
        def one(cls):
            m = re.search(r'class="%s"[^>]*>(.*?)</div>' % re.escape(cls), it, re.S)
            return txt(m.group(1)) if m else ''
        cat = one('categorie')
        langs = [txt(x) for x in re.findall(r'class="level"[^>]*>(.*?)</div>', it, re.S)]
        title = one('card_title_b2c')
        sub = one('card-subtitle')
        hb = re.search(r'class="host-wrapper"(.*?)class="card-body"', it, re.S)
        hosts = [txt(x) for x in re.findall(r'class="text-block-\d+"[^>]*>(.*?)</div>', hb.group(1), re.S)] if hb else []
        hosts = [h for h in hosts if h]
        if not hosts and hb:
            hosts = [x for x in txt(hb.group(1).replace('</div>', '\n</div>')).split('\n') if x.strip()]
        m = re.search(r'class="rich-text-block w-richtext"[^>]*>(.*?)</div>', it, re.S)
        desc = txt(m.group(1)) if m else ''
        times = [txt(x) for x in re.findall(r'class="time_text-b2c"[^>]*>(.*?)</div>', it, re.S)]
        stage = txt(re.search(r'fs-list-field="stage"[^>]*>(.*?)</div>', it, re.S).group(1)) if 'fs-list-field="stage"' in it else ''
        out.append(dict(cat=cat, langs=langs, title=title, sub=sub, hosts=hosts, desc=desc, times=times, stage=stage))
    return out
json.dump({'sat': parse(sys.argv[1]), 'sun': parse(sys.argv[2])}, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
