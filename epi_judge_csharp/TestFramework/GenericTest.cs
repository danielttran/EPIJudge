using System.Diagnostics;
using System.Text.Json;

namespace EpiJudge.TestFramework;

public static class GenericTest
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNameCaseInsensitive = true,
    };

    public static int Run<TArgument, TResult>(
        string[] args,
        string testDataFile,
        string argumentName,
        Func<TArgument, TResult> function,
        Func<TResult, TResult, bool>? comparator = null)
    {
        try
        {
            return (int)RunCore(args, testDataFile, argumentName, function, comparator);
        }
        catch (Exception exception)
        {
            Console.Error.WriteLine($"Critical error ({exception.GetType().Name}): {exception.Message}");
            return (int)TestResult.RuntimeError;
        }
    }

    private static TestResult RunCore<TArgument, TResult>(
        string[] args,
        string testDataFile,
        string argumentName,
        Func<TArgument, TResult> function,
        Func<TResult, TResult, bool>? comparator)
    {
        var options = JudgeOptions.Parse(args);
        var path = Path.Combine(options.TestDataDirectory, testDataFile);
        using var reader = new StreamReader(path);
        var signature = (reader.ReadLine() ?? throw new InvalidDataException("Missing TSV signature."))
            .Split('\t');
        if (signature.Length != 2)
        {
            throw new InvalidDataException($"Expected one argument and one result, got {signature.Length} fields.");
        }
        TypeGrammar.AssertCompatible(signature[0], typeof(TArgument));
        TypeGrammar.AssertCompatible(signature[1], typeof(TResult));

        var total = File.ReadLines(path).Skip(1).Count();
        var passed = 0;
        var failures = 0;
        var testNumber = 0;
        var elapsedMicroseconds = new List<long>();
        string? line;
        while ((line = reader.ReadLine()) is not null)
        {
            ++testNumber;
            var fields = line.Split('\t');
            if (fields.Length is < 2 or > 3)
            {
                throw new InvalidDataException($"Invalid field count on test row {testNumber}.");
            }

            var argument = Deserialize<TArgument>(fields[0]);
            var expected = Deserialize<TResult>(fields[1]);
            var stopwatch = Stopwatch.StartNew();
            TResult? actual = default;
            Exception? invocationError = null;
            var task = Task.Run(() =>
            {
                try { actual = function(argument); }
                catch (Exception exception) { invocationError = exception; }
            });
            var completed = options.TimeoutSeconds <= 0
                ? task.Wait(Timeout.InfiniteTimeSpan)
                : task.Wait(TimeSpan.FromSeconds(options.TimeoutSeconds));
            stopwatch.Stop();

            if (!completed)
            {
                PrintStatus("TIMEOUT", testNumber, total, stopwatch.Elapsed);
                return TestResult.Timeout;
            }
            if (invocationError is not null)
            {
                PrintStatus("FAILED", testNumber, total, stopwatch.Elapsed);
                Console.WriteLine($"Exception: {invocationError.GetType().Name}: {invocationError.Message}");
                ++failures;
            }
            else if (!(comparator?.Invoke(expected, actual!) ?? DeepEquals(expected, actual)))
            {
                PrintStatus("FAILED", testNumber, total, stopwatch.Elapsed);
                Console.WriteLine("Arguments");
                Console.WriteLine($"\t{argumentName}:\t{Format(argument)}");
                if (fields.Length == 3 && fields[2] is not ("" or "TODO"))
                    Console.WriteLine($"Explanation: {fields[2]}");
                Console.WriteLine($"Expected:\t{Format(expected)}");
                Console.WriteLine($"Result:\t\t{Format(actual)}");
                ++failures;
            }
            else
            {
                ++passed;
                elapsedMicroseconds.Add(stopwatch.ElapsedTicks * 1_000_000 / Stopwatch.Frequency);
                PrintStatus("PASSED", testNumber, total, stopwatch.Elapsed);
            }

            if (failures > 0 && options.FailureLimit > 0 && failures >= options.FailureLimit) break;
        }

        Console.WriteLine();
        if (failures == 0)
        {
            var average = elapsedMicroseconds.Count == 0 ? 0 : elapsedMicroseconds.Average();
            Console.WriteLine($"*** You've passed ALL tests. Congratulations! *** ({passed}/{total}, average {average:F0} us)");
            return TestResult.Passed;
        }
        return TestResult.Failed;
    }

    private static T Deserialize<T>(string json) =>
        JsonSerializer.Deserialize<T>(json, JsonOptions)
        ?? throw new InvalidDataException($"Cannot deserialize null as {typeof(T)}.");

    private static bool DeepEquals<T>(T expected, T? actual) =>
        JsonSerializer.Serialize(expected, JsonOptions) == JsonSerializer.Serialize(actual, JsonOptions);

    private static string Format<T>(T value) => JsonSerializer.Serialize(value, JsonOptions);

    private static void PrintStatus(string status, int current, int total, TimeSpan elapsed) =>
        Console.WriteLine($"Test {status} ({current,4}/{total}) [{elapsed.TotalMilliseconds:F2} ms]");
}
