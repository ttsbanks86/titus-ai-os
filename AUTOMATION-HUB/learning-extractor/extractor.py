#!/usr/bin/env python3
"""AI Learning Extractor for Titus AI OS.

Turns a URL, text snippet, or local text file into a practical learning report.
This intentionally avoids secrets and heavyweight dependencies so it can be
called safely from desktop, Telegram, or WhatsApp agent workflows.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import os
import re
import sys
import textwrap
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip = 0
        self.parts: list[str] = []
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[no-untyped-def]
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip += 1
        elif tag == "title":
            self._in_title = True
        elif tag in {"p", "div", "section", "article", "li", "h1", "h2", "h3", "br"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"} and self._skip:
            self._skip -= 1
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        cleaned = re.sub(r"\s+", " ", data).strip()
        if not cleaned:
            return
        if self._in_title:
            self.title += cleaned + " "
        self.parts.append(cleaned + " ")

    def text(self) -> str:
        raw = html.unescape("".join(self.parts))
        lines = [re.sub(r"\s+", " ", line).strip() for line in raw.splitlines()]
        lines = [line for line in lines if line]
        return "\n".join(lines)


def fetch_url(url: str, timeout: int = 25) -> tuple[str, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 Titus-AI-OS-LearningExtractor/1.0",
            "Accept": "text/html,text/plain,application/xhtml+xml",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get("content-type", "")
            body = response.read(1_500_000)
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not fetch URL: {exc}") from exc

    encoding_match = re.search(r"charset=([^;]+)", content_type, re.I)
    encoding = encoding_match.group(1) if encoding_match else "utf-8"
    decoded = body.decode(encoding, errors="replace")
    if "html" in content_type.lower() or "<html" in decoded[:500].lower():
        parser = _TextExtractor()
        parser.feed(decoded)
        title = parser.title.strip() or url
        return title, parser.text()
    return url, decoded


def read_file(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}:
        return (
            path.name,
            "[IMAGE INPUT]\n"
            "This file is an image/screenshot. OCR is not enabled in the lightweight extractor. "
            "Use the assistant's vision tool, paste visible text, or install an approved local OCR tool later.",
        )
    if suffix == ".pdf":
        return (
            path.name,
            "[PDF INPUT]\n"
            "PDF parsing is intentionally not enabled in this lightweight extractor. "
            "Use existing PDF tools or paste extracted text, then rerun the extractor.",
        )
    return path.name, path.read_text(encoding="utf-8", errors="replace")


def normalize_text(text: str, limit: int = 50_000) -> str:
    text = html.unescape(text)
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text[:limit]


def sentences(text: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return []
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", cleaned)
    return [p.strip() for p in parts if 40 <= len(p.strip()) <= 280]


def score_sentence(sentence: str) -> int:
    keywords = {
        "learn": 4,
        "lesson": 4,
        "workflow": 5,
        "system": 4,
        "prompt": 5,
        "skill": 5,
        "agent": 5,
        "automation": 5,
        "extract": 4,
        "summar": 4,
        "recommend": 4,
        "implement": 5,
        "improve": 3,
        "process": 3,
        "template": 4,
        "course": 3,
        "training": 3,
    }
    lower = sentence.lower()
    return sum(weight for word, weight in keywords.items() if word in lower) + min(len(sentence) // 80, 3)


def top_items(items: Iterable[str], count: int = 6) -> list[str]:
    unique: list[str] = []
    seen: set[str] = set()
    for item in sorted(items, key=score_sentence, reverse=True):
        key = re.sub(r"\W+", "", item.lower())[:120]
        if key and key not in seen:
            unique.append(item)
            seen.add(key)
        if len(unique) >= count:
            break
    return unique


def infer_patterns(text: str) -> list[str]:
    lower = text.lower()
    patterns: list[str] = []
    if any(word in lower for word in ["course", "training", "lesson", "module"]):
        patterns.append("Course-to-workflow extraction: turn learning material into repeatable operating procedures.")
    if any(word in lower for word in ["prompt", "claude", "chatgpt", "ai"]):
        patterns.append("Prompt distillation: capture effective prompts as reusable templates.")
    if any(word in lower for word in ["url", "website", "article", "documentation"]):
        patterns.append("URL intake: summarize public web pages and convert them into action steps.")
    if any(word in lower for word in ["screenshot", "image", "reel", "video"]):
        patterns.append("Media intake: use screenshots or transcripts as learning sources when direct text is blocked.")
    if not patterns:
        patterns.append("Learning intake: extract lessons, apply them to Titus AI OS, and create next actions.")
    return patterns


def make_report(source_label: str, source_type: str, text: str) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    text = normalize_text(text)
    ranked = top_items(sentences(text), 7)
    if not ranked:
        ranked = ["No substantial text was available. Add a transcript, screenshot text, or accessible URL and rerun the extractor."]

    patterns = infer_patterns(text)
    source_safe = source_label.replace("\n", " ").strip()

    prompt_template = textwrap.dedent(
        """
        Extract the core lessons from this source, then convert them into:
        1. practical actions for Titus AI OS,
        2. reusable prompt patterns,
        3. possible OpenCode skills or bot commands,
        4. next actions with priority.
        Keep the output direct, practical, and implementation-ready.
        """
    ).strip()

    lines: list[str] = []
    lines.append(f"# AI Learning Extractor Report")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append(f"Source type: {source_type}")
    lines.append(f"Source: {source_safe}")
    lines.append("")
    lines.append("## Core lessons")
    for idx, item in enumerate(ranked, 1):
        lines.append(f"{idx}. {item}")
    lines.append("")
    lines.append("## Practical application for Titus AI OS")
    lines.append("1. Treat every useful course, Reel, article, screenshot, or PDF as reusable system knowledge, not one-time content.")
    lines.append("2. Convert learning into workflows, skills, memory notes, and bot commands that can be reused from desktop, Telegram, or WhatsApp.")
    lines.append("3. Keep human approval gates for sending messages, purchases, account access, and external posting.")
    lines.append("")
    lines.append("## Reusable prompt/workflow patterns")
    for idx, item in enumerate(patterns, 1):
        lines.append(f"{idx}. {item}")
    lines.append("")
    lines.append("## Reusable prompt")
    lines.append("```text")
    lines.append(prompt_template)
    lines.append("```")
    lines.append("")
    lines.append("## Skill candidates")
    lines.append("- learning-extractor: intake URLs, text, files, screenshots, and transcripts, then generate implementation-ready summaries.")
    lines.append("- prompt-pattern-library: save strong prompts discovered from courses and creators.")
    lines.append("- weekly-ai-upskill-loop: review saved sources weekly and convert the best ideas into tasks.")
    lines.append("")
    lines.append("## Bot command suggestions")
    lines.append("- `/learn-source <url>`: fetch a URL and create a learning report.")
    lines.append("- `/learn-text <text>`: summarize pasted text into lessons and system actions.")
    lines.append("- `/learn-file <path>`: process a local text file; screenshots need assistant vision or local OCR.")
    lines.append("- `Learn this: <url or text>`: natural language fallback for WhatsApp/Telegram.")
    lines.append("")
    lines.append("## Next actions")
    lines.append("1. Review this report and mark any skill candidates worth building.")
    lines.append("2. Save strong prompt patterns into the AI Knowledge OS vault or a dedicated prompt library.")
    lines.append("3. If the source is a video/Reel, capture screenshots or transcript snippets and rerun with `--text`.")
    lines.append("4. If a command should be permanent, add it to the bot instruction card and Project Radar.")
    lines.append("")
    lines.append("## Extracted source preview")
    preview = text[:2500] if text else "No text extracted."
    lines.append("```text")
    lines.append(preview)
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def default_output_path(source_label: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", source_label.lower()).strip("-")[:48] or "learning-source"
    return OUTPUT_DIR / f"{stamp}-{slug}.md"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a Titus AI OS learning extraction report.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Public URL to fetch and summarize")
    group.add_argument("--text", help="Plain text to summarize")
    group.add_argument("--file", help="Local file path to process")
    parser.add_argument("--out", help="Output Markdown path")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        if args.url:
            label, content = fetch_url(args.url)
            source_type = "url"
            source_label = args.url if label == args.url else f"{label} ({args.url})"
        elif args.text:
            content = args.text
            source_type = "text"
            source_label = "pasted text"
        else:
            path = Path(args.file).expanduser().resolve()
            if not path.exists():
                raise FileNotFoundError(str(path))
            label, content = read_file(path)
            source_type = "file"
            source_label = str(path)

        report = make_report(source_label, source_type, content)
        out_path = Path(args.out).expanduser().resolve() if args.out else default_output_path(source_label)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(str(out_path))
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI should report cleanly
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
