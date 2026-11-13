"""Build both hosts from one content source. No browser rendering is required."""
import argparse
import html
import json
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
ORIGIN = 'https://sandydcarter.com'
VERSION = 'edition-20261113'
EMAIL = 'rajan@houseofbrands.in'
PHONE = '917303681194'

def esc(value):
    return html.escape(str(value), quote=True)

def wa(message):
    return 'https://wa.me/' + PHONE + '?text=' + quote(message)

def link(path, label, cls='text-link'):
    return f'<a class="{cls}" href="/{path}">{label}<span aria-hidden="true">↗</span></a>'

def photo(name='navy', alt='Navy-dial watch campaign study on pale stone', eager=False):
    return f'<img src="/assets/editorial/{name}-1200.webp" srcset="/assets/editorial/{name}-640.webp 640w, /assets/editorial/{name}-1200.webp 1200w, /assets/editorial/{name}-1800.webp 1800w" sizes="(max-width: 700px) 100vw, 65vw" width="{1536 if name == "navy" else 1122}" height="{1024 if name == "navy" else 1402}" alt="{esc(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async" {"fetchpriority=high" if eager else ""}>'

NAV = [('shop.html','Watches'),('mens-watches.html','Men'),('womens-watches.html','Women'),('story-behind-the-brand/','Our story'),('journal.html','Journal')]

def header(path):
    items = ''.join(f'<a href="/{p}" {"aria-current=page" if path == p else ""}>{label}</a>' for p,label in NAV)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><a class="brand" href="/" aria-label="Sandy D. Carter home"><img src="/assets/brand/logo-black.png" width="2172" height="724" alt="Sandy D. Carter"></a><nav class="desktop-nav" aria-label="Main navigation">{items}</nav><a class="header-contact" href="/contact.html">Get in touch <span aria-hidden="true">↗</span></a><details class="mobile-menu"><summary aria-label="Navigation menu"><span>Menu</span><span class="menu-lines" aria-hidden="true"></span></summary><nav aria-label="Mobile navigation">{items}<a href="/contact.html">Get in touch</a></nav></details></header>'''

def footer():
    return '''<footer class="site-footer"><div class="footer-main"><a class="footer-logo" href="/" aria-label="Sandy D. Carter home"><img src="/assets/brand/logo-white.png" alt="Sandy D. Carter" width="2172" height="724"></a><div class="footer-links"><a href="/shop.html">The collection</a><a href="/story-behind-the-brand/">Our story</a><a href="/contact.html">Contact</a></div><div class="footer-links"><a href="https://www.instagram.com/sandydcarter/" target="_blank" rel="noopener noreferrer">Instagram ↗</a><a href="https://www.linkedin.com/company/13190990/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a><a href="/faqs.html">Questions & answers</a></div><p class="footer-signoff">Amsterdam inspiration.<br>Everyday perspective.</p></div><div class="footer-bottom"><span>© 2026 Sandy D. Carter</span><div><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a><a href="/shipping-returns.html">Delivery & returns</a></div></div></footer>'''

def contact_strip():
    return '<section class="contact-strip"><div><p class="eyebrow">The first collection</p><h2>Be part of what comes next.</h2></div>'+link('contact.html','Ask about the launch','button')+'</section>'

