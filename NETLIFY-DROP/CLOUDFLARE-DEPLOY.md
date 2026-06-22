# Cloudflare Pages Deployment - Titus Banks Sites
**Created:** 2026-06-06
**Sites to deploy:** 4 (opendoor, ba, fjq, audit)
**Tool:** Wrangler 4.98.0

## The 4 Sites

| Folder | Site | URL Pattern |
|---|---|---|
| `opendoor/` | Open Door AI Systems | `opendoor.pages.dev` |
| `ba/` | Business Analysis and Operations | `ba-tb.pages.dev` |
| `fjq/` | Faithful Journey Quest | `fjq-tb.pages.dev` |
| `audit/` | Faith and Operations Gap Audit | `audit-tb.pages.dev` |

## One-Time Setup (5 minutes)

### Step 1: Log in to Cloudflare via Wrangler
```powershell
wrangler login
```
This opens a browser. Approve the connection. Token is saved automatically.

### Step 2: Verify you're logged in
```powershell
wrangler whoami
```
Should show your Cloudflare account email and account ID.

## Deploy Each Site

For each of the 4 sites, run this pattern. Example for `opendoor`:

```powershell
# From the NETLIFY-DROP folder:
cd "C:\Users\tbank\Desktop\Live Cowork\NETLIFY-DROP"

# Create the project (first time only)
wrangler pages project create opendoor --production-branch=main

# Deploy
wrangler pages deploy opendoor --project-name=opendoor
```

Repeat for `ba`, `fjq`, `audit` — just swap the folder and project name.

## One-Command Deploy All (after first setup)

```powershell
cd "C:\Users\tbank\Desktop\Live Cowork\NETLIFY-DROP"
wrangler pages deploy opendoor --project-name=opendoor
wrangler pages deploy ba --project-name=ba
wrangler pages deploy fjq --project-name=fjq
wrangler pages deploy audit --project-name=audit
```

## Custom Domains (After Deploy)

For each site, in Cloudflare dashboard:
1. Go to Workers & Pages > [site-name]
2. Click Custom domains tab
3. Add `opendoor.titusbanks.com` (or your domain)
4. Cloudflare auto-configures DNS

Or via CLI:
```powershell
wrangler pages domain add opendoor.titusbanks.com opendoor
```

## Why Cloudflare Pages vs Netlify Drop

| Feature | Cloudflare Pages | Netlify Drop |
|---------|------------------|--------------|
| Free tier | Unlimited sites, 500 builds/mo | 100 GB bandwidth/mo |
| Global CDN | 300+ cities | ~15 regions |
| Custom domains | Free, auto DNS | Free, manual DNS |
| Serverless functions | Yes (Workers) | Yes (Functions) |
| Build time | Seconds | Seconds |
| Account required | Yes (free) | No (first drop) |

**Bottom line:** Cloudflare Pages is faster globally and gives more control. Netlify Drop is the fastest "zero account" path. Both are free.

## Re-Deploying After Edits

If you edit any HTML file inside a subfolder:
```powershell
cd "C:\Users\tbank\Desktop\Live Cowork\NETLIFY-DROP"
wrangler pages deploy opendoor --project-name=opendoor
```

The deploy overwrites the previous version. No downtime.
