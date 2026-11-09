# Zürich → Firenze by train

An animated, single-file website (`public/index.html`) showing a rail journey from Zürich to Florence: EuroCity through the Gotthard and Ceneri base tunnels to Milano Centrale, then Frecciarossa via Bologna to Firenze S. M. Novella.

Open `public/index.html` in a browser. Press Play (or Space), drag the slider or the train on the map, click a stop in the timetable, or change the departure time.

Times and the map are approximate and for illustration only.

## Deploy (Cloudflare Pages)

Only the `public/` folder is published; settings live in `wrangler.toml`.

**Automatic deploys from this (private) repo**

1. Cloudflare dashboard → **Workers & Pages → Create → Pages → Connect to Git**.
2. Authorize GitHub and pick this repository (grant access to this repo only).
3. Framework preset: **None**. Build command: *(empty)*. Output directory: `public`.
4. Save and Deploy. Every push to the production branch redeploys; other branches get preview URLs.

**Manual deploy (no Git connection)**

```sh
npx wrangler login
npx wrangler pages deploy
```

**Local preview**: `npx wrangler pages dev` → http://localhost:8788

**Keep the site private**: Zero Trust → Access → Applications → Add → Self-hosted, domain `<project>.pages.dev` (and `*.<project>.pages.dev` for previews), policy *Allow* → *Emails* → your address. Free for up to 50 users.

**Database (optional)**: Cloudflare D1 (SQLite) — see the commented block in `wrangler.toml`; query it from Pages Functions in `functions/`.
