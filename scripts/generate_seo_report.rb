#!/usr/bin/env ruby
# Generates an evidence-based inventory from the deployable HTML.

require 'cgi'
require 'json'
require 'pathname'

root = Pathname.new(__dir__).join('..').expand_path
public_dir = root.join('public')
output = root.join('SEO-IMPLEMENTATION-REPORT.md')

targets = {
  'index.html' => ['Sandy D Carter watches', 'official website; premium designer watches; India'],
  'shop.html' => ['Sandy D Carter collection preview', 'premium designer watches; contemporary watches'],
  'mens-watches.html' => ['designer watches for men', 'minimalist watches for men; contemporary men’s watches'],
  'womens-watches.html' => ['designer watches for women', 'minimalist watches for women; elegant watches'],
  'signature.html' => ['signature watch collection', 'contemporary watch design; timeless watch aesthetics'],
  'about-us.html' => ['Sandy D Carter watch brand', 'India-registered watch brand; Amsterdam-inspired design'],
  'story-behind-the-brand/index.html' => ['Story Behind Sandy D. Carter', 'Amsterdam design journey since 2011; Sandy and Carter designers'],
  'design-philosophy.html' => ['watch design philosophy', 'minimalist watch design; functional aesthetics'],
  'netherlands.html' => ['Amsterdam design inspiration', 'Dutch design influence; European-inspired watches'],
  'journal.html' => ['watch design journal', 'watch education; contemporary watch design'],
  'contact.html' => ['contact Sandy D Carter', 'brand enquiries; retail partnerships'],
  'faqs.html' => ['Sandy D Carter FAQs', 'India launch; Myntra launch; pre-launch watches']
}

def text(value)
  CGI.unescapeHTML(value.to_s.gsub(/<[^>]+>/, ' ').gsub(/\s+/, ' ').strip)
end

rows = Dir[public_dir.join('**', '*.html')].sort.map do |path|
  html = File.read(path)
  name = Pathname.new(path).relative_path_from(public_dir).to_s
  title = text(html[/<title>(.*?)<\/title>/m, 1])
  description = html[/<meta\s+name="description"\s+content="([^"]*)"/m, 1].to_s
  h1s = html.scan(/<h1(?:\s[^>]*)?>(.*?)<\/h1>/m).flatten.map { |h| text(h) }
  canonical = html[/<link\s+rel="canonical"\s+href="([^"]+)"/m, 1].to_s
  noindex = html.match?(/<meta\s+name="robots"\s+content="[^"]*noindex/i)
  schemas = html.scan(/<script[^>]+type="application\/ld\+json"[^>]*>(.*?)<\/script>/m).flatten.map do |payload|
    begin
      data = JSON.parse(payload)
      types = [data['@type']]
      types.concat(Array(data['@graph']).map { |item| item['@type'] }) if data['@graph']
      types.compact
    rescue JSON::ParserError
      ['INVALID']
    end
  end.compact.flatten.uniq
  main = html[/<main\b.*?<\/main>/m].to_s
  word_count = text(main).split.length
  internal_links = main.scan(/href="(?!https?:|mailto:|tel:|#)([^"]+)"/).length
  images = main.scan(/<img\b/).length
  primary, secondary = targets.fetch(name) do
    base = title.sub(/\s*[|—-]\s*SANDY D\.? CARTER.*\z/i, '').strip
    [base.empty? ? name.sub('.html', '').tr('-', ' ') : base, 'Sandy D. Carter; watch design']
  end
  [name, title, description, h1s.join(' / '), primary, secondary, canonical, schemas.join(', '), noindex ? 'Noindex, follow' : 'Indexable', word_count, internal_links, images]
end

report = <<~MD
  # SANDY D. CARTER SEO implementation report

  Generated: 11 November 2026  
  Scope: `https://watches.sandydcarter.com/` only  
  Keyword data status: qualitative mapping. No approved live keyword-volume or difficulty provider was available, so no numeric estimates are presented.

  ## Page inventory

  | Page | SEO title | Meta description | H1 | Primary target | Secondary targets | Canonical | Schema | Indexability | Main words | Internal links | Images |
  |---|---|---|---|---|---|---|---|---:|---:|---:|---:|
MD

rows.each do |row|
  escaped = row.map { |value| value.to_s.gsub('|', '\\|').gsub(/\s+/, ' ').strip }
  report << "| #{escaped.join(' | ')} |\n"
end

report << <<~MD

  ## Technical SEO status

  - Canonical hostname: HTTPS `watches.sandydcarter.com`.
  - HTTP redirects to HTTPS. `/index.html` and query-string variants use the root homepage canonical because GitHub Pages does not provide repository-level redirect rules.
  - All important page bodies are prerendered into the delivered HTML. JavaScript remains as progressive enhancement.
  - `robots.txt` permits public crawling and declares the XML sitemap.
  - The sitemap includes canonical, indexable pages and excludes the custom 404, the legacy noindex alias, and three thin pre-launch utility pages.
  - Organization, WebSite, WebPage, BreadcrumbList and Article schema are used where appropriate. Product, Offer, Review, AggregateRating and LocalBusiness schema are intentionally absent.
  - Official social profiles are included in Organization schema. The Droog Amsterdam address is published only as a clearly attributed design-inspiration reference, not as a brand business address.
  - Every public HTML document has unique title and description metadata, canonical URL, Open Graph metadata and Twitter card metadata.

  ## Keyword architecture

  - Homepage: brand and official-site discovery.
  - Shop: pre-launch collection discovery without purchase intent claims.
  - Men, Women and Signature: distinct collection-design and styling intent.
  - About: factual brand identity and India registration wording.
  - Our Story: the approved real design journey beginning in Amsterdam in 2011, including the founder connection and attributed Droog inspiration reference.
  - Design Philosophy and Netherlands: design education and Amsterdam/Dutch influence.
  - Journal and individual articles: informational watch-design, fit, movement, material, care and styling queries.
  - Customer-care pages: policy intent only; thin unavailable services remain noindex until operational.

  ## External actions

  - Google Search Console verification, sitemap submission, URL inspection and indexing status: pending account access.
  - Bing Webmaster Tools verification and sitemap submission: pending account access.
  - Search volume, keyword difficulty and competitor metrics: pending access to an approved keyword-data provider.
  - Product schema, prices, specifications and marketplace purchase links: pending genuine approved products.

MD

File.write(output, report)
puts "Wrote #{output} with #{rows.length} page rows."
