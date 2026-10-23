using EpiJudge.Runner;

namespace EpiJudge.Tests;

public class CodeFormatterTests
{
    private readonly CodeFormatter formatter = new(Directory.GetCurrentDirectory());

    [Theory]
    [InlineData("class X{int F(){return 1;}}")]
    [InlineData("class X{int F(){var required=1;return required;}}")]
    [InlineData("class X{string F(){return \"a  b\";}}")]
    public async Task RoslynFormatsValidCSharpWithoutChangingTokens(string code)
    {
        var result = await formatter.FormatAsync("csharp", code, "callable-v1", default);
        Assert.Null(result.Error);
        Assert.Contains("\n", result.Code);
        var twice = await formatter.FormatAsync("csharp", result.Code!, "callable-v1", default);
        Assert.Equal(result.Code, twice.Code);
    }
    [Theory]
    [InlineData("class X { int F( }")]
    [InlineData("class X { string x = \"unterminated;")]
    public async Task IncompleteSyntaxDoesNotReturnReplacement(string code)
    {
        var result = await formatter.FormatAsync("csharp", code, "callable-v1", default);
        Assert.Equal("invalid", result.Error);
        Assert.Null(result.Code);
    }
    [Theory]
    [InlineData("ruby", "x", "callable-v1")]
    [InlineData("java", "", "callable-v1")]
    [InlineData("python", "x=1", "other")]
    public async Task InvalidRequestsNeverStartTools(string language, string code, string format)
    {
        Assert.Equal("invalid", (await formatter.FormatAsync(language, code, format, default)).Error);
    }
    [Fact]
    public async Task MissingLocalToolOrDirectoryReturnsAnAvailabilityErrorWithoutCode()
    {
        var missing = new CodeFormatter(Path.Combine(Path.GetTempPath(), Guid.NewGuid().ToString("N")));
        var result = await missing.FormatAsync("python", "x=1", "callable-v1", default);
        Assert.Equal("unavailable", result.Error);
        Assert.Null(result.Code);
        Assert.Contains("Code was not changed", result.Message);
    }
    [Fact]
    public async Task OversizedCodeIsRejectedBeforeParsing()
    {
        var result = await formatter.FormatAsync("csharp", new string('x', 40_001), "callable-v1", default);
        Assert.Equal("invalid", result.Error);
        Assert.Null(result.Code);
    }
    [Fact]
    public async Task CancellationDoesNotReturnAReplacement()
    {
        await Assert.ThrowsAnyAsync<OperationCanceledException>(() => formatter.FormatAsync("csharp", "class X{}", "callable-v1", new CancellationToken(true)));
    }

}
