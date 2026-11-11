#!/usr/bin/env ruby

require 'cgi'
require 'json'
require 'pathname'
require 'rexml/document'
require 'set'

root = Pathname.new(__dir__).join('..').expand_path
public_dir = root.join('public')
errors = []
titles = Hash.new { |hash, key| hash[key] = [] }
descriptions = Hash.new { |hash, key| hash[key] = [] }

def clean_html(value)
  CGI.unescapeHTML(value.to_s.gsub(/<[^>]+>/, ' ').gsub(/\s+/, ' ').strip)
end

html_paths = Dir[public_dir.join('**', '*.html')].sort
html_paths.each do |path|
  path = Pathname.new(path)
  name = path.relative_path_from(public_dir).to_s
  html = File.read(path)
  base_href = html[/<base\s+href="([^"]+)"/m, 1]
  reference_base = base_href ? path.dirname.join(base_href).cleanpath : path.dirname
  title = clean_html(html[/<title>(.*?)<\/title>/m, 1])
  description = html[/<meta\s+name="description"\s+content="([^"]+)"/m, 1].to_s
  h1s = html.scan(/<h1(?:\s[^>]*)?>(.*?)<\/h1>/m).flatten
  main = html[/<main\b.*?<\/main>/m].to_s

  errors << "#{name}: missing title" if title.empty?
  errors << "#{name}: missing description" if description.empty?
  errors << "#{name}: expected one H1, found #{h1s.length}" unless h1s.length == 1
  errors << "#{name}: empty main content" if clean_html(main).split.length < 10
  errors << "#{name}: missing canonical" if name != '404.html' && !html.match?(/<link\s+rel="canonical"\s+href="https:\/\/watches\.sandydcarter\.com\//)
  errors << "#{name}: contains local preview URL" if html.include?('127.0.0.1')

  html.scan(/<script[^>]+type="application\/ld\+json"[^>]*>(.*?)<\/script>/m).flatten.each do |payload|
    begin
      JSON.parse(payload)
    rescue JSON::ParserError => error
      errors << "#{name}: invalid JSON-LD (#{error.message})"
    end
  end

  main.scan(/(?:href|src)="([^"]+)"/).flatten.each do |reference|
    next if reference.match?(/\A(?:https?:|mailto:|tel:|#|data:)/)
    local = reference.split(/[?#]/).first
    next if local.nil? || local.empty?
    target = reference_base.join(local).cleanpath
    resolved = target.file? || target.join('index.html').file?
    errors << "#{name}: missing local reference #{local}" unless resolved
  end

  titles[title] << name unless title.empty?
  descriptions[description] << name unless description.empty?
end

titles.each { |value, pages| errors << "duplicate title #{value.inspect}: #{pages.join(', ')}" if pages.length > 1 }
descriptions.each { |value, pages| errors << "duplicate description #{value.inspect}: #{pages.join(', ')}" if pages.length > 1 }

sitemap = REXML::Document.new(File.read(public_dir.join('sitemap.xml')))
sitemap_paths = Set.new
REXML::XPath.each(sitemap, "//*[local-name()='loc']") do |node|
  relative = node.text.sub('https://watches.sandydcarter.com/', '')
  relative = 'index.html' if relative.empty?
  sitemap_paths << relative
  target = public_dir.join(relative)
  target = target.join('index.html') if target.directory?
  errors << "sitemap: missing target #{relative}" unless target.file?
  errors << "sitemap: noindex target #{relative}" if target.file? && File.read(target).match?(/name="robots"\s+content="[^"]*noindex/i)
end

%w[order-tracking.html payment-information.html care-instructions.html 404.html].each do |excluded|
  errors << "sitemap: excluded page present #{excluded}" if sitemap_paths.include?(excluded)
end

forbidden_schema = /"@type":"(?:Product|Offer|AggregateRating|Review|LocalBusiness)"/
Dir[public_dir.join('**', '*.html')].each do |path|
  html = File.read(path)
  errors << "#{File.basename(path)}: forbidden schema type" if html.match?(forbidden_schema)
end

if errors.empty?
  puts "PASS: #{html_paths.length} HTML pages, #{sitemap_paths.length} sitemap URLs, unique metadata, valid JSON-LD and resolved local references."
else
  warn errors.join("\n")
  exit 1
end
