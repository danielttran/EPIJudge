using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<string> PermutationsDistinct(string text)
    {
        char[] chars = text.ToCharArray();
        var result = new List<string>();
        void Visit(int depth)
        {
            if (depth == chars.Length)
            {
                result.Add(new string(chars));
                return;
            }
            for (int i = depth; i < chars.Length; ++i)
            {
                char temporary = chars[depth];
                chars[depth] = chars[i];
                chars[i] = temporary;
                Visit(depth + 1);
                temporary = chars[depth];
                chars[depth] = chars[i];
                chars[i] = temporary;
            }
        }
        Visit(0);
        return result;
    }
}
