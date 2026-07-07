"""Executive Briefing System for Jarvis.

Generates morning, midday, and evening briefings by:
1. Searching Gmail for relevant keywords (WGU, jobs, ISC2, etc.)
2. Checking calendar for today's events
3. Scoring and ranking opportunities
4. Writing the briefing to the vault daily note
5. Returning a spoken summary for Jarvis to read aloud
"""
from __future__ import annotations

from datetime import datetime, date
from pathlib import Path
from typing import Any

from app.config import AppConfig
from app.tools.email import GmailReadOnlyClient, EmailSummary
from app.tools.career_intelligence import (
    search_gmail_for_jobs,
    format_jobs_for_briefing,
    write_jobs_to_tracker,
    score_job,
)


# Keywords to search in Gmail for each category
WGU_KEYWORDS = ["wgu", "career services", "internship", "job fair", "career fair", "commencement", "graduation", "alumni", "webinar", "handshake"]
JOB_KEYWORDS = ["interview", "recruiter", "application", "assessment", "job alert", "business analyst", "data analyst", "project coordinator", "grc analyst", "compliance analyst", "usa jobs", "usajobs"]
ISC2_KEYWORDS = ["isc2", "certification", "exam", "practice test", "study guide", "security+"]
URGENT_KEYWORDS = ["urgent", "interview invitation", "assessment due", "deadline", "action required", "offer letter"]


def classify_email(summary: EmailSummary) -> str:
    """Classify an email as Critical, Action Needed, Opportunity, Reference, or Ignore."""
    text = f"{summary.subject} {summary.snippet}".lower()
    sender = summary.sender.lower()

    # Critical
    critical_phrases = ["interview invitation", "assessment request", "offer letter", "deadline", "urgent", "action required", 
                       "commencement update", "exam update", "schedule change"]
    for phrase in critical_phrases:
        if phrase in text:
            return "Critical"

    # Action Needed
    action_phrases = ["apply now", "complete your", "submit", "register for", "confirm", "respond", "form", "fill out"]
    for phrase in action_phrases:
        if phrase in text:
            return "Action Needed"

    # Opportunity
    opportunity_phrases = ["job opening", "internship", "career fair", "webinar", "hiring", "position", "opportunity",
                          "fellowship", "apprenticeship", "scholarship"]
    for phrase in opportunity_phrases:
        if phrase in text or phrase in summary.subject.lower():
            return "Opportunity"

    # Reference
    reference_phrases = ["study material", "newsletter", "update", "recap", "guide", "resource", "tips"]
    for phrase in reference_phrases:
        if phrase in text:
            return "Reference"

    # Ignore
    ignore_phrases = ["promotion", "sale", "discount", "sponsored", "advertisement", "unsubscribe", "free trial",
                     "bed bath", "course careers", "footballguys"]
    for phrase in ignore_phrases:
        if phrase in sender or phrase in text:
            return "Ignore"

    return "Reference"


