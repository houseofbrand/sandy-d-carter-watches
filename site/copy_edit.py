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

HERITAGE_META={
 'about-us.html':('About SANDY D. CARTER | An Idea Born in Amsterdam','Discover the SANDY D. CARTER brand history: an Amsterdam-born creative vision, its 2014 Indian trademark filing and its international future.'),
 'founder.html':('Rajan Mehta, Founder of SANDY D. CARTER','Meet Rajan Mehta, founder of SANDY D. CARTER, and discover how five years in Amsterdam shaped his vision for a European-inspired international watch brand.'),
 'design-philosophy.html':('European Watch Design Philosophy | SANDY D. CARTER','Explore the Dutch design influence, balanced proportions, thoughtful details and understated character behind SANDY D. CARTER watches.'),
 'our-journey.html':('Our Journey: Amsterdam to the World | SANDY D. CARTER','Follow the SANDY D. CARTER timeline from Rajan Mehta’s Amsterdam years and the December 2014 trademark filing to the planned December 2026 India launch.'),
 'story-behind-the-brand/index.html':('SANDY D. CARTER Brand History | Born in Amsterdam','The complete SANDY D. CARTER story: Rajan Mehta, Sandy and Carter, Droog Amsterdam, the 2014 India trademark filing and the next global chapter.'),
}

def heritage_hero(eyebrow,title,lead,image,alt,depth=''):
 asset=image if '/' in image else 'visual-story/'+image
 return f'''<section class="heritage-hero"><div class="heritage-hero-copy"><p class="eyebrow light">{eyebrow}</p><h1>{title}</h1><p class="heritage-hero-lead">{lead}</p></div><figure class="heritage-hero-media"><img src="{depth}assets/{asset}" alt="{alt}" width="1536" height="1024"></figure></section>'''

def chapter(number,label,body,paper=False):
 return f'''<section class="heritage-chapter{' paper' if paper else ''}"><div class="heritage-grid"><div class="heritage-index"><strong>{number}</strong>{label}</div><div class="heritage-prose">{body}</div></div></section>'''

