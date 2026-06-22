# Appointment Setting Script — Booking the Sales Call

---

## Opening

"Great. So you're interested in learning more about how I can help {{Business Name}} get more Google reviews and follow up with missed leads. Let me ask you a few quick questions to make sure this is a good fit."

---

## Qualifying Questions

1. "How many Google reviews does {{Business Name}} currently have?"
2. "How many of those reviews have you responded to?"
3. "How many customers do you get per week?"
4. "How do you currently follow up with leads?"
5. "What's your average job value?"

---

## Booking the Call

"Perfect. Based on what you've told me, I think I can help. I'd love to show you exactly what I'd do for {{Business Name}}. Would a quick 15-minute call work better on Tuesday or Thursday?"

**If Tuesday:** "Great. Tuesday at {{Time}} work for you?"
**If Thursday:** "Great. Thursday at {{Time}} work for you?"

**If neither works:** "No problem. What day and time works better for you?"

---

## Confirmation

"Perfect. So that's {{Day}} at {{Time}}. I'll send you a calendar invite with a Zoom link. Is that the best email address to use?"

**If yes:** "Great. You'll get the invite in the next 5 minutes. Looking forward to it, {{First Name}}."

**If no:** "No problem. What's the best email address?"

---

## Pre-Call Prep

After booking the call:
1. Send calendar invite with Zoom link
2. Send confirmation email (see template below)
3. Review mini-audit notes
4. Prepare personalized recommendations
5. Log call in LEAD-TRACKER.csv
6. Update status: "Call Booked — {{Date}}"

---

## Confirmation Email Template

**Subject:** Our call on {{Day}} — {{Business Name}}

---

Hi {{First Name}},

Looking forward to our call on {{Day}} at {{Time}}.

Here's the Zoom link: {{Zoom Link}}

I'll walk you through:
- What I found in my audit of {{Business Name}}'s online presence
- How I help businesses like yours get more Google reviews
- A simple system for following up with missed leads

Talk soon,
Titus

---

**Notes:**
- Always book the call before ending the conversation
- Offer specific days and times (don't say "sometime next week")
- Send calendar invite immediately after booking
- Send confirmation email within 15 minutes
- Log the call in LEAD-TRACKER.csv immediately after
- Update status: "Call Booked — {{Date}}"
- Set reminder for 1 hour before call

**Template Variables:**
- `{{Business Name}}` — Business name from Google Maps
- `{{First Name}}` — Contact name if available, otherwise use "there"
- `{{Day}}` — Day of the week for the call
- `{{Time}}` — Time for the call
- `{{Zoom Link}}` — Zoom meeting link
