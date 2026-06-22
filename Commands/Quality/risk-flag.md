# Risk Flag

## Purpose
Identify, assess, and recommend mitigation for project or operational risks.

## Inputs
- Project or initiative name
- Risk context (scope, timeline, resources, dependencies)
- Risk categories to assess (technical, resource, schedule, external)
- Historical risks (optional)

## Outputs
- Risk register with severity and probability
- Risk heat map data
- Mitigation strategies for each risk
- Early warning indicators
- Risk ownership assignments

## Workflow
1. Gather project context and known concerns
2. Brainstorm risks across categories:
   - **Technical**: Architecture, integration, performance
   - **Resource**: Staffing, skills, availability
   - **Schedule**: Timeline, dependencies, external factors
   - **Financial**: Budget, cost overruns, ROI
   - **Stakeholder**: Alignment, communication, expectations
3. For each risk, assess:
   - Probability: Low (1-3), Medium (4-6), High (7-10)
   - Impact: Low (1-3), Medium (4-6), High (7-10)
   - Risk Score: Probability × Impact
4. Classify risk level:
   - 🔴 Critical: Score ≥ 49
   - 🟠 High: Score 25-48
   - 🟡 Medium: Score 10-24
   - 🟢 Low: Score < 10
5. Develop mitigation strategies and early warning indicators

## Example Execution
```
/risk-flag --project "Dashboard v2 Launch" --context "tight timeline, new tech stack"

Output:
━━━ RISK REGISTER: Dashboard v2 Launch ━━━

🔴 CRITICAL RISKS (Score ≥ 49)
  None identified.

🟠 HIGH RISKS (Score 25-48)
  | Risk                          | Prob | Impact | Score | Owner  |
  |-------------------------------|------|--------|-------|--------|
  | Real-time sync API unreliable | 7    | 7      | 49    | Mike   |
  | Sarah overloaded (launch lead)| 8    | 6      | 48    | Ops    |

🟡 MEDIUM RISKS (Score 10-24)
  | Risk                          | Prob | Impact | Score | Owner  |
  |-------------------------------|------|--------|-------|--------|
  | Testing bottleneck at EOW     | 6    | 5      | 30    | Jess   |
  | Client feedback delays launch | 5    | 4      | 20    | PM     |
  | Scope creep from stakeholders | 4    | 5      | 20    | PM     |

🟢 LOW RISKS (Score < 10)
  | Risk                          | Prob | Impact | Score | Owner  |
  |-------------------------------|------|--------|-------|--------|
  | Minor UI bugs post-launch     | 5    | 2      | 10    | Team   |

🛡️ MITIGATION STRATEGIES
  1. Real-time sync API (Score: 49):
     - Mitigation: Set up mock API for testing; have fallback to polling
     - Trigger: If API fails 2x in testing, escalate to vendor
     - Owner: Mike

  2. Sarah overloaded (Score: 48):
     - Mitigation: Redistribute 2 client tickets to Jess
     - Trigger: If Sarah exceeds 90% capacity, auto-defer non-critical tasks
     - Owner: Ops

⚠️ EARLY WARNING INDICATORS
  - If sync API test fails before June 10 → escalate immediately
  - If Sarah logs >45 hours in a week → trigger rebalance
  - If client feedback not received by June 11 → follow up and escalate

📅 RISK REVIEW DATE: June 12, 2026 (mid-sprint)
```

## Validation Checks
- Confirm probability and impact scores are justified with evidence
- Ensure each critical/high risk has a mitigation strategy
- Verify risk owners are identified and available
- Check that early warning indicators are measurable and triggerable
- Validate that risk scores are recalculated at each review
