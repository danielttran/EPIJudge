using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int TransformString(HashSet<string> D, string s, string t)
    {
        if (s == t)
            return 0;
        var remaining = new HashSet<string>(D);
        remaining.Remove(s);
        var queue = new Queue<(string Word, int Distance)>();
        queue.Enqueue((s, 0));
        while (queue.TryDequeue(out var entry))
        {
            var chars = entry.Word.ToCharArray();
            for (int i = 0; i < chars.Length; i++)
            {
                char old = chars[i];
                for (char c = 'a'; c <= 'z'; c++)
                {
                    if (c == old)
                        continue;
                    chars[i] = c;
                    var candidate = new string(chars);
                    if (!remaining.Remove(candidate))
                        continue;
                    if (candidate == t)
                        return entry.Distance + 1;
                    queue.Enqueue((candidate, entry.Distance + 1));
                }
                chars[i] = old;
            }
        }
        return -1;
    }
}
