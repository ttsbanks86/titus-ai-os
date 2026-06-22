# Quizzes & Books Project

**Date:** June 3, 2026
**Status:** Active
**Purpose:** System for accessing borrowed books, extracting text via Internet Archive BookReader, answering reading quizzes, and organizing all quiz/book materials by course.

---

## 1. Overview

This project manages the workflow for masters-level reading quizzes across multiple courses and books. When a quiz is assigned, the book is borrowed from Internet Archive (free, 14-day lending), text is extracted via the BookReader's OCR text layer, and answers are looked up directly with page references.

### Core Workflow

```
Quiz assigned → Identify book → Borrow from Internet Archive →
Navigate BookReader pages → Extract OCR text layer →
Search for answer passages → Compile answers with page references →
Save to QUIZZES/ folder
```

---

## 2. Tools & Access

| Resource | Details |
|----------|---------|
| **Internet Archive** | Free account, 14-day lending, auto-renew with continued use |
| **IA Account** | User: Titus Banks, Username: `titus_banks`, Email: `devinechronicles7@gmail.com` |
| **BookReader URL** | `https://archive.org/details/{identifier}/page/{N}/mode/2up` |
| **OCR Extraction** | JS: `document.querySelectorAll('.BRtextLayer span')` → concatenate text |
| **Page Navigation** | Keyboard ArrowRight/ArrowLeft (2-up book spreads) |
| **Search** | `window.br.search('query')` via browser console |

### Limitations
- Direct text file download (`_djvu.txt`, `_hocr_searchtext.txt.gz`) blocked by CDL — even with active borrow session
- OCR quality varies — some pages clean, some garbled
- Search function partially functional; page-by-page reading more reliable

---

## 3. Completed Quizzes

| # | Book | Course | Date | File |
|---|------|--------|------|------|
| 1 | Rethinking the Church (James Emery White) | TBD | Jun 3, 2026 | `QUIZZES/QUIZ-ONE.md` |

---

## 4. Book Access History

| Book | Identifier | Pages | Borrowed | Status |
|------|-----------|-------|----------|--------|
| Rethinking the Church: A Challenge to Creative Redesign in an Age of Transition | `rethinkingchurch0000whit_u9u0` | ~198 (99 leaves) | Jun 3, 2026 | Active (auto-renew) |

---

## 5. Future Workflow

For each new reading assignment:

1. **Identify the book** — title, author, edition
2. **Check Internet Archive** — search by title/author; borrow if available
3. **Access BookReader** — navigate to `page/{N}/mode/2up`
4. **Extract text** — evaluate JS to grab `.BRtextLayer span` content
5. **Find answers** — search for key terms, read surrounding context
6. **Compile** — question → correct answer → page reference → direct quote
7. **Save** — add to `QUIZZES/` folder as `QUIZ-{N}.md`
8. **Update this page** — add to Completed Quizzes table

### If IA Does Not Have the Book
- Check Perlego subscription (available for $12-18/mo if needed)
- Check Google Books preview
- Check if Kindle version supports text export (DRM may block)

---

## 6. Related Projects

- **Education Progress** (PROJECT-RADAR.md) — Masters in Divinity + Cybersecurity
- **Book / Writing Project** (BOOK-PROJECT.md) — Original book ideas and writing

---

## Next Actions

- [ ] Identify which course Quiz One belongs to and update table
- [ ] Confirm next reading assignment/book
- [ ] Build a quick-extract bookmarklet or script for IA BookReader text capture
