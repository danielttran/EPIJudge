using System.Collections;
using System.Diagnostics;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace EpiJudge.TestFramework;

public static class GenericTest
{
    private static readonly JsonSerializerOptions JsonOptions = CreateJsonOptions();

    public static int Run<TArgument, TResult>(
        string[] args,
        string testDataFile,
        string argumentName,
        Func<TArgument, TResult> function,
        Func<TResult, TResult, bool>? comparator = null) =>
        Run(args, testDataFile, new[] { argumentName }, new[] { typeof(TArgument) }, typeof(TResult),
            values => function((TArgument)values[0]!),
            comparator is null ? null : (expected, actual) =>
                comparator((TResult)expected!, (TResult)actual!));

    public static int Run(
        string[] args,
        string testDataFile,
        string[] argumentNames,
        Type[] argumentTypes,
        Type resultType,
        Func<object?[], object?> function,
        Func<object?, object?, bool>? comparator = null) =>
        RunCore(args, testDataFile, argumentNames, argumentTypes, resultType, function, comparator, false);

    public static int RunVoid(
        string[] args,
        string testDataFile,
        string[] argumentNames,
        Type[] argumentTypes,
        Action<object?[]> function) =>
        RunCore(args, testDataFile, argumentNames, argumentTypes, typeof(void), values =>
        {
            function(values);
            return null;
        }, null, true);

    private static int RunCore(
        string[] args,
        string testDataFile,
        string[] argumentNames,
        Type[] argumentTypes,
        Type resultType,
        Func<object?[], object?> function,
        Func<object?, object?, bool>? comparator,
        bool returnsVoid)
    {
        try
        {
            return (int)RunCoreUnsafe(args, testDataFile, argumentNames, argumentTypes,
                resultType, function, comparator, returnsVoid);
        }
        catch (Exception exception)
        {
            Console.Error.WriteLine($"Critical error ({exception.GetType().Name}): {exception.Message}");
            return (int)TestResult.RuntimeError;
        }
    }