def frame(path, title, description, body, section='', canonical=None, noindex=False):
    url = ORIGIN + '/' + ('' if path == 'index.html' else path)
    if url.endswith('/index.html'):
        url=url[:-10]
    canon = ORIGIN + '/' + canonical if canonical else url
    graph = {'@context':'https://schema.org','@graph':[
        {'@type':'Brand','@id':ORIGIN+'/#brand','name':'SANDY D. CARTER','url':ORIGIN+'/', 'logo':ORIGIN+'/assets/brand/logo-black.png','sameAs':['https://www.instagram.com/sandydcarter/','https://www.linkedin.com/company/13190990/']},
        {'@type':'WebSite','@id':ORIGIN+'/#website','url':ORIGIN+'/','name':'SANDY D. CARTER','inLanguage':'en'},
        {'@type':'WebPage','@id':canon+'#webpage','url':canon,'name':title,'description':description,'isPartOf':{'@id':ORIGIN+'/#website'},'about':{'@id':ORIGIN+'/#brand'}}]}
    schema=json.dumps(graph, ensure_ascii=False).replace('<', chr(92)+'u003c')
    return f'''<!doctype html><html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(description)}"><meta name="theme-color" content="#f6f5f1"><link rel="canonical" href="{esc(canon)}">{'<meta name="robots" content="noindex,follow">' if noindex else ''}<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{esc(canon)}"><meta property="og:image" content="{ORIGIN}/assets/editorial/navy-1200.webp"><meta property="og:image:alt" content="Sandy D. Carter navy watch campaign study"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/assets/brand/logo-black.png"><link rel="preload" href="/assets/fonts/schibsted-400.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/edition.css?v={VERSION}"><script type="application/ld+json">{schema}</script><script defer src="/edition.js?v={VERSION}"></script></head><body class="{section}">{header(path)}<main id="main">{body}</main>{footer()}</body></html>'''

def home():
    return f'''<a class="announcement" href="/shop.html">Planned India debut · December 2026 · <span>Discover the collection story <span aria-hidden="true">↗</span></span></a>
<section class="home-hero"><div class="hero-copy"><p class="eyebrow">Sandy D. Carter / Watches</p><h1>Time, on<br>your terms.</h1><p>Clean lines. An easy presence.<br>Watches for the way you move.</p>{link('shop.html','Discover the collection','button')}<span class="hero-edition">01 — The first chapter</span></div><figure class="hero-image">{photo(eager=True)}<figcaption>Collection direction / December 2026</figcaption></figure></section>
<section class="intro"><p class="eyebrow">An everyday point of view</p><h2>Good design leaves<br>room for you.</h2><div><p>Inspired by Amsterdam and Scandinavian simplicity. A considered balance of shape, colour and detail.</p>{link('story-behind-the-brand/','Our story')}</div></section>
<section class="collection-edit"><div class="section-heading"><h2>Two perspectives.<br>One collection.</h2><span class="eyebrow">Launching December 2026</span></div><div class="edit-grid"><a class="edit-card" href="/mens-watches.html"><div class="image-wrap">{photo()}</div><div class="card-label"><div><span class="eyebrow">01 / For him</span><h3>A quieter statement.</h3></div><span aria-hidden="true">↗</span></div></a><a class="edit-card" href="/womens-watches.html"><div class="image-wrap">{photo('ivory','Ivory-dial watch campaign study on natural linen')}</div><div class="card-label"><div><span class="eyebrow">02 / For her</span><h3>Ease, in every detail.</h3></div><span aria-hidden="true">↗</span></div></a></div></section>
<section class="journal-home"><div><p class="eyebrow">The journal</p><h2>A closer look.</h2></div><div class="journal-lines"><a href="/watch-case-shapes-and-sizes.html"><span>01 / Proportion</span><h3>Finding your fit</h3><b aria-hidden="true">↗</b></a><a href="/metal-vs-leather-watch-straps.html"><span>02 / Materials</span><h3>Leather or metal?</h3><b aria-hidden="true">↗</b></a><a href="/how-to-style-a-watch-for-office-wear.html"><span>03 / Everyday</span><h3>From work to the weekend</h3><b aria-hidden="true">↗</b></a></div></section>{contact_strip()}'''

