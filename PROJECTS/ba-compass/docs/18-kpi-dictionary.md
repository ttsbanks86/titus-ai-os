# KPI Dictionary

**Company:** BrightCare Home Services (Fictional)  
**Document:** 18-kpi-dictionary.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## KPIs

### KPI-001: Shift Fill Rate

| Field | Value |
|-------|-------|
| KPI Name | Shift Fill Rate |
| Definition | Percentage of scheduled shifts that have a confirmed caregiver assignment |
| Formula | `(Confirmed Shifts / Total Scheduled Shifts) x 100` |
| Data Inputs | Total shifts scheduled, shifts with confirmed caregiver |
| Unit | Percentage (%) |
| Target | 95% |
| Warning Threshold | Below 90% |
| Owner | STK-002 Operations Manager |
| Refresh Frequency | Daily |
| Business Interpretation | Higher is better. Indicates scheduling effectiveness and staffing adequacy. |
| Limitations | Does not account for last-minute changes or caregiver no-shows after confirmation |
| Linked BR | BR-001 |

### KPI-002: Missed Shift Rate

| Field | Value |
|-------|-------|
| KPI Name | Missed Shift Rate |
| Definition | Percentage of scheduled shifts where no caregiver arrived |
| Formula | `(Missed Shifts / Total Scheduled Shifts) x 100` |
| Data Inputs | Total shifts scheduled, shifts marked as missed |
| Unit | Percentage (%) |
| Target | < 2% |
| Warning Threshold | Above 5% |
| Owner | STK-002 Operations Manager |
| Refresh Frequency | Daily |
| Business Interpretation | Lower is better. Missed shifts directly impact client care. |
| Limitations | Does not distinguish between prevented (filled by replacement) and actual missed shifts |
| Linked BR | BR-001, BR-002 |

### KPI-003: Late Arrival Rate

| Field | Value |
|-------|-------|
| KPI Name | Late Arrival Rate |
| Definition | Percentage of completed shifts where the caregiver arrived more than 15 minutes after scheduled start |
| Formula | `(Late Arrivals / Total Completed Shifts) x 100` |
| Data Inputs | Total completed shifts, shifts with arrival time > 15 min past scheduled start |
| Unit | Percentage (%) |
| Target | < 10% |
| Warning Threshold | Above 15% |
| Owner | STK-002 Operations Manager |
| Refresh Frequency | Per shift, aggregated weekly |
| Business Interpretation | Lower is better. Late arrivals reduce client satisfaction and care time. |
| Limitations | Does not capture severity of lateness (15 min vs 60 min) |
| Linked BR | BR-011 |

### KPI-004: Average Escalation Time

| Field | Value |
|-------|-------|
| KPI Name | Average Escalation Time |
| Definition | Average time between issue identification and initial escalation action |
| Formula | `SUM(Time from issue ID to first escalation for all issues) / Total Escalated Issues` |
| Data Inputs | Issue records with identification timestamp, escalation action timestamp |
| Unit | Minutes |
| Target | < 30 minutes |
| Warning Threshold | Above 60 minutes |
| Owner | STK-004 Care Coordinator |
| Refresh Frequency | Per issue, aggregated weekly |
| Business Interpretation | Lower is better. Faster escalation means quicker response to service failures. |
| Limitations | Only tracks time to first escalation, not total resolution time |
| Linked BR | BR-003 |

### KPI-005: Documentation Completion Rate

| Field | Value |
|-------|-------|
| KPI Name | Documentation Completion Rate |
| Definition | Percentage of completed shifts with service documentation completed within 24 hours |
| Formula | `(Shifts with Documentation Completed / Total Completed Shifts) x 100` |
| Data Inputs | Total completed shifts, shifts with documentation submitted |
| Unit | Percentage (%) |
| Target | 95% |
| Warning Threshold | Below 85% |
| Owner | STK-006 Quality Assurance Lead |
| Refresh Frequency | Daily |
| Business Interpretation | Higher is better. Incomplete documentation creates compliance and billing risk. |
| Limitations | Measures completion status, does not evaluate documentation quality |
| Linked BR | BR-005 |

