param([string]$BaseUrl = 'http://localhost:5178', [switch]$CheckFrontend)
$ErrorActionPreference = 'Stop'

if ($CheckFrontend) {
    $home = Invoke-WebRequest "$BaseUrl/" -MaximumRedirection 0
    if ([int]$home.StatusCode -ne 200 -or $home.Headers.Location -or
        -not $home.Content.Contains('/src/main.tsx') -or $home.Content.Contains('Launching the SPA proxy')) {
        throw 'The website must serve React directly with HTTP 200 and no redirect.'
    }
    $vite = Invoke-WebRequest "$BaseUrl/@vite/client"
    if ([int]$vite.StatusCode -ne 200 -or -not $vite.Content.Contains('/__vite_hmr')) {
        throw 'The frontend client and hot-reload path are not available through the website origin.'
    }
    Write-Output 'Direct website launch: HTTP 200, no redirect, same-origin hot reload'
}

function Invoke-Judge([string]$Problem, [string]$Code, [string]$Mode = 'run') {
    Invoke-RestMethod "$BaseUrl/api/submissions" -Method Post -ContentType 'application/json' `
        -Headers @{ 'X-EpiJudge-Client' = 'local-editor' } `
        -Body (@{ problemId = $Problem; code = $Code; mode = $Mode } | ConvertTo-Json) -TimeoutSec 90
}
function Assert-Status($Result, [string]$Expected, [string]$Label) {
    if ($Result.status -ne $Expected) { throw "$Label expected $Expected, got $($Result.status): $($Result.diagnostics)" }
    Write-Output "$Label`: $($Result.status) ($($Result.passed)/$($Result.total))"
}

$countBits = @'
public class Solution {
    public int CountBits(int x) {
        var count = 0;
        for (uint value = unchecked((uint)x); value != 0; value &= value - 1) ++count;
        return count;
    }
}
'@
$twoSum = @'
public class Solution {
    public bool HasTwoSum(List<int> values, int target) {
        int left = 0, right = values.Count - 1;
        while (left <= right) {
            var sum = (long)values[left] + values[right];
            if (sum == target) return true;
            if (sum < target) ++left; else --right;
        }
        return false;
    }
}
'@
$anagrams = @'
public class Solution {
    public List<List<string>> FindAnagrams(List<string> dictionary) =>
        dictionary.GroupBy(word => string.Concat(word.OrderBy(character => character)))
            .Where(group => group.Count() > 1).Select(group => group.Reverse().ToList()).Reverse().ToList();
}
'@

$visible = Invoke-Judge 'count_bits' $countBits
Assert-Status $visible 'Accepted' 'Visible cases'
if ($visible.total -ne 3 -or $visible.cases.Count -ne 3 -or $visible.cases[0].hidden) { throw 'Visible case data is missing.' }
Assert-Status (Invoke-Judge 'count_bits' $countBits 'submit') 'Accepted' 'Count Bits full corpus'
Assert-Status (Invoke-Judge 'two_sum' $twoSum 'submit') 'Accepted' 'Two Sum full corpus'
Assert-Status (Invoke-Judge 'anagrams' $anagrams 'submit') 'Accepted' 'Anagrams unordered full corpus'
Assert-Status (Invoke-Judge 'count_bits' 'public class Solution { public int CountBits(int x) => 0; }') 'Wrong answer' 'Wrong answer'
Assert-Status (Invoke-Judge 'count_bits' 'public class Solution { syntax error }') 'Compilation error' 'Compilation error'
Assert-Status (Invoke-Judge 'count_bits' 'public class Solution { public int CountBits(int x) => throw new Exception("Example error"); }') 'Runtime error' 'Runtime error'
Assert-Status (Invoke-Judge 'count_bits' 'public class Solution { public int CountBits(int x) { while (true) {} } }') 'Time limit exceeded' 'Infinite loop timeout'
$hidden = Invoke-Judge 'count_bits' 'public class Solution { public int CountBits(int x) => 0; }' 'submit'
Assert-Status $hidden 'Wrong answer' 'Hidden failure'
foreach ($case in $hidden.cases) {
    if (-not $case.hidden -or $null -ne $case.input -or $null -ne $case.expected -or $null -ne $case.actual) { throw 'Hidden case contents were exposed.' }
}
try {
    Invoke-RestMethod "$BaseUrl/api/submissions" -Method Post -ContentType 'application/json' `
        -Body (@{ problemId = 'count_bits'; code = $countBits; mode = 'run' } | ConvertTo-Json) | Out-Null
    throw 'A request without the client header was accepted.'
} catch [Microsoft.PowerShell.Commands.HttpResponseException] {
    if ([int]$_.Exception.Response.StatusCode -ne 403) { throw }
    Write-Output 'Cross-origin form protection: 403'
}
Write-Output 'Website runner checks passed.'