def collection(kind='all'):
    names={'all':('The first collection.','Watches','The debut collection arrives in India in December 2026, in partnership with Myntra.'),'men':('Less noise.<br>More character.','Watches for men','A restrained approach to everyday watches. Explore the men’s collection at the December launch.'),'women':('Your own<br>sense of time.','Watches for women','Simple forms, subtle details and room for individual style. Discover the women’s collection this December.'),'signature':('The essentials,<br>considered.','Signature collection','An introduction to the shapes and details that define Sandy D. Carter.')}
    title,label,intro=names[kind]
    banner = '<figure class="launch-banner" id="collection-story"><img src="/assets/campaigns/Banner.png" alt="Sandy D. Carter Amsterdam — launching soon in India in partnership with Myntra" width="1672" height="941" fetchpriority="high"></figure>' if kind=='all' else ''
    media = photo('ivory','Ivory watch campaign study on linen',True) if kind=='women' else photo(eager=True)
    return banner+f'''<section class="collection-head"><div><p class="eyebrow">{label}</p><h1>{title}</h1></div><div><p>{intro}</p>{link('contact.html','Enquire about the collection','button')}</div></section><nav class="collection-nav" aria-label="Collections"><a href="/shop.html" {'aria-current="page"' if kind=='all' else ''}>All watches</a><a href="/mens-watches.html" {'aria-current="page"' if kind=='men' else ''}>For him</a><a href="/womens-watches.html" {'aria-current="page"' if kind=='women' else ''}>For her</a><a href="/signature.html" {'aria-current="page"' if kind=='signature' else ''}>Signature</a></nav><section class="collection-feature"><figure>{media}<figcaption>Campaign imagery. Final models, prices and specifications will be shared at launch.</figcaption></figure><div class="collection-details"><p class="eyebrow">A first look</p><h2>Shape. Colour.<br>Just enough detail.</h2><p>Our starting point is an uncluttered dial, balanced proportions and a watch that feels at home in your day.</p><dl><div><dt>India debut</dt><dd>December 2026</dd></div><div><dt>Launch partner</dt><dd>Myntra</dd></div><div><dt>Availability</dt><dd>Collection reveal coming soon</dd></div></dl>{link('contact.html','Ask us a question')}</div></section>'''

def story():
    return f'''<section class="story-title"><p class="eyebrow">Our story / Amsterdam, 2011</p><h1>A shared eye.<br>An individual spirit.</h1><p>A watch should feel like part of your day.<br>That is where our design story begins.</p></section><section class="story-split"><figure>{photo('ivory','Ivory and brown watch campaign still life')}</figure><div><p class="eyebrow">The perspective</p><h2>Less to distract.<br>More to notice.</h2><p>Sandy D. Carter takes its inspiration from Amsterdam: the rhythm of its architecture, its independent spirit and an appreciation for useful, beautiful things.</p><p>Scandinavian minimalism informs the approach. Clear dials, measured proportions and a restrained palette leave space for the person wearing the watch.</p><p>Sandy and Carter express two sides of that perspective: imagination and precision. The letter D acknowledges Droog Amsterdam as a design influence, without implying a commercial affiliation.</p>{link('design-philosophy.html','Explore the design approach')}</div></section><section class="story-note"><p class="eyebrow">The next chapter / India</p><h2>A new place.<br>The same point of view.</h2><p>Developed in the Netherlands, the brand’s India debut is planned for December 2026 with Myntra. House Of Brands Fashion LLP is the global development and marketing partner.</p>{link('shop.html','Meet the collection')}</section>'''

def contact():
    message='Hello Sandy D. Carter, I would like to know more about the December 2026 watch launch.'
    return f'''<section class="page-title"><p class="eyebrow">Contact</p><h1>Let’s talk.</h1><p>Questions about the collection, retail partnerships or the launch?<br>Speak with the House Of Brands team.</p></section><section class="contact-layout"><div class="contact-direct"><p class="eyebrow">Direct enquiries</p><a class="contact-email" href="mailto:{EMAIL}?subject=Sandy%20D.%20Carter%20enquiry">{EMAIL}</a><a class="button" data-contact="whatsapp" href="{wa(message)}" target="_blank" rel="noopener noreferrer">Chat on WhatsApp <span aria-hidden="true">↗</span></a><a class="phone" href="tel:+{PHONE}">+91 73036 81194</a><p class="small">Brand enquiries are handled by House Of Brands Fashion LLP, India.</p></div><form class="enquiry-form" id="enquiry-form" hidden><h2>A little context helps.</h2><label>Your name<input name="name" autocomplete="name" required maxlength="100"></label><label>I’m interested in<select name="interest"><option>The December collection launch</option>Retail or distribution</option>Press and collaborations</option>A general question</option></select></label><label>Your message<textarea name="message" rows="4" required maxlength="2000"></textarea></label><div class="form-actions"><button class="button" type="submit" name="channel" value="whatsapp">Continue on WhatsApp <span aria-hidden="true">↗</span></button><button class="text-link" type="submit" name="channel" value="email">Use email instead ↗</button></div><p class="small">This opens a draft in WhatsApp or your email app. Press send there to contact us. Details are not stored by this form.</p><p class="form-status" role="status" aria-live="polite"></p></form><noscript><p>Please use the email or WhatsApp link above to contact us.</p></noscript></section>'''

