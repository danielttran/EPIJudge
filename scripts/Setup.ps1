param([switch]$CheckOnly)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$settings = Join-Path $root '.epijudge-tools.json'
if (Test-Path -LiteralPath $settings) {
    $local = Get-Content -LiteralPath $settings -Raw | ConvertFrom-Json
    foreach ($property in $local.PSObject.Properties) {
        if ($property.Name -in @('EPI_NODE_PATH','EPI_PYTHON_PATH','EPI_JAVA_HOME','EPI_CPP_COMPILER','EPI_VCVARS64') -and
            $property.Value -and ![Environment]::GetEnvironmentVariable($property.Name)) {
            [Environment]::SetEnvironmentVariable($property.Name, [string]$property.Value, 'Process')
        }
    }
}
function Find-Tool([string]$Name, [string]$Override) {
    $configured = if ($Override) { [Environment]::GetEnvironmentVariable($Override) } else { $null }
    if ($configured -and (Test-Path -LiteralPath $configured)) { return $configured }
    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if ($command -and !($Name -eq 'python' -and $command.Source -like '*\Microsoft\WindowsApps\*')) { return $command.Source }
    return $null
}
$missing = [System.Collections.Generic.List[string]]::new()
$dotnet = Find-Tool 'dotnet' ''
if (!$dotnet) { $missing.Add('.NET 10 SDK: https://dotnet.microsoft.com/download/dotnet/10.0') }
else {
    Push-Location $root
    try { $version = & $dotnet --version; if ($LASTEXITCODE -ne 0 -or $version -notmatch '^10\.') { $missing.Add('Install the .NET 10 SDK selected by global.json.') } else { Write-Output "PASS .NET SDK $version" } }
    finally { Pop-Location }
}
$node = Find-Tool 'node' 'EPI_NODE_PATH'
if (!$node) { $missing.Add('Node.js 24 LTS on PATH: https://nodejs.org/') }
else {
    $version = & $node -p 'process.versions.node'
    if ($LASTEXITCODE -ne 0 -or [int]($version.Split('.')[0]) -lt 24) { $missing.Add('Node.js 24 or newer is required.') }
    else { Write-Output "PASS Node.js $version" }
    $env:PATH = (Split-Path $node -Parent) + [IO.Path]::PathSeparator + $env:PATH
}
$python = Find-Tool 'python' 'EPI_PYTHON_PATH'
if (!$python) { $python = Find-Tool 'python3' 'EPI_PYTHON_PATH' }
if (!$python) { $missing.Add('Python 3.10+ on PATH: https://www.python.org/downloads/') }
else {
    $version = & $python -c 'import sys; print("%d.%d" % sys.version_info[:2])'
    if ($LASTEXITCODE -ne 0 -or [version]$version -lt [version]'3.10') { $missing.Add('Python 3.10 or newer is required.') }
    else { Write-Output "PASS Python $version"; $env:EPI_PYTHON_PATH = $python }
}
$javaHome = if ($env:EPI_JAVA_HOME) { $env:EPI_JAVA_HOME } else { $env:JAVA_HOME }
$javac = if ($javaHome) { Join-Path $javaHome ('bin' + [IO.Path]::DirectorySeparatorChar + 'javac.exe') } else { Find-Tool 'javac' '' }
if ($javaHome -and !(Test-Path -LiteralPath $javac)) { $javac = Join-Path $javaHome 'bin/javac' }
if (!$javac -or !(Test-Path -LiteralPath $javac)) { $missing.Add('JDK 21+ on PATH or JAVA_HOME: https://adoptium.net/temurin/releases/?version=21') }
else {
    $version = (& $javac -version 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or $version -notmatch 'javac (\d+)' -or [int]$Matches[1] -lt 21) { $missing.Add('JDK 21 or newer is required.') }
    else { Write-Output "PASS $version" }
}
$cpp = Find-Tool 'g++' 'EPI_CPP_COMPILER'
if (!$cpp) { $cpp = Find-Tool 'clang++' 'EPI_CPP_COMPILER' }
$vcvars = $env:EPI_VCVARS64
if (!$cpp -and !$vcvars -and $env:OS -eq 'Windows_NT') {
    foreach ($base in @($env:ProgramFiles, ${env:ProgramFiles(x86)})) {
        $vs = Join-Path $base 'Microsoft Visual Studio'
        if (!(Test-Path -LiteralPath $vs)) { continue }
        foreach ($year in Get-ChildItem -LiteralPath $vs -Directory) {
            foreach ($edition in Get-ChildItem -LiteralPath $year.FullName -Directory) {
                $candidate = Join-Path $edition.FullName 'VC/Auxiliary/Build/vcvars64.bat'
                if (Test-Path -LiteralPath $candidate) { $vcvars = $candidate }
            }
        }
    }
}
if (!$cpp -and (!$vcvars -or !(Test-Path -LiteralPath $vcvars))) { $missing.Add('A C++17 compiler: Visual Studio C++ build tools on Windows, or g++/clang++ on PATH.') }
else { Write-Output 'PASS C++ compiler'; if ($vcvars) { $env:EPI_VCVARS64 = $vcvars } }
if ($missing.Count) { throw ("Install these prerequisites, then rerun scripts/Setup.ps1:`n - " + ($missing -join "`n - ")) }
if ($CheckOnly) { return }
Push-Location (Join-Path $root 'epijudge.client')
try {
    $npm = Find-Tool 'npm.cmd' ''; if (!$npm) { $npm = Find-Tool 'npm' '' }
    if (!$npm) { throw 'npm is missing from the Node.js installation.' }
    & $npm ci; if ($LASTEXITCODE -ne 0) { throw 'npm ci failed.' }
    & $npm run build; if ($LASTEXITCODE -ne 0) { throw 'Frontend build failed.' }
} finally { Pop-Location }
Push-Location $root
try { & $dotnet build EPIJudge.Web.slnx --maxcpucount:1; if ($LASTEXITCODE -ne 0) { throw 'Website build failed.' } }
finally { Pop-Location }
Write-Output 'Setup complete. Run ./Start.ps1 to start the website.'
