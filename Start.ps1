param([string]$Url = 'http://localhost:5178')
$ErrorActionPreference = 'Stop'
$setup = Join-Path $PSScriptRoot 'scripts/Setup.ps1'
if (!(Test-Path (Join-Path $PSScriptRoot 'epijudge.client/node_modules')) -or
    !(Test-Path (Join-Path $PSScriptRoot 'EpiJudge.Web/bin/Debug/net10.0/EpiJudge.Web.dll'))) {
    & $setup
} else { & $setup -CheckOnly }
Push-Location $PSScriptRoot
try { dotnet run --project EpiJudge.Web --launch-profile Website --urls $Url }
finally { Pop-Location }