def article(data):
    blocks=''.join(f'<section><h2>{esc(h)}</h2><p>{esc(p)}</p></section>' for h,p in data['sections'])
    related=''.join(link(p,l) for p,l in data.get('related',[('journal.html','More from the journal'),('shop.html','The collection')]))
    art=photo('ivory','Watch and linen campaign detail') if data.get('image')=='ivory' else photo()
    return f'''<section class="article-title"><a class="eyebrow" href="/{'journal.html' if data.get('group')=='Journal' else 'story-behind-the-brand/'}">{esc(data.get('group','Design notes'))}</a><h1>{esc(data['heading'])}</h1><p>{esc(data['intro'])}</p></section><div class="article-layout"><article class="article-body">{blocks}<nav class="related" aria-label="Read next">{related}</nav></article><aside class="article-aside"><figure>{art}<figcaption>Details from the campaign.</figcaption></figure><p class="eyebrow">The collection / December 2026</p>{link('contact.html','Ask about the launch')}</aside></div>'''

def journal(pages):
    cards=''.join(f'<a class="journal-entry" href="/{p}"><span class="eyebrow">{i:02d} / {esc(d.get("tag","Design"))}</span><h2>{esc(d["heading"])}</h2><p>{esc(d["intro"])}</p><span class="read-link">Read the story ↗</span></a>' for i,(p,d) in enumerate([(p,d) for p,d in pages.items() if d.get('group')=='Journal'],1))
    return '<section class="page-title"><p class="eyebrow">The journal</p><h1>Small details.<br>A different perspective.</h1><p>Notes on watches, personal style and taking care of the things you wear.</p></section><section class="journal-grid">'+cards+'</section>'

