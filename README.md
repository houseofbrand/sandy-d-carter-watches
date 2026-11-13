# SANDY D. CARTER

One source for the parent brand website and its watch-subdomain mirror.

- `site/build.py`: shared HTML components and build-time rendering.
- `site/pages.json`: concise page-specific content.
- `site/edition.css` and `site/edition.js`: responsive design and progressive enhancement.
- `site/assets/`: licensed fonts, supplied artwork and editorial campaign images.
- `public/`: generated watch mirror; deployed by GitHub Pages from `main`.
- `source/full-watch-site/` and `archive/`: historical snapshots only. Do not edit or deploy them.

Build with Python 3.9+: `python3 site/build.py`.
Validate with Python 3.9+: `python3 scripts/validate.py public`.
The GitHub workflow rebuilds and validates before deployment. No npm install, browser render or external font service is required.

## Parent publishing

Parent production is the existing Sites project `appgprj_6af02477305481919a64165d2e06a8d8`, not the historical Shopify site described in earlier revisions. Build with `python3 site/build.py --output <checkout>/dist --host sandydcarter.com`, copy the source into that site's existing checkout, and use the Sites source-push/package/save/deploy workflow. Preserve its public audience and custom domain. Do not change DNS.

Both hosts serve complete static HTML. The parent domain is canonical for matching content; the watch subdomain stays independently accessible without redirects. Existing URL paths are preserved. Superseded overlapping keyword URLs point to the appropriate preferred canonical page. Unavailable pricing, payment and tracking pages are omitted from the sitemap and marked noindex.

The contact form composes email/WhatsApp drafts; it does not store leads or send messages automatically. Without JavaScript the direct contact links remain available. Replace the campaign concept images with actual product photography when confirmed models are available. See `site/ASSET-NOTES.md`.
