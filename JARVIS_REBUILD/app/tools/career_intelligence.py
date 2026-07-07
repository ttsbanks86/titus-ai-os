"""Career Intelligence Engine for Jarvis.

Finds, scores, ranks, and tracks job opportunities from Gmail alerts.
When a USAJobs API key is available, it can also search USAJobs directly.

Job scoring (0-100):
- Resume match: 30 points (keyword overlap with target roles and skills)
- Pay: 20 points ($35-40/hr = 20, $30-35 = 15, $25-30 = 10)
- Remote/Dallas fit: 15 points (remote=15, dallas=15, seattle=10, other=5)
- Low barrier to entry: 15 points (BA required only=15, BA+2yr=10, BA+5yr=5)
- Career growth: 10 points (growth potential at company)
- Application effort: 10 points (easy apply=10, standard=7, long app=3)

Priority:
- P1 (85-100): Apply immediately
- P2 (70-84): Apply today  
- P3 (55-69): Review this week
- Ignore (<55): Skip unless unusual value
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from app.config import AppConfig
from app.tools.email import GmailReadOnlyClient, EmailSummary


# Target job titles for scoring
PRIMARY_ROLES = [
    "business analyst", "business systems analyst", "business intelligence analyst",
    "data analyst", "project coordinator", "program coordinator",
    "grc analyst", "compliance analyst", "governance analyst", "operations analyst",
    "management analyst", "program analyst", "it specialist", "contract specialist",
    "loan specialist", "administrative analyst"
]

SECONDARY_ROLES = [
    "underwriting", "loan operations", "financial services", "healthcare it",
    "it support", "customer success", "implementation specialist",
    "technical account", "administrative assistant"
]

# Location preferences (higher score = better fit)
LOCATION_SCORES = {
    "remote": 15, "dallas": 15, "seattle": 10, "texas": 12,
    "anywhere": 10, "united states": 8
}

# Keywords that indicate good pay
PAY_INDICATORS = {
    r"\$\s*(\d+)[kK]\s*[-–]\s*\$?\s*(\d+)[kK]": lambda m: (int(m.group(1)) * 1000 + int(m.group(2)) * 1000) / 2,
    r"\$\s*(\d+)\s*[-–]\s*\$?\s*(\d+)\s*\/\s*(hr|hour|hr\.)": lambda m: (float(m.group(1)) + float(m.group(2))) / 2,
    r"\$\s*(\d+)\s*\/\s*(hr|hour|hr\.)": lambda m: float(m.group(1)),
    r"\$\s*(\d+)[kK]": lambda m: int(m.group(1)) * 1000 / 2080,  # Convert annual to hourly
}


@dataclass
class ScoredJob:
    title: str = ""
    company: str = ""
    location: str = ""
    pay_range: str = ""
    source: str = ""
    link: str = ""
    score: int = 0
    priority: str = ""
    resume_match: int = 0
    pay_score: int = 0
    location_score: int = 0
    barrier_score: int = 0
    growth_score: int = 0
    effort_score: int = 0
    found_date: str = ""
    status: str = "Interested"
    notes: str = ""

    def to_markdown_row(self) -> str:
        return (
            f"| {self.found_date} | {self.title} | {self.company} | {self.location} | "
            f"{self.pay_range} | {self.source} | {self.link[:60] if self.link else ''} | "
            f"{self.score} | {self.priority} | {self.status} | Apply now | | {self.notes} |"
        )


def score_job(job_title: str, snippet: str = "", location: str = "", pay_text: str = "") -> ScoredJob:
    """Score a job opportunity from 0-100 based on title match, pay, location, and fit."""
    result = ScoredJob(title=job_title, location=location, pay_range=pay_text)
    title_lower = job_title.lower()

    # 1. Resume match (30 points)
    for role in PRIMARY_ROLES:
        if role in title_lower:
            result.resume_match = 30
            break
    if result.resume_match == 0:
        for role in SECONDARY_ROLES:
            if role in title_lower:
                result.resume_match = 20
                break
    if result.resume_match == 0:
        # Partial match - check individual words
        match_words = ["analyst", "coordinator", "specialist", "manager"]
        for word in match_words:
            if word in title_lower:
                result.resume_match = 15
                break
        if result.resume_match == 0 and snippet:
            # Check snippet for role mentions
            for role in PRIMARY_ROLES:
                if role in snippet.lower():
                    result.resume_match = 10
                    break

    # 2. Pay (20 points) - extracted from snippet or pay_text
    extracted_rate = _extract_hourly_rate(pay_text or snippet)
    if extracted_rate:
        if extracted_rate >= 40:
            result.pay_score = 20
        elif extracted_rate >= 35:
            result.pay_score = 18
        elif extracted_rate >= 30:
            result.pay_score = 15
        elif extracted_rate >= 25:
            result.pay_score = 10
        else:
            result.pay_score = 5
        result.pay_range = f"${extracted_rate}/hr" if extracted_rate < 1000 else f"${extracted_rate/1000:.0f}K/yr"
    else:
        result.pay_score = 8  # Unknown pay, moderate score

    # 3. Remote/Dallas fit (15 points)
    loc_lower = location.lower()
    for loc_name, score in LOCATION_SCORES.items():
        if loc_name in loc_lower:
            result.location_score = score
            break
    if result.location_score == 0:
        result.location_score = 5  # Unknown location, neutral

    # 4. Low barrier to entry (15 points) - based on snippet
    if snippet:
        snippet_lower = snippet.lower()
        if "entry level" in snippet_lower or "entry-level" in snippet_lower:
            result.barrier_score = 15
        elif "bachelor" in snippet_lower and ("1 year" not in snippet_lower and "2 year" not in snippet_lower):
            result.barrier_score = 15
        elif "bachelor" in snippet_lower and "2 year" in snippet_lower:
            result.barrier_score = 12
        elif "bachelor" in snippet_lower and "3 year" in snippet_lower:
            result.barrier_score = 8
        elif "bachelor" in snippet_lower and "5 year" in snippet_lower:
            result.barrier_score = 5
        elif "no experience" in snippet_lower or "training provided" in snippet_lower:
            result.barrier_score = 15
        else:
            result.barrier_score = 8  # Unknown, moderate
    else:
        result.barrier_score = 8

    # 5. Career growth (10 points)
    if snippet:
        growth_keywords = ["growth", "promotion", "advancement", "career path", "development program",
                          "training program", "mentorship", "leadership", "tuition", "certification"]
        for kw in growth_keywords:
            if kw in snippet.lower():
                result.growth_score = min(result.growth_score + 3, 10)
    if result.growth_score == 0:
        result.growth_score = 5  # Unknown, moderate

    # 6. Application effort (10 points)
    if snippet:
        easy_indicators = ["easy apply", "quick apply", "one-click", "linkedin easy apply", "simplified"]
        for ind in easy_indicators:
            if ind in snippet.lower():
                result.effort_score = 10
                break
        if result.effort_score == 0:
            hard_indicators = ["cover letter", "writing sample", "portfolio", "case study", "presentation",
                              "video interview", "assessment test", "multiple rounds"]
            for ind in hard_indicators:
                if ind in snippet.lower():
                    result.effort_score = 3
                    break
        if result.effort_score == 0:
            result.effort_score = 7  # Standard application
    else:
        result.effort_score = 7

    # Calculate total and priority
    result.score = (
        result.resume_match + result.pay_score + result.location_score +
        result.barrier_score + result.growth_score + result.effort_score
    )

    if result.score >= 85:
        result.priority = "P1 - Apply Now"
    elif result.score >= 70:
        result.priority = "P2 - Apply Today"
    elif result.score >= 55:
        result.priority = "P3 - Review This Week"
    else:
        result.priority = "Ignore"

    result.found_date = date.today().isoformat()
    return result


def _extract_hourly_rate(text: str) -> float | None:
    """Extract hourly pay rate from job description text."""
    if not text:
        return None
    for pattern, converter in PAY_INDICATORS.items():
        match = re.search(pattern, text)
        if match:
            try:
                return converter(match)
            except (ValueError, IndexError):
                pass
    return None


def search_gmail_for_jobs(config: AppConfig, max_results: int = 20) -> list[ScoredJob]:
    """Search Gmail for job alert emails and score the opportunities."""
    client = GmailReadOnlyClient.from_config(config)
    if not client:
        return []

    scored_jobs = []

    # Search for job-related emails from various sources
    search_queries = [
        "job alert business analyst OR data analyst OR project coordinator",
        "USAJobs OR usajobs application status",
        "new job posting analyst OR coordinator OR specialist",
        "job match OR job recommendation OR we found jobs",
        "hiring business analyst OR data analyst",
    ]

    seen_titles = set()

    for query in search_queries:
        try:
            emails = client.search(query, max_results=5)
        except Exception:
            continue

        for email in emails:
            subject = email.subject
            snippet = email.snippet

            # Extract job title from subject
            job_title = _extract_job_title(subject, snippet)
            if not job_title or job_title in seen_titles:
                continue
            seen_titles.add(job_title)

            # Extract location from subject/snippet
            location = _extract_location(subject + " " + snippet)

            # Score the job
            scored = score_job(job_title, snippet, location)
            scored.source = f"Gmail ({email.sender})"
            scored.company = _extract_company(subject, snippet)

            if scored.score >= 55:  # Only track P3 or better
                scored_jobs.append(scored)

    # Sort by score descending
    scored_jobs.sort(key=lambda j: j.score, reverse=True)
    return scored_jobs


def _extract_job_title(subject: str, snippet: str) -> str:
    """Extract job title from email subject or snippet."""
    # Common patterns in job alert emails
    patterns = [
        r'"([^"]+)"',  # Quoted text
        r'[:\-]\s*([A-Z][A-Za-z\s]+(?:Analyst|Coordinator|Specialist|Manager|Consultant|Engineer|Administrator|Officer|Director))',
        r'Job Title:\s*([A-Za-z\s]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, subject + " " + snippet)
        if match:
            title = match.group(1).strip()
            if len(title) > 5 and len(title) < 80:
                return title

    # Fallback: use the email subject directly
    if len(subject) < 80:
        return subject.strip()
    return subject[:80].strip()


def _extract_location(text: str) -> str:
    """Extract location from job posting text."""
    locations = []
    loc_options = ["Remote", "Dallas, TX", "Seattle, WA", "Washington, DC", "Austin, TX",
                  "Houston, TX", "San Antonio, TX", "Fort Worth, TX", "Plano, TX",
                  "Bellevue, WA", "Tacoma, WA", "Redmond, WA"]
    for loc in loc_options:
        if loc.lower() in text.lower():
            locations.append(loc)
    return ", ".join(locations) if locations else ""


def _extract_company(subject: str, snippet: str) -> str:
    """Extract company name from email content."""
    patterns = [
        r'at ([A-Z][A-Za-z\s&]+?)(?:\s*[-–]\s*|\s*in\s+|\s*\(|\s*$)',
        r'Company:\s*([A-Za-z\s&]+)',
        r'([A-Z][a-z]+(?: [A-Z][a-z]+){0,3})\s+is hiring',
    ]
    for pattern in patterns:
        match = re.search(pattern, subject + " " + snippet)
        if match:
            company = match.group(1).strip()
            if len(company) > 2 and company.lower() not in ("remote", "the", "this"):
                return company
    return ""


def format_jobs_for_briefing(jobs: list[ScoredJob], max_show: int = 5) -> str:
    """Format scored jobs for the daily briefing."""
    if not jobs:
        return "No new job opportunities found today."

    p1_jobs = [j for j in jobs if j.priority.startswith("P1")]
    p2_jobs = [j for j in jobs if j.priority.startswith("P2")]

    lines = []
    if p1_jobs:
        lines.append(f"**P1 - Apply Now ({len(p1_jobs)}):**")
        for j in p1_jobs[:3]:
            pay_str = f" ({j.pay_range})" if j.pay_range else ""
            loc_str = f" - {j.location}" if j.location else ""
            lines.append(f"- {j.title} at {j.company}{loc_str}{pay_str} [Score: {j.score}]")

    if p2_jobs:
        lines.append(f"\n**P2 - Apply Today ({len(p2_jobs)}):**")
        for j in p2_jobs[:3]:
            if len(lines) >= max_show + 2:
                break
            pay_str = f" ({j.pay_range})" if j.pay_range else ""
            loc_str = f" - {j.location}" if j.location else ""
            lines.append(f"- {j.title} at {j.company}{loc_str}{pay_str} [Score: {j.score}]")

    remaining = len(p1_jobs) + len(p2_jobs) - len(p1_jobs[:3]) - len(p2_jobs[:3])
    if remaining > 0:
        lines.append(f"\nPlus {remaining} more opportunities. Full list in [[Job-Applications-Tracker]].")

    return "\n".join(lines)


def write_jobs_to_tracker(jobs: list[ScoredJob], vault_path: Path) -> str:
    """Write scored jobs to the Obsidian job tracker."""
    tracker_path = vault_path / "05-Career" / "Job-Applications-Tracker.md"

    if not tracker_path.exists():
        return "Job tracker file not found."

    # Read existing content
    content = tracker_path.read_text(encoding="utf-8")

    # Add new jobs before the status options section
    new_rows = []
    for job in jobs[:10]:  # Max 10 new jobs per run
        if job.score >= 55:
            new_rows.append(job.to_markdown_row())

    if new_rows:
        # Insert after the header table row
        insert_marker = "| # | Date | Job Title | Company | Location | Remote | Pay | Source | Link | Score | Priority | Status | Next Action | Deadline | Notes |"
        insert_pos = content.find(insert_marker)
        if insert_pos >= 0:
            next_line = content.find("\n", insert_pos) + 1
            # Skip the separator line
            next_line = content.find("\n", next_line) + 1
            content = content[:next_line] + "\n".join(new_rows) + "\n" + content[next_line:]
            tracker_path.write_text(content, encoding="utf-8")
            return f"Added {len(new_rows)} jobs to tracker."
        else:
            # Append to end
            with open(tracker_path, "a", encoding="utf-8") as f:
                f.write("\n".join(new_rows) + "\n")
            return f"Appended {len(new_rows)} jobs to tracker."

    return "No new jobs to add."


# ---------------------------------------------------------------------------
# TODO: USAJobs API Integration
# ---------------------------------------------------------------------------
# When a USAJobs API key is obtained (free at https://developer.usajobs.gov/):
# 1. Set USAJOBS_API_KEY in system env vars
# 2. Uncomment the function below
# 3. Add "usajobs" to the search_gmail_for_jobs function

# def search_usajobs(config: AppConfig, keywords: list[str], location: str = "") -> list[ScoredJob]:
#     """Search USAJobs API for matching positions."""
#     api_key = os.getenv("USAJOBS_API_KEY", "")
#     if not api_key:
#         return []
#     import requests
#     scored = []
#     for keyword in keywords[:5]:
#         try:
#             r = requests.get(
#                 "https://data.usajobs.gov/api/search",
#                 params={"Keyword": keyword, "ResultsPerPage": 10},
#                 headers={
#                     "Host": "data.usajobs.gov",
#                     "User-Agent": "TitusBanksJarvisOS/1.0",
#                     "Authorization-Key": api_key,
#                 },
#                 timeout=15,
#             )
#             if r.status_code == 200:
#                 data = r.json()
#                 for item in data.get("SearchResult", {}).get("SearchResultItems", []):
#                     match = item.get("MatchedObjectDescriptor", {})
#                     title = match.get("PositionTitle", "")
#                     snippet = " ".join(match.get("UserArea", {}).get("Details", {}).get("MajorDuties", []))
#                     location = match.get("PositionLocationDisplay", "")
#                     pay = match.get("PositionRemuneration", [{}])[0].get("MinimumRange", "")
#                     scored.append(score_job(title, snippet, location, str(pay)))
#         except Exception:
#             continue
#     return scored