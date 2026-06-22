# n8n Setup Guide
## Book Marketing Automation System

**Date:** June 10, 2026  
**Status:** n8n Running on http://localhost:5678

---

## Step 1: Create API Key

1. Open n8n: http://localhost:5678
2. Click **Settings** (gear icon, bottom left)
3. Click **API** in the left sidebar
4. Click **Create API Key**
5. Copy the API key
6. Save it somewhere safe

---

## Step 2: Import Workflows

Once you have the API key, run these commands in PowerShell:

```powershell
# Set your API key
$apiKey = "YOUR_API_KEY_HERE"

# Import Book Launch Main Workflow
$headers = @{
    "X-N8N-API-KEY" = $apiKey
    "Content-Type" = "application/json"
}
$body = Get-Content -Path "C:\Users\tbank\Desktop\Live Cowork\BOOK-MARKETING-SYSTEM\01_N8N_WORKFLOWS\book-launch-main.json" -Raw
Invoke-RestMethod -Uri "http://localhost:5678/api/v1/workflows" -Method Post -Body $body -Headers $headers

# Import Email Sequence Workflow
$body = Get-Content -Path "C:\Users\tbank\Desktop\Live Cowork\BOOK-MARKETING-SYSTEM\01_N8N_WORKFLOWS\email-sequence.json" -Raw
Invoke-RestMethod -Uri "http://localhost:5678/api/v1/workflows" -Method Post -Body $body -Headers $headers

# Import Social Scheduler Workflow
$body = Get-Content -Path "C:\Users\tbank\Desktop\Live Cowork\BOOK-MARKETING-SYSTEM\01_N8N_WORKFLOWS\social-scheduler.json" -Raw
Invoke-RestMethod -Uri "http://localhost:5678/api/v1/workflows" -Method Post -Body $body -Headers $headers

# Import Review Collector Workflow
$body = Get-Content -Path "C:\Users\tbank\Desktop\Live Cowork\BOOK-MARKETING-SYSTEM\01_N8N_WORKFLOWS\review-collector.json" -Raw
Invoke-RestMethod -Uri "http://localhost:5678/api/v1/workflows" -Method Post -Body $body -Headers $headers
```

---

## Step 3: Configure Credentials

### Email (Gmail/SMTP)
1. In n8n, go to **Credentials**
2. Click **Add Credential**
3. Search for **SMTP** or **Gmail**
4. Enter your email credentials
5. Test the connection

### Social Media (Optional)
1. Add **Facebook** credential
2. Add **Instagram** credential
3. Add **Twitter** credential

---

## Step 4: Activate Workflows

1. Go to **Workflows** in n8n
2. Find each imported workflow
3. Toggle the **Active** switch to ON
4. Verify the schedule is correct

---

## Workflow Status

| Workflow | Status | Schedule |
|----------|--------|----------|
| Book Launch Main | ⏳ | Daily 9 AM |
| Email Sequence | ⏳ | Mon/Wed/Fri 9 AM |
| Social Scheduler | ⏳ | Daily 10 AM |
| Review Collector | ⏳ | Weekly Monday 10 AM |

---

*Guide by Titus Banks AI Operating System*
*Last updated: June 10, 2026*
