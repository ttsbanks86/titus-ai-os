# Outreach Sequence

## Purpose
Create a multi-touch outreach sequence for lead engagement.

## Inputs
- Lead profile and contact information
- Sequence goal (demo, meeting, content download)
- Sequence length (5, 7, or 10 touchpoints)
- Channels (email, LinkedIn, phone, SMS)
- Timing preferences (business hours, frequency)

## Outputs
- Step-by-step sequence with timing
- Message templates for each touchpoint
- Channel mix and cadence
- Personalization variables
- Success metrics and benchmarks

## Workflow
1. Define sequence goal and target outcome
2. Design touchpoint cadence:
   - Space touches 2-3 days apart
   - Mix channels for variety
   - Front-load high-value touches
3. Write message templates with personalization variables
4. Include conditional logic (if opened/clicked, then X; else Y)
5. Define exit conditions (replied, booked, bounced)
6. Set success benchmarks

## Example Execution
```
/outreach-sequence --lead "DataFlow/Sarah Chen" --goal "book-demo" --length 7 --channels "email,linkedin"

Output:
━━━ OUTREACH SEQUENCE: DataFlow | Sarah Chen ━━━
Goal: Book Demo | Length: 7 touches | Duration: 14 days

📅 SEQUENCE CADENCE

DAY 1 (Tuesday) — Email
  Subject: Quick idea for scaling DataFlow's SDR team
  Body: Hi Sarah,
  [Personalized opener referencing Series B + SDR hiring]
  [Value prop: half the ramp time, 12 hrs/week saved]
  [CTA: 20-minute walkthrough?]
  [Signature]

DAY 2 (Wednesday) — LinkedIn Connection
  Connection note: "Hi Sarah – congrats on the Series B! Would love to connect and share how we've helped similar SaaS teams scale sales ops."

DAY 4 (Thursday) — Email (Follow-up)
  Subject: Re: Quick idea for scaling DataFlow's SDR team
  Body: Sarah,
  [Reference to first email]
  [Add social proof: case study link]
  [CTA: Worth a quick look?]

DAY 6 (Saturday) — LinkedIn Content Share
  Share relevant post or article about scaling sales teams
  Comment: "Thought this might be relevant given DataFlow's growth!"

DAY 8 (Monday) — Email (Value-Add)
  Subject: SDR ramp benchmarks for SaaS teams
  Body: Sarah,
  [Share useful resource or data]
  [Soft CTA: Let me know if you'd like to discuss]

DAY 10 (Wednesday) — LinkedIn Message
  "Hi Sarah – wanted to bump this in case it got buried. Happy to share how [Similar Company] ramped 10 SDRs in 3 weeks. Worth 15 minutes?"

DAY 12 (Friday) — Email (Break-up)
  Subject: Should I close the loop?
  Body: Sarah,
  [Acknowledge timing may not be right]
  [Offer to reconnect later]
  [Final CTA: Reply STOP if not interested]

📊 EXIT CONDITIONS
  - Replied → Exit sequence, enter nurture
  - Booked demo → Exit sequence, enter onboarding
  - Bounced → Flag for list cleanup
  - Completed all 7 → Move to monthly nurture

📈 BENCHMARKS
  Open rate target: 35-45%
  Reply rate target: 10-15%
  Demo booking rate: 5-8%
  Sequence completion: 80%

⚙️ PERSONALIZATION VARIABLES
  {{first_name}} = Sarah
  {{company}} = DataFlow
  {{trigger}} = Series B funding + SDR hiring
  {{case_study}} = [Similar Company success story]
  {{mutual_connection}} = [If applicable]
```

## Validation Checks
- Confirm sequence timing doesn't cluster on weekends (unless intentional)
- Verify all personalization variables are populated
- Check that messages are not repetitive or spammy
- Ensure exit conditions are clearly defined
- Validate that sequence length is appropriate for lead temperature