    private static TestResult RunCoreUnsafe(
        string[] args,
        string testDataFile,
        string[] argumentNames,
        Type[] argumentTypes,
        Type resultType,
        Func<object?[], object?> function,
        Func<object?, object?, bool>? comparator,
        bool returnsVoid)
    {
        if (argumentNames.Length != argumentTypes.Length)
        {
            throw new ArgumentException("The argument name and type counts must match.");
        }

        var options = JudgeOptions.Parse(args);
        var path = Path.Combine(options.TestDataDirectory, testDataFile);
        using var reader = new StreamReader(path);
        var signature = (reader.ReadLine() ?? throw new InvalidDataException("Missing TSV signature."))
            .Split('\t');
        if (signature.Length != argumentTypes.Length + 1)
        {
            throw new InvalidDataException(
                $"Expected {argumentTypes.Length} arguments and one result, got {signature.Length} fields.");
        }

        for (var index = 0; index < argumentTypes.Length; ++index)
        {
            TypeGrammar.AssertCompatible(signature[index], argumentTypes[index]);
        }
        TypeGrammar.AssertCompatible(signature[^1], returnsVoid ? typeof(void) : resultType);

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
            var requiredFieldCount = argumentTypes.Length + 1;
            if (fields.Length < requiredFieldCount || fields.Length > requiredFieldCount + 1)
            {
                throw new InvalidDataException($"Invalid field count on test row {testNumber}.");
            }

            var arguments = new object?[argumentTypes.Length];
            for (var index = 0; index < argumentTypes.Length; ++index)
            {
                arguments[index] = Deserialize(fields[index], argumentTypes[index]);
            }

            var expected = returnsVoid ? null : Deserialize(fields[argumentTypes.Length], resultType);
            var stopwatch = Stopwatch.StartNew();
            object? actual = null;
            Exception? invocationError = null;
            var task = Task.Run(() =>
            {
                try { actual = function(arguments); }
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
            else if (!returnsVoid && !(comparator?.Invoke(expected, actual) ?? DeepEquals(expected, actual, resultType)))
            {
                PrintStatus("FAILED", testNumber, total, stopwatch.Elapsed);
                Console.WriteLine("Arguments");
                for (var index = 0; index < argumentNames.Length; ++index)
                {
                    Console.WriteLine($"\t{argumentNames[index]}:\t{Format(arguments[index], argumentTypes[index])}");
                }
                if (fields.Length == requiredFieldCount + 1 && fields[^1] is not ("" or "TODO"))
                    Console.WriteLine($"Explanation: {fields[^1]}");
                Console.WriteLine($"Expected:\t{Format(expected, resultType)}");
                Console.WriteLine($"Result:\t\t{Format(actual, resultType)}");
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

    private static object? Deserialize(string json, Type type) =>
        JsonSerializer.Deserialize(json, type, JsonOptions);

    public static bool UnorderedEquals(object? expected, object? actual, Type type) =>
        EqualsCore(expected, actual, type, unorderedSequences: true);

    private static bool DeepEquals(object? expected, object? actual, Type type) =>
        EqualsCore(expected, actual, type, unorderedSequences: false);

    private static bool EqualsCore(object? expected, object? actual, Type type, bool unorderedSequences)
    {
        if (ReferenceEquals(expected, actual)) return true;
        if (expected is null || actual is null) return false;
        if (type == typeof(double) || type == typeof(float))
        {
            var left = Convert.ToDouble(expected);
            var right = Convert.ToDouble(actual);
            return Math.Abs(left - right) <= 1e-9 * Math.Max(Math.Abs(left), Math.Abs(right));
        }

        if (IsValueTuple(type))
        {
            var fields = type.GetGenericArguments();
            for (var index = 0; index < fields.Length; ++index)
            {
                var name = $"Item{index + 1}";
                if (!EqualsCore(type.GetField(name)!.GetValue(expected),
                    type.GetField(name)!.GetValue(actual), fields[index], unorderedSequences)) return false;
            }
            return true;
        }

        var isSet = IsSet(type);
        TryGetSequenceElementType(type, out var elementType);
        if (isSet || elementType is not null)
        {
            elementType ??= type.GetGenericArguments()[0];
            return SequenceEquals((IEnumerable)expected, (IEnumerable)actual, elementType,
                unorderedSequences || isSet);
        }

        return JsonSerializer.Serialize(expected, type, JsonOptions) ==
            JsonSerializer.Serialize(actual, type, JsonOptions);
    }

    private static bool IsSet(Type type) =>
        type.GetInterfaces().Append(type).Any(candidate =>
            candidate.IsGenericType && candidate.GetGenericTypeDefinition() == typeof(ISet<>));

    private static bool SequenceEquals(IEnumerable expected, IEnumerable actual, Type elementType, bool unordered)
    {
        var expectedItems = expected.Cast<object?>().ToList();
        var actualItems = actual.Cast<object?>().ToList();
        if (expectedItems.Count != actualItems.Count) return false;

        if (!unordered)
        {
            return expectedItems.Select((item, index) =>
                EqualsCore(item, actualItems[index], elementType, unorderedSequences: false)).All(equal => equal);
        }

        foreach (var expectedItem in expectedItems)
        {
            var match = actualItems.FindIndex(actualItem =>
                EqualsCore(expectedItem, actualItem, elementType, unorderedSequences: unordered));
            if (match < 0) return false;
            actualItems.RemoveAt(match);
        }
        return true;
    }

    private static bool IsValueTuple(Type type) =>
        type.IsGenericType && type.GetGenericTypeDefinition().FullName?.StartsWith("System.ValueTuple`", StringComparison.Ordinal) == true;

    private static bool TryGetSequenceElementType(Type type, out Type? elementType)
    {
        if (type == typeof(string))
        {
            elementType = null;
            return false;
        }

        elementType = type.IsArray ? type.GetElementType() : type.GetInterfaces().Append(type)
            .FirstOrDefault(candidate => candidate.IsGenericType &&
                candidate.GetGenericTypeDefinition() == typeof(IEnumerable<>))?.GetGenericArguments()[0];
        return elementType is not null;
    }

    private static string Format(object? value, Type type) =>
        JsonSerializer.Serialize(value, type, JsonOptions);

    private static void PrintStatus(string status, int current, int total, TimeSpan elapsed) =>
        Console.WriteLine($"Test {status} ({current,4}/{total}) [{elapsed.TotalMilliseconds:F2} ms]");

    private static JsonSerializerOptions CreateJsonOptions()
    {
        var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
        options.Converters.Add(new ValueTupleConverterFactory());
        options.Converters.Add(new BinaryTreeNodeConverterFactory());
        options.Converters.Add(new ListNodeConverterFactory());
        return options;
    }
}
