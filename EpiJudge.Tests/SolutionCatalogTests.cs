using EpiJudge.Runner;

namespace EpiJudge.Tests;

public sealed class SolutionCatalogTests
{
    private readonly ProblemCatalog problems = new();

    [Fact]
    public void EveryCodingQuestionHasACompleteOfflineSolutionInEachLanguage()
    {
        var solutions = new SolutionCatalog(problems);
        Assert.Equal(218, problems.Problems.Count(p=>p.Collection=="epi"));
        Assert.Equal(75, problems.Problems.Count(p=>p.Collection=="blind75"));
        Assert.Equal(41, problems.Problems.Count(p=>p.Collection=="interviewcake"));
        foreach(var problem in problems.Problems)
        foreach(var language in SolutionCatalog.Languages)
        {
            var solution = Assert.IsType<ProblemSolution>(solutions.Find(problem.Id,language));
            Assert.Equal(problem.Id,solution.ProblemId);
            Assert.Equal(problem.Collection,solution.Collection);
            Assert.Equal(language,solution.Language);
            Assert.InRange(solution.Code.Length,1,40_000);
            Assert.DoesNotContain("NotImplementedException",solution.Code);
            Assert.False(string.IsNullOrWhiteSpace(solution.Explanation));
            Assert.False(string.IsNullOrWhiteSpace(solution.TimeComplexity));
            Assert.False(string.IsNullOrWhiteSpace(solution.SpaceComplexity));
            Assert.False(string.IsNullOrWhiteSpace(solution.Attribution));
            {
                Assert.False(string.IsNullOrWhiteSpace(solution.Correctness));
                Assert.False(string.IsNullOrWhiteSpace(solution.Walkthrough));
                Assert.NotEmpty(solution.EdgeCases!);
                Assert.All(solution.EdgeCases!,value=>Assert.False(string.IsNullOrWhiteSpace(value)));
            }
        }
        Assert.Null(solutions.Find("unknown"));
        Assert.Null(solutions.Find("reading-parent-pointer-lca"));
    }

    [Theory]
    [InlineData("csharp")]
    [InlineData("javascript")]
    [InlineData("python")]
    [InlineData("cpp")]
    [InlineData("java")]
    public void EveryLanguageRequiresReasoningBeyondAnApproach(string language)
    {
        var entries = Entries();
        var index = Array.FindIndex(entries, entry => entry.Language == language);
        foreach (var invalid in new[] {
            entries[index] with { Correctness = " " },
            entries[index] with { Walkthrough = null },
            entries[index] with { EdgeCases = [] }
        })
        {
            var changed = entries.ToArray();
            changed[index] = invalid;
            Assert.Throws<InvalidOperationException>(() => SolutionCatalog.Validate(problems, changed));
        }
    }

    [Fact]
    public void MissingDuplicateAndUnknownIdsCannotSilentlyHideCoverageGaps()
    {
        var entries=Entries();
        Assert.Throws<InvalidOperationException>(()=>SolutionCatalog.Validate(problems,entries.Skip(1).ToArray()));
        var duplicate=entries.ToArray();duplicate[0]=duplicate[1];
        Assert.Throws<InvalidOperationException>(()=>SolutionCatalog.Validate(problems,duplicate));
        var unknown=entries.ToArray();unknown[0]=unknown[0] with {ProblemId="not-a-question"};
        Assert.Throws<InvalidOperationException>(()=>SolutionCatalog.Validate(problems,unknown));
    }

    [Theory]
    [InlineData("collection")]
    [InlineData("language")]
    [InlineData("code")]
    [InlineData("explanation")]
    [InlineData("time")]
    [InlineData("space")]
    [InlineData("attribution")]
    [InlineData("correctness")]
    [InlineData("walkthrough")]
    [InlineData("edgeCases")]
    [InlineData("length")]
    public void IncompleteOrMismatchedMetadataFailsClearly(string field)
    {
        var entries=Entries();
        entries[0]=field switch
        {
            "collection"=>entries[0] with {Collection="wrong"},
            "language"=>entries[0] with {Language="ruby"},
            "code"=>entries[0] with {Code=" "},
            "explanation"=>entries[0] with {Explanation=""},
            "time"=>entries[0] with {TimeComplexity=""},
            "space"=>entries[0] with {SpaceComplexity=""},
            "correctness"=>entries[0] with {Correctness=""},
            "walkthrough"=>entries[0] with {Walkthrough=""},
            "edgeCases"=>entries[0] with {EdgeCases=[]},
            "length"=>entries[0] with {Code=new string('x',40_001)},
            _=>entries[0] with {Attribution=""}
        };
        Assert.Throws<InvalidOperationException>(()=>SolutionCatalog.Validate(problems,entries));
    }

    private ProblemSolution[] Entries()=>problems.Problems.SelectMany(p=>SolutionCatalog.Languages.Select(language=>new ProblemSolution(p.Id,p.Collection,language,
        "public class Solution {}","An algorithm.","O(n)","O(n)","Original implementation.","An invariant.","An original trace.",["Empty input."]))).ToArray();
}
