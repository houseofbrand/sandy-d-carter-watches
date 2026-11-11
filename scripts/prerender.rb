#!/usr/bin/env ruby
# Freeze JavaScript-rendered content into the deployable HTML documents.
# Usage: ruby scripts/prerender.rb [http://127.0.0.1:4180] [--all]

require 'open3'
require 'pathname'
require 'tempfile'

ROOT = Pathname.new(__dir__).join('..').expand_path
PUBLIC = ROOT.join('public')
render_all = ARGV.delete('--all')
BASE_URL = ARGV.fetch(0, 'http://127.0.0.1:4180').sub(%r{/$}, '')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

abort "Chrome not found at #{CHROME}" unless File.executable?(CHROME)

pages = Dir[PUBLIC.join('*.html')].sort.select do |path|
  next false if File.basename(path) == '404.html'
  html = File.read(path)
  render_all || html.include?('<main id="main"></main>')
end

pages.each do |path|
  name = File.basename(path)
  command = [
    CHROME,
    '--headless',
    '--disable-gpu',
    '--no-first-run',
    '--disable-background-networking',
    '--virtual-time-budget=2500',
    '--dump-dom',
    "#{BASE_URL}/#{name}?prerender=1"
  ]
  html, error, status = Open3.capture3(*command)
  abort "Failed to prerender #{name}: #{error}" unless status.success? && html.include?('<main id="main">')

  # Query parameters are used only to bypass caches during the build.
  html.gsub!(/\?prerender=1/, '')
  html.sub!(/\A<html/, '<!doctype html>\n<html') unless html.lstrip.start_with?('<!DOCTYPE', '<!doctype')

  temporary = Tempfile.new([name, '.tmp'], PUBLIC.to_s)
  temporary.write(html)
  temporary.close
  File.rename(temporary.path, path)
  puts "Prerendered #{name}"
end

puts "Prerendered #{pages.length} pages."
