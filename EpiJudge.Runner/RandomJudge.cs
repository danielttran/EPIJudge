using System.Text.Json;

namespace EpiJudge.Runner;

internal static class RandomJudge
{
    private const int Samples = 100_000;
    public static bool Validate(string id, JsonElement[] args, dynamic solution)
    {
        // Independent batches tolerate rare statistical false negatives.
        for (int attempt = 0; attempt < 3; attempt++)
            if (Batch(id, args, solution)) return true;
        throw new JudgeValidationException("The generated samples failed distribution or independence checks.");
    }

    private static bool Batch(string id, JsonElement[] a, dynamic s)
    {
        var values = id is "offline_sampling" ? JudgeAdapters.Arg<List<int>>(a, 1)
            : id is "online_sampling" or "nonuniform_random_number" ? JudgeAdapters.Arg<List<int>>(a, 0) : [];
        var probabilities = id == "nonuniform_random_number" ? JudgeAdapters.Arg<List<double>>(a, 1) : [];
        int n = id is "random_permutation" or "random_subset" ? JudgeAdapters.Arg<int>(a, 0) : values.Count;
        int k = id == "offline_sampling" ? JudgeAdapters.Arg<int>(a, 0)
            : id is "online_sampling" or "random_subset" ? JudgeAdapters.Arg<int>(a, 1) : n;
        int lower = id == "uniform_random_number" ? JudgeAdapters.Arg<int>(a, 0) : 0;
        int upper = id == "uniform_random_number" ? JudgeAdapters.Arg<int>(a, 1) : 0;
        double outcomes = id switch
        {
            "uniform_random_number" => (long)upper-lower+1,
            "random_permutation" => Factorial(n),
            "nonuniform_random_number" => values.Count,
            _ => Choose(n, k)
        };
        var labels = new Dictionary<string,int>();
        var sequence = new int[Samples];
        for (int i = 0; i < Samples; i++)
        {
            string label;
            if (id == "uniform_random_number")
            {
                int x = s.UniformRandom(lower, upper);
                Require(x >= lower && x <= upper); label = x.ToString();
            }
            else if (id == "nonuniform_random_number")
            {
                int x = s.NonuniformRandomNumberGeneration(values, probabilities);
                int index = values.IndexOf(x); Require(index >= 0 && probabilities[index] > 0); label = index.ToString();
            }
            else
            {
                List<int> sample;
                if (id == "random_permutation") sample = s.ComputeRandomPermutation(n);
                else if (id == "random_subset") sample = s.RandomSubset(n, k);
                else if (id == "online_sampling") sample = s.OnlineRandomSample(new List<int>(values), k);
                else
                {
                    var copy = new List<int>(values); s.RandomSampling(k, copy);
                    Require(copy.Count == values.Count && copy.Order().SequenceEqual(values.Order())); sample = copy.Take(k).ToList();
                }
                Require(sample.Count == (id == "random_permutation" ? n : k) && sample.Distinct().Count() == sample.Count);
                Require(id is "random_subset" or "random_permutation" ? sample.All(x => x >= 0 && x < n) : sample.All(values.Contains));
                IEnumerable<int> orderedSample = id == "random_permutation" ? sample : sample.Order();
                label = string.Join(",", orderedSample);
            }
            if (!labels.TryGetValue(label, out int code)) { code = labels.Count; labels[label] = code; }
            sequence[i] = code;
        }
        if (id == "nonuniform_random_number")
        {
            var counts = sequence.GroupBy(x => x).ToDictionary(g => g.Key, g => g.Count());
            for (int j = 0; j < probabilities.Count; j++)
            {
                double p = probabilities[j], expected = Samples*p;
                int observed = labels.TryGetValue(j.ToString(), out int code) ? counts.GetValueOrDefault(code) : 0;
                if (Math.Abs(observed-expected) > Math.Max(25, 6*Math.Sqrt(expected*(1-p)))) return false;
            }
            return true;
        }
        if (!Frequency(sequence, outcomes)) return false;
        if (!Frequency(sequence.Zip(sequence.Skip(1), (x,y) => (x,y)), outcomes*outcomes)) return false;
        if (!Frequency(Enumerable.Range(0, sequence.Length-2).Select(i => (sequence[i],sequence[i+1],sequence[i+2])), outcomes*outcomes*outcomes)) return false;
        return true;
    }
    private static bool Frequency<T>(IEnumerable<T> sequence, double outcomes) where T : notnull
    {
        var counts = new Dictionary<T,int>(); int total = 0;
        foreach (var x in sequence) { counts[x] = counts.GetValueOrDefault(x)+1; total++; }
        double expected = total/outcomes;
        double tolerance = Math.Max(25, 7*Math.Sqrt(expected*(1-1/outcomes)));
        if (expected >= 50 && counts.Count < outcomes) return false;
        return counts.Values.All(x => Math.Abs(x-expected) <= tolerance);
    }
    private static double Factorial(int n) { double value = 1; for (int i = 2; i <= n; i++) value *= i; return value; }
    private static double Choose(int n, int k) { double value = 1; for (int i = 1; i <= k; i++) value = value*(n-i+1)/i; return value; }
    private static void Require(bool condition)
    {
        if (!condition) throw new JudgeValidationException("A generated sample has the wrong size, values, or duplicates.");
    }
}
