using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public bool MatchesPattern(string pattern, string text)
    {
        if (pattern.Length == 0)
            return text.Length == 0;
        int countA = 0;
        foreach (char symbol in pattern)
            if (symbol == 'a')
                ++countA;
        int countB = pattern.Length - countA, maximum = countA == 0 ? 0 : text.Length / countA;
        for (int lengthA = 0; lengthA <= maximum; ++lengthA)
        {
            int remaining = text.Length - countA * lengthA;
            if (countB == 0 ? remaining != 0 : remaining % countB != 0)
                continue;
            int lengthB = countB == 0 ? 0 : remaining / countB;
            string? a = null, b = null;
            int offset = 0;
            bool valid = true;
            foreach (char symbol in pattern)
            {
                int length = symbol == 'a' ? lengthA : lengthB;
                string? part = text.Substring(offset, length);
                if (symbol == 'a')
                {
                    if (a == null)
                        a = part;
                    else if (a != part)
                    {
                        valid = false;
                        break;
                    }
                }
                else
                {
                    if (b == null)
                        b = part;
                    else if (b != part)
                    {
                        valid = false;
                        break;
                    }
                }
                offset += length;
            }
            if (valid && offset == text.Length)
                return true;
        }
        return false;
    }
}