def render_heritage(path):
 depth='../' if path=='story-behind-the-brand/index.html' else ''
 if path in ['about-us.html','story-behind-the-brand/index.html']:
  hero=heritage_hero('The SANDY D. CARTER story','An idea born<br>in Amsterdam.<em>A brand created for the world.</em>','Between 2009 and 2014, founder Rajan Mehta’s years in Amsterdam became the setting for a watch-brand idea shaped by European design, creative exchange and the belief that refinement begins with restraint.','01-amsterdam-inspiration-branded-web.jpg','Amsterdam canal houses representing the creative birthplace of SANDY D. CARTER',depth)
  body=chapter('01','Amsterdam · 2009–2014','''<p class="lede">The story begins with a place, an experience and an ambition—not with a legal entity in the Netherlands.</p><h2>The Amsterdam beginning.</h2><p>Rajan Mehta lived and worked in Amsterdam from 2009 to 2014. Immersed in the city’s design culture, architecture and instinct for purposeful simplicity, he began imagining a distinctive watch brand with a European point of view and an international identity.</p><p>The intention was never to create another conventional fashion-watch label. It was to build something more considered: watches guided by timeless aesthetics, thoughtful proportions, functional elegance and individual character.</p><div class="evidence-note"><strong>Brand integrity:</strong> Amsterdam is the creative birthplace of SANDY D. CARTER. The brand was subsequently formalised through an Indian trademark filing; no Dutch legal incorporation or manufacturing claim is made.</div>''')
  body+=chapter('02','The creative collaboration','''<h2>Two designers.<br>One shared philosophy.</h2><p>During this journey, Rajan connected with two designers: Sandy, a woman, and Carter, a man. Their discussions explored how European design sensibilities could shape a contemporary watch—simple without becoming anonymous, balanced without feeling rigid, and individual without excess.</p><div class="story-pair"><article><span>Creative perspective</span><h3>Sandy</h3><p>Sandy brought one of the two design perspectives behind the original collaboration.</p></article><article><span>Creative perspective</span><h3>Carter</h3><p>Carter brought the complementary perspective that helped give the brand its identity.</p></article></div><p>Sandy and Carter are presented as the designers in the original creative collaboration. They are not described as legal co-founders, and no unsupported biographies or credentials are assigned to them.</p>''',True)
  body+=chapter('03','Droog Amsterdam · the meaning of D','''<h2>Where the idea<br>found its name.</h2><p>The founding creative conversations took place at Droog Amsterdam. In the brand’s history, Droog is the setting in which the concept began to take shape—a design environment that gave those early discussions context and energy.</p><div class="name-key"><div><strong>SANDY</strong><span>The female designer in the original creative collaboration.</span></div><div><strong>D</strong><span>Droog, the Amsterdam setting for the founding design conversations.</span></div><div><strong>CARTER</strong><span>The male designer in the original creative collaboration.</span></div></div><div class="evidence-note">This is a historical and inspirational reference. SANDY D. CARTER does not claim an official partnership, endorsement, ownership relationship or design approval from Droog Amsterdam.</div>''')
  body+=chapter('04','India · December 2014','''<h2>From creative concept<br>to commercial foundation.</h2><p>The Amsterdam concept was subsequently formalised in India. The SANDY D. CARTER trademark application was filed on 17 December 2014 in Class 14, marking an important step in turning the creative vision into a commercial brand.</p><p>House Of Brands Fashion LLP was established in India in 2015. Founded by Rajan Mehta, the business brings experience across e-commerce, product sourcing and development, brand building, retail and marketplace distribution.</p><div class="trademark-card"><h4>A deliberately international foundation</h4><dl><div><dt>Creative birthplace</dt><dd>Amsterdam, Netherlands</dd></div><div><dt>Trademark foundation</dt><dd>India · December 2014</dd></div><div><dt>Business support</dt><dd>House Of Brands Fashion LLP</dd></div><div><dt>Marketplace relationship</dt><dd>Myntra</dd></div></dl></div><p>Myntra is a marketplace partner of House Of Brands. This relationship supports the planned Indian market presence; it does not imply that Myntra owns, founded or exclusively distributes SANDY D. CARTER.</p>''',True)
  body+=chapter('05','The next chapter','''<h2>From Amsterdam<br>to the world.</h2><p>Conceived in Amsterdam and established in India, SANDY D. CARTER is preparing for its renewed India launch in December 2026. The Netherlands remains the brand’s creative birthplace and an intended future market.</p><p>The wider ambition includes planned expansion into the United Arab Emirates and the United Kingdom, alongside a future office presence in Los Angeles. These are future intentions, not claims of current offices, shops or market operations.</p><div class="world-markets"><article><span>Creative birthplace</span><h3>Amsterdam</h3><p>The origin of the brand idea and a future European market.</p></article><article><span>Planned launch</span><h3>India</h3><p>First major launch market · December 2026.</p></article><article><span>Future market</span><h3>UAE</h3><p>Part of the planned international expansion.</p></article><article><span>Future market</span><h3>London</h3><p>An intended United Kingdom market.</p></article><article><span>Future presence</span><h3>Los Angeles</h3><p>A planned office ambition; not currently operational.</p></article></div>''')
  body+=f'''<section class="heritage-cta"><p class="eyebrow light">TIME. REFINED.</p><h2>Different cities. Different perspectives. One design philosophy.</h2><p>Meet the founder behind the Amsterdam-born vision, or explore the first collection direction ahead of the planned India launch.</p><a class="button button-light" href="{depth}founder.html">Meet the founder</a> <a class="button button-light" href="{depth}shop.html">Explore the collection</a></section>'''
  return hero+body
 if path=='founder.html':
  hero=heritage_hero('Founder · Rajan Mehta','A global journey.<em>One considered vision.</em>','Rajan Mehta’s experience across India, Europe, the Netherlands, the Middle East and China shaped an ambition: to create a watch brand with European design roots and international relevance.','founder/rajan-mehta-baselworld.jpg','Rajan Mehta, founder of SANDY D. CARTER')
  body=chapter('01','The founder','''<div class="founder-profile"><figure class="founder-portrait"><img src="assets/founder/rajan-mehta-baselworld.jpg" alt="Rajan Mehta at the Baselworld watch trade fair" width="1200" height="1500"><figcaption>Rajan Mehta · Founder of SANDY D. CARTER and House Of Brands Fashion LLP</figcaption></figure><div><p class="lede">An entrepreneur, product developer and brand builder with more than 25 years of experience in watches, fashion accessories and lifestyle products.</p><h2>From product to brand.</h2><p>Rajan Mehta’s career spans product development, sourcing, manufacturing, packaging, retail strategy and e-commerce. His international experience includes work across India, Europe, the Middle East and China, bringing together an understanding of how ideas move from first concept to commercial reality.</p><p>From 2009 to 2014, Rajan lived and worked in Amsterdam. The city’s creative culture and approach to purposeful design became the backdrop for the original SANDY D. CARTER idea.</p><h3>The Amsterdam vision</h3><p>Rajan wanted to create an international watch brand that felt considered rather than conventional. Through discussions with designers Sandy and Carter at Droog Amsterdam, that ambition developed into a philosophy centred on simplicity, proportion, balance and character.</p><blockquote class="founder-quote">“During my years in Amsterdam, I began imagining a watch brand that would reflect the design values I admired in Europe. SANDY D. CARTER grew from those conversations, creative perspectives and a belief that simplicity can create something truly distinctive.”<span class="quote-status">Proposed founder statement · requires Rajan Mehta’s approval before it is treated as a verbatim quotation</span></blockquote><h3>Building the business foundation</h3><p>Rajan founded House Of Brands Fashion LLP, established in India in 2015. Its experience in product development, international sourcing, e-commerce, brand building and marketplace distribution provides the commercial foundation for SANDY D. CARTER’s next chapter.</p><h3>A long-term international view</h3><p>His ambition is to reconnect the brand with the Netherlands, launch its renewed identity in India in December 2026, and build future relevance across the UAE, London and Los Angeles—one market at a time, without losing the clarity of the original Amsterdam idea.</p><p><a class="text-link" href="https://rajanmehta.in/" target="_blank" rel="noopener noreferrer">Visit Rajan Mehta’s official website</a></p></div></div>''')
  return hero+body+'''<section class="heritage-cta"><p class="eyebrow light">The complete story</p><h2>An idea shaped by place, people and purpose.</h2><a class="button button-light" href="about-us.html">Discover our story</a></section>'''
 if path=='design-philosophy.html':
  hero=heritage_hero('Our design philosophy','Considered,<br>not complicated.<em>European by instinct.</em>','Born from a creative vision in Amsterdam, our philosophy brings together Dutch design sensibilities and a contemporary understanding of time.','03-creative-philosophy-branded-web.jpg','Watch sketches and material studies representing the SANDY D. CARTER design philosophy')
  body=chapter('01','The principles','''<p class="lede">True refinement does not demand attention. It earns it through proportion, purpose and character.</p><h2>Design that leaves<br>room to breathe.</h2><p>We begin with clarity: what the watch needs to communicate, how it should sit on the wrist and which details deserve to remain. Simplicity is not emptiness. It is the result of choosing carefully.</p><div class="principles-editorial"><article><span>01</span><h3>Timelessness</h3><p>Coherent choices that can live beyond a temporary trend.</p></article><article><span>02</span><h3>Simplicity</h3><p>A disciplined edit that reveals character instead of removing it.</p></article><article><span>03</span><h3>Proportion</h3><p>Dial, bezel, case, lugs and crown considered as one composition.</p></article><article><span>04</span><h3>Thoughtful detail</h3><p>Typography, texture, colour and finishing used with intention.</p></article><article><span>05</span><h3>Functional elegance</h3><p>Legibility, comfort and daily usefulness as part of the aesthetic.</p></article><article><span>06</span><h3>Understatement</h3><p>Confidence expressed through restraint rather than excess.</p></article><article><span>07</span><h3>Individuality</h3><p>A quiet point of view that makes each design recognisable.</p></article></div>''')
  body+=chapter('02','Amsterdam influence','''<h2>Dutch design,<br>international outlook.</h2><p>Amsterdam’s architecture often brings old and new into the same frame. Dutch design culture pairs clear thinking with unexpected personality. Those ideas inform our approach without becoming a costume or a claim of manufacture.</p><p>Droog Amsterdam matters as the historical setting for the founding creative discussions. It did not manufacture, approve or officially endorse SANDY D. CARTER watches.</p><h3>Material and finishing</h3><p>Materials and finishes will be specified model by model once the launch collection is approved. Our design direction favours contrasts that reveal form: brushed against polished, open space against fine markers, restrained colour against the natural character of metal or leather.</p><h3>Designed beyond trends</h3><p>A timeless watch need not be anonymous. We look for the point at which an object feels calm but still personal—recognisable through its relationships, not through unnecessary decoration.</p>''',True)
  return hero+body+'''<section class="heritage-cta"><p class="eyebrow light">TIME. REFINED.</p><h2>Refinement through proportion, purpose and character.</h2><a class="button button-light" href="shop.html">Explore the collection direction</a></section>'''
 if path=='our-journey.html':
  hero=heritage_hero('Our journey','Amsterdam, India<em>and the road ahead.</em>','A timeline of the documented milestones behind SANDY D. CARTER—from Rajan Mehta’s Amsterdam years to the planned December 2026 India launch.','05-concept-to-creation-branded-web.jpg','Design sketches and watch forms representing the SANDY D. CARTER journey')
  body=chapter('01','Documented milestones','''<h2>A story built<br>across borders.</h2><div class="timeline-editorial"><article><time>2009</time><div><h3>The Amsterdam journey begins</h3><p>Rajan Mehta begins living and working in Amsterdam, Netherlands.</p></div></article><article><time>2009–2014</time><div><h3>The original vision develops</h3><p>His experience of Dutch and wider European design culture shapes the ambition for an international watch brand.</p></div></article><article><time>During these years</time><div><h3>A creative collaboration takes shape</h3><p>Rajan connects with designers Sandy and Carter. Their founding design discussions take place at Droog Amsterdam. No unsupported exact meeting date is assigned.</p></div></article><article><time>Dec 2014</time><div><h3>The Indian trademark application</h3><p>The SANDY D. CARTER trademark application is filed in India on 17 December 2014, distinguishing the brand’s legal foundation from its Amsterdam creative origin.</p></div></article><article><time>2015</time><div><h3>House Of Brands is established</h3><p>House Of Brands Fashion LLP is incorporated in India, building expertise across development, sourcing, e-commerce and distribution.</p></div></article><article><time>Previous years</time><div><h3>Products enter the Indian marketplace</h3><p>Brand products appear in the Indian marketplace. Exact first-sale dates are not asserted without further documentation.</p></div></article><article><time>2026</time><div><h3>A renewed identity</h3><p>SANDY D. CARTER prepares for its planned December India launch, with Myntra forming an important part of the marketplace strategy.</p></div></article><article><time>Future</time><div><h3>From Amsterdam to the world</h3><p>Planned ambitions include the Netherlands, UAE, UK and a future Los Angeles office presence. These are not presented as current operations.</p></div></article></div>''')
  return hero+body+'''<section class="heritage-cta"><p class="eyebrow light">The next chapter</p><h2>Different cities. One design philosophy.</h2><a class="button button-light" href="about-us.html">Read the complete story</a></section>'''
 return None

