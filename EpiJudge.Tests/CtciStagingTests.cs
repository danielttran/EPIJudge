using System.Text.Json;
using EpiJudge.Runner;

namespace EpiJudge.Tests;

public sealed class CtciStagingTests
{
    private static readonly string Root = ProblemCatalog.FindRepositoryRoot(AppContext.BaseDirectory);
    private static CtciStagingDefinition Definition(string reference) => CtciStagingCatalog.Load(Root).Single(row => row.Ref == reference);
    private static JsonElement Json<T>(T value) => JsonSerializer.SerializeToElement(value);
    private static TestCase Case(object?[] arguments, object? expected) => new(arguments.Select(Json).ToArray(), Json(expected));
    private static JsonElement Observe(int?[][] before, int? returned = null, bool? boolean = null,
        int[]? ids = null, int[]? values = null, int?[][]? after = null) => Json(new
        {
            before, after = after ?? before, returnedId = returned, returnedBool = boolean,
            reachableIds = ids ?? [], reachableValues = values ?? [], cycle = false
        });

    [Fact]
    public void OnlyTheReviewedSnapshotEntersTheLibrary()
    {
        using var inventory = JsonDocument.Parse(File.ReadAllText(Path.Combine(Root, "ctci6", "inventory.json")));
        var approved = inventory.RootElement.GetProperty("questions").EnumerateArray()
            .Where(row => row.GetProperty("classification").GetString() == "coding")
            .Select(row => "ctci6_" + row.GetProperty("ref").GetString()!.Replace('.', '_')).ToHashSet();
        Assert.True(approved.SetEquals(CtciCatalog.Problems.Select(problem => problem.Id)));
        Assert.Equal(218, new ProblemCatalog().Problems.Count(problem => problem.Collection == "epi"));
        Assert.DoesNotContain(CtciCatalog.Problems, problem => problem.Id == "ctci6_5_5");
        var staged = CtciStagingCatalog.Load(Root);
        Assert.True(staged.Count >= CtciCatalog.Problems.Count);
        Assert.All(staged, definition => Assert.Equal(5, definition.Languages.Count));
    }

    [Theory]
    [InlineData("csharp")]
    [InlineData("javascript")]
    [InlineData("python")]
    [InlineData("cpp")]
    [InlineData("java")]
    public void SuppliedEntriesUseTheExistingCallablePreparationWithoutRegistration(string language)
    {
        int livePairs = CallableCodeCatalog.All.Count;
        var definition = Definition("2.2").Callable(language) with { ProblemId = "ctci6_unpublished" };
        var prepared = CallableCodeCatalog.PrepareCallable(definition, definition.SolutionCode);
        Assert.Equal(definition.Filename, prepared.Filename);
        Assert.Equal(CallableCodeCatalog.CallableFormat, prepared.CodeFormat);
        Assert.Contains("LinkedListNode", prepared.Code);
        Assert.Equal(livePairs, CallableCodeCatalog.All.Count);
        Assert.Null(CallableCodeCatalog.Find(definition.ProblemId, language));
    }

    [Theory]
    [InlineData("../outside.cs")]
    [InlineData("bad\".cs")]
    [InlineData("")]
    public void SuppliedCallableFilenamesMustRemainLocalAndValidForLineDirectives(string filename)
    {
        var entry = Definition("1.1").Callable("csharp") with { Filename = filename };
        Assert.Throws<ArgumentException>(() => CallableCodeCatalog.PrepareCallable(entry, entry.SolutionCode));
    }

    [Theory]
    [InlineData("3.1")]
    [InlineData("3.2")]
    [InlineData("3.3")]
    [InlineData("3.4")]
    [InlineData("3.6")]
    [InlineData("10.10")]
    [InlineData("16.25")]
    public void JavaStateClassUsesItsOwnMatchingFilename(string reference)
    {
        var definition = Definition(reference);
        Assert.Equal(definition.Method + ".java", definition.Callable("java").Filename);
        Assert.Equal(definition.Callable("java").Filename, CallableCodeCatalog.Find(definition.Id, "java")!.Filename);
        if (reference == "3.1") Assert.Contains("capacity: int", definition.Languages["python"].Signature);
    }

