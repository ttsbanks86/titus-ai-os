---
owner: Titus
domain: Reference
status: Active
priority: High
project: TKOS
area: Evidence Governance
created: 2026-07-12
updated: 2026-07-12
reviewed: 2026-07-12
related:
  - "[[Knowledge Standards]]"
  - "[[Batch 005 Evidence Search Log]]"
  - "[[Evidence Needed from Titus]]"
tags:
  - tkos/evidence
  - governance
---
# Evidence Registry

Evidence order: official credential, official registration, official school record, official employer/application confirmation, email, calendar, user tracker, general note.

## CourseCareers completion

```yaml
fact: Titus Banks completed the CourseCareers Information Technology Course on January 2, 2026.
owner: Titus
domain: Titus
evidence_type: Official certificate
source_file: 10-Archive/.../Attachments/PDFs/file_00000000a4ac720c862ad77f0317e791-CourseCareersCertificate.jpeg.pdf
source_date: 2026-01-02
verified_date: 2026-07-12
confidence: 100
status: Verified
related_record: "[[Resume Source of Truth]]"
notes: SHA256 D4CCED644B753C8C13E0C4B33ADA8CE634B17CBD7D6B36C0B6A6339EA8D1A3F5. Original retained in place.
```

## MDiv institution and program plan

```yaml
fact: Mosaic Christian College issued a degree plan for Titus Banks for Master of Divinity - Church Ministry specialization (72 Hours).
owner: Titus
domain: Titus
evidence_type: Official school record
source_file: 10-Archive/.../Attachments/PDFs/file_00000000bddc71f593d96a0e3b03bb2f-Banks Titus MDiv.pdf
source_date: 2026-04-23
verified_date: 2026-07-12
confidence: 100
status: Verified
related_record: "[[Master of Divinity Hub]]"
notes: SHA256 3F4DD72FBCBA69167C3F4AAD66B434DD2934D1EF09ED9194ACB9D52E05D2BC8A. Verifies degree plan and curriculum, not enrollment or current registration.
```

## MDiv enrollment

```yaml
fact: Titus is currently enrolled in the Mosaic Christian College MDiv program.
owner: Titus
domain: Titus
evidence_type: General note plus degree plan
source_file: Multiple TKOS summaries and Banks Titus MDiv.pdf
source_date:
verified_date: 2026-07-12
confidence: Review Required
status: Partially Verified
related_record: "[[Master of Divinity Hub]]"
notes: The degree plan names Titus and the program but does not state current enrollment, term, registered courses, or academic standing.
```

## WGU program evidence

```yaml
fact: A WGU transfer evaluation was prepared for Bachelor of Science Information Technology Management with 72 transfer competency units.
owner: Titus
domain: Titus
evidence_type: Official school record
source_file: 10-Archive/.../Attachments/PDFs/file_0000000092f071fda10d415eeed8816d-WGU transcript .pdf
source_date: 2025-12-03
verified_date: 2026-07-12
confidence: 100
status: Verified
related_record: "[[Resume Source of Truth]]"
notes: SHA256 AE43A9B2B6DD256CEB490DEC0AED8BDAC4BE4FA5818D2CFBA575F3F379760871. This is a pre-enrollment transfer evaluation and does not prove graduation.
```

## Upcoming ISC2 exam date

```yaml
fact: An upcoming ISC2 exam is recorded for July 28, 2026.
owner: Titus
domain: Titus
evidence_type: General notes and daily countdowns
source_file: My-Goals.md, Personal-Context.md, Daily Notes 2026-07-07 through 2026-07-11
source_date: 2026-07-07 to 2026-07-11
verified_date: 2026-07-12
confidence: Review Required
status: Partially Verified
related_record: "[[ISC2 Exam Command Center]]"
notes: No Pearson VUE or ISC2 registration confirmation was found. Exact exam name remains unverified.
```

## Completed ISC2 credential claim

```yaml
fact: Titus has a completed ISC2 credential.
owner: Titus
domain: Titus
evidence_type: General summaries only
source_file: No official artifact found
source_date:
verified_date: 2026-07-12
confidence: 0
status: Unverified
related_record: "[[ISC2 Credentials Registry]]"
notes: No certificate, digital badge, score report, credential record, or pass confirmation was found.
```

## PM resume claims

```yaml
fact: Archived PM resume files contain Titus-authored employment, internship, skills, and metric claims.
owner: Titus
domain: Titus
evidence_type: User-authored resume
source_file: Titus_Banks_PM_Resume.docx and Titus_Banks_PM_Resume_Federal.docx
source_date:
verified_date: 2026-07-12
confidence: 70
status: Partially Verified
related_record: "[[Resume Source of Truth]]"
notes: SHA256 6757638304862F21CCA3551D3CA1E1EB1B76CD77F61153DA7E27782F7D1F6A15 and 92D88ECE0C0913199B89F82E6D1404B39B074D012F95BD8D42AFCF6ECEA986DC. Resume wording supports provenance but not independent verification of metrics.
```
