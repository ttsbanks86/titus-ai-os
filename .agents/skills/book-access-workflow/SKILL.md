---
name: book-access-workflow
description: Use when Titus asks for help finding, opening, reading, verifying, or answering questions from a book across Kindle, Kindle for Web, Google Books, Everand/Scribd, Internet Archive/Open Library, WorldCat/libraries, publisher samples, Logos, or other legal platforms. Trigger keywords: find the book, read the book, Kindle, Everand, Internet Archive, Open Library, Google Books, book questions, chapter questions, answer these questions.
---

# Book Access Workflow

Use this skill whenever Titus asks for help with a book and wants the agent to find where it is available, open it, read accessible sections, or answer chapter questions.

## Core rule

Use only legal and authorized access paths. Do not recommend piracy, bypass DRM, scrape hidden paid content, handle passwords, submit MFA codes, purchase books, or change accounts without explicit approval. If a login, password, MFA, payment, or account-security prompt appears, stop and let Titus handle it.

## Titus preference

Titus does not want to re-explain the book access process each time. Remember this workflow and apply it proactively.

When answering book-study questions, use Titus's preferred format:

```text
## Chapter X

Question: ...
Answer: ...
C: optional comment if helpful
```

For multiple-choice questions, keep answers in the original order and include the option letter plus answer text when possible.

## Access search order

1. Confirm the exact title, author, edition, and ISBN/ASIN if available.
2. Check the user's existing authorized platforms first:
   - Kindle for Web: `https://read.amazon.com/kindle-library`
   - Kindle Windows app
   - Everand/Scribd
   - Google Books / Google Play Books
3. Check legal public/library options:
   - Internet Archive / Open Library
   - WorldCat / local libraries
   - publisher sample PDFs
   - Logos / Christianbook / other authorized retailers
4. If no full access is available, use previews, table of contents, public samples, and user-provided screenshots, clearly marking what is verified.

## Kindle workflow

Prefer **Kindle for Web** when the Windows Kindle app fails to sync.

Known successful path:

1. Open `https://read.amazon.com/kindle-library` in the browser.
2. Search the visible library text for the title.
3. Open the book tile.
4. Use the Kindle reader controls:
   - Kindle Library
   - Table of Contents
   - Search
   - Reader settings
   - Previous/Next page
5. Use Table of Contents to jump directly to the relevant chapter.
6. If accessible text only shows controls/page numbers, capture a screenshot of the visible page and use vision to read the page.

Important Kindle note: Kindle for Web may render the book body in a protected layer. Normal DOM text extraction may only show controls. Use screenshots/vision for visible pages. Do not attempt to bypass DRM.

Example from prior successful workflow:

- Book: `On Being a Pastor: Understanding Our Calling and Work`
- Authors: Derek J. Prime and Alistair Begg
- Kindle ASIN found in browser reader URL: `B00EZFCHNO`
- Kindle for Web worked even when Kindle for Windows showed only samples and did not sync the book.
- Table of Contents jump opened Chapter 3 at page 47 of 297.
- Body text required screenshot/vision reading.

## Everand/Scribd workflow

1. Open the book in the controlled browser if Titus is already logged in.
2. Use visible page text and page-turning controls.
3. If Everand shows an access boundary such as “available soon,” do not guess. Use other legal sources or ask Titus for screenshots/pages.
4. Internal book search may help confirm phrases, but answers must be marked verified only when the relevant text is visible or sourced.

## Google Books workflow

1. Open the Google Books page for the exact title or edition.
2. Check preview availability, selected pages, table of contents, and common terms.
3. Use previews for verification only. If the page is not available, do not infer exact answers unless supported by another source.

## Internet Archive / Open Library workflow

1. Search Open Library by title and author.
2. Check fields such as `ebook_access`, `has_fulltext`, `ia`, and `public_scan_b`.
3. If borrowable, guide Titus through authorized borrowing. Do not create accounts or handle credentials.
4. If `ebook_access` is `no_ebook`, report that it is listed but not digitally borrowable.

## Publisher samples and retailer previews

Use these for table of contents, chapter headings, and excerpts. They are useful for mapping questions to chapters but may not include full answers.

## Verification discipline

- Do not guess exact answers.
- If only a table of contents is available, say so.
- If screenshots are needed, ask Titus for screenshots or capture visible browser screenshots when authorized.
- When using public snippets, distinguish snippet-confirmed facts from full-text-confirmed answers.

## Bot usage

If Titus sends a book request through WhatsApp or Telegram, the bot should:

1. Identify the title and platform mentioned.
2. Try legal access routes in the order above.
3. Ask Titus to complete login/MFA/payment prompts if needed.
4. If a screenshot is attached, extract visible text and answer from that.
5. Save useful platform findings into a local note or report for future reuse.

Suggested bot phrases Titus may use:

```text
Find this book and help me answer questions.
Open this on Kindle.
Check if this is on Internet Archive.
Use Google Books preview.
Read this screenshot and answer the chapter questions.
```

## Restore note

This skill should be backed up in the Titus AI OS GitHub repository under:

```text
.agents/skills/book-access-workflow/SKILL.md
```

It can also be copied to personal skill folders if needed:

```text
C:\Users\tbank\.agents\skills\book-access-workflow\SKILL.md
C:\Users\tbank\.config\opencode\skills\book-access-workflow\SKILL.md
```
