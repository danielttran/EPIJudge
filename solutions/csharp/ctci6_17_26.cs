using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[][] SparseSimilarities(int[] documentIds, int[][] documents)
    {
        int n = documentIds.Length;
        var postings = new Dictionary<int, List<int>>();
        for (int i = 0; i < n; ++i)
            foreach (int word in documents[i])
            {
                if (!postings.TryGetValue(word, out var posting))
                {
                    posting = new List<int>();
                    postings[word] = posting;
                }
                posting.Add(i);
            }
        var intersections = new Dictionary<int, int>();
        foreach (var posting in postings.Values)
            for (int a = 0; a < posting.Count; ++a)
                for (int b = a + 1; b < posting.Count; ++b)
                {
                    int key = posting[a] * n + posting[b];
                    intersections.TryGetValue(key, out int count);
                    intersections[key] = count + 1;
                }
        var result = new List<int[]>();
        foreach (var entry in intersections)
        {
            int left = entry.Key / n, right = entry.Key % n, count = entry.Value,
                a = documentIds[left], b = documentIds[right];
            result.Add([
                Math.Min(a, b), Math.Max(a, b), count,
                documents[left].Length + documents[right].Length - count
            ]);
        }
        result.Sort((a, b) =>
                    {
                        int first = a[0].CompareTo(b[0]);
                        return first != 0 ? first : a[1].CompareTo(b[1]);
                    });
        return result.ToArray();
    }
}
