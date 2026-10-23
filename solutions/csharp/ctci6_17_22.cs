using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<string> WordTransformation(string start, string stop, string[] dictionary)
    {
        var words = new HashSet<string>(dictionary, StringComparer.Ordinal);
        var previous = new Dictionary<string, string?>(StringComparer.Ordinal) { { start, null } };
        var queue = new List<string> { start };
        for (int head = 0; head < queue.Count; ++head)
        {
            string word = queue[head];
            if (word == stop)
            {
                var path = new List<string>();
                for (string? current = stop; current != null; current = previous[current])
                    path.Add(current);
                path.Reverse();
                return path;
            }
            char[] letters = word.ToCharArray();
            for (int position = 0; position < letters.Length; ++position)
            {
                char original = letters[position];
                for (char letter = 'a'; letter <= 'z'; ++letter)
                {
                    if (letter == original)
                        continue;
                    letters[position] = letter;
                    string candidate = new string(letters);
                    if (words.Contains(candidate) && !previous.ContainsKey(candidate))
                    {
                        previous[candidate] = word;
                        queue.Add(candidate);
                    }
                }
                letters[position] = original;
            }
        }
        return [];
    }
}
