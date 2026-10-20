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
function Check-Submission($Language, $Problem, $Code, $Mode, $Expected, [switch]$CheckHidden) {
    $script:checks++
    $body = @{ problemId=$Problem; language=$Language; code=$Code; mode=$Mode } | ConvertTo-Json -Compress
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
        if ($starters.Count -ne 293) { throw "$language requires 293 starters, got $($starters.Count)" }
        Write-Output "PASS $language catalog: 293 starters"
        $folder = Join-Path $PSScriptRoot "NativeWebFixtures\$language"
        $countFile = if ($language -eq 'cpp') {'count_bits.cc'} else {'CountBits.java'}
        $accepted = Get-Content (Join-Path $folder $countFile) -Raw
        Check-Submission $language 'count_bits' $accepted 'run' 'Accepted'
        Check-Submission $language 'count_bits' $accepted 'submit' 'Accepted' -CheckHidden
        $stub = ($problems | Where-Object id -eq 'count_bits').starters.$language.starterCode
        Check-Submission $language 'count_bits' $stub 'submit' 'Wrong answer' -CheckHidden
        Check-Submission $language 'count_bits' ($stub + "`ninvalid syntax!!!") 'run' 'Compilation error'
        $exception = if ($language -eq 'cpp') {'throw std::runtime_error("native audit");'} else {'throw new RuntimeException("native audit");'}
        Check-Submission $language 'count_bits' ($stub.Replace('return 0;', $exception)) 'run' 'Runtime error'
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
        $brokenPartition = ($problems | Where-Object id -eq 'dutch_national_flag').starters.$language.starterCode
        Check-Submission $language 'dutch_national_flag' $brokenPartition 'submit' 'Wrong answer' -CheckHidden
        if (!$SkipTimeout) {
            Check-Submission $language 'count_bits' ($stub.Replace('return 0;', 'while (true) {}')) 'run' 'Time limit exceeded'
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
