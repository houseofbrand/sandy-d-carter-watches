#!/usr/bin/env ruby
# Completes social metadata consistently using each page's existing SEO fields.

require 'cgi'
require 'json'
require 'pathname'

root = Pathname.new(__dir__).join('..').expand_path
files = Dir[root.join('public', '*.html')].sort

files.each do |path|
  html = File.read(path)
  html.sub!(/<html(?:\s+lang="[^"]*")?/, '<html lang="en-IN"')

  title = html[/<title>(.*?)<\/title>/m, 1]
  description = html[/<meta\s+name="description"\s+content="([^"]*)"/m, 1]
  image = html[/<meta\s+property="og:image"\s+content="([^"]*)"/m, 1]
  next unless title && description

  h1 = CGI.unescapeHTML(html[/<h1(?:\s[^>]*)?>(.*?)<\/h1>/m, 1].to_s.gsub(/<[^>]+>/, ' ').gsub(/\s+/, ' ').strip)
  canonical = html[/<link\s+rel="canonical"\s+href="([^"]+)"/m, 1]
  html.gsub!(/(<script[^>]+type="application\/ld\+json"[^>]*>)(.*?)(<\/script>)/m) do
    opening, payload, closing = Regexp.last_match.captures
    begin
      data = JSON.parse(payload)
      if data['@type'] == 'Article'
        data['headline'] = h1 unless h1.empty?
        data['mainEntityOfPage'] = canonical if canonical
        data['image'] = data['image'].to_s.sub(%r{https?://127\.0\.0\.1:\d+/}, 'https://watches.sandydcarter.com/')
        data['datePublished'] ||= '2026-11-11'
        data['dateModified'] = '2026-11-11'
      elsif data['@type'] == 'BreadcrumbList' && data.dig('itemListElement', 1)
        data['itemListElement'][1]['name'] = h1 unless h1.empty?
      end
      "#{opening}#{JSON.generate(data)}#{closing}"
    rescue JSON::ParserError
      "#{opening}#{payload}#{closing}"
    end
  end

  additions = []
  additions << %(<meta name="twitter:card" content="summary_large_image">) unless html.include?('name="twitter:card"')
  additions << %(<meta name="twitter:title" content="#{title}">) unless html.include?('name="twitter:title"')
  additions << %(<meta name="twitter:description" content="#{description}">) unless html.include?('name="twitter:description"')
  additions << %(<meta name="twitter:image" content="#{image}">) if image && !html.include?('name="twitter:image"')
  additions << %(<meta property="og:image:alt" content="SANDY D CARTER — Amsterdam-inspired contemporary watch design">) if image && !html.include?('property="og:image:alt"')

  html.sub!('</head>', "#{additions.join}\n</head>") unless additions.empty?
  File.write(path, html)
end

puts "Enhanced metadata for #{files.length} HTML documents."
