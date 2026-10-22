using EpiJudge.Runner;

namespace EpiJudge.Tests;

public sealed class CallableContractCatalogTests
{
    [Fact]
    public void EveryVisibleCallableHasGuidanceBeforeOpeningTheSolution()
    {
        foreach (var entry in CallableCodeCatalog.All)
        {
            var contract = CallableContractCatalog.Find(entry.ProblemId, entry.Language);
            Assert.NotEmpty(contract);
            Assert.All(contract, line => Assert.False(string.IsNullOrWhiteSpace(line)));
        }
    }

    [Theory]
    [InlineData("python")]
    [InlineData("cpp")]
    [InlineData("java")]
    public void DuplicateCompactionDistinguishesReturnFromObservedPrefix(string language)
    {
        var lines = CallableContractCatalog.Find("sorted_array_remove_dups", language);
        Assert.Contains(lines, line => line.Contains("return integer k"));
        Assert.Contains(lines, line => line.Contains("not") && line.Contains("return value"));
    }

    [Theory]
    [InlineData("csharp")]
    [InlineData("javascript")]
    public void SequenceReturningVariantsDoNotRequestAnInteger(string language)
    {
        var lines = CallableContractCatalog.Find("sorted_array_remove_dups", language);
        Assert.Contains(lines, line => line.Contains("Return the"));
        Assert.DoesNotContain(lines, line => line.Contains("return integer k"));
    }

    [Fact]
    public void SameWeightContractsRetainNativeWidths()
    {
        Assert.Contains(CallableContractCatalog.Find("closest_int_same_weight", "csharp"), line => line.Contains("63"));
        Assert.Contains(CallableContractCatalog.Find("closest_int_same_weight", "cpp"), line => line.Contains("64"));
        Assert.Contains(CallableContractCatalog.Find("closest_int_same_weight", "python"), line => line.Contains("64"));
    }
}
