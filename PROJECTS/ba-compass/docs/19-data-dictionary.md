# Data Dictionary

**Company:** BrightCare Home Services (Fictional)  
**Document:** 19-data-dictionary.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Disclaimer

All entities and data described here are **synthetic and fictional**. No real personal information is represented.

---

## Entity: Shift

| Field | Type | Description | Required | Allowed Values | Example | Privacy | Validation |
|-------|------|-------------|----------|---------------|---------|---------|------------|
| shift_id | String (UUID) | Unique shift identifier | Yes | UUID format | "SFT-20260721-001" | None | Must be unique |
| client_id | String | Reference to client account | Yes | Valid client ID | "CLT-042" | Low (fictional) | Must exist in clients |
| caregiver_id | String (nullable) | Assigned caregiver | No | Valid caregiver ID or null | "CGW-018" | Low (fictional) | Must exist in caregivers if set |
| scheduled_date | Date | Shift date | Yes | Valid date | "2026-07-21" | None | Must be future or today |
| scheduled_start | Time | Shift start time | Yes | HH:MM format | "09:00" | None | Must be valid time |
| scheduled_end | Time | Shift end time | Yes | HH:MM format | "13:00" | None | Must be after start |
| status | String | Shift status | Yes | confirmed, unconfirmed, in_progress, completed, missed, cancelled | "confirmed" | None | Must be valid status |
| confirmation_time | DateTime (nullable) | When shift was confirmed | No | Valid datetime | "2026-07-20T14:30:00Z" | None | Must be before scheduled start |
| actual_arrival | Time (nullable) | Actual arrival time | No | HH:MM format | "09:12" | None | Must be valid time |
| documentation_status | String | Documentation status | Yes | complete, incomplete, not_required | "complete" | None | Must be valid value |
| documentation_time | DateTime (nullable) | When documentation was submitted | No | Valid datetime | "2026-07-21T15:30:00Z" | None | Must be after shift end |
| is_late | Boolean | Flag for late arrival | Yes | true, false | false | None | Calculated: actual_arrival > scheduled_start + 15min |
| notes | String (nullable) | Free-text notes | No | Any text | "Client requested extra assistance today" | Low | Max 500 chars |

---

## Entity: Caregiver

| Field | Type | Description | Required | Allowed Values | Example | Privacy | Validation |
|-------|------|-------------|----------|---------------|---------|---------|------------|
| caregiver_id | String (UUID) | Unique caregiver identifier | Yes | UUID format | "CGW-018" | Low | Must be unique |
| first_name | String | Caregiver first name (fictional) | Yes | Non-empty string | "Maria" | Low (fictional) | Fictional only |
| last_name | String | Caregiver last name (fictional) | Yes | Non-empty string | "Garcia" | Low (fictional) | Fictional only |
| status | String | Current employment status | Yes | active, on_leave, inactive | "active" | None | Must be valid status |
| availability | String | Typical availability pattern | Yes | full_time, part_time, weekend_only | "full_time" | None | Must be valid pattern |
| preferred_region | String | Service region preference | Yes | Non-empty string | "Northside" | None | Must be valid region |
| active_clients | Integer | Number of currently assigned clients | Yes | 0-10 | 3 | Low | Must match assignments |

---

## Entity: Client Account

| Field | Type | Description | Required | Allowed Values | Example | Privacy | Validation |
|-------|------|-------------|----------|---------------|---------|---------|------------|
| client_id | String (UUID) | Unique client identifier | Yes | UUID format | "CLT-042" | Low | Must be unique |
| first_name | String | Client first name (fictional) | Yes | Non-empty string | "Eleanor" | Low (fictional) | Fictional only |
| last_name | String | Client last name (fictional) | Yes | Non-empty string | "Whitfield" | Low (fictional) | Fictional only |
| region | String | Service region | Yes | Non-empty string | "Northside" | None | Must be valid region |
| care_level | String | Level of care needed | Yes | companion, personal, specialized | "personal" | None | Must be valid level |
| status | String | Account status | Yes | active, inactive, pending | "active" | None | Must be valid status |
| preferred_caregiver_id | String (nullable) | Preferred caregiver reference | No | Valid caregiver ID | "CGW-018" | Low | Must exist in caregivers |

