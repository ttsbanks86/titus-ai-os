# Goldmine Automation - Creator & GitHub Intelligence

$goldDir = "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\intelligence\goldmine"
$date = Get-Date -Format "yyyyMMdd"
$reportPath = Join-Path $goldDir "goldmine-report-$date.md"

$creators = @(
    @{N="Marco Kazandjieff"; T="Developer tools, AI workflows, code exploration"; P="Facebook"},
    @{N="Wassim younes AI"; T="Claude Fable 5, visual AI, prompting"; P="Facebook"},
    @{N="Seb Hardy"; T="Loop engineering, AI coding, GLM models"; P="Facebook"},
    @{N="Salavat Shirgaleev"; T="AI skills, career tools, resume"; P="Facebook"},
    @{N="Giga Qian"; T="AI research, China AI, ASI-Evolve"; P="Facebook"},
    @{N="Devin Karpes"; T="Fable 5 skills, AI tools"; P="Facebook"}
)

$githubRepos = @(
    @{R="1jehuang/jcode"; D="Coding agent harness, Rust, multi-agent swarm"},
    @{R="kpab/claude-fable-5-skills"; D="10 Fable 5-native agent skills - INSTALLED"},
    @{R="ComposioHQ/awesome-claude-skills"; D="Curated Claude Code skills directory"},
    @{R="bytedance/deer-flow"; D="Super agent harness, sandboxed execution"},
    @{R="aaif-goose/goose"; D="Open source AI agent"},
    @{R="n8n-io/n8n"; D="Workflow automation"},
    @{R="thewaltero/mythos-router"; D="Leaked Anthropic reasoning protocol, 210 stars"}
)

$reportLines = @()
$reportLines += "# Goldmine Report - $(Get-Date -Format 'MMMM dd, yyyy')"
$reportLines += ""
$reportLines += "## Tracked Facebook Creators"
$reportLines += ""
foreach ($c in $creators) {
    $reportLines += "* **$($c.N)** - $($c.T) ($($c.P))"
}
$reportLines += ""
$reportLines += "## Tracked GitHub Repositories"
$reportLines += ""
foreach ($r in $githubRepos) {
    $reportLines += "* **$($r.R)** - $($r.D)"
}
$reportLines += ""
$reportLines += "## Recent Finds"
$reportLines += ""
$reportLines += "### From Marco Kazandjieff"
$reportLines += "* jcode: Open-source Rust-based coding agent harness with 20x better memory"
$reportLines += "* Mega-list of 100 tools across 12 categories (pending extraction)"
$reportLines += ""
$reportLines += "### From Wassim younes AI / Devin Karpes"
$reportLines += "* Claude Fable 5 skills - 10 agent skills now installed locally"
$reportLines += "* Fable 5 prompt patterns - extracted and added to PROMPT-MINE"
$reportLines += ""
$reportLines += "### From Seb Hardy"
$reportLines += "* Loop engineering concept - already implemented in PROMPT-MINE agent loop"
$reportLines += "* GLM-5.1 model from Z.ai - tracked for future evaluation"
$reportLines += ""
$reportLines += "### GitHub Gems Found"
$reportLines += "* kpab/claude-fable-5-skills - INSTALLED (10 skills active)"
$reportLines += "* 1jehuang/jcode - CLONED to Live Cowork/jcode-test (ready for testing)"
$reportLines += "* mythos-router - 210 stars, leaked Anthropic reasoning protocol"
$reportLines += ""
$reportLines += "## Next Actions"
$reportLines += "* Extract Marco's 100-tool list when video is available"
$reportLines += "* Test jcode against our current stack"
$reportLines += "* Monitor Fable 5 skill updates (just released June 9)"
$reportLines += "* Check mythos-router for reasoning protocol patterns we can adopt"

$reportLines -join "`r`n" | Out-File -FilePath $reportPath -Encoding UTF8
Write-Output $reportLines -join "`n"