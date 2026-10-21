param(
    [string]$BaseUrl = 'http://localhost:5189',
    [switch]$StartServer,
    [switch]$SkipTimeout,
    [string]$DllPath
)
$ErrorActionPreference = 'Stop'
$startWindowOptions = @{}
if ($IsWindows) { $startWindowOptions.WindowStyle = 'Hidden' }
$root = Split-Path $PSScriptRoot -Parent
$server = $null
$failures = [System.Collections.Generic.List[string]]::new()
$checks = 0
function Check-Submission($Language, $Problem, $Code, $Mode, $Expected, [switch]$CheckHidden, [string]$CodeFormat) {
    $script:checks++
    $request = @{ problemId=$Problem; language=$Language; code=$Code; mode=$Mode }
    if ($CodeFormat) { $request.codeFormat = $CodeFormat }
    $body = $request | ConvertTo-Json -Compress
    $result = Invoke-RestMethod "$BaseUrl/api/submissions" -Method Post -ContentType 'application/json' -Body $body -NoProxy -TimeoutSec 135 -Headers @{'X-EpiJudge-Client'='local-editor'}
    $label = "$Language $Problem $Mode $Expected"
    if ($result.status -ne $Expected) {
        $script:failures.Add("$label -> $($result.status): $($result.diagnostics)")
        Write-Output "FAIL $label -> $($result.status): $($result.diagnostics)"
    } elseif ($Expected -eq 'Accepted' -and $result.passed -ne $result.total) {
        $script:failures.Add("$label returned inconsistent totals")
    } else { Write-Output "PASS $label ($($result.passed)/$($result.total))" }
    if ($CheckHidden) {
        foreach ($case in $result.cases) {
            if (!$case.hidden -or $null -ne $case.input -or $null -ne $case.expected -or $null -ne $case.actual) {
                $script:failures.Add("$label leaked a hidden test case")
            }
        }
    }
}
function Replace-ScaffoldThrow($Code, $Language, $Replacement) {
    $scaffoldThrow = if ($Language -eq 'cpp') { 'throw std::logic_error("Implement this method");' } else { 'throw new UnsupportedOperationException("Implement this method");' }
    if (!$Code.Contains($scaffoldThrow)) { throw "$Language starter has no expected scaffold throw to replace" }
    return $Code.Replace($scaffoldThrow, $Replacement)
}
try {
    if ($StartServer) {
        $env:ASPNETCORE_ENVIRONMENT = 'Development'
        $env:Frontend__Enabled = 'false'
        $logRoot = Join-Path $root '.epi-runs'
        New-Item -ItemType Directory -Force -Path $logRoot | Out-Null
        $env:Practice__DataDirectory = Join-Path $logRoot ('test-native-data-' + [guid]::NewGuid().ToString('N'))
        $dll = if ($DllPath) { [IO.Path]::GetFullPath($DllPath) } else { Join-Path $root 'EpiJudge.Web\bin\Debug\net10.0\EpiJudge.Web.dll' }
        $content = Join-Path $root 'EpiJudge.Web'
        $server = Start-Process dotnet -ArgumentList @("`"$dll`"", '--urls', $BaseUrl, '--contentRoot', "`"$content`"") -WorkingDirectory $root @startWindowOptions -PassThru -RedirectStandardOutput (Join-Path $logRoot 'native-audit.log') -RedirectStandardError (Join-Path $logRoot 'native-audit.err')
        $ready = $false
        for ($i=0; $i -lt 20; $i++) {
            try { $null = Invoke-RestMethod "$BaseUrl/api/health" -NoProxy -TimeoutSec 1; $ready=$true; break } catch { Start-Sleep -Milliseconds 500 }
        }
        if (!$ready) { throw 'Temporary native audit server did not start.' }
    }
    $problems = Invoke-RestMethod "$BaseUrl/api/problems" -NoProxy -TimeoutSec 20
    foreach ($language in @('cpp','java')) {
        $starters = @($problems | Where-Object { $_.starters.$language.starterCode })
        if ($starters.Count -ne 334) { throw "$language requires 334 starters, got $($starters.Count)" }
        if (@($starters | Where-Object { $_.starters.$language.codeFormat -ne 'callable-v1' }).Count) { throw "$language starters require an explicit callable format" }
        Write-Output "PASS $language catalog: 334 starters"
        $folder = Join-Path $PSScriptRoot "NativeWebFixtures\$language"
        $countFile = if ($language -eq 'cpp') {'count_bits.cc'} else {'CountBits.java'}
        $accepted = Get-Content (Join-Path $folder $countFile) -Raw
        Check-Submission $language 'count_bits' $accepted 'run' 'Accepted'
        Check-Submission $language 'count_bits' $accepted 'submit' 'Accepted' -CheckHidden
        $starter = ($problems | Where-Object id -eq 'count_bits').starters.$language
        $stub = $starter.starterCode
        $wrongCount = Replace-ScaffoldThrow $stub $language 'return 0;'
        Check-Submission $language 'count_bits' $wrongCount 'submit' 'Wrong answer' -CheckHidden -CodeFormat $starter.codeFormat
        Check-Submission $language 'count_bits' ($stub + "`ninvalid syntax!!!") 'run' 'Compilation error' -CodeFormat $starter.codeFormat
        $exception = if ($language -eq 'cpp') {'throw std::runtime_error("native audit");'} else {'throw new RuntimeException("native audit");'}
        Check-Submission $language 'count_bits' (Replace-ScaffoldThrow $stub $language $exception) 'run' 'Runtime error' -CodeFormat $starter.codeFormat
        foreach ($pair in @(
            @('anagrams','anagrams.cc','Anagrams.java'),
            @('reverse_list','reverse_list.cc','ReverseList.java'),
            @('dutch_national_flag','dutch_national_flag.cc','DutchNationalFlag.java'),
            @('copy_posting_list','copy_posting_list.cc','CopyPostingList.java'),
            @('lowest_common_ancestor','lowest_common_ancestor_with_parent.cc','LowestCommonAncestorWithParent.java')
        )) {
            $filename = if ($language -eq 'cpp') {$pair[1]} else {$pair[2]}
            Check-Submission $language $pair[0] (Get-Content (Join-Path $folder $filename) -Raw) 'submit' 'Accepted' -CheckHidden
        }
        $partitionStarter = ($problems | Where-Object id -eq 'dutch_national_flag').starters.$language
        $brokenPartition = Replace-ScaffoldThrow $partitionStarter.starterCode $language 'return;'
        Check-Submission $language 'dutch_national_flag' $brokenPartition 'submit' 'Wrong answer' -CheckHidden -CodeFormat $partitionStarter.codeFormat
        if (!$SkipTimeout) {
            Check-Submission $language 'count_bits' (Replace-ScaffoldThrow $stub $language 'while (true) {}') 'run' 'Time limit exceeded' -CodeFormat $starter.codeFormat
        }
    }
    if ($failures.Count) { throw ($failures -join "`n") }
    Write-Output "PASS all $checks native submission checks, plus both complete catalogs"
} finally {
    if ($server -and !$server.HasExited) {
        try { Invoke-RestMethod "$BaseUrl/api/internal/shutdown" -Method Post -NoProxy -TimeoutSec 5 | Out-Null } catch { }
        if (!$server.WaitForExit(10000)) { $server.Kill($true) }
    }
}
