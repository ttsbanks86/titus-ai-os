# Create Offer

## Purpose
Generate a personalized offer based on lead profile and pain points.

## Inputs
- Lead profile (company, role, industry, size)
- Pain points or challenges identified
- Product/service fit
- Pricing tier or discount authority
- Offer type (demo, trial, consultation, custom proposal)

## Outputs
- Personalized offer message
- Value proposition tailored to lead
- Pricing or package recommendation
- Call-to-action
- Follow-up sequence suggestion

## Workflow
1. Analyze lead profile and identified pain points
2. Map product/service features to their specific needs
3. Craft personalized value proposition
4. Select appropriate offer type based on lead temperature
5. Generate offer message with clear CTA
6. Suggest follow-up cadence

## Example Execution
```
/create-offer --lead "DataFlow" --pain "scaling sales ops, onboarding 10 SDRs" --tier "professional" --type demo

Output:
━━━ OFFER: DataFlow | Sarah Chen, VP Sales ━━━

🎯 OFFER TYPE: Personalized Demo

📧 EMAIL DRAFT

Subject: Scaling DataFlow's sales team (quick idea for you)

Hi Sarah,

Congrats on the Series B – exciting times at DataFlow!

I noticed you're scaling your SDR team (congrats on the hires!). When teams grow that fast, the biggest challenge is usually getting everyone ramped consistently without burning out your senior reps.

We helped [Similar Company] solve exactly this when they went from 5 to 15 SDRs in 90 days. Their ramp time dropped from 6 weeks to 3 weeks, and their manager saved 12 hours/week on process overhead.

Would a 20-minute walkthrough be useful? I can show you exactly how they did it and whether it'd work for your HubSpot setup.

Worth a quick look?

[Your Name]

━━━

💡 VALUE PROPOSITION (for Sarah specifically)
  "Get your 10 new SDRs productive in half the time, without pulling your senior reps into onboarding full-time."

💰 PRICING RECOMMENDATION
  Tier: Professional
  Price: $2,400/mo (10 users)
  Discount: 15% annual = $2,040/mo
  ROI pitch: "Pays for itself in 2 weeks of faster ramp"

📞 FOLLOW-UP SEQUENCE
  | Day | Channel  | Action                              |
  |-----|----------|-------------------------------------|
  | 0   | Email    | Send personalized offer above       |
  | 1   | LinkedIn | Connect with Sarah + note           |
  | 3   | Email    | Follow up with case study link      |
  | 5   | LinkedIn | Share relevant content (sales ops)  |
  | 7   | Email    | Final follow-up + alternative CTA   |
  | 10  | Phone    | If no response, direct call         |

📊 SUCCESS METRICS
  Target: Demo booked within 7 days
  Expected response rate: 25-30%
  Conversion to opportunity: 40%
```

## Validation Checks
- Confirm offer aligns with lead's actual pain points
- Verify pricing and discount are within authorized range
- Ensure personalization is genuine (not templated)
- Check that value proposition is specific to the lead
- Validate follow-up sequence is appropriate for lead temperature
