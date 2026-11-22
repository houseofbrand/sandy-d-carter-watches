"""Restore the established visual design and apply copy-only editorial changes."""
import argparse,re,shutil
from copy_edit import edit
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT.parent/'public'));p.add_argument('--host',default='watches.sandydcarter.com');a=p.parse_args();out=Path(a.output)
shutil.copytree(ROOT/'classic/public',out,dirs_exist_ok=True)
shutil.copy2(ROOT/'assets/brand/official-logo.png',out/'assets/brand/official-logo.png')
shutil.copy2(ROOT/'product-data.json',out/'product-data.json')
replacements={
'Scandinavian-inspired minimalism, balanced proportions and contemporary quartz timepieces for men and women. In global alliance with House Of Brands Fashion LLP, India.':'Clean dials, balanced proportions and quartz watches for men and women.',
'Two designer personalities. One shared perspective. A watch-design journey that began in Amsterdam in 2011, shaped by a belief in simplicity, thoughtful detailing and timeless design.':'Our story began in Amsterdam in 2011, with Sandy and Carter’s shared interest in simple forms and thoughtful details.',
'A watch develops through a sequence of deliberate decisions. This visual pathway describes the design and product-development process; it does not identify a factory or claim European or Swiss manufacture.':'From the first outline to the finished form, each stage brings proportion, materials and function into focus.',
'Inspired by Amsterdam and shaped by a philosophy of simplicity, balanced proportions and thoughtful detailing, the collection represents the next chapter of a design journey that began in 2011.':'Explore the shapes, colours and details behind our first collection.',
'Collection reveal and launch updates coming soon. Until a verified subscription service is available, follow the official website and social profiles for confirmed news.':'Follow the collection’s progress, design stories and December launch news.',
'An expression of considered design is taking shape.':'A first look at what comes next.',
'Premium lifestyle watches · Developed in the Netherlands':'SANDY D. CARTER · Amsterdam',
'AMSTERDAM-INSPIRED WATCH DESIGN':'TIME. REFINED.',
'Something timeless is taking shape. Our first collection is planned for December 2026.':'The first collection arrives in India in December 2026.',
'Two Designers.<br>One Shared Perspective.':'Two perspectives.<br>One shared vision.',
'SANDY D. CARTER is an emerging premium lifestyle watch brand developed in the Netherlands and inspired by Amsterdam and European design aesthetics. The brand brings together Scandinavian-inspired minimalism, considered detailing and contemporary quartz timepieces for men and women.':'SANDY D. CARTER is a contemporary watch brand developed in the Netherlands, inspired by Amsterdam and the principles of refined European design. Every collection reflects an appreciation for simplicity, balance, character and detail.',
'"slogan":"Two Designers. One Shared Perspective."':'"slogan":"TIME. REFINED."',
}
for f in out.rglob('*.html'):
 s=f.read_text()
 for before,after in replacements.items():s=s.replace(before,after)
 s=re.sub(r'<script src="[^"]+"[^>]*></script>','',s)
 s=s.replace('</body>','<script src="classic-interactions.js?v=20261113-mobile"></script></body>')
 s=s.replace('</head>','<style>.reveal{opacity:1!important;transform:none!important}@media(max-width:600px){.world-hero-copy h1{font-size:clamp(36px,9vw,56px)!important;overflow-wrap:normal}.world-hero-copy{max-width:100%}img{max-width:100%}}</style></head>')
 s=s.replace('https://watches.sandydcarter.com','https://sandydcarter.com')
 s=s.replace('shop.html#collection-story','shop.html')
 s=s.replace('sandy-d-carter-logo-black-transparent-v2.png','official-logo.png')
 s=s.replace('sandy-d-carter-logo-white-transparent-v2.png','official-logo.png')
 # Prefer the matched campaign variants in which only the separate dial marking
 # has been removed. The studio scene has no watch and therefore no variant.
 s=re.sub(r'([0-9]{2}-[a-z0-9-]+)-amsterdam-v2\.jpg',lambda m:(m.group(1)+'-branded-web.jpg') if (out/'assets/visual-story'/(m.group(1)+'-branded-web.jpg')).exists() else m.group(0),s)
 # Preserve the original page composition, not the repeated production caveats.
 s=re.sub(r'<figcaption>Conceptual illustration[^<]*</figcaption>','<figcaption>Collection design study</figcaption>',s)
 s=edit(s,f.relative_to(out).as_posix())
 f.write_text('\n'.join(line.rstrip() for line in s.splitlines())+'\n')
shutil.copy2(ROOT/'copy-edit.css',out/'copy-edit.css')
shutil.copy2(ROOT/'classic-interactions.js',out/'classic-interactions.js')
for name in ['sitemap.xml','robots.txt','llms.txt']:
 f=out/name
 if f.exists():f.write_text(f.read_text().replace('https://watches.sandydcarter.com','https://sandydcarter.com'))
if a.host=='watches.sandydcarter.com':(out/'CNAME').write_text(a.host+'\n')
elif (out/'CNAME').exists():(out/'CNAME').unlink()
print('Restored original design across',len(list(out.rglob('*.html'))),'pages')
