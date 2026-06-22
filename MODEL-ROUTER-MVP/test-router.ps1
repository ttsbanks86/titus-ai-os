param(
    [string]$Route = "coding",
    [string]$Prompt = "Say hello from the model router"
)

$ErrorActionPreference = "Stop"

$ConfigPath = Join-Path $PSScriptRoot "router-config.json"
if (-not (Test-Path -LiteralPath $ConfigPath)) {
    throw "router-config.json not found at $ConfigPath"
}

$config = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json

if (-not ($config.routes.PSObject.Properties.Name -contains $Route)) {
    $available = ($config.routes.PSObject.Properties.Name -join ", ")
    throw "Unknown route '$Route'. Available routes: $available"
}

$routeConfig = $config.routes.$Route
$providerName = $routeConfig.provider
$modelKey = $routeConfig.modelKey

if (-not $providerName -or -not $modelKey) {
    throw "Route '$Route' is not a chat route. It may be a reference-only route."
}

$provider = $config.providers.$providerName
if (-not $provider) {
    throw "Provider '$providerName' not found in config."
}

$model = $provider.models.$modelKey
if (-not $model) {
    throw "Model key '$modelKey' not found for provider '$providerName'."
}

$temperature = 0.2
if ($null -ne $routeConfig.temperature) {
    $temperature = [double]$routeConfig.temperature
}

$uri = ($provider.baseUrl.TrimEnd('/')) + "/chat/completions"

$body = @{
    model = $model
    messages = @(
        @{
            role = "system"
            content = "You are a concise local model used by a model-router MVP. Do not ask for secrets."
        },
        @{
            role = "user"
            content = $Prompt
        }
    )
    temperature = $temperature
    stream = $false
} | ConvertTo-Json -Depth 8

$headers = @{
    "Authorization" = "Bearer $($provider.apiKey)"
    "Content-Type" = "application/json"
}

Write-Host "Route: $Route"
Write-Host "Provider: $providerName"
Write-Host "Model: $model"
Write-Host "Endpoint: $uri"
Write-Host "--- Response ---"

try {
    $response = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body -TimeoutSec 120
    if ($response.choices -and $response.choices.Count -gt 0) {
        $message = $response.choices[0].message.content
        Write-Output $message
    } else {
        Write-Output ($response | ConvertTo-Json -Depth 8)
    }
} catch {
    Write-Error "Router test failed for route '$Route' using $providerName/$model. $($_.Exception.Message)"
    exit 1
}