---

## Entity: Assignment

| Field | Type | Description | Required | Allowed Values | Example | Privacy | Validation |
|-------|------|-------------|----------|---------------|---------|---------|------------|
| assignment_id | String (UUID) | Unique assignment identifier | Yes | UUID format | "ASN-20260721-001" | None | Must be unique |
| shift_id | String | Reference to shift | Yes | Valid shift ID | "SFT-20260721-001" | None | Must exist in shifts |
| caregiver_id | String | Reference to caregiver | Yes | Valid caregiver ID | "CGW-018" | Low | Must exist in caregivers |
| assigned_time | DateTime | When assignment was made | Yes | Valid datetime | "2026-07-20T10:00:00Z" | None | Must be before shift start |
| assignment_method | String | How assignment was made | Yes | auto, manual, replacement | "manual" | None | Must be valid method |
| confirmed | Boolean | Whether shift was confirmed | Yes | true, false | true | None | Boolean |

---

## Entity: Escalation

| Field | Type | Description | Required | Allowed Values | Example | Privacy | Validation |
|-------|------|-------------|----------|---------------|---------|---------|------------|
| escalation_id | String (UUID) | Unique escalation identifier | Yes | UUID format | "ESC-001" | None | Must be unique |
| shift_id | String | Reference to related shift | Yes | Valid shift ID | "SFT-20260721-001" | None | Must exist in shifts |
| issue_type | String | Type of issue | Yes | missed_shift, late_arrival, no_show, client_complaint, documentation_missing | "late_arrival" | None | Must be valid type |
| severity | String | Issue severity level | Yes | low, medium, high, critical | "high" | None | Must be valid severity |
| identified_time | DateTime | When issue was identified | Yes | Valid datetime | "2026-07-21T09:30:00Z" | None | Must be after shift start |
| escalation_time | DateTime (nullable) | When escalation action occurred | No | Valid datetime | "2026-07-21T09:45:00Z" | None | Must be after identified_time |
| resolved_time | DateTime (nullable) | When issue was resolved | No | Valid datetime | "2026-07-21T11:00:00Z" | None | Must be after escalation_time |
| status | String | Current escalation status | Yes | open, in_progress, resolved, closed | "resolved" | None | Must be valid status |
| owner | String | Person responsible | Yes | Non-empty string | "T. Chen (Care Coordinator)" | Low (fictional) | Must be valid fictional name |
| resolution_notes | String (nullable) | Notes on resolution | No | Any text | "Replacement caregiver dispatched" | Low | Max 1000 chars |

---

## Entity: Documentation Record

| Field | Type | Description | Required | Allowed Values | Example | Privacy | Validation |
|-------|------|-------------|----------|---------------|---------|---------|------------|
| doc_id | String (UUID) | Unique documentation identifier | Yes | UUID format | "DOC-001" | None | Must be unique |
| shift_id | String | Reference to shift | Yes | Valid shift ID | "SFT-20260721-001" | None | Must exist in shifts |
| caregiver_id | String | Reference to caregiver | Yes | Valid caregiver ID | "CGW-018" | Low | Must exist in caregivers |
| submitted_time | DateTime | When documentation was submitted | Yes | Valid datetime | "2026-07-21T14:00:00Z" | None | Must be after shift end |
| status | String | Documentation status | Yes | complete, incomplete, overdue | "complete" | None | Must be valid status |
| service_summary | String (nullable) | Summary of services provided | No | Any text | "Personal care, light housekeeping, medication reminder" | None | Max 1000 chars |

---

## Entity: Service Issue

| Field | Type | Description | Required | Allowed Values | Example | Privacy | Validation |
|-------|------|-------------|----------|---------------|---------|---------|------------|
| issue_id | String (UUID) | Unique issue identifier | Yes | UUID format | "ISS-001" | None | Must be unique |
| shift_id | String | Reference to related shift | Yes | Valid shift ID | "SFT-20260721-001" | None | Must exist in shifts |
| reported_by | String | Who reported the issue | Yes | Non-empty string | "Client Services Desk" | Low (fictional) | Fictional only |
| reported_time | DateTime | When issue was reported | Yes | Valid datetime | "2026-07-21T09:15:00Z" | None | Must be valid datetime |
| description | String | Description of the issue | Yes | Any text | "Caregiver not arrived at 9:00 AM start time" | Low | Max 2000 chars |
| category | String | Issue category | Yes | scheduling, attendance, quality, communication, documentation | "attendance" | None | Must be valid category |
| status | String | Issue status | Yes | open, in_progress, resolved | "resolved" | None | Must be valid status |