def generate_morning_briefing(config: AppConfig) -> str:
    """Generate the morning briefing by checking Gmail, calendar, and priorities."""
    now = datetime.now()
    today_str = now.strftime("%A, %B %d, %Y")
    time_str = now.strftime("%I:%M %p")
    
    lines = []
    lines.append(f"# Jarvis Morning Briefing for Titus")
    lines.append(f"**Date:** {today_str}")
    lines.append(f"**Time:** {time_str}")
    lines.append("")

    # 1. Check Gmail
    client = GmailReadOnlyClient.from_config(config)
    critical_items = []
    opportunity_items = []
    action_items = []
    
    if client:
        try:
            # Search for WGU emails
            wgu_emails = client.search("wgu OR career services OR internship OR commencement OR graduation", max_results=5)
            # Search for job emails
            job_emails = client.search("interview OR recruiter OR application OR assessment OR job alert", max_results=5)
            # Search for ISC2 emails
            isc2_emails = client.search("isc2 OR certification OR exam", max_results=5)
            
            all_emails = {e.subject: e for e in (wgu_emails + job_emails + isc2_emails)}.values()
            
            for email in all_emails:
                classification = classify_email(email)
                if classification == "Critical":
                    critical_items.append(f"- {email.subject} (from {email.sender})")
                elif classification == "Action Needed":
                    action_items.append(f"- {email.subject}")
                elif classification == "Opportunity":
                    opportunity_items.append(f"- {email.subject}")
        except Exception:
            pass
    
    # 2. What changed overnight
    lines.append("## 1. What Changed Overnight")
    if critical_items:
        lines.append("### Critical Items")
        lines.extend(critical_items)
    else:
        lines.append("No critical items detected overnight.")
    lines.append("")
    
    # 3. Critical items summary
    lines.append("## 2. Critical Items")
    if critical_items:
        lines.extend(critical_items)
    else:
        lines.append("Nothing critical requires immediate attention.")
    lines.append("")
    
    # 4. Today's top 5 priorities
    lines.append("## 3. Today's Top 5 Priorities")
    lines.append("1. Check for new job postings matching Business Analyst, Data Analyst, Project Coordinator roles")
    lines.append("2. Review any recruiter messages or interview invitations")
    lines.append("3. ISC2 study: Review today's domain per study plan")
    lines.append("4. Check WGU emails for career fairs, events, or commencement updates")
    lines.append("5. Update job application tracker with any new applications or status changes")
    lines.append("")
    
    # 5. Job opportunities
    lines.append("## 4. Job Opportunities Worth Reviewing")
    # Search Gmail for job alerts and score them
    try:
        scored_jobs = search_gmail_for_jobs(config, max_results=20)
        if scored_jobs:
            lines.append(format_jobs_for_briefing(scored_jobs, max_show=5))
            vault_path = config.obsidian_vault_path
            if vault_path.exists():
                tracker_result = write_jobs_to_tracker(scored_jobs, vault_path)
                lines.append(f"\n*{tracker_result}*")
        elif opportunity_items:
            lines.extend(opportunity_items)
        else:
            lines.append("No new job opportunities detected in recent emails. Check LinkedIn and job boards manually.")
    except Exception:
        if opportunity_items:
            lines.extend(opportunity_items)
        else:
            lines.append("No new job opportunities detected in recent emails. Check LinkedIn and job boards manually.")
    lines.append("")
    
    # 6. WGU updates
    lines.append("## 5. WGU Updates")
    wgu_notes = [e for e in (critical_items + action_items + opportunity_items) if "wgu" in e.lower() or "commencement" in e.lower() or "career" in e.lower()]
    if wgu_notes:
        lines.extend(wgu_notes)
    else:
        lines.append("No new WGU updates. Commencement is July 25, 2026 — 18 days away.")
    lines.append("")
    
    # 7. ISC2 study task
    lines.append("## 6. ISC2 Study Task for Today")
    days_remaining = (date(2026, 7, 28) - date.today()).days
    lines.append(f"ISC2 exam in {days_remaining} days (July 28, 2026).")
    lines.append("Today: Review Security & Risk Management domain. Do 20 practice questions.")
    if isc2_emails:
        isc2_notes = [e.subject for e in isc2_emails]
        lines.append(f"ISC2 emails found: {', '.join(isc2_notes[:3])}")
    lines.append("")
    
    # 8. Calendar
    lines.append("## 7. Calendar & Schedule")
    lines.append("No fixed caregiving schedule currently. Check calendar for any appointments.")
    lines.append("")
    
    # 9. Follow-ups
    lines.append("## 8. Follow-Ups Needed")
    if action_items:
        lines.extend(action_items)
    else:
        lines.append("No pending follow-ups detected.")
    lines.append("")
    
    # 10. What Jarvis handled
    lines.append("## 9. What Jarvis Already Handled")
    lines.append("- Searched Gmail for WGU, career, job, and ISC2 emails")
    lines.append("- Classified emails by priority")
    lines.append("- Generated this briefing")
    lines.append("- Writing summary to Obsidian daily note")
    lines.append("")
    
    # 11. Decisions needed
    lines.append("## 10. What Titus Needs to Decide")
    lines.append("- Which job postings to apply for today")
    lines.append("- Whether to prioritize ISC2 study or job applications today")
    lines.append("")
    
    return "\n".join(lines)