    [Fact]
    public void ListyResultsEnforceQueryBoundsAndAcceptAnyMatchingIndex()
    {
        var definition = Definition("10.4");
        var test = Case([new[] { 1, 1, 2, 4 }, 1], 0);
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = 1, probes = 4, mutationOk = true })));
        foreach (int probes in new[] { -1, 1000 }) Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = 1, probes, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = -1, probes = 4, mutationOk = true })));
    }

    [Theory]
    [InlineData("csharp")]
    [InlineData("javascript")]
    [InlineData("python")]
    [InlineData("cpp")]
    [InlineData("java")]
    public void ListyApiIsVisibleWithoutItsPrivateJudgeStorage(string language)
    {
        var reference = Assert.Single(CallableCodeCatalog.Find("ctci6_10_4", language)!.References);
        Assert.Contains("Listy", reference.Names);
        Assert.Contains("ElementAt", reference.Code);
        Assert.DoesNotContain("JudgeListy", reference.Code);
    }

    [Fact]
    public void StreamRankCountsOtherEqualOccurrencesAndAbsentValuesRemainAbsent()
    {
        var definition = Definition("10.10");
        var test = Case([new[] { "RankTracker", "Track", "Track", "Track", "Track", "GetRank", "GetRank" }, new int[][] { [], [5], [1], [4], [4], [4], [2] }], new object?[] { null, null, null, null, null, 2, -1 });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new object?[] { null, null, null, null, null, 2, -1 }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new object?[] { null, null, null, null, null, 1, -1 }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new object?[] { null, null, null, null, null, 2, 1 }, mutationOk = true })));
    }

    [Fact]
    public void DuplicateOutputsPreserveRepeatedEncounterOrderAndMultiplicity()
    {
        var definition = Definition("10.8");
        var test = Case([new[] { 8, 1, 8, 8, 32000, 32000 }], new[] { 8, 8, 32000 });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { 8, 8, 32000 }, mutationOk = true })));
        foreach (var values in new int[][] { [8, 32000], [32000, 8, 8] }) Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = values, mutationOk = true })));
    }

    [Fact]
    public void SmallestDifferenceAcceptsExactWidenedEndpointResult()
    {
        var definition = Definition("16.6");
        var test = Case([new[] { int.MinValue }, new[] { int.MaxValue }], 4294967295L);
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = 4294967295L, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = 1, mutationOk = true })));
    }

    [Fact]
    public void ComposedWordsResolveLongestTiesAndRejectAnUncomposedSelfMatch()
    {
        var definition = Definition("17.15");
        var test = Case([new[] { "cat", "dog", "dogcat", "catdog" }], "catdog");
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = "catdog", mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = "dogcat", mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, Case([new[] { "cat", "cat" }], ""), Json(new { actual = "cat", mutationOk = true })));
    }

    [Fact]
    public void PatternMappingsAllowEmptyStringsButCannotIgnoreATrailingSuffix()
    {
        var definition = Definition("16.18");
        Assert.Null(CtciStagingGrader.FailureReason(definition, Case(["ab", "x"], true), Json(new { actual = true, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, Case(["aa", "xxx"], false), Json(new { actual = true, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, Case(["ab", "x"], true), Json(new { actual = 1, mutationOk = true })));
    }

    [Fact]
    public void AdditionOnlyDivisionTruncatesTowardZero()
    {
        var definition = Definition("16.9");
        var test = Case([-7, 3, "divide"], -2);
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = -2, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = -3, mutationOk = true })));
    }

    [Fact]
    public void CacheResultsDistinguishMissingValuesFromStoredEmptyStrings()
    {
        var definition = Definition("16.25");
        var test = Case([1, new[] { "LRUCache", "Set", "Get", "Get" }, new[] { 0, 7, 7, 8 }, new[] { "", "", "", "" }], new object?[] { null, null, "", null });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new object?[] { null, null, "", null }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new object?[] { null, null, null, null }, mutationOk = true })));
    }

    [Fact]
    public void BuildOrderAcceptsEveryValidFullOrdering()
    {
        var definition = Definition("4.7");
        var test = Case([4, new int[][] { [0, 2], [1, 2], [2, 3] }], new[] { 0, 1, 2, 3 });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { 1, 0, 2, 3 }, mutationOk = true })));
        foreach (var order in new int[][] { [], [0, 1, 2], [0, 0, 2, 3], [2, 0, 1, 3] })
            Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = order, mutationOk = true })));
    }

    [Fact]
    public void BuildOrderRejectsPartialOutputFromACyclicComponent()
    {
        var definition = Definition("4.7");
        var test = Case([3, new int[][] { [0, 1], [1, 0] }], Array.Empty<int>());
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = Array.Empty<int>(), mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { 2 }, mutationOk = true })));
    }

    [Theory]
    [InlineData("csharp")]
    [InlineData("javascript")]
    [InlineData("python")]
    [InlineData("cpp")]
    [InlineData("java")]
    public void TreeNodeApiIsVisibleWithoutPrivateIdentityOrDecoderHelpers(string language)
    {
        var reference = Assert.Single(CallableCodeCatalog.Find("ctci6_4_6", language)!.References);
        Assert.Contains("TreeNode", reference.Names);
        foreach (string field in new[] { "Data", "Left", "Right", "Parent" }) Assert.Contains(field, reference.Code);
        Assert.DoesNotContain("nodeId", reference.Code);
        Assert.DoesNotContain("readTree", reference.Code);
    }

    [Fact]
    public void SuccessorRequiresOriginalIdentityAndReadonlyParentLinks()
    {
        var definition = Definition("4.6");
        var test = Case([new { nodes = new int[][] { [2, 1, -1], [1, -1, -1] }, selected = 1 }], 0);
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = 0, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = -2, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = 0, mutationOk = false })));
    }

    [Fact]
    public void DuplicateLeftBstAndDownwardPathContractsRemainDistinct()
    {
        var bst = Definition("4.5");
        var validLeft = Case([new { nodes = new int[][] { [5, 1, -1], [5, -1, -1] }, selected = 0 }], true);
        Assert.Null(CtciStagingGrader.FailureReason(bst, validLeft, Json(new { actual = true, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(bst, validLeft, Json(new { actual = false, mutationOk = true })));
        var paths = Definition("4.12");
        var siblings = Case([new { nodes = new int[][] { [0, 1, 2], [0, -1, -1], [0, -1, -1] }, selected = 0 }, 0], 5);
        Assert.Null(CtciStagingGrader.FailureReason(paths, siblings, Json(new { actual = 5, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(paths, siblings, Json(new { actual = 6, mutationOk = true })));
    }

    [Fact]
    public void MinimalTreeAcceptsDifferentValidMiddleChoices()
    {
        var definition = Definition("4.2");
        var lower = new { root = 0, nodes = new int[][] { [1, -1, 1, -1], [2, -1, -1, 0] } };
        var upper = new { root = 0, nodes = new int[][] { [2, 1, -1, -1], [1, -1, -1, 0] } };
        var test = Case([new[] { 1, 2 }], upper);
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = lower, mutationOk = true })));
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = upper, mutationOk = true })));
    }

    [Fact]
    public void MinimalTreeRequiresMinimumHeightAndCorrectParents()
    {
        var definition = Definition("4.2");
        var chain = new { root = 0, nodes = new int[][] { [1, -1, 1, -1], [2, -1, 2, 0], [3, -1, -1, 1] } };
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, Case([new[] { 1, 2, 3 }], chain), Json(new { actual = chain, mutationOk = true })));
        var wrongParent = new { root = 0, nodes = new int[][] { [1, -1, 1, -1], [2, -1, -1, -1] } };
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, Case([new[] { 1, 2 }], wrongParent), Json(new { actual = wrongParent, mutationOk = true })));
    }

    [Fact]
    public void DepthListsRequireOriginalNodeIdentitiesInLeftToRightOrder()
    {
        var definition = Definition("4.3");
        var test = Case([new { nodes = new int[][] { [7, 1, 2], [7, -1, -1], [7, -1, -1] }, selected = 0 }], new int[][] { [0], [1, 2] });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [0], [1, 2] }, mutationOk = true })));
        foreach (var wrong in new int[][][] { [[7], [7, 7]], [[-2], [-2, -2]], [[0], [2, 1]] })
            Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = wrong, mutationOk = true })));
    }

    [Fact]
    public void BstSequencesAllowOuterReorderingWithoutLosingInnerOrderOrMultiplicity()
    {
        var definition = Definition("4.9");
        var test = Case([new { nodes = new int[][] { [2, 1, 2], [1, -1, -1], [3, -1, -1] }, selected = 0 }], new int[][] { [2, 1, 3], [2, 3, 1] });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [2, 3, 1], [2, 1, 3] }, mutationOk = true })));
        foreach (var wrong in new int[][][] { [[2, 1, 3], [2, 1, 3], [2, 3, 1]], [[1, 2, 3], [2, 3, 1]] })
            Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = wrong, mutationOk = true })));
        var empty = Case([new { nodes = Array.Empty<int[]>(), selected = -1 }], new int[][] { [] });
        Assert.Null(CtciStagingGrader.FailureReason(definition, empty, Json(new { actual = new int[][] { [] }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, empty, Json(new { actual = Array.Empty<int[]>(), mutationOk = true })));
    }

    [Fact]
    public void CircusTowerAllowsMaximumTiesButRequiresBothDimensionsStrict()
    {
        var definition = Definition("17.8");
        var test = Case([new int[][] { [1, 1], [1, 2], [2, 3] }], new[] { 0, 2 });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { 1, 2 }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { 0, 1 }, mutationOk = true })));
    }

    [Fact]
    public void ReSpaceRequiresOptimalActualTokenCoverageAndAcceptsUnknownGrouping()
    {
        var definition = Definition("17.13");
        var test = Case(["abcd", new[] { "ab", "abc", "cd" }], new[] { "ab", "cd" });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { "ab", "cd" }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { "abc", "d" }, mutationOk = true })));
        var unknown = Case(["xyz", Array.Empty<string>()], new[] { "x", "y", "z" });
        Assert.Null(CtciStagingGrader.FailureReason(definition, unknown, Json(new { actual = new[] { "xyz" }, mutationOk = true })));
    }

    [Fact]
    public void WordTransformationAcceptsAValidNonshortestSimplePath()
    {
        var definition = Definition("17.22");
        var words = new[] { "aaa", "aba", "abb", "aab", "bab", "bbb" };
        var test = Case(["aaa", "bbb", words], new[] { "aaa", "aab", "bab", "bbb" });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = words, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { "aaa", "bbb" }, mutationOk = true })));
    }

    [Fact]
    public void WordRectangleAcceptsMaximumOrientationsAndVocabularyReuse()
    {
        var definition = Definition("17.25");
        var test = Case([new[] { "ab", "a", "b" }], new[] { "ab" });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { "a", "b" }, mutationOk = true })));
        var reused = Case([new[] { "aa", "a" }], new[] { "aa", "aa" });
        Assert.Null(CtciStagingGrader.FailureReason(definition, reused, Json(new { actual = new[] { "aa", "aa" }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, reused, Json(new { actual = new[] { "a" }, mutationOk = true })));
    }

    [Fact]
    public void SparseSimilarityPreservesDocumentIdsAndActualCounts()
    {
        var definition = Definition("17.26");
        var expected = new int[][] { [10, 20, 2, 4] };
        var test = Case([new[] { 20, 10 }, new int[][] { [1, 2, 3], [2, 3, 4] }], expected);
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = expected, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [10, 20, 1, 2] }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [0, 1, 2, 4] }, mutationOk = true })));
    }

    [Fact]
    public void AntRenderingUsesVisitedBoundsAndOverlaysTheFinalDirection()
    {
        var definition = Definition("16.22");
        var test = Case([5], new[] { ".U", "#.", "##" });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { ".U", "#.", "##" }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { "#.", "##" }, mutationOk = true })));
    }

    [Fact]
    public void MultiSearchKeepsOverlapsAndTheLastEmptyPatternBoundary()
    {
        var definition = Definition("17.17");
        var test = Case(["aaa", new[] { "aa", "" }], new int[][] { [0, 1], [0, 1, 2, 3] });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [0, 1], [0, 1, 2, 3] }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [0], [0, 1, 2] }, mutationOk = true })));
    }

    [Fact]
    public void PairSumUsesDisjointOccurrencesRatherThanAllIndexPairs()
    {
        var definition = Definition("16.24");
        var test = Case([new[] { 2, 2, 2 }, 4], new int[][] { [2, 2] });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [2, 2] }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [2, 2], [2, 2], [2, 2] }, mutationOk = true })));
    }

    [Fact]
    public void SumSwapDoesNotAcceptAValueObtainedByWrappingTheRequiredCandidate()
    {
        var definition = Definition("16.21");
        var test = Case([new[] { 0 }, new[] { int.MinValue, int.MaxValue, int.MaxValue, int.MaxValue, 3 }], Array.Empty<int>());
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = Array.Empty<int>(), mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { 0, int.MinValue }, mutationOk = true })));
    }

    [Fact]
    public void AnagramsAcceptAnyContiguousGroupOrderButKeepEveryOccurrence()
    {
        var definition = Definition("10.2");
        var test = Case([new[] { "ab", "x", "ba", "ab", "" }], new[] { "", "ab", "ab", "ba", "x" });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { "ba", "ab", "ab", "", "x" }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { "ab", "x", "ba", "ab", "" }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { "ab", "ba", "x", "" }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new object?[] { "ab", "ba", "ab", "x", null }, mutationOk = true })));
    }

    [Fact]
    public void DuplicateSearchesAcceptAnyMatchAndSparseGapsAreNotTargets()
    {
        var rotated = Definition("10.3");
        var test = Case([new[] { 1, 1, 2, 1 }, 1], 0);
        foreach (int index in new[] { 0, 1, 3 }) Assert.Null(CtciStagingGrader.FailureReason(rotated, test, Json(new { actual = index, mutationOk = true })));
        foreach (int index in new[] { -1, 2, 4 }) Assert.NotNull(CtciStagingGrader.FailureReason(rotated, test, Json(new { actual = index, mutationOk = true })));
        var sparse = Definition("10.5");
        var gaps = Case([new[] { "", "a", "", "a" }, ""], -1);
        Assert.Null(CtciStagingGrader.FailureReason(sparse, gaps, Json(new { actual = -1, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(sparse, gaps, Json(new { actual = 0, mutationOk = true })));
    }

    [Fact]
    public void MatrixSearchAcceptsAlternativeCoordinatesAndRejectsInvalidOnes()
    {
        var definition = Definition("10.9");
        var test = Case([new int[][] { [1, 1], [1, 2] }, 1], new[] { 0, 0 });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { 1, 0 }, mutationOk = true })));
        foreach (var coordinate in new int[][] { [-1, -1], [1, 1], [2, 0], [] })
            Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = coordinate, mutationOk = true })));
    }

    [Fact]
    public void PeaksRequireTheMultisetAndOddPeakOrientation()
    {
        var definition = Definition("10.11");
        var test = Case([new[] { 3, 1, 2 }], new[] { 1, 3, 2 });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { 2, 3, 1 }, mutationOk = true })));
        foreach (var values in new int[][] { [3, 1, 2], [1, 9, 2] }) Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = values, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { 2, 3, 1 }, mutationOk = false })));
    }

    [Fact]
    public void MergeRequiresBothCorrectValuesAndPreservationObservation()
    {
        var definition = Definition("10.1");
        var test = Case([new[] { 1, 4, 99, 99 }, 2, new[] { 2, 3 }], new[] { 1, 2, 3, 4 });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { 1, 2, 3, 4 }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { 1, 2, 3, 4 }, mutationOk = false })));
    }

    [Fact]
    public void RobotAcceptsAlternativePathsButRejectsDiagonalAndBlockedSteps()
    {
        var definition = Definition("8.2");
        var test = Case([new int[][] { [1, 1], [1, 1] }], new int[][] { [0, 0], [1, 0], [1, 1] });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [0, 0], [0, 1], [1, 1] }, mutationOk = true })));
        foreach (var path in new int[][][] { [], [[0, 0], [1, 1]], [[0, 0], [0, 1], [0, 0], [1, 0], [1, 1]] })
            Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = path, mutationOk = true })));
        var blocked = Case([new int[][] { [1, 0], [0, 1] }], Array.Empty<int[]>());
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, blocked, Json(new { actual = new int[][] { [0, 0], [1, 1] }, mutationOk = true })));
    }

    [Fact]
    public void MagicIndexAcceptsAnyValidIndexAndRejectsFalseAbsence()
    {
        var definition = Definition("8.3");
        var test = Case([new[] { 0, 1, 1, 3 }, false], 0);
        foreach (int value in new[] { 0, 1, 3 })
            Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = value, mutationOk = true })));
        foreach (int value in new[] { -1, 2, 4, int.MaxValue })
            Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = value, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = 0, mutationOk = false })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = true, mutationOk = true })));
        Assert.Null(CtciStagingGrader.FailureReason(definition, Case([Array.Empty<int>(), true], -1), Json(new { actual = -1, mutationOk = true })));
    }

    [Fact]
    public void QueensMayReorderBoardsButCannotSortEachBoardsColumns()
    {
        var definition = Definition("8.12");
        var test = definition.Tests(Root, true)[0];
        var boards = test.Expected.EnumerateArray().Select(board => board.EnumerateArray().Select(v => v.GetInt32()).ToArray()).ToArray();
        Assert.Equal(92, boards.Length);
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = boards.Reverse(), mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = boards.Select(board => board.Order()), mutationOk = true })));
        boards[1] = boards[0];
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = boards, mutationOk = true })));
    }

    [Fact]
    public void PowerSetAcceptsBothKindsOfReorderingButRejectsDuplicateSubsets()
    {
        var test = Case([new[] { 3, 1 }], new int[][] { [], [3], [1], [3, 1] });
        var definition = Definition("8.4");
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [1, 3], [1], [], [3] }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [], [3], [1], [3, 1], [1, 3] }, mutationOk = true })));
    }

    [Theory]
    [InlineData("8.7")]
    [InlineData("8.8")]
    [InlineData("8.9")]
    public void StringEnumerationsAcceptAnyOrderButRejectRepeatedOrMissingResults(string reference)
    {
        var definition = Definition(reference);
        var test = definition.Tests(Root, true)[0];
        var values = test.Expected.EnumerateArray().Select(value => value.GetString()!).Reverse().ToArray();
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = values, mutationOk = true })));
        values[1] = values[0];
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = values, mutationOk = true })));
    }

    [Fact]
    public void SetGradingRejectsInputMutationAndBooleanMembers()
    {
        var definition = Definition("8.4");
        var test = Case([new[] { 1 }], new int[][] { [], [1] });
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [], [1] }, mutationOk = false })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new object[][] { [], [true] }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new long[][] { [], [long.MaxValue] }, mutationOk = true })));
    }

    [Fact]
    public void BitResultsMustUseTheSignedPatternRatherThanAnUnsignedAlias()
    {
        var test = Case([0, -1, 0, 31], -1);
        Assert.Null(CtciStagingGrader.FailureReason(Definition("5.1"), test, Json(new { actual = -1, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(Definition("5.1"), test, Json(new { actual = 4294967295L, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(Definition("5.1"), test, Json(new { actual = true, mutationOk = true })));
    }

    [Fact]
    public void StateTranscriptsKeepTypedResultsAndDocumentedErrors()
    {
        var definition = Definition("3.1");
        var test = Case([new[] { "ThreeStacks", "IsEmpty" }, new[] { new[] { 1 }, new[] { 0 } }], new object?[] { null, true });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new object?[] { null, true }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new object?[] { null, 1 }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new object?[] { null, true }, mutationOk = 1 })));
    }

    [Fact]
    public void AnimalIdentityFailureCannotPassByMatchingDisplayedIds()
    {
        var test = Case([new[] { "AnimalShelter" }, new object?[] { Array.Empty<int>() }], new object?[] { null });
        Assert.NotNull(CtciStagingGrader.FailureReason(Definition("3.6"), test, Json(new { actual = new object?[] { null }, mutationOk = false })));
    }

    [Fact]
    public void SortedStackMustKeepEveryDuplicate()
    {
        var test = Case([new[] { 2, 1, 2 }], new[] { 1, 2, 2 });
        Assert.Null(CtciStagingGrader.FailureReason(Definition("3.5"), test, Json(new { actual = new[] { 1, 2, 2 }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(Definition("3.5"), test, Json(new { actual = new[] { 1, 2 }, mutationOk = true })));
    }

    [Fact]
    public void PartitionAllowsUnstableOrderAndLargerValuesBeforeEqualPivotValues()
    {
        var test = Case([new[] { 5, 1, 4, 2 }, 4], new[] { 1, 2, 5, 4 });
        var observed = Observe([[5, 1], [1, 2], [4, 3], [2, null]], returned: 3,
            ids: [3, 1, 0, 2], values: [2, 1, 5, 4], after: [[5, 2], [1, 0], [4, null], [2, 1]]);
        Assert.Null(CtciStagingGrader.FailureReason(Definition("2.4"), test, observed));
    }

    [Fact]
    public void KthResultMustBeTheOriginalNodeRatherThanAnEqualValuedCopy()
    {
        var test = Case([new[] { 7, 7 }, 1], 1);
        var observed = Observe([[7, 1], [7, null]], returned: 2);
        Assert.Contains("original", CtciStagingGrader.FailureReason(Definition("2.2"), test, observed)!);
    }

    [Fact]
    public void InputObservationsMustMatchTheDeclaredGraph()
    {
        var test = Case([new[] { 7, 7 }, 1], 1);
        var observed = Observe([[9, 1], [7, null]], returned: 1);
        Assert.Contains("topology", CtciStagingGrader.FailureReason(Definition("2.2"), test, observed)!);
    }

    [Fact]
    public void DeletionPreservesTheBypassedSuccessorAlias()
    {
        var test = Case([new[] { 8, 4, 7, 2 }, 1], new { success = true, values = new[] { 8, 7, 2 } });
        var observed = Observe([[8, 1], [4, 2], [7, 3], [2, null]], boolean: true,
            ids: [0, 1, 3], values: [8, 7, 2], after: [[8, 1], [7, 3], [7, null], [2, null]]);
        Assert.Contains("successor aliases", CtciStagingGrader.FailureReason(Definition("2.3"), test, observed)!);
    }

    [Fact]
    public void SumMayNotAliasAnOperandEvenWhenItsDigitsAreCorrect()
    {
        var test = Case([new[] { 1 }, Array.Empty<int>(), false], new[] { 1 });
        var observed = Observe([[1, null]], returned: 0, ids: [0], values: [1]);
        Assert.Contains("new sum list", CtciStagingGrader.FailureReason(Definition("2.5"), test, observed)!);
    }

    [Fact]
    public void IntersectionDisplaysAnIndexInTheFirstListRatherThanTheInternalUnion()
    {
        var test = Case([new[] { 4, 4 }, new[] { 4 }, new[] { 9, 2 }], 2);
        var observed = Observe([[4, 1], [4, 3], [4, 3], [9, 4], [2, null]], returned: 3);
        Assert.Null(CtciStagingGrader.FailureReason(Definition("2.7"), test, observed));
        Assert.Equal(2, CtciStagingGrader.Display(Definition("2.7"), test, observed).GetInt32());
    }

    [Fact]
    public void ACollisionNodeIsNotNecessarilyTheCycleEntry()
    {
        var test = Case([new[] { 6, 1, 6, 4, 8 }, 2], 2);
        var observed = Observe([[6, 1], [1, 2], [6, 3], [4, 4], [8, 2]], returned: 3);
        Assert.Contains("cycle-entry", CtciStagingGrader.FailureReason(Definition("2.8"), test, observed)!);
    }
    [Fact]
    public void BestLineAcceptsScalingAndUsesExactWideArithmetic()
    {
        var definition = Definition("16.14");
        var test = Case([new int[][] { [0, 0], [1, 1], [2, 2], [0, 1] }], new[] { 1, -1, 0 });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { int.MaxValue, -int.MaxValue, 0 }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { 0, 0, 0 }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { 1, 0, 0 }, mutationOk = true })));
    }

    [Fact]
    public void BabyNamesAcceptsAnyRepresentativeAndIncludesZeroComponents()
    {
        var definition = Definition("17.7");
        var test = Case([new[] { "John", "Jon", "Johnny", "Chris" }, new[] { 10, 3, 0, 0 }, new int[][] { [0, 1], [1, 2], [1, 0] }], new int[][] { [0, 13], [3, 0] });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [3, 0], [2, 13] }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [0, 13] }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new int[][] { [0, 13], [1, 13], [3, 0] }, mutationOk = true })));
    }
    [Fact]
    public void CalculatorRequiresRealDivisionAndFiniteValuesWithinTolerance()
    {
        var definition = Definition("16.26");
        var test = Case(["1/3"], 1.0 / 3);
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = 1.0 / 3 + 0.0000005, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = 0, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = true, mutationOk = true })));
    }

    [Fact]
    public void ContinuousMediansRequireEveryActualHalfIntegerValue()
    {
        var definition = Definition("17.20");
        var test = Case([new[] { int.MinValue, int.MaxValue }], new[] { (double)int.MinValue, -0.5 });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { (double)int.MinValue, -0.5 }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { (double)int.MinValue, 0.0 }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { -0.5 }, mutationOk = true })));
    }
    [Fact]
    public void SegmentIntersectionAllowsAnyOverlapPointButRejectsInfiniteLineOnlyCrossings()
    {
        var definition = Definition("16.3");
        var overlap = Case([new int[][] { [0, 0], [4, 0], [2, 0], [6, 0] }], new[] { 2.0, 0 });
        Assert.Null(CtciStagingGrader.FailureReason(definition, overlap, Json(new { actual = new[] { 3.0, 0 }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, overlap, Json(new { actual = new[] { 5.0, 0 }, mutationOk = true })));
        var disjoint = Case([new int[][] { [0, 0], [1, 1], [2, 0], [2, 3] }], Array.Empty<double>());
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, disjoint, Json(new { actual = new[] { 2.0, 2 }, mutationOk = true })));
    }

    [Fact]
    public void SquareBisectorAcceptsEitherEndpointOrderAndAnyConcentricDirection()
    {
        var definition = Definition("16.13");
        var separate = Case([new int[][] { [0, 0, 2], [4, 0, 2] }], new[] { 0.0, 1, 6, 1 });
        Assert.Null(CtciStagingGrader.FailureReason(definition, separate, Json(new { actual = new[] { 6.0, 1, 0, 1 }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, separate, Json(new { actual = new[] { 1.0, 1, 5, 1 }, mutationOk = true })));
        var concentric = Case([new int[][] { [0, 0, 4], [1, 1, 2] }], new[] { 2.0, 0, 2, 4 });
        Assert.Null(CtciStagingGrader.FailureReason(definition, concentric, Json(new { actual = new[] { 0.0, 0, 4, 4 }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, concentric, Json(new { actual = new[] { 1.0, 2, 3, 2 }, mutationOk = true })));
    }
    [Fact]
    public void XmlEncodingKeepsLiteralTokenBoundariesAndBothEndMarkers()
    {
        var definition = Definition("16.12");
        var test = Case([new[] { "node" }, new[] { "Text" }, new[] { Array.Empty<int>() }, new[] { 0 }, new[] { "key" }, new[] { "A B" }, new[] { "node", "key" }, new[] { 7, 2 }], new[] { "7", "2", "A B", "0", "Text", "0" });
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { "7", "2", "A B", "0", "Text", "0" }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { "7", "2", "A", "B", "0", "Text", "0" }, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = new[] { "7", "2", "A B", "0", "Text" }, mutationOk = true })));
    }
    [Fact]
    public void MissingNumberRequiresBitQueryEvidenceWithinItsLinearBudget()
    {
        var definition = Definition("17.4");
        var test = Case([new[] { 0, 1, 3 }], 2);
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = 2, mutationOk = true, probes = 5 })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = 2, mutationOk = true, probes = 45 })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = true, mutationOk = true, probes = 5 })));
        Assert.Contains(definition.Callable("python").References, reference => reference.Names.Contains("BitArray"));
    }
    [Fact]
    public void BiNodeConversionRequiresOriginalIdentityAndBothLinkDirections()
    {
        var definition = Definition("17.12");
        var expected = new { head = 1, order = new[] { 1, 0, 2 }, values = new[] { 1, 2, 3 }, previous = new[] { -1, 1, 0 }, next = new[] { 0, 2, -1 }, cycle = false };
        var test = Case([new { nodes = new int[][] { [2, 1, 2], [1, -1, -1], [3, -1, -1] }, selected = 0 }], expected);
        Assert.Null(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = expected, mutationOk = true })));
        var bad = new { head = 1, order = expected.order, values = expected.values, previous = new[] { -1, -1, -1 }, next = expected.next, cycle = false };
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = bad, mutationOk = true })));
        Assert.NotNull(CtciStagingGrader.FailureReason(definition, test, Json(new { actual = expected, mutationOk = false })));
        Assert.Contains(definition.Callable("python").References, reference => reference.Names.Contains("BiNode"));
    }
}