def edit(text,path):
 soup=BeautifulSoup(text,'html.parser');data=EXTRA.get(path) or PAGES.get(path)
 depth='../' if path=='story-behind-the-brand/index.html' else ''
 heritage=render_heritage(path)
 if heritage:
  main=soup.select_one('#main')
  if main:
   main.clear();main.append(BeautifulSoup(heritage,'html.parser'))
  if soup.body:soup.body['data-page']='heritage'
  title,description=HERITAGE_META[path]
  if soup.title:soup.title.string=title
  meta=soup.select_one('meta[name="description"]')
  if not meta:
   meta=soup.new_tag('meta');meta['name']='description';soup.head.append(meta)
  meta['content']=description
  canonical=soup.select_one('link[rel="canonical"]')
  canonical_path={'about-us.html':'about-us.html','founder.html':'founder.html','design-philosophy.html':'design-philosophy.html','our-journey.html':'our-journey.html','story-behind-the-brand/index.html':'story-behind-the-brand/'}[path]
  if canonical:canonical['href']='https://sandydcarter.com/'+canonical_path
  for tag in soup.select('meta[property="og:title"],meta[name="twitter:title"]'):tag['content']=title
  for tag in soup.select('meta[property="og:description"],meta[name="twitter:description"]'):tag['content']=description
  for tag in soup.select('meta[property="og:url"]'):tag['content']='https://sandydcarter.com/'+canonical_path
 launch_href='#launch-list' if path=='index.html' else depth+'index.html#launch-list'
 for image in soup.select('img[src*="assets/brand/"]'):
  image['src']=depth+'assets/brand/official-logo.png'
  image['alt']='SANDY D. CARTER — Amsterdam Inspired Design'
 for link in soup.select('.launch-pill'):
  link['href']=launch_href;link.string='Join the launch list'
 mobile=soup.select_one('.mobile-nav')
 if mobile and not mobile.select_one('a[href*="launch-list"]'):
  mobile.append(BeautifulSoup(f'<a href="{launch_href}">Join the launch list</a>','html.parser'))
 # A consistent, factual brand-story navigation across every page.
 for link in soup.select('.nav a'):
  if link.get_text(' ',strip=True).lower()=='our story':link['href']=depth+'about-us.html'
 if mobile:
  for link in list(mobile.find_all('a')):
   if link.get_text(' ',strip=True) in ['Our story','About the brand']:link.decompose()
  contact=mobile.select_one('a[href$="contact.html"]')
  brand_links=BeautifulSoup(f'<a href="{depth}about-us.html">Our story</a><a href="{depth}founder.html">Founder</a><a href="{depth}our-journey.html">Our journey</a>','html.parser')
  if contact:
   for link in list(brand_links.contents):contact.insert_before(link)
  else:mobile.append(brand_links)
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
  hero=soup.select_one('.world-hero-copy')
  if hero:
   hero.clear();hero.append(BeautifulSoup('''<p class="eyebrow light">Amsterdam-born watch design</p><h1 id="home-title">SANDY D. CARTER<br><span>TIME. REFINED.</span></h1><p class="world-hero-lead">An idea born in Amsterdam. A vision shaped by design.</p><p>European-inspired watches guided by simplicity, proportion and individual character. The renewed collection is planned to launch in India in December 2026.</p><div class="hero-actions"><a class="button button-light" href="shop.html">Explore the collection</a><a class="text-link light" href="about-us.html">Discover our story</a></div>''','html.parser'))
  creative=soup.select_one('.creative-intro .creative-copy')
  if creative:
   creative.clear();creative.append(BeautifulSoup('''<p class="eyebrow">The creative collaboration</p><h2 id="creative-heading">Sandy. Droog.<br>Carter.</h2><p>Sandy and Carter were the two designers in the original creative collaboration. The letter D represents Droog Amsterdam, the setting for the founding design discussions. No official Droog affiliation is claimed.</p><a class="text-link" href="about-us.html">The meaning behind the name</a>''','html.parser'))
  intro=soup.select_one('.creative-intro')
  if intro:
   story=BeautifulSoup('''<section class="heritage-home-story" aria-labelledby="home-story-title"><div><p class="eyebrow">An idea born in Amsterdam</p><h2 id="home-story-title">The original vision,<br>2009–2014.</h2><p>Between 2009 and 2014, an idea took shape in Amsterdam. Inspired by European design culture and developed through the creative collaboration of Rajan Mehta, Sandy and Carter, SANDY D. CARTER was imagined around simplicity, proportion and individuality.</p><p>The concept found its identity through conversations at Droog Amsterdam before being formalised through an Indian trademark filing in December 2014. Today, that original vision enters a new chapter.</p><a class="text-link" href="about-us.html">Discover our story</a></div><figure><img src="assets/visual-story/01-amsterdam-inspiration-branded-web.jpg" alt="Amsterdam canal architecture representing the origin of SANDY D. CARTER" width="1536" height="1024" loading="lazy"/></figure></section><section class="heritage-home-founder" aria-labelledby="home-founder-title"><figure><img src="assets/founder/rajan-mehta-baselworld.jpg" alt="Rajan Mehta, founder of SANDY D. CARTER" width="1200" height="1500" loading="lazy"/></figure><div><p class="eyebrow">The vision behind the brand</p><h2 id="home-founder-title">Meet<br>Rajan Mehta.</h2><p>Founded by Rajan Mehta, SANDY D. CARTER brings together international watch-industry experience, an Amsterdam-born creative vision and a contemporary approach to European-inspired design.</p><a class="text-link" href="founder.html">Meet the founder</a></div></section>''','html.parser')
   intro.insert_after(story)
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
 for column in soup.select('.footer-col'):
  heading=column.find('h3')
  if heading and heading.get_text(' ',strip=True)=='Brand':
   column.clear();column.append(BeautifulSoup(f'''<h3>Brand</h3><a href="{depth}about-us.html">Our story</a><a href="{depth}founder.html">Founder</a><a href="{depth}design-philosophy.html">Design philosophy</a><a href="{depth}our-journey.html">Our journey</a><a href="{depth}journal.html">Journal</a>''','html.parser'))
 footer_tagline=soup.select_one('.footer-bottom span:last-child')
 if footer_tagline:footer_tagline.string='TIME. REFINED.'
 footer_care=soup.select_one('.footer-col:last-of-type')
 if footer_care and not footer_care.select_one('a[href*="launch-list"]'):
  footer_care.append(BeautifulSoup(f'<a href="{launch_href}">Join the launch list</a>','html.parser'))
 if soup.body:
  soup.body.append(BeautifulSoup('<a class="whatsapp-float" href="https://wa.me/917303681194?text=Hello%20SANDY%20D.%20CARTER%20team%2C%20I%20would%20like%20to%20know%20more%20about%20the%20December%202026%20collection%20launch." target="_blank" rel="noopener noreferrer" aria-label="Enquire with SANDY D. CARTER on WhatsApp"><span aria-hidden="true">WA</span><b>Enquire</b></a>','html.parser'))
 seo={
  'index.html':('SANDY D. CARTER | Amsterdam-Inspired Watches','Discover SANDY D. CARTER, an Amsterdam-born watch brand shaped by European design and preparing for its December 2026 India launch.'),
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
 # Replace legacy entity claims with a single evidence-aligned graph.
 for old_graph in soup.select('script[data-entity-graph]'):old_graph.decompose()
 canonical=soup.select_one('link[rel="canonical"]')
 canonical_url=canonical.get('href') if canonical else 'https://sandydcarter.com/'
 title=soup.title.get_text(strip=True) if soup.title else 'SANDY D. CARTER'
 description=(soup.select_one('meta[name="description"]') or {}).get('content','Amsterdam-born, European-inspired watch design.')
 graph={'@context':'https://schema.org','@graph':[
  {'@type':'Organization','@id':'https://sandydcarter.com/#organization','name':'House Of Brands Fashion LLP','url':'https://sandydcarter.com/','description':'The India-based business supporting the commercial development and distribution of SANDY D. CARTER.','founder':{'@id':'https://sandydcarter.com/#rajan-mehta'},'brand':{'@id':'https://sandydcarter.com/#brand'}},
  {'@type':'Person','@id':'https://sandydcarter.com/#rajan-mehta','name':'Rajan Mehta','url':'https://rajanmehta.in/','jobTitle':'Founder','worksFor':{'@id':'https://sandydcarter.com/#organization'}},
  {'@type':'Brand','@id':'https://sandydcarter.com/#brand','name':'SANDY D. CARTER','url':'https://sandydcarter.com/','description':'A watch brand creatively conceived in Amsterdam and commercially established through an Indian trademark filing in December 2014.','logo':'https://sandydcarter.com/assets/brand/official-logo.png','slogan':'TIME. REFINED.','founder':{'@id':'https://sandydcarter.com/#rajan-mehta'}},
  {'@type':'WebSite','@id':'https://sandydcarter.com/#website','url':'https://sandydcarter.com/','name':'SANDY D. CARTER','inLanguage':'en','publisher':{'@id':'https://sandydcarter.com/#organization'},'about':{'@id':'https://sandydcarter.com/#brand'}},
  {'@type':'WebPage','@id':canonical_url+'#webpage','url':canonical_url,'name':title,'description':description,'isPartOf':{'@id':'https://sandydcarter.com/#website'},'about':{'@id':'https://sandydcarter.com/#brand'},'inLanguage':'en'}]}
 schema=soup.new_tag('script',type='application/ld+json');schema['data-entity-graph']='true';schema.string=json.dumps(graph,separators=(',',':'));soup.head.append(schema)
 head=soup.find('head')
 if head:
  css=soup.new_tag('link',rel='stylesheet',href='copy-edit.css?v=20261113-mobile');head.append(css)
  heritage_css=soup.new_tag('link',rel='stylesheet',href=depth+'heritage.css?v=20261122');head.append(heritage_css)
 output=str(soup)
 corrections={
  'developed in the Netherlands':'creatively conceived in Amsterdam',
  'Developed in the Netherlands':'Creatively conceived in Amsterdam',
  'Netherlands-developed':'Amsterdam-born',
  'netherlands-developed':'Amsterdam-born',
  'a design journey that began in 2011':'a creative vision that developed in Amsterdam between 2009 and 2014',
  'Amsterdam, 2011':'Amsterdam, 2009–2014',
  'Two Designers. One Shared Perspective.':'TIME. REFINED.',
  'Scandinavian-inspired minimalism':'European design restraint',
  'global development and marketing partner':'business foundation for commercial development and distribution',
  'global alliance with House Of Brands Fashion LLP, India':'the support of House Of Brands Fashion LLP, India',
  'Amsterdam design journey that began in 2011':'original Amsterdam creative collaboration',
  'Amsterdam design journey since 2011':'Amsterdam creative origin, 2009–2014',
  'fictional creative personalities':'designers in the original creative collaboration',
  'fictional creative personality':'designer in the original creative collaboration',
  'two fictional creative personalities':'two designers in the original creative collaboration',
  'Fictional creative personality':'Designer in the original creative collaboration',
 }
 for before,after in corrections.items():output=output.replace(before,after)
 return output
