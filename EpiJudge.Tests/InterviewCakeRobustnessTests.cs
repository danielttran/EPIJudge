using System.Reflection;
using System.Text.Json;
using EpiJudge.Runner;

namespace EpiJudge.Tests;

public sealed class InterviewCakeRobustnessTests
{
    private static readonly MethodInfo MatchesMethod = typeof(SubmissionRunner).Assembly
        .GetType("EpiJudge.Runner.InterviewCakeSubmissionRunner", throwOnError: true)!
        .GetMethod("Matches", BindingFlags.NonPublic | BindingFlags.Static)!;

    [Fact]
    public void CollectionInventoryKeepsEveryExistingQuestionAndAllFiveInterfaces()
    {
        var problems = new ProblemCatalog().Problems;
        Assert.Equal(334, problems.Count);
        Assert.Equal(218, problems.Count(problem => problem.Collection == "epi"));
        Assert.Equal(75, problems.Count(problem => problem.Collection == "blind75"));
        Assert.Equal(41, problems.Count(problem => problem.Collection == "interviewcake"));
        Assert.Equal(334, problems.Select(problem => problem.Id).Distinct().Count());
        foreach (var definition in InterviewCakeCatalog.Definitions)
        {
            Assert.Equal(new[] { "cpp", "csharp", "java", "javascript", "python" }, definition.Starters.Keys.Order().ToArray());
            Assert.All(definition.Starters.Values, starter => Assert.InRange(starter.StarterCode.Length, 1, 40_000));
            Assert.Equal(3, definition.Examples.Length);
        }
    }

    [Theory]
    [InlineData("interviewcake_find-duplicate-optimize-for-space")]
    [InlineData("interviewcake_find-duplicate-optimize-for-space-beast-mode")]
    public void DuplicateValidationAcceptsEveryActualDuplicateWithoutCanonicalTieBreaking(string problemId)
    {
        var test = Case("[[2,3,1,2,3]]", "2");
        Assert.True(Matches(problemId, test, "2"));
        Assert.True(Matches(problemId, test, "3"));
        Assert.False(Matches(problemId, test, "1"));
        Assert.False(Matches(problemId, test, "2.5"));
        Assert.False(Matches(problemId, test, "true"));
    }

    [Fact]
    public void PathValidationAcceptsEitherShortestRouteAndRejectsLongerAndBrokenRoutes()
    {
        const string arguments = """
            [{"a":["b","c"],"b":["a","c","d"],"c":["a","b","d"],"d":["b","c"]},"a","d"]
            """;
        var test = Case(arguments, "[\"a\",\"b\",\"d\"]");
        Assert.True(Matches("interviewcake_mesh-message", test, "[\"a\",\"b\",\"d\"]"));
        Assert.True(Matches("interviewcake_mesh-message", test, "[\"a\",\"c\",\"d\"]"));
        Assert.False(Matches("interviewcake_mesh-message", test, "[\"a\",\"b\",\"c\",\"d\"]"));
        Assert.False(Matches("interviewcake_mesh-message", test, "[\"a\",\"missing\",\"d\"]"));
        Assert.False(Matches("interviewcake_mesh-message", test, "[\"a\",null,\"d\"]"));
        Assert.False(Matches("interviewcake_mesh-message", test, "null"));
        var isolated = Case("[{\"a\":[],\"b\":[]},\"a\",\"b\"]", "null");
        Assert.True(Matches("interviewcake_mesh-message", isolated, "null"));
        Assert.False(Matches("interviewcake_mesh-message", isolated, "[]"));
        var same = Case("[{\"a\":[]},\"a\",\"a\"]", "[\"a\"]");
        Assert.True(Matches("interviewcake_mesh-message", same, "[\"a\"]"));
        Assert.False(Matches("interviewcake_mesh-message", same, "[]"));
    }

    [Fact]
    public void TemperatureValidationAcceptsEveryTiedModeAndChecksEachHistoricalState()
    {
        var test = Case("""
            [["GetMean","Insert","Insert","GetMode","GetMean","Insert","GetMode","GetMean","GetMin","GetMax"],
             [[],[3],[8],[],[],[8],[],[],[],[]]]
            """, "[null,null,null,3,5.5,null,8,6.333333333333333,3,8]");
        const string firstMode = "[null,null,null,3,5.5,null,8,6.333333333333333,3,8]";
        const string alternateMode = "[null,null,null,8,5.5,null,8,6.333333333333333,3,8]";
        Assert.True(Matches("interviewcake_temperature-tracker", test, firstMode));
        Assert.True(Matches("interviewcake_temperature-tracker", test, alternateMode));
        Assert.False(Matches("interviewcake_temperature-tracker", test, "[null,null,null,8,5.5,null,3,6.333333333333333,3,8]"));
        Assert.False(Matches("interviewcake_temperature-tracker", test, "[null,null,null,8,5,null,8,6,3,8]"));
        Assert.False(Matches("interviewcake_temperature-tracker", test, "[null,null,null,8,5.5,null,8,1e10000,3,8]"));
        Assert.False(Matches("interviewcake_temperature-tracker", test, "[null,null,null,\"8\",5.5,null,8,6.333333333333333,3,8]"));
    }

