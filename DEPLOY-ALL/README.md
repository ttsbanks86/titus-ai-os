# Titus Banks - Deploy Guide

The 3 landing pages are ready to ship. All you need is 5 minutes and a free Netlify account.

## What's Ready

| File | Purpose | Best For |
|---|---|---|
| `01-opendoor-ai-landing.html` | Open Door AI Systems hero landing | Sub-brand showcase |
| `02-ba-services-landing.html` | Business Analysis and Operations services | Lead generation |
| `03-faithful-journey-quest-cover.html` | Faithful Journey Quest magazine cover | Editorial showcase |

All 3 are complete HTML files with zero dependencies. They use Google Fonts (Bricolage Grotesque, Inter, Playfair Display, JetBrains Mono) loaded via CDN. No build step. No server needed.

## Fastest Deploy: Netlify Drop (5 minutes)

1. Open `https://app.netlify.com/drop` in your browser
2. Sign up free if you have not (email + password, 60 seconds)
3. Drag the `DEPLOY-ALL` folder from your desktop onto the page
4. Netlify gives you 3 URLs - one per HTML file
5. Click each URL to verify they work
6. Optional: in Netlify dashboard, rename the sites and add custom domain

The deploy URLs will look like:
- `https://random-name-123.netlify.app/01-opendoor-ai-landing.html`
- `https://random-name-456.netlify.app/02-ba-services-landing.html`
- `https://random-name-789.netlify.app/03-faithful-journey-quest-cover.html`

You can rename each site in Netlify settings.

## Alternative: Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in the `DEPLOY-ALL` folder
3. Follow the prompts (signup with email, 60 seconds)
4. Vercel gives you 1 URL with all 3 pages as sub-paths

## Alternative: Surge.sh

1. Install: `npm i -g surge`
2. `cd DEPLOY-ALL`
3. `surge` (first run asks for email + password)
4. Pick a domain like `titus-banks.surge.sh`
5. All 3 pages will be at that URL

## After Deploy

Once you have the 3 URLs:

1. Update the Linkpod master page (`https://my.linkpod.site/titus-banks`) with the BA services URL as the primary CTA
2. Add the Open Door AI URL to the Open Door AI sub-brand
3. Add the FJQ URL to the Faithful Journey Quest sub-brand
4. Use the BA services URL in the first LinkedIn post
5. Send the BA services URL to 10 people in your network as a soft launch

## The BA Services URL is the Most Important

That is the lead-gen engine. Every LinkedIn post, every email, every DM should point there. The Open Door AI URL is a showcase. The FJQ URL is a magazine. The BA services URL is the MONEY page.

## Status

- Builds: DONE (3 HTML files, 0 em dashes, all 4 brand tokens)
- Screenshots: DONE in `BRAND-SYSTEM/BUILDS-SCREENSHOTS/`
- Local preview: Servers running on ports 8901, 8902, 8903 (will be killed at end of session)
- Public URLs: PENDING (5 min manual deploy)

The VistaCreate slide 1 replacement is also pending - the new cover PNG is at `BRAND-SYSTEM/BUILDS-SCREENSHOTS/ba-carousel-cover-slide-v2-1080.png`. Drop it into VistaCreate project 2 slide 1 to replace.