def faq():
    questions=[('When does the collection launch?','The India debut is planned for December 2026, in partnership with Myntra. Product listings and prices will be shared at launch.'),('Can I buy a watch now?','The site currently introduces the collection. Online purchasing is not yet available. Contact us with collection or availability questions.'),('What inspires the design?','Amsterdam is the starting point, with Scandinavian-inspired simplicity informing proportion, colour and detail.'),('Who can I contact?','Email rajan@houseofbrands.in or use the WhatsApp link on our contact page. House Of Brands Fashion LLP handles brand and partnership enquiries.'),('Where can I find product specifications?','Confirmed case sizes, materials, movement details and water-resistance ratings will accompany individual product listings at launch.'),('What are the delivery, returns and warranty terms?','These will be provided with the launch listings. Review the terms on the platform where you place your order.')]
    return '<section class="page-title"><p class="eyebrow">Questions & answers</p><h1>A few useful details.</h1></section><section class="faq-list">'+''.join(f'<details><summary>{esc(q)}<span aria-hidden="true">+</span></summary><p>{esc(a)}</p></details>' for q,a in questions)+'</section>'+contact_strip()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(ROOT.parent/'public'));parser.add_argument('--host',default='watches.sandydcarter.com');args=parser.parse_args()
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    pages=json.loads((ROOT/'pages.json').read_text())
    for asset in (ROOT/'assets').rglob('*'):
        if asset.is_file() and not asset.name.endswith(('-source.png','.ttf')):
            target=out/'assets'/asset.relative_to(ROOT/'assets');target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(asset,target)
    for file in ['edition.css','edition.js']:shutil.copy2(ROOT/file,out/file)
    special={
        'index.html':('SANDY D. CARTER | Watches for Your Everyday','Discover Sandy D. Carter: contemporary watches inspired by Amsterdam and Scandinavian simplicity. India debut, December 2026.',home(),'home'),
        'shop.html':('The Watch Collection | SANDY D. CARTER','Explore the Sandy D. Carter collection story. Our first watch collection launches in India in December 2026 with Myntra.',collection(),'collection'),
        'mens-watches.html':('Watches for Men | SANDY D. CARTER','Discover the direction of the Sandy D. Carter men’s watch collection. Clean dials and understated design, launching December 2026.',collection('men'),'collection'),
        'womens-watches.html':('Watches for Women | SANDY D. CARTER','Explore the Sandy D. Carter women’s watch collection preview. Simple forms and considered details, launching December 2026.',collection('women'),'collection'),
        'signature.html':('Signature Collection | SANDY D. CARTER','An introduction to Sandy D. Carter signature watch design: shape, proportion and a considered approach to everyday style.',collection('signature'),'collection'),
        'story-behind-the-brand/index.html':('Our Story | SANDY D. CARTER','The Amsterdam inspiration behind Sandy D. Carter. Discover a shared perspective on watch design, individuality and Scandinavian simplicity.',story(),'story'),
        'contact.html':('Contact the Team | SANDY D. CARTER','Contact the Sandy D. Carter team for collection, launch, retail, distribution and press enquiries. Email and WhatsApp contact details.',contact(),'contact'),
        'journal.html':('The Journal | SANDY D. CARTER','Practical notes on watch proportions, straps, movements, styling and care from Sandy D. Carter.',journal(pages),'journal'),
        'faqs.html':('Questions & Answers | SANDY D. CARTER','Answers about the Sandy D. Carter December 2026 India launch, collection availability, product information and contact details.',faq(),'faq'),
        '404.html':('Page Not Found | SANDY D. CARTER','Find the Sandy D. Carter collection, journal and contact details.', '<section class="page-title error-page"><p class="eyebrow">404</p><h1>A different direction.</h1><p>We couldn’t find that page. The collection is a good place to start.</p>'+link('shop.html','Explore the collection','button')+'</section>','error')}
    sitemap=[]
    for path,(title,desc,body,section) in special.items():
        target=out/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(frame(path,title,desc,body,section,noindex=path=='404.html'))
        if path!='404.html':sitemap.append('' if path=='index.html' else path.replace('/index.html','/'))
    for path,data in pages.items():
        canonical=data.get('canonical')
        target=out/path;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(frame(path,data['title'],data['description'],article(data),'article',canonical=canonical,noindex=data.get('noindex',False)))
        if not canonical and not data.get('noindex'):sitemap.append(path)
    # Existing story URL remains useful and shares the preferred story canonical.
    (out/'our-story.html').write_text(frame('our-story.html','Our Amsterdam Story | SANDY D. CARTER','Read the Amsterdam-inspired design story of Sandy D. Carter.',story(),'story',canonical='story-behind-the-brand/'))
    (out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}/{p}</loc></url>' for p in sitemap)+'</urlset>')
    (out/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
    (out/'llms.txt').write_text('# SANDY D. CARTER\n\nOfficial website: '+ORIGIN+'\nContemporary watch brand. Amsterdam inspiration and Scandinavian-inspired design. India debut planned for December 2026 with Myntra.\nContact: '+EMAIL+'\nCampaign previews are not final product specifications.\n')
    if args.host=='watches.sandydcarter.com':(out/'CNAME').write_text(args.host+'\n')
    elif (out/'CNAME').exists():(out/'CNAME').unlink()
    print(f'Built {len(special)+len(pages)+1} pages; {len(sitemap)} canonical sitemap entries in {out}')

if __name__=='__main__':main()
