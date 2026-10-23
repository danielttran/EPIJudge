using EpiJudge.Runner;

namespace EpiJudge.Tests;

public sealed class CallableCodeCatalogTests
{
    [Fact]
    public void EveryRunnableQuestionHasBothVisibleArtifactsInEveryLanguage()
    {
        var problems = new ProblemCatalog().Problems;
        Assert.Equal(334 + CtciCatalog.Problems.Count, problems.Count);
        Assert.Equal((334 + CtciCatalog.Problems.Count)*5, CallableCodeCatalog.All.Count);
        foreach (var problem in problems)
            foreach (var language in SolutionCatalog.Languages)
            {
                var entry = Assert.IsType<CallableCodeDefinition>(CallableCodeCatalog.Find(problem.Id, language));
                Assert.InRange(entry.StarterCode.Length, 1, 40_000);
                Assert.InRange(entry.SolutionCode.Length, 1, 40_000);
                Assert.NotNull(entry.References);
            }
        Assert.Empty(CallableCodeCatalog.Find("interviewcake_stock-price", "csharp")!.References);
    }

    [Fact]
    public void LegacySourceIsPreservedWithoutInspectingItsDeclarations()
    {
        const string source = "class GraphNode { }\r\n// user-owned source\n";
        Assert.Equal(source, CallableCodeCatalog.Prepare("unknown", "csharp", source, null).Code);
        Assert.Equal(source, CallableCodeCatalog.Prepare("unknown", "csharp", source, "legacy-v1").Code);
        Assert.Throws<ArgumentException>(() => CallableCodeCatalog.Prepare("unknown", "csharp", source, "future"));
    }

    [Theory]
    [InlineData("java", "Solution.java", "Solution.java:12: error: visible\nat Solution.run(Solution.java:13)", "Solution.java:2: error: visible\nat Solution.run(Solution.java:3)")]
    [InlineData("javascript", "solution.js", "at run (solution.js:12:7)", "at run (solution.js:2:7)")]
    [InlineData("python", "solution.py", "File \"/submission/solution.py\", line 12, in run", "File \"/submission/solution.py\", line 2, in run")]
    public void DiagnosticsUseEditorLineNumbers(string language, string filename, string diagnostic, string expected)
    {
        _ = language;
        var prepared = new PreparedCode("", 10, 5, filename, "callable-v1");
        var result = new SubmissionResult("id", "Compilation error", 0, 1, 0, diagnostic,
            [new CaseResult(1, false, null, null, null, diagnostic, 0, false)]);
        var mapped = CallableCodeCatalog.MapResult(result, prepared);
        Assert.Equal(expected, mapped.Diagnostics);
        Assert.Equal(expected, mapped.Cases[0].Error);
    }

    [Fact]
    public void HiddenSupportDiagnosticIsNotMisreportedAsAUserLine()
    {
        var prepared = new PreparedCode("", 10, 5, "Solution.java", "callable-v1");
        var result = new SubmissionResult("id", "Runtime error", 0, 1, 0, "Solution.java:4", []);
        Assert.Equal("Solution.java:4", CallableCodeCatalog.MapResult(result, prepared).Diagnostics);
    }

    [Fact]
    public void ArbitraryExceptionTextCannotOverflowDiagnosticLineMapping()
    {
        const string diagnostic = "at run (solution.js:999999999999999999999999:7)";
        var prepared = new PreparedCode("", 10, 5, "solution.js", "callable-v1");
        var result = new SubmissionResult("id", "Runtime error", 0, 1, 0, diagnostic, []);
        var mapped = CallableCodeCatalog.MapResult(result, prepared);
        Assert.Equal("Runtime error", mapped.Status);
        Assert.Equal(diagnostic, mapped.Diagnostics);
    }

    [Fact]
    public void PythonSourceCompilesSeparatelyWithoutLosingUnicodeOrFutureImports()
    {
        const string code = "from __future__ import annotations\n# λ 😀\nclass Solution:\n    def Fib(self, n):\n        return n\n";
        var prepared = CallableCodeCatalog.Prepare("interviewcake_nth-fibonacci", "python", code, "callable-v1");
        var encoded = Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes(code));
        Assert.Contains("b64decode('" + encoded + "')", prepared.Code);
        Assert.Contains("'solution.py', 'exec'", prepared.Code);
        Assert.Equal(0, prepared.PrefixLines);
    }

    [Fact]
    public void JavaImportsMoveBeforeTheBankClassWhileEditorLinesRemainStable()
    {
        const string code = "// import fake.NotAType;\nimport java.math.BigInteger;\nimport /* ; */ static java.lang.Math.*;\npublic static short countBits(int x) { return 0; }\n";
        var prepared = CallableCodeCatalog.Prepare("count_bits", "java", code, "callable-v1");
        var outer = prepared.Code.IndexOf("public class CountBits", StringComparison.Ordinal);
        Assert.True(prepared.Code.IndexOf("import java.math.BigInteger;", StringComparison.Ordinal) < outer);
        Assert.True(prepared.Code.IndexOf("import /* ; */ static java.lang.Math.*;", StringComparison.Ordinal) < outer);
        Assert.Contains("// import fake.NotAType;", prepared.Code);
        var result = new SubmissionResult("id", "Compilation error", 0, 1, 0,
            "CountBits.java:" + (prepared.PrefixLines + 4), []);
        Assert.Equal("CountBits.java:4", CallableCodeCatalog.MapResult(result, prepared).Diagnostics);
    }

    [Fact]
    public void JavaScriptSubmissionBindingsAreScopedApartFromHiddenSupport()
    {
        const string code = "const fs = require('node:fs');\nclass Solution {}\n";
        var prepared = CallableCodeCatalog.Prepare("interviewcake_stock-price", "javascript", code, "callable-v1");
        var entry = CallableCodeCatalog.Find("interviewcake_stock-price", "javascript")!;
        Assert.Contains("(() => {\n" + code + "\n" + entry.Suffix + "\n})();\n", prepared.Code);
        Assert.Equal(entry.Prefix.Count(character => character == '\n') + 1, prepared.PrefixLines);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(3)]
    public void JavaImportDiagnosticsRetainTheirOriginalEditorLine(int commentLines)
    {
        var code = string.Concat(Enumerable.Repeat("// user comment\n", commentLines)) +
            "import missing.bank.Type;\npublic static short countBits(int x) { return 0; }\n";
        var prepared = CallableCodeCatalog.Prepare("count_bits", "java", code, "callable-v1");
        var result = new SubmissionResult("id", "Compilation error", 0, 1, 0,
            "CountBits.java:2: error: package missing.bank does not exist", []);
        Assert.Equal("CountBits.java:" + (commentLines + 1) + ": error: package missing.bank does not exist",
            CallableCodeCatalog.MapResult(result, prepared).Diagnostics);
    }

    [Fact]
    public void JavaMultilineImportsRetainEachOriginalEditorLine()
    {
        const string code = "// comment\n\nimport /* ;\n comment */ missing.bank.Type;\npublic static short countBits(int x) { return 0; }\n";
        var prepared = CallableCodeCatalog.Prepare("count_bits", "java", code, "callable-v1");
        var result = new SubmissionResult("id", "Compilation error", 0, 1, 0, "CountBits.java:3: error", []);
        Assert.Equal("CountBits.java:4: error", CallableCodeCatalog.MapResult(result, prepared).Diagnostics);
    }
}
