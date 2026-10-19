param([switch]$Coverage)
$ErrorActionPreference = 'Stop'

# Referenced web/runner projects must also build here: the development server
# can hold their normal bin/Debug assemblies open on Windows.
$testBuild = Join-Path $PSScriptRoot '.epi-runs/test-build'
$testProject = Join-Path $PSScriptRoot 'EpiJudge.Tests/EpiJudge.Tests.csproj'
Push-Location $PSScriptRoot
try {
    $testArguments = @('test', $testProject, '--artifacts-path', $testBuild, '-p:ShouldRunNpmInstall=false')
    if ($Coverage) { $testArguments += '--collect:XPlat Code Coverage' }
    & dotnet @testArguments
    if ($LASTEXITCODE -ne 0) { throw 'Backend tests failed.' }

    Push-Location (Join-Path $PSScriptRoot 'epijudge.client')
    try {
        if (!(Test-Path -LiteralPath 'node_modules')) {
            & npm ci
            if ($LASTEXITCODE -ne 0) { throw 'Frontend dependency installation failed.' }
        }
        $testCommand = if ($Coverage) { 'test:coverage' } else { 'test' }
        & npm run $testCommand
        if ($LASTEXITCODE -ne 0) { throw 'Frontend tests failed.' }
    } finally { Pop-Location }
} finally { Pop-Location }

Write-Output 'All backend and frontend tests passed.'
