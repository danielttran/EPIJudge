using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public bool IsMatch(string regex, string s)
    {
        bool anchored = regex.StartsWith('^');
        int first = anchored ? 1 : 0;
        var memo = new Dictionary<(int Pattern, int Text), bool>();
        bool Match(int p, int t)
        {
            if (memo.TryGetValue((p, t), out bool known))
                return known;
            bool result;
            if (p == regex.Length)
                result = true;
            else if (p == regex.Length - 1 && regex[p] == '$')
                result = t == s.Length;
            else
            {
                bool fits = t < s.Length && (regex[p] == '.' || regex[p] == s[t]);
                result = p + 1 < regex.Length && regex[p + 1] == '*'
                    ? Match(p + 2, t) || (fits && Match(p, t + 1))
                    : fits && Match(p + 1, t + 1);
            }
            memo[(p, t)] = result;
            return result;
        }
        if (anchored)
            return Match(first, 0);
        for (int start = 0; start <= s.Length; start++)
            if (Match(first, start))
                return true;
        return false;
    }
}
