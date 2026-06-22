# Archive Index

## Overview
Nothing is ever deleted. Files that are no longer actively used are moved here for reference. This is a dead-letter directory — content here may be useful for historical reference but is not actively maintained.

## Current State
Archive is organized into subdirectories matching the categories of archived content. See individual directories for details.

## Archive Structure
- [[ChatGPT-Exports/]] — 5,725 ChatGPT-exported files (ABOUT ME)
- [[Daily-Notes/]] — Deprecated daily notes from previous system
- [[Deprecated-Projects/]] — Projects that are no longer active
- [[Legacy-Agents/]] — Agent definitions from Claude Code (now archived)
- [[Legacy-Commands/]] — Commands from previous system
- [[Legacy-Rules/]] — Rules from previous system
- [[Legacy-Skills/]] — Skill definitions from Claude Code (now archived)
- [[Staging/]] — Content awaiting classification or decision

## Restoration
To restore any archived file: `Move-Item -Path "10-Archive/<path>" -Destination "<original-location>"`

## Rules
- No permanent deletion. Archive is forever.
- Archive index updated when new content is added.
- Archive is NOT read at startup — only on demand.

## References
- [[01-Dashboard/Home]]
