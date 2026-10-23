using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<string> LargestWordRectangle(string[] words)
    {
        var seen = new HashSet<string>(StringComparer.Ordinal);
        var groups = new List<string>[6];
        for (int i = 0; i < groups.Length; ++i)
            groups[i] = new List<string>();
        int maximum = 0;
        foreach (string word in words)
            if (seen.Add(word))
            {
                groups[word.Length].Add(word);
                maximum = Math.Max(maximum, word.Length);
            }
        for (int area = maximum * maximum; area > 0; --area)
            for (int height = 1; height <= maximum; ++height)
            {
                if (area % height != 0)
                    continue;
                int width = area / height;
                if (width > maximum || groups[width].Count == 0 || groups[height].Count == 0)
                    continue;
                var prefixes = new HashSet<string>(StringComparer.Ordinal);
                foreach (string word in groups[height])
                    for (int length = 1; length <= height; ++length)
                        prefixes.Add(word.Substring(0, length));
                var rows = new List<string>();
                bool Search()
                {
                    if (rows.Count == height)
                        return true;
                    foreach (string word in groups[width])
                    {
                        rows.Add(word);
                        bool valid = true;
                        for (int column = 0; column < width; ++column)
                        {
                            var prefix = new StringBuilder();
                            foreach (string row in rows)
                                prefix.Append(row[column]);
                            if (!prefixes.Contains(prefix.ToString()))
                            {
                                valid = false;
                                break;
                            }
                        }
                        if (valid && Search())
                            return true;
                        rows.RemoveAt(rows.Count - 1);
                    }
                    return false;
                }
                if (Search())
                    return rows;
            }
        return [];
    }
}
