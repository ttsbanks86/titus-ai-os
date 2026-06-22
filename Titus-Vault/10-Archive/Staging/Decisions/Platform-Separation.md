# Platform Separation

Decision: keep three standalone AI systems connected by one memory/registry layer.

## OpenCode

Location: `C:\Users\tbank\.config\opencode`

Role: primary daily operator and execution layer. Keep curated agents/skills only.

## Goose / .agents

Location: `C:\Users\tbank\.agents\skills`

Role: reusable personal workflow skills. Keep portable, non-OpenCode-specific workflows.

## Claude / Cloud

Location: `C:\Users\tbank\.claude`

Role: specialist research, review, deep skill library, and advanced Claude workflows.

## Workspace Skills

Location: `C:\Users\tbank\Desktop\Live Cowork\.agents\skills`

Role: project-specific media/video/HyperFrames workflows.

## Rule

Do not merge every skill into OpenCode. Separate runtime-specific tools and connect them through memory, registry, and Command Center.