### KPI-006: Open Staffing Gaps

| Field | Value |
|-------|-------|
| KPI Name | Open Staffing Gaps |
| Definition | Number of scheduled shifts within the next 48 hours that do not have an assigned caregiver |
| Formula | `Count of shifts without assigned caregiver in next 48 hours` |
| Data Inputs | All upcoming shifts, caregiver assignments |
| Unit | Count (integer) |
| Target | < 3 |
| Warning Threshold | Above 5 |
| Owner | STK-003 Scheduling Coordinator |
| Refresh Frequency | Real-time (every shift change) |
| Business Interpretation | Lower is better. Open gaps require immediate attention to prevent missed shifts. |
| Limitations | Does not account for difficulty of filling specific gaps (time of day, location) |
| Linked BR | BR-002 |

### KPI-007: Issue Resolution Time

| Field | Value |
|-------|-------|
| KPI Name | Issue Resolution Time |
| Definition | Average time from service issue identification to resolution confirmation |
| Formula | `SUM(Resolution time for all resolved issues) / Total Resolved Issues` |
| Data Inputs | Issue records with identification and resolution timestamps |
| Unit | Hours |
| Target | < 4 hours |
| Warning Threshold | Above 8 hours |
| Owner | STK-004 Care Coordinator |
| Refresh Frequency | Per issue, aggregated weekly |
| Business Interpretation | Lower is better. Faster resolution means better client service. |
| Limitations | Resolution is self-reported; may not reflect client satisfaction with resolution |
| Linked BR | BR-003, BR-004 |

### KPI-008: Follow-Up Completion Rate

| Field | Value |
|-------|-------|
| KPI Name | Follow-Up Completion Rate |
| Definition | Percentage of resolved issues that receive a scheduled follow-up within the required timeframe |
| Formula | `(Completed Follow-Ups / Required Follow-Ups) x 100` |
| Data Inputs | Required follow-up records, completed follow-up records |
| Unit | Percentage (%) |
| Target | 90% |
| Warning Threshold | Below 75% |
| Owner | STK-004 Care Coordinator |
| Refresh Frequency | Weekly |
| Business Interpretation | Higher is better. Follow-up ensures issues are truly resolved and patterns identified. |
| Limitations | Does not measure quality or outcome of follow-up interaction |
| Linked BR | BR-004 |

---

## KPI Data Consistency Verification

| Metric | Formula Consistency | Notes |
|--------|-------------------|-------|
| Shift Fill Rate + Missed Shift Rate | Not directly additive | Filled + Missed does not equal 100% because some shifts are cancelled or replaced |
| Documentation Completion Rate | Based on completed shifts only | Does not include cancelled or rescheduled shifts |
| Late Arrival Rate | Based on completed shifts | A missed shift is not included as a late arrival |
| Open Staffing Gaps | Point-in-time (next 48 hours) | Changes as gaps are filled or new gaps appear |
| Escalation Time vs Resolution Time | Related but distinct | Escalation is sub-step of resolution |

---

## KPI Summary

| ID | Name | Target | Warning | Unit | Refresh |
|----|------|--------|---------|------|---------|
| KPI-001 | Shift Fill Rate | 95% | < 90% | % | Daily |
| KPI-002 | Missed Shift Rate | < 2% | > 5% | % | Daily |
| KPI-003 | Late Arrival Rate | < 10% | > 15% | % | Weekly |
| KPI-004 | Average Escalation Time | < 30 min | > 60 min | Minutes | Weekly |
| KPI-005 | Documentation Completion Rate | 95% | < 85% | % | Daily |
| KPI-006 | Open Staffing Gaps | < 3 | > 5 | Count | Real-time |
| KPI-007 | Issue Resolution Time | < 4 hrs | > 8 hrs | Hours | Weekly |
| KPI-008 | Follow-Up Completion Rate | 90% | < 75% | % | Weekly |

---

## Related Documents

- 10-business-requirements.md — Business requirements linked to KPIs
- 15-requirements-traceability-matrix.md — RTM
- 19-data-dictionary.md — Data inputs for KPI calculations
