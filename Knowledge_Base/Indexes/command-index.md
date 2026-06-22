# Command Index

## Overview
Quick reference for all available commands across the Live Cowork ecosystem.

---

## File System Commands

### Read/Write
| Command | Purpose | Usage |
|---------|---------|-------|
| `read` | Read file contents | `read(filePath)` |
| `write` | Create/overwrite file | `write(filePath, content)` |
| `edit` | Edit file content | `edit(filePath, oldString, newString)` |

### Search/Navigation
| Command | Purpose | Usage |
|---------|---------|-------|
| `glob` | Find files by pattern | `glob(pattern)` |
| `grep` | Search file contents | `grep(pattern)` |
| `read_directory` | List directory contents | `read_directory(path)` |

---

## Browser Automation Commands

### Navigation
| Command | Purpose | Usage |
|---------|---------|-------|
| `browser_navigate` | Go to URL | `browser_navigate(url)` |
| `browser_click` | Click element | `browser_click(target)` |
| `browser_type` | Type text | `browser_type(target, text)` |
| `browser_fill_form` | Fill multiple fields | `browser_fill_form(fields)` |

### Extraction
| Command | Purpose | Usage |
|---------|---------|-------|
| `browser_snapshot` | Get page snapshot | `browser_snapshot()` |
| `browser_take_screenshot` | Capture screenshot | `browser_take_screenshot(type)` |
| `browser_evaluate` | Run JavaScript | `browser_evaluate(function)` |

---

## Communication Commands

### Gmail
| Command | Purpose | Usage |
|---------|---------|-------|
| `gmail_list_messages` | List emails | `gmail_list_messages(query)` |
| `gmail_get_message` | Get email content | `gmail_get_message(id)` |
| `gmail_send_message` | Send email | `gmail_send_message(to, subject, body)` |
| `gmail_create_label` | Create label | `gmail_create_label(name)` |

### LinkedIn
| Command | Purpose | Usage |
|---------|---------|-------|
| `linkedin_search_people` | Search professionals | `linkedin_search_people(keywords)` |
| `linkedin_get_person_profile` | View profile | `linkedin_get_person_profile(username)` |
| `linkedin_send_message` | Send message | `linkedin_send_message(username, message)` |
| `linkedin_connect_with_person` | Connect | `linkedin_connect_with_person(username)` |

---

## Research Commands

### Web Research
| Command | Purpose | Usage |
|---------|---------|-------|
| `websearch` | Search web | `websearch(query)` |
| `webfetch` | Fetch URL content | `webfetch(url)` |
| `firecrawl_scrape` | Scrape webpage | `firecrawl_scrape(url, formats)` |
| `firecrawl_search` | Search and scrape | `firecrawl_search(query)` |

### Perplexity
| Command | Purpose | Usage |
|---------|---------|-------|
| `perplexity_ask` | Ask question | `perplexity_ask(messages)` |
| `perplexity_search` | Search web | `perplexity_search(query)` |
| `perplexity_research` | Deep research | `perplexity_research(messages)` |

---

## Documentation Commands

### Notion
| Command | Purpose | Usage |
|---------|---------|-------|
| `notion_API-post-page` | Create page | `notion_API-post-page(parent, properties)` |
| `notion_API-retrieve-a-page` | Get page | `notion_API-retrieve-a-page(page_id)` |
| `notion_API-patch-page` | Update page | `notion_API-patch-page(page_id, properties)` |
| `notion_API-post-search` | Search pages | `notion_API-post-search(query)` |
| `notion_API-query-data-source` | Query database | `notion_API-query-data-source(data_source_id)` |

---

## Knowledge Management Commands

### Claude Memory
| Command | Purpose | Usage |
|---------|---------|-------|
| `claude-mem_search` | Search memory | `claude-mem_search(query)` |
| `claude-mem_memory_add` | Add observation | `claude-mem_memory_add(content)` |
| `claude-mem_memory_context` | Get context | `claude-mem_memory_context(query)` |
| `claude-mem_query_corpus` | Query knowledge | `claude-mem_query_corpus(name, question)` |

---

## Finance Commands

### Yahoo Finance
| Command | Purpose | Usage |
|---------|---------|-------|
| `yahoo-finance_get_quote` | Get stock quote | `yahoo-finance_get_quote(symbol)` |
| `yahoo-finance_get_financials` | Get financials | `yahoo-finance_get_financials(symbol, statement)` |
| `yahoo-finance_get_news` | Get stock news | `yahoo-finance_get_news(symbol)` |
| `yahoo-finance_search_symbols` | Search stocks | `yahoo-finance_search_symbols(query)` |

---

## System Commands

### Bash/PowerShell
| Command | Purpose | Usage |
|---------|---------|-------|
| `bash` | Run command | `bash(command, description)` |

### Environment
| Command | Purpose | Usage |
|---------|---------|-------|
| `envsitter_keys` | List env keys | `envsitter_keys(filePath)` |
| `envsitter_set` | Set env value | `envsitter_set(filePath, key, value)` |
| `envsitter_get` | Get env value | `envsitter_get(filePath, key)` |

---

## Quick Reference by Task

| Task | Primary Commands |
|------|-----------------|
| Read file | `read`, `filesystem_read_text_file` |
| Write file | `write`, `filesystem_write_file` |
| Search files | `glob`, `filesystem_search_files` |
| Search content | `grep`, `filesystem_search_files` |
| Browse website | `playwright_browser_navigate`, `playwright_browser_snapshot` |
| Send email | `linkedin_send_message`, Gmail MCP |
| Research topic | `websearch`, `perplexity_ask` |
| Create document | `notion_API-post-page` |
| Check stocks | `yahoo-finance_get_quote` |

---

*Last Updated: 2026-06-07*
*Version: 1.0.0*
