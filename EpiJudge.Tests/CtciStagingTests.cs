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
    public void UnpublishedEntriesDoNotChangeTheLiveLibrary()
    {
        Assert.DoesNotContain(new ProblemCatalog().Problems, problem => problem.Collection == "ctci6");
        var staged = CtciStagingCatalog.Load(Root);
        Assert.Equal(26, staged.Count);
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
        var definition = Definition("2.2").Callable(language);
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
