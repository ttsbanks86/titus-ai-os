# Vercel Deployment Guide — BA Compass

This guide walks through deploying BA Compass to Vercel. The application is configured for static export and requires no server runtime, database, or environment variables.

---

## Prerequisites

- A GitHub repository containing the BA Compass codebase
- A Vercel account (sign up at https://vercel.com using your GitHub account)
- Node.js 18+ installed locally (for verification build)
- Access to push to the repository's main branch

---

## Step 1: Prepare Your Repository

Ensure your repository is clean and the latest code is pushed:

```bash
git status                 # Confirm no uncommitted changes
git push origin main       # Push latest code
```

The repository should contain the entire project including `docs/`, `src/`, `public/`, and root configuration files (`next.config.ts`, `package.json`, `tsconfig.json`, etc.).

---

## Step 2: Import the Project in Vercel

1. Log in to your Vercel dashboard at https://vercel.com
2. Click **Add New** > **Project**
3. Select your BA Compass GitHub repository from the list
4. If the repository is not visible, click **Adjust GitHub App Permissions** and grant access

---

## Step 3: Configure Build Settings

Vercel auto-detects Next.js projects. Verify or set the following:

| Setting | Value |
|---------|-------|
| **Framework Preset** | Next.js (auto-detected) |
| **Root Directory** | Leave blank (default) |
| **Build Command** | `npm run build` |
| **Output Directory** | `out` (auto-detected from `next.config.ts`) |
| **Install Command** | `npm install` (auto-detected) |
| **Node.js Version** | 18.x or 20.x (Vercel default is fine) |

No other configuration is needed. The `next.config.ts` already sets `output: "export"` for static generation.

### Environment Variables

BA Compass requires **zero environment variables**. The `.env.example` file documents available variables, but none are required for build or runtime.

If you see "No server functions required" in the Vercel dashboard output, the configuration is correct.

---

## Step 4: Deploy

Click **Deploy**. Vercel will:

1. Clone the repository
2. Install dependencies with `npm install`
3. Run `npm run build` which:
   - Runs TypeScript type checking
   - Builds all 18+ static pages
   - Outputs to the `out/` directory
4. Deploy the static output to Vercel's global CDN

The initial deployment takes approximately 60-90 seconds. You will see a progress log in real time.

---

## Step 5: Verify Deployment

Once the build completes, Vercel assigns a `.vercel.app` domain (e.g., `ba-compass.vercel.app`).

Open the URL and verify:
- The landing page loads with the KPI snapshot
- All navigation links work
- Charts render on the dashboard
- The 5-minute recruiter tour functions

See `33-production-smoke-test.md` for the complete verification checklist.

---

## Step 6: Custom Domain (Optional)

To use a custom domain:

1. In the Vercel dashboard, go to your project > **Settings** > **Domains**
2. Enter your domain (e.g., `bacompass.yourname.com`)
3. Follow the DNS configuration instructions:
   - Add a CNAME record pointing `www` to `cname.vercel-dns.com`
   - Or configure nameservers for apex domain
4. Wait for DNS propagation (up to 48 hours, typically minutes)
5. Vercel automatically provisions an SSL certificate via Let's Encrypt

---

## Step 7: Continuous Deployment

Any push to the configured branch (default: `main`) automatically triggers a new deployment:

```bash
git add .
git commit -m "Update content"
git push origin main
# Vercel deploys automatically
```

Preview deployments are also available for pull requests. Vercel creates a unique preview URL for each PR, which is useful for reviewing changes before merging.

---

## Troubleshooting

### Build fails with "Command not found"

Ensure `package.json` is in the repository root and contains the build script:
```json
"scripts": {
  "build": "next build"
}
```

### Output directory is `out` but Vercel expects `.next`

This is expected. BA Compass uses `output: "export"` in `next.config.ts`, which produces a static `out/` directory. Vercel detects this automatically. Verify the setting in `next.config.ts`:
```typescript
const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true },
  reactStrictMode: true,
};
```

### Images not loading

Because this is a static export, the Next.js Image Optimization API is unavailable. This is already handled in `next.config.ts` with `images: { unoptimized: true }`. All images use standard `<img>` tags.

### 404 on direct navigation

Vercel serves `404.html` for unknown routes. BA Compass has a custom 404 page at `src/app/not-found/page.tsx`. Vercel handles this automatically for static exports.

### Preview deployment shows different content

Preview deployments build from the PR branch. If you have uncommitted changes, they will not appear. Commit and push all changes.

---

## Post-Deployment Checklist

After successful deployment, complete the smoke test in `33-production-smoke-test.md`.

Key items to verify:
- All 16 routes respond correctly
- Direct URL navigation works (not just clicking links)
- localStorage editing persists across page reloads
- Exports download correct content
- Charts render in the KPI dashboard
- Mobile navigation is functional
- 404 page renders for unknown routes
- Social preview appears on link sharing
- No mixed content warnings in the browser console
