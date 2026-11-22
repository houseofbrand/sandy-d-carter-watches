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
 depth='../' if path=='story-behind-the-brand/index.html' else ''
 launch_href='#launch-list' if path=='index.html' else depth+'index.html#launch-list'
 for image in soup.select('img[src*="assets/brand/"]'):
  image['src']=depth+'assets/brand/official-logo.png'
  image['alt']='SANDY D. CARTER — Amsterdam Inspired Design'
 for link in soup.select('.launch-pill'):
  link['href']=launch_href;link.string='Join the launch list'
 mobile=soup.select_one('.mobile-nav')
 if mobile and not mobile.select_one('a[href*="launch-list"]'):
  mobile.append(BeautifulSoup(f'<a href="{launch_href}">Join the launch list</a>','html.parser'))
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
  hero_actions=soup.select_one('.hero-actions')
  if hero_actions:
   hero_actions.clear();hero_actions.append(BeautifulSoup('<a class="button button-light" href="shop.html">Explore collection</a><a class="text-link light" href="story-behind-the-brand/">Discover our story</a>','html.parser'))
  newsletter=soup.select_one('.newsletter')
  if newsletter:
   launch=BeautifulSoup('''<section class="launch-acquisition editorial-pad" id="launch-list" aria-labelledby="launch-heading"><div class="launch-copy"><p class="eyebrow light">Private preview · December 2026</p><h2 id="launch-heading">Be among<br>the first.</h2><p>Discover SANDY D. CARTER before the official collection launch. Receive collection previews, product introductions and launch announcements.</p><div class="myntra-note"><span>A new expression of time.</span><strong>Coming December 2026 on Myntra.</strong></div></div><form class="lead-form launch-form" data-form-kind="Launch list" novalidate><div class="form-grid"><label>Full name<input name="name" autocomplete="name" required maxlength="80"></label><label>Email address<input name="email" type="email" autocomplete="email" required maxlength="120"></label><label>Mobile number <span>(optional)</span><input name="mobile" type="tel" autocomplete="tel" inputmode="tel" pattern="[+0-9 ()-]{7,20}" maxlength="20"></label><label>Interested collection<select name="interest" required><option value="">Choose one</option><option>Men's</option><option>Women's</option><option>Both</option></select></label></div><label class="consent"><input name="consent" type="checkbox" required> I agree to be contacted about SANDY D. CARTER collection and launch updates. See the <a href="privacy.html">privacy notice</a>.</label><label class="trap" aria-hidden="true">Leave empty<input name="website" tabindex="-1" autocomplete="off"></label><div class="lead-actions"><button class="button button-light" type="submit" value="email">Join by email</button><button class="text-link light" type="submit" value="whatsapp">Join via WhatsApp</button></div><p class="form-status" role="status" aria-live="polite">Your message is sent only after you confirm it in your email or WhatsApp app.</p></form></section>''','html.parser')
   newsletter.insert_before(launch)
  journal=soup.select_one('.home-journal')
  if journal:
   trust=BeautifulSoup('''<section class="trust-rail editorial-pad" aria-label="Customer care"><div><span>01</span><a href="warranty.html"><strong>Warranty</strong><small>Approved terms published before sales begin</small></a></div><div><span>02</span><a href="shipping-returns.html"><strong>Shipping</strong><small>Coverage and delivery terms at launch</small></a></div><div><span>03</span><a href="returns-refunds.html"><strong>Returns</strong><small>Clear eligibility and support guidance</small></a></div><div><span>04</span><a href="contact.html"><strong>Customer care</strong><small>Email and verified WhatsApp support</small></a></div></section>''','html.parser')
   journal.insert_before(trust)
 if path in ['shop.html','mens-watches.html','womens-watches.html','signature.html']:
  prose=soup.select_one('.prose')
  if prose:
   collection={'shop.html':'The collection','mens-watches.html':"Men's collection",'womens-watches.html':"Women's collection",'signature.html':'Signature collection'}[path]
   interest={'shop.html':'Both','mens-watches.html':"Men's",'womens-watches.html':"Women's",'signature.html':'Signature'}[path]
   preview=BeautifulSoup(f'''<section class="collection-preview" aria-labelledby="preview-{path.replace('.html','')}"><p class="eyebrow">Collection preview</p><h2 id="preview-{path.replace('.html','')}">{collection}.<br>Revealed with facts, not assumptions.</h2><p class="preview-intro">The approved catalogue, model names, reference numbers, prices and specifications have not yet been supplied. This preview keeps discovery open without presenting concept art as saleable inventory.</p><div class="preview-cards"><article><span>01</span><h3>First reveal</h3><p>Approved product photography, model identity and complete specifications will appear here.</p><b>December 2026 · Planned launch</b></article><article><span>02</span><h3>Details that matter</h3><p>Movement, materials, glass, dimensions and water resistance will be published only after verification.</p><b>Verification in progress</b></article><article><span>03</span><h3>Your early view</h3><p>Register your interest to receive the collection reveal and model introductions.</p><b>Early access open</b></article></div><form class="lead-form notify-form" data-form-kind="Collection notification" novalidate><input type="hidden" name="interest" value="{interest}"><div><label>Email address<input name="email" type="email" autocomplete="email" required maxlength="120"></label><label>Mobile number <span>(optional)</span><input name="mobile" type="tel" autocomplete="tel" inputmode="tel" pattern="[+0-9 ()-]{{7,20}}" maxlength="20"></label></div><label class="consent"><input name="consent" type="checkbox" required> Notify me when this collection is revealed. I agree to the <a href="privacy.html">privacy notice</a>.</label><label class="trap" aria-hidden="true">Leave empty<input name="website" tabindex="-1" autocomplete="off"></label><div class="lead-actions"><button class="button button-dark" type="submit" value="email">Notify me by email</button><button class="text-link" type="submit" value="whatsapp">Notify me on WhatsApp</button></div><p class="form-status" role="status" aria-live="polite">Your message is sent only after you confirm it in your email or WhatsApp app.</p></form></section>''','html.parser')
   prose.append(preview)
 if path=='contact.html':
  prose=soup.select_one('.prose')
  if prose:
   retail=BeautifulSoup('''<section class="retail-enquiry" aria-labelledby="retail-heading"><p class="eyebrow">Retail &amp; distribution</p><h2 id="retail-heading">Introduce your business.</h2><p>For retail, distribution or corporate enquiries, share your details with the House Of Brands team.</p><form class="lead-form retail-form" data-form-kind="Retail and distribution enquiry" novalidate><div class="form-grid"><label>Business name<input name="business" required maxlength="120"></label><label>Contact person<input name="name" autocomplete="name" required maxlength="80"></label><label>Email<input name="email" type="email" autocomplete="email" required maxlength="120"></label><label>Mobile<input name="mobile" type="tel" autocomplete="tel" required inputmode="tel" pattern="[+0-9 ()-]{7,20}" maxlength="20"></label><label>Country<input name="country" autocomplete="country-name" required maxlength="80"></label><label class="full">Message<textarea name="message" required rows="5" maxlength="1200"></textarea></label></div><label class="consent"><input name="consent" type="checkbox" required> I agree to be contacted about this business enquiry.</label><label class="trap" aria-hidden="true">Leave empty<input name="website" tabindex="-1" autocomplete="off"></label><div class="lead-actions"><button class="button button-dark" type="submit" value="email">Send by email</button><button class="text-link" type="submit" value="whatsapp">Send on WhatsApp</button></div><p class="form-status" role="status" aria-live="polite">Your enquiry is sent only after you confirm it in your email or WhatsApp app.</p></form></section>''','html.parser')
   prose.append(retail)
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
 footer_care=soup.select_one('.footer-col:last-of-type')
 if footer_care and not footer_care.select_one('a[href*="launch-list"]'):
  footer_care.append(BeautifulSoup(f'<a href="{launch_href}">Join the launch list</a>','html.parser'))
 if soup.body:
  soup.body.append(BeautifulSoup('<a class="whatsapp-float" href="https://wa.me/917303681194?text=Hello%20SANDY%20D.%20CARTER%20team%2C%20I%20would%20like%20to%20know%20more%20about%20the%20December%202026%20collection%20launch." target="_blank" rel="noopener noreferrer" aria-label="Enquire with SANDY D. CARTER on WhatsApp"><span aria-hidden="true">WA</span><b>Enquire</b></a>','html.parser'))
 seo={
  'index.html':('SANDY D. CARTER | Premium Minimalist Watches','Discover SANDY D. CARTER, a contemporary watch brand developed in the Netherlands and inspired by Amsterdam and refined European design.'),
  'mens-watches.html':('Premium Watches for Men | SANDY D. CARTER','Preview the upcoming SANDY D. CARTER men’s collection and register for the December 2026 India launch.'),
  'womens-watches.html':('Designer Watches for Women | SANDY D. CARTER','Preview the upcoming SANDY D. CARTER women’s collection and register for the December 2026 India launch.'),
  'signature.html':('Signature Watches | SANDY D. CARTER','Discover the design direction behind the upcoming SANDY D. CARTER signature collection.'),
 }
 if path in seo and soup.title:
  title,description=seo[path];soup.title.string=title
  meta=soup.select_one('meta[name="description"]')
  if meta:meta['content']=description
  for tag in soup.select('meta[property="og:title"],meta[name="twitter:title"]'):tag['content']=title
  for tag in soup.select('meta[property="og:description"],meta[name="twitter:description"]'):tag['content']=description
  graph=soup.select_one('script[data-entity-graph]')
  if graph:
   try:
    payload=json.loads(graph.string)
    for item in payload.get('@graph',[]):
     if item.get('@type')=='WebPage':item['name']=title;item['description']=description
    graph.string=json.dumps(payload,separators=(',',':'))
   except (TypeError,ValueError):pass
 # Readable captions only; no repeated technical commentary around campaign images.
 for el in soup.find_all('figcaption'):
  if any(x in el.get_text().lower() for x in ['conceptual','not a','not historical']):el.clear();el.append('Collection study')
 for el in soup.select('.reveal'):el['class']=list(dict.fromkeys(el.get('class',[])+['visible']))
 head=soup.find('head')
 if head:
  css=soup.new_tag('link',rel='stylesheet',href='copy-edit.css?v=20261113-mobile');head.append(css)
 return str(soup)
