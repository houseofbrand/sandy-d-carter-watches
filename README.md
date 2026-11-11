# SANDY D CARTER Watches

Independent website source for `https://watches.sandydcarter.com`.

## Deployment architecture

- `public/` is the only directory deployed by GitHub Pages. It contains the initial Coming Soon experience.
- `source/full-watch-site/` preserves the previously developed watch website for a future launch. It is intentionally excluded from the Pages artifact.
- `.github/workflows/pages.yml` deploys `public/` from the `main` branch.
- `public/CNAME` configures the custom subdomain only.

The Shopify website at `sandydcarter.com`, its `www` host, settings, theme, content, integrations, and DNS are outside this repository and are not modified by this project.

## DNS record

The isolated subdomain record is configured at the current DNS provider:

| Type | Host | Target | TTL |
| --- | --- | --- | --- |
| CNAME | `watches` | `houseofbrand.github.io` | 1 hour |

Do not alter the root (`@`) or `www` records.
