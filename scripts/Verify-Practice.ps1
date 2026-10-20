param([string]$BaseUrl = 'http://localhost:5196', [string]$DllPath, [switch]$CheckFrontend)
$ErrorActionPreference = 'Stop'
$startWindowOptions = @{}
if ($IsWindows) { $startWindowOptions.WindowStyle = 'Hidden' }
$root = Split-Path $PSScriptRoot -Parent
if (!$DllPath) { $DllPath = Join-Path $root 'EpiJudge.Web/bin/Debug/net10.0/EpiJudge.Web.dll' }
$testRoot = Join-Path $root ('.epi-runs/practice-tests-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path $testRoot | Out-Null
$headers = @{'X-EpiJudge-Client'='local-editor'}
$server = $null
$launch = 0
$checks = 0
$passed = $false
$oldEnvironment = $env:ASPNETCORE_ENVIRONMENT
$oldFrontend = $env:Frontend__Enabled
$oldData = $env:Practice__DataDirectory
$oldCache = $env:EPI_VITE_CACHE_DIR
function Assert($Condition, [string]$Label) {
    if (!$Condition) { throw $Label }
    $script:checks++
    "PASS $Label"
}
function Api([string]$Path, [string]$Method = 'GET', $Body = $null) {
    $params = @{ Uri="$BaseUrl$Path"; Method=$Method; Headers=$headers; NoProxy=$true; TimeoutSec=100 }
    if ($null -ne $Body) { $params.ContentType='application/json'; $params.Body=ConvertTo-Json -InputObject $Body -Depth 30 -Compress }
    $response=Invoke-RestMethod @params
    return $response
}
function Stop-TestServer {
    if ($script:server -and !$script:server.HasExited) {
        try { $null = Api '/api/internal/shutdown' 'POST' } catch { }
        if (!$script:server.WaitForExit(15000)) { $script:server.Kill($true); $script:server.WaitForExit(5000) | Out-Null }
    }
}
function Start-TestServer([string]$DataName) {
    $env:ASPNETCORE_ENVIRONMENT='Development'
    $env:Frontend__Enabled=if($CheckFrontend){'true'}else{'false'}
    $env:Practice__DataDirectory=Join-Path $testRoot $DataName
    $script:launch++
    $env:EPI_VITE_CACHE_DIR=Join-Path $testRoot "vite-cache-$launch"
    $script:server=Start-Process dotnet -ArgumentList @("`"$DllPath`"",'--urls',$BaseUrl,'--contentRoot',"`"$(Join-Path $root 'EpiJudge.Web')`"") -WorkingDirectory $root @startWindowOptions -PassThru -RedirectStandardOutput (Join-Path $testRoot "server-$launch.log") -RedirectStandardError (Join-Path $testRoot "server-$launch.err")
    for($i=0;$i -lt 90;$i++) {
        try { $null=Invoke-RestMethod "$BaseUrl/api/health" -NoProxy -TimeoutSec 1; return } catch { Start-Sleep -Milliseconds 500 }
    }
    throw "Practice test server did not start. See $testRoot"
}
try {
    Start-TestServer 'primary'
    Assert (@((Api '/api/practice').drafts).Count -eq 0) 'Isolated database starts empty'
    if($CheckFrontend) { Assert ((Invoke-WebRequest "$BaseUrl/src/Editor.tsx" -NoProxy).StatusCode -eq 200) 'Frontend and editor available' }
    foreach($language in @('csharp','javascript','python','cpp','java')) {
        $draft=Api "/api/practice/drafts/count_bits/$language" 'PUT' @{code="answer-$language ' -- literal SQL text";revision=0}
        Assert ($draft.revision -eq 1 -and $draft.language -eq $language) "$language draft saved separately"
    }
    $empty=Api '/api/practice/drafts/anagrams/python' 'PUT' @{code='';revision=0}
    Assert ($empty.code -ceq '') 'Empty draft preserved without falling back to a starter'
    $response=Invoke-WebRequest "$BaseUrl/api/practice/drafts/count_bits/csharp" -Method Put -Headers $headers -ContentType application/json -Body '{"code":"stale writer","revision":0}' -NoProxy -SkipHttpErrorCheck
    Assert ($response.StatusCode -eq 409) 'Stale draft revision is rejected'
    $response=Invoke-WebRequest "$BaseUrl/api/practice/drafts/count_bits/csharp" -Method Put -ContentType application/json -Body '{"code":"cross origin","revision":1}' -NoProxy -SkipHttpErrorCheck
    Assert ($response.StatusCode -eq 403) 'Draft writes require same-app request header'

    $http=[Net.Http.HttpClient]::new([Net.Http.HttpClientHandler]@{UseProxy=$false})
    try {
        $requests=@('writer A','writer B') | ForEach-Object {
            $message=[Net.Http.HttpRequestMessage]::new([Net.Http.HttpMethod]::Put,"$BaseUrl/api/practice/drafts/count_bits/csharp")
            $message.Headers.Add('X-EpiJudge-Client','local-editor')
            $message.Content=[Net.Http.StringContent]::new((@{code=$_;revision=1}|ConvertTo-Json),[Text.Encoding]::UTF8,'application/json')
            $http.SendAsync($message)
        }
        $responses=[Threading.Tasks.Task]::WhenAll([Threading.Tasks.Task[Net.Http.HttpResponseMessage][]]$requests).GetAwaiter().GetResult()
        $codes=@($responses | ForEach-Object {[int]$_.StatusCode} | Sort-Object)
        Assert (($codes -join ',') -eq '200,409') 'Concurrent writers cannot silently overwrite each other'
    } finally { $http.Dispose() }

    $wrong='function countBits(x) { return 0; } module.exports={countBits};'
    $correct='function countBits(x) { x>>>=0; let n=0; while(x){n+=x&1;x>>>=1;} return n; } module.exports={countBits};'
    $failed=Api '/api/submissions' 'POST' @{problemId='count_bits';language='javascript';mode='submit';code=$wrong}
    Assert ($failed.status -eq 'Wrong answer') 'Real failed submission recorded'
    Assert (@((Api '/api/practice').progress | Where-Object problemId -eq count_bits)[0].status -eq 'attempted') 'Failed problem is attempted (orange)'
    $accepted=Api '/api/submissions' 'POST' @{problemId='count_bits';language='javascript';mode='submit';code=$correct}
    Assert ($accepted.status -eq 'Accepted' -and $accepted.passed -eq 10001) 'Real accepted full submission recorded'
    $null=Api '/api/submissions' 'POST' @{problemId='count_bits';language='javascript';mode='submit';code=$wrong}
    $progress=@((Api '/api/practice').progress | Where-Object problemId -eq count_bits)[0]
    Assert ($progress.status -eq 'solved' -and $progress.acceptedLanguages -contains 'javascript') 'Solved stays green after a later failure'
    $snapshot=Api "/api/practice/history/$($accepted.id)"
    Assert ($snapshot.code -ceq $correct -and $snapshot.language -eq 'javascript') 'History preserves exact submitted code and language'
    Assert (@($snapshot.result.cases | Where-Object hidden).Count -eq 0) 'Stored result contains no hidden cases'
    $null=Api '/api/practice/drafts/count_bits/javascript' 'PUT' @{code='new draft after submission';revision=1}
    Assert ((Api "/api/practice/history/$($accepted.id)").code -ceq $correct) 'Changing a draft cannot alter submitted source'
    $null=Api '/api/submissions' 'POST' @{problemId='two_sum';language='javascript';mode='run';code='throw new Error("storage fixture");'}
    Assert (@((Api '/api/practice').progress | Where-Object problemId -eq two_sum)[0].status -eq 'attempted') 'Run-only problem remains attempted, not solved'

    $timestamp=[DateTimeOffset]::UtcNow.ToString('O')
    $legacy=@{migrationId='browser-test';drafts=@(@{problemId='anagrams';language='csharp';code='legacy browser answer';revision=0;updatedAt=$timestamp});attempts=@(@{id='legacy:test';problemId='anagrams';language=$null;code=$null;mode='run';status='Wrong answer';passed=0;total=3;elapsedMs=0;timestamp=$timestamp;result=$null;legacy=$true});solvedIds=@('tree_preorder')}
    $null=Api '/api/practice/migrate' 'POST' $legacy
    $again=Api '/api/practice/migrate' 'POST' $legacy
    Assert (!$again.imported -and @((Api '/api/practice/history?problemId=anagrams') | Where-Object id -eq 'legacy:test').Count -eq 1) 'Legacy browser migration is idempotent'
    Assert ($null -eq (Api '/api/practice/history/legacy:test').code) 'Legacy summaries do not invent missing code'
    Assert (@((Api '/api/practice').progress | Where-Object problemId -eq tree_preorder)[0].status -eq 'solved') 'Legacy solved status preserved'

    $solutions=@{
        csharp='public class Solution { public int CountBits(int x) => System.Numerics.BitOperations.PopCount((uint)x); }'
        python="def count_bits(x: int) -> int:`n    return (x & 0xffffffff).bit_count()`n"
        cpp=(Get-Content (Join-Path $PSScriptRoot 'NativeWebFixtures/cpp/count_bits.cc') -Raw)
        java=(Get-Content (Join-Path $PSScriptRoot 'NativeWebFixtures/java/CountBits.java') -Raw)
    }
    foreach($language in @('csharp','python','cpp','java')) {
        foreach($mode in @('run','submit')) {
            $result=Api '/api/submissions' 'POST' @{problemId='count_bits';language=$language;mode=$mode;code=$solutions[$language]}
            Assert ($result.status -eq 'Accepted') "$language $mode grading and source persistence"
            Assert ((Api "/api/practice/history/$($result.id)").code -ceq $solutions[$language]) "$language $mode exact source snapshot"
        }
    }

    $readingId='reading-shared-state'
    $readingCode=@{version=1;notes="My explanation of a lost update. λ";reviewed=$true;checkpoints=@('contract');answers=@{understanding=0}} | ConvertTo-Json -Depth 10 -Compress
    $reading=Api "/api/practice/drafts/$readingId/reading" 'PUT' @{code=$readingCode;revision=0}
    Assert ($reading.code -ceq $readingCode -and $reading.revision -eq 1) 'Reading document autosave preserves notes and review state'
    $badReading=Invoke-WebRequest "$BaseUrl/api/practice/drafts/$readingId/reading" -Method Put -Headers $headers -ContentType application/json -Body (@{code='{}';revision=1}|ConvertTo-Json) -NoProxy -SkipHttpErrorCheck
    Assert ($badReading.StatusCode -eq 400) 'Malformed reading document rejected'
    $badReading=Invoke-WebRequest "$BaseUrl/api/practice/drafts/count_bits/reading" -Method Put -Headers $headers -ContentType application/json -Body (@{code=$readingCode;revision=0}|ConvertTo-Json) -NoProxy -SkipHttpErrorCheck
    Assert ($badReading.StatusCode -eq 400) 'Reading cannot replace a coding draft'
    $badReading=Invoke-WebRequest "$BaseUrl/api/practice/drafts/$readingId/python" -Method Put -Headers $headers -ContentType application/json -Body (@{code='pass';revision=0}|ConvertTo-Json) -NoProxy -SkipHttpErrorCheck
    Assert ($badReading.StatusCode -eq 400) 'Reading cannot use an executable language'
    $readingConflict=Invoke-WebRequest "$BaseUrl/api/practice/drafts/$readingId/reading" -Method Put -Headers $headers -ContentType application/json -Body (@{code=$readingCode.Replace('lost update','different explanation');revision=0}|ConvertTo-Json) -NoProxy -SkipHttpErrorCheck
    Assert ($readingConflict.StatusCode -eq 409) 'Stale reading save cannot overwrite another tab'
    Assert (@((Api '/api/practice').progress | Where-Object problemId -eq $readingId).Count -eq 0) 'Manual reading review never marks a coding problem solved'

    Stop-TestServer
    Start-TestServer 'primary'
    $state=Api '/api/practice'
    Assert (@($state.drafts | Where-Object problemId -eq $readingId)[0].code -ceq $readingCode) 'Reading notes and review survive server restart'
    Assert (@($state.drafts | Where-Object {$_.problemId -eq 'count_bits'}).Count -eq 5) 'All five language drafts survive server restart'
    Assert ((Api "/api/practice/history/$($accepted.id)").code -ceq $correct) 'Submission code survives server restart'
    Assert (@($state.progress | Where-Object problemId -eq count_bits)[0].status -eq 'solved') 'Green solved status survives server restart'
    $backup=Api '/api/practice/export'
    Assert ($backup.version -eq 1 -and $backup.attempts.Count -ge 5) 'Portable backup includes drafts and history'
    $invalid=@{version=999;drafts=@();attempts=@();solvedIds=@()}
    $response=Invoke-WebRequest "$BaseUrl/api/practice/import" -Method Post -Headers $headers -ContentType application/json -Body ($invalid|ConvertTo-Json) -NoProxy -SkipHttpErrorCheck
    Assert ($response.StatusCode -eq 400) 'Invalid backup rejected before writing'
    Stop-TestServer
    Start-TestServer 'restored'
    $null=Api '/api/practice/import' 'POST' $backup
    $restored=Api '/api/practice'
    Assert (@($restored.drafts | Where-Object problemId -eq $readingId)[0].code -ceq $readingCode) 'Reading notes and review transfer to a new database through backup'
    Assert ($restored.drafts.Count -eq $backup.drafts.Count) 'Backup restores drafts into a new database'
    Assert ((Api "/api/practice/history/$($accepted.id)").code -ceq $correct) 'Backup restores exact historical source'
    $null=Api '/api/practice/import' 'POST' $backup
    Assert (@(Api '/api/practice/history?problemId=count_bits').Count -eq @($backup.attempts | Where-Object problemId -eq count_bits).Count) 'Repeated backup import does not duplicate submissions'
    $draft=@($restored.drafts | Where-Object {$_.problemId -eq 'count_bits' -and $_.language -eq 'python'})[0]
    $null=Api '/api/practice/drafts/count_bits/python' 'PUT' @{code='newer local answer';revision=$draft.revision}
    $null=Api '/api/practice/import' 'POST' $backup
    Assert (@((Api '/api/practice').drafts | Where-Object {$_.problemId -eq 'count_bits' -and $_.language -eq 'python'})[0].code -ceq 'newer local answer') 'Import never overwrites an existing draft'
    $summaries=1..55 | ForEach-Object { @{id="legacy-page-$_";problemId='anagrams';language=$null;code=$null;mode='run';status='Wrong answer';passed=0;total=3;elapsedMs=0;timestamp=$timestamp;result=$null;legacy=$true} }
    $null=Api '/api/practice/import' 'POST' @{version=1;drafts=@();attempts=@($summaries);solvedIds=@()}
    $firstPage=@(Api '/api/practice/history?problemId=anagrams')
    $secondPage=@(Api "/api/practice/history?problemId=anagrams&before=$($firstPage[-1].sequence)")
    Assert ($firstPage.Count -eq 50 -and $secondPage.Count -eq 6 -and @(@($firstPage+$secondPage).id | Select-Object -Unique).Count -eq 56) 'History pagination has no omissions or duplicates'

    # A process crash must not lose source or leave an attempt permanently Running.
    $crashCode='while (true) {}'
    $crashClient=[Net.Http.HttpClient]::new([Net.Http.HttpClientHandler]@{UseProxy=$false})
    try {
        $message=[Net.Http.HttpRequestMessage]::new([Net.Http.HttpMethod]::Post,"$BaseUrl/api/submissions")
        $message.Headers.Add('X-EpiJudge-Client','local-editor')
        $message.Content=[Net.Http.StringContent]::new((@{problemId='tree_postorder';language='javascript';mode='run';code=$crashCode}|ConvertTo-Json),[Text.Encoding]::UTF8,'application/json')
        $pending=$crashClient.SendAsync($message)
        $running=$null
        for($i=0;$i -lt 30;$i++) {
            $running=@(Api '/api/practice/history?problemId=tree_postorder' | Where-Object status -eq Running) | Select-Object -First 1
            if($running){break}; Start-Sleep -Milliseconds 100
        }
        Assert ($null -ne $running -and (Api "/api/practice/history/$($running.id)").code -ceq $crashCode) 'Source is durable before grading finishes'
        $server.Kill($true)
        $server.WaitForExit(5000) | Out-Null
        try { $null=$pending.GetAwaiter().GetResult() } catch { }
        Start-TestServer 'restored'
        $recovered=Api "/api/practice/history/$($running.id)"
        Assert ($recovered.status -eq 'Interrupted' -and $recovered.code -ceq $crashCode) 'Crash recovery preserves code and marks abandoned grading interrupted'
    } finally { $crashClient.Dispose() }
    "PASS all $checks answer-storage checks"
    $passed = $true
} finally {
    Stop-TestServer
    $env:ASPNETCORE_ENVIRONMENT=$oldEnvironment
    $env:Frontend__Enabled=$oldFrontend
    $env:Practice__DataDirectory=$oldData
    $env:EPI_VITE_CACHE_DIR=$oldCache
    # Retain a failed run for diagnosis; successful runs leave no private test database behind.
    if ($passed) {
        $absolute=[IO.Path]::GetFullPath($testRoot)
        $allowed=[IO.Path]::GetFullPath((Join-Path $root '.epi-runs'))+[IO.Path]::DirectorySeparatorChar
        if (!$absolute.StartsWith($allowed,[StringComparison]::OrdinalIgnoreCase)) { throw 'Unsafe test cleanup path' }
        Remove-Item -LiteralPath $absolute -Recurse -Force
    }
}
