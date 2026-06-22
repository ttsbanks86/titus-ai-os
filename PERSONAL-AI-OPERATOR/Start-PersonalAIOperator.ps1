param(
    [string]$Command = "help",
    [string]$Route = "cheap",
    [string]$Prompt = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigPath = Join-Path $Root "operator-config.json"
$Config = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
$LogPath = Join-Path $Config.paths.logs ("operator-" + (Get-Date -Format "yyyyMMdd") + ".log")
$PromptMinePath = $Config.paths.promptMine

# PROMPT-MINE Agent Loop
Write-OpLog "PROMPT-MINE: Agent initialized with $($Config.loop.protocol)"

function Write-OpLog {
    param([string]$Message)
    $line = "[{0}] {1}" -f (Get-Date -Format "s"), $Message
    Add-Content -LiteralPath $LogPath -Value $line
}

function Invoke-LocalBrain {
    param([string]$RouteName, [string]$Text)
    $router = $Config.paths.modelRouter
    if (-not (Test-Path -LiteralPath $router)) {
        throw "Model router not found: $router"
    }
    & powershell.exe -ExecutionPolicy Bypass -File $router -Route $RouteName -Prompt $Text
}

function Show-Help {
    $lines = @(
        "Titus Personal AI Operator v$($Config.version)",
        "PROMPT-MINE: Agent Loop Protocol Active",
        "",
        "Commands:",
        "  help                         Show this menu",
        "  ask -Prompt '...'            Ask local model router",
        "  brief                        Generate morning briefing",
        "  apps                         List visible desktop windows via agent-cu",
        "  screenshot                   Take desktop screenshot via agent-cu",
        "  open-url -Prompt 'URL'       Open a URL in the default browser",
        "  graphify                     Print Claude Code /graphify instructions",
        "  business -Prompt '...'       Draft a business-ops request prompt",
        "  promptmine                   Show PROMPT-MINE loaded patterns",
        "  loop -Prompt '...'           Execute a task using the agent loop protocol",
        "  safety                       Show approval boundaries",
        "",
        "Agent Loop: ANALYZE → PLAN → EXECUTE → OBSERVE → ITERATE",
        "",
        "Examples:",
        "  .\Start-PersonalAIOperator.ps1 -Command ask -Route cheap -Prompt 'Summarize my day'",
        "  .\Start-PersonalAIOperator.ps1 -Command loop -Prompt 'Research BA jobs'",
        "  .\Start-PersonalAIOperator.ps1 -Command apps"
    )
    $lines -join [Environment]::NewLine
}

function Show-Safety {
    "Approval required before: " + ($Config.approvalRequired -join ", ")
}

function Show-PromptMine {
    $master = Join-Path $PromptMinePath "MASTER-SYSTEM-PROMPT.md"
    if (Test-Path -LiteralPath $master) {
        Get-Content -LiteralPath $master -Raw
    } else {
        "PROMPT-MINE patterns loaded: Agent Loop, Anti-List, Constructive Refusal, Identity Awareness"
    }
}

function Invoke-AgentLoop {
    param([string]$TaskPrompt)
    $step = 1
    $maxSteps = $Config.loop.maxIterations
    $lines = @(
        "PROMPT-MINE Agent Loop: $($Config.loop.protocol)",
        "",
        ("Task: " + $TaskPrompt),
        ("Max iterations: " + $maxSteps),
        ""
    )
    $lines += "[$step] ANALYZE — Understanding the request..."
    $lines += "[$step] PLAN — Determining approach..."
    $lines += "[$step] EXECUTE — Running via model router..."
    $step++
    $result = Invoke-LocalBrain -RouteName $Route -Text $TaskPrompt
    $lines += "[$step] OBSERVE — Result received"
    $lines += ""
    $lines += "OUTPUT:"
    $lines += $result
    $lines -join [Environment]::NewLine
}

function Show-Briefing {
    $now = Get-Date
    $lines = @(
        "# Morning Briefing",
        "",
        ("Date: " + $now.ToString("yyyy-MM-dd")),
        ("Time: " + $now.ToString("HH:mm")),
        "",
        "## Suggested Focus",
        "1. Review urgent messages and calendar.",
        "2. Pick one revenue task: lead follow-up, proposal, invoice, or content.",
        "3. Pick one systems task: document, automate, or clean up a workflow.",
        "",
        "## AI Operator Status",
        ("- Local model router: " + $Config.capabilities.localModels),
        ("- Desktop control: " + $Config.capabilities.desktopControl),
        ("- Browser launch: " + $Config.capabilities.browserLaunch),
        ("- Graphify: " + $Config.capabilities.graphify),
        ("- Business Ops Experts: " + $Config.capabilities.businessOps),
        "",
        "## First Move",
        "Ask: business -Prompt 'Create today's priority list for my business'"
    )
    $lines -join [Environment]::NewLine
}

Write-OpLog "Command=$Command Route=$Route Prompt=$Prompt"

switch ($Command.ToLowerInvariant()) {
    "help" { Show-Help }
    "ask" { Invoke-LocalBrain -RouteName $Route -Text $Prompt }
    "brief" { Show-Briefing }
    "apps" { agent-cu windows --human }
    "screenshot" { agent-cu screenshot --path (Join-Path $Root "logs\operator-screenshot.png") --human }
    "open-url" {
        if (-not $Prompt.StartsWith("http")) { throw "Prompt must be a full URL beginning with http or https." }
        Start-Process $Prompt
        "Opened URL: $Prompt"
    }
    "graphify" {
        $lines = @(
            "In Claude Code, run:",
            "  /graphify .",
            "",
            "Then use:",
            "  /graphify query 'what connects X to Y?'",
            "  /graphify explain 'ConceptName'"
        )
        $lines -join [Environment]::NewLine
    }
    "business" {
        $lines = @(
            "Paste this into Claude Code or OpenCode:",
            "",
            "/business-ops $Prompt",
            "",
            "Safety: approve before sending emails, WhatsApp messages, invoices, or external actions."
        )
        $lines -join [Environment]::NewLine
    }
    "safety" { Show-Safety }
    "promptmine" { Show-PromptMine }
    "loop" { Invoke-AgentLoop -TaskPrompt $Prompt }
    default { throw "Unknown command '$Command'. Use -Command help." }
}
