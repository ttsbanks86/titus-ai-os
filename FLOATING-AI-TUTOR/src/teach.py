#!/usr/bin/env python3
"""Teach Mode — structured lessons, quizzes, and progress tracking."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

DATA_DIR = Path.home() / ".floating-ai-tutor"
LESSONS_DIR = DATA_DIR / "lessons"
PROGRESS_FILE = DATA_DIR / "learning_progress.json"

TOPIC_TEMPLATES = {
    "python": {
        "title": "Python Programming",
        "steps": [
            "Variables and data types",
            "Control flow (if/else, loops)",
            "Functions and scope",
            "Lists, dictionaries, and collections",
            "File handling",
            "Error handling",
            "Classes and objects",
            "Modules and packages",
        ],
    },
    "excel": {
        "title": "Microsoft Excel",
        "steps": [
            "Cells, rows, columns, and ranges",
            "Basic formulas (SUM, AVERAGE, COUNT)",
            "Cell references (relative vs absolute)",
            "Conditional formatting",
            "Charts and graphs",
            "Pivot tables",
            "VLOOKUP and XLOOKUP",
            "Data validation and protection",
        ],
    },
    "powerbi": {
        "title": "Power BI",
        "steps": [
            "Connecting to data sources",
            "Data transformation with Power Query",
            "Building visualizations",
            "DAX basics",
            "Filters and slicers",
            "Dashboards vs reports",
            "Publishing and sharing",
            "Row-level security",
        ],
    },
    "cybersecurity": {
        "title": "Cybersecurity Fundamentals",
        "steps": [
            "Security principles (CIA triad)",
            "Common threats and attack vectors",
            "Network security basics",
            "Authentication and access control",
            "Encryption fundamentals",
            "Security policies and compliance",
            "Incident response",
            "Security tools and monitoring",
        ],
    },
    "networking": {
        "title": "Computer Networking",
        "steps": [
            "OSI model and TCP/IP",
            "IP addressing and subnetting",
            "Routing and switching",
            "DNS and DHCP",
            "Firewalls and NAT",
            "VPNs and remote access",
            "Network troubleshooting",
            "Wireless networking",
        ],
    },
    "sql": {
        "title": "SQL and Databases",
        "steps": [
            "SELECT and basic queries",
            "WHERE and filtering",
            "JOINs (INNER, LEFT, RIGHT)",
            "GROUP BY and aggregation",
            "Subqueries",
            "INSERT, UPDATE, DELETE",
            "Indexes and performance",
            "Database design basics",
        ],
    },
}


def detect_topic(text: str) -> str:
    """Detect the likely topic from captured screen content."""
    text_lower = text.lower()
    scores = {}
    for topic, template in TOPIC_TEMPLATES.items():
        score = 0
        keywords = template["title"].lower().split()
        for kw in keywords:
            if kw in text_lower:
                score += 1
        for step in template["steps"]:
            for word in step.lower().split():
                if len(word) > 3 and word in text_lower:
                    score += 0.5
        scores[topic] = score

    best = max(scores, key=scores.get)
    if scores[best] > 0:
        return best
    return "general"


def create_lesson_plan(topic: str, level: str = "beginner") -> dict:
    """Create a structured lesson plan for a topic."""
    template = TOPIC_TEMPLATES.get(topic)
    if not template:
        template = {
            "title": topic.title(),
            "steps": [
                f"Introduction to {topic}",
                f"Core concepts of {topic}",
                f"Practical applications of {topic}",
                f"Advanced topics in {topic}",
                f"Review and practice",
            ],
        }

    plan = {
        "topic": topic,
        "title": template["title"],
        "level": level,
        "created_at": datetime.now().isoformat(),
        "steps": [],
    }

    for i, step_title in enumerate(template["steps"]):
        plan["steps"].append({
            "number": i + 1,
            "title": step_title,
            "status": "pending",
            "notes": "",
            "quiz_score": None,
        })

    return plan


def generate_quiz(topic: str, step_title: str, content: str = "") -> list[dict]:
    """Generate a simple quiz for a lesson step."""
    quizzes = {
        "python": {
            "Variables and data types": [
                {"q": "What type is the value 42?", "a": "int (integer)", "choices": ["int", "float", "str", "bool"]},
                {"q": "How do you create a variable in Python?", "a": "x = value", "choices": ["var x = value", "x = value", "let x = value", "x := value"]},
                {"q": "What does type('hello') return?", "a": "str", "choices": ["str", "string", "text", "char"]},
            ],
            "Control flow (if/else, loops)": [
                {"q": "What keyword starts a conditional block?", "a": "if", "choices": ["if", "when", "check", "case"]},
                {"q": "How do you loop 5 times in Python?", "a": "for i in range(5)", "choices": ["for i=0;i<5;i++", "for i in range(5)", "loop 5 times", "repeat 5"]},
                {"q": "What does 'else' do in an if statement?", "a": "Runs when the condition is False", "choices": ["Runs when True", "Runs when False", "Always runs", "Never runs"]},
            ],
        },
    }

    topic_quizzes = quizzes.get(topic, {})
    step_quiz = topic_quizzes.get(step_title, [
        {"q": f"What is the main purpose of {step_title}?", "a": "To understand and apply the concept", "choices": ["Memorization", "Understanding and application", "Speed", "None of the above"]},
        {"q": f"Which best describes {step_title}?", "a": "A fundamental building block", "choices": ["A fundamental building block", "An advanced technique", "A debugging tool", "A design pattern"]},
        {"q": f"When should you use {step_title}?", "a": "When working with related data or logic", "choices": ["Always", "Never", "When working with related data or logic", "Only in production"]},
    ])

    return step_quiz


def load_progress() -> dict:
    """Load learning progress from disk."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LESSONS_DIR.mkdir(parents=True, exist_ok=True)
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"topics": {}, "current_lesson": None}


def save_progress(progress: dict):
    """Save learning progress to disk."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding="utf-8")


def save_lesson(lesson: dict):
    """Save a lesson plan to disk."""
    LESSONS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{lesson['topic']}_{lesson['created_at'][:10]}.json"
    path = LESSONS_DIR / filename
    path.write_text(json.dumps(lesson, indent=2, ensure_ascii=False), encoding="utf-8")


def get_saved_lessons() -> list[dict]:
    """List all saved lessons."""
    LESSONS_DIR.mkdir(parents=True, exist_ok=True)
    lessons = []
    for file in sorted(LESSONS_DIR.glob("*.json"), reverse=True):
        try:
            lessons.append(json.loads(file.read_text(encoding="utf-8")))
        except Exception:
            pass
    return lessons


def get_lesson_summary(lesson: dict) -> str:
    """Get a readable summary of a lesson."""
    completed = sum(1 for s in lesson["steps"] if s["status"] == "completed")
    total = len(lesson["steps"])
    return (
        f"📚 {lesson['title']} ({lesson['level']})\n"
        f"Progress: {completed}/{total} steps completed\n"
        f"Created: {lesson['created_at'][:10]}"
    )
