using System.Reflection;
using EpiJudge.Runner;

namespace EpiJudge.Tests;

public sealed class PythonHarnessTests
{
    [Theory]
    [InlineData("anagrams")]
    [InlineData("bst_from_preorder")]
    [InlineData("bst_from_sorted_array")]
    public async Task OriginalPythonContractsAcceptActualAlgorithmsAndRejectWrongAlgorithms(string problemId)
    {
        var sourceRoot = ProblemCatalog.FindRepositoryRoot(AppContext.BaseDirectory);
        using var repository = new IsolatedPythonRepository(sourceRoot);
        var (header, row, correct, incorrect) = Scenario(problemId);
        File.WriteAllText(Path.Combine(repository.Root, "test_data", problemId + ".tsv"), header + "\n" + row + "\n");
        var problem = new ProblemCatalog().Find(problemId)!;
        var runner = new SubmissionRunner(repository.Root);

        var accepted = await runner.RunAsync(problem, correct, false, "python", CancellationToken.None);
        Assert.NotNull(accepted);
        Assert.True(accepted.Status == "Accepted", accepted.Diagnostics ?? accepted.Status);
        Assert.Equal(1, accepted.Passed);
        Assert.Equal(1, accepted.Total);

        var rejected = await runner.RunAsync(problem, incorrect, false, "python", CancellationToken.None);
        Assert.NotNull(rejected);
        Assert.True(rejected.Status == "Wrong answer", rejected.Diagnostics ?? rejected.Status);
        Assert.Equal(0, rejected.Passed);
        Assert.Equal(1, rejected.Total);
    }

    [Fact]
    public void OnlyOriginalStatisticalCorporaReceiveTheLongerPythonProcessBudget()
    {
        var statistical = new HashSet<string>
        {
            "random_permutation", "random_subset", "online_sampling", "offline_sampling",
            "nonuniform_random_number", "uniform_random_number"
        };
        var method = typeof(SubmissionRunner).GetMethod("PythonExecutionBudget", BindingFlags.NonPublic | BindingFlags.Static)!;
        foreach (var problem in new ProblemCatalog().Problems)
        {
            var budget = (TimeSpan)method.Invoke(null, [problem.Id])!;
            Assert.Equal(TimeSpan.FromSeconds(statistical.Contains(problem.Id) ? 180 : 30), budget);
        }
    }

    private static (string Header, string Row, string Correct, string Incorrect) Scenario(string problemId) => problemId switch
    {
        "anagrams" => (
            "array(string)\tarray(array(string))",
            "[\"act\",\"cat\",\"gum\",\"mug\",\"sun\"]\t[[\"act\",\"cat\"],[\"gum\",\"mug\"]]\tunordered comparator regression",
            """
            def find_anagrams(dictionary):
                groups = {}
                for word in dictionary:
                    groups.setdefault(''.join(sorted(word)), []).append(word)
                return [list(reversed(group)) for group in reversed(list(groups.values())) if len(group) > 1]
            """,
            """
            def find_anagrams(dictionary):
                return []
            """),
        "bst_from_preorder" => (
            "array(int)\tbinary_tree(int)",
            "[]\t[null]\tempty tree normalization regression",
            """
            from bst_node import BstNode
            def rebuild_bst_from_preorder(values):
                if not values:
                    return None
                root = BstNode(values[0])
                ancestors = [root]
                for value in values[1:]:
                    node = BstNode(value)
                    if value < ancestors[-1].data:
                        ancestors[-1].left = node
                    else:
                        parent = None
                        while ancestors and value >= ancestors[-1].data:
                            parent = ancestors.pop()
                        parent.right = node
                    ancestors.append(node)
                return root
            """,
            """
            from bst_node import BstNode
            def rebuild_bst_from_preorder(values):
                return BstNode(1)
            """),
        "bst_from_sorted_array" => (
            "array(int)\tint",
            "[1,2]\t2\tvalid alternative minimum-height tree regression",
            """
            from bst_node import BstNode
            def build_min_height_bst_from_sorted_array(values):
                def build(start, end):
                    if start >= end:
                        return None
                    middle = start + (end - start - 1) // 2
                    return BstNode(values[middle], build(start, middle), build(middle + 1, end))
                return build(0, len(values))
            """,
            """
            from bst_node import BstNode
            def build_min_height_bst_from_sorted_array(values):
                return BstNode(values[0]) if values else None
            """),
        _ => throw new ArgumentOutOfRangeException(nameof(problemId))
    };

    private sealed class IsolatedPythonRepository : IDisposable
    {
        public string Root { get; } = Path.Combine(Path.GetTempPath(), "epijudge-python-contracts-" + Guid.NewGuid().ToString("N"));

        public IsolatedPythonRepository(string sourceRoot)
        {
            Directory.CreateDirectory(Path.Combine(Root, "test_data"));
            var source = Path.Combine(sourceRoot, "epi_judge_python");
            var destination = Path.Combine(Root, "epi_judge_python");
            Directory.CreateDirectory(destination);
            foreach (var path in Directory.GetFiles(source, "*.py"))
                File.Copy(path, Path.Combine(destination, Path.GetFileName(path)));
            foreach (var path in Directory.GetFiles(Path.Combine(source, "test_framework"), "*.py", SearchOption.AllDirectories))
            {
                var target = Path.Combine(destination, Path.GetRelativePath(source, path));
                Directory.CreateDirectory(Path.GetDirectoryName(target)!);
                File.Copy(path, target);
            }
        }

        public void Dispose()
        {
            if (Directory.Exists(Root)) Directory.Delete(Root, recursive: true);
        }
    }
}