---

## Entity: Follow-Up Record

| Field | Type | Description | Required | Allowed Values | Example | Privacy | Validation |
|-------|------|-------------|----------|---------------|---------|---------|------------|
| followup_id | String (UUID) | Unique follow-up identifier | Yes | UUID format | "FUP-001" | None | Must be unique |
| issue_id | String | Reference to related issue | Yes | Valid issue ID | "ISS-001" | None | Must exist in issues |
| owner | String | Person responsible for follow-up | Yes | Non-empty string | "M. Rivera (QA)" | Low (fictional) | Fictional only |
| deadline | Date | Follow-up completion deadline | Yes | Valid date | "2026-07-23" | None | Must be future |
| completed_time | DateTime (nullable) | When follow-up was completed | No | Valid datetime | "2026-07-22T16:00:00Z" | None | Must be valid |
| status | String | Follow-up status | Yes | pending, in_progress, completed | "completed" | None | Must be valid status |
| notes | String (nullable) | Follow-up notes | No | Any text | "Client satisfied with resolution" | Low | Max 1000 chars |

---

## Entity: Requirement

| Field | Type | Description | Required | Allowed Values | Example | Privacy | Validation |
|-------|------|-------------|----------|---------------|---------|---------|------------|
| req_id | String | Unique requirement ID | Yes | BR-XXX, FR-XXX, NFR-XXX format | "BR-001" | None | Must match ID format |
| type | String | Requirement type | Yes | business, functional, nonfunctional | "business" | None | Must be valid type |
| statement | Text | Requirement description | Yes | Any text | "The system shall provide visibility..." | None | Max 5000 chars |
| priority | String | Priority level | Yes | high, medium, low | "high" | None | Must be valid priority |
| status | String | Current status | Yes | proposed, approved, in_progress, implemented | "proposed" | None | Must be valid status |

---

## Entity: Risk

| Field | Type | Description | Required | Allowed Values | Example | Privacy | Validation |
|-------|------|-------------|----------|---------------|---------|---------|------------|
| risk_id | String | Unique risk identifier | Yes | R-XXX format | "R-001" | None | Must match format |
| description | Text | Risk description | Yes | Any text | "Scope growth beyond portfolio needs" | None | Max 2000 chars |
| category | String | Risk category | Yes | scope, quality, privacy, usability, technical | "scope" | None | Must be valid category |
| likelihood | Integer | Likelihood rating (1-5) | Yes | 1-5 | 4 | None | Numeric range |
| impact | Integer | Impact rating (1-5) | Yes | 1-5 | 3 | None | Numeric range |
| risk_score | Integer | Calculated risk score | Yes | 1-25 | 12 | None | likelihood * impact |
| status | String | Risk status | Yes | active, mitigated, closed | "active" | None | Must be valid status |

---

## Entity: KPI Result

| Field | Type | Description | Required | Allowed Values | Example | Privacy | Validation |
|-------|------|-------------|----------|---------------|---------|---------|------------|
| kpi_id | String | KPI identifier | Yes | KPI-XXX format | "KPI-001" | None | Must match format |
| period | String | Time period | Yes | daily, weekly, monthly | "daily" | None | Must be valid period |
| period_date | Date | Period start date | Yes | Valid date | "2026-07-21" | None | Must be valid |
| actual_value | Float | Calculated KPI value | Yes | Numeric | 92.5 | None | Must match formula |
| target_value | Float | KPI target | Yes | Numeric | 95.0 | None | Defined in KPI dictionary |
| status | String | Performance status | Yes | on_track, warning, critical | "warning" | None | Comparison to target |

---

## Related Documents

- 18-kpi-dictionary.md — KPI definitions using these data entities
- 20-product-backlog.md — Data implementation tasks
