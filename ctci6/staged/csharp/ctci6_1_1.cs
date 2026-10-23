using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public bool IsUnique(string text)
    {
        bool[] seen = new bool[128];
        for (int i = 0; i < text.Length; ++i)
        {
            int code = text[i];
            if (seen[code])
                return false;
            seen[code] = true;
        }
        return true;
    }
}