    [Fact]
    public void ObjectResultsCompareByPropertiesAndValuesIncludingNestedErrors()
    {
        var cloud = Case("[\"red blue red\"]", "{\n  \"red\": 2,\n  \"blue\": 1\n}");
        Assert.True(Matches("interviewcake_word-cloud", cloud, "{\"blue\":1,\"red\":2}"));
        Assert.False(Matches("interviewcake_word-cloud", cloud, "{\"blue\":1,\"red\":2,\"extra\":0}"));
        Assert.False(Matches("interviewcake_word-cloud", cloud, "{\"blue\":2,\"red\":1}"));
        var infinite = Case("[[[0,2]],0]", "{\n \"error\" : \"infinite\"\n}");
        Assert.True(Matches("interviewcake_cake-thief", infinite, "{\"error\":\"infinite\"}"));
        Assert.False(Matches("interviewcake_cake-thief", infinite, "{\"error\":\"empty\"}"));
        var empty = Case("[[\"Dequeue\"],[[]]]", "[{\n \"error\" : \"empty\"\n}]");
        Assert.True(Matches("interviewcake_queue-two-stacks", empty, "[{\"error\":\"empty\"}]"));
    }

    [Fact]
    public void FilesValidationChecksSamplingAllGroupsOrientationAndDistinctFullPaths()
    {
        const string arguments = """
            [[{"path":"first/a","content":"same","modified":10},
              {"path":"second/b","content":"same","modified":20},
              {"path":"left","content":"other","modified":30},
              {"path":"right","content":"other","modified":30}]]
            """;
        var test = Case(arguments, "[[\"first/a\",\"second/b\"],[\"left\",\"right\"]]");
        var root = Path.Combine(Path.GetTempPath(), "interviewcake-validation-root");
        var valid = new[]
        {
            new[] { Path.Combine(root, "right"), Path.Combine(root, "left") },
            new[] { Path.Combine(root, "first", "a"), Path.Combine(root, "second", "b") }
        };
        Assert.True(Matches("interviewcake_find-duplicate-files", test, JsonSerializer.Serialize(valid), root));
        Assert.False(Matches("interviewcake_find-duplicate-files", test, JsonSerializer.Serialize(valid.Take(1)), root));
        var reversed = new[] { valid[0], new[] { valid[1][1], valid[1][0] } };
        Assert.False(Matches("interviewcake_find-duplicate-files", test, JsonSerializer.Serialize(reversed), root));
        Assert.False(Matches("interviewcake_find-duplicate-files", test, JsonSerializer.Serialize(valid.Concat([valid[0]])), root));
        Assert.False(Matches("interviewcake_find-duplicate-files", test, "[[\"first/a\",\"second/b\"],[\"left\",\"right\"]]", root));
        Assert.False(Matches("interviewcake_find-duplicate-files", test, JsonSerializer.Serialize(new[] { new[] { valid[1][0], valid[1][0] } }), root));
    }

    [Theory]
    [InlineData("interviewcake_find-duplicate-optimize-for-space")]
    [InlineData("interviewcake_mesh-message")]
    [InlineData("interviewcake_temperature-tracker")]
    [InlineData("interviewcake_find-duplicate-files")]
    public void MalformedActualResultsAreRejectedWithoutEscapingTheValidator(string problemId)
    {
        var definition = InterviewCakeCatalog.Find(problemId)!;
        var repository = ProblemCatalog.FindRepositoryRoot(AppContext.BaseDirectory);
        var test = InterviewCakeCatalog.LoadTests(repository, problemId, false)[0];
        string[] malformed =
        [
            "null", "true", "false", "3.5", "1e10000", "\"wrong\"", "{}", "{\"error\":\"empty\"}",
            "[]", "[null]", "[{}]", "[1,2]", "[[null,null]]", "[[\"a\",1]]", "[[\"a\\u0000b\",\"other\"]]"
        ];
        var wire = definition.Mode == "files" ? new[] { Element(Path.GetTempPath()) } : test.Arguments;
        foreach (var raw in malformed)
        {
            var exception = Record.Exception(() => Assert.False(InvokeMatches(test, Parse(raw), definition, wire)));
            Assert.Null(exception);
        }
        Assert.False(InvokeMatches(test, default, definition, wire));
    }

    private static TestCase Case(string arguments, string expected) =>
        new(Parse(arguments).EnumerateArray().Select(value => value.Clone()).ToArray(), Parse(expected));

    private static JsonElement Parse(string raw)
    {
        using var document = JsonDocument.Parse(raw);
        return document.RootElement.Clone();
    }

    private static JsonElement Element(string value) => JsonSerializer.SerializeToElement(value);

    private static bool Matches(string problemId, TestCase test, string actual, string? filesRoot = null)
    {
        var definition = InterviewCakeCatalog.Find(problemId)!;
        var wire = filesRoot is null ? test.Arguments : [Element(filesRoot)];
        return InvokeMatches(test, Parse(actual), definition, wire);
    }

    private static bool InvokeMatches(TestCase test, JsonElement actual, InterviewCakeDefinition definition, JsonElement[] wire) =>
        (bool)MatchesMethod.Invoke(null, [test, actual, definition, wire])!;
}
