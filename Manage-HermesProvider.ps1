param(
  [Parameter(Mandatory=$true)]
  [ValidateSet("status","openrouter","ollama","disable-openrouter-fallback","restore-openrouter")]
  [string]$Action
)

$configPath = "C:\Users\tbank\AppData\Local\hermes\config.yaml"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item -LiteralPath $configPath -Destination "$configPath.provider-switch-backup.$timestamp" -Force

$py = @"
from pathlib import Path
import sys, yaml
path = Path(r'$configPath')
action = '$Action'
cfg = yaml.safe_load(path.read_text(encoding='utf-8')) or {}
model = cfg.get('model') if isinstance(cfg.get('model'), dict) else {}
providers = cfg.get('providers') if isinstance(cfg.get('providers'), dict) else {}
if action == 'status':
    print('Provider:', model.get('provider'))
    print('Model:', model.get('default') or model.get('model'))
    print('Fallbacks:', cfg.get('fallback_providers', []))
    print('Configured providers:', ', '.join(providers.keys()))
    raise SystemExit(0)
if action == 'openrouter':
    model['provider'] = 'openrouter'
    model['default'] = 'deepseek/deepseek-v4-flash'
    cfg['model'] = model
    cfg['fallback_providers'] = []
elif action == 'ollama':
    model['provider'] = 'local-ollama'
    model['default'] = 'qwen2.5-coder:14b'
    model['base_url'] = 'http://localhost:11434/v1'
    cfg['model'] = model
    cfg['fallback_providers'] = []
elif action == 'disable-openrouter-fallback':
    cfg['fallback_providers'] = []
    # Leaves OpenRouter configured, but prevents silent fallback.
elif action == 'restore-openrouter':
    model['provider'] = 'openrouter'
    model['default'] = 'deepseek/deepseek-v4-flash'
    model.pop('base_url', None)
    cfg['model'] = model
    cfg['fallback_providers'] = []
path.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True, width=1000), encoding='utf-8')
print('Updated Hermes provider action:', action)
print('Provider:', cfg.get('model', {}).get('provider'))
print('Model:', cfg.get('model', {}).get('default') or cfg.get('model', {}).get('model'))
"@
$pyPath = Join-Path $env:TEMP "hermes-provider-switch.py"
Set-Content -LiteralPath $pyPath -Value $py
python $pyPath
