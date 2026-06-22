# Email Triage SOP

## 1. Purpose
Standardize email management to ensure timely response, proper categorization, and consistent follow-up across all team communications.

## 2. Scope
All incoming emails across business accounts. Covers inbox processing, categorization, response drafting, and follow-up scheduling.

## 3. Prerequisites
- Access to Gmail via Gmail MCP
- Labels configured (see `gmail-automation` skill)
- Email templates loaded from `Templates/email-templates.md`
- Lead database access (CRM or spreadsheet)

## 4. Procedure

### Step 1: Initial Triage (Every 2 Hours)
```
1. Load Gmail inbox via gmail-automation
2. Sort by newest first
3. For each unread email, classify:
   - [ ] URGENT — requires response within 1 hour
   - [ ] NORMAL — requires response within 24 hours
   - [ ] LOW — informational, no response needed
   - [ ] SPAM/JUNK — archive or delete
   - [ ] LEAD — potential business opportunity
```

### Step 2: Apply Labels
```
Labels to apply:
- @Urgent
- @Respond-Today
- @Follow-Up
- @Lead
- @Invoice
- @Newsletter
- @Team
- @Client
```

### Step 3: Draft Responses
```
1. For URGENT: Draft response immediately using email-templates.md
2. For NORMAL: Queue for next response batch
3. For LOW: Archive with label, no response needed
4. For LEAD: Transfer to lead management SOP
```

### Step 4: Follow-Up Scheduling
```
1. If email requires follow-up, add to calendar/task system
2. Set reminder for appropriate interval:
   - Sales lead: 3 days
   - Client request: 1 business day
   - Internal: 2 business days
   - Vendor: 3 business days
```

## 5. Quality Checks
- [ ] All urgent emails responded to within 1 hour
- [ ] All normal emails responded to within 24 hours
- [ ] Labels applied correctly to all processed emails
- [ ] Follow-ups scheduled for all emails requiring action
- [ ] No emails left unprocessed for more than 48 hours

## 6. Escalation Path
| Issue | Escalate To | Method |
|-------|------------|--------|
| Client complaint | Team Lead | Direct message + email CC |
| Legal/compliance issue | Legal Contact | Email with full thread |
| Technical failure | IT Support | Support ticket |
| VIP urgent | Executive Team | Phone call |

## 7. Version History
| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2026-06-07 | Initial SOP creation | Admin |

---
*Last Updated: 2026-06-07*
