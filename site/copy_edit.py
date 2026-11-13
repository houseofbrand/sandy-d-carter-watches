"""Editorial copy pass; keep established page wrappers, imagery and navigation."""
import json,re
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).parent
PAGES=json.loads((ROOT/'pages.json').read_text())
EXTRA={
'shop.html':dict(heading='The first collection.',intro='A first look at Sandy D. Carter watches. Arriving in India this December.',sections=[['A watch for your everyday','Clear dials, balanced cases and a palette that works with the things you already wear. The collection brings an Amsterdam perspective to familiar watch forms.'],['Find your perspective','Explore the men’s, women’s and signature collections below. Individual models, prices and specifications will be shared at launch.']]),
'mens-watches.html':dict(heading='A quieter statement.',intro='Watches for men, with clean lines and an easy presence.',sections=[['Proportion, not excess','The width of a bezel, the space around a marker and the curve of a lug shape how a watch feels on the wrist. Our starting point is a composition that feels balanced as a whole.'],['From work to the weekend','A restrained dial leaves room for personal style. Pair it with a crisp cuff, a favourite knit or a well-worn jacket.'],['The first collection','The men’s range joins the India debut in December 2026. Model details and availability will be shared with the launch listings.']]),
'womens-watches.html':dict(heading='Your own sense of time.',intro='Watches for women, shaped by subtle details and individual style.',sections=[['A personal balance','A softer tone, a slim marker or a contrast of finishes can change the character of a familiar shape. Choose the expression that feels natural to you.'],['Wear it your way','Alongside jewellery or on its own, a watch becomes part of your routine. Comfort and proportion matter as much as its first impression.'],['The first collection','The women’s range joins the India debut in December 2026. Model details and availability will be shared with the launch listings.']]),
'signature.html':dict(heading='The essentials, considered.',intro='The details that make a Sandy D. Carter watch recognisable.',sections=[['A clear composition','An open dial, measured markers and a case that frames rather than crowds. The signature direction brings these elements together.'],['Character in the details','Subtle contrasts of colour and texture give each design its own presence. The complete range will be revealed with the December collection.']]),
'story-behind-the-brand/index.html':dict(heading='A shared eye for design.',intro='Amsterdam, 2011. The starting point for Sandy D. Carter.',sections=[['Two perspectives','Sandy and Carter embody complementary creative perspectives: imagination and precision. Their shared language is built around simple forms, practical details and individuality.'],['The meaning of D','The letter D acknowledges Droog Amsterdam as a design influence. It is an inspiration reference, without a commercial affiliation.'],['An international outlook','Developed in the Netherlands, the brand draws on Amsterdam’s independent spirit and Scandinavian minimalism. House Of Brands Fashion LLP is its global development and marketing partner.'],['The India chapter','The collection makes its planned India debut in December 2026, in partnership with Myntra.']]),
'contact.html':dict(heading='Start a conversation.',intro='Collection questions, retail partnerships and press enquiries.',sections=[['Speak with the team','Brand enquiries are handled by House Of Brands Fashion LLP. Email rajan@houseofbrands.in or contact us on WhatsApp at +91 73036 81194.']]),
}

def edit(text,path):
 soup=BeautifulSoup(text,'html.parser');data=EXTRA.get(path) or PAGES.get(path)
 if data:
  hero=soup.select_one('.page-hero-inner, .static-page-hero')
  if hero:
   h=hero.find('h1')
   if h:h.clear();h.append(data['heading'])
   ps=hero.find_all('p',recursive=False)
   if ps:ps[-1].clear();ps[-1].append(data['intro'])
  prose=soup.select_one('.prose')
  if prose:
   for child in list(prose.children):
    if getattr(child,'name',None) in ['p','h2','h3','ul','ol']:child.decompose()
   for block in prose.select('.coming-soon-panel,.droog-reference,.studio-card'):block.decompose()
   fragment=''.join('<section class="edited-copy"><h2>'+h+'</h2><p>'+p+'</p></section>' for h,p in data['sections'])
   prose.insert(0,BeautifulSoup(fragment,'html.parser'))
   if path=='contact.html':
    prose.append(BeautifulSoup('<div class="contact-actions"><a class="button button-dark" href="mailto:rajan@houseofbrands.in">Email the team</a><a class="text-link" href="https://wa.me/917303681194" target="_blank" rel="noopener noreferrer">Chat on WhatsApp ↗</a></div>','html.parser'))
 if path=='index.html':
  edits={
   '.creative-copy p:not(.eyebrow)':'Sandy brings imagination. Carter brings precision. Together, they shape a watch collection with a clear point of view.',
   '.mosaic-title p:not(.eyebrow)':'The rhythm of Amsterdam’s façades. The contrast of old and new. Everyday surroundings, seen with a designer’s eye.',
   '.archive-head > p':'Explore how marker spacing, case shape and material choices change the character of a watch.',
   '.craft-copy p:not(.eyebrow)':'An outline becomes a dial. A dial finds its case. Materials and finishing bring the complete watch into focus.',
   '.collection-title p:not(.eyebrow)':'Explore three directions within the debut collection.',
   '.newsletter-inner p:not(.eyebrow)':'Notes on watches, personal style and the ideas behind the collection.',
  }
  for sel,copy in edits.items():
   for el in soup.select(sel):el.clear();el.append(copy)
  for el in soup.select('.world-hero-caption,.hero-launch'):el.decompose()
  news=soup.select_one('.newsletter-inner h2')
  if news:news.clear();news.append('A closer look.');
 # A single, compact launch announcement, not nested boxes repeating coming soon.
 for panel in soup.select('.coming-soon-panel'):
  panel.clear();panel.append(BeautifulSoup('<div><p class="eyebrow light">The India debut</p><h2>December 2026. On Myntra.</h2><p>Discover the collection as the first models arrive.</p></div><a class="button button-light" href="contact.html">Ask about the launch</a>','html.parser'))
 descriptions={'Men’s Collection':'Clean lines. Everyday versatility.','Women’s Collection':'Subtle details. Individual expression.','Signature Collection':'The defining forms of Sandy D. Carter.'}
 for card in soup.select('.content-card, .collection-editorial-grid a'):
  h=card.find('h3');p=card.find('p')
  if h and p and h.get_text(strip=True) in descriptions:p.clear();p.append(descriptions[h.get_text(strip=True)])
 for el in soup.select('.collection-editorial-grid span'):
  if 'COMING SOON' in el.get_text().upper():el.clear()
 for el in soup.select('.footer-studio,.droog-reference,.studio-card'):el.decompose()
 # Readable captions only; no repeated technical commentary around campaign images.
 for el in soup.find_all('figcaption'):
  if any(x in el.get_text().lower() for x in ['conceptual','not a','not historical']):el.clear();el.append('Collection study')
 for el in soup.select('.reveal'):el['class']=list(dict.fromkeys(el.get('class',[])+['visible']))
 head=soup.find('head')
 if head:
  css=soup.new_tag('link',rel='stylesheet',href='copy-edit.css?v=20261113b');head.append(css)
 return str(soup)
