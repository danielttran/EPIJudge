# C# Judge

The C# judge uses the same TSV test cases as the other EPIJudge languages. It
contains a starter stub for each of the 218 problems in `test_data`.

## Requirements

- .NET 8 SDK
- Visual Studio 2026 with the .NET development workload, if you want to use the IDE

## Open in Visual Studio

1. Open `EPIJudge.slnx` from the repository root.
2. Set the **EpiJudge** project as the startup project.
3. Set the project's command-line arguments to a problem ID, such as `two_sum`.
4. Start debugging. The judge reads that problem's tests from `test_data`.

You can also run a problem from a terminal at the repository root:

```powershell
dotnet run --project epi_judge_csharp/EpiJudge.csproj -- two_sum
```

The problem ID is the TSV filename without `.tsv`. See
[`problem_catalog.json`](problem_catalog.json) for all IDs. For example,
`two_sum` uses `Problems/TwoSum.cs` and `test_data/two_sum.tsv`.

## Implement a problem

Open the matching file under `Problems/` and replace the TODO body in `Solve`.
The file already connects `Solve` to the correct test data. A starter stub is
expected to fail until its implementation is complete.

Run just that problem after making changes:

```powershell
dotnet run --project epi_judge_csharp/EpiJudge.csproj -- two_sum
```

The runner prints a status for each case it reaches. By default, it stops at
the first failed case and exits successfully only when all cases pass. To use a
different test-data directory, pass it after the problem ID:

```powershell
dotnet run --project epi_judge_csharp/EpiJudge.csproj -- two_sum --test-data-dir C:\path\to\test_data
```

For a full compile without running a problem, build the solution:

```powershell
dotnet build EPIJudge.slnx
```

## C# test-data types

The test framework reads primitive values, lists, sets, tuples, binary trees,
and linked lists from the TSV JSON fields. Tree and list nodes are available in
the `EpiJudge.TestFramework` namespace as `BinaryTreeNode<T>` and `ListNode<T>`.
The runner also uses unordered comparison for problems whose tests accept
results in any order.

Some TSV problems have a `void` result because their test method is a wrapper.
For those, implement the wrapper behavior in `Solve` and throw an exception
when an expected result or mutation is incorrect; an exception marks that test
case as failed.

## Reference solutions

The separate `epi_judge_csharp_solutions` project currently contains reference
solutions for `count_bits` and `anagrams`. Run one with:

```powershell
dotnet run --project epi_judge_csharp_solutions/EpiJudge.Solutions.csproj -- count_bits
```

The files under `Problems/` are exercise stubs and are separate from those
reference solutions.
