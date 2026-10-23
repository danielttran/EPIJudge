using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<string> PermutationsWithDuplicates(string text)
    {
        int[] counts = new int[26];
        foreach (char c in text)
            ++counts[c - 'a'];
        char[] buffer = new char[text.Length];
        var result = new List<string>();
        void Visit(int depth)
        {
            if (depth == buffer.Length)
            {
                result.Add(new string(buffer));
                return;
            }
            for (int letter = 0; letter < 26; ++letter)
            {
                if (counts[letter] > 0)
                {
                    --counts[letter];
                    buffer[depth] = (char)('a' + letter);
                    Visit(depth + 1);
                    ++counts[letter];
                }
            }
        }
        Visit(0);
        return result;
    }
}
