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
    public void JavaStateClassUsesItsOwnMatchingFilename(string reference)
    {
        var definition = Definition(reference);
        Assert.Equal(definition.Method + ".java", definition.Callable("java").Filename);
        Assert.Equal(definition.Callable("java").Filename, CallableCodeCatalog.Find(definition.Id, "java")!.Filename);
        if (reference == "3.1") Assert.Contains("capacity: int", definition.Languages["python"].Signature);
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
}
