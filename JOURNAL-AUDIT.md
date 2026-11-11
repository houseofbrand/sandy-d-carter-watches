# Journal and editorial audit

Audit date: 11 November 2026  
Canonical host: `https://watches.sandydcarter.com/`

## Result

The Journal index exposes every current long-form brand, design, buying, style, education and care article listed below as an ordinary crawlable link. Every URL is also present in `public/sitemap.xml`, has a self-referencing canonical URL, a unique page title and description, responsive layout rules, and internal links back to the Journal or a related collection/guide.

Structured `Article` data is included directly in static article pages where available. The shared refinement script adds `Article` data to the long-form dynamically rendered editorial pages while avoiding duplicate Article schema.

## Indexed editorial inventory

| Article | URL | Type | Journal link | Sitemap |
|---|---|---|---|---|
| The Story Behind SANDY D CARTER | `/our-story.html` | Brand story | Yes | Yes |
| Amsterdam and the Art of Minimalist Design | `/netherlands.html` | Design influence | Yes | Yes |
| Why Minimalism Matters in Watch Design | `/minimalist-watches.html` | Design principle | Yes | Yes |
| Purposeful Simplicity in European Design | `/scandinavian-design-watches.html` | Design history | Yes | Yes |
| Understanding Watch Dial Architecture | `/watch-dials-cases-finishing.html` | Watch education | Yes | Yes |
| How to Choose a Premium Designer Watch | `/what-makes-a-premium-watch.html` | Buying guide | Yes | Yes |
| The Importance of Proportion in Watch Design | `/watch-case-shapes-and-sizes.html` | Watch education | Yes | Yes |
| Understanding Watch Movements | `/understanding-watch-movements.html` | Watch education | Yes | Yes |
| Timeless Design Versus Temporary Trends | `/timeless-design-versus-trends.html` | Design perspective | Yes | Yes |
| The Art of Watchmaking | `/art-of-watchmaking.html` | Watch education | Yes | Yes |
| From Sketch to Watch | `/from-sketch-to-watch.html` | Creative process | Yes | Yes |
| Where Ideas Take Shape | `/design-studio.html` | Creative process | Yes | Yes |
| Metal or Leather Watch Straps? | `/metal-vs-leather-watch-straps.html` | Material guide | Yes | Yes |
| Choosing a Watch for Men | `/premium-watches-for-men.html` | Buying guide | Yes | Yes |
| Choosing a Watch for Women | `/premium-watches-for-women.html` | Buying guide | Yes | Yes |
| Choosing an Everyday Watch | `/choosing-a-watch-for-everyday-use.html` | Buying guide | Yes | Yes |
| Styling a Watch for Office Wear | `/how-to-style-a-watch-for-office-wear.html` | Style guide | Yes | Yes |
| How to Care for Your Watch | `/watch-care-guide.html` | Care guide | Yes | Yes |
| A Thoughtful Watch Gift Guide | `/watch-gift-guide.html` | Gift guide | Yes | Yes |

## Indexing notes

- `robots.txt` permits crawling and points to the canonical sitemap.
- The sitemap contains 42 canonical public URLs; legacy utility aliases intentionally excluded from the sitemap remain `noindex,follow` where applicable.
- Core title, description, Open Graph and canonical tags are present in static document heads so crawlers do not need JavaScript for metadata.
- Several primary long-form page bodies are rendered by the site’s shared JavaScript architecture. They remain directly addressable and render without user interaction, but a future static-generation migration would make the body copy available in the initial HTML response as well.

