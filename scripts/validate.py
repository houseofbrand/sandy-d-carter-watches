"""Check publishable HTML, route coverage, assets and canonical consistency."""
import json
import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from xml.etree import ElementTree as ET

root=Path(sys.argv[1] if len(sys.argv)>1 else 'public').resolve()
errors=[]
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.tags=[]; self.ids=set(); self.feed(text)
    def handle_starttag(self,tag,attrs):
        d=dict(attrs);self.tags.append((tag,d))
        if 'id' in d:self.ids.add(d['id'])

files=list(root.rglob('*.html'))
pages={p.relative_to(root).as_posix():Page(p.read_text()) for p in files}
for path,page in pages.items():
    text=(root/path).read_text()
    def require(ok,message):
        if not ok:errors.append(path+': '+message)
    require(sum(t=='h1' for t,a in page.tags)==1,'requires exactly one H1 in raw HTML')
    require(any(t=='main' and a.get('id')=='main' for t,a in page.tags),'missing main landmark')
    canon=[a['href'] for t,a in page.tags if t=='link' and a.get('rel')=='canonical']
    require(len(canon)==1 and canon[0].startswith('https://sandydcarter.com/'),'incorrect canonical')
    if canon:
        target=canon[0].removeprefix('https://sandydcarter.com/');target=target+'index.html' if not target or target.endswith('/') else target
        require(target in pages,'canonical target missing')
    for schema in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S):
        try:json.loads(schema)
        except ValueError:require(False,'invalid JSON-LD')
    require('application/ld+json' in text,'missing structured data')
    require('name="description"' in text,'missing meta description')
    require(not any(x in text for x in ['Watches only · Pre-launch preview','The Founder Connection','November 2026','visual-story/','fonts.googleapis.com','enhancements.js']),'legacy content or asset present')
    for tag,attrs in page.tags:
        if tag=='img':
            require(bool(attrs.get('alt')),'image has no meaningful alt text')
            require('width' in attrs and 'height' in attrs,'image dimensions missing')
        if tag=='a' and attrs.get('target')=='_blank':require('noopener' in attrs.get('rel',''),'unsafe new tab')
        urls=[attrs[k] for k in ('href','src') if k in attrs]
        urls += [s.strip().split()[0] for s in attrs.get('srcset','').split(',') if s.strip()]
        for url in urls:
            parsed=urlsplit(url)
            if parsed.scheme or parsed.netloc:continue
            target=unquote(parsed.path.lstrip('/')) or path
            if target.endswith('/'):target+='index.html'
            if url=='/':target='index.html'
            require((root/target).is_file(),'missing internal target '+target)
            if parsed.fragment and target in pages:require(parsed.fragment in pages[target].ids,'missing fragment '+url)
    require(len([1 for t,a in page.tags if t=='script' and a.get('src')])==1,'unexpected executable script count')
    require('<header' in text and '<footer' in text,'shared layout missing')

sitemap=ET.parse(root/'sitemap.xml')
urls=[e.text for e in sitemap.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
if len(urls)!=len(set(urls)):errors.append('Duplicate sitemap entries')
for url in urls:
    path=url.removeprefix('https://sandydcarter.com/');path=path+'index.html' if not path or path.endswith('/') else path
    content=(root/path).read_text()
    if f'rel="canonical" href="{url}"' not in content or 'noindex' in content:errors.append('Sitemap noncanonical/noindex '+url)
shop=pages['shop.html'];main_start=next(i for i,(t,a) in enumerate(shop.tags) if t=='main')
first_image=next(a for t,a in shop.tags[main_start:] if t=='img')
if first_image.get('src')!='/assets/campaigns/Banner.png':errors.append('Supplied banner is not the first collection visual')
for old in ['styles.css','enhancements.js','site.js','refinement.js','brand-data.js','entity-seo.js']:
    if (root/old).exists():errors.append('Stale runtime remains: '+old)
if errors:
    print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(files)} static pages, all internal references, image dimensions, JSON-LD, canonical targets and {len(urls)} sitemap entries.')