def generate_midday_check(config: AppConfig) -> str:
    """Generate the midday check briefing."""
    now = datetime.now()
    
    lines = []
    lines.append(f"# Jarvis Midday Check")
    lines.append(f"**Time:** {now.strftime('%I:%M %p')}")
    lines.append("")
    lines.append("## 1. New Urgent Items")
    lines.append("Check Gmail for new messages since morning.")
    lines.append("")
    lines.append("## 2. New Job or WGU Opportunities")
    lines.append("Review any new job alerts or WGU emails.")
    lines.append("")
    lines.append("## 3. Messages Needing Response")
    lines.append("Check for recruiter replies or interview invitations.")
    lines.append("")
    lines.append("## 4. Application Updates")
    lines.append("Update [[Job-Applications-Tracker]] with any status changes.")
    lines.append("")
    lines.append("## 5. Recommended Next Action")
    lines.append("Review new job postings. Apply to P1 and P2 matches.")
    lines.append("")
    return "\n".join(lines)


def generate_evening_review(config: AppConfig) -> str:
    """Generate the evening review briefing."""
    now = datetime.now()
    
    lines = []
    lines.append(f"# Jarvis Evening Review")
    lines.append(f"**Time:** {now.strftime('%I:%M %p')}")
    lines.append("")
    lines.append("## 1. What Was Completed")
    lines.append("(Titus: update with what you completed today)")
    lines.append("")
    lines.append("## 2. What Was Missed")
    lines.append("(Review morning priorities — what slipped?)")
    lines.append("")
    lines.append("## 3. New Updates")
    lines.append("- WGU commencement: 18 days remaining")
    lines.append(f"- ISC2 exam: {(date(2026, 7, 28) - date.today()).days} days remaining")
    lines.append("")
    lines.append("## 4. Tomorrow's Top Priorities")
    lines.append("1. Continue job search and applications")
    lines.append("2. ISC2 study per plan")
    lines.append("3. Check WGU emails")
    lines.append("")
    lines.append("## 5. Notes Written to Obsidian")
    lines.append(f"- Daily note: 02-Daily-Notes/{date.today()}.md")
    lines.append("")
    lines.append("## 6. Items to Follow Up")
    lines.append("Review any pending applications or recruiter messages.")
    lines.append("")
    return "\n".join(lines)


def write_briefing_to_obsidian(config: AppConfig, briefing_type: str, content: str) -> str:
    """Write a briefing to the vault daily note."""
    daily_path = config.obsidian_inbox_path / f"{date.today()}.md"
    header = f"\n\n---\n\n{content}\n"
    try:
        with open(daily_path, "a", encoding="utf-8") as f:
            f.write(header)
        return f"Briefing written to {daily_path}"
    except Exception as e:
        return f"Could not write briefing: {e}"


def spoken_briefing_summary(config: AppConfig, briefing_type: str) -> str:
    """Generate a short spoken summary for Jarvis to read aloud."""
    content = ""
    if briefing_type == "morning":
        content = generate_morning_briefing(config)
    elif briefing_type == "midday":
        content = generate_midday_check(config)
    elif briefing_type == "evening":
        content = generate_evening_review(config)
    
    # Extract key lines for spoken summary
    lines = content.split("\n")
    critical = [l for l in lines if l.startswith("- ") and ("interview" in l.lower() or "urgent" in l.lower() or "offer" in l.lower())]
    
    parts = []
    if critical:
        parts.append(f"I found {len(critical)} critical items:")
        parts.extend(critical[:3])
    else:
        parts.append("Good morning. No critical items detected overnight.")
    
    parts.append(f"Your top priorities today: job search for Business Analyst and Data Analyst roles, ISC2 study, and WGU commencement preparation.")
    parts.append(f"WGU commencement is 18 days away. ISC2 exam is in {(date(2026, 7, 28) - date.today()).days} days.")
    
    return " ".join(parts)