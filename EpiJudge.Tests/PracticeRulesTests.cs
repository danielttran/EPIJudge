using EpiJudge.Web;
using EpiJudge.Runner;

namespace EpiJudge.Tests;

public sealed class PracticeRulesTests
{
    private static Draft Draft => new("count_bits", "python", "code", 0, "2026-01-01T00:00:00Z");
    private static SavedAttempt Attempt => new("a", "count_bits", "python", "code", "submit", "Accepted", 1, 1, 1, "2026-01-01T00:00:00Z", null);
    private static PracticeBackup Backup => new(1, [Draft], [Attempt], ["count_bits"]);
    private static bool Valid(PracticeBackup? backup) => PracticeBackupValidator.Validate(backup, id => id == "count_bits");

    [Fact]
    public void ValidEmptyFullAndLegacyBackupsAreAccepted()
    {
        Assert.True(Valid(new(1, [], [], []))); Assert.True(Valid(Backup));
        Assert.True(Valid(Backup with { Attempts = [Attempt with { Code = null, Language = null, Result = null, Legacy = true }] }));
    }

    public static IEnumerable<object[]> InvalidBackups()
    {
        yield return [null!]; yield return [Backup with { Version = 2 }];
        yield return [Backup with { Drafts = null! }]; yield return [Backup with { Attempts = null! }]; yield return [Backup with { SolvedIds = null! }];
        yield return [Backup with { Drafts = new Draft[2001] }]; yield return [Backup with { Attempts = new SavedAttempt[100001] }];
        yield return [Backup with { SolvedIds = new string[1001] }]; yield return [Backup with { SolvedIds = ["unknown"] }];
        foreach (var draft in new Draft?[] { null, Draft with { ProblemId = "unknown" }, Draft with { ProblemId = null! },
            Draft with { Language = "rust" }, Draft with { Code = null! }, Draft with { Code = new string('x', 40001) },
            Draft with { UpdatedAt = "invalid" }, Draft with { Revision = -1 } })
            yield return [Backup with { Drafts = [draft!] }];
        foreach (var attempt in new SavedAttempt?[] { null, Attempt with { Id = "" }, Attempt with { Id = new string('a',201) },
            Attempt with { ProblemId = "unknown" }, Attempt with { Language = "rust" }, Attempt with { Code = new string('x',40001) },
            Attempt with { Mode = "other" }, Attempt with { Status = "" }, Attempt with { Status = new string('a',101) },
            Attempt with { Passed = -1 }, Attempt with { Total = 0 }, Attempt with { ElapsedMs = double.NaN },
            Attempt with { ElapsedMs = double.PositiveInfinity }, Attempt with { ElapsedMs = -1 }, Attempt with { Timestamp = "invalid" },
            Attempt with { Result = new("a","Accepted",1,1,1,null,null!) },
            Attempt with { Result = new("a","Accepted",1,1,1,null,new CaseResult[10002]) },
            Attempt with { Result = new("a","Accepted",1,1,1,null,[null!]) },
            Attempt with { Result = new("a","Accepted",1,1,1,null,[new(1,true,null,null,null,null,double.NaN,false)]) } })
            yield return [Backup with { Attempts = [attempt!] }];
    }
    [Theory]
    [MemberData(nameof(InvalidBackups))]
    public void RejectsInvalidBackupBeforeImport(PracticeBackup? backup) => Assert.False(Valid(backup));

    [Fact]
    public void MaximumCodeLengthAndEmptyCodeAreValid()
    {
        Assert.True(Valid(Backup with { Drafts = [Draft with { Code = "" }] }));
        Assert.True(Valid(Backup with { Drafts = [Draft with { Code = new string('x', 40000) }] }));
    }

    [Theory]
    [InlineData("run", "Accepted", "attempted")]
    [InlineData("submit", "Accepted", "solved")]
    [InlineData("submit", "Wrong answer", "attempted")]
    [InlineData("run", "Compilation error", "attempted")]
    [InlineData("submit", "Running", null)]
    [InlineData("submit", "Not run", null)]
    public void ProgressRules(string mode, string status, string? expected)
    {
        var progress = PracticeProgress.Calculate([new("p", "python", mode, status)]);
        if (expected is null) Assert.Empty(progress);
        else Assert.Equal(expected, Assert.Single(progress).Status);
    }

    [Fact]
    public void SolvedIsMonotonicAcrossLanguagesAndLaterFailures()
    {
        var progress = PracticeProgress.Calculate([
            new("p","python","submit","Accepted"), new("p","java","submit","Accepted"),
            new("p","python","submit","Accepted"), new("p","cpp","submit","Wrong answer"),
            new("legacy",null,"submit","Accepted"), new("other","cpp","run","Accepted")]);
        var solved = Assert.Single(progress, p => p.ProblemId == "p");
        Assert.Equal("solved", solved.Status); Assert.Equal(new[] { "java", "python" }, solved.AcceptedLanguages);
        Assert.Empty(Assert.Single(progress, p => p.ProblemId == "legacy").AcceptedLanguages);
        Assert.Equal("attempted", Assert.Single(progress, p => p.ProblemId == "other").Status);
    }
}
