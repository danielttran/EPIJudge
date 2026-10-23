using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int WordDistance(string[] words, string first, string second)
    {
        int lastFirst = -1, lastSecond = -1, best = words.Length + 1;
        for (int i = 0; i < words.Length; ++i)
        {
            if (words[i] == first)
            {
                lastFirst = i;
                if (lastSecond >= 0)
                    best = Math.Min(best, i - lastSecond);
            }
            else if (words[i] == second)
            {
                lastSecond = i;
                if (lastFirst >= 0)
                    best = Math.Min(best, i - lastFirst);
            }
        }
        return best == words.Length + 1 ? -1 : best;
    }
}
