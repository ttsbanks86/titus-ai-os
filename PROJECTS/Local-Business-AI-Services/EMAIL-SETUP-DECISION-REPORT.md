# Email Setup Decision Report
## Review & Lead Recovery System
**Date:** 2026-06-07
**Status:** READY FOR CEO APPROVAL

---

## 1. Domain Availability (All Confirmed Available)

| Domain | Available | Price | Recommended? |
|--------|-----------|-------|--------------|
| reviewleadrecovery.com | YES | $13.48/yr | **RECOMMENDED** |
| reviewleadrecoverysystems.com | YES | $13.48/yr | Backup |
| leadreviewrecovery.com | YES | $13.48/yr | Backup |
| titusbanks.com | YES | $13.48/yr | Personal brand only |

**Recommendation:** `reviewleadrecovery.com`
- Shortest, cleanest, easiest to say on phone
- Matches business name "Review & Lead Recovery"
- Easy for customers to remember and type

---

## 2. Email Provider Comparison

| Feature | Microsoft 365 Business Basic | Google Workspace Business Starter |
|---------|------------------------------|-----------------------------------|
| **Price (annual)** | $6.00/user/month | $7.00/user/month |
| **Price (monthly)** | $7.20/user/month | $8.40/user/month |
| **Annual cost (1 user)** | **$72.00** | **$84.00** |
| **Email storage** | 50 GB mailbox | 30 GB pooled |
| **Cloud storage** | 1 TB OneDrive | 30 GB Drive |
| **Uptime SLA** | 99.9% | 99.9% |
| **Custom domain email** | Yes (titus@reviewleadrecovery.com) | Yes |
| **Calendar** | Outlook | Google Calendar |
| **Video meetings** | Teams (included) | Google Meet |
| **Spam/malware protection** | Exchange Online Protection | Google spam filtering |
| **Admin console** | Yes | Yes |
| **Support** | Phone + web | Phone + web |

**Recommendation:** Microsoft 365 Business Basic ($6/month)
- $12/year cheaper than Google Workspace
- 50 GB mailbox vs 30 GB (better for outreach volume)
- Teams included (useful for future client calls)
- Familiar Outlook interface
- Already in your existing Microsoft 365 tools

---

## 3. Cost Summary

### Option A: Microsoft 365 (RECOMMENDED)

| Item | First Month | First Year |
|------|-------------|------------|
| Domain: reviewleadrecovery.com | $13.48 | $13.48 |
| Microsoft 365 Business Basic (1 user) | $6.00 | $72.00 |
| Email alias: support@reviewleadrecovery.com | $0 | $0 |
| **TOTAL** | **$19.48** | **$85.48** |

### Option B: Google Workspace

| Item | First Month | First Year |
|------|-------------|------------|
| Domain: reviewleadrecovery.com | $13.48 | $13.48 |
| Google Workspace Business Starter (1 user) | $7.00 | $84.00 |
| Email alias: support@reviewleadrecovery.com | $0 | $0 |
| **TOTAL** | **$20.48** | **$97.48** |

**Savings with Microsoft 365: $12/year**

---

## 4. Recommended Email Setup

| Email | Purpose | Type |
|-------|---------|------|
| titus@reviewleadrecovery.com | Primary business email | Main mailbox |
| support@reviewleadrecovery.com | Customer inquiries | Alias (free) |
| info@reviewleadrecovery.com | General inquiries | Alias (free, optional) |

**Phone:** Google Voice (free) — forward to personal cell for now

---

## 5. Step-by-Step Setup Instructions

### Phase 1: Domain Purchase (10 minutes)
1. Go to [Cloudflare Registrar](https://www.cloudflare.com/products/registrar/) or [Namecheap](https://www.namecheap.com)
2. Search for `reviewleadrecovery.com`
3. Add to cart ($13.48/year)
4. Complete checkout (create account if needed)
5. Enable WHOIS privacy (free at both registrars)
6. **DO NOT enable auto-renew yet** — test first

### Phase 2: Microsoft 365 Setup (20 minutes)
1. Go to [microsoft.com/microsoft-365/business/microsoft-365-business-basic](https://www.microsoft.com/en-us/microsoft-365/business/microsoft-365-business-basic)
2. Click "Try for free" or "Buy now"
3. Enter business name: **Review & Lead Recovery Systems**
4. Enter your name and contact info
5. Enter credit card for $6/month (annual plan)
6. Choose "I already own a domain" → enter `reviewleadrecovery.com`
7. Microsoft will guide you to update DNS records

### Phase 3: DNS Configuration (15 minutes)
1. Log into your domain registrar (Cloudflare or Namecheap)
2. Add these DNS records from Microsoft:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| MX | @ | yourdomain-com.mail.protection.outlook.com | 3600 |
| TXT | @ | MS=msXXXXXXXX | 3600 |
| TXT | @ | v=spf1 include:spf.protection.outlook.com ~all | 3600 |
| CNAME | autodiscover | autodiscover.outlook.com | 3600 |

3. Wait 15-30 minutes for DNS propagation
4. Microsoft will verify automatically

### Phase 4: Email Configuration (10 minutes)
1. Log into [outlook.office.com](https://outlook.office.com)
2. Create password for titus@reviewleadrecovery.com
3. Go to Settings → Mail → Accounts → Aliases
4. Add alias: support@reviewleadrecovery.com
5. Add alias: info@reviewleadrecovery.com (optional)
6. Test sending from each alias

### Phase 5: Google Voice Setup (10 minutes)
1. Go to [voice.google.com](https://voice.google.com)
2. Sign in with personal Google account
3. Choose a Seattle-area number (206, 425, or 253 area code)
4. Forward calls to personal cell
5. Test call/text

---

## 6. Risks Before Purchase

| Risk | Impact | Mitigation |
|------|--------|------------|
| Domain not available at checkout | Can't buy domain | Check availability NOW (confirmed available as of 2026-06-07) |
| DNS propagation delay | Email setup takes longer | Allow 24-48 hours; most propagation completes in 1-4 hours |
| Microsoft 365 price increase | Higher costs | Annual plan locks price for 12 months |
| Domain auto-renews at higher price | Unexpected charge | Disable auto-renew; manually renew at $13.48/yr |
| Google Voice number not available | Need different area code | Try multiple area codes; Seattle has plenty |
| Personal cell exposed | Privacy risk | Use Google Voice for ALL business communications |
| Business name not registered | Legal risk | File WA state LLC ($200) — NOT required for email setup, but recommended for business legitimacy |

---

## 7. CEO Action Items

1. **APPROVE domain:** reviewleadrecovery.com
2. **APPROVE email provider:** Microsoft 365 Business Basic ($6/month)
3. **APPROVE email addresses:** titus@, support@, info@
4. **PURCHASE domain** ($13.48) — I will guide you step by step
5. **SET UP Microsoft 365** ($6/month) — I will guide you step by step
6. **SET UP Google Voice** (free) — I will guide you step by step
7. **UPDATE outreach templates** with new email and phone — I will do this after setup

---

## 8. Decision Template

**CEO Decision:**

- [ ] APPROVED: Domain = reviewleadrecovery.com
- [ ] APPROVED: Email provider = Microsoft 365 Business Basic
- [ ] APPROVED: Email addresses = titus@, support@, info@
- [ ] APPROVED: Phone = Google Voice
- [ ] READY TO PURCHASE: Domain ($13.48) + Microsoft 365 ($6/month)

**Total first-month cost: $19.48**
**Total yearly cost: $85.48**
