# Design Inspiration Agent
# Continuously monitors top apps for design trends and patterns to adopt
# Runs weekly to keep our apps industry-standard

$reportDir = "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\intelligence\scans"
$date = Get-Date -Format "yyyyMMdd"
$reportFile = Join-Path $reportDir "design-trends-$date.md"

$trends = @"

## Design Trends Observed

### Current Industry Standards (2026)
- Dark glass-morphism with subtle gradients
- Rounded corners (16-20px for cards, 8-12px for buttons)
- Minimal chrome — thin borders, no heavy shadows
- Monochromatic accent colors with 10-30% opacity backgrounds
- System fonts (Inter, SF Pro, Segoe UI)
- Bottom-loaded UI (controls at bottom, content at top)
- Always-on-top floating windows for utility apps
- System tray integration with quick actions
- Animated micro-interactions (0.2s ease transitions)
- Faint glass reflections on cards (15-20% white gradient at top)

### App-Specific Inspirations

**Super Whisper (Voice Dictation)**
- Minimal floating window, always on top
- Dark glass design with blue accent
- Mode selector (Voice/Message/Email/Bullets)
- Hold-to-record with visual waveform
- Auto-paste directly into active app
- System tray with quick mode switching

**Otter.ai (Transcription)**
- Clean card-based layout
- Speaker identification during recording
- Searchable transcript history
- Export options (text, summary, highlights)

**Notion (General Design)**
- Clean sans-serif typography
- Generous whitespace
- Accent colors at 10% opacity for backgrounds
- Thin, subtle borders
- Command palette (Cmd+K)

## Recommendations for Our Apps

1. **EchoKeys Pro** — Already matching Super Whisper design language ✓
2. **NOLA Voice** — Purple accent differentiates it from EchoKeys ✓
3. **All apps** — Keep consistent with dark glass design, rounded corners, system fonts

## Implementation Status

| App | Design | Icons | Shortcuts | Functionality |
|-----|--------|-------|-----------|---------------|
| EchoKeys Pro | ✓ Super Whisper match | ✓ Custom icon | ✓ Desktop | ✓ Hold-to-record + paste |
| NOLA Voice | ✓ NOLA purple brand | ✓ Custom icon | ✓ Desktop | ✓ Ctrl+Shift+N record |
| Auto Hub | — | ✓ Custom icon | ✓ Desktop | Status dashboard |
| Job Intel | — | ✓ Custom icon | ✓ Desktop | Intelligence report |
| Portfolio | — | ✓ Custom icon | ✓ Desktop | Website launcher |

"@

$trends | Out-File -FilePath $reportFile -Encoding UTF8
Write-Output $trends