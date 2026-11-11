# SANDY D CARTER Watches

Independent website source for `https://watches.sandydcarter.com`.

## Deployment architecture

- `public/` is the only directory deployed by GitHub Pages. It contains the complete multi-page watch website.
- `source/full-watch-site/` preserves the synchronized local-source snapshot used for this launch.
- `archive/coming-soon/` preserves the former launch page and is not deployed.
- `.github/workflows/pages.yml` deploys `public/` from the `main` branch.
- `public/CNAME` configures the custom subdomain only.

The Shopify website at `sandydcarter.com`, its `www` host, settings, theme, content, integrations, and DNS are outside this repository and are not modified by this project.

## DNS record

The isolated subdomain record is configured at the current DNS provider:

| Type | Host | Target | TTL |
| --- | --- | --- | --- |
| CNAME | `watches` | `houseofbrand.github.io` | 1 hour |

Do not alter the root (`@`) or `www` records.
